# routers/step4_model_params.py
import numpy as np
from fastapi import APIRouter, HTTPException, Header
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix as sk_confusion_matrix,
    roc_auc_score, roc_curve as sk_roc_curve,
)

from services import session_store
from models.schemas import (
    TrainRequest, TrainResponse,
    SVMParams, RandomForestParams,
    KNNParams, DecisionTreeParams,
    LogisticRegressionParams, NaiveBayesParams,
)

router = APIRouter(prefix="/api/step4", tags=["Step 4 - Model & Parameters"])

SUPPORTED_MODELS = {
    "svm", "random_forest", "knn",
    "decision_tree", "logistic_regression", "naive_bayes"
}


# ── Model builders ────────────────────────────────────────────────────────────

def _train_svm(raw_params: dict):
    """US-011: SVM Kernel Selection. When kernel=RBF, C and gamma apply."""
    try:
        p = SVMParams(**raw_params)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid SVM params: {exc}")

    if p.kernel not in {"linear", "rbf"}:
        raise HTTPException(status_code=422, detail=f"Invalid kernel '{p.kernel}'. Choose 'linear' or 'rbf'.")
    if p.C <= 0:
        raise HTTPException(status_code=422, detail=f"C must be > 0 (got {p.C}).")

    model_kwargs = {"kernel": p.kernel, "C": p.C, "probability": True}
    if p.kernel == "rbf":
        model_kwargs["gamma"] = p.gamma
    model = SVC(**model_kwargs)
    params_used = {k: v for k, v in model_kwargs.items() if k != "probability"}
    return model, params_used


def _train_random_forest(raw_params: dict):
    """US-012: Random Forest Tree Count Tuning."""
    try:
        p = RandomForestParams(**raw_params)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid Random Forest params: {exc}")

    if not (1 <= p.n_estimators <= 1000):
        raise HTTPException(status_code=422, detail=f"n_estimators must be 1–1000 (got {p.n_estimators}).")

    model = RandomForestClassifier(
        n_estimators=p.n_estimators,
        max_depth=p.max_depth,
        random_state=p.random_state,
    )
    params_used = {"n_estimators": p.n_estimators, "max_depth": p.max_depth, "random_state": p.random_state}
    return model, params_used


def _train_knn(raw_params: dict):
    """KNN — K-Nearest Neighbors. Finds K most similar past patients."""
    try:
        p = KNNParams(**raw_params)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid KNN params: {exc}")

    if not (1 <= p.n_neighbors <= 50):
        raise HTTPException(status_code=422, detail=f"n_neighbors must be 1–50 (got {p.n_neighbors}).")

    model = KNeighborsClassifier(
        n_neighbors=p.n_neighbors,
        metric=p.metric,
    )
    params_used = {"n_neighbors": p.n_neighbors, "metric": p.metric}
    return model, params_used


def _train_decision_tree(raw_params: dict):
    """Decision Tree — Series of yes/no questions to classify patients."""
    try:
        p = DecisionTreeParams(**raw_params)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid Decision Tree params: {exc}")

    model = DecisionTreeClassifier(
        max_depth=p.max_depth,
        criterion=p.criterion,
        random_state=p.random_state,
    )
    params_used = {"max_depth": p.max_depth, "criterion": p.criterion, "random_state": p.random_state}
    return model, params_used


def _train_logistic_regression(raw_params: dict):
    """Logistic Regression — Estimates probability of each class."""
    try:
        p = LogisticRegressionParams(**raw_params)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid Logistic Regression params: {exc}")

    model = LogisticRegression(
        C=p.C,
        max_iter=p.max_iter,
        random_state=p.random_state,
    )
    params_used = {"C": p.C, "max_iter": p.max_iter, "random_state": p.random_state}
    return model, params_used


def _train_naive_bayes(raw_params: dict):
    """Naive Bayes — Probabilistic classifier based on Bayes theorem."""
    try:
        p = NaiveBayesParams(**raw_params)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid Naive Bayes params: {exc}")

    model = GaussianNB(var_smoothing=p.var_smoothing)
    params_used = {"var_smoothing": p.var_smoothing}
    return model, params_used


# ── Evaluation helper ─────────────────────────────────────────────────────────

