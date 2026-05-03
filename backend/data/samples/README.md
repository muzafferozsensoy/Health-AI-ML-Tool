# Sample Datasets

This folder is intended for example CSV datasets used during demos and walkthroughs.

## Cardiology demo

For the live demo, place the UCI **Heart Failure Clinical Records** dataset here as:

```
backend/data/samples/heart_failure_clinical_records_dataset.csv
```

Source: <https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records>

The file is not committed to the repository because of dataset licensing. Download it manually before the demo.

## Adding more samples

For each domain in `backend/data/clinical_contexts.py`, the `example_dataset` field names the expected CSV file. Drop matching files into this folder and they can be referenced from the demo script.
