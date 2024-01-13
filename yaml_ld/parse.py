from pathlib import Path
from typing import Iterable

import yaml
from bs4 import BeautifulSoup
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.scanner import ScannerError

from yaml_ld.errors import (
    DocumentIsScalar,
    LoadingDocumentFailed,
    UndefinedAliasFound, MappingKeyError, InvalidEncoding,
)
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import Document, DocumentType


def try_extracting_yaml_from_html(
    yaml_string: str,
    fragment: str | None,
) -> Iterable[str]:
    """Extract YAML from <script> tags in an HTML page."""
    soup = BeautifulSoup(yaml_string, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if script['type'] not in {'application/ld+json', 'application/ld+yaml'}:
            continue

        if fragment is not None and script['id'] != fragment:
            continue

        yield script.text


def _parse_html(html_string: str, fragment: str | None) -> Document:
    """Parse all YAML-LD scripts embedded into HTML."""
    html_yaml_scripts = list(try_extracting_yaml_from_html(
        html_string,
        fragment=fragment,
    ))

    if not html_yaml_scripts:
        return {}

    first_script, *_other_scripts = html_yaml_scripts
    return parse(first_script)


def parse(   # noqa: WPS238, WPS231, C901
    raw_document: str | bytes | Path | URL,
) -> Document:
    """Parse a YAML-LD document."""
    document_type = None
    fragment = None

    if isinstance(raw_document, URL):
        fragment = raw_document.fragment
        raw_document = Path(raw_document.path)

    if isinstance(raw_document, Path):
        document_type = {
            '.json': DocumentType.YAML,
            '.jsonld': DocumentType.YAML,
            '.yaml': DocumentType.YAML,
            '.yamlld': DocumentType.YAML,
            '.html': DocumentType.HTML,
        }.get(raw_document.suffix)

        raw_document = raw_document.read_bytes()

    if isinstance(raw_document, bytes):
        try:
            raw_document = raw_document.decode('utf-8')
        except UnicodeDecodeError as err:
            raise InvalidEncoding() from err

    try:
        document: Document = yaml.load(  # noqa: S506
            stream=raw_document,
            Loader=YAMLLDLoader,
        )
    except ScannerError as err:
        if document_type != DocumentType.YAML:
            return _parse_html(raw_document, fragment=fragment)

        raise LoadingDocumentFailed() from err

    except ComposerError as err:
        raise UndefinedAliasFound() from err

    except ConstructorError as err:
        if err.problem == 'found unhashable key':
            raise MappingKeyError() from err

        raise

    if not isinstance(document, (dict, list)):
        raise DocumentIsScalar(document=document)

    return document
