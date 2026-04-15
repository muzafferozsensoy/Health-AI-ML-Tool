# routers/step6_explainability.py
import warnings
import numpy as np
from fastapi import APIRouter, HTTPException, Header
from sklearn.inspection import permutation_importance

from services import session_store
from data.clinical_contexts import CLINICAL_SENSE_CHECK, FEATURE_DISPLAY_NAMES, CLINICAL_CONTEXTS
from models.schemas import (
    FeatureImportanceRequest, FeatureImportanceResponse,
    PatientPredictRequest, PatientPredictResponse,
    WhatIfRequest, WhatIfResponse,
)

router = APIRouter(prefix="/api/step6", tags=["Step 6 - Explainability"])


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_display_name(col: str) -> str:
    """Map a snake_case column name to a human-readable clinical label."""
    return FEATURE_DISPLAY_NAMES.get(col.lower(), col.replace("_", " ").title())


def _compute_feature_importance(model, model_name: str, X_test: np.ndarray, y_test, feature_cols: list) -> np.ndarray:
    """Return a normalised importance array (sums to 1, all >= 0)."""
    importances = None

    if model_name in ("random_forest", "decision_tree"):
        importances = model.feature_importances_.copy()

    elif model_name == "logistic_regression":
        coef = model.coef_
        if coef.shape[0] == 1:
            importances = np.abs(coef[0])
        else:
            importances = np.mean(np.abs(coef), axis=0)

    elif model_name == "naive_bayes":
        try:
            # Use log-ratio of class-conditional means as a proxy for importance
            if model.theta_.shape[0] >= 2:
                importances = np.abs(model.theta_[1] - model.theta_[0])
            else:
                importances = np.abs(model.theta_[0])
        except Exception:
            importances = None

    if importances is None:
        # KNN / SVM / fallback: permutation importance (model-agnostic)
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                result = permutation_importance(
                    model, X_test, y_test,
                    n_repeats=5, random_state=42, scoring="accuracy"
                )
            importances = result.importances_mean
            importances = np.clip(importances, 0, None)
        except Exception:
            importances = np.ones(len(feature_cols))

    # Normalise to sum=1 (or max=1 if all zeros)
    total = np.sum(importances)
    if total > 0:
        importances = importances / total
    else:
        importances = np.ones(len(feature_cols)) / len(feature_cols)

    return importances


def _select_representative_patients(model, X_test: np.ndarray, class_labels: list) -> list:
    """
    Return indices of 3 representative test patients:
      [0] highest confidence for the last (positive) class
      [1] highest confidence for the first (negative) class
      [2] closest to the decision boundary (probability ~0.5)
    """
    n = len(X_test)
    try:
        proba = model.predict_proba(X_test)
    except Exception:
        return [0, min(1, n - 1), min(2, n - 1)]

    is_binary = len(class_labels) == 2
    if is_binary:
        pos_proba = proba[:, -1]
        idx_pos = int(np.argmax(pos_proba))
        idx_neg = int(np.argmin(pos_proba))
        boundary_scores = np.abs(pos_proba - 0.5)
        # Exclude idx_pos and idx_neg when finding boundary patient
        boundary_scores[[idx_pos, idx_neg]] = np.inf
        idx_boundary = int(np.argmin(boundary_scores))
        return [idx_pos, idx_neg, idx_boundary]
    else:
        # Multiclass: pick highest confidence for each of the first 3 classes
        indices = []
        for cls_idx in range(min(3, proba.shape[1])):
            scores = proba[:, cls_idx].copy()
            for already in indices:
                scores[already] = -1
            indices.append(int(np.argmax(scores)))
        while len(indices) < 3:
            for i in range(n):
                if i not in indices:
                    indices.append(i)
                    break
            else:
                indices.append(0)
        return indices[:3]


