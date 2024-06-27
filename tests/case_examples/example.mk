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

subject_jsonld ?=
ifeq ($(subject_jsonld),)
$(error subject_jsonld must be specified)
endif

subject_dfxml := $(subst .json,.dfxml,$(shell basename $(subject_jsonld)))
ifeq ($(subject_dfxml),)
$(error subject_dfxml could not be computed from subject_jsonld=$(subject_jsonld))
endif

top_srcdir := ../..

dfxml_top_srcdir := $(top_srcdir)/deps/dfxml

dfxml_xsd := $(dfxml_top_srcdir)/dependencies/dfxml_schema/dfxml.xsd

objects_py_dependencies := \
  $(dfxml_top_srcdir)/dfxml/__init__.py \
  $(dfxml_top_srcdir)/dfxml/objects.py

case_to_dfxml_dependencies := \
  $(objects_py_dependencies) \
  $(top_srcdir)/case_dfxml/case_to_dfxml.py

all: \
  $(subject_dfxml)

$(subject_dfxml): \
  $(subject_jsonld) \
  $(dfxml_xsd) \
  $(case_to_dfxml_dependencies) \
  ../.venv.done.log
	rm -f __$@ _$@
	source ../venv/bin/activate \
	  && case_to_dfxml \
	    $< \
	    __$@
	xmllint \
	  --format \
	  --schema $(dfxml_xsd) \
	  __$@ \
	  > _$@
	rm __$@
	mv _$@ $@
