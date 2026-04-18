import itertools

import numpy as np

from nows_esc.stats.hodges_lehmann import hodges_lehmann


def test_hl_matches_walsh_median() -> None:
    diff = np.array([1, 3, -1, 2], dtype=float)
    walsh = sorted((a + b) / 2 for a, b in itertools.combinations_with_replacement(diff, 2))
    hand = float(np.median(np.array(walsh)))
    assert abs(hand - hodges_lehmann(diff)) < 1e-12
