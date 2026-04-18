# NOWS-ESC Analysis

This repository contains a fully reproducible paired pre-post analysis pipeline for an educational simulation study on the Eat-Sleep-Console approach for Neonatal Opioid Withdrawal Syndrome (NOWS-ESC), with one participant row per response and prespecified paired outcome analyses.

Headline result: item-level and domain-level results are generated end-to-end from the raw workbook, with strongest paired improvements observed in comfort domain metrics, and all core outputs are reproducible by rerunning the scripts and tests.

## Start Here (Share-Friendly)

If you are opening this repo in Claude or another coding assistant, start with this prompt:

1. "Read `README.md` and summarize the project in 5 bullets."
2. "Show me how to run the analysis pipeline on Windows PowerShell."
3. "Walk me through `analyses/01_clean_and_audit.py` to `analyses/09_manuscript_numbers.py` in order."
4. "Explain how each main p-value is validated by tests in `tests/`."
5. "Point me to the final outputs in `results/tables/`, `results/figures/`, and `manuscript/results.md`."

Human quick-start:
- Read `manuscript/results.md` for plain-language output.
- Open `results/figures/*.png` for visual results.
- Open `results/tables/` for manuscript-ready tables.

## Run Instructions

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e ".[dev]"
make all
make test
```

On Windows PowerShell where `make` is not installed, run scripts in `analyses/` sequentially.

## Repository Map

- `data/raw/` - untouched input workbook copy used by pipeline.
- `data/interim/` - cleaned wide and long intermediate artifacts.
- `data/processed/` - final analysis-ready tabular outputs.
- `src/nows_esc/` - package modules for I/O, cleaning, stats, tables, figures, and report rendering.
- `analyses/` - numbered executable pipeline scripts.
- `tests/` - formula-level and cross-check tests.
- `results/tables/` - manuscript-grade table outputs (`csv`, `tex`, `docx`).
- `results/figures/` - figure outputs (`png`).
- `results/logs/` - cleaning audit, run logs, session metadata, transcript reconciliation.
- `manuscript/` - methods/results/SAP/checklist/limitations markdown.
- `docs/proofs/` - derivation notes for primary tests and effect sizes.

## Data Citation and Ethics

- Source workbook filename: `NOWS_data__1_.xlsx`
- Study topic: NOWS-ESC educational simulation analysis dataset
- IRB placeholder: `IRB-TO-BE-INSERTED`

## Reproducibility Hash

- `sha256(data/raw/NOWS_data__1_.xlsx)`:
  - `49dc4b5d10c166dd21a9ed95da4de15027ef33d38d126768559dc09a7b43e7f7`

## P-value Traceability

| Outcome | p-value source script | verification test |
|---|---|---|
| Knowledge Q5-Q9 exact McNemar | `analyses/03_primary_tests.py` | `tests/test_mcnemar_hand.py` |
| Knowledge total Wilcoxon | `analyses/03_primary_tests.py` | `tests/test_against_scipy.py` |
| Comfort items/domain Wilcoxon | `analyses/03_primary_tests.py` | `tests/test_wilcoxon_hand.py` |
| Attitude items/domain Wilcoxon | `analyses/03_primary_tests.py` | `tests/test_against_scipy.py` |
| Family-wise adjusted p-values | `analyses/07_multiple_comparisons.py` | `tests/test_stats_additional.py` |

## Additional Notes

- Global seed is fixed at `20260418`.
- Reverse-scoring is parsed from Key sheet text, not hardcoded.
- Knowledge primary item set is Q5 through Q9 only; Q10 is prior-training indicator.
