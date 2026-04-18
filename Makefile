PYTHON ?= python

.PHONY: all clean test lint

all:
	$(PYTHON) analyses/01_clean_and_audit.py
	$(PYTHON) analyses/02_descriptives.py
	$(PYTHON) analyses/03_primary_tests.py
	$(PYTHON) analyses/04_effect_sizes_and_cis.py
	$(PYTHON) analyses/07_multiple_comparisons.py
	$(PYTHON) analyses/08_tables_and_figures.py

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests analyses

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p, ignore_errors=True) for p in [Path('data/interim'), Path('data/processed'), Path('results')]]"
