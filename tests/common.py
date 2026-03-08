from pathlib import Path
from typing import Iterable

from rdflib import ConjunctiveGraph, URIRef

from ldtest.models import TestCase, SPECIFICATIONS_ROOT
from ldtest.plugin import LDTest

from iolanta.iolanta import Iolanta

tests_root = Path(__file__).parent
project_root = tests_root.parent

PYTEST = URIRef('https://pytest.org')


def _manifest_paths() -> list[Path]:
    """Paths to manifest files to load."""
    return list(SPECIFICATIONS_ROOT.glob("**/tests/*manifest.jsonld"))


def iolanta() -> Iolanta:
    graph = ConjunctiveGraph()
    for manifest_path in _manifest_paths():
        graph.parse(manifest_path)

    return Iolanta(
        graph=graph,
        project_root=project_root / 'ldtest' / 'data',
        force_plugins=[LDTest],
    )


def load_tests(test_class: URIRef) -> Iterable[TestCase]:
    return iolanta().render(
        node=test_class,
        as_datatype=PYTEST,
    )
