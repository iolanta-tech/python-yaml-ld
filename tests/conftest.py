import json
import os

import pytest
from pydantic import ValidationError
from rdflib import FOAF
from yarl import URL

import yaml_ld
from ldtest.models import TestCase
from tests.errors import FailureToFail
from yaml_ld.errors import YAMLLDError

URLS = (
    URL('https://prefix.cc/context.jsonld'),
    URL('https://schema.org'),
    URL('https://schema.org/Person'),
    URL('https://dbpedia.org/data/Arthur_C._Clarke.json'),
    URL('https://dbpedia.org/data/Arthur_C._Clarke.jsonld'),
    URL('https://dbpedia.org/resource/Arthur_C._Clarke'),
    URL('https://www.wikidata.org/wiki/Special:EntityData/Q42.jsonld'),
    URL('https://id.loc.gov/authorities/names/n79081644.jsonld'),
    URL(str(FOAF)),
)


def _url_to_id(url: URL) -> str:
    return str(url.with_scheme('')).lstrip('/')


@pytest.fixture(params=URLS, ids=_url_to_id)
def url(request) -> URL:
    if os.environ.get('CI'):
        pytest.skip('This test is long and unreliable, skipping it in CI.')

    document = yaml_ld.load_document(request.param)
    assert document
    return request.param


@pytest.fixture()
def verify_from_rdf():   # noqa: C901, WPS231
    def _test(   # noqa: WPS430
        test_case: TestCase,
        from_rdf,
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

        assert actual_ld == expected_ld, (test_case.input, test_case.result)

    return _test
