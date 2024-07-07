from pathlib import Path

import more_itertools
import pytest
import yaml
from yaml.parser import ParserError
from yarl import URL

from tests.common import tests_root
from yaml_ld.string_as_url_or_path import as_url_or_path


def test_closing_html_comment_in_yaml():
    """This document ends with `-->`, not a valid piece of YAML."""
    source_path = tests_root / 'data/tr016.yaml'

    with pytest.raises(ParserError):
        more_itertools.consume(
            yaml.load_all(
                source_path.read_text(),
                Loader=yaml.SafeLoader,
            ),
        )


@pytest.mark.parametrize(
    ('given', 'expected'),
    [
        (raw := 'http://schema.org', URL(raw)),
        (raw := 'https://schema.org', URL(raw)),
        (raw := 'ipns://iolanta.tech', URL(raw)),
        (raw := 'ipfs://iolanta.tech', URL(raw)),
        (raw := '/home/iolanta/', Path(raw)),
        (raw := '/home/iolanta/test.jsonld', Path(raw)),
        (raw := '/home/iolanta/test.yamlld', Path(raw)),
        (raw := 'test.yamlld', Path(raw)),
    ],
)
def test_string_as_url_or_path(given: str, expected: URL):
    assert as_url_or_path(given) == expected
