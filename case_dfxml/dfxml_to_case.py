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

"""
This program is based on example data from:
https://github.com/casework/case/blob/master/examples/file.json
"""

__version__ = "0.0.4"

import argparse
import logging
import os
from typing import Any, List, Optional

import cdo_local_uuid
from case_utils.inherent_uuid import (
    L_MD5,
    L_SHA1,
    L_SHA256,
    get_facet_uriref,
    hash_method_value_uuid,
)
from case_utils.namespace import (
    NS_OWL,
    NS_RDF,
    NS_RDFS,
    NS_UCO_CORE,
    NS_UCO_OBSERVABLE,
    NS_UCO_TYPES,
    NS_XSD,
)
from cdo_local_uuid import local_uuid
from dfxml import objects as Objects
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.util import guess_format

_logger = logging.getLogger(os.path.basename(__file__))

NS_DRAFTING = Namespace("http://example.org/ontology/drafting/")


def _inline_storage_medium_range_definition(graph: Graph) -> None:
    for triple in graph.triples(
        (NS_DRAFTING.StorageMediumRange, NS_RDF.type, NS_OWL.Class)
    ):
        # Already defined once.
        return
    graph.add((NS_DRAFTING.StorageMediumRange, NS_RDF.type, NS_OWL.Class))
    graph.add(
        (
            NS_DRAFTING.StorageMediumRange,
            NS_RDFS.label,
            Literal("StorageMediumRange", lang="en"),
        )
    )
    graph.add(
        (
            NS_DRAFTING.StorageMediumRange,
            NS_RDFS.subClassOf,
            NS_UCO_OBSERVABLE.ObservableRelationship,
        )
    )
    # The intended restrictions on the uco-core:Relationship properties
    # are as follows, but aren't inlined in order to avoid duplicate blank node
    # issues:
    #
    # kindOfRelationship: Contained_Within suggested.
    # source: A storage system object, including File, FileSystem,
    #         Partition, PartitionSystem, and non-File Image.
    # target: The union of Image, Disk, and possibly a new class to
    #         represent the available storage presented by multi-disk
    #         storage systems (e.g. RAID arrays).


