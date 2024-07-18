bentoml build --containerize
nvidia-smi
nvcc --version
docker images
docker run -it --gpus all --rm -p 3000:3000 faster_whisper:$TAG serve
