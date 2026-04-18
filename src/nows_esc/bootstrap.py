"""Bootstrap utilities."""

from __future__ import annotations

import numpy as np

from .config import GLOBAL_SEED
from .stats.effect_sizes import rank_biserial_from_diff


def bootstrap_rank_biserial(diff: np.ndarray, n_boot: int = 10_000) -> tuple[float, float]:
    """Percentile bootstrap CI for rank-biserial."""
    rng = np.random.default_rng(GLOBAL_SEED)
    vals = []
    d = diff[np.isfinite(diff)]
    for _ in range(n_boot):
        sample = rng.choice(d, size=d.size, replace=True)
        vals.append(rank_biserial_from_diff(sample))
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))
