# Use the official NVIDIA CUDA image with Ubuntu and Python 3.9
FROM nvidia/12.1.0-cudnn8-devel-ubuntu20.04

# Set the working directory inside the container
WORKDIR /app

# Install Python 3.9 and other necessary tools
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3-pip \
    python3.9-distutils \
    wget \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.9 as the default python
RUN ln -s /usr/bin/python3.9 /usr/local/bin/python

# Install ffmpeg
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg

# Copy all files from the current directory to the /app directory in the container
COPY . /app

# Install Python dependencies if a requirements.txt file is provided
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Command that runs when the container starts, keeps it running in a loop
CMD ["bash", "-c", "while :; do sleep 10; done"]
