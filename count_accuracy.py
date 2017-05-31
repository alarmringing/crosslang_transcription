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
		pred = f.readlines()[1].split()
		for word in pred:
			pred_dict[word] += 1

	truth_dict = collections.defaultdict(int) #dictionary of words in prediction file
	with open(truth_file, 'r') as f:
		truth = f.readlines()[1].split()
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

	accuracy = (wc-float(len(diff)))/wc
	print("ACCURACY: ", accuracy)

	return accuracy, diff #reports accuracy and diff



'''
find keywords that are important, and should be added to the keyword list
'''
def find_keywords(diff, global_dict, consider):
	sorted_diff = sorted(list(diff), key=global_dict.get)
	#consider top $consider$ options 
	return sorted_diff[0:consider]
	

'''
Write to given keywords file
'''	
def write_keywords(keywords, filepath, consider, global_dict):
	existing_keywords = set()
	with open(filepath, 'r+') as f:
		#read file first to test overlap
		existing = f.readlines()
		for i in range(len(existing)):
			existing_keywords.add(existing[i].lower().strip())

	#add this keyword to existing keywords
	count = 0
	for word in keywords:
		if word not in existing_keywords:
			existing_keywords.add(word.lower().strip()) 
			count += 1
			if count > consider: #only add certain amount of words in there
				break

	#only take the top 50
	existing_keywords = list(existing_keywords)
	if len(existing_keywords) > 50:
		existing_keywords = sorted(existing_keywords, key=global_dict.get)
		existing_keywords = existing_keywords[:50]

	with open(filepath, 'w+') as f:
		for word in existing_keywords:
			f.write(word + '\n')
			



'''
< USAGE >
python count_accuracy.py output_location project_name batch_number(id)
'''
if __name__ == '__main__':
	
	pred_file = sys.argv[1] + '/' + sys.argv[2] + '/pred/' + sys.argv[3] + '_pred.txt'
	truth_file = sys.argv[1] + '/' + sys.argv[2] + '/truth/' + sys.argv[3] + '_truth.txt'
	keyword_file = sys.argv[1] + '/' + sys.argv[2] + '/' + 'keywords.txt'

	global_dict = build_dict("wordfreq.txt")
	acc, diff = count_accuracy(pred_file, truth_file)
	keywords = find_keywords(diff, global_dict, 30)
	write_keywords(keywords, keyword_file, 5, gloabl_dict)





