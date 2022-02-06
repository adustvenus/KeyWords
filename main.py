
import youtube_dl
import requests
import pprint
from time import sleep

auth_key = "e0de07cbc0664769a3e96453a2585746"

ydl_opts = {
   'format': 'bestaudio/best',
   'postprocessors': [{
       'key': 'FFmpegExtractAudio',
       'preferredcodec': 'mp3',
       'preferredquality': '192',
   }],
   'ffmpeg-location': './',
   'outtmpl': "./%(id)s.%(ext)s",
}

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'

headers_auth_only = {'authorization': auth_key}
headers = {
   "authorization": auth_key,
   "content-type": "application/json"
}
CHUNK_SIZE = 5242880
def youtube_to_text(link):
    def transcribe_from_link(link, categories: bool):
    	_id = link.strip()
    
    	def get_vid(_id):
    		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    			return ydl.extract_info(_id)
    
    	# download the audio of the YouTube video locally
    	meta = get_vid(_id)
    	save_location = meta['id'] + ".mp3"
    
    	print('Saved mp3 to', save_location)
    
    
    	def read_file(filename):
    		with open(filename, 'rb') as _file:
    			while True:
    				data = _file.read(CHUNK_SIZE)
    				if not data:
    					break
    				yield data
    
    
    	# upload audio file to AssemblyAI
    	upload_response = requests.post(
    		upload_endpoint,
    		headers=headers_auth_only, data=read_file(save_location)
    	)
    
    	audio_url = upload_response.json()['upload_url']
    	print('Uploaded to', audio_url)
    
    	# start the transcription of the audio file
    	transcript_request = {
    		'audio_url': audio_url,
    		'iab_categories': 'True' if categories else 'False',
    	}
    
    	transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    
    	# this is the id of the file that is being transcribed in the AssemblyAI servers
    	# we will use this id to access the completed transcription
    	transcript_id = transcript_response.json()['id']
    	polling_endpoint = transcript_endpoint + "/" + transcript_id
    
    	print("Transcribing at", polling_endpoint)
    
    	return polling_endpoint
    
    def get_status(polling_endpoint):
        polling_response = requests.get(polling_endpoint, headers=headers)
        status = polling_response.json()['status']
        return status
    
    polling_endpoint = transcribe_from_link(link, False)
    
    transcript=''
    if get_status(polling_endpoint) =='completed':
    	polling_response = requests.get(polling_endpoint, headers=headers)
    	transcript = polling_response.json()['text']
    