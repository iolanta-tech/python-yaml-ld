import json

import yaml_ld


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
