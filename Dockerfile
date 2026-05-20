# 1. Use an official, lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only requirements first (to leverage Docker caching)
COPY requirements.txt .

# 4. Install git! 'python:slim' doesn't have it, and DVC secretly needs it.
RUN apt-get update && apt-get install -y git && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project
COPY . .

# 6. MLOps Magic: Pull the actual ML model from DagsHub
ARG DAGSHUB_USERNAME
ARG DAGSHUB_TOKEN

# THE SILVER BULLET: Disable Git checks, inject credentials directly, and pull!
RUN dvc config core.no_scm true && \
    dvc remote modify origin url https://${DAGSHUB_USERNAME}:${DAGSHUB_TOKEN}@dagshub.com/aniketdesh004/Fraud_detection.dvc && \
    dvc pull

# 7. Open the port for the FastAPI web server
EXPOSE 8000

# 8. Start the server (pointing to the api folder)
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]