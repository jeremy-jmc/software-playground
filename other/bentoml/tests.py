# -----------------------------------------------------------------------------
# Prueba Whisper
# -----------------------------------------------------------------------------
import logging
import os
import subprocess
import time
import uuid

import bentoml
import numpy as np
import torch
from faster_whisper import WhisperModel
import faster_whisper
print(faster_whisper.__version__)
from pydub import AudioSegment

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.__version__)
print(torch.version.cuda)

LANGUAGE_CODE = "es"

warmup_sample_audio = "./segmento_000.mp3"  # AudioSegment.from_file("./segmento_000.mp3")
warmup_sample_audio = np.random.rand(10000).astype(np.float32)
model = WhisperModel("medium", device="cuda", compute_type="int8_float16")

segments, transcription_info = \
    model.transcribe(warmup_sample_audio,  task="transcribe", language=LANGUAGE_CODE, word_timestamps=True)

print(segments)
print(transcription_info)

transcription = ""
words_info = []
for segment in segments:
    # transcription += segment.text
    for word in segment.words:
        # print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
        transcription += word.word

        word_info = {
            "segment_start": word.start,
            "segment_end": word.end,
            "text": word.word,
        }

        words_info.append(word_info)
print(segments)

print(transcription)
print(words_info)

torch.cuda.empty_cache()
del segments, transcription_info

# -----------------------------------------------------------------------------
# Prueba Bento
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

