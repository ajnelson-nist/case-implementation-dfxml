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

top_srcdir := ..

dfxml_top_srcdir := $(top_srcdir)/deps/dfxml

objects_py_dependencies := \
  $(dfxml_top_srcdir)/dfxml/__init__.py \
  $(dfxml_top_srcdir)/dfxml/objects.py

make_differential_dfxml_dependencies := \
  $(dfxml_top_srcdir)/dfxml/bin/make_differential_dfxml.py \
  $(objects_py_dependencies)

case_to_dfxml_dependencies := \
  $(objects_py_dependencies) \
  $(top_srcdir)/case_to_dfxml.py

dfxml_to_case_dependencies := \
  $(objects_py_dependencies) \
  $(top_srcdir)/dfxml_to_case.py

all:

%.dfxml.validates.log: \
  %.dfxml
	xmllint --schema ../deps/dfxml_schema/dfxml.xsd $< >/dev/null
	touch $@

.PHONY: \
  check-TODO \
  check-basic \
  check-basic-TODO \
  check-case_examples \
  check-case_implementation_plaso_examples \
  check-case_implementation_plaso_examples-TODO \
  clean-case_examples \
  clean-case_implementation_plaso_examples \
  clean-recursive

check: \
  check-case_examples \
  check-case_implementation_plaso_examples
	@echo "Unit tests pass!"

check-TODO: \
  check-basic-TODO \
  check-case_implementation_plaso_examples-TODO

check-basic: \
  empty.json \
  single_file_1.rdf \
  verify_single_file.log \
  verify_single_filesystem_single_file.log

check-basic-TODO: \
  verify_single_file_via_jsonld.log

check-case_examples: \
  check-basic
	$(MAKE) -C case_examples check

check-case_implementation_plaso_examples: \
  check-basic
	$(MAKE) -C case_implementation_plaso_examples check

check-case_implementation_plaso_examples-TODO: \
  check-case_implementation_plaso_examples
	$(MAKE) -C case_implementation_plaso_examples check-TODO

clean: \
  clean-recursive
	@rm -rf *dfxml *json *log *pyc *rdf *ttl __pycache__

clean-case_examples:
	$(MAKE) -C case_examples clean

clean-case_implementation_plaso_examples:
	$(MAKE) -C case_implementation_plaso_examples clean

clean-recursive: \
  clean-case_examples \
  clean-case_implementation_plaso_examples

empty.json: \
  ../.setup_complete \
  empty_json.py
	rm -f _$@
	python empty_json.py _$@
	mv _$@ $@

single_file_0.dfxml: \
  $(objects_py_dependencies) \
  empty.json \
  single_file_0_dfxml.py
	rm -f _$@ __$@
	python single_file_0_dfxml.py >(xmllint --format - > _$@)
	mv _$@ $@

single_file_0_2_deltas.dfxml: \
  $(make_differential_dfxml_dependencies) \
  single_file_2.dfxml.validates.log
	rm -f _$@
	make_differential_dfxml --retain-unchanged single_file_{0,2}.dfxml | xmllint --format - > _$@
	mv _$@ $@

single_file_0_json_2_deltas.dfxml: \
  $(make_differential_dfxml_dependencies) \
  single_file_2.json.dfxml.validates.log
	rm -f _$@
	make_differential_dfxml --retain-unchanged single_file_0.dfxml single_file_2.json.dfxml | xmllint --format - > _$@
	mv _$@ $@

single_file_1.json: \
  ../.setup_complete \
  $(dfxml_to_case_dependencies) \
  single_file_0.dfxml.validates.log
	rm -f _$@
	python ../dfxml_to_case.py --debug --output-format=json-ld single_file_0.dfxml _$@
	mv _$@ $@

single_file_1.rdf: \
  ../.setup_complete \
  $(dfxml_to_case_dependencies) \
  single_file_0.dfxml.validates.log
	rm -f _$@
	python ../dfxml_to_case.py --debug --output-format=xml single_file_0.dfxml _$@
	mv _$@ $@

single_file_1.ttl: \
  ../.setup_complete \
  $(dfxml_to_case_dependencies) \
  single_file_0.dfxml.validates.log
	rm -f _$@
	python ../dfxml_to_case.py --debug --output-format=ttl single_file_0.dfxml _$@
	mv _$@ $@

single_file_2.dfxml: \
  $(case_to_dfxml_dependencies) \
  single_file_1.ttl
	rm -f _$@ __$@
	python ../case_to_dfxml.py --debug single_file_1.ttl >(xmllint --format - > _$@)
	mv _$@ $@

single_file_2.json.dfxml: \
  $(case_to_dfxml_dependencies) \
  single_file_1.json
	rm -f _$@ __$@
	python ../case_to_dfxml.py --debug single_file_1.json >(xmllint --format - > _$@)
	mv _$@ $@

single_filesystem_single_file_0.dfxml: \
  $(objects_py_dependencies) \
  empty.json \
  single_filesystem_single_file_0_dfxml.py
	rm -f _$@ __$@
	python single_filesystem_single_file_0_dfxml.py >(xmllint --format - > _$@)
	mv _$@ $@

single_filesystem_single_file_0_2_deltas.dfxml: \
  $(make_differential_dfxml_dependencies) \
  single_filesystem_single_file_2.dfxml.validates.log
	rm -f _$@
	make_differential_dfxml --debug --retain-unchanged single_filesystem_single_file_{0,2}.dfxml | xmllint --format - > _$@
	mv _$@ $@

single_filesystem_single_file_1.ttl: \
  ../.setup_complete \
  $(dfxml_to_case_dependencies) \
  single_filesystem_single_file_0.dfxml.validates.log
	rm -f _$@
	python ../dfxml_to_case.py --debug --output-format=ttl single_filesystem_single_file_0.dfxml _$@
	mv _$@ $@

single_filesystem_single_file_2.dfxml: \
  $(case_to_dfxml_dependencies) \
  single_filesystem_single_file_1.ttl
	rm -f _$@ __$@
	python ../case_to_dfxml.py --debug single_filesystem_single_file_1.ttl >(xmllint --format - > _$@)
	mv _$@ $@

# Verify a DFXML file that just lists a single file can translate into CASE and back via some format.
verify_single_file.log: \
  single_file_0_2_deltas.dfxml.validates.log \
  verify_single_file.py
	python verify_single_file.py single_file_0_2_deltas.dfxml
	touch $@

# Verify a DFXML file that just lists a single file can translate into CASE and back via JSON-LD.
# This is a dependency of check-basic-TODO because at the time of this writing the CASE API currently doesn't read the JSON-LD output it generates.  The parse() method returns an empty graph.
verify_single_file_via_jsonld.log: \
  single_file_0_json_2_deltas.dfxml.validates.log \
  verify_single_file.py
	python verify_single_file.py single_file_0_json_2_deltas.dfxml
	touch $@

verify_single_filesystem_single_file.log: \
  single_filesystem_single_file_0_2_deltas.dfxml.validates.log \
  verify_single_filesystem_single_file.py
	python verify_single_file.py single_filesystem_single_file_0_2_deltas.dfxml
	touch $@
