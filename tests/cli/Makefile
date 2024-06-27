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

make_differential_dfxml_dependencies := \
  $(dfxml_top_srcdir)/dfxml/bin/make_differential_dfxml.py \
  $(objects_py_dependencies)

all: \
  empty.json \
  single_file_1.rdf \
  single_file_0_2_deltas.dfxml \
  single_file_0_json_2_deltas.dfxml \
  single_filesystem_single_file_0_2_deltas.dfxml

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
	  .pytest_cache
	@rm -f \
	  *.json \
	  *.rdf \
	  *.ttl

empty.json: \
  $(top_srcdir)/tests/.venv.done.log \
  empty_json.py
	rm -f _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && python empty_json.py \
	    _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_validate \
	    _$@
	mv _$@ $@

single_file_0.dfxml: \
  $(dfxml_xsd) \
  $(objects_py_dependencies) \
  empty.json \
  single_file_0_dfxml.py
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && python single_file_0_dfxml.py \
	    __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

single_file_0_2_deltas.dfxml: \
  $(make_differential_dfxml_dependencies) \
  single_file_2.dfxml
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && make_differential_dfxml \
	    --retain-unchanged \
	    single_file_{0,2}.dfxml \
	    > __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

single_file_0_json_2_deltas.dfxml: \
  $(make_differential_dfxml_dependencies) \
  single_file_2.json.dfxml
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && make_differential_dfxml \
	    --retain-unchanged \
	    single_file_0.dfxml \
	    single_file_2.json.dfxml \
	    > __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

single_file_1.json: \
  $(dfxml_to_case_dependencies) \
  single_file_0.dfxml
	rm -f _$@
	export CDO_DEMO_NONRANDOM_UUID_BASE=$(top_srcdir) \
	  && source $(top_srcdir)/tests/venv/bin/activate \
	    && dfxml_to_case \
	      --debug \
	      --output-format=json-ld \
	      single_file_0.dfxml \
	      _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_validate \
	    _$@
	mv _$@ $@

single_file_1.rdf: \
  $(dfxml_to_case_dependencies) \
  single_file_0.dfxml
	rm -f _$@
	export CDO_DEMO_NONRANDOM_UUID_BASE=$(top_srcdir) \
	  && source $(top_srcdir)/tests/venv/bin/activate \
	    && dfxml_to_case \
	      --debug \
	      --output-format=xml \
	      single_file_0.dfxml \
	      _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_validate \
	    _$@
	mv _$@ $@

single_file_1.ttl: \
  $(dfxml_to_case_dependencies) \
  single_file_0.dfxml
	rm -f _$@
	export CDO_DEMO_NONRANDOM_UUID_BASE=$(top_srcdir) \
	  && source $(top_srcdir)/tests/venv/bin/activate \
	    && dfxml_to_case \
	      --debug  \
	      --output-format=ttl \
	      single_file_0.dfxml \
	      _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_validate \
	    _$@
	mv _$@ $@

single_file_2.dfxml: \
  $(case_to_dfxml_dependencies) \
  single_file_1.ttl
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_to_dfxml \
	    --debug \
	    single_file_1.ttl \
	    __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

single_file_2.json.dfxml: \
  $(case_to_dfxml_dependencies) \
  single_file_1.json
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_to_dfxml \
	    --debug \
	    single_file_1.json \
	    __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

single_filesystem_single_file_0.dfxml: \
  $(dfxml_xsd) \
  $(objects_py_dependencies) \
  empty.json \
  single_filesystem_single_file_0_dfxml.py
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && python single_filesystem_single_file_0_dfxml.py \
	    __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

single_filesystem_single_file_0_2_deltas.dfxml: \
  $(make_differential_dfxml_dependencies) \
  single_filesystem_single_file_2.dfxml
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && make_differential_dfxml \
	    --debug \
	    --retain-unchanged \
	    single_filesystem_single_file_{0,2}.dfxml \
	    > __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

single_filesystem_single_file_1.ttl: \
  $(dfxml_to_case_dependencies) \
  single_filesystem_single_file_0.dfxml
	rm -f _$@
	export CDO_DEMO_NONRANDOM_UUID_BASE=$(top_srcdir) \
	  && source $(top_srcdir)/tests/venv/bin/activate \
	    && dfxml_to_case \
	      --debug \
	      --output-format=ttl \
	      single_filesystem_single_file_0.dfxml \
	      _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_validate \
	    _$@
	mv _$@ $@

single_filesystem_single_file_2.dfxml: \
  $(case_to_dfxml_dependencies) \
  single_filesystem_single_file_1.ttl
	rm -f __$@ _$@
	source $(top_srcdir)/tests/venv/bin/activate \
	  && case_to_dfxml \
	    --debug \
	    single_filesystem_single_file_1.ttl \
	    __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@
