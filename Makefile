PYTHON = python3
MAIN   = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint lint-strict build-pkg

install:
	pip install flake8 build mypy

run:
	PYTHONPATH=. $(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name __pycache__ | xargs rm -rf
	find . -type d -name .mypy_cache | xargs rm -rf
	find . -type d -name "*.egg-info" | xargs rm -rf
	find . -type d -name "build" | xargs rm -rf
	find . -type d -name "dist" | xargs rm -rf
	find . -name "*.pyc" -delete

lint:
	flake8 .
	mypy . --warn-return-any \
	       --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

build-pkg:
	$(PYTHON) -m build --wheel
	cp dist/*.whl .
