from math import comb

import pandas as pd

from nows_esc.stats.mcnemar import mcnemar_exact


def test_mcnemar_direct_binomial_q7() -> None:
    df = pd.read_csv("data/interim/cleaned_wide.csv")
    pre = pd.to_numeric(df["Pre Simulation Knowledge: Question 7"], errors="coerce")
    post = pd.to_numeric(df["Post Simulation Knowledge: Question 7"], errors="coerce")
    b = int(((pre == 1) & (post == 0)).sum())
    c = int(((pre == 0) & (post == 1)).sum())
    n = b + c
    k = min(b, c)
    hand = min(1.0, 2.0 * sum(comb(n, i) for i in range(0, k + 1)) / (2**n)) if n > 0 else 1.0
    got = mcnemar_exact(b, c)["exact_p"]
    assert abs(hand - got) < 1e-12
