#!/usr/bin/env python3
import sys, re, json
'''
Build a Bayesian Classifer model and write model parameters to nbmodel.txt
Each word is a feature. Calculate probabilities for the word based on train-text.txt
'''


STOP_WORDS = ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 
'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 
'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 
'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'computer', 'con', 
'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 
'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 
'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 
'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 
'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 
'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 
'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 
'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 
'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 
'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thick', 'thin', 
'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 
'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 
'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 
'yet', 'you', 'your', 'yours', 'yourself', 'yourselves']

def hasDigit(text):
	return any(char.isdigit() for char in text)

def filter(token):
	''' 
	Converts to lower case
	Retains only english alphabet characters from the token
	'''
	pattern = r'[^a-zA-Z]'
	result = re.sub(pattern, '', token)
	return result

def filter_tokens(tag_token):
	''' Remove stop words'''
	filtered_tag_token = {}
	#for tag, tokens in tag_token.items():
	#	for 
	return tag_token

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

			if tokens[2].strip('\n').lower() == 'positive':
				tag_positive_label[tag]['positive'] = True
			else:
				tag_positive_label[tag]['negative'] = True

	return tag_truth_label, tag_positive_label

def write_model(data):
	with open('nbmodel.txt', 'w') as model_file:
		json.dump(data, model_file)

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
	vocabulary_count = len(vocabulary)

	feature_params = {}
	for t,v in token_dict.items():
		pos_prob = float(v['positive_count'] + 1) / (positive_token_count + vocabulary_count)
		neg_prob = float(v['negative_count'] + 1) / (negative_token_count + vocabulary_count)
		truth_prob = float(v['truth_count'] + 1) / (truth_token_count + vocabulary_count)
		decep_prob = float(v['deceptive_count'] + 1) / (deceptive_token_count + vocabulary_count)
		feature_params[t] = {'positive_probability': pos_prob, 'negative_probability': neg_prob, 'truth_probability': truth_prob,
							 'deceptive_probability': decep_prob}

	model_data = {'class_probability': {'positive_prior': positive_prior, 'negative_prior': negative_prior, 'truth_prior': truth_prior, 
										'deceptive_prior': deceptive_prior}, 'feature_probability': feature_params}

	print(model_data)
	write_model(model_data)

def construct_model(text_file, label_file):
	tag_token = parse_text_file(text_file)
	filtered_tag_token = filter_tokens(tag_token)
	tag_truth_label, tag_positive_label = parse_label_file(label_file)
	create_model(filtered_tag_token, tag_truth_label, tag_positive_label)



if __name__ == '__main__':
	assert (len(sys.argv) == 3),'Expects one text file and one training file'
	text_file = sys.argv[1]
	label_file = sys.argv[2]
	construct_model(text_file, label_file)
