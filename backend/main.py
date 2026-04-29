# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    step1_clinical_context,
    step2_data_exploration,
    step3_data_preparation,
    step4_model_params,
    step5_results,
    step6_explainability,
    step7_ethics_bias,
)

app = FastAPI(
    title="HEALTH-AI ML Visualisation Tool — Backend",
    description=(
        "REST API for the Erasmus+ KA220-HED HEALTH-AI project. "
        "Sprint 4: Full 7-step ML pipeline (Steps 1–7)."
    ),
    version="0.4.0",
)

# ── CORS (allow the React/Next dev server) ────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten to your frontend URL in production
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
app.include_router(step6_explainability.router)
app.include_router(step7_ethics_bias.router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Meta"])
def health():
    return {"status": "ok", "sprint": 4, "steps_implemented": [1, 2, 3, 4, 5, 6, 7]}


@app.get("/", tags=["Meta"])
def root():
    return {
        "message": "HEALTH-AI Backend is running.",
        "docs": "/docs",
        "redoc": "/redoc",
    }
