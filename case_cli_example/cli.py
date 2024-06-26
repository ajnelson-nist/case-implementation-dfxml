#!/usr/bin/env python3

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

# TODO - Adapt below.

import argparse
import logging

import cdo_local_uuid
from case_utils.namespace import NS_RDF, NS_UCO_CORE, NS_UCO_IDENTITY, NS_XSD
from cdo_local_uuid import local_uuid
from rdflib import Graph, Literal, Namespace
from rdflib.util import guess_format


def main() -> None:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--kb-prefix",
        default="kb",
        help="Prefix label to use for knowledge-base individuals.  E.g. with defaults, 'http://example.org/kb/Thing-1' would compact to 'kb:Thing-1'.",
    )
    argument_parser.add_argument(
        "--kb-prefix-iri",
        default="http://example.org/kb/",
        help="Prefix IRI to use for knowledge-base individuals.  E.g. with defaults, 'http://example.org/kb/Thing-1' would compact to 'kb:Thing-1'.",
    )
    argument_parser.add_argument("--debug", action="store_true")
    argument_parser.add_argument(
        "--output-format", help="Override extension-based format guesser."
    )
    # The output graph is suggested as the first positional argument to
    # allow for an arbitrary number of input files as the command's end.
    argument_parser.add_argument(
        "out_graph",
        help="A self-contained RDF graph file, in the format either requested by --output-format or guessed based on extension.",
    )
    argument_parser.add_argument("in_file", nargs="*", help="One or more input files.")

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

    # Bind various prefixes to prefix-IRIs in the output graph.
    # At the time of this writing, this compacts Turtle data, but does
    # not induce a JSON-LD Context Dictionary.
    graph.namespace_manager.bind(args.kb_prefix, ns_kb)
    graph.namespace_manager.bind("uco-core", NS_UCO_CORE)
    graph.namespace_manager.bind("uco-identity", NS_UCO_IDENTITY)

    # This binding should be kept, because various RDF frameworks
    # disagree on whether "xs:" or "xsd:" should be the prefix, and
    # conflicting usage can lead to confusion or data errors when
    # multiple tools contribute to the same graph.
    graph.namespace_manager.bind("xsd", NS_XSD)

    # Generate an example object.
    n_example_organization = ns_kb["Organization-" + local_uuid()]
    graph.add((n_example_organization, NS_RDF.type, NS_UCO_IDENTITY.Organization))
    graph.add(
        (n_example_organization, NS_UCO_CORE.name, Literal("Cyber Domain Ontology"))
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
