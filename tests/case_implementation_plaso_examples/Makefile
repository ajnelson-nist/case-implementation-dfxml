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

.PHONY: \
  check-TODO

# Retain inferred .dfxml files.
#  C/o: https://www.gnu.org/software/make/manual/html_node/Chained-Rules.html
.PRECIOUS: \
  %.dfxml

%.dfxml: \
  ../../deps/case-implementation-plaso/examples/% \
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

#TODO These files have a problem parsing.  Issue filed here:
#  https://github.com/casework/case-implementation-plaso/issues/2
check-TODO: \
  android_calls.xml.dfxml \
  android_sms.xml.dfxml \
  lvm.xml.dfxml \
  mft.xml.dfxml \
  skype.xml.dfxml \
  tsk_volume_system.xml
	@echo "INFO:Makefile:The check-TODO targets now pass and can be put back into place in the validates.log dependencies." >&2

android_calls.validates.log: \
  android_calls.json.dfxml \
  android_calls.ttl.dfxml
	touch $@

android_sms.validates.log: \
  android_sms.json.dfxml \
  android_sms.ttl.dfxml
	touch $@

bz2.validates.log: \
  bz2.json.dfxml \
  bz2.ttl.dfxml \
  bz2.xml.dfxml
	touch $@

check: \
  android_calls.validates.log \
  android_sms.validates.log \
  bz2.validates.log \
  lvm.validates.log \
  mft.validates.log \
  skype.validates.log \
  tsk_volume_system.validates.log

clean:
	@rm -f \
	  *.dfxml

lvm.validates.log: \
  lvm.json.dfxml \
  lvm.ttl.dfxml
	touch $@

mft.validates.log: \
  mft.json.dfxml \
  mft.ttl.dfxml
	touch $@

skype.validates.log: \
  skype.json.dfxml \
  skype.ttl.dfxml
	touch $@

tsk_volume_system.validates.log: \
  tsk_volume_system.json.dfxml \
  tsk_volume_system.ttl.dfxml
	touch $@
