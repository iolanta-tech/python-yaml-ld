import functools
from pathlib import Path
from typing import Iterable

import funcy
from iolanta.iolanta import Iolanta
from iolanta.namespaces import LOCAL
from rdflib import ConjunctiveGraph, URIRef

from ldtest.models import TestCase
from ldtest.plugin import LDTest


@functools.lru_cache
def iolanta() -> Iolanta:
    # Load the JSON-LD tests from the test suite
    # Return a list of test cases
    project_root = Path(__file__).parent.parent
    specifications_root = project_root / 'specifications'

    graph = ConjunctiveGraph()
    for manifest_path in specifications_root.glob('*/tests/*manifest.jsonld'):
        # FIXME: Use `iolanta.add()`.
        #   At this point, we can't do that: `iolanta` does not resolve the
        #   `context.jsonld` file which this document is referring to.
        graph.parse(manifest_path)

    return Iolanta(graph=graph, force_plugins=[LDTest])


def load_tests(test_class: URIRef) -> Iterable[TestCase]:
    return funcy.first(
        iolanta().render(
            node=test_class,
            environments=[LOCAL.pytest],
        ),
    )
