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

all:

%.dfxml.validates.log: \
  %.dfxml
	xmllint --schema ../deps/dfxml_schema/dfxml.xsd $< >/dev/null
	touch $@

check: \
  empty.json \
  single_file_1.rdf \
  verify_single_file.log \
  verify_single_filesystem_single_file.log
	@echo "Unit tests pass!"

clean:
	@rm -rf *dfxml *json *log *pyc *rdf *ttl __pycache__

clean-recursive:
	$(MAKE) -C case_examples clean

empty.json: \
  ../.setup_complete \
  empty_json.py
	rm -f _$@
	python empty_json.py _$@
	mv _$@ $@

single_file_0.dfxml: \
  Objects.py \
  empty.json \
  single_file_0_dfxml.py
	rm -f _$@ __$@
	python single_file_0_dfxml.py >(xmllint --format - > _$@)
	mv _$@ $@

single_filesystem_single_file_0.dfxml: \
  Objects.py \
  empty.json \
  single_filesystem_single_file_0_dfxml.py
	rm -f _$@ __$@
	python single_filesystem_single_file_0_dfxml.py >(xmllint --format - > _$@)
	mv _$@ $@

single_file_1.rdf: \
  ../.setup_complete \
  ../dfxml_to_case.py \
  single_file_0.dfxml.validates.log
	rm -f _$@
	python ../dfxml_to_case.py --debug --output-format=xml single_file_0.dfxml _$@
	mv _$@ $@

single_file_1.ttl: \
  ../.setup_complete \
  ../dfxml_to_case.py \
  single_file_0.dfxml.validates.log
	rm -f _$@
	python ../dfxml_to_case.py --debug --output-format=ttl single_file_0.dfxml _$@
	mv _$@ $@

single_filesystem_single_file_1.ttl: \
  ../.setup_complete \
  ../dfxml_to_case.py \
  single_filesystem_single_file_0.dfxml.validates.log
	rm -f _$@
	python ../dfxml_to_case.py --debug --output-format=ttl single_filesystem_single_file_0.dfxml _$@
	mv _$@ $@

single_file_2.dfxml: \
  ../case_to_dfxml.py \
  single_file_1.ttl
	rm -f _$@ __$@
	python ../case_to_dfxml.py --debug single_file_1.ttl >(xmllint --format - > _$@)
	mv _$@ $@

single_filesystem_single_file_2.dfxml: \
  ../case_to_dfxml.py \
  single_filesystem_single_file_1.ttl
	rm -f _$@ __$@
	python ../case_to_dfxml.py --debug single_filesystem_single_file_1.ttl >(xmllint --format - > _$@)
	mv _$@ $@

single_file_0_2_deltas.dfxml: \
  make_differential_dfxml.py \
  single_file_2.dfxml.validates.log
	rm -f _$@
	python make_differential_dfxml.py --retain-unchanged single_file_{0,2}.dfxml | xmllint --format - > _$@
	mv _$@ $@

single_filesystem_single_file_0_2_deltas.dfxml: \
  make_differential_dfxml.py \
  single_filesystem_single_file_2.dfxml.validates.log
	rm -f _$@
	python make_differential_dfxml.py --retain-unchanged single_filesystem_single_file_{0,2}.dfxml | xmllint --format - > _$@
	mv _$@ $@

verify_single_file.log: \
  single_file_0_2_deltas.dfxml.validates.log \
  verify_single_file.py
	python verify_single_file.py single_file_0_2_deltas.dfxml
	touch $@

verify_single_filesystem_single_file.log: \
  single_filesystem_single_file_0_2_deltas.dfxml.validates.log \
  verify_single_filesystem_single_file.py
	python verify_single_file.py single_filesystem_single_file_0_2_deltas.dfxml
	touch $@
