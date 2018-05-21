#!/usr/bin/env python

from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

from data_prep import get_syn_dict
		

def get_potential_synsets(source, syn_dict, pos):
	ss_list = []
	for ss in wn.synsets(source, pos=pos):
		for l in ss.lemma_names():
			if l in syn_dict[source]:
				ss_list.append(ss)
				break
	return ss_list


def select_synonym_with_wn(source, sentence, pos):
	syn_dict = get_syn_dict(pos)
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


if __name__ == "__main__":
	source = "increase"
	sentence = "an increase of 28.3 per cent"
	print select_synonym_with_wn(source, sentence, 'n')