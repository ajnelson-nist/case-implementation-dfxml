#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

PYTHON3 ?= python3

all: \
  .venv-pre-commit/var/.pre-commit-built.log

.PHONY: \
  check-TODO \
  check-supply-chain \
  check-supply-chain-mypy \
  check-supply-chain-pre-commit \
  clean-tests \
  setup

# Removing this flag file checks for added or removed submodules, but does not cause a submodule update to occur on submodules that have already been checked out at least once.
.git_submodule_init: \
  .gitmodules
	git submodule sync
	test -r deps/case/.git || \
	  (git submodule init deps/case && git submodule update deps/case)
	test -r deps/case-api-python/.git || \
	  (git submodule init deps/case-api-python && git submodule update deps/case-api-python)
	test -r deps/case-implementation-plaso/.git || \
	  (git submodule init deps/case-implementation-plaso && git submodule update deps/case-implementation-plaso)
	test -r deps/dfxml/.git || \
	  (git submodule init deps/dfxml && git submodule update deps/dfxml)
	test -r deps/dfxml_schema/.git || \
	  (git submodule init deps/dfxml_schema && git submodule update deps/dfxml_schema)
	touch $@

.git_submodule_init.done.log: \
  .gitmodules
	git submodule update --init
	touch $@

# This virtual environment is meant to be built once and then persist, even through 'make clean'.
# If a recipe is written to remove this flag file, it should first run `pre-commit uninstall`.
.venv-pre-commit/var/.pre-commit-built.log:
	rm -rf .venv-pre-commit
	test -r .pre-commit-config.yaml \
	  || (echo "ERROR:Makefile:pre-commit is expected to install for this repository, but .pre-commit-config.yaml does not seem to exist." >&2 ; exit 1)
	$(PYTHON3) -m venv \
	  .venv-pre-commit
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    pre-commit
	source .venv-pre-commit/bin/activate \
	  && pre-commit install
	mkdir -p \
	  .venv-pre-commit/var
	touch $@

check: \
  .venv-pre-commit/var/.pre-commit-built.log \
  check-supply-chain-mypy
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory tests \
	  check

check-TODO: \
  check
	$(MAKE) \
	  --directory tests \
	  check-TODO

# This target's dependencies potentially modify the working directory's Git state, so it is intentionally not a dependency of check.
check-supply-chain: \
  check-supply-chain-pre-commit \
  check-supply-chain-mypy

check-supply-chain-mypy: \
  .git_submodule_init.done.log
	$(MAKE) \
	  PYTHON3=$(PYTHON3) \
	  --directory tests \
	  check-mypy

# Update pre-commit configuration and use the updated config file to
# review code.  Only have Make exit if 'pre-commit run' modifies files.
check-supply-chain-pre-commit: \
  .venv-pre-commit/var/.pre-commit-built.log
	source .venv-pre-commit/bin/activate \
	  && pre-commit autoupdate
	git diff \
	  --exit-code \
	  .pre-commit-config.yaml \
	  || ( \
	      source .venv-pre-commit/bin/activate \
	        && pre-commit run \
	          --all-files \
	          --config .pre-commit-config.yaml \
	    ) \
	    || git diff \
	      --stat \
	      --exit-code \
	      || ( \
	          echo \
	            "WARNING:Makefile:pre-commit configuration can be updated.  It appears the updated would change file formatting." \
	            >&2 \
	            ; exit 1 \
                )
	@git diff \
	  --exit-code \
	  .pre-commit-config.yaml \
	  || echo \
	    "INFO:Makefile:pre-commit configuration can be updated.  It appears the update would not change file formatting." \
	    >&2

clean: \
  clean-tests
	@rm -rf \
	  *.egg-info \
	  __pycache__ \
	  build \
	  dist
	@rm -f \
	  .git_submodule_init.done.log

clean-tests:
	@$(MAKE) \
	  --directory tests \
	  clean

deps/dfxml/setup.cfg: \
  .git_submodule_init
	touch -c $@
	test -r $@

setup: \
  .setup_complete
	@echo "Setup complete."
