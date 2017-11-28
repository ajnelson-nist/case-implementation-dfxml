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

__version__ = "0.0.7"

import collections
import logging
import os
import sys

_logger = logging.getLogger(os.path.basename(__file__))

import rdflib.plugins.sparql

import Objects

def main():
    if args.input_format:
        input_format = args.input_format
    else:
        # Guess format from input extension.
        input_ext = os.path.splitext(args.in_file)[1][1:]
        input_format = {
          "json":"json-ld",
          "ttl":"ttl",
          "xml":"xml"
        }[input_ext]
    g = rdflib.Graph()
    g.parse(args.in_file, format=input_format)

    _logger.debug("len(g) = %d." % len(g))

    dobj = Objects.DFXMLObject(version="1.1.1")
    dobj.program = sys.argv[0]
    dobj.program_version = __version__
    dobj.command_line = " ".join(sys.argv)
    dobj.dc["type"] = "CASE transcription"
    dobj.add_creator_library("Python", ".".join(map(str, sys.version_info[0:3]))) #A bit of a bend, but gets the major version information out.
    dobj.add_creator_library("Objects.py", Objects.__version__)
    dobj.add_creator_library("dfxml.py", Objects.dfxml.__version__)

    nsdict = {k:v for (k,v) in g.namespace_manager.namespaces()}

    # Key: UUID in the CASE graph.
    # Value: DFXML Object with an 'append' method.
    uuid_to_container = dict()
    uuid_to_container[""] = dobj
    filesystem_query = rdflib.plugins.sparql.prepareQuery("""\
SELECT ?trace ?fileSystemType ?partitionOffset
WHERE
{
  ?trace a case:Trace .
  ?trace case:propertyBundle ?propertyBundleFileSystem .
  ?propertyBundleFileSystem a case:FileSystem ;

  OPTIONAL
  {
    ?propertyBundleFileSystem case:fileSystemType ?fileSystemType .
  }

  OPTIONAL
  {
    ?propertyBundleFileSystem case:partitionOffset ?partitionOffset .
  }
}
""", initNs=nsdict)
    filesystem_results = g.query(filesystem_query)
    for filesystem_result in filesystem_results:
        (l_uuid, l_ftype_str, l_partition_offset) = filesystem_result
        fsobj = Objects.VolumeObject()
        if l_ftype_str:
            #File system names are lowercased in DFXML.
            fsobj.ftype_str = l_ftype_str.toPython().lower()
        if not l_partition_offset is None:
            fsobj.partition_offset = l_partition_offset.toPython()
        uuid_to_container[l_uuid.toPython()] = fsobj
        dobj.append(fsobj)
    _logger.debug("len(uuid_to_container) = %d." % len(uuid_to_container))
    _logger.debug("uuid_to_container = %r." % uuid_to_container)

    # Group UUIDs of file traces by their containing file system's UUID (empty string if file system UUID is absent).
    fsobj_uuid_to_fobj_uuid_set = collections.defaultdict(set)
    fsobj_containee_results = g.query("""\
SELECT ?fstrace ?ftrace
WHERE
{
  ?ftrace a case:Trace .
  ?ftrace case:propertyBundle ?propertyBundleFile .
  ?propertyBundleFile a case:File .

  OPTIONAL
  {
    ?relationship a case:Relationship ;
      case:isDirectional true ;
      case:kindOfRelationship "contained-within" ;
      case:source ?ftrace ;
      case:target ?fstrace .

    ?fstrace a case:Trace .
    ?fstrace case:propertyBundle ?propertyBundleFileSystem .
    ?propertyBundleFileSystem a case:FileSystem .
  }
}
""")
    for fsobj_containee_result in fsobj_containee_results:
        (l_fs_uuid, l_f_uuid) = fsobj_containee_result
        f_uuid = l_f_uuid.toPython()
        fs_uuid = "" if l_fs_uuid is None else l_fs_uuid.toPython()
        fsobj_uuid_to_fobj_uuid_set[fs_uuid].add(f_uuid)
    #_logger.debug("len(fsobj_uuid_to_fobj_uuid_set) = %d." % len(fsobj_uuid_to_fobj_uuid_set))
    #_logger.debug("fsobj_uuid_to_fobj_uuid_set = %r." % fsobj_uuid_to_fobj_uuid_set)

    file_query = rdflib.plugins.sparql.prepareQuery("""\
SELECT ?filename ?mtime ?atime ?ctime ?crtime ?filesize ?md5 ?sha1 ?sha256
WHERE
{
  ?trace a case:Trace .
  ?trace case:propertyBundle ?propertyBundleFile .
  ?propertyBundleFile a case:File .

  OPTIONAL { ?propertyBundleFile case:filePath ?filename . }
  OPTIONAL { ?propertyBundleFile case:accessedTime ?atime . }
  OPTIONAL { ?propertyBundleFile case:changedTime ?ctime . }
  OPTIONAL { ?propertyBundleFile case:createdTime ?crtime . }
  OPTIONAL { ?propertyBundleFile case:modifiedTime ?mtime . }

  OPTIONAL
  {
    ?trace case:propertyBundle ?propertyBundleContentData .
    ?propertyBundleContentData a case:ContentData .
    ?propertyBundleContentData case:sizeInBytes ?filesize .

    OPTIONAL
    {
      ?propertyBundleContentData case:hash ?caseHashMD5 .
      ?caseHashMD5 a case:Hash ;
        case:hashMethod "MD5" ;
        case:hashValue ?md5 .
    }

    OPTIONAL
    {
      ?propertyBundleContentData case:hash ?caseHashSHA1 .
      ?caseHashSHA1 a case:Hash ;
        case:hashMethod "SHA1" ;
        case:hashValue ?sha1 .
    }

    OPTIONAL
    {
      ?propertyBundleContentData case:hash ?caseHashSHA256 .
      ?caseHashSHA256 a case:Hash ;
        case:hashMethod "SHA256" ;
        case:hashValue ?sha256 .
    }
  }
}
""", initNs=nsdict)
    for fs_uuid in fsobj_uuid_to_fobj_uuid_set.keys():
        container = uuid_to_container[fs_uuid]
        _logger.debug(container)
        for f_uuid in fsobj_uuid_to_fobj_uuid_set[fs_uuid]:
            file_results = g.query(file_query, initBindings={'trace': rdflib.URIRef(f_uuid)})

            for (l_filename, l_mtime, l_atime, l_ctime, l_crtime, l_filesize, l_md5, l_sha1, l_sha256) in file_results:
                fobj = Objects.FileObject()
                fobj.filename = None if l_filename is None else l_filename.toPython()
                fobj.filesize = None if l_filesize is None else l_filesize.toPython()
                fobj.mtime = None if l_mtime is None else l_mtime.toPython()
                fobj.atime = None if l_atime is None else l_atime.toPython()
                fobj.ctime = None if l_ctime is None else l_ctime.toPython()
                fobj.crtime = None if l_crtime is None else l_crtime.toPython()
                fobj.md5 = None if l_md5 is None else l_md5.toPython()
                fobj.sha1 = None if l_sha1 is None else l_sha1.toPython()
                fobj.sha256 = None if l_sha256 is None else l_sha256.toPython()
                container.append(fobj)

    with open(args.out_dfxml, "w") as out_fh:
        dobj.print_dfxml(output_fh=out_fh)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    # Thanks to case_plaso_export.py for this one-liner.
    format_choices = sorted([
      p.name \
        for p in rdflib.plugin.plugins(kind=rdflib.serializer.Serializer) \
          if '/' not in p.name
    ])
    parser.add_argument("--input-format", choices=format_choices)
    parser.add_argument("in_file")
    parser.add_argument("out_dfxml")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    main()
