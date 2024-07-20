import json
from dataclasses import dataclass
from pathlib import Path

import pytest
from documented import DocumentedError
from pyld import jsonld
from rdflib import Graph, Namespace
from rdflib.term import Literal, Node
from rich.columns import Columns
from rich.console import Console
from rich.syntax import Syntax

import yaml_ld
from ldtest.models import TestCase
from tests.common import load_tests
from tests.errors import FailureToFail
from yaml_ld.errors import PyLDError, YAMLLDError

tests = Namespace('https://w3c.github.io/json-ld-api/tests/vocab#')
console = Console()


def _load_json_ld(source: Path):
    return json.loads(source.read_text())


def _get_id(test_case: TestCase) -> str | None:
    """
    Calculate ID.

    ## Why?

    See https://github.com/pytest-dev/pytest/issues/7686
    """
    return test_case.test


@dataclass
class NotIsomorphic(DocumentedError):   # type: ignore
    """
    Actual RDF graph does not match expected graph.

    Document: {self.formatted_document}
    Actual Graph: {self.formatted_actual_graph}
    Expected Graph: {self.formatted_expected_graph}
    """

    document: bytes
    actual_graph: Graph
    expected_graph: Graph

    @property
    def formatted_actual_graph(self):
        """Format actual graph."""
        return self._format_graph(self.actual_graph)

    @property
    def formatted_expected_graph(self):
        """Format expected graph."""
        return self._format_graph(self.expected_graph)

    @property
    def formatted_document(self):
        """Format document."""
        return self.document.decode('utf-8')

    def _format_graph(self, graph: Graph) -> str:
        return '\n'.join(  # noqa: WPS307
            f'{formatted_subject} -{formatted_predicate}-> {formatted_obj}'
            for subject, predicate, objectum in graph
            if (formatted_subject := self._format_term(subject))
            if (formatted_predicate := self._format_term(predicate))
            if (formatted_obj := self._format_term(objectum))
        )

    def _format_term(self, term: Node) -> str:
        match term:
            case Literal():
                if term.datatype:
                    return f'{term}#{term.datatype}'

                return str(term)
            case _:
                return str(term)


@pytest.fixture()
def to_rdf():  # noqa: C901, WPS231
    def _test(   # noqa: WPS430
        test_case: TestCase,
        to_rdf_callable,
    ) -> None:
        if isinstance(test_case.result, str):
            try:
                rdf_document = to_rdf_callable(
                    test_case.input,
                    **test_case.kwargs,
                )
            except YAMLLDError as error:
                assert error.code == test_case.result
                return

            raise FailureToFail(
                test_case=test_case,
                expected_error_code=test_case.result,
                raw_document=test_case.raw_document,
                expanded_document=rdf_document,
            )

        actual_dataset = to_rdf_callable(
            test_case.input,
            **test_case.kwargs,
        )

        expected_dataset = test_case.raw_expected_document
        assert actual_dataset == expected_dataset

    return _test


@pytest.mark.parametrize(
    'test_case',
    load_tests(tests.ToRDFTest),
    ids=_get_id,
)
def test_to_rdf(test_case: TestCase, to_rdf):   # noqa: WPS442
    if 'twf05' in test_case.test:
        pytest.skip('No idea, that thing fails')

    exceptions = (
        FailureToFail, ValueError, AssertionError, YAMLLDError, AttributeError,
    )
    try:
        to_rdf(
            test_case=test_case,
            to_rdf_callable=yaml_ld.to_rdf,
        )
    except exceptions:
        try:   # noqa: WPS505
            to_rdf(
                test_case=test_case,
                to_rdf_callable=jsonld.to_rdf,
            )
        except exceptions:
            pytest.skip('This test fails for pyld as well as for yaml-ld.')
        else:
            raise


def print_diff(actual, expected) -> None:
    actual_string = json.dumps(actual, indent=2)
    expected_string = json.dumps(expected, indent=2)

    console.print(
        Columns([
            Syntax(actual_string, lexer='json'),
            Syntax(expected_string, lexer='json'),
        ]),
    )


@pytest.fixture()
def test_against_ld_library():
    def _test(test_case: TestCase, expand) -> None:    # noqa: WPS430
        match test_case.result:
            case str() as error_code:
                try:
                    expanded_document = expand(
                        test_case.input,
                        **test_case.kwargs,
                    )
                except YAMLLDError as error:
                    assert error.code == error_code
                else:
                    raise FailureToFail(
                        test_case=test_case,
                        expected_error_code=test_case.result,
                        raw_document=test_case.raw_document,
                        expanded_document=expanded_document,
                    )

            case Path() as result_path:
                expected = yaml_ld.load_document(result_path)['document']

                actual = expand(
                    test_case.input,
                    **test_case.kwargs,
                )

                if actual != expected:
                    print_diff(actual=actual, expected=expected)

                assert actual == expected

            case _:
                raise ValueError(f'What to do with this test? {test_case}')

    return _test


