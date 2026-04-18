"""Exact McNemar and related helpers."""

from __future__ import annotations

from math import comb

from scipy.stats import beta


def exact_binom_two_sided(k: int, n: int) -> float:
    """Two-sided exact binomial p-value under p=0.5."""
    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2**n)
    return min(1.0, 2.0 * tail)


def mcnemar_exact(b: int, c: int) -> dict[str, float]:
    """Return exact and mid-p McNemar p-values from discordant counts."""
    n = b + c
    k = min(b, c)
    exact = exact_binom_two_sided(k, n) if n > 0 else 1.0
    pmf_k = comb(n, k) / (2**n) if n > 0 else 0.0
    midp = max(0.0, min(1.0, exact - pmf_k))
    return {"exact_p": exact, "mid_p": midp}


def mcnemar_or_and_ci(b: int, c: int, alpha: float = 0.05) -> dict[str, float]:
    """Conditional OR and exact CI based on discordant-p binomial inversion."""
    eps = 0.5
    p_hat = (b + eps) / (b + c + 2 * eps)
    or_hat = p_hat / (1 - p_hat)
    lo_p = beta.ppf(alpha / 2, b + 1, c + 1)
    hi_p = beta.ppf(1 - alpha / 2, b + 1, c + 1)
    return {"or": float(or_hat), "or_ci_low": float(lo_p / (1 - lo_p)), "or_ci_high": float(hi_p / (1 - hi_p))}
