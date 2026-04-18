"""Table builders."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_table(df: pd.DataFrame, stem: Path) -> None:
    """Export table in CSV and LaTeX formats."""
    stem.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(stem.with_suffix(".csv"), index=False)
    stem.with_suffix(".tex").write_text(df.to_latex(index=False, float_format="%.3f"), encoding="utf-8")
