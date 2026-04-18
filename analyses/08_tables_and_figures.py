"""Step 8: produce final core table bundle."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.tables import export_table


def main() -> None:
    root = ROOT
    primary = pd.read_csv(root / "results" / "tables" / "table2_primary_outcomes.csv")
    effect = pd.read_csv(root / "results" / "tables" / "effect_sizes.csv")
    merged = primary.merge(effect, on="outcome", how="left")
    export_table(merged, root / "results" / "tables" / "table2_primary_outcomes_final")
    print("tables complete")


if __name__ == "__main__":
    main()
