"""Hodges-Lehmann estimator and Walsh CI."""

from __future__ import annotations

import itertools

import numpy as np


def walsh_averages(diff: np.ndarray) -> np.ndarray:
    """Return sorted Walsh averages for paired differences."""
    d = np.asarray(diff, dtype=float)
    d = d[np.isfinite(d)]
    vals = [(a + b) / 2.0 for a, b in itertools.combinations_with_replacement(d, 2)]
    return np.sort(np.asarray(vals, dtype=float))


def hodges_lehmann(diff: np.ndarray) -> float:
    """HL estimator as median of Walsh averages."""
    return float(np.median(walsh_averages(diff)))


def walsh_ci(diff: np.ndarray, alpha: float = 0.05) -> tuple[float, float]:
    """Approximate Walsh CI via quantiles."""
    w = walsh_averages(diff)
    lo = float(np.quantile(w, alpha / 2))
    hi = float(np.quantile(w, 1 - alpha / 2))
    return lo, hi
