import os
import types
from pathlib import Path
from typing import Iterable

from iolanta.facets.facet import Facet
from rdflib import Literal, Namespace, URIRef
from yarl import URL

import yaml_ld
from ldtest.models import TestCase, SPECIFICATIONS_ROOT

mf = Namespace('http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#')
tests = Namespace('https://w3c.github.io/json-ld-api/tests/vocab#')

# URL prefixes per spec name for rewriting to local paths when SPEC_PATH is set
SPEC_URL_PREFIXES = types.MappingProxyType({
    'yaml-ld': [
        'https://w3c.github.io/yaml-ld/tests/',
        'https://json-ld.github.io/yaml-ld/tests/',
    ],
    'json-ld-api': ['https://w3c.github.io/json-ld-api/tests/'],
    'json-ld-framing': ['https://w3c.github.io/json-ld-framing/tests/'],
    'rdf-canon': ['https://w3c.github.io/rdf-canon/tests/'],
})


def _url_to_local(url: URL) -> Path | None:
    """Rewrite URL to local path when SPEC_PATH is set and URL matches known prefix."""
    if "SPEC_PATH" not in os.environ:
        return None
    url_str = str(url)
    prefixes = SPEC_URL_PREFIXES.get(SPECIFICATIONS_ROOT.name, [])
    for prefix in prefixes:
        if url_str.startswith(prefix):
            rel = url_str[len(prefix):]
            local = SPECIFICATIONS_ROOT / 'tests' / rel
            return local if local.exists() else None
    return None


def _local_input(input_url: URL) -> Path | URL:
    """Use local file when SPEC_PATH is set and URL is from a known spec tests base."""
    local = _url_to_local(input_url)
    return local if local else input_url


class JSONLDTests(Facet[Iterable[TestCase]]):
    def show(self) -> Iterable[TestCase]:
        for row in self.stored_query('tests.sparql', test_class=self.this):
            yield self._row_to_test_case(row)

    def _row_to_test_case(self, row) -> TestCase:  # noqa: WPS210
        test_url = URL(row['test'])
        try:
            extract_all_scripts = row['extract_all_scripts'].value
        except KeyError:
            extract_all_scripts = False

        try:
            compact_arrays = row['compact_arrays'].value
        except KeyError:
            compact_arrays = True

        try:
            ctx = yaml_ld.load_document(
                str(Path(URL(row['context']).path)),
            )['document']
        except KeyError:
            ctx = None

        try:
            frame = yaml_ld.load_document(row['frame'])['document']
        except KeyError:
            frame = None

        redirect_to = row.get('redirect_to')
        base = row.get('base')
        if not base and redirect_to:
            base = 'https://example.com/'
        if not base:
            base = f"{URL(row['input']).parent}/"

        input_source = _local_input(URL(row['input']))
        req = row.get('req')
        base_iri = row.get('base_iri')

        return TestCase(
            test_class=URL(self.this).fragment,
            test=f'{test_url.name}#{test_url.fragment}',
            input=input_source,
            result=self._process_result(row['result']),
            req=req and req.value,
            extract_all_scripts=extract_all_scripts,
            base=base,
            ctx=ctx,
            frame=frame,
            redirect_to=redirect_to,
            base_iri=base_iri and URL(base_iri),
            compact_arrays=compact_arrays,
        )

    def _process_result(
        self,
        result: URIRef | Literal,  # noqa: WPS110
    ) -> Path | str:
        if isinstance(result, URIRef):
            result_url = URL(str(result))
            local = _url_to_local(result_url)
            if local:
                return local
            return Path(result_url.path)

        return result.value
