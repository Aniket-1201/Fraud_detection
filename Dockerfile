# 1. Use an official, lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only requirements first (to leverage Docker caching)
COPY requirements.txt .

# NEW: Install git! 'python:slim' doesn't have it, and DVC secretly needs it.
RUN apt-get update && apt-get install -y git && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy the entire project
COPY . .

# 5. MLOps Magic: Pull the actual ML model from DagsHub
ARG DAGSHUB_USERNAME
ARG DAGSHUB_TOKEN

# THE SILVER BULLET: Inject credentials directly into the URL!
RUN dvc remote modify origin url https://${DAGSHUB_USERNAME}:${DAGSHUB_TOKEN}@dagshub.com/aniketdesh004/Fraud_detection.dvc && \
    dvc pull
    
# 6. Open the port for the FastAPI web server
EXPOSE 8000

# 7. Start the server (pointing to the api folder)
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]