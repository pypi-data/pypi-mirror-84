import re

from nltk import sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer

spacy_patterns = {
    "forward-slash": [{"IS_ALPHA": True}, {"ORTH": "/"}, {"IS_ALPHA": True}],
    "1-hyphen": [{"IS_ALPHA": True}, {"ORTH": "-"}, {"IS_ALPHA": True}],
    "2-hyphen": [
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
    ],
    "3-hyphen": [
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
    ],
    "4-hyphen": [
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
        {"ORTH": "-"},
        {"IS_ALPHA": True},
    ],
    "cannot": [{"LOWER": "can"}, {"LOWER": "not"}],
}


class Converter:
    def __init__(self, nlp):
        self.nlp = nlp
        self.patterns = spacy_patterns
        self.matcher = Matcher(self.nlp.vocab)
        self.tokenizer = Tokenizer(self.nlp.vocab)
        self.detokenizer = TreebankWordDetokenizer()

        self.load_patterns()

    def load_patterns(self):
        for label, pattern in self.patterns.items():
            self.matcher.add(label, None, pattern)

    def merge(self, doc):
        matched_spans = []
        matches = self.matcher(doc)
        for _, start, end in matches:
            span = doc[start:end]
            matched_spans.append(span)
        for span in matched_spans:
            span.merge()
        return doc

    def to_spacy(self, text):
        pre_doc = self.nlp(text)
        doc = self.merge(pre_doc)
        return doc

    def to_tokenized_text(self, text):
        doc = self.to_spacy(text)
        return " ".join([t.text for t in doc])

    def to_detokenized_text(self, text):
        """
        works only on complete sentences
        use contract text to detokenize sentence fragments
        """
        text_split = text.split(" ")
        return self.detokenizer.detokenize(text_split)

    def to_sentences(self, text):
        return sent_tokenize(text)

    @staticmethod
    def contract_text(string):
        """
        regexp based detokenizer
        """
        matches = re.search(r"\" .+? \"", string)
        if matches:
            normalized = matches.group(0).replace('" ', '"').replace(' "', '"')
            string = string.replace(matches.group(0), normalized)

        matches = re.search(r"\' .+? \'", string)
        if matches:
            normalized = matches.group(0).replace("' ", "'").replace(" '", "'")
            string = string.replace(matches.group(0), normalized)

        string = re.sub(r" %", "%", string)
        string = re.sub(r"£ ", "£", string)
        string = re.sub(r" :", ":", string)
        string = re.sub(r" ;", ";", string)
        string = re.sub(r" \.", ".", string)
        string = re.sub(r" \'m", "'m", string)
        string = re.sub(r" \'s", "'s", string)
        string = re.sub(r" \'ve", "'ve", string)
        string = re.sub(r" n\'t", "n't", string)
        string = re.sub(r" \'re", "'re", string)
        string = re.sub(r" \'d", "'d", string)
        string = re.sub(r" \'ll", "'ll", string)
        string = re.sub(r" ,", ",", string)
        string = re.sub(r" !", "!", string)
        string = re.sub(r"\( ", "(", string)
        string = re.sub(r" \)", ")", string)
        string = re.sub(r" \?", "?", string)
        string = re.sub(r"\s{2,}", " ", string)
        string = string.strip("\r\n").strip()

        return string
