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
        'accept': 'application/json',
    }

    response = requests.post(url, headers=headers, files=files)

print(json.dumps(response.json(), indent=2))

