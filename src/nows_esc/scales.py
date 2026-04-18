"""Scale score construction and validation."""

from __future__ import annotations

import pandas as pd


def knowledge_items() -> tuple[list[str], list[str]]:
    """Return pre and post knowledge item columns for Q5-Q9."""
    pre = [f"Pre Simulation Knowledge: Question {i}" for i in range(5, 10)]
    post = [f"Post Simulation Knowledge: Question {i}" + (" " if i == 9 else "") for i in range(5, 10)]
    return pre, post


def comfort_items() -> tuple[list[str], list[str]]:
    """Return pre and post comfort item columns."""
    pre = [f"Pre Simulation Comfort: 11{x}" for x in "abcd"]
    post = [f"Post Simulation Comfort: 10{x}" for x in "abcd"]
    return pre, post


def attitude_items_rev() -> tuple[list[str], list[str]]:
    """Return reverse-transformed attitude columns."""
    pre = [f"Pre Simulation Attitude: 12{x}__rev" for x in "abcde"]
    post = [f"Post Simulation Attitude: 11{x}__rev" for x in "abcde"]
    return pre, post


def add_domain_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Compute total/domain pre-post scores."""
    out = df.copy()
    k_pre, k_post = knowledge_items()
    c_pre, c_post = comfort_items()
    a_pre, a_post = attitude_items_rev()
    out["knowledge_pre_total"] = out[k_pre].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    out["knowledge_post_total"] = out[k_post].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    out["comfort_pre_total"] = out[c_pre].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    out["comfort_post_total"] = out[c_post].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    out["attitude_pre_total"] = out[a_pre].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    out["attitude_post_total"] = out[a_post].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    return out
