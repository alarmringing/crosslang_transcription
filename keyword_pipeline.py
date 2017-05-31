import argparse
import io
import os
import sys
import soundfile as sf
import count_accuracy
import prototype_transcribe

'''
Provides a pipeline to generate a set of keywords, 30 max
Takes one input audio file
Reads from keygen_toedit file, edited by user 
Compares with keygen_pred file, runs count_accuracy, adds keywords
Looks at timestamp on keygen_pred, then regenerate keygen_pred using one minute from last timestamp
Copy content to keygen_toedit for user to edit
If reached end, return with message
'''


'''
Read pred and edited file, add to keywords
Returns the start_timestep for the recognizer to start from
'''
def read_edited(pred_file, edit_file, keyword_file):

	start_timestamp = 0

	#if such pred and edit file exists. 
	if os.path.exists(pred_file) and os.path.exists(edit_file):
		#read timestep, which will be a number in the first line of pred file
		with open(pred_file, 'r') as f:
			start_timestamp = int(f.readlines()[0])

		#add to keywords
		acc, diff = count_accuracy.count_accuracy(pred_file, edit_file)
		global_dict = count_accuracy.build_dict("wordfreq.txt")
		keywords = count_accuracy.find_keywords(diff, global_dict, 30)
		count_accuracy.write_keywords(keywords, keyword_file, 5, global_dict)

	#else, timestep remains 0.
	return start_timestamp



'''
<Usage>
python keyword_pipeline.py input_location[1] output_location[2] project_name[3] batch_number(id)[4]
'''

if __name__ == '__main__':

	input_file = sys.argv[1] + '/' + sys.argv[3] + '/' + sys.argv[4] + '.wav'
	keygen_dir = sys.argv[2] + '/' + sys.argv[3] + '/keygen'
	keygen_pred_file = keygen_dir + '/' + sys.argv[4] + '_keygen_pred.txt'
	keygen_edit_file = keygen_dir + '/' + sys.argv[4] + '_keygen_toedit.txt'
	keyword_file = sys.argv[2] + '/' + sys.argv[3] + '/' +'keywords.txt'


	start_timestamp = read_edited(keygen_pred_file, keygen_edit_file, keyword_file)
	print("start_timestamp looks like ", start_timestamp)
	transcription = prototype_transcribe.transcribe_file(\
		input_file, keygen_pred_file, keyword_file, start_timestamp, 60)

	#copy contents of pred_file to edit_file for user to edit
	edit_file = open(keygen_edit_file, "w+")
	edit_file.write(transcription.encode('utf-8'))
	edit_file.close()



