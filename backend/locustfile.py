from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Add some wait time between requests

    @task
    def predict_endpoint(self):
        # Replace the URL with your FastAPI server URL
        response = self.client.post("/predict", files={"file": open("path/to/your/test/image.jpg", "rb")})
        assert response.status_code == 200

    # Add more tasks for other endpoints if needed

