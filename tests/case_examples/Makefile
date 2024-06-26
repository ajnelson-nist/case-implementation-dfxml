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

top_srcdir := ../..

dfxml_xsd := $(top_srcdir)/deps/dfxml_schema/dfxml.xsd

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

%.dfxml: \
  ../../deps/case/examples/%.json \
  $(dfxml_xsd) \
  $(case_to_dfxml_dependencies) \
  ../.venv.done.log
	rm -f __$@ _$@
	source ../venv/bin/activate \
	  && python ../../case_to_dfxml.py \
	    $< \
	    __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@

# NOTE: Some example files are purposefully omitted because they include design comments that Python's JSON library cannot parse.  These files are:
#  reconstructed_file.json
#  sms_and_contacts.json

check: \
  Oresteia.dfxml \
  accounts.dfxml \
  bulk_extractor_forensic_path.dfxml \
  call_log.dfxml \
  device.dfxml \
  exif_data.dfxml \
  file.dfxml \
  forensic_lifecycle.dfxml \
  location.dfxml \
  message.dfxml \
  multipart_file.dfxml \
  raw_data.dfxml

clean:
	@rm -f \
	  *.dfxml