def fileobject_to_trace(
    graph: Graph,
    ns_kb: Namespace,
    fobj: Objects.FileObject,
    *args: Any,
    parent_trace: Optional[URIRef] = None,
    use_inherent_uuids: bool = False,
    **kwargs: Any
) -> URIRef:
    n_file = ns_kb["File-" + local_uuid()]
    graph.add((n_file, NS_RDF.type, NS_UCO_OBSERVABLE.File))

    # This variable should be accessed with one or more calls to _n_content_data_facet().
    n_content_data_facet: Optional[URIRef] = None

    def _n_content_data_facet() -> URIRef:
        """
        Idempotent initialization of n_content_data_facet.
        """
        nonlocal n_content_data_facet
        nonlocal use_inherent_uuids
        if n_content_data_facet is None:
            if use_inherent_uuids:
                n_content_data_facet = get_facet_uriref(
                    n_file, NS_UCO_OBSERVABLE.ContentDataFacet, namespace=ns_kb
                )
            else:
                n_content_data_facet = ns_kb["ContentDataFacet-" + local_uuid()]
            graph.add(
                (n_content_data_facet, NS_RDF.type, NS_UCO_OBSERVABLE.ContentDataFacet)
            )
            graph.add((n_file, NS_UCO_CORE.hasFacet, n_content_data_facet))
        return n_content_data_facet

    # This variable should be accessed with one or more calls to _n_file_facet().
    n_file_facet: Optional[URIRef] = None

    def _n_file_facet() -> URIRef:
        """
        Idempotent initialization of n_file_facet.
        """
        nonlocal n_file_facet
        nonlocal use_inherent_uuids
        if n_file_facet is None:
            if use_inherent_uuids:
                n_file_facet = get_facet_uriref(
                    n_file, NS_UCO_OBSERVABLE.FileFacet, namespace=ns_kb
                )
            else:
                n_file_facet = ns_kb["FileFacet-" + local_uuid()]
            graph.add((n_file_facet, NS_RDF.type, NS_UCO_OBSERVABLE.FileFacet))
            graph.add((n_file, NS_UCO_CORE.hasFacet, n_file_facet))
        return n_file_facet

    if fobj.filename:
        graph.add((_n_file_facet(), NS_UCO_OBSERVABLE.filePath, Literal(fobj.filename)))
    if fobj.atime:
        graph.add(
            (
                _n_file_facet(),
                NS_UCO_OBSERVABLE.accessedTime,
                Literal(str(fobj.atime), datatype=NS_XSD.dateTime),
            )
        )
    if fobj.ctime:
        graph.add(
            (
                _n_file_facet(),
                NS_UCO_OBSERVABLE.metadataChangeTime,
                Literal(str(fobj.ctime), datatype=NS_XSD.dateTime),
            )
        )
    if fobj.crtime:
        graph.add(
            (
                _n_file_facet(),
                NS_UCO_OBSERVABLE.observableCreatedTime,
                Literal(str(fobj.crtime), datatype=NS_XSD.dateTime),
            )
        )
    if fobj.mtime:
        graph.add(
            (
                _n_file_facet(),
                NS_UCO_OBSERVABLE.modifiedTime,
                Literal(str(fobj.mtime), datatype=NS_XSD.dateTime),
            )
        )

    if fobj.filesize is not None:
        graph.add(
            (
                _n_content_data_facet(),
                NS_UCO_OBSERVABLE.sizeInBytes,
                Literal(fobj.filesize),
            )
        )
        graph.add(
            (_n_file_facet(), NS_UCO_OBSERVABLE.sizeInBytes, Literal(fobj.filesize))
        )

    def _add_hash(l_hash_method: Literal, s_hash_value: str) -> None:
        l_hash_value = Literal(s_hash_value, datatype=NS_XSD.hexBinary)
        if use_inherent_uuids:
            n_hash = ns_kb[
                "Hash-" + str(hash_method_value_uuid(l_hash_method, l_hash_value))
            ]
        else:
            n_hash = ns_kb["Hash-" + local_uuid()]
        graph.add((n_hash, NS_RDF.type, NS_UCO_TYPES.Hash))
        graph.add((n_hash, NS_UCO_TYPES.hashMethod, l_hash_method))
        graph.add((n_hash, NS_UCO_TYPES.hashValue, l_hash_value))
        graph.add((_n_content_data_facet(), NS_UCO_OBSERVABLE.hash, n_hash))

    if fobj.md5:
        _add_hash(L_MD5, fobj.md5)
    if fobj.sha1:
        _add_hash(L_SHA1, fobj.sha1)
    if fobj.sha256:
        _add_hash(L_SHA256, fobj.sha256)

    if parent_trace is not None:
        # Create a parent-child relationship.
        n_relationship = ns_kb["Relationship-" + local_uuid()]
        graph.add(
            (n_relationship, NS_RDF.type, NS_UCO_OBSERVABLE.ObservableRelationship)
        )
        graph.add((n_relationship, NS_UCO_CORE.isDirectional, Literal(True)))
        graph.add((n_relationship, NS_UCO_CORE.kindOfRelationship, Literal("Child_Of")))
        graph.add((n_relationship, NS_UCO_CORE.source, n_file))
        graph.add((n_relationship, NS_UCO_CORE.target, parent_trace))
        # _logger.debug("Parent: %r." % parent_trace)
        # _logger.debug("Child: %r." % n_file)

    return n_file


