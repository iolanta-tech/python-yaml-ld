from pathlib import Path

from yaml_ld.document_loaders.http import parse_raw_link_header


def test_parse_raw_link_header():
    header_path = Path(__file__).parent / 'data' / 'header.txt'
    header = header_path.read_text()

    links = list(
        parse_raw_link_header(
            page_url='http://www.wikidata.org/prop/P101',
            link_header=header,
        ),
    )

    assert len(links) > 1
    assert links[-1].content_type == 'application/ld+json'
    assert str(links[-1].url) == (
        'https://www.wikidata.org/wiki/Special:EntityData/P101.jsonld'
    )
