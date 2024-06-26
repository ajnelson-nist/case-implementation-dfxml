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

from pathlib import Path
from typing import Set

import pytest
from case_utils.namespace import NS_RDF, NS_UCO_IDENTITY
from rdflib import Graph, URIRef
from rdflib.query import ResultRow


@pytest.mark.parametrize(
    ["filename"],
    [
        ("example_output.jsonld",),
        ("example_output.rdf",),
        ("example_output.ttl",),
        ("example_output_debug.jsonld",),
        ("example_output_debug.rdf",),
        ("example_output_debug.ttl",),
    ],
)
def test_example_output_with_iterator(filename: str) -> None:
    srcdir = Path(__file__).parent
    graph = Graph()
    graph.parse(srcdir / filename)
    n_organizations: Set[URIRef] = set()
    for n_subject in graph.subjects(NS_RDF.type, NS_UCO_IDENTITY.Organization):
        assert isinstance(n_subject, URIRef)
        n_organizations.add(n_subject)
    assert len(n_organizations) == 1


@pytest.mark.parametrize(
    ["filename"],
    [
        ("example_output.jsonld",),
        ("example_output.rdf",),
        ("example_output.ttl",),
        ("example_output_debug.jsonld",),
        ("example_output_debug.rdf",),
        ("example_output_debug.ttl",),
    ],
)
def test_example_output_with_sparql(filename: str) -> None:
    srcdir = Path(__file__).parent
    graph = Graph()
    graph.parse(srcdir / filename)

    # This query includes a prefix statement that is typically provided
    # by the data graph.  However, some graph generators omit prefixes
    # if they are never referenced in the triples.  In that case,
    # attempting to run this query without a PREFIX statement would fail
    # due to an unbound prefix.  While ultimately the test would be
    # correct in failing, it would fail for a potentially confusing
    # reason appearing to be a syntax error, rather than a real reason
    # of the query having no data to find.
    query = """\
PREFIX uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/>
SELECT ?nOrganization
WHERE {
  ?nOrganization
    a uco-identity:Organization ;
    .
}
"""
    n_organizations: Set[URIRef] = set()
    for result in graph.query(query):
        assert isinstance(result, ResultRow)
        assert isinstance(result[0], URIRef)
        n_organizations.add(result[0])
    assert len(n_organizations) == 1
