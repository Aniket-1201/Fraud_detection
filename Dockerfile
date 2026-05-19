# 1. Use an official, lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only requirements first (to leverage Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the entire project (This brings in your api, pipeline, AND the .dvc configuration files)
COPY . .

# 5. MLOps Magic: Pull the actual ML model from DagsHub
# We use ARG to catch the secret token from Render, and ENV to expose it to DVC
ARG DAGSHUB_TOKEN
ENV DAGSHUB_TOKEN=$DAGSHUB_TOKEN
RUN dvc pull --no-scm

# 6. Open the port for the FastAPI web server
EXPOSE 8000

# 7. Start the server (pointing to the api folder)
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]