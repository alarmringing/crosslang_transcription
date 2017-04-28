import argparse
import io
import sys
import soundfile as sf

PAYLOAD_LIMIT = 10485760
OVERLAP = PAYLOAD_LIMIT/float(20)

def transcribe_file(speech_file):
	"""Transcribe the given audio file."""
	from google.cloud import speech
	speech_client = speech.Client()

	print("speech_file looks like ", speech_file)
	save_file = open("Output.txt", "w")
	text = ''
	for audio in sf.blocks(speech_file, blocksize=PAYLOAD_LIMIT, overlap=OVERLAP):
		sf.SoundFile('buffer.wav', 'w', 44100, 1, 'PCM_16').write(audio.sum(axis=1) / float(2))
		content = io.open('buffer.wav', 'rb').read()
		audio_sample = speech_client.sample(
			content=content,
			source_uri=None,
			encoding='LINEAR16',
			sample_rate_hertz=44100)
		alternatives = audio_sample.recognize('en-US')
	for alternative in alternatives:
		#text_file.write("%s" % alternative.transcript)
		text += '\n' + alternative.transcript
		#print('Transcript: {}'.format(alternative.transcript))

	save_file.write(text)
	save_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument(
		'path', help='type audio file path to be recognized')
	args = parser.parse_args()
	print("args is ", args)
	transcribe_file(args.path)