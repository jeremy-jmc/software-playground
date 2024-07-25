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

sudo chmod 777 /var/run/docker.sock
docker ps -a
kill -9 $(lsof -t -i:3000)
# https://stackoverflow.com/questions/9346211/how-to-kill-a-process-on-a-port-on-ubuntu
watch -n 1 nvidia-smi
while (1) {nvidia-smi; sleep 2; clear}

# https://www.gpu-mart.com/blog/nvidia-smi-has-failed-because-it-couldnt-communicate-with-the-nvidia-driver
docker build -t bentoml-cuda-python . 
docker run -d --gpus all -p 3000:3000 --name my_container bentoml-cuda-python
docker exec -it my_container bash
docker logs --follow container_id

docker compose -f docker-compose-gpu-models.yml build
docker compose -f docker-compose-gpu-models.yml up
docker compose -f docker-compose-gpu-models.yml down
docker compose up --build --scale airflow-worker=7

watch -n 1 "echo 'CPU:'; mpstat | grep 'all'; echo 'MEMORY:'; free -h; echo 'GPU:'; nvidia-smi --query-gpu=utilization.gpu,memory.total,memory.used --format=csv,noheader"
glances
gpustat
htop
