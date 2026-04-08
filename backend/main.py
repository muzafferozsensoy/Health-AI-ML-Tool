# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    step1_clinical_context,
    step2_data_exploration,
    step3_data_preparation,
    step4_model_params,
    step5_results,
)

app = FastAPI(
    title="HEALTH-AI ML Visualisation Tool — Backend",
    description=(
        "REST API for the Erasmus+ KA220-HED HEALTH-AI project. "
        "Sprint 3: Steps 1–5 of the 7-step ML pipeline."
    ),
    version="0.3.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-Id"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(step1_clinical_context.router)
app.include_router(step2_data_exploration.router)
app.include_router(step3_data_preparation.router)
app.include_router(step4_model_params.router)
app.include_router(step5_results.router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Meta"])
def health():
    return {"status": "ok", "sprint": 3, "steps_implemented": [1, 2, 3, 4, 5]}


@app.get("/", tags=["Meta"])
def root():
    return {
        "message": "HEALTH-AI Backend is running.",
        "docs": "/docs",
        "redoc": "/redoc",
    }
