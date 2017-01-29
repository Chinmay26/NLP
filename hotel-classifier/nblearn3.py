#!/usr/bin/env python3
import sys

'''
Learns from model and writes model parameters to nbmodel.txt
'''

def hasDigit(text):
	return any(char.isdigit() for char in text)

def tokenise(text_data):
	tokens = []
	for i in text_data:
		k = i.lower()
		if hasDigit(k):
			continue
		else:
			tokens.append(i)

	return tokens

def parse_text_file(text_file):
	tag_token = {}
	with open(text_file, 'r') as ipfile:
		for line in ipfile:
			tsplit = line.split(' ')
			#first token is label
			tlabel = tsplit[0]
			tokens = tokenise(tsplit[1:])
			tag_token[tlabel] = tokens

	return tag_token

def parse_label_file(label_file):
	tag_truth_label = {}
	tag_positive_label = {}
	with open(label_file, 'r') as lf:
		for line in lf:
			tokens = line.split(' ')
			tag = tokens[0]
			tag_truth_label[tag] = {'truthful': False, 'deceptive': False}
			tag_positive_label[tag] = {'positive': False, 'negative': False}

			if tokens[1].lower() == 'deceptive':
				tag_truth_label[tag]['deceptive'] = True
			else:
				tag_truth_label[tag]['truthful'] = True


			if tokens[2].lower() == 'positive':
				tag_positive_label[tag]['positive'] = True
			else:
				tag_positive_label[tag]['negative'] = True

	return tag_truth_label, tag_positive_label


def construct_model(text_file, label_file):
	tag_token = parse_text_file(text_file)
	print(tag_token['0117CBUj98k8MKQp8svI'])
	tag_truth_label, tag_positive_label = parse_label_file(label_file)

if __name__ == '__main__':
	assert (len(sys.argv) == 3),'Expects one text file and one training file'
	text_file = sys.argv[1]
	label_file = sys.argv[2]
	construct_model(text_file, label_file)
