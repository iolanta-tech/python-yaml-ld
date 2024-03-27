import pytest
import yaml

import yaml_ld
from tests.common import specifications_root, tests_root
from yaml_ld.errors import LoadingDocumentFailed


def test_invalid_yaml():
    document = specifications_root / (
        'yaml-ld/tests/cases/cr-well-formed-2-negative-in.yamlld'
    )
    with pytest.raises(LoadingDocumentFailed):
        yaml_ld.parse(document)


def test_closing_html_comment_in_yaml():
    """This document ends with `-->`, not a valid piece of YAML."""
    with pytest.raises(Exception):
        yaml.parse(tests_root / 'data/tr016.yaml', Loader=yaml.Loader)
