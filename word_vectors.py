#!/usr/bin/env python

import spacy

nlp = spacy.load('en_core_web_md')

from corpus_based_construct import extract_context_from_sent
from data_prep import preprocess_sent


def select_synonym_with_vectors(word, sentence, syn_dict, pos):
	s_tok = preprocess_sent(sentence)
	if word not in s_tok:
		return
	context_v = nlp(u" ".join(extract_context_from_sent(word, s_tok)))
	scores_d = dict()
	for syn in syn_dict[word]:
		scores_d[syn] = context_v.similarity(nlp(syn))

	result = max(scores_d, key=scores_d.get)
	# suggest synonym only if score high enough
	if scores_d[result] > 0.3:
		return result
	else:
		return
	