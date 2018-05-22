#!/usr/bin/env python

import csv

from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
from data_prep import get_syn_dict, preprocess_sent


def get_potential_synsets(source, syn_dict, pos):
	# TODO map syn dict to POS
	ss_list = []
	for ss in wn.synsets(source, pos=pos):
		for l in ss.lemma_names():
			if l in syn_dict[source]:
				ss_list.append(ss)
				break
	return ss_list


def select_synonym_with_wn(source, sentence, syn_dict, pos):
	# TODO map syn dict to pos
	list_ss = get_potential_synsets(source, syn_dict, pos)
	if not list_ss:
		return []
	elif len(list_ss) == 1:
		# only choice --> meaningless, return result anyway + source
		lemmas = [l for l in list_ss[0].lemma_names() if l in syn_dict[source]]
		return lemmas + [source]
	else:
		ss = lesk(sentence, source, synsets=list_ss)
		lemmas = [l for l in ss.lemma_names() if l in syn_dict[source]]
		return lemmas


def get_syn_without_syn_dict(source, sentence):
	# just for comparison: get synonyms with wordnet without the syn dict constraint
	ss = lesk(sentence, source)
	lemmas = [l for l in ss.lemma_names() if l != source]
	return lemmas or [source]


def create_test_set():
	syn_dict = get_syn_dict('n')
	with open("data/test_set_wn.csv", 'w+') as csvfile:
		wr = csv.writer(csvfile)
		for word in syn_dict:
			entries = get_sentences_for_word(word, syn_dict, 'n')
			if entries:
				wr.writerows(entries)
	return

	
def get_sentences_for_word(word, syn_dict, pos):
	result = []
	clear = False
	for ss in wn.synsets(word, pos=pos):
		ss_added = False
		for lemma in ss.lemma_names():
			if lemma in syn_dict[word]:
				ss_added = True
				for sent in ss.examples():
					if word in preprocess_sent(sent):
						row = [word, sent, lemma, pos]
						result.append(row)
		if not ss_added and not clear:
			for sent in ss.examples():
				if word in preprocess_sent(sent):
					clear = True
					result.append([word, sent, word, pos])
					break
	if len(result) > 1:
		return result
	else:
		return []
		


if __name__ == "__main__":
	create_test_set()