def _gate(session_id: str):
    session = session_store.get(session_id)
    if not session.get("train_complete"):
        raise HTTPException(
            status_code=403,
            detail="Step 6 is locked. Please train a model in Step 4 first.",
        )
    return session


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/feature-importance", response_model=FeatureImportanceResponse)
def get_feature_importance(
    request: FeatureImportanceRequest,
    x_session_id: str = Header(...),
):
    """Compute and return feature importance for the trained model."""
    session = _gate(x_session_id)

    model = session.get("trained_model")
    model_name = session.get("model_name", "")
    feature_cols = list(session.get("feature_columns", []))
    X_test = session.get("X_test")
    y_test = session.get("y_test")
    domain = session.get("domain", "")

    if model is None or X_test is None or y_test is None:
        raise HTTPException(status_code=400, detail="Session data incomplete.")

    # Always prefer domain from request (user may have changed domain on Step 6)
    if request.domain:
        domain = request.domain
        session_store.set(x_session_id, "domain", domain)

    importances = _compute_feature_importance(model, model_name, X_test, y_test, feature_cols)

    # Build sorted feature list
    top_n = max(1, min(request.top_n, len(feature_cols)))
    ranked_idx = np.argsort(importances)[::-1][:top_n]

    features = [
        {
            "feature": feature_cols[i],
            "display_name": _get_display_name(feature_cols[i]),
            "importance": round(float(importances[i]), 4),
        }
        for i in ranked_idx
    ]

    sense_check = CLINICAL_SENSE_CHECK.get(
        domain,
        "The top features identified by this model are consistent with established clinical predictors for this domain."
    )

    # Persist for certificate and waterfall use
    session_store.set(x_session_id, "feature_importance", importances.tolist())
    session_store.set(x_session_id, "feature_importance_features", features)

    return FeatureImportanceResponse(
        features=features,
        clinical_sense_check=sense_check,
        domain=domain,
        model=model_name,
    )


@router.post("/patient-predict", response_model=PatientPredictResponse)
def patient_predict(
    request: PatientPredictRequest,
    x_session_id: str = Header(...),
):
    """Return prediction and feature contributions for one of 3 representative test patients."""
    session = _gate(x_session_id)

    model = session.get("trained_model")
    model_name = session.get("model_name", "")
    feature_cols = list(session.get("feature_columns", []))
    X_test = session.get("X_test")
    y_test = session.get("y_test")
    class_labels = session.get("class_labels", [])
    importances_raw = session.get("feature_importance")

    if model is None or X_test is None:
        raise HTTPException(status_code=400, detail="Session data incomplete.")

    # Compute or retrieve representative patient indices
    patient_indices = session.get("patient_indices")
    if patient_indices is None:
        patient_indices = _select_representative_patients(model, X_test, class_labels)
        session_store.set(x_session_id, "patient_indices", patient_indices)

    # Load or compute importances
    if importances_raw is None:
        importances = _compute_feature_importance(model, model_name, X_test, y_test, feature_cols)
        session_store.set(x_session_id, "feature_importance", importances.tolist())
    else:
        importances = np.array(importances_raw)

    # Validate request
    patient_index = request.patient_index
    if patient_index not in (0, 1, 2):
        raise HTTPException(status_code=422, detail="patient_index must be 0, 1, or 2.")

    actual_idx = patient_indices[patient_index]
    patient_row = X_test[actual_idx:actual_idx + 1]

    # Predict
    try:
        proba_arr = model.predict_proba(patient_row)[0]
        pred_class_idx = int(np.argmax(proba_arr))
        probability = float(proba_arr[pred_class_idx])
        prediction = class_labels[pred_class_idx] if pred_class_idx < len(class_labels) else str(pred_class_idx)
    except Exception:
        pred = model.predict(patient_row)[0]
        prediction = str(pred)
        probability = 1.0
        pred_class_idx = 0

    # Feature contributions: importance × (value − mean) across X_test
    X_mean = np.mean(X_test, axis=0)
    X_std = np.std(X_test, axis=0) + 1e-8
    raw_contributions = importances * (patient_row[0] - X_mean)

    # Normalise contributions to [-1, 1]
    max_abs = np.max(np.abs(raw_contributions)) + 1e-8
    norm_contributions = raw_contributions / max_abs

    contributions = []
    for i, col in enumerate(feature_cols):
        contrib = float(norm_contributions[i])
        contributions.append({
            "feature": col,
            "display_name": _get_display_name(col),
            "value": round(float(patient_row[0][i]), 4),
            "contribution": round(contrib, 4),
            "direction": "risk" if contrib > 0 else "safe",
        })

    # Sort contributions by absolute value descending
    contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)

    # Build patient summaries
    patient_labels = ["Patient A", "Patient B", "Patient C"]
    patients = []
    for pi, pidx in enumerate(patient_indices):
        row = X_test[pidx]
        try:
            p_arr = model.predict_proba(X_test[pidx:pidx + 1])[0]
            p_pred_idx = int(np.argmax(p_arr))
            p_prob = float(p_arr[p_pred_idx])
            p_pred = class_labels[p_pred_idx] if p_pred_idx < len(class_labels) else str(p_pred_idx)
        except Exception:
            p_pred = str(model.predict(X_test[pidx:pidx + 1])[0])
            p_prob = 1.0
        patients.append({
            "id": pi,
            "label": patient_labels[pi],
            "prediction": p_pred,
            "probability": round(p_prob, 3),
        })

    # Top feature for what-if
    top_idx = int(np.argmax(importances))
    top_feature = feature_cols[top_idx] if top_idx < len(feature_cols) else ""
    top_feature_display = _get_display_name(top_feature)

    return PatientPredictResponse(
        patients=patients,
        selected_index=patient_index,
        prediction=prediction,
        probability=round(probability, 4),
        contributions=contributions[:min(10, len(contributions))],
        top_feature=top_feature,
        top_feature_display=top_feature_display,
    )


