import requests
import time

def mp3file_to_text(filename):
    authKey = 'e0de07cbc0664769a3e96453a2585746'
    
    headers = {
        'authorization' : authKey,
        'content-type'  : 'application/json'
    }
    
    uploadUrl      = 'https://api.assemblyai.com/v2/upload'
    transcriptUrl  = 'https://api.assemblyai.com/v2/transcript'
    
    def uploadMyFile(fileName):
    
        def _readMyFile(fn):
    
            chunkSize = 10
    
            with open(fn, 'rb') as fileStream:
    
                while True:
                    data = fileStream.read(chunkSize)
    
                    if not data:
                        break
    
                    yield data
    
        response = requests.post(
            uploadUrl,
            headers= headers,
            data= _readMyFile(fileName)
        )
    
        json = response.json()
    
        return json['upload_url']
    
    def startTranscription(aurl):
    
        response = requests.post(
            transcriptUrl,
            headers= headers,
            json= { 'audio_url' : aurl }
        )
        
        json = response.json()
    
        return json['id']
    
    def getTranscription(tid):
    
        maxAttempts = 10
        timedout    = False
    
        while True:
            response = requests.get(
                f'{transcriptUrl}/{tid}',
                headers= headers
            )
    
            json = response.json()
    
            if json['status'] == 'completed':
                break
    
            maxAttempts -= 1
            timedout = maxAttempts <= 0
    
            if timedout:
                break
    
            time.sleep(3)
    
        return 'Timeout...' if timedout else json['text']
    
    
    
    audioUrl = uploadMyFile(filename)
    
    transcriptionID = startTranscription(audioUrl)
    
    text = getTranscription(transcriptionID)
    
    mp3 = '.mp3'
    
    text_file_name = filename.replace(mp3, '.txt')
    
    f = open(text_file_name, "w")
    f.write(text)
    f.close() 
    
    return text_file_name
    #print(f'Result: {text}')
    
    
