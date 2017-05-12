import io
import os
import sys
import collections

'''
builds dictionary of word frequencies in order of frequent -> less frequent
''' 
def build_dict(filepath):
	global_dict = collections.defaultdict(int)
	with open(filepath, 'r') as f:
		lines = f.readlines()
		count = len(lines)+1 #the more common the word, the higher this val is 
		for word in lines:
			global_dict[word.lower().strip()] = count
			count -= 1 #this descends, so that reaaaaly rare words can have a value of 0.
	return global_dict



'''
returns accuracy of the said batch, given two text inputs 
'''
def count_accuracy(pred_file, truth_file):

	pred_dict = collections.defaultdict(int) #dictionary of words in prediction file
	with open(pred_file, 'r') as f:
		pred = f.readlines()[0].split()
		for word in pred:
			pred_dict[word] += 1

	truth_dict = collections.defaultdict(int) #dictionary of words in prediction file
	with open(truth_file, 'r') as f:
		truth = f.readlines()[0].split()
		for word in truth:
			truth_dict[word] += 1 #subtract from pred_dict, later check diff using this 
	
	diff = set() #dict of differences
	wc = 0 #wordcount
	#compare pred_dict and truth_dict for errors, then add to diff
	for key,value in truth_dict.items():

		if any(i.isdigit() for i in key): #ignore any number-related words
			continue

		key = key.replace("\'s", '') #strip possessive clause, if that's a thing
		if key not in pred_dict:
			diff.add(key.lower())
		else: 
			if pred_dict[key] != value:
				diff.add(key.lower())
		wc += value

	accuracy = float(len(diff))/wc

	return accuracy, diff #reports accuracy and diff



'''
find keywords that are important, and should be added to the keyword list
'''
def find_keywords(diff, global_dict, consider):
	sorted_diff = sorted(list(diff), key=global_dict.get)
	#consider top $consider$ options 
	for i in range(consider):
		print("rarer element is... ", sorted_diff[i], " and their rarity value is ", global_dict[sorted_diff[i]])


'''
main
'''
if __name__ == '__main__':

	global_dict = build_dict("wordfreq.txt")
	acc, diff = count_accuracy(sys.argv[1], sys.argv[2])
	find_keywords(diff, global_dict, 5)





