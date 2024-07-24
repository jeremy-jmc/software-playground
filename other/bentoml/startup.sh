# https://github.com/search?type=code&q=%22bentoml+build%22
# https://github.com/HieuBui99/end-to-end-recsys/blob/main/Makefile
bentoml build
bentoml containerize faster_whisper -t faster_whisper:latest
nvidia-smi
nvcc --version
docker images
docker run -it --cpus 8 --gpus all --rm -p 3000:3000 faster_whisper:latest serve
# -u 0 
cd $(bentoml get BENTO_TAG -o path) && cd ./src && ls
# https://stackoverflow.com/questions/9346211/how-to-kill-a-process-on-a-port-on-ubuntu
watch -n 1 nvidia-smi
while (1) {nvidia-smi; sleep 2; clear}