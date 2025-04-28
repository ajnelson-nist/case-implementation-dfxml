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

SHELL = /bin/bash

PYTHON3 ?= python3

top_srcdir := $(shell cd .. ; pwd)

dfxml_top_srcdir := $(top_srcdir)/deps/dfxml

dfxml_xsd := $(dfxml_top_srcdir)/dependencies/dfxml_schema/dfxml.xsd

objects_py_dependencies := \
  $(dfxml_top_srcdir)/dfxml/__init__.py \
  $(dfxml_top_srcdir)/dfxml/objects.py

case_to_dfxml_dependencies := \
  $(objects_py_dependencies) \
  $(top_srcdir)/case_dfxml/case_to_dfxml.py

dfxml_to_case_dependencies := \
  $(objects_py_dependencies) \
  $(top_srcdir)/case_dfxml/dfxml_to_case.py

# Dependencies are listed here in desired execution-progression order.
all:

.PHONY: \
  check-case_examples \
  check-cli \
  check-mypy \
  clean-case_examples \
  clean-recursive

.venv.done.log: \
  $(dfxml_top_srcdir)/setup.cfg \
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
  check-package \
  check-case_examples
	@echo "Unit tests pass!"

check-case_examples: \
  check-cli
	$(MAKE) -C case_examples check

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
	    $(top_srcdir)/case_dfxml

check-mypy: \
  .venv.done.log
	source venv/bin/activate \
	  && mypy \
	    --exclude venv \
	    --strict \
	    $(top_srcdir)/case_dfxml \
	    .

check-package: \
  .venv.done.log
	$(MAKE) \
	  --directory package \
	  check

clean: \
  clean-recursive
	@rm -f \
	  *dfxml \
	  *json \
	  *pyc \
	  *rdf \
	  *ttl \
	  .venv.done.log
	@rm -rf \
	  __pycache__ \
	  venv

clean-case_examples:
	$(MAKE) -C case_examples clean

clean-recursive: \
  clean-case_examples
