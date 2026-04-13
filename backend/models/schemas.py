# models/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any


# ── Step 1: Clinical Context ──────────────────────────────────────────────────

class ClinicalContextResponse(BaseModel):
    domain: str
    title: str
    problem: str
    goal: str
    target_column: str
    recommended_features: List[str]
    class_labels: Dict[str, str]
    example_dataset: str


# ── Step 2: Data Exploration ──────────────────────────────────────────────────

class ColumnInfo(BaseModel):
    name: str
    dtype: str
    missing_count: int
    missing_pct: float
    unique_count: int
    sample_values: List[Any]


class DatasetSummary(BaseModel):
    filename: str
    row_count: int
    column_count: int
    columns: List[ColumnInfo]
    class_distribution: Optional[Dict[str, int]] = None
    schema_ok: bool = False  # True after column mapper is saved


class ColumnMapping(BaseModel):
    """Sent by the frontend after the user maps columns in the modal."""
    target_column: str
    feature_columns: List[str]
    drop_columns: List[str] = []


class ColumnMappingResponse(BaseModel):
    schema_ok: bool
    message: str
    mapped_target: str
    mapped_features: List[str]
    class_distribution: Dict[str, int]


# ── Step 3: Data Preparation ──────────────────────────────────────────────────

class DataPrepRequest(BaseModel):
    missing_strategy: str = "mean"          # mean | median | mode | drop
    normalisation: str = "minmax"           # minmax | standard | none
    test_size: float = 0.2                  # 0.1 – 0.4
    apply_smote: bool = False
    random_state: int = 42


class DistributionBar(BaseModel):
    label: str
    before: float
    after: float


class DataPrepResponse(BaseModel):
    success: bool
    train_rows: int
    test_rows: int
    features_used: List[str]
    missing_handled: int                    # number of cells imputed / rows dropped
    normalisation_applied: str
    smote_applied: bool
    class_balance_before: Dict[str, int]
    class_balance_after: Dict[str, int]
    normalisation_chart: List[DistributionBar]   # before/after per feature
    class_balance_chart: List[DistributionBar]   # before/after class counts
    message: str


# ── Step 4: Model & Parameters ────────────────────────────────────────────────

class SVMParams(BaseModel):
    kernel: str = "linear"          # "linear" | "rbf"
    C: float = 1.0                  # regularisation strength
    gamma: str = "scale"            # "scale" | "auto" | float — only used for RBF

class RandomForestParams(BaseModel):
    n_estimators: int = 100         # number of trees (US-012)
    max_depth: Optional[int] = None
    random_state: int = 42

class KNNParams(BaseModel):
    n_neighbors: int = 5            # K value
    metric: str = "euclidean"       # "euclidean" | "manhattan" | "minkowski"

class DecisionTreeParams(BaseModel):
    max_depth: int = 5
    criterion: str = "gini"         # "gini" | "entropy"
    min_samples_split: int = 2

class LogisticRegressionParams(BaseModel):
    C: float = 1.0                  # regularisation strength
    solver: str = "lbfgs"           # "lbfgs" | "liblinear" | "saga"
    max_iter: int = 100

class NaiveBayesParams(BaseModel):
    var_smoothing: float = 1e-9     # variance smoothing

class TrainRequest(BaseModel):
    model: str                      # "svm" | "random_forest" | "knn" | "decision_tree" | "logistic_regression" | "naive_bayes"
    params: Dict[str, Any]          # validated per-model inside the router

class TrainResponse(BaseModel):
    model: str
    params_used: Dict[str, Any]
    accuracy: float
    precision: float
    recall: float
    f1: float
    specificity: Optional[float] = None
    auc: Optional[float] = None
    roc_curve: Optional[Dict[str, Any]] = None   # {"fpr": [...], "tpr": [...], "auc": float}
    confusion_matrix: List[List[int]]
    class_labels: List[str]
    message: str
    visualization: Optional[Dict[str, Any]] = None  # model-specific visualization data


# ── Step 6: Explainability ────────────────────────────────────────────────────

class FeatureImportanceRequest(BaseModel):
    top_n: int = 10
    domain: str = ""


class FeatureImportanceResponse(BaseModel):
    features: List[Dict[str, Any]]  # [{feature, display_name, importance}]
    clinical_sense_check: str
    domain: str
    model: str


class PatientPredictRequest(BaseModel):
    patient_index: int  # 0, 1, or 2 (maps to Patient A/B/C)


class PatientPredictResponse(BaseModel):
    patients: List[Dict[str, Any]]   # [{id, label, key_features}]
    selected_index: int
    prediction: str
    probability: float
    contributions: List[Dict[str, Any]]  # [{feature, display_name, value, contribution, direction}]
    top_feature: str
    top_feature_display: str


class WhatIfRequest(BaseModel):
    patient_index: int
    feature_name: str
    delta_std: float = 1.0  # shift by N standard deviations


class WhatIfResponse(BaseModel):
    original_probability: float
    new_probability: float
    delta: float
    direction: str   # "higher_risk" | "lower_risk" | "unchanged"
    feature_display: str


# ── Step 7: Ethics & Bias ─────────────────────────────────────────────────────

class SubgroupMetric(BaseModel):
    name: str
    n: int
    sensitivity: float
    specificity: float
    gap: float           # pp below overall sensitivity (negative = above)
    fairness_flag: str   # "OK" | "Review" | "⚠"


class BiasAnalysisResponse(BaseModel):
    overall_sensitivity: float
    subgroups: List[SubgroupMetric]
    bias_detected: bool


class PopulationCategory(BaseModel):
    label: str
    training_pct: float
    population_pct: float
    gap: float
    warn: bool


class PopulationComparisonResponse(BaseModel):
    categories: List[PopulationCategory]
    domain: str


class GenerateCertificateRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    checklist_status: List[bool]  # 8 items
    domain: str
    model_name: str
