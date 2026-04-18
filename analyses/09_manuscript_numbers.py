"""Step 9: manuscript auto-generated numbers and logs."""

from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from nows_esc.report import generate_results_markdown


def main() -> None:
    root = ROOT
    generate_results_markdown(
        root / "results" / "tables" / "table2_primary_outcomes_final.csv",
        root / "manuscript" / "results.md",
    )
    session = "\n".join(
        [
            f"python_version: {platform.python_version()}",
            f"platform: {platform.platform()}",
        ]
    )
    (root / "results" / "logs").mkdir(parents=True, exist_ok=True)
    (root / "results" / "logs" / "session_info.txt").write_text(session, encoding="utf-8")
    (root / "results" / "logs" / "transcript_reconciliation.md").write_text(
        "# Transcript reconciliation\n\n"
        "- Prior anchor retained: n=23 participants.\n"
        "- Any numeric differences should be treated as findings to inspect.\n",
        encoding="utf-8",
    )
    pipeline_log = root / "results" / "logs" / "pipeline_run.log"
    existing = pipeline_log.read_text(encoding="utf-8") if pipeline_log.exists() else ""
    pipeline_log.write_text(existing + "step09_complete\n", encoding="utf-8")
    print("manuscript numbers complete")


if __name__ == "__main__":
    main()
