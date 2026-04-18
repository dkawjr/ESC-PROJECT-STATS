"""Cleaning and audit logic."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def parse_reverse_map(key_df: pd.DataFrame) -> dict[str, bool]:
    """Parse reverse-scoring from Key sheet column E text."""
    var_col = key_df.columns[0]
    flag_col = key_df.columns[4]
    out: dict[str, bool] = {}
    for _, row in key_df.iterrows():
        text = str(row[flag_col]).strip().lower()
        if "strongly agree =" not in text:
            continue
        item = str(row[var_col]).strip()
        out[item] = "negative attitude" in text
    return out


def build_codebook(key_df: pd.DataFrame) -> dict[str, dict[str, str | float]]:
    """Build a lightweight codebook dictionary from the Key sheet."""
    col0, col1, col2, col3 = key_df.columns[:4]
    codebook: dict[str, dict[str, str | float]] = {}
    current_var: str | None = None
    for _, row in key_df.iterrows():
        var = row[col0]
        if pd.notna(var):
            current_var = str(var).strip()
            codebook[current_var] = {"type": str(row[col1]).strip() if pd.notna(row[col1]) else ""}
        if current_var and pd.notna(row[col2]) and pd.notna(row[col3]):
            codebook[current_var][str(row[col2]).strip()] = float(row[col3])
    return codebook


def coerce_types(data_df: pd.DataFrame) -> pd.DataFrame:
    """Coerce analysis dtypes to study specification."""
    out = data_df.copy()
    knowledge_cols = [
        c for c in out.columns if "Knowledge: Question" in c and ("Question 5" in c or "Question 6" in c or "Question 7" in c or "Question 8" in c or "Question 9" in c or "Question 10" in c)
    ]
    for col in knowledge_cols:
        out[col] = pd.array(out[col], dtype="Int8")
    likert_cols = [c for c in out.columns if "Comfort" in c or "Attitude" in c]
    for col in likert_cols:
        out[col] = pd.Categorical(out[col], categories=[1, 2, 3, 4, 5], ordered=True)
    if "Years in Practice" in out.columns:
        out["Years in Practice"] = out["Years in Practice"].astype("float64")
    return out


def add_reverse_columns(df: pd.DataFrame, reverse_map: dict[str, bool]) -> pd.DataFrame:
    """Create *_rev columns for flagged Likert variables."""
    out = df.copy()
    for col, reverse in reverse_map.items():
        if col not in out.columns:
            continue
        numeric = pd.to_numeric(out[col].astype("object"), errors="coerce")
        if reverse:
            out[f"{col}__rev"] = 6 - numeric
        else:
            out[f"{col}__rev"] = numeric
    return out


def missingness_audit(df: pd.DataFrame) -> dict[str, object]:
    """Return per-variable and per-participant missingness counts."""
    by_var = df.isna().sum().to_dict()
    by_participant = (
        pd.DataFrame({"Participant ID": df["Participant ID"], "missing_count": df.isna().sum(axis=1)})
        .set_index("Participant ID")["missing_count"]
        .to_dict()
    )
    return {
        "n_participants_data_sheet": int(df.shape[0]),
        "expected_n": 23,
        "n_discrepancy_note": "If prior document states n=24, this workbook confirms n=23.",
        "missing_by_variable": {k: int(v) for k, v in by_var.items()},
        "missing_by_participant": {k: int(v) for k, v in by_participant.items()},
        "total_missing_cells": int(df.isna().sum().sum()),
    }


def save_json(payload: dict[str, object], path: Path) -> None:
    """Save JSON payload with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
