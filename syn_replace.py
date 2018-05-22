#!/usr/bin/env python

import time
import pandas as pd
from knowledge_based import select_synonym_with_wn
from corpus_based import select_synonym_with_context, load_context_file
from data_prep import get_syn_dict


test_file = "test_set.csv"


if __name__ == "__main__":
	data = pd.read_csv(test_file, names=['source', 'sentence', 'target', 'pos'])
	syn_dict = get_syn_dict('n')
	total = 0
	out_1 = 0
	out_2 = 0
	ok_1 = 0
	ok_2 = 0
	context_list = load_context_file('n')
	syn_dict = get_syn_dict('n')
	for index, row in data.iterrows():
		sent = row['sentence']
		source = row['source']
		target = row['target']
		pos = row['pos']
		if source in syn_dict and target in syn_dict[source] and pos == 'n':
			total += 1
			r1 = select_synonym_with_wn(source, sent, syn_dict, 'n')
			r2 = select_synonym_with_context(source, sent, syn_dict, 'n', context_list)
			if r1:
				out_1 += 1
				if target in r1 and source not in r1:
					ok_1 += 1
			if r2:
				out_2 += 1
				if target in r2 and source not in r2:
					ok_2 += 1
			#if r2:
			#	print sent
			#	print "<" + source + ">: " + ", ".join(syn_dict[source])
			#	print "    result with wordnet: {0}".format(", ".join(r1))
			#	print "    result with corpus: {0}".format(", ".join(r2))
			#	print "    expected result: {0}".format(target)
			#	print "#####"
	print "precision wordnet {0}%, corpus {1}%".format(float(ok_1) * 100 / out_1, float(ok_2) * 100 / out_2)
	print "accuracy wordnet {0}%, corpus {1}%".format(float(ok_1) * 100 / total, float(ok_2) * 100 / total)
	print "coverage wordnet {0}%, corpus {1}%".format(float(out_1) * 100 / total, float(out_2) * 100 / total)

