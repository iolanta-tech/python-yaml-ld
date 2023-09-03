from pathlib import Path
from typing import Iterable

from iolanta.facets.facet import Facet
from rdflib import Namespace, URIRef, Literal
from urlpath import URL

from ldtest.models import TestCase
from yaml_ld.errors import YAMLLDError

mf = Namespace('http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#')
tests = Namespace('https://w3c.github.io/json-ld-api/tests/vocab#')


class JSONLDTests(Facet[Iterable[TestCase]]):
    def show(self) -> Iterable[TestCase]:
        rows = self.stored_query('tests.sparql', test_class=self.iri)
        for row in rows:
            yield TestCase(
                test=URL(row['test']).fragment,
                input=Path(URL(row['input']).path),
                result=self._process_result(row['result']),
                req=row['req'].value,
            )

    def _process_result(self, result: URIRef | Literal) -> Path | str:
        if isinstance(result, URIRef):
            return Path(URL(result).path)

        return yaml_ld_error_class_by_code(result.value)


def yaml_ld_error_class_by_code(code: str) -> type[YAMLLDError]:
    classes = YAMLLDError.__subclasses__()

    for cls in classes:
        if cls.code == code:
            return cls

    raise ValueError(f'Unknown error message: {code}')
