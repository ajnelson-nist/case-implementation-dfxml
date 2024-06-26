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

top_srcdir := $(shell cd .. ; pwd)

PYTHON3 ?= python3

# Dependencies are listed here in desired execution-progression order.
all:

.PHONY: \
  check-cli \
  check-mypy

.venv.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py
	rm -rf venv
	$(PYTHON3) -m venv \
	  venv
	source venv/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source venv/bin/activate \
	  && pip install \
	    --editable \
	    $(top_srcdir)[testing]
	touch $@

# Dependencies are listed here in desired execution-progression order.
check: \
  check-mypy \
  check-doctest \
  check-cli \
  check-package

check-cli: \
  .venv.done.log
	$(MAKE) \
	  --directory cli \
	  check

check-doctest: \
  .venv.done.log
	source venv/bin/activate \
	  && pytest \
	    --doctest-modules \
	    --log-level=DEBUG \
	    $(top_srcdir)/case_cli_example

check-package: \
  .venv.done.log
	$(MAKE) \
	  --directory package \
	  check

check-mypy: \
  .venv.done.log
	source venv/bin/activate \
	  && mypy \
	    --exclude venv \
	    --strict \
	    $(top_srcdir)/case_cli_example \
	    .

clean:
	@rm -f \
	  .venv.done.log
	@rm -rf \
	  venv
