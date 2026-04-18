import numpy as np

from nows_esc.stats.effect_sizes import cohen_dz, hedges_gz, rank_biserial_from_diff
from nows_esc.stats.hodges_lehmann import walsh_ci
from nows_esc.stats.mcnemar import mcnemar_or_and_ci
from nows_esc.stats.multiple_comparisons import bh_adjust, holm_adjust


def test_effect_sizes_finite() -> None:
    pre = np.array([1, 2, 3, 2, 4], dtype=float)
    post = np.array([2, 3, 3, 4, 5], dtype=float)
    assert np.isfinite(cohen_dz(pre, post))
    assert np.isfinite(hedges_gz(pre, post))
    assert rank_biserial_from_diff(post - pre) > 0


def test_walsh_ci_ordered() -> None:
    lo, hi = walsh_ci(np.array([1, -1, 2, 3, 0], dtype=float))
    assert lo <= hi


def test_mcnemar_or_ci_positive() -> None:
    out = mcnemar_or_and_ci(1, 6)
    assert out["or"] > 0
    assert out["or_ci_low"] < out["or_ci_high"]


def test_multiple_adjustments_length() -> None:
    p = [0.01, 0.04, 0.2, 0.5]
    assert len(holm_adjust(p)) == len(p)
    assert len(bh_adjust(p)) == len(p)