def volumeobject_to_trace(
    graph: Graph,
    ns_kb: Namespace,
    vobj: Objects.VolumeObject,
    *args: Any,
    container_image_trace: Optional[URIRef] = None,
    use_inherent_uuids: bool = False,
    **kwargs: Any
) -> URIRef:
    # Behave differently depending on whether vobj is a file system or an archive.
    if vobj.ftype_str == "7z":
        n_volume = ns_kb["File-" + local_uuid()]
        graph.add((n_volume, NS_RDF.type, NS_UCO_OBSERVABLE.ArchiveFile))
    else:
        n_volume = ns_kb["FileSystem-" + local_uuid()]
        graph.add((n_volume, NS_RDF.type, NS_UCO_OBSERVABLE.FileSystem))

        # This variable should be accessed with one or more calls to _n_file_system_facet().
        n_file_system_facet: Optional[URIRef] = None

        def _n_file_system_facet() -> URIRef:
            """
            Idempotent initialization of n_file_system_facet.
            """
            nonlocal n_file_system_facet
            nonlocal use_inherent_uuids
            if n_file_system_facet is None:
                if use_inherent_uuids:
                    n_file_system_facet = get_facet_uriref(
                        n_volume, NS_UCO_OBSERVABLE.FileSystemFacet, namespace=ns_kb
                    )
                else:
                    n_file_system_facet = ns_kb["FileSystmFacet-" + local_uuid()]
                graph.add(
                    (
                        n_file_system_facet,
                        NS_RDF.type,
                        NS_UCO_OBSERVABLE.FileSystemFacet,
                    )
                )
                graph.add((n_volume, NS_UCO_CORE.hasFacet, n_file_system_facet))
            return n_file_system_facet

        if vobj.ftype_str:
            # Default to uppercase of DFXML's value.
            graph.add(
                (
                    _n_file_system_facet(),
                    NS_UCO_OBSERVABLE.fileSystemType,
                    Literal(vobj.ftype_str.upper()),
                )
            )
        if vobj.partition_offset is not None:
            # Create a contained-within relationship to anchor what the
            # offset is relative to.
            # To disambiguate from other Contained_Within-described
            # relationships, assign a type.
            # TODO - vobj.partition_offset entails that a
            # PartitionObject exists.  This is something that may need
            # to be adjusted in the schema.
            _n_container: URIRef
            if container_image_trace is None:
                _n_container = ns_kb["ObservableObject-" + local_uuid()]
                graph.add(
                    (_n_container, NS_RDF.type, NS_UCO_OBSERVABLE.ObservableObject)
                )
                graph.add(
                    (
                        _n_container,
                        NS_RDFS.comment,
                        Literal(
                            "This object was created as a placeholder for a file system object that described itself as having a location-offset from its most-directly-containing storage medium, but without having a recorded reference to the storage medium object."
                        ),
                    )
                )
            else:
                _n_container = container_image_trace

            n_relationship = ns_kb["Relationship-" + local_uuid()]
            graph.add(
                (
                    n_relationship,
                    NS_RDF.type,
                    NS_UCO_OBSERVABLE.ObservableRelationship,
                )
            )
            graph.add(
                (
                    n_relationship,
                    NS_RDF.type,
                    NS_DRAFTING.StorageMediumRange,
                )
            )
            _inline_storage_medium_range_definition(graph)
            graph.add((n_relationship, NS_UCO_CORE.isDirectional, Literal(True)))
            graph.add(
                (
                    n_relationship,
                    NS_UCO_CORE.kindOfRelationship,
                    Literal("Contained_Within"),
                )
            )
            graph.add((n_relationship, NS_UCO_CORE.source, n_volume))
            graph.add((n_relationship, NS_UCO_CORE.target, _n_container))
            # _logger.debug("Container: %r." % _n_container)
            # _logger.debug("Containee: %r." % n_file_system)
            if use_inherent_uuids:
                n_data_range_facet = get_facet_uriref(
                    n_relationship, NS_UCO_OBSERVABLE.DataRangeFacet, namespace=ns_kb
                )
            else:
                n_data_range_facet = ns_kb["DataRangeFacet-" + local_uuid()]
            graph.add(
                (n_data_range_facet, NS_RDF.type, NS_UCO_OBSERVABLE.DataRangeFacet)
            )
            graph.add(
                (
                    n_data_range_facet,
                    NS_UCO_OBSERVABLE.rangeOffset,
                    Literal(vobj.partition_offset),
                )
            )
            graph.add((n_relationship, NS_UCO_CORE.hasFacet, n_data_range_facet))

    return n_volume


