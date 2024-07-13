import pytest
from rdflib import FOAF, DC, DCTERMS
from yarl import URL

import yaml_ld

URLS = [
    URL('https://prefix.cc/context.jsonld'),
    URL('https://schema.org'),
    URL('https://dbpedia.org/data/Arthur_C._Clarke.json'),
    URL('https://dbpedia.org/data/Arthur_C._Clarke.jsonld'),
    URL('https://dbpedia.org/resource/Arthur_C._Clarke'),
    URL('https://www.wikidata.org/wiki/Special:EntityData/Q42.jsonld'),
    # URL('http://bnb.data.bl.uk/doc/resource/007446272'),
    URL('http://id.loc.gov/authorities/names/n79081644.jsonld'),
    URL('http://data.europeana.eu/item/9200285/BibliographicResource_3000117691317'),
    URL(str(FOAF)),
    URL(str(DC)),
    URL(str(DCTERMS)),
]


def _url_to_id(url: URL) -> str:
    return str(url.with_scheme('')).lstrip('/')


@pytest.fixture(params=URLS, ids=_url_to_id)
def url(request) -> URL:
    yaml_ld.load_document(request.param)
    return request.param


def test_expand(url: URL):
    yaml_ld.expand(url)


def test_compact(url: URL):
    yaml_ld.compact(url, ctx={})


def test_flatten(url: URL):
    yaml_ld.flatten(url)


def test_to_rdf(url: URL):
    yaml_ld.to_rdf(url)
