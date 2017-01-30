#!/usr/bin/env python
import sys, re, json
'''
Reads model parameters and classify hotel reviews from test data into nboutput.txt
'''

def read_model_params():
	with open('nbmodel.txt') as ip:
		model_data = json.load(ip)
	return model_data

def filter(token):
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

def write_output(result):
	with open('nboutput.txt', 'w') as output_file:
		for tag, res in result.items():
			data = tag + ' ' + res[0] + ' ' + res[1] + '\n'
			output_file.write(data)

def classify_test(text_file):
	tag_token = parse_text_file(text_file)
	model_data = read_model_params()
	positive_prior = model_data['class_probability']['positive_prior']
	negative_prior = model_data['class_probability']['negative_prior']
	truth_prior = model_data['class_probability']['truth_prior']
	deceptive_prior = model_data['class_probability']['deceptive_prior']
	feature_data = model_data['feature_probability']
	tag_result = {}

	for tag, tokens in tag_token.items():
		truth_class_val = truth_prior
		deceptive_class_val = deceptive_prior
		positive_class_val = positive_prior
		negative_class_val = negative_prior
		for t in tokens:
			tok = filter(t)
			if tok in feature_data:
				truth_class_val += feature_data[tok]['truth_probability']
				deceptive_class_val += feature_data[tok]['deceptive_probability']
				positive_class_val += feature_data[tok]['positive_probability']
				negative_class_val += feature_data[tok]['negative_probability']

		if truth_class_val > deceptive_class_val:
			tag_result[tag] = ['truthful']
		else:
			tag_result[tag] = ['deceptive']

		if positive_class_val > negative_class_val:
			tag_result[tag].append('positive')
		else:
			tag_result[tag].append('negative')

	write_output(tag_result)


if __name__ == '__main__':
	assert (len(sys.argv) == 2), 'Expects one test data file as argument'
	test_data_file = sys.argv[1]
	classify_test(test_data_file)