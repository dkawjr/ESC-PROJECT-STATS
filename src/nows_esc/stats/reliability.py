"""Reliability metrics for small-scale psychometric domains."""

from __future__ import annotations

import numpy as np
import pandas as pd


def cronbach_alpha(items: pd.DataFrame) -> float:
    """Compute Cronbach alpha from item matrix."""
    x = items.apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    k = x.shape[1]
    if k < 2 or x.shape[0] < 2:
        return float("nan")
    item_vars = x.var(axis=0, ddof=1).sum()
    total_var = x.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return float("nan")
    return float((k / (k - 1)) * (1 - (item_vars / total_var)))


def omega_total(items: pd.DataFrame) -> float:
    """Approximate McDonald omega total using one-factor PCA loadings."""
    x = items.apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    if x.shape[0] < 3 or x.shape[1] < 2:
        return float("nan")
    z = (x - x.mean()) / x.std(ddof=1)
    corr = np.corrcoef(z.to_numpy().T)
    try:
        vals, vecs = np.linalg.eigh(corr)
    except np.linalg.LinAlgError:
        return float("nan")
    idx = np.argmax(vals)
    loadings = vecs[:, idx] * np.sqrt(vals[idx])
    common_var = np.sum(loadings) ** 2
    uniq_var = np.sum(1 - loadings**2)
    return float(common_var / (common_var + uniq_var))


def bootstrap_ci(
    items: pd.DataFrame,
    metric: str,
    n_boot: int = 10_000,
    seed: int = 20260418,
) -> tuple[float, float]:
    """Bootstrap percentile CI for alpha or omega."""
    rng = np.random.default_rng(seed)
    x = items.apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    if x.empty:
        return float("nan"), float("nan")
    vals = []
    for _ in range(n_boot):
        sample = x.iloc[rng.integers(0, x.shape[0], size=x.shape[0])]
        if metric == "alpha":
            vals.append(cronbach_alpha(sample))
        elif metric == "omega":
            vals.append(omega_total(sample))
        else:
            raise ValueError("metric must be 'alpha' or 'omega'")
    arr = np.asarray(vals, dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return float("nan"), float("nan")
    return float(np.quantile(finite, 0.025)), float(np.quantile(finite, 0.975))
