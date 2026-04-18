"""I/O helpers for workbook loading and exports."""

from pathlib import Path

import pandas as pd

from .config import RAW_XLSX


def load_workbook(path: Path | None = None) -> dict[str, pd.DataFrame]:
    """Load all sheets from source workbook."""
    src = path or RAW_XLSX
    xl = pd.ExcelFile(src)
    return {name: xl.parse(name) for name in xl.sheet_names}


def save_df(df: pd.DataFrame, csv_path: Path, parquet_path: Path) -> None:
    """Save dataframe to CSV and parquet."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)
