PYTHON = python3
DOCS = docs

.PHONY: all
all: fix-style style-check type-check unittest clean
	@echo "all done..."

.PHONY: kattis-test
kattis-test:
	@kattis test

unittest:
	$(PYTHON) -m pytest -v

clean:
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: check-types
check-types:
	mypy --disallow-untyped-defs --strict .
	@echo "Used mypy to verify type checking correctness"

.PHONY: check-style
check-style:
	flake8 . ./tests
	@echo "Used flake8 for style checking"

.PHONY: fix-style
fix-style:
	autopep8 --in-place --recursive --aggressive --aggressive . ./tests
	@echo "Used autopep8 to fix style mistakes"

.PHONY: aesthetics fix-style check-style check-types
aesthetics: fix-style check-style check-types

.PHONY: create-docs-folder
create-docs-folder:
	mkdir -p $(DOCS)
.PHONY: run
run:
	python3 chips_core_escape.py

.PHONY: create-docs
create-docs: create-docs-folder
	pdoc --output-dir $(DOCS) .

.PHONY: create-cov-report
create-cov-report:
	pytest --verbose --color=yes --cov --cov-report term --cov-report xml:docs/coverage.xml --cov-report=html:docs/htmlcov tests/
	@echo "Coverage report created in $(DOCS) folder"