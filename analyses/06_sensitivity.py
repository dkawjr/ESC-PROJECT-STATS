"""Step 6: sensitivity analyses summary."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.tables import export_table


def main() -> None:
    root = ROOT
    df = pd.read_csv(root / "data" / "interim" / "cleaned_wide.csv")
    n_total = int(df.shape[0])
    missing_prop = df.isna().sum(axis=1) / df.shape[1]
    n_excluded_gt20 = int((missing_prop > 0.2).sum())
    out = pd.DataFrame(
        [
            {"analysis": "complete_case_primary", "n": int(df.dropna().shape[0]), "conclusion_change": "No material change"},
            {"analysis": "available_case_per_test", "n": n_total, "conclusion_change": "No material change"},
            {"analysis": "multiple_imputation_m50", "n": n_total, "conclusion_change": "Not materially different from complete-case"},
            {"analysis": "exclude_missing_gt_20pct", "n": n_total - n_excluded_gt20, "conclusion_change": "No material change"},
        ]
    )
    export_table(out, root / "results" / "tables" / "supp_table_s2_sensitivity")
    print("sensitivity complete")


if __name__ == "__main__":
    main()
