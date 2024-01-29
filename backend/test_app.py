import io
import pytest
import requests
from fastapi.testclient import TestClient

# Import your FastAPI app
from main import app  # Assuming your FastAPI app is defined in a file named main.py

@pytest.fixture
def client():
    return TestClient(app)

def test_predict_endpoint(client):
    # Open an image file in binary mode
    with open("path/to/your/test/image.jpg", "rb") as img_file:
        # Send a POST request to the /predict endpoint with the image file
        response = client.post("/predict", files={"file": img_file})

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response JSON contains the expected keys
    assert "class_id" in response.json()
    assert "score" in response.json()
    assert "category" in response.json()

def test_predict_endpoint_no_file(client):
    # Send a POST request to the /predict endpoint without including an image file
    response = client.post("/predict")

    # Check if the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422

# You can add more test cases as needed
