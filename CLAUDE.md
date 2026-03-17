# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HEALTH-AI is a full-stack ML visualization tool for healthcare education. It guides users through a 7-step workflow (Clinical Context → Data Exploration → Data Preparation → Model & Params → Results → Explainability → Ethics & Bias) across 10 healthcare domains (Cardiology, Nephrology, Oncology, Neurology, Diabetes, Pulmonology, Sepsis/ICU, Fetal Health, Dermatology, Stroke).

**Status:** Early scaffolding phase — architecture and UI designs are finalized but most implementation code is not yet written.

## Tech Stack

- **Frontend:** React 18 + Vite (JavaScript/JSX) — port 5173
- **Backend:** FastAPI + Python 3.10+ — port 8000
- **ML Engine:** scikit-learn (6 classifiers: KNN, SVM, Decision Tree, Random Forest, Logistic Regression, Naive Bayes)
- **Data:** CSV files only, no persistent database. Session-based processing.

## Build & Run Commands

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
API docs at http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Architecture

The system is stateless — the frontend holds session state via React useState/useReducer and Session Storage, and communicates with the backend via REST API calls.

**Backend services** (in `backend/`):
- `api/` — REST endpoints: `/api/upload`, `/api/preprocess`, `/api/train`, `/api/predict`, `/api/results`, `/api/explain`, `/api/certificate`
- `ml_engine/` — scikit-learn model wrappers and evaluation
- `data/` — default CSV datasets per healthcare domain

**Frontend** (in `frontend/src/`):
- `pages/` — one component per workflow step (7 steps)
- `components/` — reusable UI: Stepper, DomainPillBar, CSVUploadZone, ParameterSliders, VisualizationCharts, EthicsAndBiasPanel, Certificate
- `App.jsx` — main application entry point and routing

## External Resources

- **JIRA Board:** https://student-team-unknown-seng430.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog
- **Figma Prototype:** linked in `docs/wireframes/`
- **Architecture Diagram:** `docs/architecture/HEALTH-AI_Architecture_Diagram.drawio.pdf`
