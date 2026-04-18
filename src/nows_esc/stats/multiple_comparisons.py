"""Multiple comparison procedures."""

from __future__ import annotations

import numpy as np
from statsmodels.stats.multitest import multipletests


def holm_adjust(p_values: list[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values."""
    return list(multipletests(np.asarray(p_values), alpha=0.05, method="holm")[1])


def bh_adjust(p_values: list[float]) -> list[float]:
    """Benjamini-Hochberg adjusted p-values."""
    return list(multipletests(np.asarray(p_values), alpha=0.05, method="fdr_bh")[1])
