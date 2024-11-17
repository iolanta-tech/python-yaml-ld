import json

import pytest
from dirty_equals import IsList, IsPartialDict
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


def test_https():
    response = yaml_ld.expand(
        'https://json-ld.github.io/yaml-ld/tests/manifest.jsonld',
    )

    assert response == [
        IsPartialDict({
            '@id': 'https://json-ld.github.io/yaml-ld/tests/basic-manifest',
        }),
    ]


def test_expand_iolanta_index():
    assert yaml_ld.expand(
        {
            '@context': {
                '@import': (
                    'https://json-ld.org/contexts/dollar-convenience.jsonld'
                ),
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'iolanta': 'https://iolanta.tech/',
                '@base': 'https://iolanta.tech/visualizations/',
                '→': {'@id': 'iolanta:visualized-with', '@type': '@id'},
            },
            '$id': 'https://iolanta.tech/visualizations/index.yaml',
            'rdfs:label': 'Iolanta visualizations index 1.0',
            '$included': [
                {'$id': 'rdfs:', '→': 'rdfs.yaml'},
                {
                    '$id': 'http://xmlns.com/foaf/0.1/',
                    '→': 'foaf.yaml',
                },
            ],
        },
    )
