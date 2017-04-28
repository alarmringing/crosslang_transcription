import argparse
import io
import os
import sys
import soundfile as sf

PAYLOAD_LIMIT = 10485760
OVERLAP = PAYLOAD_LIMIT/float(20)

def transcribe_file(lang, speech_file, output_dir):
	"""Transcribe the given audio file."""
	from google.cloud import speech
	speech_client = speech.Client()
	#set language
	language = ''
	if lang == '-e':
		language = 'en-US'
	else:
		language = 'ja-JP'

	"""create and open text file to save transcription"""
	if not os.path.exists(os.path.dirname(output_dir)):
	    try:
	        os.makedirs(os.path.dirname(output_dir))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	save_file = open(output_dir + os.path.basename(speech_file).split('.')[0] + '_output.txt', "w")
	text = ''

	"""Slice audio into # of blocks, then send to google cloud for analysis"""

	for audio in sf.blocks(speech_file, blocksize=PAYLOAD_LIMIT, overlap=OVERLAP):
		sf.SoundFile('buffer.wav', 'w', 44100, 1, 'PCM_16').write(audio.sum(axis=1) / float(2))
		content = io.open('buffer.wav', 'rb').read()
		audio_sample = speech_client.sample(
			content=content,
			source_uri=None,
			encoding='LINEAR16',
			sample_rate_hertz=44100)
		alternatives = audio_sample.recognize(language)
	for alternative in alternatives:
		text += alternative.transcript

	"""final save"""
	save_file.write(text.encode('utf-8'))
	save_file.close()

if __name__ == '__main__':

	transcribe_file(sys.argv[1], sys.argv[2], sys.argv[3])