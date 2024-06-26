#!/usr/bin/make -f

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL = /bin/bash

PYTHON3 ?= python3

all: \
  .venv-pre-commit/var/.pre-commit-built.log

.PHONY: \
  check-TODO \
  check-recursive \
  clean-recursive \
  reset \
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

.setup_complete: \
  deps/dfxml/setup.cfg
	test -d venv || \
	  $(PYTHON3) -m venv venv
	test -r venv/lib/python3.*/site-packages/case-*.egg || \
	  ( \
	    source venv/bin/activate ; \
	      pip install deps/case-api-python || exit $$? ; \
	    deactivate \
	  )
	source venv/bin/activate \
	  && pip install \
	    --editable \
	    deps/dfxml
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
  check-recursive

check-TODO: \
  check-recursive
	source venv/bin/activate ; \
	  $(MAKE) -C tests check-TODO ; \
	deactivate

check-recursive: \
  .setup_complete
	source venv/bin/activate ; \
	  $(MAKE) -C tests check ; \
	deactivate

clean: \
  clean-recursive
	@rm -rf __pycache__

clean-recursive:
	@$(MAKE) -C tests clean

deps/dfxml/setup.cfg: \
  .git_submodule_init
	touch -c $@
	test -r $@

reset: \
  clean
	@rm -rf .git_submodule_init .setup_complete venv

setup: \
  .setup_complete
	@echo "Setup complete."