def _evaluate(model, X_test, y_test, y_train, class_labels):
    """Compute all metrics: accuracy, precision, recall, F1, specificity, AUC, ROC, confusion matrix."""
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
    specificity_val = None
    try:
        cm_arr = np.array(cm)
        if cm_arr.shape == (2, 2):
            tn, fp = cm_arr[0, 0], cm_arr[0, 1]
            specificity_val = round(float(tn / (tn + fp)), 4) if (tn + fp) > 0 else 0.0
        else:
            spec_sum, weight_sum = 0.0, 0.0
            for i in range(cm_arr.shape[0]):
                tp_i = cm_arr[i, i]
                tn_i = cm_arr.sum() - cm_arr[i, :].sum() - cm_arr[:, i].sum() + tp_i
                fp_i = cm_arr[:, i].sum() - tp_i
                denom = tn_i + fp_i
                spec_i = tn_i / denom if denom > 0 else 0.0
                class_count = cm_arr[i, :].sum()
                spec_sum += spec_i * class_count
                weight_sum += class_count
            specificity_val = round(float(spec_sum / weight_sum), 4) if weight_sum > 0 else 0.0
    except Exception:
        pass

    # AUC & ROC curve
    auc_val = None
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

    return accuracy, precision, recall, f1, specificity_val, auc_val, roc_curve_data, cm


# ── Train endpoint ────────────────────────────────────────────────────────────

@router.post(
    "/train",
    response_model=TrainResponse,
    summary="Train any of the 6 ML models with selected parameters",
)
def train_model(
    request: TrainRequest,
    x_session_id: str = Header(...),
):
    """
    Trains the selected model using prepared data from Step 3.
    Gate: requires prep_complete = True.

    Supported models: svm, random_forest, knn, decision_tree, logistic_regression, naive_bayes
    """
    session = session_store.get(x_session_id)

    if not session.get("prep_complete", False):
        raise HTTPException(
            status_code=403,
            detail="Step 4 is locked. Please complete Data Preparation in Step 3 first.",
        )

    if request.model not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported model '{request.model}'. Choose from: {sorted(SUPPORTED_MODELS)}",
        )

    df         = session.get("df_raw")
    target_col = session.get("target_column")
    feature_cols = session.get("feature_columns")
    prep_req   = session.get("prep_request")

    if df is None or not target_col or not feature_cols or prep_req is None:
        raise HTTPException(status_code=400, detail="Session data incomplete. Complete Steps 2 and 3 first.")

    from services.train_service import get_splits
    X_train, X_test, y_train, y_test = get_splits(df, target_col, feature_cols, prep_req)

    # Validate target is categorical
    n_unique = len(np.unique(y_train))
    if n_unique > 20:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Target column '{target_col}' has {n_unique} unique values and appears continuous. "
                f"Please select a categorical target column (e.g. 0/1, Yes/No) in Step 2."
            ),
        )

    # Build model
    builders = {
        "svm":                  _train_svm,
        "random_forest":        _train_random_forest,
        "knn":                  _train_knn,
        "decision_tree":        _train_decision_tree,
        "logistic_regression":  _train_logistic_regression,
        "naive_bayes":          _train_naive_bayes,
    }
    model, params_used = builders[request.model](request.params)

    try:
        model.fit(X_train, y_train)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}")

    class_labels = [str(c) for c in sorted(np.unique(np.concatenate([y_train, y_test])))]
    accuracy, precision, recall, f1, specificity_val, auc_val, roc_curve_data, cm = _evaluate(
        model, X_test, y_test, y_train, class_labels
    )

    # Persist for Step 5
    session_store.set(x_session_id, "trained_model", model)
    session_store.set(x_session_id, "model_name", request.model)
    session_store.set(x_session_id, "class_labels", class_labels)
    session_store.set(x_session_id, "X_test", X_test)
    session_store.set(x_session_id, "y_test", y_test)
    session_store.set(x_session_id, "train_complete", True)
    session_store.set(x_session_id, "last_metrics", {
        "accuracy": accuracy, "precision": precision,
        "recall": recall, "f1": f1,
        "specificity": specificity_val, "auc": auc_val,
    })

    return TrainResponse(
        model=request.model,
        params_used=params_used,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        specificity=specificity_val,
        auc=auc_val,
        roc_curve=roc_curve_data,
        confusion_matrix=cm,
        class_labels=class_labels,
        message=(
            f"{request.model.replace('_', ' ').title()} trained successfully. "
            f"Accuracy: {accuracy * 100:.1f}%"
        ),
    )


