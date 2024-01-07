import pytest
from pyld.jsonld import JsonLdError

import yaml_ld
from tests.common import specifications_root


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


@pytest.mark.xfail(
    raises=JsonLdError,
    reason='`pyld` does not handle `file://` paths.',
)
def test_local_context():
    document = specifications_root / 'json-ld-api/tests/expand/0127-in.jsonld'
    yaml_ld.expand(document)
