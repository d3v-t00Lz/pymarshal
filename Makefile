ORG ?= $(shell jq -r .org meta.json)
PRODUCT ?= $(shell jq -r .product meta.json)
VERSION ?= $(shell grep __version__ src/pymarshal/__init__.py | grep -oE "([0-9]+\.[0-9]+\.[0-9]+)")
DESTDIR ?=
PREFIX ?= /usr

DOCKER ?= podman

LINUX_APPLICATIONS_DIR ?= $(DESTDIR)/usr/share/applications
UI ?= qt

.PHONY: test venv

clean:
	# Remove temporary build files
	rm -rf build/ dist/ htmlcov/ ./*.egg-info ./*.nsi .pytest_cache/ \
		./.build/ ./*. ./*.
	find test/ src/ -name __pycache__ -type d \
		-exec rm -rf {} \; 2>/dev/null \
		|| true

git-hooks:
	# Install git hooks for this repository to enable running tests before
	# committing, etc...
	cp -f tools/git-hooks/* .git/hooks/

pypi: test type-check
	# Upload your package to PyPi so that anybody can install using pip.
	# Requires `twine` to be installed, and a local twine config with your
	# pypi username and password
	rm -rf dist/*.tar.gz dist/*.whl
	python3 -m build
	twine upload dist/*

test:
	# Run the unit tests
	#tox -e $(shell python3 -c "import sys; v = sys.version_info; print(f'py{v[0]}{v[1]}')")
	python3 -m pytest

test-all-docker:
	# Test against all versions of Python supported by this code using Docker
	tools/test-all-py-versions.sh $(DOCKER)

test-all-tox:
	# Test against all versions of Python supported by this code using tox
	# This only works if every supported version of Python is installed on
	# this computer
	tox

test-pdb:
	# Debug unit tests that raise Exceptions with PDB
	python3 -m pytest --pdb

type-check:
	# Check typing of Python type hints
	mypy --ignore-missing-imports \
		src/pymarshal \

venv:
	# Create a Python "virtual environment" aka venv
	# Run this target before running:
	#     source venv/bin/activate
	#     pip3 install -e .
	python3 -m venv venv

