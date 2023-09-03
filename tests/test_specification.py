import operator
from pathlib import Path
from typing import Iterable

import funcy
import pytest
from iolanta.iolanta import Iolanta
from iolanta.namespaces import LOCAL
from rdflib import Graph, ConjunctiveGraph, Namespace

import yaml_ld
from ldtest.models import TestCase
from yaml_ld.errors import YAMLLDError

tests = Namespace('https://w3c.github.io/json-ld-api/tests/vocab#')


def load_tests() -> Iterable[TestCase]:
    # Load the JSON-LD tests from the test suite
    # Return a list of test cases
    manifest_path = Path(__file__).parent.parent / 'specification/tests/basic-manifest.jsonld'

    # FIXME: Use `iolanta.add()`.
    #   At this point, we can't do that: `iolanta` does not resolve the
    #   `context.jsonld` file.
    graph = ConjunctiveGraph()
    graph.parse(manifest_path)
    iolanta = Iolanta(graph=graph)

    iolanta.add({
        '$id': tests.ExpandTest,
        'iolanta:facet': {
            '$id': 'python://ldtest.JSONLDTests',
            'iolanta:supports': LOCAL.test,
        },
        'iolanta:hasInstanceFacet': {
            '$id': 'python://ldtest.JSONLDTest',
            'iolanta:supports': LOCAL.test,
        },
    })

    return funcy.first(
        iolanta.render(
            node=tests.ExpandTest,
            environments=[LOCAL.test],
        ),
    )


@pytest.mark.parametrize(
    "test_case",
    load_tests(),
    ids=operator.attrgetter('test'),
)
def test_spec(test_case: TestCase):
    if isinstance(test_case.result, Path) and test_case.result.suffix == '.yamlld':
        pytest.skip('Expansion test is not applicable.')

    if isinstance(test_case.result, str):
        with pytest.raises(YAMLLDError) as error_info:
            yaml_ld.expand(test_case.input.read_bytes())

        assert error_info.value.code == test_case.result

    else:
        raise ValueError(f'What to do with this test? {test_case}')
