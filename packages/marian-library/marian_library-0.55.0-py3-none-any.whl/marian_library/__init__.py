import argparse
import json
import re
from os.path import join

from functional import seq
from marian_library.gramer import GramError
from marian_library.string_converter import Converter
from marian_client import MarianClient

from quote_manager import Quotes

class Grammar:
    def __init__(self, marian_host, port=80, nlp=None, spacy_output=False):

        self.nlp = nlp

        if not self.nlp:
            import spacy

            self.nlp = spacy.load("en_core_web_sm")

        self.spacy_output = spacy_output
        self.converter = Converter(self.nlp)
        self.gram_error = GramError(nlp=self.nlp)
        self.marian_gec = MarianClient(HOST=marian_host, PORT=port, timeout=10)
        self.contr_dict = {
            " 've ": "'ve ",
            " 're ": "'re ",
            " 'm ": "'m ",
            " 's ": "'s ",
            " 'd ": "'d ",
            " 'll ": "'ll ",
            " n't ": "n't "
        }
        self.build_contr_dict()

    def build_contr_dict(self):
        full_contr_dict = self.contr_dict.copy()
        for k, v in self.contr_dict.items():
            for q in Quotes.singles:
                full_contr_dict[k.replace("'", q)] = v.replace("'", q)
        self.contr_dict = full_contr_dict

    def get_pred(self, tokenized_sent: str):
        """
        Prediction tokenized_sentence.
        Args:
            tokenized_sent: string
        Returns:
            Predicted sentence (grammatically corrected) if suceess
            Input sentence otherwise
        """
        success, tokenized_corrected_sentence, _ = self.marian_gec(tokenized_sent)
        if not success:
            tokenized_corrected_sentence = tokenized_sent
        return tokenized_corrected_sentence

    def format_edits(self, edits_in, leading_signs):
        """
        Format edits to match qai issue formatting.
        Args:
            edits: output error categories from gram_error
        Returns:
            List of dictionaries with keys:
            - from - starting word,
            - until - ending word
            - editType - error type (see: https://github.com/chrisjbryant/errant)
            - suggestions - corrected error string
        """

        leading_token_len = len(self.converter.to_spacy(leading_signs))

        edits_out = []
        for edit_in in edits_in:
            edit_out = {}
            edit_out["token_from"] = edit_in[0] + leading_token_len
            edit_out["token_until"] = edit_in[1] + leading_token_len
            edit_out["editType"] = edit_in[2]

            edit_out["correction"] = self.converter.contract_text(edit_in[3])

            edits_out.append(edit_out)
        return edits_out

    def align_output(self, line, tokenized_pred_line, edits, leading_signs):
        """
        - Detokenizes output sentences
        - Corrects the output by remembered leading signs
        Args:
            - tokenized_line: model input string
            - tokenized_pred_line: model output string
            - edits: gram_error output
        Returns:
            Dictionary with keys:
            - text: input sentence doc
            - corrected_text: corrected sentence doc
            - edits - list of dictionaries with keys:
                - token_from: error start token
                - token_until: error end token -1
                - correction: suggested correction string
                - editType: ERRANT error category
        """

        token_edits = self.format_edits(edits, leading_signs)
        line_doc = self.converter.to_spacy(line)
        pred_line = self.converter.to_detokenized_text(tokenized_pred_line)
        full_pred_line = leading_signs + pred_line
        pred_line_doc = self.converter.to_spacy(full_pred_line)

        item = {}
        item["text"] = line_doc
        item["corrected_text"] = pred_line_doc
        item["edits"] = token_edits

        return item

    def extend_span(self, segment_span, edit, replaced):
        """
        If error_type is insertion, error_span is '',
        Extension means appending adjacent token to error_span
        but only if its not being replaced by other edits(self.replaced).
        """
        sep = " "

        if "PUNCT" in edit["editType"].split(":"):
            sep = ""

        span = edit["span"]
        correction = edit["correction"]

        # last word - insertion at the end
        if span.start == len(segment_span) and span.end == len(segment_span):
            span = segment_span[-1:]
            correction = sep.join([span.text, correction]).strip()

        # first word
        elif span.start == 0:
            span = segment_span[:1]
            correction = sep.join([correction, span.text]).strip()

        # has non replaced preceeding token
        elif not replaced[span.start - 1]:
            span = segment_span[span.start - 1 : span.start]
            correction = sep.join([span.text, correction]).strip()

        # has non replaced suceeding token
        elif span.start < len(segment_span) - 1:
            if not replaced[span.start + 1]:
                span = segment_span[span.start : span.start + 1]
                correction = sep.join([correction, span.text]).strip()

        # fallback case - highlight previous
        else:
            span = segment_span[span.start - 1 : span.start]
            correction = sep.join([span.text, correction]).strip()

        return span, correction

    # currently not used, moved to service.gec
    def merge_adjacent_suggestions(self, out):
        text = out["text"]
        edits = out["edits"]

        edits = seq(edits).sorted(key=lambda e: e["until"]).list()

        # Merge adjacent suggestions
        edits_merged = []
        for edit in edits:

            merged = False

            for m_edit in edits_merged:
                if (m_edit["until"] + 1 == edit["from"]) or (
                    m_edit["until"] == edit["from"]
                ):

                    merged = True

                    if m_edit["until"] + 1 == edit["from"]:
                        m_edit["correction"] = (
                            m_edit["correction"] + " " + edit["correction"]
                        ).strip()
                    elif m_edit["until"] == edit["from"]:
                        m_edit["correction"] = (
                            m_edit["correction"] + edit["correction"]
                        ).strip()

                    m_edit["until"] = edit["until"]
                    m_edit["editType"] = "R:OTHER"

                    edit_span = text.char_span(m_edit["from"], m_edit["until"])

                    if edit_span:
                        m_edit["span"] = edit_span

            if not merged:
                edits_merged.append(edit)

        out["edits"] = edits_merged
        return out
    
    # currently not used, moved to service.gec
    def merge_contractions(self, out):
        text = out["text"]
        edits = out["edits"]

        # merge succeeding
        for edit in edits:
            """
            if tokenization respects word boundaries next sign is " "
            if next token is contraction ie:
            ie starts with "n": n't
            or starts with "'": 's, 'd, 'll
            """
            # if there is next sign
            if edit["until"] < len(text.text):
                
                contraction_starts = ["n", "'"] + Quotes.singles

                # if next sign starts a contraction ie. no break, "n" or "'"
                if text.text[edit["until"]] in contraction_starts:
                    succeeding_words = text.text[edit["until"] :].split()

                    if len(succeeding_words):
                        missing_token = succeeding_words[0]
                        edit["until"] = edit["until"] + len(missing_token)
                        edit["span"] = text.char_span(edit["from"], edit["until"])
                        edit["correction"] = edit["correction"] + missing_token

        # merge precceeding
        for edit in edits:
            """
            if tokenization respects word boundaries next sign is " "
            if the token starts with "n'" or "'"
            means we should merge prev token
            """

            contraction_ends = Quotes.singles + ['n' + q for q in Quotes.singles]

            def is_contraction_end(text):
                for e in contraction_ends:
                    if text.startswith(e):
                        return True
                return False

            # if there is prev sign
            if edit["from"] > 0 and hasattr(edit["span"], "text"):
                if is_contraction_end(edit["span"].text):
                    precceeding_words = text.text[: edit["from"]].split()
                    
                    if len(precceeding_words):
                        missing_token = precceeding_words[-1]
                        edit["from"] = edit["from"] - len(missing_token)
                        edit_span = text.char_span(edit["from"], edit["until"])
                        # char_span returns None if character indices don’t map to a valid span
                        # if this fails, we return prev span and correction
                        if edit_span:
                            edit["span"] = edit_span
                            edit["correction"] = missing_token + edit["correction"]

        out["edits"] = edits

        return out

    # currently not used, moved to service.gec
    def extend_multitoken_suggestions(self, out):
        """
        1. Extends contraction suggestions (error type: mapped from the original suggestion)
        2. Merges adjacent suggestions (error type: R:OTHER)
        """
        # merge adjacent
        out = self.merge_adjacent_suggestions(out)

        # merge contractions
        # we are safe since adjacent edits aren't suggestions
        out = self.merge_contractions(out)

        # merge again, adjacency has changed
        out = self.merge_adjacent_suggestions(out)

        return out

    def mark_replaced(self, segment_span, edits):
        """
        Mark words to be replaced.
        Used when spans are extended (insertion error) to avoid overlapping spans.
        """
        replaced = [False] * len(segment_span)
        for edit in edits:
            span = edit["span"]
            for i in range(span.start, span.end):
                replaced[i] = True
        return replaced

    def format_output(self, aligned_item):
        """
        - Calculates char offsets (instead of token offsets).
        - if spacy_output - text, corrected text and span are spaCy spans
        Args:
            - aligned_item - output from align_output
        Returns:
            Dictinary with keys:
            - text - input text (or spacy doc)
            - corrected_text - output corrected text (or spacy doc)
            - edits - list of dictinaries with keys:
                - span - detected error string (or spacy span)
                - from - span start char
                - until - span end char -1
                - correction - suggested correction string
                - editType - ERRANT error category
        """

        out = {}

        text = aligned_item["text"].text
        corrected_text = aligned_item["corrected_text"].text

        text_doc = self.converter.to_spacy(text)
        corrected_text_doc = self.converter.to_spacy(corrected_text)

        edits_out = []

        for edit in aligned_item["edits"]:
            edit_out = {}
            token_from = edit["token_from"]
            token_until = edit["token_until"]
            edit_out["span"] = text_doc[token_from:token_until]

            if token_from < len(text_doc):
                edit_out["from"] = text_doc[token_from].idx
            else:
                edit_out["from"] = len(text_doc.text)

            edit_out["until"] = edit_out["from"] + len(edit_out["span"].text)

            edit_out["correction"] = edit["correction"]
            edit_out["editType"] = edit["editType"]

            edits_out.append(edit_out)

        out["text"] = text_doc
        out["corrected_text"] = corrected_text_doc
        out["edits"] = edits_out

        replaced = self.mark_replaced(text_doc, out["edits"])

        for edit in out["edits"]:
            if len(edit["span"].text) == 0:
                edit["span"], edit["correction"] = self.extend_span(
                    text_doc, edit, replaced
                )
                edit["from"] = edit["span"][0].idx
                edit["until"] = edit["from"] + len(edit["span"].text)

        # moved to service.gec - cat based filtering before merging
        # out_merged = self.extend_multitoken_suggestions(out)
        out_merged = out

        if not self.spacy_output:
            out_merged["text"] = out_merged["text"].text
            out_merged["corrected_text"] = out_merged["corrected_text"].text

            for edit in out_merged["edits"]:
                edit["span"] = edit["span"].text

        return out_merged

    def filter_output(self, output):
        """
        Remove suggestions identical to errors, ie. noon -> noon
        """
        for edit in output["edits"]:
            span_text = edit["span"]
            if self.spacy_output:
                span_text = edit["span"].text
            if span_text == edit["correction"]:
                output["edits"].remove(edit)
        return output

    
    def detokenize_contractions(self, sent):
        regex = re.compile(
            "|".join(map(re.escape, self.contr_dict.keys()))
        )
        return regex.sub(lambda match: self.contr_dict[match.group(0)], sent)


    def __call__(self, sentences_arr):
        """
        Detects grammar errors in text, returns grammar edits.
        Args:
            sentences_arr: array of sentences
            ( we DO assume segments are sentences )
        Returns:
            out: dictionary with keys
            - text: input sentence text
            - corrected text: text after grammar corrections
            - edits: detected grammar corrections, for format ref see: format_edits
        """

        arr_out = []
        leading_signs_arr = []
        tokenized_sents = []

        for sent in sentences_arr:
            leading_signs_len = len(sent) - len(sent.lstrip())
            leading_signs = sent[:leading_signs_len]
            leading_signs_arr.append(leading_signs)

            sent_trimmed = sent.strip()
            tokenized_sent = self.converter.to_tokenized_text(sent_trimmed)
            tokenized_sents.append(tokenized_sent)

        # Batch Prediction - currently not used
        # pred_sents = self.get_pred(tokenized_sents)

        pred_sents = seq(tokenized_sents).map(lambda x: self.get_pred(x)).list()

        for i in range(len(sentences_arr)):

            edits = []

            # extract edits only if nonempty segment
            if len(tokenized_sents[i]):
                sent_detoken = self.detokenize_contractions(tokenized_sents[i])
                pred_detoken = self.detokenize_contractions(pred_sents[i])
                edits = self.gram_error(sent_detoken, pred_detoken)

            item = self.align_output(
                sentences_arr[i], pred_sents[i], edits, leading_signs_arr[i]
            )
            formatted_item = self.format_output(item)
            filtered_item = self.filter_output(formatted_item)

            # clear corrected text if enpty segments - possible noise
            if len(tokenized_sents[i]) == 0:
                filtered_item["corrected_text"] = ""

            arr_out.append(filtered_item)

        return arr_out