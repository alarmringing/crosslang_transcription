import argparse
import io
import os
import sys
import soundfile as sf

#PAYLOAD_LIMIT = 10485760
PAYLOAD_LIMIT = 2500000
#PAYLOAD_LIMIT = 3000000
OVERLAP = PAYLOAD_LIMIT/60


def transcribe_file(speech_filepath, output_filepath, keyword_file, start_timestamp, length):
	"""Transcribe the given audio file. Length is in seconds."""
	from google.cloud import speech
	speech_client = speech.Client()

	"""Read keyword_file, if any."""
	keywords = [] #empty list
	if os.path.exists(keyword_file):
		with open(keyword_file, 'r') as f:
			keywords_raw = f.readlines()
			for i in range(len(keywords_raw)):
				keywords.append(keywords_raw[i].lower().strip())

	#MULTILINGUAL SUPPORT DISABLED FOR NOW
	language = 'en-US'
	'''
	#set language
	language = ''
	if lang == '-e':
		language = 'en-US'
	else:
		language = 'ja-JP'
	'''


	"""create and open text file to save transcription"""
	save_file = open(output_filepath, "w+")
	text = ''

	"""Slice audio into # of blocks, then send to google cloud for analysis"""
	sample_rate = 44100
	stop = -1
	if length > 0:
		stop = start_timestamp + sample_rate * length
	print("start and stop is ", start_timestamp, stop)

	count = 0
	for audio in sf.blocks(speech_filepath, start=start_timestamp, stop=stop, \
		blocksize=PAYLOAD_LIMIT, overlap=OVERLAP):
		sf.SoundFile('buffer.wav', 'w', sample_rate, 1, 'PCM_16').write(audio.sum(axis=1) / float(2))
		content = io.open('buffer.wav', 'rb').read()
		audio_sample = speech_client.sample(
			content=content,
			source_uri=None,
			encoding='LINEAR16',
			sample_rate=sample_rate)
		print("evaluating block ", count)
		count += 1
		
		try:
			alternatives = audio_sample.sync_recognize(language_code=language, speech_context=keywords)
			for alternative in alternatives:
				text += alternative.transcript + ' '
		except ValueError:
			continue
	

	"""final save"""
	#add stop timestep on top
	text = str(stop) + "\n" + text
	save_file.write(text.encode('utf-8'))
	save_file.close()
	return text

'''
<Usage>
python prototype_transcribe.py input_location[1] output_location[2] project_name[3] batch_number(id)[4]
'''
if __name__ == '__main__':

	input_file = sys.argv[1] + '/' + sys.argv[3] + '/' + sys.argv[4] + '.wav'
	output_file = sys.argv[2] + '/' + sys.argv[3] + '/pred/' +  sys.argv[4] + '_pred.txt'
	keyword_file = sys.argv[2] + '/' + sys.argv[3] + '/' +'keywords.txt'

	#read the whole file
	transcribe_file(input_file, output_file, keyword_file, 0, -1)