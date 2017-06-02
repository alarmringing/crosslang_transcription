# crosslang_transcription
Transcription pipeline of Japanese-American Interviews, sponsored by the Hoover Institution

crosslang_transcription is developed to automate the transcription of archives of the Hoover Tower Institution, by using the Google Cloud's Google Speech API. 

First, set up a virtual environment: 
pip install virtualenv
virtualenv .env
source .env/bin/activate 

Download all required dependencies: 
pip install -r requirements.txt

Remember to manually create folders pred, truth, and keygen under output_location/project_name, and organize project folders in the input_location.

There are largely two separate modules in this repo, prototype transcribe and keyword pipeline.

1. Prototype Transcribe, given an input file and a list of keywords, generates a transcription result. The list of keywords refer to any relevent key vocabularies regarding the input audio that are provided beforehand. To see how one can automatically generate keywords, check keyword_pipeline. 

The usage is: 
python prototype_transcribe.py input_location output_location project_name batch_number(id)


2. Keyword Pipeline. Given an input file, this pipeline iterates through each one minute segments of the input file to generate keywords. Each iteration adds 10 words to a maximum of 50 word keyword list, based on how rare a given correction is, where if there are more than 50 keywords given the algorithm takes the top 50 keywords in the order of rare to common.

The usage is: 
python keyword_pipeline.py input_location output_location project_name batch_number(id)

This will generate two files in the location output_location/project_name/keygen, batch_number_pred and batch_number_toedit. Edit the batch_number_toedit by manually correcting the automated transcript and run keyword_pipeline again with the same parameters. Each iteration will edit the keywords.txt file under output_location/project_name to be used by the prototype transcribe module. 
