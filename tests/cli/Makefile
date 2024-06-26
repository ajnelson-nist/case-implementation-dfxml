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

top_srcdir := $(shell cd ../.. ; pwd)

all: \
  example_output.jsonld \
  example_output.rdf \
  example_output.ttl \
  example_output_debug.jsonld \
  example_output_debug.rdf \
  example_output_debug.ttl

.PHONY: \
  check-pytest

check: \
  check-pytest

check-pytest: \
  all
	source $(top_srcdir)/tests/venv/bin/activate \
	  && pytest \
	    --log-level=DEBUG

clean:
	@rm -rf \
	  *.jsonld \
	  *.rdf \
	  *.ttl \
	  .pytest_cache

example_output.%: \
  $(top_srcdir)/case_dfxml/cli.py \
  $(top_srcdir)/tests/.venv.done.log
	export CDO_DEMO_NONRANDOM_UUID_BASE="$(top_srcdir)" \
	  && source $(top_srcdir)/tests/venv/bin/activate \
	    && case_dfxml \
	      _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_validate \
	    _$@
	mv _$@ $@

example_output_debug.%: \
  $(top_srcdir)/case_dfxml/cli.py \
  $(top_srcdir)/tests/.venv.done.log
	export CDO_DEMO_NONRANDOM_UUID_BASE="$(top_srcdir)" \
	  && source $(top_srcdir)/tests/venv/bin/activate \
	    && case_dfxml \
	      --debug \
	      _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_validate \
	    _$@
	mv _$@ $@
