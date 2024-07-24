# -----------------------------------------------------------------------------
# Download Faster Whisper model
# -----------------------------------------------------------------------------

import os
import faster_whisper

model_path = './medium'
faster_whisper.download_model('medium', model_path)

# -----------------------------------------------------------------------------
# Prueba API Bento
# -----------------------------------------------------------------------------

import requests
import json

url = 'http://localhost:3000/transcribe'
file_path = 'segmento_000.mp3'

with open(file_path, 'rb') as f:
    files = {'audio_path': (file_path, f, 'audio/mpeg')}
    headers = {
        'accept': 'application/json'
    }

    response = requests.post(url, headers=headers, files=files)

print(json.dumps(response.json(), indent=2))



import requests

url = 'http://localhost:3000/transcribe'
headers = {
    'accept': 'application/json'
}
files = {
    'audio_path': ('audio_20240907123104.wav', open('audio_20240907123104.wav', 'rb'), 'audio/wav')
}

response = requests.post(url, headers=headers, files=files)

print(response.json())



from pathlib import Path
import bentoml

file_path = 'segmento_000.mp3'
with bentoml.SyncHTTPClient('http://localhost:3000') as client:
    response = client.transcribe(audio_file=file_path)
    print(response)



import requests
whisper_api = 'http://localhost:80'
with open('segmento_000.mp3', 'rb') as audio_file:
    print(whisper_api)
    request_body = {'audio': audio_file}
    response_text = requests.post(f"{whisper_api}/predict", files=request_body).json()

# se obtiene el texto y el tiempo de ejecucion
text = response_text['transcription']
execution_time = response_text['execution_time']
segments = response_text['segments']

print(text, segments)
print(execution_time)
