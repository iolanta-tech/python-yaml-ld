import functools
import json
import operator
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import funcy
import pytest
from documented import Documented
from iolanta.iolanta import Iolanta
from iolanta.namespaces import LOCAL
from rdflib import ConjunctiveGraph, Namespace, URIRef

import yaml_ld
from ldtest.models import TestCase
from ldtest.plugin import LDTest
from yaml_ld.errors import YAMLLDError
from yaml_ld.models import Document

tests = Namespace('https://w3c.github.io/json-ld-api/tests/vocab#')


@dataclass
class FailureToFail(Documented):
    """
    YAMLLDError not raised.

    Expected error code: {self.expected_error_code}
    Raw input document: {self.formatted_raw_document}
    Expanded document: {self.formatted_expanded_document}
    """

    expected_error_code: str
    raw_document: bytes
    expanded_document: Document

    @property
    def formatted_raw_document(self) -> str:
        """Present the raw document."""
        return self.raw_document.decode()

    @property
    def formatted_expanded_document(self) -> str:
        """JSON prettify expanded document for display."""
        return json.dumps(self.expanded_document, indent=2)


@functools.lru_cache
def iolanta() -> Iolanta:
    # Load the JSON-LD tests from the test suite
    # Return a list of test cases
    project_root = Path(__file__).parent.parent
    tests_root = project_root / 'specification/tests'
    manifest_path = tests_root / 'basic-manifest.jsonld'
    manifest_path = tests_root / 'extended-manifest.jsonld'

    # FIXME: Use `iolanta.add()`.
    #   At this point, we can't do that: `iolanta` does not resolve the
    #   `context.jsonld` file.
    graph = ConjunctiveGraph()
    graph.parse(manifest_path)
    return Iolanta(graph=graph, force_plugins=[LDTest])


def load_tests(test_class: URIRef) -> Iterable[TestCase]:
    return funcy.first(
        iolanta().render(
            node=test_class,
            environments=[LOCAL.pytest],
        ),
    )


@pytest.mark.parametrize(
    "test_case",
    load_tests(tests.PositiveEvaluationTest),
    ids=operator.attrgetter('test'),
)
def test_positive(test_case: TestCase):
    if test_case.test == 'cir-scalar-other-1-positive':
        pytest.skip(
            'When parsing the …out.yamlld file, the floating point value of '
            '123.456e78 is interpreted as string. This is due to the fact that '
            'PyYAML supports only YAML 1.1, which requires a sign to precede '
            'mantissa of a number in exponential notation. YAML 1.2 lifts that '
            'requirement. There is an open PR to resolve the issue: '
            'https://github.com/yaml/pyyaml/pull/555 which is currently being '
            'promised to be merged in November 2023. We shall see.',
        )

    if isinstance(test_case.result, str):
        raw_document = test_case.input.read_bytes()
        try:
            expanded_document = yaml_ld.expand(raw_document)
        except YAMLLDError as error:
            assert error.code == test_case.result
        else:
            pytest.fail(str(FailureToFail(
                expected_error_code=test_case.result,
                raw_document=raw_document,
                expanded_document=expanded_document,
            )))

    elif isinstance(test_case.result, Path):
        expected = yaml_ld.parse(test_case.result.read_text())
        actual = yaml_ld.expand(test_case.input.read_text())
        assert actual == expected
    else:
        raise ValueError(f'What to do with this test? {test_case}')


@pytest.mark.parametrize(
    "test_case",
    load_tests(tests.NegativeEvaluationTest),
    ids=operator.attrgetter('test'),
)
def test_negative(test_case: TestCase):
    if test_case.test == 'cir-scalar-other-1-positive':
        pytest.skip(
            'When parsing the …out.yamlld file, the floating point value of '
            '123.456e78 is interpreted as string. This is due to the fact that '
            'PyYAML supports only YAML 1.1, which requires a sign to precede '
            'mantissa of a number in exponential notation. YAML 1.2 lifts that '
            'requirement. There is an open PR to resolve the issue: '
            'https://github.com/yaml/pyyaml/pull/555 which is currently being '
            'promised to be merged in November 2023. We shall see.',
        )

    if isinstance(test_case.result, str):
        raw_document = test_case.input.read_bytes()
        try:
            expanded_document = yaml_ld.expand(raw_document)
        except YAMLLDError as error:
            assert error.code == test_case.result
        else:
            pytest.fail(str(FailureToFail(
                expected_error_code=test_case.result,
                raw_document=raw_document,
                expanded_document=expanded_document,
            )))

    elif isinstance(test_case.result, Path):
        expected = yaml_ld.parse(test_case.result.read_text())
        actual = yaml_ld.expand(test_case.input.read_text())
        assert actual == expected
    else:
        raise ValueError(f'What to do with this test? {test_case}')
