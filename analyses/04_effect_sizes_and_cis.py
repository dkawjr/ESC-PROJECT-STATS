"""Step 4: additional effect size outputs."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.bootstrap import bootstrap_rank_biserial
from nows_esc.stats.effect_sizes import cohen_dz, hedges_gz, rank_biserial_from_diff


def main() -> None:
    root = ROOT
    df = pd.read_csv(root / "data" / "interim" / "cleaned_wide.csv")
    rows = []
    for pre_col, post_col, label in [
        ("knowledge_pre_total", "knowledge_post_total", "knowledge_total"),
        ("comfort_pre_total", "comfort_post_total", "comfort_domain"),
        ("attitude_pre_total", "attitude_post_total", "attitude_domain"),
    ]:
        pre = pd.to_numeric(df[pre_col], errors="coerce").to_numpy(dtype=float)
        post = pd.to_numeric(df[post_col], errors="coerce").to_numpy(dtype=float)
        diff = post - pre
        lo, hi = bootstrap_rank_biserial(diff)
        rows.append(
            {
                "outcome": label,
                "cohen_dz": cohen_dz(pre, post),
                "hedges_gz": hedges_gz(pre, post),
                "rank_biserial_boot_ci_low": lo,
                "rank_biserial_boot_ci_high": hi,
                "rank_biserial": rank_biserial_from_diff(diff),
            }
        )
    pd.DataFrame(rows).to_csv(root / "results" / "tables" / "effect_sizes.csv", index=False)
    print("effect sizes complete")


if __name__ == "__main__":
    main()
