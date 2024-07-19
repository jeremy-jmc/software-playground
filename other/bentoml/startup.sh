# https://github.com/search?type=code&q=%22bentoml+build%22
# https://github.com/HieuBui99/end-to-end-recsys/blob/main/Makefile
bentoml build
bentoml containerize faster_whisper -t faster_whisper:latest
nvidia-smi
nvcc --version
docker images
docker run -it --cpus 8 --gpus all --rm -p 3000:3000 faster_whisper:latest serve
# -u 0 