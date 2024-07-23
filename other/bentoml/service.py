"""
https://docs.bentoml.com/en/latest/use-cases/audio/whisperx.html
"""
import typing as t
from io import BytesIO
from pathlib import Path

import time
import bentoml
import numpy as np
import numpy.typing as npt
import torch
from fastapi import File, UploadFile
from pydub import AudioSegment
import subprocess

LANGUAGE_CODE = "es"

# Function extracted from pypi whisperx
def load_audio(file: str, sr: int = 16000) -> np.ndarray:
    try:
        cmd = [
            "ffmpeg",
            "-nostdin",
            "-threads",
            "0",
            "-i",
            file,
            "-f",
            "s16le",
            "-ac",
            "1",
            "-acodec",
            "pcm_s16le",
            "-ar",
            str(sr),
            "-",
        ]
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


@bentoml.service(
    traffic={
        "timeout": 60,
        "concurrency": 3,
    },
    workers=3,
    resources={
        "gpu": torch.cuda.device_count(),
        # "gpu_type": "nvidia_gtx_1650",  # "nvidia_tesla_t4"
    },
)
class FasterWhisper:
    """
    Faster Whisper service
    """

    def __init__(self):
        import torch
        from faster_whisper import WhisperModel, BatchedInferencePipeline
        self.model = WhisperModel("./medium", device="cuda", compute_type="int8_float16")
        self.batched_model = BatchedInferencePipeline(model=self.model)

    
    @bentoml.api()
    async def transcribe(self, audio_path: Path) -> t.Dict:
        torch.cuda.empty_cache()
        
        start_time = time.time()
        audio = load_audio(audio_path)
        segments, transcription_info = \
                self.batched_model.transcribe(audio, task="transcribe", language=LANGUAGE_CODE, batch_size=8, word_timestamps=True)
        
        # print(segments)
        transcription = ""
        words_info = []
        for segment in segments:
            for word in segment.words:
                transcription += word.word

                word_info = {
                    "segment_start": word.start,
                    "segment_end": word.end,
                    "text": word.word,
                }

                words_info.append(word_info)
        execution_time = time.time() - start_time
        torch.cuda.empty_cache()
        return {
            "execution_time": execution_time,
            "transcription": transcription,
            "segments": words_info,
        }
    
        
    @bentoml.api()
    def is_alive(self) -> dict:
        total_vram_mb = 0
        if torch.cuda.is_available():
            total_vram_mb = sum([torch.cuda.get_device_properties(i).total_memory for i in range(torch.cuda.device_count())]) // 1024**2
        return {
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count(),
            "torch_version": torch.__version__,
            "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
            "available_gpus": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
            "total_vram": f"{total_vram_mb} MB",
        }
    
    
    @bentoml.api()
    def gpu_info(self) -> dict:
        try:
            output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=index,name,uuid,utilization.gpu,memory.total,memory.used,memory.free",
                    "--format=csv,noheader",
                ]
            ).decode("utf-8")
            return {"result": output}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}
        

"""
bentoml serve service:FasterWhisper --development --reload

bentoml build
bentoml list
bentoml
bentoml containerize faster_whisper:latest
history

bentoml build && bentoml containerize faster_whisper -t faster_whisper:latest && docker run -it --cpus 8 --gpus all --rm -p 3000:3000 faster_whisper:latest serve
"""