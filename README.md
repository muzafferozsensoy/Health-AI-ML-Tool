# Health-AI-ML-Tool
# HEALTH-AI: ML Visualisation Tool for Healthcare

This repository contains the source code and documentation for the HEALTH-AI Machine Learning Visualisation Tool, developed as part of a 10-Week Agile development cycle.

## Repository Structure

Based on our system architecture, the repository is divided into frontend, backend, and documentation layers:

```text
HEALTH-AI-ML-Tool/
│
├── frontend/               # React 18 + Vite Application (UI Layer)
│   ├── src/
│   │   ├── components/     # Reusable UI components (Stepper, Sliders, Charts)
│   │   ├── pages/          # 7 Step screens (Clinical Context to Ethics & Bias)
│   │   └── App.jsx         # Main application routing
│   └── package.json        # Frontend dependencies
│
├── backend/                # FastAPI + Python Backend (API & ML Engine)
│   ├── api/                # REST API endpoints (upload, preprocess, train, predict)
│   ├── ml_engine/          # scikit-learn models (KNN, SVM, Decision Tree, etc.)
│   ├── data/               # Default domain CSV datasets (No persistent DB)
│   └── requirements.txt    # Python dependencies
│
├── docs/                   # Documentation & Design Assets
│   ├── architecture/       # Architecture diagrams
│   └── wireframes/         # Figma design exports
│
├── README.md               # Project overview and repository structure
└── SETUP.md                # Installation and local setup instructions (Skeleton)
```

## Quick Start with Docker

The fastest way to run the full stack locally is with Docker Compose:

```bash
docker compose up --build
```

Once both containers are healthy:

- **Frontend (nginx):** <http://localhost:80>
- **Backend (FastAPI):** <http://localhost:8000>
- **API docs (Swagger UI):** <http://localhost:8000/docs>

To stop and remove the containers:

```bash
docker compose down
```

## Local Development (without Docker)

See [`SETUP.md`](./SETUP.md) for the Python venv + npm workflow.

## Environment Variables

Each service ships with a `.env.example` documenting the variables it reads. Copy them before customising:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

| Variable | Service | Purpose |
|----------|---------|---------|
| `CORS_ORIGINS` | backend | Comma-separated whitelist of allowed origins |
| `PYTHONUNBUFFERED` | backend | Stream Python logs immediately |
| `VITE_API_URL` | frontend | Backend base URL (baked in at Vite build time) |

## Live Deployment

- **Frontend (Vercel):** _add deployed URL here_
- **Backend (Render):** _add deployed URL here_

The frontend is configured to deploy to Vercel (see `frontend/vercel.json`); the backend ships with `backend/render.yaml` for one-click Render deployment.
