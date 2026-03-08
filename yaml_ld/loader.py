from typing import Iterator

from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor


class _CoreSchemaConstructor(SafeConstructor):
    """SafeConstructor without timestamp resolution (YAML Core Schema compliance).

    The Core Schema (YAML 1.2.2 §10.3) does not include timestamp recognition.
    Date-like strings such as 2024-01-15 must remain plain strings.
    """


_CoreSchemaConstructor.add_constructor(
    'tag:yaml.org,2002:timestamp',
    SafeConstructor.construct_yaml_str,
)

_safe_yaml = YAML(typ='safe')
_safe_yaml.Constructor = _CoreSchemaConstructor


def load_all(stream: str | object) -> Iterator[object]:
    """Load all YAML documents from stream. YAML 1.2.2 compliant."""
    return _safe_yaml.load_all(stream)
