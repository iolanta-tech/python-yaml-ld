import operator
from pathlib import Path

import pytest
from rdflib import Namespace

import yaml_ld
from ldtest.models import TestCase
from tests.common import load_tests
from tests.errors import FailureToFail
from yaml_ld.errors import YAMLLDError

tests = Namespace('https://w3c.github.io/json-ld-api/tests/vocab#')


@pytest.mark.parametrize(
    "test_case",
    load_tests(tests.ExpandTest),
    ids=operator.attrgetter('test'),
)
def test_expand(test_case: TestCase):
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
