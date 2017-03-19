#!/usr/bin/env python
import sys, json
'''
Reads model parameters and does POS tagging
'''
e_prob = {}
t_prob = {}
incoming_states = {}
def read_model_params():
	global e_prob
	global t_prob
	global incoming_states
	with open('hmmmodel.txt') as ip:
		model_data = json.load(ip)
		e_prob = model_data["model_probability"]["emission_probability"]
		t_prob = model_data["model_probability"]["transition_probability"]
		incoming_states = model_data["model_probability"]["incoming_states"]

def write_output(result):
	with open('hmmoutput.txt', 'a') as output_file:
		output_file.write(result)

def viterbi_algo(words):
	l = len(words)
	k = list(t_prob.keys())
	total_states = list(t_prob[k[0]].keys())
	word_tag = {}
	result = {words[0]: {0: {}}}
	back_ptr = {words[0]: {0: {}}}
	back_res = {words[0]: {0: {}}}

	'''
	for state, tr_pr in t_prob.items():
		if words[0] in e_prob:
			if state in e_prob[words[0]]:
				e_val = e_prob[words[0]][state]
			else:
				e_val = -float("inf")
		else:
			e_val = -float("inf")
		if state in t_prob['start']:
			t_val = t_prob['start'][state]
		else:
			t_val = -float("inf")
		result[words[0]][0][state] = t_val + e_val
		back_ptr[words[0]][0][state] = 'start'
	'''
	if words[0] in e_prob:
		start_states = e_prob[words[0]]
		prev_states = start_states
		for s in start_states:
			#if s in t_prob['start']:
			result[words[0]][0][s] = t_prob['start'][s] + e_prob[words[0]][s]
			back_res[words[0]][0][s] = result[words[0]][0][s]
			back_ptr[words[0]][0][s] = 'start'

	else:
		prev_states = t_prob['start'].keys()
		for s, st in t_prob['start'].items():
			result[words[0]][0][s] = t_prob['start'][s]
			back_res[words[0]][0][s] = result[words[0]][0][s]
			back_ptr[words[0]][0][s] = 'start'

	
	for i,w in enumerate(words[1:]):
		#print(json.dumps(result))
		if w in result:
			if (i+1) in result[w]:
				pass
			else:
				result[w][i+1] = {}
		else:
			result[w] = {i+1: {}}
			
		if w in back_ptr:
			if (i+1) in back_ptr[w]:
				pass
			else:
				back_ptr[w][i+1] = {}
		else:
			back_ptr[w] = {i+1: {}}

		if w in back_res:
			if (i+1) in back_res[w]:
				pass
			else:
				back_res[w][i+1] = {}
		else:
			back_res[w] = {i+1: {}}
		
		if w in e_prob:
			cur_states = e_prob[w].keys()
			for cur in cur_states:
				val = -float("inf")
				#incoming = incoming_states[cur]
				incoming = prev_states
				for st in incoming:
					#print(st,cur)
					if cur in t_prob[st]:

						v = t_prob[st][cur] +  e_prob[w][cur] + result[words[i]][i][st]
						if v > val:
							val = v
							back_ptr[w][i+1][cur] = st
							result[w][i+1][cur] = val
			prev_states = cur_states
		else:
			#unknown token
			#cur_states = prev_states
			cur_states = total_states
			for cur in cur_states:
				val = -float("inf")
				#incoming = incoming_states[cur]
				incoming = prev_states
				for st in incoming:
					if cur in t_prob[st]:
						v = t_prob[st][cur] +  result[words[i]][i][st]
						if v > val:
							val = v
							back_ptr[w][i+1][cur] = st
							result[w][i+1][cur] = val
			prev_states = cur_states


	last_word = words[-1]
	v = -float("inf")
	tagged_result = u""
	pr_values = result[last_word][l-1]
	for st, val in pr_values.items():
		if val > v:
			v = val
			state = st
	tagged_result = (last_word + "/" + state + " ") + tagged_result

	p_state = back_ptr[last_word][l-1][state]
	k = l-2
	while k >= 0:
		w = words[k]
		tagged_result = (w + "/" + p_state + " ") + tagged_result
		if k > 0:
			prev_state = back_ptr[w][k][p_state]		
			p_state = prev_state
		k -= 1

	tagged_result += '\n'
	write_output(tagged_result)



def classify_test(test_file):
	read_model_params()
	op_file = open('hmmoutput.txt', 'w')
	with open(test_file, 'r') as lf:
		for line in lf:
			words = line.strip().split(' ')
			viterbi_algo(words)

if __name__ == '__main__':
	assert (len(sys.argv) == 2), 'Expects one test data file as argument'
	test_data_file = sys.argv[1]
	classify_test(test_data_file)