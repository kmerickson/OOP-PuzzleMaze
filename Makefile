TEST = pytest
TEST_ARGS = -s --verbose --color=yes
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8
COVERAGE = python3 -m pytest
DEMO-ASSIGNMENT = ./demo-assignments

.PHONY: all
all: check-style check-type run-test-coverage clean
	@echo "All checks passed"

.PHONY: check-type
check-type:
	$(TYPE_CHECK) Puzzle_Maze

.PHONY: check-style
check-style:
	$(STYLE_CHECK) Puzzle_Maze

# discover and run all tests
.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) Puzzle_Maze/tests

.PHONY: run-test-coverage
run-test-coverage:
	cd Puzzle_Maze && pytest --verbose --color=yes --cov --cov-report term --cov-report xml:docs/coverage.xml --cov-report=html:docs/htmlcov tests/

.PHONY: clean
clean:
	# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -name .coverage` # remove all coverage cache 
