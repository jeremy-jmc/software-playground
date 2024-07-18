bentoml build
bentoml containerize faster_whisper -t faster_whisper:latest
nvidia-smi
nvcc --version
docker images
docker run -it --gpus all --rm -p 3000:3000 faster_whisper:latest serve
