import argparse
from os import path
import sys
import marian_library.errant_tools.align_text as align_text
import marian_library.errant_tools.cat_rules as cat_rules
import marian_library.errant_tools.toolbox as toolbox
from marian_library.string_converter import Converter
from nltk.stem.lancaster import LancasterStemmer
from pathlib import Path


class GramError:
    """
    Wrapper for ERRANT error classification
    For ref see:
        https://github.com/chrisjbryant/errant
    No changes have been made to ERRANT source files (copied to this repo).
    """

    def __init__(self, nlp=None, merge="all-split", lev=None):

        self.nlp = nlp

        if not self.nlp:
            import spacy

            self.nlp = spacy.load("en_core_web_sm")

        self.stemmer = LancasterStemmer()
        self.converter = Converter(self.nlp)

        this_file_dir = path.dirname(path.abspath(__file__))
        self.data_dir = path.join(this_file_dir, "data")

        self.gb_spell = toolbox.loadDictionary(
            path.join(self.data_dir, "en_GB-large.txt")
        )
        self.tag_map = toolbox.loadTagMap(path.join(self.data_dir, "en-ptb_map"))

        self.opts = argparse.Namespace()
        d = vars(self.opts)
        d["merge"] = merge
        d["lev"] = None

    def __call__(self, orig_sent, cor_sent):
        """
        Compares orig_sent with cor_sent (gramatically corrected orig sent),
        ouputs differences (edits, grammar errors) with assigned error categories.
        see: parallel_to_m2.py
        Args:
            orig_sent: tokenized original sentence, input for grammar correction system
            cor_sent: tokenized sentence, result of grammar correction of orig_sent
            custom_apply_spacy: ERRANT was orignally designed to run against CoNLL-2014, which has the
                strange property that input is a tokenized string, in between a string and a list of tokens.
                ex:
                    string = "I'd've done it differently"
                    tokenized_string = "I 'd 've done it differently"
                    tokens = ["I", "'d", "'ve", "done", "it", "differently"]
                because of this partial tokenization, ERRANT originally tokenized using toolbox.applySpacy
                which raises an exception if there are extra whitespace characters.
                This option is retained for backward compatibility, but may not be necessary
        Returns:
            edits: list (original errant format)
            0 - edit start word id
            1 - edits end word id (exclusive)
            2 - corrected sting
            3 - correction start word id
            4 - correction end word id
        """
        edits = []
        proc_orig = self.converter.to_spacy(orig_sent.strip())
        proc_cor = self.converter.to_spacy(cor_sent.strip())
        if proc_orig != proc_cor:

            auto_edits = align_text.getAutoAlignedEdits(proc_orig, proc_cor, self.opts)
            for auto_edit in auto_edits:
                cat = cat_rules.autoTypeEdit(
                    auto_edit,
                    proc_orig,
                    proc_cor,
                    self.gb_spell,
                    self.tag_map,
                    self.nlp,
                    self.stemmer,
                )
                auto_edit[2] = cat
                edits.append(auto_edit)
        return edits