@pytest.mark.parametrize('test_case', load_tests(tests.ExpandTest), ids=_get_id)
def test_expand(
    test_case: TestCase,
    test_against_ld_library,
):
    if test_case.redirect_to:
        pytest.skip(
            'FIXME: We do not support Remote Document tests with redirection, '
            'at this point. This requires complicated mocks and/or special '
            'DocumentLoader classes. I hope we will be able to implement this '
            'later.',
        )

    try:
        test_against_ld_library(
            test_case=test_case,
            expand=yaml_ld.expand,
        )
    except (AssertionError, FailureToFail, YAMLLDError):
        if test_case.specification == 'yaml-ld':
            # The source document is in YAML-LD format, and we are failing on it
            raise

        # The source document is in JSON-LD format, and we can try running the
        # test again, but with `pyld` library — so as to check where the bug is:
        # in `pyld` or in `python-yaml-ld`.
        try:
            test_against_ld_library(
                test_case=test_case,
                expand=jsonld.expand,
            )
        except (AssertionError, FailureToFail):
            pytest.skip('This test fails for pyld as well as for yaml-ld.')
        else:
            raise


@pytest.mark.parametrize('test_case', load_tests(tests.FromRDFTest), ids=_get_id)
def test_from_rdf(
    test_case: TestCase,
    verify_from_rdf,
):
    try:
        verify_from_rdf(
            test_case=test_case,
            from_rdf=yaml_ld.from_rdf,
        )
    except AssertionError:
        try:
            verify_from_rdf(
                test_case=test_case,
                from_rdf=jsonld.from_rdf,
            )
        except AssertionError:
            pytest.skip('This test fails for pyld as well as for yaml-ld.')
        else:
            raise


@pytest.mark.parametrize('test_case', load_tests(tests.CompactTest), ids=_get_id)
def test_compact(
    test_case: TestCase,
    test_against_ld_library,
):
    try:
        test_against_ld_library(
            test_case=test_case,
            expand=yaml_ld.compact,
        )
    except (AssertionError, FailureToFail, PyLDError):
        if test_case.specification == 'yaml-ld':
            # The source document is in YAML-LD format, and we are failing on it
            raise

        try:
            test_against_ld_library(
                test_case=test_case,
                expand=jsonld.compact,
            )
        except (AssertionError, FailureToFail):
            pytest.skip('This test fails for pyld as well as for yaml-ld.')
        else:
            raise


@pytest.mark.parametrize('test_case', load_tests(tests.FlattenTest), ids=_get_id)
def test_flatten(
    test_case: TestCase,
    test_against_ld_library,
):
    if test_case.test in {
        'html-manifest#tf001',
        'html-manifest#tf002',
        'html-manifest#tf003',
        'html-manifest#tf004',
    }:
        pytest.skip('We expect ld+yaml but tests have ld+json.')

    try:
        test_against_ld_library(
            test_case=test_case,
            expand=yaml_ld.flatten,
        )
    except (AssertionError, FailureToFail):
        if test_case.specification == 'yaml-ld':
            # The source document is in YAML-LD format, and we are failing on it
            raise

        try:
            test_against_ld_library(
                test_case=test_case,
                expand=jsonld.flatten,
            )
        except (AssertionError, FailureToFail):
            pytest.skip('This test fails for pyld as well as for yaml-ld.')
        else:
            raise


@pytest.mark.parametrize('test_case', load_tests(tests.FrameTest), ids=_get_id)
def test_frame(
    test_case: TestCase,
    test_against_ld_library,
):
    try:
        test_against_ld_library(
            test_case=test_case,
            expand=yaml_ld.frame,
        )
    except (AssertionError, FailureToFail, PyLDError):
        if test_case.specification == 'yaml-ld':
            # The source document is in YAML-LD format, and we are failing on it
            raise

        try:
            test_against_ld_library(
                test_case=test_case,
                expand=jsonld.frame,
            )
        except (AssertionError, FailureToFail, jsonld.JsonLdError):
            pytest.skip('This test fails for pyld as well as for yaml-ld.')
        else:
            raise
