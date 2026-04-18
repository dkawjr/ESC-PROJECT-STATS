"""Effect size calculators for paired tests."""

from __future__ import annotations

import numpy as np


def cohen_dz(pre: np.ndarray, post: np.ndarray) -> float:
    """Paired Cohen d_z."""
    diff = np.asarray(post, dtype=float) - np.asarray(pre, dtype=float)
    return float(np.nanmean(diff) / np.nanstd(diff, ddof=1))


def hedges_gz(pre: np.ndarray, post: np.ndarray) -> float:
    """Small-sample corrected paired g_z."""
    diff = np.asarray(post, dtype=float) - np.asarray(pre, dtype=float)
    n = np.isfinite(diff).sum()
    d = cohen_dz(pre, post)
    j = 1.0 - (3.0 / (4.0 * (n - 1) - 1.0))
    return float(j * d)


def rank_biserial_from_diff(diff: np.ndarray) -> float:
    """Matched-pairs rank-biserial based on sign of nonzero paired differences."""
    d = np.asarray(diff, dtype=float)
    d = d[np.isfinite(d)]
    pos = np.sum(d > 0)
    neg = np.sum(d < 0)
    den = pos + neg
    return float((pos - neg) / den) if den > 0 else 0.0
