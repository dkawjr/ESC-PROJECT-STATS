import numpy as np
import pandas as pd

from nows_esc.clean import add_reverse_columns


def test_double_reverse_invariant() -> None:
    df = pd.DataFrame({"item": [1, 2, 3, 4, 5, np.nan]})
    out = add_reverse_columns(df, {"item": True})
    first = out["item__rev"]
    second = 6 - first
    original = pd.to_numeric(df["item"], errors="coerce")
    assert np.allclose(second.fillna(-99), original.fillna(-99))
