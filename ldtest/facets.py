from pathlib import Path
from typing import Iterable

from iolanta.facets.facet import Facet
from rdflib import Namespace, URIRef, Literal
from urlpath import URL

from ldtest.models import TestCase
from rdflib_yaml_ld.errors import MappingKeyError

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

        return {
            'mapping-key-error': MappingKeyError,
            'loading document failed': ...,
            'invalid encoding': ...,
        }[result.value]
