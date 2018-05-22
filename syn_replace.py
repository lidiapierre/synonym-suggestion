#!/usr/bin/env python

import time
import pandas as pd
from knowledge_based import select_synonym_with_wn
from corpus_based import SuggestWithCorpus
from word_vectors import select_synonym_with_vectors
from data_prep import get_syn_dict


#test_file = "data/test_set.csv"
test_file = "data/test_set_wn.csv"


def evaluate_corpus_replace(data, syn_dict, pos, display=False):
	s = SuggestWithCorpus(syn_dict, pos)
	suggestions = 0
	correct = 0
	for index, row in data.iterrows():
		sent = row['sentence']
		source = row['source']
		target = row['target']
		result = s.select_synonym_with_context(source, sent)
		if display:
			print sent
			print "<" + source + ">: " + ", ".join(syn_dict[source])
			print "    result: {0}".format(", ".join(result))
			print "    expected result: {0}".format(target)
			print "#####"
		if result:
			suggestions += 1
		if target in result and source not in result:
			correct += 1
	
	return suggestions, correct


def evaluate_wordnet_replace(data, syn_dict, pos, display=False):
	suggestions = 0
	correct = 0
	for index, row in data.iterrows():
		sent = row['sentence']
		source = row['source']
		target = row['target']
		result = select_synonym_with_wn(source, sent, syn_dict, pos)
		if display:
			print sent
			print "<" + source + ">: " + ", ".join(syn_dict[source])
			print "    result: {0}".format(", ".join(result))
			print "    expected result: {0}".format(target)
			print "#####"
		if result:
			suggestions += 1
		if target in result and source not in result:
			correct += 1
	
	return suggestions, correct


def evaluate_wordvectors_replace(data, syn_dict, pos, display=False):
	suggestions = 0
	correct = 0
	for index, row in data.iterrows():
		sent = row['sentence']
		source = row['source']
		target = row['target']
		result = select_synonym_with_vectors(source, sent, syn_dict, pos)
		if display:
			print sent
			print "<" + source + ">: " + ", ".join(syn_dict[source])
			print "    result: {0}".format(result)
			print "    expected result: {0}".format(target)
			print "#####"
		if result:
			suggestions += 1
		if target == result:
			correct += 1
	return suggestions, correct


if __name__ == "__main__":
	data = pd.read_csv(test_file, names=['source', 'sentence', 'target', 'pos'])
	syn_dict = get_syn_dict('n')
	test_sentences = pd.DataFrame([], columns=['source', 'sentence', 'target', 'pos'])
	for index, row in data.iterrows():
	# attention: target can be source !
	# ######
		if row['source'] in syn_dict and row['target'] in syn_dict[row['source']] and row['pos'] == 'n':
			test_sentences.loc[index] = row
	
	total = len(test_sentences.index)

	#suggestions, correct = evaluate_corpus_replace(test_sentences, syn_dict, 'n', display=False)
	#suggestions, correct = evaluate_wordnet_replace(test_sentences, syn_dict, 'n', display=True)
	suggestions, correct = evaluate_wordvectors_replace(test_sentences, syn_dict, 'n', display=False)

	print "coverage {0}%".format(float(suggestions) * 100 / total)
	print "accuracy {0}%".format(float(correct) * 100 / total)
	print "precision {0}%".format(float(correct) * 100 / suggestions)
