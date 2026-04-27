from typing import Iterator

from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor
from ruamel.yaml.nodes import MappingNode, ScalarNode, SequenceNode


class _CoreSchemaConstructor(SafeConstructor):
    """SafeConstructor without timestamp resolution (YAML Core Schema compliance).

    The Core Schema (YAML 1.2.2 §10.3) does not include timestamp recognition.
    Date-like strings such as 2024-01-15 must remain plain strings.
    """


def _make_yaml_loader() -> YAML:
    yaml = YAML(typ='safe')
    yaml.Constructor = _CoreSchemaConstructor
    return yaml


def _construct_unknown_tag(
    constructor: _CoreSchemaConstructor,
    _tag_suffix: str,
    node,
):
    """Ignore non-core YAML tags when extended YAML processing is disabled."""
    if isinstance(node, ScalarNode):
        return _make_yaml_loader().load(node.value)

    if isinstance(node, SequenceNode):
        return constructor.construct_sequence(node)

    if isinstance(node, MappingNode):
        return constructor.construct_mapping(node)

    return constructor.construct_object(node)


_CoreSchemaConstructor.add_constructor(
    'tag:yaml.org,2002:timestamp',
    SafeConstructor.construct_yaml_str,
)

_CoreSchemaConstructor.add_multi_constructor('', _construct_unknown_tag)
_safe_yaml = _make_yaml_loader()


def load_all(stream: str | object) -> Iterator[object]:
    """Load all YAML documents from stream. YAML 1.2.2 compliant."""
    return _safe_yaml.load_all(stream)
