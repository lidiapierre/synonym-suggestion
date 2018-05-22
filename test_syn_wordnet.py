#!/usr/bin/env python

from knowledge_based import get_potential_synsets, select_synonym_with_wn


def test_get_potential_synsets_none():
	source = "plant"
	syn_dict = {"plant": []}
	result = get_potential_synsets(source, syn_dict, 'n')
	assert not result


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


def test_select_synonym_with_wn_unknown():
	result = select_synonym_with_wn("unknown_word", "test sentence", dict(), 'n')
	assert not result
	

def test_select_synonym_with_wn_single():
	source = "relation"
	syn_dict = {"relation": ["telling", "respect"]}
	result = select_synonym_with_wn(source, "test sentence", syn_dict, 'n')
	assert len(result) == 2
	assert source in result


def test_select_synonym_with_wn():
	source = "hazard"
	syn_dict = {"hazard": ["chance", "risk"]}
	sentence = "we can form no calculation concerning the laws of hazard"
	result = select_synonym_with_wn(source, sentence, syn_dict, 'n')
	assert result
	assert source not in result
	