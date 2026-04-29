# routers/step5_results.py
import numpy as np
from fastapi import APIRouter, HTTPException, Header
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix as sk_confusion_matrix,
    roc_auc_score, roc_curve as sk_roc_curve,
)

from services import session_store

router = APIRouter(prefix="/api/step5", tags=["Step 5 - Results"])


@router.get(
    "/results",
    summary="Get full results for the last trained model",
)
def get_results(x_session_id: str = Header(...)):
    """
    Returns all metrics, confusion matrix, and ROC curve for the trained model.
    Gate: train_complete must be True (model must be trained in Step 4 first).

    Note: The Step 5 frontend component primarily reads from the model store
    (populated by the Step 4 train response). This endpoint provides a
    fallback REST interface for the same data.
    """
    session = session_store.get(x_session_id)

    if not session.get("train_complete", False):
        raise HTTPException(
            status_code=403,
            detail="Step 5 is locked. Please train a model in Step 4 first.",
        )

    model        = session.get("trained_model")
    X_test       = session.get("X_test")
    y_test       = session.get("y_test")
    class_labels = session.get("class_labels", [])
    model_name   = session.get("model_name", "unknown")
    metrics      = session.get("last_metrics", {})

    if model is None or X_test is None or y_test is None:
        raise HTTPException(
            status_code=400,
            detail="No trained model found in session. Please complete Step 4.",
        )

    # Re-compute predictions for full response
    y_pred = model.predict(X_test)
    is_binary = len(class_labels) == 2
    avg = "binary" if is_binary else "weighted"
    pos_lbl = class_labels[-1] if is_binary else None

    accuracy  = round(float(accuracy_score(y_test, y_pred)), 4)
    precision = round(float(precision_score(y_test, y_pred, average=avg, pos_label=pos_lbl, zero_division=0)), 4)
    recall    = round(float(recall_score(y_test, y_pred, average=avg, pos_label=pos_lbl, zero_division=0)), 4)
    f1        = round(float(f1_score(y_test, y_pred, average=avg, pos_label=pos_lbl, zero_division=0)), 4)
    cm        = sk_confusion_matrix(y_test, y_pred).tolist()

    # Specificity
    specificity_val = metrics.get("specificity")

    # AUC & ROC curve
    auc_val = metrics.get("auc")
    roc_curve_data = None
    try:
        y_proba = model.predict_proba(X_test)
        if is_binary:
            auc_val = round(float(roc_auc_score(y_test, y_proba[:, 1])), 4)
            fpr, tpr, _ = sk_roc_curve(y_test, y_proba[:, 1], pos_label=pos_lbl)
            roc_curve_data = {
                "fpr": [round(float(v), 4) for v in fpr],
                "tpr": [round(float(v), 4) for v in tpr],
                "auc": auc_val,
            }
        else:
            auc_val = round(float(roc_auc_score(y_test, y_proba, multi_class="ovr", average="weighted")), 4)
    except Exception:
        pass

    return {
        "model": model_name,
        "metrics": {
            "accuracy":    accuracy,
            "precision":   precision,
            "recall":      recall,
            "f1":          f1,
            "specificity": specificity_val,
            "auc":         auc_val,
        },
        "confusion_matrix": cm,
        "roc_curve":        roc_curve_data,
        "class_labels":     class_labels,
        "test_size":        int(len(y_test)),
    }


@router.post(
    "/compare",
    summary="Add current model metrics to comparison table",
)
def add_to_comparison(x_session_id: str = Header(...)):
    """
    Saves current model metrics to the session comparison list.
    Frontend calls this when user clicks '+ Compare'.
    """
    session = session_store.get(x_session_id)

    if not session.get("train_complete", False):
        raise HTTPException(
            status_code=403,
            detail="No trained model to compare. Please train a model in Step 4 first.",
        )

    metrics    = session.get("last_metrics", {})
    model_name = session.get("model_name", "unknown")

    entry = {
        "model":       model_name,
        "accuracy":    metrics.get("accuracy"),
        "precision":   metrics.get("precision"),
        "recall":      metrics.get("recall"),
        "f1":          metrics.get("f1"),
        "specificity": metrics.get("specificity"),
        "auc":         metrics.get("auc"),
    }

    comparison = session.get("comparison_table", [])
    comparison.append(entry)
    session_store.set(x_session_id, "comparison_table", comparison)

    return {
        "message":          f"{model_name} added to comparison table.",
        "comparison_count": len(comparison),
        "comparison_table": comparison,
    }


@router.get(
    "/compare",
    summary="Get the full model comparison table",
)
def get_comparison(x_session_id: str = Header(...)):
    """Returns all models added to the comparison table this session."""
    session    = session_store.get(x_session_id)
    comparison = session.get("comparison_table", [])
    return {"comparison_table": comparison, "count": len(comparison)}


@router.delete(
    "/compare",
    summary="Clear the comparison table",
)
def clear_comparison(x_session_id: str = Header(...)):
    session_store.set(x_session_id, "comparison_table", [])
    return {"message": "Comparison table cleared."}
