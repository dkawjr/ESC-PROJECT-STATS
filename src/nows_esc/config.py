"""Global configuration for deterministic analysis."""

from pathlib import Path

GLOBAL_SEED = 20260418
ROOT = Path(__file__).resolve().parents[2]
RAW_XLSX = ROOT / "data" / "raw" / "NOWS_data__1_.xlsx"
