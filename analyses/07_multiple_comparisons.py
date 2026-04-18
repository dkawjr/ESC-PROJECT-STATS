"""Step 7: p-value adjustment by test family."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.stats.multiple_comparisons import bh_adjust, holm_adjust


def main() -> None:
    root = ROOT
    df = pd.read_csv(root / "results" / "tables" / "primary_outcomes_raw.csv")
    out = []
    for family in ["knowledge_items", "comfort_items", "attitude_items"]:
        sub = df[df["family"] == family].copy()
        if sub.empty:
            continue
        sub["p_holm"] = holm_adjust(sub["p_exact"].tolist())
        sub["p_bh"] = bh_adjust(sub["p_exact"].tolist())
        out.append(sub)
    if out:
        adjusted = pd.concat(out, ignore_index=True)
        adjusted.to_csv(root / "results" / "tables" / "primary_outcomes_adjusted.csv", index=False)
    print("multiple comparisons complete")


if __name__ == "__main__":
    main()
