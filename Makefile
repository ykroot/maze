PYTHON = python3
MAIN   = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean fclean lint lint-strict build-pkg

install:
	pip install flake8 mypy build

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

fclean: clean
	find . -name maze.txt | xargs rm -rf
	find . -name mazegen-*-*-*-*.whl | xargs rm -rf

lint:
	flake8 ./mazegen *.py
	mypy ./mazegen *.py --warn-return-any \
	       --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs

lint-strict:
	flake8 ./mazegen *.py
	mypy ./mazegen *.py --strict

build-pkg:
	$(PYTHON) -m build --wheel
	cp dist/*.whl .
