# -----------------------------------------------------------------------------
# Prueba Whisper
# -----------------------------------------------------------------------------
import logging
import os
import subprocess
import time
import uuid

# import bentoml
import numpy as np
import torch
from faster_whisper import WhisperModel, BatchedInferencePipeline
import faster_whisper
print(faster_whisper.__version__)
# from pydub import AudioSegment

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.version.cuda)

LANGUAGE_CODE = "es"

warmup_sample_audio = "./segmento_059.mp3"  # AudioSegment.from_file("./segmento_000.mp3")
# warmup_sample_audio = np.random.rand(10000).astype(np.float32)
model = WhisperModel("medium", device="cuda", compute_type="int8_float16")

start_time_seq = time.time()
segments, transcription_info = \
    model.transcribe(warmup_sample_audio, task="transcribe", language=LANGUAGE_CODE, word_timestamps=True)

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
end_time_seq = time.time()
print(segments)
print(transcription)
print(words_info)


batched_model = BatchedInferencePipeline(model=model)

start_time_batched = time.time()
segments_batched, transcription_info_batched = \
    batched_model.transcribe(warmup_sample_audio, task="transcribe", language=LANGUAGE_CODE, word_timestamps=True, 
                             batch_size=8)

transcription_batched = ""
words_info_batched = []
for segment in segments_batched:
    # transcription_batched += segment.text
    for word in segment.words:
        # print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
        transcription_batched += word.word

        word_info = {
            "segment_start": word.start,
            "segment_end": word.end,
            "text": word.word,
        }

        words_info_batched.append(word_info)
end_time_batched = time.time()
print(segments_batched)
print(transcription_batched)
print(words_info_batched)


print(transcription)
print(transcription_batched)

print("Sequential time: %.2fs" % (end_time_seq - start_time_seq))
print("Batched time: %.2fs" % (end_time_batched - start_time_batched))