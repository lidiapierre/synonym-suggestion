#!/usr/bin/env python

from knowledge_based import get_potential_synsets
from corpus_based_construct import extract_context_from_sent


# Tests WordNet
def test_get_potential_synsets_n():
	source = "plant"
	syn_dict = {"plant": ["herb", "flora"]}
	result = get_potential_synsets(source, syn_dict, 'n')
	assert len(result) == 1


def test_get_potential_synsets_v():
	source = "plant"
	syn_dict = {"plant": ["set", "implant"]}
	result = get_potential_synsets(source, syn_dict, 'v')
	assert len(result) == 3

	
# Tests Corpus based version
def test_extract_context_from_sent():
	word = "run"
	s_tok = ["I", "want", "to", "run", "in", "the", "race"]
	assert len(extract_context_from_sent(word, s_tok)) == 6
	s_tok = ["want", "to", "run", "in", "the", "race"]
	assert len(extract_context_from_sent(word, s_tok)) == 5
	s_tok = ["I", "want", "to", "run"]
	assert len(extract_context_from_sent(word, s_tok)) == 3
	