PYTHON = python3
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports --explicit-package-bases .
#TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports .
STYLE_CHECK = flake8
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

type-check:
	$(TYPE_CHECK)

style-check:
	flake8

fix-style:
	autopep8 --in-place --recursive --aggressive --aggressive .

.PHONY: create-docs-folder
create-docs-folder:
	mkdir -p $(DOCS)

.PHONY: create-docs
create-docs: create-docs-folder
	pdoc --output-dir $(DOCS) .

.PHONY: create-cov-report
create-cov-report:
	pytest --verbose --color=yes --cov --cov-report term --cov-report=html:$(DOCS)/pycov tests/
	@echo "Coverage report created in $(DOCS) folder"