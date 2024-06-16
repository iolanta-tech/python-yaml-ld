import json
from typing import Callable

import pytest
from pydantic import ValidationError

from ldtest.models import TestCase
from tests.errors import FailureToFail
from yaml_ld.errors import YAMLLDError


@pytest.fixture()
def verify_from_rdf():
    def _test(
        test_case: TestCase,
        from_rdf: Callable,
    ) -> None:
        if isinstance(test_case.result, str):
            try:
                rdf_document = from_rdf(
                    test_case.raw_document.decode(),
                    **test_case.kwargs,
                )
            except YAMLLDError as error:
                assert error.code == test_case.result
                return

            else:
                raise FailureToFail(
                    test_case=test_case,
                    expected_error_code=test_case.result,
                    raw_document=test_case.raw_document,
                    expanded_document=rdf_document,
                )

        try:
            actual_ld = from_rdf(
                test_case.raw_document.decode(),
                **test_case.kwargs,
            )
        except ValidationError:
            raise ValueError(
                f'{test_case.raw_document!r} has type '
                f'{type(test_case.raw_document)}, that is not what {from_rdf} '
                'expects.',
            )

        expected_ld = json.loads(test_case.raw_expected_document)

        assert actual_ld == expected_ld

    return _test
