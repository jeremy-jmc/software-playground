import json
import os
from locust import HttpUser, TaskSet, task, between

class AudioTranscriptionTaskSet(TaskSet):

    @task
    def transcribe_audio(self):
        file_path = 'segmento_000.mp3'
        url = '/transcribe'
        
        with open(file_path, 'rb') as f:
            files = {'audio_path': (file_path, f, 'audio/mpeg')}
            headers = {'accept': 'application/json'}
            response = self.client.post(url, headers=headers, files=files)
            print(f'Response status code: {response.status_code}')
            # print(f'HTTP request name: {response.request.method} {response.request.url}')
            if response.status_code != 200:
                print(f'\t{response.text}')
            # print(json.dumps(response.json(), indent=2))

class WebsiteUser(HttpUser):
    tasks = [AudioTranscriptionTaskSet]
    wait_time = between(1, 5)  # Tiempo de espera entre tareas (en segundos)
    host = 'http://localhost:3000'  # Especificar el host base
