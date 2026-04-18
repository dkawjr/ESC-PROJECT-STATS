"""Step 5: reliability metrics and confidence intervals."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.stats.reliability import bootstrap_ci, cronbach_alpha, omega_total
from nows_esc.tables import export_table


def main() -> None:
    root = ROOT
    df = pd.read_csv(root / "data" / "interim" / "cleaned_wide.csv")
    scales = [
        ("Comfort pre", [f"Pre Simulation Comfort: 11{x}" for x in "abcd"]),
        ("Comfort post", [f"Post Simulation Comfort: 10{x}" for x in "abcd"]),
        ("Attitude pre reversed", [f"Pre Simulation Attitude: 12{x}__rev" for x in "abcde"]),
        ("Attitude post reversed", [f"Post Simulation Attitude: 11{x}__rev" for x in "abcde"]),
    ]
    rows = []
    for label, cols in scales:
        items = df[cols].apply(pd.to_numeric, errors="coerce")
        a = cronbach_alpha(items)
        o = omega_total(items)
        a_lo, a_hi = bootstrap_ci(items, "alpha")
        o_lo, o_hi = bootstrap_ci(items, "omega")
        rows.append(
            {
                "scale": label,
                "k_items": len(cols),
                "n_participants": int(items.dropna().shape[0]),
                "alpha": a,
                "alpha_ci_low": a_lo,
                "alpha_ci_high": a_hi,
                "omega": o,
                "omega_ci_low": o_lo,
                "omega_ci_high": o_hi,
                "note": "Interpret with caution at n=23 due to wide uncertainty.",
            }
        )
    out = pd.DataFrame(rows)
    export_table(out, root / "results" / "tables" / "table3_reliability")
    print("reliability complete")


if __name__ == "__main__":
    main()
