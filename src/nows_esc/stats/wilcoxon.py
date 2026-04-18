"""Wilcoxon signed-rank wrappers."""

from __future__ import annotations

import numpy as np
from scipy.stats import wilcoxon as sp_wilcoxon


def wilcoxon_signed_rank(
    pre: np.ndarray, post: np.ndarray, zero_method: str = "wilcox", method: str = "auto"
) -> dict[str, float]:
    """Compute paired signed-rank test."""
    diff = np.asarray(post) - np.asarray(pre)
    result = sp_wilcoxon(diff, zero_method=zero_method, method=method, correction=False)
    return {"statistic": float(result.statistic), "p_value": float(result.pvalue), "n": int(np.isfinite(diff).sum())}
