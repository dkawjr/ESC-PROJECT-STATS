import itertools

import numpy as np
from scipy.stats import rankdata, wilcoxon


def exact_wplus_enum(diff: np.ndarray) -> tuple[float, float]:
    ranks = rankdata(np.abs(diff), method="average")
    obs = float(ranks[diff > 0].sum())
    dist = []
    for bits in itertools.product([0, 1], repeat=len(ranks)):
        wplus = float(sum(r for r, b in zip(ranks, bits) if b == 1))
        dist.append(wplus)
    dist = np.array(dist, dtype=float)
    p = min(1.0, 2.0 * min(np.mean(dist <= obs), np.mean(dist >= obs)))
    return obs, float(p)


def test_wilcoxon_exact_enumeration() -> None:
    diff = np.array([1, 2, 3, -4, -5], dtype=float)
    _, p_enum = exact_wplus_enum(diff)
    p_scipy = wilcoxon(diff, method="exact").pvalue
    assert abs(p_enum - p_scipy) < 1e-10
