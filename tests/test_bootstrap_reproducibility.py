import numpy as np

from nows_esc.bootstrap import bootstrap_rank_biserial


def test_bootstrap_ci_reproducible() -> None:
    diff = np.array([1, 2, -1, 0, 3, 4, -2, 1], dtype=float)
    ci1 = bootstrap_rank_biserial(diff, n_boot=3000)
    ci2 = bootstrap_rank_biserial(diff, n_boot=3000)
    assert np.allclose(ci1, ci2, atol=1e-12)