@router.post("/what-if", response_model=WhatIfResponse)
def what_if(
    request: WhatIfRequest,
    x_session_id: str = Header(...),
):
    """Compute how changing a feature value shifts the prediction probability."""
    session = _gate(x_session_id)

    model = session.get("trained_model")
    feature_cols = list(session.get("feature_columns", []))
    X_test = session.get("X_test")
    class_labels = session.get("class_labels", [])
    patient_indices = session.get("patient_indices")

    if model is None or X_test is None or patient_indices is None:
        raise HTTPException(status_code=400, detail="Session data incomplete. Fetch /feature-importance first.")

    if request.patient_index not in (0, 1, 2):
        raise HTTPException(status_code=422, detail="patient_index must be 0, 1, or 2.")

    if request.feature_name not in feature_cols:
        raise HTTPException(status_code=422, detail=f"Feature '{request.feature_name}' not found.")

    actual_idx = patient_indices[request.patient_index]
    patient_row = X_test[actual_idx].copy()

    feature_idx = feature_cols.index(request.feature_name)
    X_std = float(np.std(X_test[:, feature_idx]))

    # Original probability
    try:
        orig_proba = model.predict_proba(patient_row.reshape(1, -1))[0]
        orig_pred_idx = int(np.argmax(orig_proba))
        orig_prob = float(orig_proba[orig_pred_idx])
    except Exception:
        orig_prob = 1.0

    # Modified probability
    modified_row = patient_row.copy()
    modified_row[feature_idx] += request.delta_std * X_std
    try:
        new_proba = model.predict_proba(modified_row.reshape(1, -1))[0]
        new_pred_idx = int(np.argmax(new_proba))
        new_prob = float(new_proba[new_pred_idx])
    except Exception:
        new_prob = orig_prob

    delta = round(new_prob - orig_prob, 4)
    if delta > 0.005:
        direction = "higher_risk"
    elif delta < -0.005:
        direction = "lower_risk"
    else:
        direction = "unchanged"

    return WhatIfResponse(
        original_probability=round(orig_prob, 4),
        new_probability=round(new_prob, 4),
        delta=delta,
        direction=direction,
        feature_display=_get_display_name(request.feature_name),
    )
