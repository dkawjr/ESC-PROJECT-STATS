"""Manuscript number injection helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from jinja2 import Template


RESULTS_TEMPLATE = """# Results

Primary outcomes were analyzed in paired pre-post format (n={{ n }} participants).
The knowledge total score changed from median {{ knowledge_pre_median }} pre to {{ knowledge_post_median }} post (exact p={{ knowledge_p }}).
The comfort domain score changed from median {{ comfort_pre_median }} to {{ comfort_post_median }} (exact p={{ comfort_p }}).
The attitude domain score changed from median {{ attitude_pre_median }} to {{ attitude_post_median }} (exact p={{ attitude_p }}).
"""


def generate_results_markdown(table_path: Path, cleaned_path: Path, out_path: Path) -> None:
    """Render results markdown from computed table and cleaned-domain values."""
    table = pd.read_csv(table_path)
    cleaned = pd.read_csv(cleaned_path)
    n = int(cleaned.shape[0])
    domain = table[table["family"] == "domain_primary"].copy()
    p_map = {
        row["outcome"]: row["p_exact"]
        for _, row in domain.iterrows()
        if pd.notna(row.get("p_exact"))
    }
    summary = {
        "n": n,
        "knowledge_pre_median": float(cleaned["knowledge_pre_total"].median()),
        "knowledge_post_median": float(cleaned["knowledge_post_total"].median()),
        "comfort_pre_median": float(cleaned["comfort_pre_total"].median()),
        "comfort_post_median": float(cleaned["comfort_post_total"].median()),
        "attitude_pre_median": float(cleaned["attitude_pre_total"].median()),
        "attitude_post_median": float(cleaned["attitude_post_total"].median()),
        "knowledge_p": f"{float(p_map.get('knowledge_total', float('nan'))):.4f}",
        "comfort_p": f"{float(p_map.get('comfort_domain', float('nan'))):.4g}",
        "attitude_p": f"{float(p_map.get('attitude_domain', float('nan'))):.4f}",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(Template(RESULTS_TEMPLATE).render(**summary), encoding="utf-8")
