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

#BOOKMARK^
dfxml_xsd := $(top_srcdir)/deps/dfxml_schema/dfxml.xsd

dfxml_top_srcdir := $(top_srcdir)/deps/dfxml

objects_py_dependencies := \
  $(dfxml_top_srcdir)/dfxml/__init__.py \
  $(dfxml_top_srcdir)/dfxml/objects.py

case_to_dfxml_dependencies := \
  $(objects_py_dependencies) \
  $(top_srcdir)/case_to_dfxml.py

#BOOKMARKv

all:

Oresteia.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/Oresteia/Oresteia.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

accounts.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/accounts/accounts.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

bulk_extractor_forensic_path.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/bulk_extractor_forensic_path/bulk_extractor_forensic_path.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

call_log.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/call_log/call_log.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

device.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/device/device.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

exif_data.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/exif_data/exif_data.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

file.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/file/file.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

forensic_lifecycle.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/forensic_lifecycle/forensic_lifecycle.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

location.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/location/location.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

message.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/message/message.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

multipart_file.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/multipart_file/multipart_file.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

raw_data.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/raw_data/raw_data.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

reconstructed_file.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/reconstructed_file/reconstructed_file.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

sms_and_contacts.dfxml: \
  ../../deps/CASE-Examples/examples/illustrations/sms_and_contacts/sms_and_contacts.json
	$(MAKE) \
	  subject_jsonld=$< \
	  --file example.mk

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
  raw_data.dfxml \
  reconstructed_file.dfxml \
  sms_and_contacts.dfxml

clean:
	@rm -f \
	  *.dfxml
