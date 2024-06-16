import json
from pathlib import Path

import pytest
from pyld import jsonld
from pyld.jsonld import JsonLdError

import yaml_ld
from tests.common import specifications_root


def test_pyld_expand_json_string():
    """
    pyld does not accept a string serialization of a JSON document to expand.

    We shall do the same.
    """
    document = {
        '@context': {'@vocab': 'https://example.com'},
        'something': None,
    }

    with pytest.raises(JsonLdError) as error_info:
        jsonld.expand(json.dumps(document))

    assert error_info.value.type == 'jsonld.InvalidUrl'


def test_empty_value():
    """
    None as value is removing the key from the document.

    This is confirmed at JSON-LD Playground.
    """
    document = {
        '@context': {'@vocab': 'https://example.com'},
        'something': None,
    }

    assert not yaml_ld.expand(document)


def test_local_context():
    document = specifications_root / 'json-ld-api/tests/expand/0127-in.jsonld'
    yaml_ld.expand(document)


def test_api_html_e016():
    source = specifications_root / 'json-ld-api/tests/html/e016-in.html'
    jsonld.expand(source)
