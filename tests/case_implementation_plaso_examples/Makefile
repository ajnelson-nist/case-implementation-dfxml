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

.PHONY: \
  check-TODO

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
  ../../deps/case-implementation-plaso/examples/% \
  $(case_to_dfxml_dependencies) \
  ../../.setup_complete
	python ../../case_to_dfxml.py $< >(xmllint --format - > _$@)
	mv _$@ $@

#TODO These files have a problem parsing.  Issue filed here:
#  https://github.com/casework/case-implementation-plaso/issues/2
check-TODO: \
  android_calls.xml.dfxml.validates.log \
  android_sms.xml.dfxml.validates.log \
  lvm.xml.dfxml.validates.log \
  mft.xml.dfxml.validates.log \
  skype.xml.dfxml.validates.log \
  tsk_volume_system.xml.dfxml.validates.log
	@echo "INFO:Makefile:The check-TODO targets now pass and can be put back into place in the validates.log dependencies." >&2

android_calls.validates.log: \
  android_calls.json.dfxml.validates.log \
  android_calls.ttl.dfxml.validates.log
	touch $@

android_sms.validates.log: \
  android_sms.json.dfxml.validates.log \
  android_sms.ttl.dfxml.validates.log
	touch $@

bz2.validates.log: \
  bz2.json.dfxml.validates.log \
  bz2.ttl.dfxml.validates.log \
  bz2.xml.dfxml.validates.log
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
	@rm -f *.dfxml *.log

lvm.validates.log: \
  lvm.json.dfxml.validates.log \
  lvm.ttl.dfxml.validates.log
	touch $@

mft.validates.log: \
  mft.json.dfxml.validates.log \
  mft.ttl.dfxml.validates.log
	touch $@

skype.validates.log: \
  skype.json.dfxml.validates.log \
  skype.ttl.dfxml.validates.log
	touch $@

tsk_volume_system.validates.log: \
  tsk_volume_system.json.dfxml.validates.log \
  tsk_volume_system.ttl.dfxml.validates.log
	touch $@