def main() -> None:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-d", "--debug", action="store_true")
    argument_parser.add_argument(
        "--kb-prefix-label",
        default="kb",
        help="Prefix label to use for knowledge-base individuals.  E.g. with defaults, 'http://example.org/kb/Thing-1' would compact to 'kb:Thing-1'.",
    )
    argument_parser.add_argument(
        "--kb-prefix-iri",
        default="http://example.org/kb/",
        help="Prefix IRI to use for knowledge-base individuals.  E.g. with defaults, 'http://example.org/kb/Thing-1' would compact to 'kb:Thing-1'.",
    )
    argument_parser.add_argument(
        "--output-format", help="Override extension-based format guesser."
    )
    argument_parser.add_argument("--use-inherent-uuids", action="store_true")
    argument_parser.add_argument("in_dfxml")
    argument_parser.add_argument(
        "out_graph",
        help="A self-contained RDF graph file, in the format either requested by --output-format or guessed based on extension.",
    )
    args = argument_parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    # See cdo_local_uuid._demo_uuid for how to use this to set up
    # a process call that opts in to nonrandom UUIDs.  Opting in is
    # beneficial for generating and version-controlling example runs of
    # this tool, but might not be appropriate for production operation.
    cdo_local_uuid.configure()

    # Define Namespace object to assist with generating individual nodes.
    ns_kb = Namespace(args.kb_prefix_iri)

    graph = Graph()
    graph.bind("drafting", NS_DRAFTING)
    graph.bind("owl", NS_OWL)
    graph.bind("rdfs", NS_RDFS)
    graph.bind("uco-core", NS_UCO_CORE)
    graph.bind("uco-observable", NS_UCO_OBSERVABLE)
    graph.bind("uco-types", NS_UCO_TYPES)

    # Bind various prefixes to prefix-IRIs in the output graph.
    # At the time of this writing, this compacts Turtle data, but does
    # not induce a JSON-LD Context Dictionary.
    graph.bind(args.kb_prefix_label, ns_kb)

    # This binding should be kept, because various RDF frameworks
    # disagree on whether "xs:" or "xsd:" should be the prefix, and
    # conflicting usage can lead to confusion or data errors when
    # multiple tools contribute to the same graph.
    graph.namespace_manager.bind("xsd", NS_XSD)

    trace_image_stack: List[URIRef] = []
    trace_object_stack: List[URIRef] = []
    for event, obj in Objects.iterparse(args.in_dfxml):
        container_image_trace = (
            None if len(trace_image_stack) == 0 else trace_image_stack[-1]
        )
        parent_trace = None if len(trace_object_stack) == 0 else trace_object_stack[-1]
        if event == "start":
            if isinstance(obj, Objects.DiskImageObject):
                # TODO This logic implements a stub to handle volume.partition_offset.
                trace = ns_kb["Image-" + local_uuid()]
                trace_image_stack.append(trace)
                trace_object_stack.append(trace)
            elif isinstance(obj, Objects.VolumeObject):
                trace = volumeobject_to_trace(
                    graph,
                    ns_kb,
                    obj,
                    container_image_trace=container_image_trace,
                    use_inherent_uuids=args.use_inherent_uuids,
                )
                trace_object_stack.append(trace)
        elif event == "end":
            if isinstance(obj, Objects.DiskImageObject):
                trace_image_stack.pop()
                trace_object_stack.pop()
            elif isinstance(obj, Objects.VolumeObject):
                trace_object_stack.pop()
            elif isinstance(obj, Objects.FileObject):
                trace = fileobject_to_trace(
                    graph,
                    ns_kb,
                    obj,
                    parent_trace=parent_trace,
                    use_inherent_uuids=args.use_inherent_uuids,
                )

    # Write output file.
    output_format = (
        guess_format(args.out_graph)
        if args.output_format is None
        else args.output_format
    )
    graph.serialize(destination=args.out_graph, format=output_format)


if __name__ == "__main__":
    main()
