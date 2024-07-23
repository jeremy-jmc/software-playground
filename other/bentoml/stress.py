import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configuración de la prueba
URL = 'http://localhost:3000/transcribe'
FILE_PATH = 'segmento_000.mp3'
HEADERS = {'accept': 'application/json'}
NUM_REQUESTS = 64  # Número total de solicitudes
CONCURRENT_REQUESTS = 16  # Número de solicitudes concurrentes

def transcribe_audio():
    with open(FILE_PATH, 'rb') as f:
        files = {'audio_path': (FILE_PATH, f, 'audio/mpeg')}
        start_time = time.time()
        response = requests.post(URL, headers=HEADERS, files=files)
        end_time = time.time()
        response_time = end_time - start_time
        return response, response_time

def main():
    start_time = time.time()
    success_count = 0
    failure_count = 0
    total_response_time = 0

    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        future_to_request = {executor.submit(transcribe_audio): i for i in range(NUM_REQUESTS)}
        
        for future in as_completed(future_to_request):
            try:
                response, response_time = future.result()
                total_response_time += response_time
                if response.status_code == 200:
                    success_count += 1
                else:
                    failure_count += 1
                    print(f'Request failed with status code: {response.status_code}')
                    print(f'\t{response.text}')
            except Exception as exc:
                failure_count += 1
                print(f'Generated an exception: {exc}')
                
    end_time = time.time()
    average_response_time = total_response_time / NUM_REQUESTS

    print(f'Total time for {NUM_REQUESTS} requests: {end_time - start_time} seconds')
    print(f'Successful requests: {success_count}')
    print(f'Failed requests: {failure_count}')
    print(f'Average time per response: {average_response_time} seconds')

if __name__ == '__main__':
    main()
