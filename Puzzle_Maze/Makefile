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
	flake8 .

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

.PHONY: uml-diagrams-game
uml-diagrams-game:
	plantuml ./uml/game/game.plantuml

.PHONY: uml-diagrams-game-state
uml-diagrams-game-state:
	plantuml ./uml/game_states/game_states.plantuml

.PHONY: uml-diagrams-game-objects
uml-diagrams-game-objects:
	plantuml ./uml/GameObjects/door_state_design/plantuml ./uml/GameObjects/player_and_enemy.plantuml

.PHONY: uml-diagrams-interactive
uml-diagrams-interactive:
	plantuml ./uml/interactve_ui_elements/interactive_ui_elements_contexts.plantuml ./uml/interactive_ui_elements/interactive_ui_elements_states.plantuml

.PHONY: uml-diagrams-screens
uml-diagrams-screens:
	plantuml ./uml/screens/info_screen.plantuml ./uml/screens/interation.plantuml ./uml/screens/main_menu.plantuml ./uml/screens/screen.plantuml  ./uml/screens/screens.plantuml

PHONY: uml-diagrams-ui-elements
uml-diagrams-ui-elements:
	plantuml ./uml/ui_elements/ui_elements_components ./uml/ui_elements/ui_elements_decorators.plantuml ./uml/ui_elements/ui_elements.plantuml

.PHONY: all-diagrams
all-diagrams: uml-diagrams-game uml-diagrams-game-state uml-diagrams-game-objects uml-diagrams-interactive uml-diagrams-screens uml-diagrams-ui-elements