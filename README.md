# NOWS-ESC Analysis

Reproducible analysis pipeline for a paired pre-post educational simulation study on the Eat-Sleep-Console method for neonatal opioid withdrawal syndrome (NOWS-ESC), with 23 participants and source data in an Excel workbook.

## Quick Start

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e ".[dev]"
make all
```

## Pipeline Outputs

- Cleaned datasets in `data/interim/` and `data/processed/`
- Analysis tables in `results/tables/`
- Audit logs in `results/logs/`

## Reproducibility Notes

- Global random seed: `20260418`
- Raw input workbook is copied unchanged to `data/raw/NOWS_data__1_.xlsx`
- Knowledge paired analyses use Q5-Q9 only, Q10 is treated as prior-training indicator
