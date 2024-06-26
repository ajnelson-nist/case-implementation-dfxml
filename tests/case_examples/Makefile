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

top_srcdir := ../..

dfxml_top_srcdir := $(top_srcdir)/deps/dfxml

objects_py_dependencies := \
  $(dfxml_top_srcdir)/dfxml/__init__.py \
  $(dfxml_top_srcdir)/dfxml/objects.py

case_to_dfxml_dependencies := \
  $(objects_py_dependencies) \
  $(top_srcdir)/case_to_dfxml.py

all:

# Retain inferred .dfxml files.
#  C/o: https://www.gnu.org/software/make/manual/html_node/Chained-Rules.html
.PRECIOUS: \
  %.dfxml

%.dfxml.validates.log: \
  %.dfxml \
  ../../deps/dfxml_schema/dfxml.xsd
	xmllint --schema ../../deps/dfxml_schema/dfxml.xsd $< >/dev/null
	touch $@

%.dfxml: \
  ../../deps/case/examples/%.json \
  $(case_to_dfxml_dependencies) \
  ../../.setup_complete
	python ../../case_to_dfxml.py $< >(xmllint --format - > _$@)
	mv _$@ $@

# NOTE: Some example files are purposefully omitted because they include design comments that Python's JSON library cannot parse.  These files are:
#  reconstructed_file.json
#  sms_and_contacts.json

check: \
  Oresteia.dfxml.validates.log \
  accounts.dfxml.validates.log \
  bulk_extractor_forensic_path.dfxml.validates.log \
  call_log.dfxml.validates.log \
  device.dfxml.validates.log \
  exif_data.dfxml.validates.log \
  file.dfxml.validates.log \
  forensic_lifecycle.dfxml.validates.log \
  location.dfxml.validates.log \
  message.dfxml.validates.log \
  multipart_file.dfxml.validates.log \
  raw_data.dfxml.validates.log

clean:
	@rm -f *.dfxml *.log
