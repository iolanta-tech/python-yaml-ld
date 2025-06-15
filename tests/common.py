import functools
from pathlib import Path
from typing import Iterable

import funcy
from iolanta.iolanta import Iolanta
from iolanta.namespaces import LOCAL
from rdflib import ConjunctiveGraph, URIRef

from ldtest.models import TestCase
from ldtest.plugin import LDTest

tests_root = Path(__file__).parent
project_root = tests_root.parent
specifications_root = project_root / 'specifications'

PYTEST = URIRef('https://pytest.org')


def iolanta() -> Iolanta:
    # Load the JSON-LD tests from the test suite
    # Return a list of test cases
    graph = ConjunctiveGraph()
    for manifest_path in specifications_root.glob('*/tests/*manifest.jsonld'):
        # FIXME: Use `iolanta.add()`.
        graph.parse(manifest_path)

    return Iolanta(
        graph=graph,
        project_root=project_root / 'ldtest' / 'data',
        force_plugins=[LDTest],
    )


def load_tests(test_class: URIRef) -> Iterable[TestCase]:
    return iolanta().render(
        node=test_class,
        as_datatype=PYTEST,
    )
