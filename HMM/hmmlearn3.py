#!/usr/bin/env python3
import sys, json, math
from copy import deepcopy
'''
Build a HMM model and write model parameters to nbmodel.txt
'''
transition = {'start': {}}
emission = {}
tag_c = {'start': 0}
word_c = {}
total_tags = set()
total_words = set()
tag_cp = {}
tr_cp = {}

def parse_label_file(label_file):
	#Read from the label file
	with open(label_file, 'r') as lf:
		for line in lf:
			tag_c['start'] += 1
			word_tags = line.strip().split(' ')
			cur_state = None
			prev_state = None
			for wt in word_tags:
				word, tag = wt.rsplit('/',1)
				total_tags.add(tag)
				total_words.add(word)
				if tag in tag_c:
					tag_c[tag] += 1
				else:
					tag_c[tag] = 1
				if word in word_c:
					word_c[word] += 1
				else:
					word_c[word] = 1
				cur_state = tag

				#For Transition probabilities
				if prev_state is None:
					if cur_state in transition['start']:
						transition['start'][cur_state] += 1
					else:
						transition['start'][cur_state] = 1
				else:
					if prev_state in transition:
						if cur_state in transition[prev_state]:
							transition[prev_state][cur_state] += 1
						else:
							transition[prev_state][cur_state] = 1
					else:
						transition[prev_state] = {cur_state: 1}

				#For emission probabilities
				if word in emission:
					if tag in emission[word]:
						emission[word][tag] += 1
					else:
						emission[word][tag] = 1
				else:
					emission[word] = {tag: 1}
				prev_state = tag

def apply_smoothing():
	global tr_cp
	global tag_cp
	tr_cp = deepcopy(transition)
	tag_cp = deepcopy(tag_c)
	
	
	#check if all states are there in transition
	total_s = set(tr_cp.keys())
	rem_s = total_tags - total_s
	for s in rem_s:
		tr_cp[s] = {}
		tag_cp[s] = len(total_tags)
		for t in total_tags:
			tr_cp[s][t] = 1

	#Add smoothing to all transition probabilities
	for prev_state, next_st in tr_cp.items():
		#if prev_state == 'start':
		#	continue
		total_s = set(next_st.keys())
		#print(prev_state, total_s)
		rem_s = total_tags - total_s
		for st in total_s:
			tr_cp[prev_state][st] += 1
		tag_cp[prev_state] += len(total_s)
		for st in rem_s:
			tr_cp[prev_state][st] = 1
		tag_cp[prev_state] += len(rem_s)
	
	

def write_model(data):
	with open('hmmmodel.txt', 'w') as model_file:
		json.dump(data, model_file)

def create_model():
	transition_prob = {}
	incoming_states = {}
	
	for prev_state, next_st in tr_cp.items():
		transition_prob[prev_state] = {}
		for st, count in next_st.items():
			if count == tag_cp[prev_state]:
				transition_prob[prev_state][st] = 1.0
			else:
				transition_prob[prev_state][st] = math.log(float(count)/tag_cp[prev_state]) #NOTE - tag_cp

			if st in incoming_states:
				incoming_states[st].add(prev_state)
			else:
				incoming_states[st] = set([prev_state])

	for s,st in incoming_states.items():
		incoming_states[s] = list(st)

	e_prob = {}
	for word, tc in emission.items():
		e_prob[word] = {}
		for tag, c in tc.items():
			if c == tag_c[tag]:
				e_prob[word][tag] = 1.0
			else:
				e_prob[word][tag] = math.log(float(c)/tag_c[tag]) #NOTE - tag_c


	model_data = {'model_probability': {'transition_probability': transition_prob, 'emission_probability': e_prob,
				  'incoming_states': incoming_states}}
	#print(incoming_states)
	#print(json.dumps(transition_prob))
	write_model(model_data)

def construct_model(label_file):
	parse_label_file(label_file)
	apply_smoothing()
	create_model()

if __name__ == '__main__':
	assert (len(sys.argv) == 2),'Expects one text file and one training file'
	label_file = sys.argv[1]
	construct_model(label_file)
