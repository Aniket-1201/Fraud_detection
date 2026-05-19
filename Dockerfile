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

ENV DAGSHUB_USERNAME=$DAGSHUB_USERNAME
ENV DAGSHUB_TOKEN=$DAGSHUB_TOKEN

# NEW: Added '-v' for verbose error tracking just in case!
RUN dvc remote modify origin --local auth basic && \
    dvc remote modify origin --local user $DAGSHUB_USERNAME && \
    dvc remote modify origin --local password $DAGSHUB_TOKEN && \
    dvc pull -v --no-scm

# 6. Open the port for the FastAPI web server
EXPOSE 8000

# 7. Start the server (pointing to the api folder)
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]