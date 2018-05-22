#!/usr/bin/env python

import csv
import time
from collections import Counter

from corpus_based_construct import get_context_file, extract_context_from_sent
from data_prep import get_syn_dict, preprocess_sent


class SuggestWithCorpus:
	def __init__(self, syn_dict, pos, context_list=None):
		self.syn_dict = syn_dict
		self.pos = pos
		if not context_list:
			with open(get_context_file(pos), 'rb') as csvfile:
				rd = csv.reader(csvfile)
				self.context_list = list(rd)
		else:
			self.context_list = context_list

	def select_synonym_with_context(self, word, sentence):
		# preprocess new sentence and get list of tokens
		s_tok = preprocess_sent(sentence)
		if word not in s_tok:
			return []
		
		choices = select_relevant_contexts(word, self.syn_dict, self.context_list)
		if not choices:
			# no contexts found for list of word synonym
			return []
		if len(choices) == 1:
			# only one potential synonym to be picked --> meaningless, return the source as well
			result = choices[0][0]
			return [result, word]
		# get new context
		new_context = extract_context_from_sent(word, s_tok)
		# build dict of all syn and their score
		scores_d = dict()
		for row in choices:
			syn, context = row[0], row[1:]
			s = score_context(new_context, context)
			# don't keep null scores
			if s > 0:
				scores_d[syn] = s
		result = [k for k, v in scores_d.items() if v == max(scores_d.values())]
		return result


def select_relevant_contexts(syn, syn_dict, syn_list):
	result = []
	if syn not in syn_dict:
		return
	
	for row in syn_list:
		if row[0] in syn_dict[syn]:
			result.append(row)
	return result


def score_context(new, ref):
	# ref is a list of context words
	score = 0
	# count occurences of words in ref context
	counter = Counter(ref)
	for el in new:
		if el in counter:
			score += counter[el]
	return score
		

#if __name__ == "__main__":
