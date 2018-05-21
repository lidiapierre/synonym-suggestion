#!/usr/bin/env python

import json
import string
from collections import defaultdict
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


syn_dict_n_file = "syn_dict.json"

wnl = WordNetLemmatizer()


with open(syn_dict_n_file) as f:
    syn_data_import = json.load(f)

syn_dict_n = defaultdict(list, syn_data_import)


def get_syn_dict(pos):
	if pos == 'n':
		return syn_dict_n
	else:
		return defaultdict(list)


def preprocess_sent(line):
	# lemmatize
	tokens = [wnl.lemmatize(i,j[0].lower()) if j[0].lower() in ['a','n','v'] else wnl.lemmatize(i) for i,j in pos_tag(word_tokenize(line))]
	# strip punctuation and stopwords
	tokens = [t for t in tokens if (t not in string.punctuation and t not in stopwords.words('english'))]
	# remove tokens of 1 letter
	tokens = [t for t in tokens if len(t) > 1]
	# lowercase
	tokens = [t.lower() for t in tokens]
	return tokens


def preprocess_syn_dict():
	""" TEMP """
	with open("synonyms_context_sensitive.json") as f:
		data = json.load(f)

	preprocessed_data = dict()
	for k in data:
		new_list = list(set([wnl.lemmatize(syn, 'n') for syn in data[k]]))
		if k in new_list:
			new_list.remove(k)
		if len(new_list) > 1:
			preprocessed_data[k] = new_list
	with open(syn_dict_n_file, 'w') as f:
		json.dump(preprocessed_data, f)


def add_extra_syn_to_dict(df, pos):
	""" TEMP 
	add synonyms to a dict from a test dataframe"""
	syn_dict = get_syn_dict(pos)
	for index, row in df.iterrows():
		source = row['source']
		target = row['target']
		if row['pos'] == pos and target not in syn_dict[source]:
			syn_dict[source].append(target)
	return syn_dict


if __name__ == "__main__":
	preprocess_syn_dict()

	
