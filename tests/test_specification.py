import json
import operator
from pathlib import Path
from typing import Callable

import pytest
from pyld import jsonld
from rdflib import Graph, Namespace
from rdflib_pyld_compat.convert import (  # noqa: WPS450
    _rdflib_graph_from_pyld_dataset,
)

import yaml_ld
from ldtest.models import TestCase
from tests.common import load_tests
from tests.errors import FailureToFail
from yaml_ld.errors import YAMLLDError
from lambdas import _

from yaml_ld.expand import ExpandOptions

tests = Namespace('https://w3c.github.io/json-ld-api/tests/vocab#')


def _get_id(test_case: TestCase) -> str | None:
    """
    Calculate ID.

    ## Why?

    See https://github.com/pytest-dev/pytest/issues/7686
    """
    if not isinstance(test_case, TestCase):
        return None

    return test_case.test


@pytest.mark.parametrize(
    'test_case',
    load_tests(tests.ToRDFTest),
    ids=_get_id,
)
def test_to_rdf(test_case: TestCase):
    if isinstance(test_case.result, str):
        try:
            rdf_document = yaml_ld.to_rdf(
                test_case.input,
                extract_all_scripts=test_case.extract_all_scripts,
            )
        except YAMLLDError as error:
            assert error.code == test_case.result
            return

        else:
            pytest.fail(str(FailureToFail(
                test_case=test_case,
                expected_error_code=test_case.result,
                raw_document=test_case.raw_document,
                expanded_document=rdf_document,
            )))

    actual_dataset = yaml_ld.to_rdf(test_case.raw_document)
    raw_expected_quads = test_case.raw_expected_document

    actual_triples = actual_dataset['@default']
    actual_graph: Graph = _rdflib_graph_from_pyld_dataset(actual_triples)
    expected_graph = Graph().parse(data=raw_expected_quads)

    assert actual_graph.isomorphic(expected_graph)


@pytest.fixture()
def test_against_ld_library():
    def _test(test_case: TestCase, parse: Callable, expand: Callable) -> None:
        match test_case.result:
            case str() as error_code:
                try:
                    expanded_document = expand(
                        test_case.input,
                        options=ExpandOptions(
                            extract_all_scripts=test_case.extract_all_scripts,
                        ).model_dump(by_alias=True),
                    )
                except YAMLLDError as error:
                    assert error.code == error_code
                else:
                    pytest.fail(str(FailureToFail(
                        test_case=test_case,
                        expected_error_code=test_case.result,
                        raw_document=test_case.raw_document,
                        expanded_document=expanded_document,
                    )))

            case Path() as result_path:
                expected = parse(result_path.read_text())
                actual = expand(
                    test_case.input,
                    options=ExpandOptions(
                        extract_all_scripts=test_case.extract_all_scripts,
                        base=test_case.base,
                    ).model_dump(by_alias=True),
                )

                assert actual == expected

            case _:
                raise ValueError(f'What to do with this test? {test_case}')

    return _test


@pytest.mark.parametrize('test_case', load_tests(tests.ExpandTest), ids=_get_id)
def test_expand(
    test_case: TestCase,
    test_against_ld_library,
):
    try:
        test_against_ld_library(
            test_case=test_case,
            parse=yaml_ld.parse,
            expand=yaml_ld.expand,
        )
    except Exception:
        try:
            test_against_ld_library(
                test_case=test_case,
                parse=json.loads,
                expand=jsonld.expand,
            )
        except Exception:
            pytest.skip('This test fails for pyld as well as for yaml-ld.')
        else:
            raise
