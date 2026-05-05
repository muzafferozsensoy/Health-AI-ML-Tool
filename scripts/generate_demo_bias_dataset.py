"""
Generates `backend/data/samples/heart_disease_demo_bias.csv` for the Step 7
fairness demo. Starts from `test_cardiology.csv` and flips the heart_disease
label for ~70% of female (sex=0) patients aged >=60. This guarantees a
measurable sensitivity gap on the female elderly subgroup so the demo can
showcase a red bias badge.

Run once from the repo root:
    python scripts/generate_demo_bias_dataset.py
"""
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "test_cardiology.csv"
DEST = REPO_ROOT / "backend" / "data" / "samples" / "heart_disease_demo_bias.csv"


def main():
    df = pd.read_csv(SOURCE)
    mask = (df["sex"] == 0) & (df["age"] >= 60)
    flip_idx = df[mask].sample(frac=0.7, random_state=42).index
    df.loc[flip_idx, "heart_disease"] = 1 - df.loc[flip_idx, "heart_disease"]
    df.to_csv(DEST, index=False)
    print(f"Wrote {len(df)} rows to {DEST}")
    print(f"Flipped labels for {len(flip_idx)} female (sex=0, age>=60) patients")


if __name__ == "__main__":
    main()
