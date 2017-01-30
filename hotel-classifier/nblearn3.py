#!/usr/bin/env python3
import sys, re
from collections import defaultdict
'''
Build a Bayesian Classifer model and write model parameters to nbmodel.txt
Each word is a feature. Calculate probabilities for the word based on train-text.txt
'''

def hasDigit(text):
	return any(char.isdigit() for char in text)

def filter_tokens(token):
	''' 
	Converts to lower case
	Retains only english alphabet characters from the token
	'''
	pattern = r'[^a-zA-Z]'
	result = re.sub(pattern, '', token)
	return result


def parse_text_file(text_file):
	tag_token = {}
	with open(text_file, 'r') as ipfile:
		for line in ipfile:
			tsplit = line.split(' ')
			#first token is label, rest are reviews
			tlabel = tsplit[0]
			tokens = tsplit[1:]
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



def create_model(tag_token, tag_truth_label, tag_positive_label):
	truthful_model_params = {}
	positive_model_params = {}

	positive_count = 0
	negative_count = 0
	truth_count = 0
	deceptive_count = 0

	vocabulary = set()
	token_dict = {}
	positive_token_count = 0
	negative_token_count = 0
	truth_token_count = 0
	deceptive_token_count = 0

	for tag, tokens in tag_token.items():
		if tag_truth_label[tag]['truthful'] is True:
			truth_count += 1
			truth_token_count += len(tokens)
			for token in tokens:
				vocabulary.add(token)
				if token in token_dict:
					token_dict[token]['truth_count'] += 1
				else:
					token_dict[token] = {'truth_count': 1, 'deceptive_count': 0, 'positive_count': 0, 'negative_count': 0}
		else:
			deceptive_count += 1
			deceptive_token_count += len(tokens)
			for token in tokens:
				vocabulary.add(token)
				if token in token_dict:
					token_dict[token]['deceptive_count'] += 1
				else:
					token_dict[token] = {'truth_count': 0, 'deceptive_count': 1, 'positive_count': 0, 'negative_count': 0}

		if tag_positive_label[tag]['positive'] is True:
			positive_count += 1
			positive_token_count += len(tokens)
			for token in tokens:
				vocabulary.add(token)
				if token in token_dict:
					token_dict[token]['positive_count'] += 1
				else:
					token_dict[token] = {'truth_count': 0, 'deceptive_count': 0, 'positive_count': 1, 'negative_count': 0}
		else:
			negative_count += 1
			negative_token_count += len(tokens)
			for token in tokens:
				vocabulary.add(token)
				if token in token_dict:
					token_dict[token]['negative_count'] += 1
				else:
					token_dict[token] = {'truth_count': 0, 'deceptive_count': 0, 'positive_count': 0, 'negative_count': 1}

	#calculate prior probabilities
	positive_prior = float(positive_count) / (positive_count + negative_count)
	negative_prior = float(negative_count) / (positive_count + negative_count)
	truth_prior = float(truth_count) / (truth_count + deceptive_count)
	deceptive_prior = float(deceptive_count) / (truth_count + deceptive_count)

	#print(token_dict)




def construct_model(text_file, label_file):
	tag_token = parse_text_file(text_file)
	tag_truth_label, tag_positive_label = parse_label_file(label_file)
	create_model(tag_token, tag_truth_label, tag_positive_label)



if __name__ == '__main__':
	assert (len(sys.argv) == 3),'Expects one text file and one training file'
	text_file = sys.argv[1]
	label_file = sys.argv[2]
	construct_model(text_file, label_file)
