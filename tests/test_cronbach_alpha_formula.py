import statistics

import pandas as pd
import pingouin as pg

from nows_esc.stats.reliability import cronbach_alpha


def test_cronbach_alpha_matches_formula_and_pingouin() -> None:
    df = pd.DataFrame(
        {
            "i1": [1, 2, 3, 4, 5],
            "i2": [2, 2, 3, 4, 4],
            "i3": [1, 1, 2, 3, 4],
            "i4": [2, 3, 3, 4, 5],
        }
    )
    k = df.shape[1]
    item_vars = sum(statistics.variance(df[c]) for c in df.columns)
    total_var = statistics.variance(df.sum(axis=1))
    hand = (k / (k - 1)) * (1 - item_vars / total_var)
    ours = cronbach_alpha(df)
    pg_alpha, _ = pg.cronbach_alpha(data=df)
    assert abs(hand - ours) < 1e-10
    assert abs(pg_alpha - ours) < 1e-10
