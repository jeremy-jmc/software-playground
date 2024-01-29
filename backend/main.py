"""
https://medium.com/@alexfoleydevops/hosting-yolov8-with-fastapi-5023d17f1833
https://medium.com/@pashashaik/a-guide-to-hand-calculating-flops-and-macs-fa5221ce5ccc
https://towardsdatascience.com/the-correct-way-to-measure-inference-time-of-deep-neural-networks-304a54e5187f
https://towardsdatascience.com/the-deep-learning-inference-acceleration-blog-series-part-1-introduction-668e39b8b14b
https://towardsdatascience.com/efficient-inference-in-deep-learning-where-is-the-problem-4ad59434fe36   
https://debuggercafe.com/train-pytorch-retinanet-on-custom-dataset/
https://towardsdatascience.com/boosting-pytorch-inference-on-cpu-from-post-training-quantization-to-multithreading-6820ac7349bb
https://stackoverflow.com/questions/74167896/what-cloud-run-cpu-and-memory-limits-do-app-engine-standard-instance-classes-map
https://cloud.google.com/appengine/docs/standard?hl=es-419#instance_classes
"""

from fastapi import FastAPI
# from fastapi import WebSocket, WebSocketDisconnect
from fastapi import File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import time
import json
import cv2
import numpy as np
import base64
import io
import os
import sys
import logging
import torch
from PIL import Image
from torchvision.models import resnet101, ResNet101_Weights

device = torch.device('cpu')
weights = ResNet101_Weights.DEFAULT
preprocess = weights.transforms()
model = resnet101(weights=weights).to(device)
model.eval()


app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('multipart.multipart').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"is_alive": True}

# receive an image from the client and output prediction with the model
@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict:
    try:
        # convert file to OpenCV image
        contents = await file.read()
        # logging.info(file)
        # logging.info(vars(file))
        # logging.info(dir(file))
        
        # handle received
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = Image.fromarray(img)

        # preprocess image
        img = preprocess(img).unsqueeze(0).to(device)
        logging.info(img.shape)
        
        # run inference
        with torch.no_grad():
            out = model(img).cpu()
            class_id = out.argmax(dim=1).item()
            score = out[0, class_id].item()
        
        category = weights.meta["categories"][class_id]

        # # Logging statements
        # logger.debug('Prediction successful.')
        # logger.debug('Class ID: %d', class_id)
        # logger.debug('Predicted: %s', category)
        # logger.debug('Score: %f', score)

        return {"class_id": class_id, "score": score, "category": category}
    
    except Exception as e:
        logger.error('Error processing image: %s', str(e))
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
# uvicorn main:app --reload

"""
# Build your Docker image (replace 'your-image-name' and 'path-to-your-Dockerfile' accordingly)
docker build -t your-image-name -f path-to-your-Dockerfile .

# Run the Docker container with the specified CPU and memory constraints
docker run -it --cpus=2 --memory=4g -p 8000:8000 your-image-name

ab -n 100 -c 10 http://localhost:8000/your-api-endpoint

https://www.youtube.com/watch?v=bcYmfHOrOPM
"""