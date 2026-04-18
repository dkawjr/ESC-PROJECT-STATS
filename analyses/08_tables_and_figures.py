"""Step 8: produce final core table bundle."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.figures import fig1_knowledge, fig2_comfort, fig3_attitude, fig4_domains, supp_fig_s1_symmetry
from nows_esc.tables import export_table


def main() -> None:
    root = ROOT
    df = pd.read_csv(root / "data" / "interim" / "cleaned_wide.csv")
    primary = pd.read_csv(root / "results" / "tables" / "table2_primary_outcomes.csv")
    effect = pd.read_csv(root / "results" / "tables" / "effect_sizes.csv")
    merged = primary.merge(effect, on="outcome", how="left")
    export_table(merged, root / "results" / "tables" / "table2_primary_outcomes_final")
    miss = pd.read_json(root / "results" / "logs" / "cleaning_audit.json", typ="series")
    supp_missing = pd.DataFrame(
        [{"participant_id": pid, "missing_count": cnt} for pid, cnt in miss["missing_by_participant"].items()]
    )
    export_table(supp_missing, root / "results" / "tables" / "supp_table_s1_missingness")
    fig1_knowledge(df, root / "results" / "figures")
    fig2_comfort(df, root / "results" / "figures")
    fig3_attitude(df, root / "results" / "figures")
    fig4_domains(df, root / "results" / "figures")
    supp_fig_s1_symmetry(df, root / "results" / "figures")
    print("tables and figures complete")


if __name__ == "__main__":
    main()
