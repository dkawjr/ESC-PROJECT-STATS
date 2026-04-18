from pathlib import Path

import pandas as pd


def test_transcript_reconciliation_log_exists() -> None:
    path = Path("results/logs/transcript_reconciliation.md")
    assert path.exists()


def test_known_prior_anchor_number_present() -> None:
    df = pd.read_csv("results/tables/table1_demographics.csv")
    n_row = df.loc[df["metric"] == "n", "value"]
    assert not n_row.empty
    assert int(float(n_row.iloc[0])) == 23
