# 1. Use an official, lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file and install libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the modularized code and your model into the container
COPY api/ ./api/
COPY pipeline/ ./pipeline/
COPY models/xgb_model.json ./models/

# 5. Open the port for the FastAPI web server
EXPOSE 8000

# 6. Start the server (pointing to the api folder)
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
