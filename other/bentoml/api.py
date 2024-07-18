from flask import Flask, request, jsonify
import time
from faster_whisper import WhisperModel
import uuid
import os
import subprocess
import torch

# create a new Flask app
app = Flask(__name__)

# load the machine learning model with Whisper
model = WhisperModel("/tmp/medium", device="cuda", compute_type="int8_float16")


@app.route("/")
def hello_world():
    return jsonify(
        {
            "TIPO MODELO": "GPU - Whisper",
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count(),
            "torch_version": torch.__version__,
            "cuda_version": torch.version.cuda,
        }
    )


@app.route("/gpu-info")
def gpu_info():
    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=index,name,uuid,utilization.gpu,memory.total,memory.used,memory.free",
                "--format=csv,noheader",
            ]
        ).decode("utf-8")
        return jsonify({"result": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)})


# define a route to handle audio file predictions
@app.route("/predict", methods=["POST"])
def predict():
    # Measure the execution time
    start_time = time.time()

    # get the audio file from the request
    audio_file = request.files["audio"]

    # generate a unique filename
    unique_filename = str(uuid.uuid4()) + ".wav"
    audio_path = os.path.join("/tmp", unique_filename)

    # save the audio file to the unique location
    audio_file.save(audio_path)

    transcription = ""
    words_info = []

    segments, _ = model.transcribe(
        audio_path, task="transcribe", language="es", word_timestamps=True
    )

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

    # Calculate the execution time
    execution_time = time.time() - start_time

    # delete the temporary audio file
    os.remove(audio_path)

    # return the predicted text and segments as a JSON response
    return jsonify(
        {
            "execution_time": execution_time,
            "transcription": transcription,
            "segments": words_info,
        }
    )


# start the Flask app with gunicorn or uswgi
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
