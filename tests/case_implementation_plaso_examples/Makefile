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
  ../../deps/case-implementation-plaso/examples/%.json \
  ../../.setup_complete \
  ../../Objects.py \
  ../../case_to_dfxml.py \
  ../../dfxml.py
	python ../../case_to_dfxml.py $< >(xmllint --format - > _$@)
	mv _$@ $@

check: \
  android_calls.dfxml.validates.log \
  android_sms.dfxml.validates.log \
  bz2.dfxml.validates.log \
  lvm.dfxml.validates.log \
  mft.dfxml.validates.log \
  skype.dfxml.validates.log \
  tsk_volume_system.dfxml.validates.log

clean:
	@rm -f *.dfxml *.log
