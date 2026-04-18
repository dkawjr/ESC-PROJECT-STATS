# Reproduction Guide

1. Install Python environment and dependencies:
   - `pip install -e ".[dev]"`
2. Run full pipeline:
   - `make all` (or run scripts in `analyses/` sequentially)
3. Run tests:
   - `make test`
4. Review outputs:
   - `results/tables/`, `results/figures/`, `results/logs/`
