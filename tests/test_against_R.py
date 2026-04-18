import json
from pathlib import Path


def test_r_reference_file_present_and_well_formed() -> None:
    ref_path = Path("tests/R_reference_outputs.json")
    assert ref_path.exists()
    payload = json.loads(ref_path.read_text(encoding="utf-8"))
    assert "mcnemar_q7_exact_p" in payload
    assert "wilcoxon_knowledge_total_p" in payload
    assert "alpha_comfort_pre" in payload
