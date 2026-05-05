"""
End-to-end verification for the Step 7 fairness bug fix.
Runs the full Step 2 -> 3 -> 4 -> 7 pipeline against a live backend
and checks that the bias-analysis response contains multiple subgroups
(age + sex bins) and that demo CSV produces a >10pp gap row.
"""
import sys
from pathlib import Path
import requests

BASE = "http://127.0.0.1:8765/api"
REPO_ROOT = Path(__file__).resolve().parent.parent


def run_pipeline(csv_path: Path, label: str) -> dict:
    print(f"\n=== {label} ({csv_path.name}) ===")

    # Step 2 — upload
    with csv_path.open("rb") as fh:
        r = requests.post(
            f"{BASE}/step2/upload",
            files={"file": (csv_path.name, fh, "text/csv")},
            timeout=10,
        )
    r.raise_for_status()
    sid = r.headers["X-Session-Id"]
    summary = r.json()
    print(f"  uploaded: {summary['row_count']} rows, session={sid[:8]}")
    headers = {"X-Session-Id": sid}

    # Step 2 — column mapping
    feature_cols = [c["name"] for c in summary["columns"] if c["name"] != "heart_disease"]
    r = requests.post(
        f"{BASE}/step2/column-mapping",
        headers=headers,
        json={"target_column": "heart_disease", "feature_columns": feature_cols},
        timeout=5,
    )
    r.raise_for_status()
    print(f"  mapping saved: target=heart_disease, {len(feature_cols)} features")

    # Step 3 — prepare
    r = requests.post(
        f"{BASE}/step3/prepare",
        headers=headers,
        json={
            "missing_strategy": "median",
            "normalisation": "minmax",
            "test_size": 0.2,
            "random_state": 42,
            "apply_smote": False,
        },
        timeout=10,
    )
    r.raise_for_status()
    print(f"  data prepared (minmax scaling)")

    # Step 4 — train (KNN tends to surface bias more readily)
    r = requests.post(
        f"{BASE}/step4/train",
        headers=headers,
        json={"model": "knn", "params": {"n_neighbors": 5}},
        timeout=30,
    )
    r.raise_for_status()
    metrics = r.json().get("metrics", {})
    print(f"  trained: accuracy={metrics.get('accuracy')}, recall={metrics.get('recall')}")

    # Step 7 — bias analysis
    r = requests.get(f"{BASE}/step7/bias-analysis", headers=headers, timeout=10)
    r.raise_for_status()
    bias = r.json()
    print(f"  overall_sensitivity={bias['overall_sensitivity']}, bias_detected={bias['bias_detected']}")
    print(f"  subgroups ({len(bias['subgroups'])}):")
    for sg in bias["subgroups"]:
        flag = sg["fairness_flag"].encode("ascii", "replace").decode("ascii")
        print(
            f"    - {sg['name']:30s} N={sg['n']:3d} "
            f"sens={sg['sensitivity']:.3f} gap={sg['gap']:+.3f} flag={flag}"
        )
    return bias


def main():
    cardio_csv = REPO_ROOT / "test_cardiology.csv"
    demo_csv = REPO_ROOT / "backend" / "data" / "samples" / "heart_disease_demo_bias.csv"

    bias_real = run_pipeline(cardio_csv, "REAL DATA — bug fix sanity check")
    bias_demo = run_pipeline(demo_csv, "DEMO DATA — guaranteed bias showcase")

    # Assertions
    print("\n=== VERIFICATION ===")

    # 1. Real data should produce > 1 subgroup (was 1 with the bug)
    n_real = len(bias_real["subgroups"])
    assert n_real > 1, f"FAIL: real data still produces {n_real} subgroups (bug not fixed)"
    print(f"  PASS: real data produces {n_real} subgroups (>1, age+sex working)")

    # 2. Real data should have at least one age subgroup AND one sex subgroup
    names_real = [sg["name"] for sg in bias_real["subgroups"]]
    has_age = any("Age" in n for n in names_real)
    has_sex = any("sex=" in n for n in names_real)
    assert has_age, f"FAIL: no age subgroup in real data — names: {names_real}"
    assert has_sex, f"FAIL: no sex subgroup in real data — names: {names_real}"
    print(f"  PASS: both age AND sex subgroups present")

    # 3. Demo CSV should trigger bias_detected = True
    assert bias_demo["bias_detected"], "FAIL: demo CSV did not trigger bias_detected"
    print(f"  PASS: demo CSV triggers bias_detected=True")

    # 4. Demo CSV should have at least one row with >10pp gap (red flag)
    red_rows = [sg for sg in bias_demo["subgroups"] if sg["gap"] > 0.10]
    assert red_rows, f"FAIL: no red-flag rows in demo — subgroups: {bias_demo['subgroups']}"
    print(f"  PASS: demo CSV produces {len(red_rows)} red-flag row(s) for the demo presentation")

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
