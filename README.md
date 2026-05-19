# 🛡️ End-to-End MLOps Fraud Detection System

<div align="center">

[![CI/CD Pipeline](https://github.com/Aniket-1201/Fraud_detection/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/Aniket-1201/Fraud_detection/actions)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

An enterprise-grade Machine Learning Operations (MLOps) pipeline designed to detect anomalous credit card transactions. This project bridges cross-OS development environments (ARM/x86) to systematically engineer, track, deploy, and monitor an XGBoost model.

<img style="max-width: 100%; height: auto;" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/103b019e-a21f-49b0-934c-5ac261aa05a8" />

</div>

## 📊 Business Impact & Results
* **Optimized for Recall:** Achieved **82.6% Recall** on highly imbalanced financial data by utilizing SMOTE and adjusting `scale_pos_weight`, ensuring minimal false negatives for fraudulent transactions.
* **Zero-Downtime CI/CD:** Reduced cross-OS integration failures to zero by containerizing the prediction microservice.

## 🧠 The Architecture & Engineering Justification
Rather than building a static Jupyter Notebook, this system is designed for production scalability.

* **Data Versioning (DVC & DagsHub):** Standard Git cannot handle large ML binaries. We utilized DVC to decouple our data from our code. Git tracks our lightweight `.dvc` pointers, while the heavy `xgb_model.json` is securely versioned in DagsHub's S3-compatible cloud storage.
* **Experiment Tracking (Weights & Biases):** To handle extreme class imbalance (99% normal, 1% fraud), we utilized W&B to systematically track hyperparameter tuning, allowing us to mathematically prove our V2 model maximized Recall.
* **Cross-OS Automation (GitHub Actions):** To solve local dependency issues between macOS (M2 ARM) and Windows (x86), we engineered a CI/CD pipeline. Every push triggers an Ubuntu server to authenticate with DagsHub, pull the heavy model, and build a universal Docker container.
* **Model Serving (FastAPI & Docker):** The model is served via a highly modular, self-documenting FastAPI microservice, containerized for immediate cloud deployment.
* **Observability (Evidently AI):** Models degrade over time. We integrated Evidently AI to simulate production monitoring, capturing statistical data drift across 31 features to automate retraining alerts.

## 🚀 Quick Start (Local Reproduction)

To run this pipeline on your local machine:

**1. Clone the repository**
```bash
git clone https://github.com/Aniket-1201/Fraud_detection.git
cd Fraud_detection 
```

**2. Pull the ML Artifacts via DVC**
*(Note: Requires DagsHub access token exported in your environment)*
```bash
dvc pull
```

**3. Spin up the Backend API**
```bash
docker build -t fraud-api:v1 .
docker run -p 8000:8000 fraud-api:v1
```
*The API is now live at `http://localhost:8000/docs`*

**4. Launch the Streamlit Command Center**
Open a new terminal window:
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## 📂 Repository Structure
```text
Fraud_detection/
├── .github/workflows/   # CI/CD automated Docker builds
├── api/                 # FastAPI application and schemas
├── data/                # DVC tracked data pointers
├── models/              # DVC tracked XGBoost artifacts
├── monitoring/          # Evidently AI drift detection scripts
├── pipeline/            # Prefect data orchestration
├── dashboard.py         # Streamlit UI command center
├── Dockerfile           # Infrastructure as Code
└── requirements.txt     # Python dependencies
```
