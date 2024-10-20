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
