<p align="center">
  <h1 align="center">🤖 Ask Me Anything — AI Chatbot</h1>
  <p align="center">
    A production-ready AI chatbot powered by <strong>Mistral AI</strong> &amp; <strong>Streamlit</strong>, fully containerized with Docker and deployable across multiple platforms.
  </p>
</p>


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Mistral_AI-5A67D8?logo=ai&logoColor=white" alt="Mistral AI">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/AWS_Lambda-FF9900?logo=awslambda&logoColor=white" alt="AWS Lambda">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white" alt="Grafana">
</p>

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
- [Deployment Options](#-deployment-options)
- [Monitoring](#-monitoring)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Environment Variables](#-environment-variables)
- [License](#-license)

---

## ✨ Features

- 💬 **Conversational AI** — Multi-turn chat powered by Mistral AI (`mistral-large-latest`)
- 🎨 **Polished UI** — Custom-styled Streamlit interface with gradient headers, rounded chat bubbles, and modern typography (Inter font)
- 🐳 **Dockerized** — Fully containerized with health checks and optimized layer caching
- ☸️ **Kubernetes Ready** — Includes K8s deployment & service manifests for scalable orchestration
- ⚡ **Serverless Option** — AWS Lambda + API Gateway handler via SAM template
- 📊 **Built-in Monitoring** — Prometheus metrics (request count, response latency) with Grafana dashboards
- 🔄 **CI/CD** — GitHub Actions workflow to auto-build and push Docker images to Docker Hub

---

## 🏗 Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────┐
│   User       │────▶│  Streamlit App   │────▶│  Mistral AI   │
│  (Browser)   │◀────│  (port 8501)     │◀────│    API        │
└──────────────┘     └───────┬──────────┘     └───────────────┘
                             │
                     ┌───────▼──────────┐
                     │ Prometheus Client │
                     │  (port 8000)      │
                     └───────┬──────────┘
                             │
                     ┌───────▼──────────┐     ┌───────────────┐
                     │   Prometheus     │────▶│    Grafana     │
                     │  (port 9090)     │     │  (port 3000)  │
                     └──────────────────┘     └───────────────┘
```

---

## 📁 Project Structure

```
Chatbot/
├── .github/
│   └── workflows/
│       └── docker.yml          # CI/CD — build & push image to Docker Hub
├── k8s/
│   ├── deployment.yml          # Kubernetes Deployment (2 replicas)
│   └── service.yml             # Kubernetes Service (NodePort)
├── lambda/
│   ├── app.py                  # AWS Lambda handler for serverless deployment
│   └── requirements.txt        # Lambda-specific dependencies
├── monitoring/
│   └── prometheus.yml          # Prometheus scrape config
├── app.py                      # Main Streamlit chatbot application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Compose stack (app + Prometheus + Grafana)
├── template.yaml               # AWS SAM template for Lambda deployment
├── .env                        # Environment variables (API keys)
├── .dockerignore               # Files excluded from Docker build
└── .gitignore                  # Files excluded from version control
```

---

## 🔧 Prerequisites

- **Python 3.11+**
- **Docker** & **Docker Compose** (for containerized deployment)
- **Mistral AI API Key** — Get one at [console.mistral.ai](https://console.mistral.ai/)
- *(Optional)* **kubectl** — for Kubernetes deployment
- *(Optional)* **AWS SAM CLI** — for Lambda deployment

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AKSHYRAM408/Chatbot-Dockers-.git
cd Chatbot-Dockers-
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 3. Run Locally (without Docker)

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will be available at **http://localhost:8501**

### 4. Run with Docker Compose (Recommended)

This starts the chatbot along with the full monitoring stack:

```bash
docker compose up --build
```

| Service    | URL                        |
|------------|----------------------------|
| Chatbot    | http://localhost:8501       |
| Prometheus | http://localhost:9090       |
| Grafana    | http://localhost:3000       |

> **Grafana default credentials:** `admin` / `admin`

---

## 🌐 Deployment Options

### 🐳 Docker (Railway / Any Cloud)

```bash
docker build -t chatbot .
docker run -p 8501:8501 --env-file .env chatbot
```

### ☸️ Kubernetes

```bash
# Update the MISTRAL_API_KEY in k8s/deployment.yml, then:
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
```

The deployment creates **2 replicas** exposed via a **NodePort** service on port `8501`.

### ⚡ AWS Lambda (Serverless)

Uses the AWS SAM template for deployment:

```bash
# Update MISTRAL_API_KEY in template.yaml, then:
sam build
sam deploy --guided
```

This creates an API Gateway endpoint at `/chat` that accepts `POST` requests:

```bash
curl -X POST https://your-api-url/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

---

## 📊 Monitoring

The application exports **Prometheus metrics** on port `8000`:

| Metric                       | Type      | Description                 |
|------------------------------|-----------|-----------------------------|
| `chatbot_requests_total`     | Counter   | Total number of chat requests |
| `chatbot_response_seconds`   | Histogram | Response latency in seconds  |

### Setting Up Grafana Dashboards

1. Open Grafana at **http://localhost:3000**
2. Add **Prometheus** as a data source (`http://prometheus:9090`)
3. Create a dashboard with panels for:
   - Request rate: `rate(chatbot_requests_total[5m])`
   - Average response time: `rate(chatbot_response_seconds_sum[5m]) / rate(chatbot_response_seconds_count[5m])`
   - Response time percentiles: `histogram_quantile(0.95, rate(chatbot_response_seconds_bucket[5m]))`

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/docker.yml`) automatically:

1. **Triggers** on every push to the `master` branch
2. **Builds** the Docker image from the Dockerfile
3. **Pushes** the image to Docker Hub as `akshyram/chatbot:latest`

### Required GitHub Secrets

| Secret               | Description              |
|----------------------|--------------------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN`    | Docker Hub access token  |

---

## 🔐 Environment Variables

| Variable          | Required | Description                            |
|-------------------|----------|----------------------------------------|
| `MISTRAL_API_KEY` | ✅ Yes   | API key from Mistral AI console        |

> ⚠️ **Never commit your `.env` file or API keys to version control.** The `.gitignore` is already configured to exclude it.

---

## 🛠 Tech Stack

| Technology       | Purpose                          |
|------------------|----------------------------------|
| Streamlit        | Web UI framework                 |
| Mistral AI       | LLM API for chat completions     |
| Docker           | Containerization                 |
| Docker Compose   | Multi-container orchestration    |
| Kubernetes       | Container orchestration at scale |
| AWS Lambda + SAM | Serverless deployment            |
| Prometheus       | Metrics collection               |
| Grafana          | Metrics visualization            |
| GitHub Actions   | CI/CD pipeline                   |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---





































































































































































































































































































