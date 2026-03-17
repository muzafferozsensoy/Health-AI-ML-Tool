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
