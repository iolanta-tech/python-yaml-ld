from yarl import URL

import yaml_ld


def test_expand(url: URL):
    """Try expanding a remote document."""
    yaml_ld.expand(url)


def test_compact(url: URL):
    """Try compacting a remote document."""
    yaml_ld.compact(url, ctx={})


def test_flatten(url: URL):
    """Try flattening a remote document."""
    yaml_ld.flatten(url)


def test_to_rdf(url: URL):
    """Try converting a remote document to RDF."""
    rdf = yaml_ld.to_rdf(url)
    assert isinstance(rdf, dict)
    assert rdf['@default']
