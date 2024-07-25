# Use the base image with CUDA and cuDNN support
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y git git-lfs
RUN git lfs install

# Install python and pip
RUN apt-get update && apt-get install -y python3.8 python3-pip

# Set working directory
WORKDIR /app

# Install ffmpeg
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg

# Download the latest version of the base model
# Available in __init__.py of the whisper library
RUN apt-get update && apt-get install -y curl

# Copy all files to working directory
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 3000
EXPOSE 3000

# Command that runs when the container starts, keeps it running in a loop
CMD ["bash", "-c", "bentoml serve service:FasterWhisper --development --reload"]