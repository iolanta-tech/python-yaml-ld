import pytest

import yaml_ld
from tests.common import specifications_root
from yaml_ld.errors import LoadingDocumentFailed


def test_invalid_yaml():
    document = specifications_root / (
        'yaml-ld/tests/cases/cr-well-formed-2-negative-in.yamlld'
    )
    with pytest.raises(LoadingDocumentFailed):
        yaml_ld.parse(document)
