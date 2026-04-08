# models/schemas.py
from pydantic import BaseModel
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
    schema_ok: bool = False


class ColumnMapping(BaseModel):
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
    missing_strategy: str = "mean"
    normalisation: str = "minmax"
    test_size: float = 0.2
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
    missing_handled: int
    normalisation_applied: str
    smote_applied: bool
    class_balance_before: Dict[str, int]
    class_balance_after: Dict[str, int]
    normalisation_chart: List[DistributionBar]
    class_balance_chart: List[DistributionBar]
    message: str


# ── Step 4: Model Parameters ──────────────────────────────────────────────────

class SVMParams(BaseModel):
    kernel: str = "linear"        # "linear" | "rbf"
    C: float = 1.0
    gamma: str = "scale"          # only used for rbf


class RandomForestParams(BaseModel):
    n_estimators: int = 100       # US-012: tree count
    max_depth: Optional[int] = None
    random_state: int = 42


class KNNParams(BaseModel):
    n_neighbors: int = 5          # K value
    metric: str = "euclidean"     # "euclidean" | "manhattan"


class DecisionTreeParams(BaseModel):
    max_depth: Optional[int] = 5
    criterion: str = "gini"       # "gini" | "entropy"
    random_state: int = 42


class LogisticRegressionParams(BaseModel):
    C: float = 1.0
    max_iter: int = 200
    random_state: int = 42


class NaiveBayesParams(BaseModel):
    var_smoothing: float = 1e-9


class TrainRequest(BaseModel):
    model: str                    # model id string
    params: Dict[str, Any]        # validated inside router per model


class TrainResponse(BaseModel):
    model: str
    params_used: Dict[str, Any]
    accuracy: float
    precision: float
    recall: float
    f1: float
    specificity: Optional[float] = None
    auc: Optional[float] = None
    roc_curve: Optional[Dict[str, Any]] = None
    confusion_matrix: List[List[int]]
    class_labels: List[str]
    message: str


# ── Step 5: Results ───────────────────────────────────────────────────────────

class ResultsResponse(BaseModel):
    model: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    specificity: Optional[float] = None
    auc: Optional[float] = None
    roc_curve: Optional[Dict[str, Any]] = None
    confusion_matrix: List[List[int]]
    class_labels: List[str]
    test_size: int


class CompareEntry(BaseModel):
    model: str
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    specificity: Optional[float] = None
    auc: Optional[float] = None
