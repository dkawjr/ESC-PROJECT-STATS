"""Step 1: cleaning, codebook, missingness audit."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from nows_esc.clean import add_reverse_columns, build_codebook, coerce_types, missingness_audit, parse_reverse_map, save_json
from nows_esc.io import load_workbook, save_df
from nows_esc.scales import add_domain_scores


def main() -> None:
    root = ROOT
    sheets = load_workbook()
    key_df = sheets["Key"]
    data_df = sheets["Data"]

    codebook = build_codebook(key_df)
    reverse_map = parse_reverse_map(key_df)
    save_json(codebook, root / "data" / "interim" / "codebook.json")
    workbook_summary = {
        name: {
            "rows": int(df.shape[0]),
            "cols": int(df.shape[1]),
            "columns": [str(c) for c in df.columns],
        }
        for name, df in sheets.items()
    }
    save_json(workbook_summary, root / "data" / "interim" / "workbook_summary.json")
    save_json(reverse_map, root / "data" / "interim" / "reverse_map.json")

    coerced = coerce_types(data_df)
    cleaned = add_reverse_columns(coerced, reverse_map)
    scored = add_domain_scores(cleaned)
    save_df(scored, root / "data" / "interim" / "cleaned_wide.csv", root / "data" / "interim" / "cleaned_wide.parquet")

    long_df = scored.melt(id_vars=["Participant ID"], var_name="variable", value_name="value")
    save_df(long_df, root / "data" / "interim" / "cleaned_long.csv", root / "data" / "interim" / "cleaned_long.parquet")
    save_df(scored, root / "data" / "processed" / "analysis_ready.csv", root / "data" / "processed" / "analysis_ready.parquet")

    audit = missingness_audit(data_df)
    save_json(audit, root / "results" / "logs" / "cleaning_audit.json")
    (root / "results" / "logs" / "pipeline_run.log").write_text("step01_complete\n", encoding="utf-8")
    print("clean_and_audit complete")


if __name__ == "__main__":
    main()
