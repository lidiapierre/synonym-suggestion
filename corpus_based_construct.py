#!/usr/bin/env python

import csv
import time
from data_prep import get_syn_dict, preprocess_sent

enron_file = "enron-email-dataset/emails.csv"
enron_text_file = "enron_data.txt"
enron_text_preprocessed = "enron_data_preprocessed.txt"
missing_context_file = "no_context_syn"
max_context_file = "max_context_syn"


def get_context_file(pos):
	return "context_{0}.csv".format(pos)


def enron_data_to_text():
	""" extract text from enron csv data, writes all in a text file """
	f = open(enron_text_file,"w+")
	df = pd.read_csv(enron_file, nrows=10000)
	#df = load_enron_data_frame()
	for i, row in df.iterrows():
		message = row['message']
		text = clean_enron_message(message)
		if text:
			f.write(text + "\n")
	f.close()


def load_enron_data_frame():
	""" loads enron csv file """
	mylist = []
	for chunk in  pd.read_csv(enron_file,chunksize=20000):
		mylist.append(chunk)
	enron_data = pd.concat(mylist)
	del mylist
	return enron_data


def clean_enron_message(message):
	# split sentences on full stops
	message = message.replace(". ", ".\n")
	lines = message.split("\n")
	# clean forward symbols
	lines = [l.strip('>') for l in lines]
	lines = [l for l in lines if not "----------------------" in l]
	# remove headers
	lines = [l for l in lines if not l.split()[0].endswith(":")]
	# assemble cut sentences
	lines = assemble_cut_sentences(lines)
	# keep lines of more than 1 word
	lines = [l for l in lines if len(l.split()) > 1]
	# remove all capitals
	lines = [l for l in lines if not l.istitle()]
	# remove all lines with email addresses
	lines = [l for l in lines if not "@" in l]
	# remove all lines that contain digits
	lines = [l for l in lines if not any(char.isdigit() for char in l)]
	text = "\n".join(lines)
	return text


def assemble_cut_sentences(lines):
	if not lines:
		return []
	result = []
	l = lines[0]
	for i in range(len(lines) - 1):
		if lines[i+1][0].isupper():
			result.append(l)
			l = lines[i + 1]
		else:
			l += " " + lines[i + 1]
	if l:
		result.append(l)
	return result


def preprocess_enron_text():
	""" reads enron raw data file and writes preprocessed sentences to text file """
	outfile = open(enron_text_preprocessed,"w+")
	with open(enron_text_file) as f:
		index = 0
		for line in f:
			print "processing line {0}".format(index)
			index += 1
			tokens = preprocess_sent(line)
			outfile.write( " ".join(tokens)+ "\n")
	outfile.close()

	
def save_context_lists(pos):
	""" creates context lists csv files """
	with open(enron_text_preprocessed) as f:
		all_sentences = f.readlines()
	# remove duplicates
	all_sentences = set(list(all_sentences))
	# tokenize
	all_sentences_tok = [s.split() for s in all_sentences]
	all_syn = get_all_synonyms(get_syn_dict(pos))
	with open(get_context_file(pos), 'w+') as csvfile, open(missing_context_file + "_{0}.txt".format(pos), 'w+') as f1:
		wr = csv.writer(csvfile)
		for syn in all_syn:
			context = build_context(syn, all_sentences_tok)
			if context:
				wr.writerow([syn] + context)
			else:
				f1.write(syn + "\n")
	

def get_all_synonyms(syn_dict):
	syn_list = []
	for word in syn_dict:
		syn_list += syn_dict[word]
	# remove duplicates
	return list(set(syn_list))

	
def build_context(word, sentences_tok):
	context = []
	# select sentences that contain the synonym
	keep_sentences = [s for s in sentences_tok if word in s]
	for s in keep_sentences:
		context += extract_context_from_sent(word, s)
	return context


def extract_context_from_sent(word, s_tok):
	context = []
	i = s_tok.index(word)
	# get preceding
	j = 0 
	while (i > 0) and (j < 3):
		context.append(s_tok[i - 1])
		i -= 1
		j += 1
		
	# get following
	i = s_tok.index(word)
	j = 0 
	while (i < len(s_tok) - 1) and (j < 3):
		context.append(s_tok[i + 1])
		i += 1
		j += 1
	return context


def get_largest_syn(pos):
	""" TEMP extract synonyms with largest context for testing purposes """
	syn_dict = get_syn_dict(pos)
	s_list = []
	lg = []
	with open(get_context_file(pos), 'rb') as csvfile:
		rd = csv.reader(csvfile)
		for row in rd:
			if len(row) > 100:
				sources = trace_back_syn(row[0], syn_dict)
				for el in sources:
					s_list.append(el)
					lg.append([el] + row)

	with open(max_context_file + "_{0}.txt".format(pos), 'w+') as f:
		for entry in sorted(lg, key=lambda x: x[0]):
			if s_list.count(entry[0]) > 1:
				f.write(entry[0] + " -> " + entry[1] + ": " + ", ".join(entry[2:20]) + '\n')


def trace_back_syn(syn, syn_dict):
	""" find all sources word for a syn from syn dict """
	sources = []
	for source, v in syn_dict.iteritems():
		if syn in v:
			sources.append(source)
	return sources


if __name__ == "__main__":
	start = time.time()
	#enron_data_to_text()
	#preprocess_enron_text()
	save_context_lists('n')
	get_largest_syn('n')
	print "time {0}s".format(time.time() - start)