# ── Options endpoint ──────────────────────────────────────────────────────────

@router.get("/options", summary="Return all 6 models and their configurable parameters")
def get_model_options():
    return {
        "models": [
            {
                "id": "knn",
                "label": "K-Nearest Neighbors (KNN)",
                "params": [
                    {
                        "key": "n_neighbors",
                        "label": "K — Number of Similar Patients",
                        "type": "slider",
                        "min": 1, "max": 25, "step": 1, "default": 5,
                    },
                    {
                        "key": "metric",
                        "label": "Distance Measure",
                        "type": "select",
                        "options": [
                            {"value": "euclidean", "label": "Euclidean (straight-line distance)"},
                            {"value": "manhattan", "label": "Manhattan (city-block distance)"},
                        ],
                        "default": "euclidean",
                    },
                ],
            },
            {
                "id": "svm",
                "label": "Support Vector Machine (SVM)",
                "params": [
                    {
                        "key": "kernel",
                        "label": "Kernel",
                        "type": "select",
                        "options": [
                            {"value": "linear", "label": "Linear"},
                            {"value": "rbf",    "label": "RBF (Radial Basis Function)"},
                        ],
                        "default": "linear",
                        "triggers_params": {"rbf": ["C", "gamma"]},
                    },
                    {
                        "key": "C",
                        "label": "Regularisation (C)",
                        "type": "slider",
                        "min": 0.01, "max": 100.0, "step": 0.01, "default": 1.0,
                    },
                    {
                        "key": "gamma",
                        "label": "Gamma",
                        "type": "select",
                        "options": [
                            {"value": "scale", "label": "Scale (default)"},
                            {"value": "auto",  "label": "Auto"},
                        ],
                        "default": "scale",
                        "visible_when": {"kernel": ["rbf"]},
                    },
                ],
            },
            {
                "id": "decision_tree",
                "label": "Decision Tree",
                "params": [
                    {
                        "key": "max_depth",
                        "label": "Max Tree Depth",
                        "type": "slider",
                        "min": 1, "max": 20, "step": 1, "default": 5,
                        "nullable": True,
                    },
                    {
                        "key": "criterion",
                        "label": "Split Criterion",
                        "type": "select",
                        "options": [
                            {"value": "gini",    "label": "Gini Impurity"},
                            {"value": "entropy", "label": "Information Gain (Entropy)"},
                        ],
                        "default": "gini",
                    },
                    {
                        "key": "random_state",
                        "label": "Random State (seed)",
                        "type": "number",
                        "default": 42,
                    },
                ],
            },
            {
                "id": "random_forest",
                "label": "Random Forest",
                "params": [
                    {
                        "key": "n_estimators",
                        "label": "Number of Trees",
                        "type": "slider",
                        "min": 10, "max": 500, "step": 10, "default": 100,
                    },
                    {
                        "key": "max_depth",
                        "label": "Max Tree Depth",
                        "type": "slider",
                        "min": 1, "max": 50, "step": 1, "default": None,
                        "nullable": True,
                    },
                    {
                        "key": "random_state",
                        "label": "Random State (seed)",
                        "type": "number",
                        "default": 42,
                    },
                ],
            },
            {
                "id": "logistic_regression",
                "label": "Logistic Regression",
                "params": [
                    {
                        "key": "C",
                        "label": "Regularisation (C)",
                        "type": "slider",
                        "min": 0.01, "max": 10.0, "step": 0.01, "default": 1.0,
                    },
                    {
                        "key": "max_iter",
                        "label": "Max Iterations",
                        "type": "slider",
                        "min": 100, "max": 1000, "step": 100, "default": 200,
                    },
                    {
                        "key": "random_state",
                        "label": "Random State (seed)",
                        "type": "number",
                        "default": 42,
                    },
                ],
            },
            {
                "id": "naive_bayes",
                "label": "Naïve Bayes",
                "params": [
                    {
                        "key": "var_smoothing",
                        "label": "Variance Smoothing",
                        "type": "select",
                        "options": [
                            {"value": 1e-9, "label": "1e-9 (default)"},
                            {"value": 1e-8, "label": "1e-8"},
                            {"value": 1e-7, "label": "1e-7"},
                        ],
                        "default": 1e-9,
                    },
                ],
            },
        ]
    }
