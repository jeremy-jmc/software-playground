import bentoml
import os
import typing as t

from pathlib import Path

LANGUAGE_CODE = "es"


@bentoml.service(
    traffic={
        "timeout": 30,
        "concurrency": 2,
    },
    workers=2,
    resources={
        "gpu": 1,
        # "gpu_type": "nvidia_tesla_t4",
    },
)
class WhisperX:
    """
    This class is inspired by the implementation shown in the whisperX project.
    Source: https://github.com/m-bain/whisperX
    """

    def __init__(self):
        import torch
        import whisperx

        self.batch_size = 8 # reduce if low on GPU mem
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "int8_float16" if torch.cuda.is_available() else "int8"
        self.model = whisperx.load_model("small", self.device, compute_type=compute_type, language=LANGUAGE_CODE)
        self.model_a, self.metadata = whisperx.load_align_model(language_code=LANGUAGE_CODE, device=self.device)

    @bentoml.api
    def transcribe(self, audio_file: Path) -> t.Dict:
        import whisperx

        audio = whisperx.load_audio(audio_file)
        result = self.model.transcribe(audio, batch_size=self.batch_size)
        result = whisperx.align(result["segments"], self.model_a, self.metadata, audio, self.device, return_char_alignments=False)

        return result
    
# https://docs.bentoml.com/en/latest/use-cases/audio/whisperx.html
# https://github.com/bentoml/BentoWhisperX/blob/main/bentofile.yaml