#!/usr/bin/env python

from corpus_based_construct import *
from corpus_based import SuggestWithCorpus, select_relevant_contexts, score_context
from data_prep import preprocess_sent


def test_preprocess_sent():
	s = "I live in New York City"
	assert preprocess_sent(s) == ["live", "new", "york", "city"]
	s = "How old are you ?"
	assert preprocess_sent(s) == ["how", "old"]
	s = "apples, pears and oranges"
	assert preprocess_sent(s) == ["apple", "pear", "orange"]
	s = "let's run a race together!"
	assert preprocess_sent(s) == ["let", "'s", "run", "race", "together"]


def test_clean_enron_message_plain():
	s = "First sentence.\nSecond sentence."
	assert clean_enron_message(s) == s


def test_clean_enron_message():
	s = "Subject: The subject"
	assert not clean_enron_message(s)
	s = "----------------------Forwarded message"
	assert not clean_enron_message(s)
	s = "> re 'Hello'"
	assert clean_enron_message(s) == " re 'Hello'"
	s = "Thanks"
	assert not clean_enron_message(s)
	s = "I wanted to\nthank you for your help"
	assert clean_enron_message(s) == "I wanted to thank you for your help"
	s = "This Is A Title"
	assert not clean_enron_message(s)
	s = "from pierrelidia@gmail.com"
	assert not clean_enron_message(s)
	s = "please call +331 234 567 89"
	assert not clean_enron_message(s)
	s = "Eat. Sleep. Repeat"
	assert not clean_enron_message(s)
	s = "The dog eats. The cat sleeps."
	assert clean_enron_message(s) == "The dog eats.\nThe cat sleeps."


def test_assemble_cut_sentences():
	lines = ["First sentence. Second sentence."]
	assert assemble_cut_sentences(lines) == lines
	lines = ["I wanted to", "thank you for you help"]
	assert assemble_cut_sentences(lines) == ["I wanted to thank you for you help"]
	lines = ["Hi", "Anna"]
	assert assemble_cut_sentences(lines) == lines
	lines = ["Hi Anna", "how are you ?", "See you soon"]
	assert assemble_cut_sentences(lines) == ["Hi Anna how are you ?", "See you soon"]


def test_get_all_synonyms():
	syn_dict = {"w1": ["s11", "s12"]}
	result = get_all_synonyms(syn_dict)
	assert set(result) == set(["s11", "s12"])
	syn_dict["w2"] = ["s21", "s22"]
	result = get_all_synonyms(syn_dict)
	assert set(result) == set(["s11", "s12", "s21", "s22"])
	syn_dict["w3"] = ["s11", "s31"]
	result = get_all_synonyms(syn_dict)
	assert len(result) == 5


def test_build_context():
	s1 = ["first", "sentence"]
	s2 = ["second", "sentence"]
	l = [s1, s2]
	assert not build_context("test", l)
	assert build_context("first", l) == ["sentence"]
	assert build_context("sentence", l) == ["first", "second"]


def test_extract_context_from_sent():
	word = "run"
	s_tok = ["I", "want", "to", "run", "in", "the", "race"]
	assert len(extract_context_from_sent(word, s_tok)) == 6
	s_tok = ["want", "to", "run", "in", "the", "race"]
	assert len(extract_context_from_sent(word, s_tok)) == 5
	s_tok = ["I", "want", "to", "run"]
	assert len(extract_context_from_sent(word, s_tok)) == 3
	s_tok = ["run", "the", "race"]
	assert len(extract_context_from_sent(word, s_tok)) == 2


def test_trace_back_syn():
	syn_dict = {"w1": ["a", "b", "c"], "w2": ["b", "d"]}
	assert not trace_back_syn("e", syn_dict)
	assert trace_back_syn("a", syn_dict) == ["w1"]
	assert set(trace_back_syn("b", syn_dict)) == set(["w1", "w2"])


def test_select_relevant_contexts():
	syn_dict = {"w1": ["a", "b", "c"], "w2": ["b", "d"], "w3": ["e", "f", "g"]}
	syn_list = [["a", "aa", "aaa"], ["b", "bb", "bbb"], ["d", "dd", "ddd"], ["e", "ee", "eee"]]
	result = select_relevant_contexts("w1", syn_dict, syn_list)
	assert result == [["a", "aa", "aaa"], ["b", "bb", "bbb"]]
	result = select_relevant_contexts("w2", syn_dict, syn_list)
	assert result == [["b", "bb", "bbb"], ["d", "dd", "ddd"]]
	result = select_relevant_contexts("w3", syn_dict, syn_list)
	assert result == [["e", "ee", "eee"]]


def test_score_context():
	new = ["a", "b", "c"]
	assert score_context(new, ["d"]) == 0
	assert score_context(new, ["a"]) == 1
	assert score_context(new, ["a", "b"]) == 2
	ref = ["a", "a", "e"]
	assert score_context(new, ref) == 2


def test_select_synonym_with_context_no_word():
	s = SuggestWithCorpus(dict(), 'n', [])
	assert not s.select_synonym_with_context("word", "test sentence")


def test_select_synonym_with_context_no_context():
	sentence = "word in a test sentence"
	syn_dict = {"word": ["term", "quarrel"]}
	s = SuggestWithCorpus(syn_dict, 'n', [])
	assert not s.select_synonym_with_context("word", sentence)


def test_select_synonym_with_context_single_context():
	sentence = "word in a test sentence"
	syn_dict = {"word": ["term", "quarrel"]}
	context_list = [["term", "your", "speaking", "good"]]
	s = SuggestWithCorpus(syn_dict, 'n', context_list)
	result = s.select_synonym_with_context("word", sentence)
	assert result == ["term", "word"]


def test_select_synonym_with_context_null():
	sentence = "word in a test sentence"
	syn_dict = {"word": ["term", "quarrel"]}
	context_list = [["term", "your", "speaking", "good"], ["quarrel", "father", "with", "her"]]
	s = SuggestWithCorpus(syn_dict, 'n', context_list)
	result = s.select_synonym_with_context("word", sentence)
	assert not result


def test_select_synonym_with_context():
	sentence = "word in a test sentence"
	syn_dict = {"word": ["term", "quarrel"]}
	context_list = [["term", "your", "speaking", "good", "sentence"], ["quarrel", "father", "with", "her"]]
	s = SuggestWithCorpus(syn_dict, 'n', context_list)
	result = s.select_synonym_with_context("word", sentence)
	assert result == ["term"]
