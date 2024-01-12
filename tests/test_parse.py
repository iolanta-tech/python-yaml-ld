import yaml_ld
from tests.common import specifications_root


def test_invalid_yaml():
    document = specifications_root / (
        'yaml-ld/tests/cases/cr-well-formed-2-negative-in.yamlld'
    )
    assert yaml_ld.parse(document)
