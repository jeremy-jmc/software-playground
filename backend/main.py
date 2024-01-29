"""
https://medium.com/@alexfoleydevops/hosting-yolov8-with-fastapi-5023d17f1833
https://medium.com/@pashashaik/a-guide-to-hand-calculating-flops-and-macs-fa5221ce5ccc
https://towardsdatascience.com/the-correct-way-to-measure-inference-time-of-deep-neural-networks-304a54e5187f
https://towardsdatascience.com/the-deep-learning-inference-acceleration-blog-series-part-1-introduction-668e39b8b14b
https://towardsdatascience.com/efficient-inference-in-deep-learning-where-is-the-problem-4ad59434fe36   
https://debuggercafe.com/train-pytorch-retinanet-on-custom-dataset/
https://towardsdatascience.com/boosting-pytorch-inference-on-cpu-from-post-training-quantization-to-multithreading-6820ac7349bb
"""

from fastapi import FastAPI
# from fastapi import WebSocket, WebSocketDisconnect
from fastapi import File, UploadFile, HTTPException
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
from torchvision.models import resnet50, ResNet50_Weights

device = torch.device('cpu')
weights = ResNet50_Weights.DEFAULT
preprocess = weights.transforms()
model = resnet50(weights=weights).to(device)
model.eval()


app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"is_alive": True}

# receive an image from the client and output prediction with the model
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # convert file to OpenCV image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # resize image
        img = cv2.resize(img, (256, 256))
        
        # convert image to tensor
        img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float()
        
        # preprocess image
        img = preprocess(img)
        
        # run inference
        with torch.no_grad():
            out = model(img)
            class_id = out.argmax(dim=1).item()
            score = out[0, class_id].item()
        
        category = weights.meta["categories"][class_id]

        # Logging statements
        logger.debug('Prediction successful.')
        logger.debug('Class ID: %d', class_id)
        logger.debug('Predicted: %s', category)
        logger.debug('Score: %f', score)

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
"""