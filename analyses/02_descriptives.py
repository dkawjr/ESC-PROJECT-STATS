"""Step 2: descriptives and demographics."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.tables import export_table


def main() -> None:
    root = ROOT
    df = pd.read_csv(root / "data" / "interim" / "cleaned_wide.csv")
    out = pd.DataFrame(
        {
            "metric": ["n", "years_practice_mean", "years_practice_sd", "prior_training_yes_n"],
            "value": [
                int(df.shape[0]),
                float(df["Years in Practice"].mean(skipna=True)),
                float(df["Years in Practice"].std(skipna=True)),
                int(df["Pre Simulation Knowledge: Question 10"].sum(skipna=True)),
            ],
        }
    )
    export_table(out, root / "results" / "tables" / "table1_demographics")
    print("descriptives complete")


if __name__ == "__main__":
    main()
