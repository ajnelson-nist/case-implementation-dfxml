#!/usr/bin/env python

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

"""
This program is based on example data from:
https://github.com/casework/case/blob/master/examples/file.json
"""

__version__ = "0.0.2"

import logging
import os

_logger = logging.getLogger(os.path.basename(__file__))

import rdflib

import Objects
import case

def fileobject_to_trace(case_document, fobj):
    f = case_document.create_uco_object("Trace")

    # pbd: Property bundle dictionary. Recycled variable name.

    #TODO: Type the date times as xsd:datetime.
    pbd = dict()
    if fobj.filename:
        pbd["filePath"] = fobj.filename
    if fobj.atime:
        pbd["accessedTime"] = str(fobj.atime)
    if fobj.ctime:
        pbd["changedTime"] = str(fobj.ctime)
    if fobj.crtime:
        pbd["createdTime"] = str(fobj.crtime)
    if fobj.mtime:
        pbd["modifiedTime"] = str(fobj.mtime)
    if len(pbd) > 0:
        f.create_property_bundle("File", **pbd)

    pbd = dict()
    any_hashes = None
    if not fobj.filesize is None:
        pbd["sizeInBytes"] = fobj.filesize
    if fobj.md5 or fobj.sha1 or fobj.sha256:
        any_hashes = True
    else:
        any_hashes = False
    cd_pb = None
    if len(pbd) > 0 or any_hashes:
        cd_pb = f.create_property_bundle("ContentData", **pbd)
    if cd_pb and any_hashes:
        if fobj.md5:
            hash_pb = case_document.create_hash("MD5", fobj.md5)
            cd_pb.add('hash', hash_pb)
        if fobj.sha1:
            hash_pb = case_document.create_hash("SHA1", fobj.sha1)
            cd_pb.add('hash', hash_pb)
        if fobj.sha256:
            hash_pb = case_document.create_hash("SHA256", fobj.sha256)
            cd_pb.add('hash', hash_pb)
    return f

def volumeobject_to_trace(case_document, vobj):
    v = case_document.create_uco_object("Trace")
    pbd = dict()
    if vobj.ftype_str:
        # Special-case some file systems that are spelled differently in CASE; default to uppercase of DFXML's value.
        pbd["fileSystemType"] = {
          "7z": "SevenZ"
        }.get(vobj.ftype_str) or vobj.ftype_str.upper()
    if not vobj.partition_offset is None:
        pbd["partitionOffset"] = vobj.partition_offset
    if len(pbd) > 0:
        v.create_property_bundle("FileSystem", **pbd)
    return v

def main():
    case_document = case.Document()
    trace_object_stack = []
    for (event, obj) in Objects.iterparse(args.in_dfxml):
        if event == "start":
            if isinstance(obj, Objects.VolumeObject):
                trace = volumeobject_to_trace(case_document, obj)
                trace_object_stack.append(trace)
        elif event == "end":
            if isinstance(obj, Objects.VolumeObject):
                trace_object_stack.pop()
            elif isinstance(obj, Objects.FileObject):
                trace = fileobject_to_trace(case_document, obj)
                if len(trace_object_stack) > 0:
                    # Create a containment relationship.
                    r = case_document.create_uco_object(
                      "Relationship",
                      isDirectional=True,
                      kindOfRelationship="contained-within",
                      source=rdflib.URIRef(trace.uri),
                      target=rdflib.URIRef(trace_object_stack[-1].uri)
                    )
                    #_logger.debug("Container: %r." % trace_object_stack[-1])
                    #_logger.debug("Containee: %r." % trace)
                    #_logger.debug("dir(Containee): %r." % dir(trace))
                    #_logger.debug("Container.uri: %r." % rdflib.URIRef(trace_object_stack[-1].uri))
                    #_logger.debug("Containee.uri: %r." % rdflib.URIRef(trace.uri))

    case_document.serialize(format=args.output_format, destination=args.out_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--output-format", default="ttl")
    parser.add_argument("in_dfxml")
    parser.add_argument("out_file")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    main()
