from typing import Tuple

import pytest
from marian_client.quote_manager import Quotes

from marian_library import Grammar
from marian_library.gramer import GramError

grammar = Grammar(marian_host="localhost", port="6000")

ge = GramError()

de_tokenizer_sent_pairs = [
    {
        "detokenized_text": "Modern technology is amazing, isn't it?",
        "tokenized_text": "Modern technology is amazing , is n't it ?",
    },
    {
        "detokenized_text": "You haven't been listening to a word I've said!",
        "tokenized_text": "You have n't been listening to a word I 've said !",
    },
    {
        "detokenized_text": "She's absolutely certain she's going to make it in the world.",
        "tokenized_text": "She 's absolutely certain she 's going to make it in the world .",
    },
    {
        "detokenized_text": "Hold on to your ticket - you'll need it later.",
        "tokenized_text": "Hold on to your ticket - you 'll need it later .",
    },
]


@pytest.mark.parametrize("pair", de_tokenizer_sent_pairs)
def test_detokenizer(pair):
    detokenized_text = grammar.converter.to_detokenized_text(pair["tokenized_text"])
    assert detokenized_text == pair["detokenized_text"], "It should detokenize."


@pytest.mark.parametrize("pair", de_tokenizer_sent_pairs)
def test_tokenizer(pair):
    tokenized_text = grammar.converter.to_tokenized_text(pair["detokenized_text"])
    assert tokenized_text == pair["tokenized_text"], "It should tokenize."


grammar_sent_pairs = [
    {
        "incorrect": "Anna and Mike is going skiing.",
        "corrected": "Anna and Mike are going skiing.",
        "error_type": "R:VERB:SVA",
    },
    {
        "incorrect": "Matt like fish.",
        "corrected": "Matt likes fish.",
        "error_type": "R:OTHER",
    },
    {
        "incorrect": "Matt   likes fish.",
        "corrected": "Matt likes fish.",
        "error_type": "U:SPACE",
    },
    {
        "incorrect": "It is raining when I got home last night.",
        "corrected": "It was raining when I got home last night.",
        "error_type": "R:VERB:TENSE",
    },
]


@pytest.mark.parametrize("pair", grammar_sent_pairs)
def test_gramm_errror(pair):
    edits = grammar.gram_error(pair["incorrect"], pair["corrected"])
    assert edits[0][2] == pair["error_type"], "It should classify errors."


@pytest.mark.parametrize("pair", grammar_sent_pairs)
def test_grammar(pair):
    corrected = grammar([pair["incorrect"]])[0]["corrected_text"]
    assert corrected == pair["corrected"], "It should correct grammar mistakes."


edit_pairs = [
    {
        "input": "He is cool",
        "output": "He are cool",
        "edits": [[1, 2, "R:VERB:SVA", "are", 1, 2]],
    },
    {
        "input": "he like runned",
        "output": "he likes running",
        "edits": [[1, 2, "R:OTHER", "likes", 1, 2], [2, 3, "R:SPELL", "running", 2, 3]],
    },
    {
        "input": "she went their",
        "output": "she went there",
        "edits": [[2, 3, "R:OTHER", "there", 2, 3]],
    },
    {
        "input": "We've sent you a couple of emails, but we hasn't heard back.",
        "output": "We've sent you a couple of emails, but we haven't heard back.",
        "edits": [[11, 12, "R", "have", 11, 12]],
    },
]


@pytest.mark.parametrize("edit", edit_pairs)
def test_gram_error(edit):
    assert ge(edit["input"], edit["output"]) == edit["edits"]


nonascii_quotes_pairs = [
    {
        "input": "Those’s ‘magic’ shoe.", 
        "span": "Those",
        "correction": "There",
        # changed - merging moved to service.gec
        # "span": "Those’s", 
        # "correction": "There’s"
    },
    {
        "input": "Please doesn’t skip your leg day.",
        "span": "does",
        "correction": "do",
        # changed - merging moved to service.gec
        # "span": "doesn’t",
        # "correction": "don’t",
    },
    {
        "input": "We’ve sent you a couple of emails, but we hasn’t heard back.",
        # changed - merging moved to service.gec
        # "span": "hasn’t",
        # "correction": "haven’t",
        "span": "has",
        "correction": "have",
    },
]


@pytest.mark.parametrize("pair", nonascii_quotes_pairs)
def test_gram_error(pair):
    output = grammar([pair["input"]])[0]
    edit = output["edits"][0]
    assert edit["correction"] == pair["correction"]
    assert edit["span"] == pair["span"]


smart_quotes = [
    "We’ve sent you a couple of emails, but we haven’t heard back.",
    "Yeah, he’d’ve done something ʻsmartʼ I guess.",
    "One of these customers calls in, saying, ‘I’m upset about a bad Yelp review I got and also I don’t understand how this part of my ads program is working.’",
    "You get another phone call and it’s a business that says something.",
    "They say, ‘Hey, I’d like to actually grow my business more and I’d like to spend more money.’",
]

change_words_not_quotes = [
    "We've sent you a couple of emails, but we haven't heard back.",
    "Yeah, she'll've said something 'intelligent' I suppose.",
    "A customers calls in and says, 'I'm not happy with a Yelp review I got and also I don't understand how this part of my ads program is working.'",
    "You get a second phone call and it's a company that says something.",
    "They say, 'I'd like to grow my business and I'd like to spend more money.'",
]

requoted = [
    "We’ve sent you a couple of emails, but we haven’t heard back.",
    "Yeah, she’ll’ve said something ʻintelligentʼ I suppose.",
    "A customers calls in and says, ‘I’m not happy with a Yelp review I got and also I don’t understand how this part of my ads program is working.’",
    "You get a second phone call and it’s a company that says something.",
    "They say, ‘I’d like to grow my business and I’d like to spend more money.’",
]


@pytest.mark.parametrize("text", smart_quotes)
def test_requote_no_change(text: str):
    q = Quotes(text)
    assert q.requote_modified_string(q.simplified) == q.orig


@pytest.mark.parametrize(
    "before_after_correct", list(zip(smart_quotes, change_words_not_quotes, requoted))
)
def test_text_change_but_same_quote_count(before_after_correct: Tuple[str, str, str]):
    before, after, correct = before_after_correct
    q = Quotes(before)
    assert q.requote_modified_string(after) == correct


changed_quote_cases = [
    (
        "Yeah , he’d’ve done something “intelligent”",
        'Yeah , he\'s done something "intelligent"',
        "Yeah , he’s done something “intelligent”",
    ),
    (
        "There are many storeʼs like that one , which Iʼm a fan of",
        "There are many stores like that one , which I'm a fan of",
        "There are many stores like that one , which Iʼm a fan of",
    ),
]


@pytest.mark.parametrize("before_after_correct", changed_quote_cases)
def test_change_quote_count(before_after_correct: Tuple[str, str, str]):
    before, after, correct = before_after_correct
    q = Quotes(before)
    assert q.requote_modified_string(after) == correct
