import numpy as np
from scipy.stats import wilcoxon

from nows_esc.stats.wilcoxon import wilcoxon_signed_rank


def test_wilcoxon_wrapper_matches_scipy() -> None:
    pre = np.array([1, 2, 1, 2, 3, 2], dtype=float)
    post = np.array([2, 2, 2, 3, 4, 1], dtype=float)
    wrapped = wilcoxon_signed_rank(pre, post, zero_method="wilcox", method="exact")
    direct = wilcoxon(post - pre, zero_method="wilcox", method="exact")
    assert abs(wrapped["statistic"] - direct.statistic) < 1e-12
    assert abs(wrapped["p_value"] - direct.pvalue) < 1e-12
