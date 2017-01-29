#!/usr/bin/env python
import sys
'''
Reads model parameters and classifys hotel reviews from test data into nboutput.txt
'''


if __name__ == '__main__':
	asssert (len(sys.argv[1]) == 2), 'Expects one test data file as argument'
	test_data_file = sys.argv[1]