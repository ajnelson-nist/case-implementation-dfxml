#!/usr/bin/env python

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

__version__ = "0.0.9"

import argparse
import logging
import os
import sys
from typing import Dict, Set

import dfxml
import rdflib.plugins.sparql
from case_utils.inherent_uuid import L_MD5, L_SHA1, L_SHA256
from case_utils.namespace import NS_RDF, NS_UCO_CORE, NS_UCO_OBSERVABLE, NS_UCO_TYPES
from dfxml import objects as Objects
from rdflib import Literal, URIRef
from rdflib.query import ResultRow

_logger = logging.getLogger(os.path.basename(__file__))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    # Thanks to case_plaso_export.py for this one-liner.
    format_choices = sorted(
        [
            p.name
            for p in rdflib.plugin.plugins(kind=rdflib.serializer.Serializer)
            if "/" not in p.name
        ]
    )
    parser.add_argument("--input-format", choices=format_choices)
    parser.add_argument("in_file")
    parser.add_argument("out_dfxml")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    if args.input_format:
        input_format = args.input_format
    else:
        # Guess format from input extension.
        input_ext = os.path.splitext(args.in_file)[1][1:]
        input_format = {"json": "json-ld", "ttl": "ttl", "xml": "xml"}[input_ext]
    graph = rdflib.Graph()
    graph.parse(args.in_file, format=input_format)

    _logger.debug("len(graph) = %d." % len(graph))

    dobj = Objects.DFXMLObject()
    dobj.program = sys.argv[0]
    dobj.program_version = __version__
    dobj.command_line = " ".join(sys.argv)
    dobj.dc["type"] = "CASE transcription"
    dobj.add_creator_library(
        "Python", ".".join(map(str, sys.version_info[0:3]))
    )  # A bit of a bend, but gets the major version information out.
    dobj.add_creator_library("objects.py", Objects.__version__)
    dobj.add_creator_library("dfxml", dfxml.__version__)

    nsdict = {k: v for (k, v) in graph.namespace_manager.namespaces()}

    # Get set of all files.
    n_files: Set[URIRef] = set()
    file_query = rdflib.plugins.sparql.prepareQuery(
        """\
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?nFile
WHERE {
  ?nFile
    a/rdfs:subClassOf* uco-observable:File ;
    .
}
""",
        initNs=nsdict,
    )
    for file_result in graph.query(file_query):
        assert isinstance(file_result, ResultRow)
        assert isinstance(file_result[0], URIRef)
        n_file = file_result[0]
        n_files.add(n_file)

    def _n_file_to_file_object(n_file: URIRef) -> Objects.FileObject:
        """
        Assemble FileObject on-demand.
        """
        # This function uses graph.triples and like accessors instead of
        # SPARQL to avoid unnecessary joins in a one-query-gets-all-
        # OPTIONALs call.
        fobj = Objects.FileObject()
        for n_facet in graph.objects(n_file, NS_UCO_CORE.hasFacet):
            if (n_facet, NS_RDF.type, NS_UCO_OBSERVABLE.ContentDataFacet) in graph:
                for l_size in graph.objects(n_facet, NS_UCO_OBSERVABLE.sizeInBytes):
                    assert isinstance(l_size, Literal)
                    fobj.filesize = int(l_size)
                for n_hash in graph.objects(n_facet, NS_UCO_OBSERVABLE.hash):
                    for triple in graph.triples(
                        (n_hash, NS_UCO_TYPES.hashMethod, L_MD5)
                    ):
                        for l_hash_value in graph.objects(
                            n_hash, NS_UCO_TYPES.hashValue
                        ):
                            fobj.md5 = str(l_hash_value)
                    for triple in graph.triples(
                        (n_hash, NS_UCO_TYPES.hashMethod, L_SHA1)
                    ):
                        for l_hash_value in graph.objects(
                            n_hash, NS_UCO_TYPES.hashValue
                        ):
                            fobj.sha1 = str(l_hash_value)
                    for triple in graph.triples(
                        (n_hash, NS_UCO_TYPES.hashMethod, L_SHA256)
                    ):
                        for l_hash_value in graph.objects(
                            n_hash, NS_UCO_TYPES.hashValue
                        ):
                            fobj.sha256 = str(l_hash_value)
            elif (n_facet, NS_RDF.type, NS_UCO_OBSERVABLE.FileFacet) in graph:
                for l_object in graph.objects(n_facet, NS_UCO_OBSERVABLE.filePath):
                    fobj.filename = str(l_object)
                for l_object in graph.objects(n_facet, NS_UCO_OBSERVABLE.accessedTime):
                    fobj.atime = str(l_object)
                for l_object in graph.objects(n_facet, NS_UCO_OBSERVABLE.modifiedTime):
                    fobj.mtime = str(l_object)
                for l_object in graph.objects(
                    n_facet, NS_UCO_OBSERVABLE.observableCreatedTime
                ):
                    fobj.crtime = str(l_object)
                for l_object in graph.objects(
                    n_facet, NS_UCO_OBSERVABLE.metadataChangeTime
                ):
                    fobj.ctime = str(l_object)
        return fobj

    # Key: UUID in the CASE graph.
    # Value: DFXML Object with an 'append' method.
    uriref_to_container: Dict[URIRef, Objects.AbstractParentObject] = dict()
    filesystem_query = rdflib.plugins.sparql.prepareQuery(
        """\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
SELECT ?nFileSystem ?lFileSystemType
WHERE {
  ?nFileSystem
    a/rdfs:subClassOf* uco-observable:FileSystem ;
    .

  OPTIONAL {
    ?nFileSystem
      uco-core:hasFacet / uco-observable:fileSystemType ?lFileSystemType ;
      .
  }
}
""",
        initNs=nsdict,
    )
    for filesystem_result in graph.query(filesystem_query):
        assert isinstance(filesystem_result, ResultRow)
        assert isinstance(filesystem_result[0], URIRef)
        assert filesystem_result[1] is None or isinstance(filesystem_result[1], Literal)
        n_file_system = filesystem_result[0]
        l_ftype_str = filesystem_result[1]

        # Define and attach DFXML object.
        fsobj = Objects.VolumeObject()
        uriref_to_container[n_file_system] = fsobj
        dobj.append(fsobj)

        # Map.
        if l_ftype_str:
            # File system names are lowercased in DFXML.
            fsobj.ftype_str = l_ftype_str.toPython().lower()

        for parent_result in graph.query("""\
PREFIX drafting: <http://example.org/ontology/drafting/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
SELECT ?lPartitionOffset
WHERE {
  ?nRelationship
    a drafting:StorageMediumRange ;
    uco-core:source ?nFileSystem ;
    uco-core:hasFacet / uco-observable:rangeOffset ?lPartitionOffset
    .
}
"""):
            assert isinstance(parent_result, ResultRow)
            assert isinstance(parent_result[0], Literal)
            l_partition_offset = parent_result[0]
            fsobj.partition_offset = int(l_partition_offset)

        # Append all child file objects.
        child_query = rdflib.plugins.sparql.prepareQuery("""\
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
SELECT DISTINCT ?nFile
WHERE {
  ?nRelationship
    uco-core:kindOfRelationship "Child_Of" ;
    uco-core:source ?nFile ;
    uco-core:target ?nFileSystem ;
    .
}
""")

        for child_result in graph.query(
            child_query, initBindings={"nFileSystem": n_file_system}
        ):
            assert isinstance(child_result, ResultRow)
            assert isinstance(child_result[0], URIRef)
            n_file = child_result[0]
            fsobj.append(_n_file_to_file_object(n_file))
            n_files -= {n_file}
    _logger.debug("len(n_files) = %d." % len(n_files))

    for n_file in n_files:
        dobj.append(_n_file_to_file_object(n_file))

    with open(args.out_dfxml, "w") as out_fh:
        dobj.print_dfxml(output_fh=out_fh)


if __name__ == "__main__":
    main()
