# 🛡️ FraudOps: Cloud-Native MLOps Fraud Detection Pipeline

<div align="center">

[![CI/CD Pipeline](https://github.com/Aniket-1201/Fraud_detection/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/Aniket-1201/Fraud_detection/actions)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Cloud_Hosting-000000.svg)](https://render.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg)](https://streamlit.io/)

**Live Application:** [View the Streamlit Command Center Here](https://frauddetection-ffeqnn9bpxyetcqreodepk.streamlit.app/)  
**API Endpoint:** [View the Render Backend Docs Here](https://fraud-detection-feod.onrender.com/docs)

<img style="max-width: 100%; height: auto;" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/103b019e-a21f-49b0-934c-5ac261aa05a8" />

</div>

## 📌 Executive Summary
An enterprise-grade Machine Learning Operations (MLOps) pipeline designed to detect anomalous financial transactions in real-time. Moving beyond static Jupyter Notebooks, this project bridges cross-OS development (ARM/x86) to systematically engineer, track, and deploy an **XGBoost classification model** across a distributed, fully decoupled cloud architecture.

## 📊 Business Impact & Metrics
* **Optimized for Recall:** Achieved **82.6% Recall** on financial data by utilizing SMOTE and adjusting `scale_pos_weight`, minimizing false negatives for critical security events.
* **Zero-Downtime CI/CD:** Reduced cross-OS integration failures to zero via Docker containerization and automated GitHub Actions testing prior to cloud deployments.

## 🏗️ The Cloud Architecture & Engineering Justification

This system is built for production scalability, strictly separating the frontend UI from the backend ML API.

* **1. The Client (Streamlit Community Cloud):** A lightweight, state-agnostic UI. It handles batch CSV inputs, utilizing dynamic REST API routing via environment variables (`API_URL`) to communicate with the backend.
* **2. The Brain (Render + Docker):** A headless FastAPI container. It houses the XGBoost model, exposes RESTful endpoints (`POST /predict`, `GET /logs`), and manages the centralized SQLite audit database.
* **3. Model Registry & Versioning (DVC & DagsHub):** Git tracks our lightweight `.dvc` pointers, while the heavy `xgb_model.json` artifacts are securely versioned in DagsHub's S3-compatible cloud storage.
* **4. Experiment Tracking (Weights & Biases):** Systematically tracked hyperparameter tuning to mathematically prove our V2 model maximized Recall against baseline thresholds.
* **5. Pipeline Observability (Evidently AI & Prefect):** Integrated Prefect for data orchestration and Evidently AI to simulate production monitoring, capturing statistical data drift across 31 features to automate retraining alerts.

## 🚀 Core Engineering Achievements

### 1. Headless CI/CD Model Retrieval ("The SCM-Bypass")
Cloud providers strip hidden `.git` folders during deployment builds, which natively breaks `dvc pull` commands. 
* **Solution:** Engineered a custom `Dockerfile` that injects Git into the Linux container, applies a global `core.no_scm true` bypass, and securely injects DagsHub authentication tokens directly into the remote URL. 
* **Impact:** The Render container autonomously authenticates and pulls massive ML models during the cloud build phase without requiring human intervention or a localized Git tree.

### 2. Strict Microservice Decoupling & State Management
Enforced a strict API contract. The frontend was stripped of all database logic and business rules (e.g., probability thresholding). The backend was upgraded with a secure `GET /logs` endpoint.
* **Impact:** The UI is now a completely stateless client. The FastAPI backend handles 100% of the state management and threshold decision-making, ensuring data consistency across any number of client instances.

## 💻 Tech Stack
* **Machine Learning:** Scikit-Learn, XGBoost, Pandas, SMOTE
* **Backend API:** FastAPI, Uvicorn, Pydantic, SQLite
* **Frontend UI:** Streamlit, Plotly, Requests
* **MLOps & CI/CD:** Docker, GitHub Actions, DVC, DagsHub, W&B, Prefect, Evidently AI
* **Cloud Infrastructure:** Render (Backend), Streamlit Community Cloud (Frontend)

## ⚙️ Quick Start (Local Reproduction)

To run this decoupled architecture locally:

**1. Clone the repository & pull artifacts**
```
git clone https://github.com/Aniket-1201/Fraud_detection.git
cd Fraud_detection
# Requires DagsHub access token exported in your environment
dvc pull
```

**2. Spin up the Backend API**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
# Start the API server
uvicorn api.app:app --reload --port 8000
```

**3. Setup the Frontend (Streamlit)**

*Open a new terminal window:*
```
# Ensure the API_URL points to your local backend
export API_URL="http://localhost:8000"
# Launch the dashboard
streamlit run dashboard.py
```
