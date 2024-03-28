from pathlib import Path
from typing import Iterable

import funcy
import yaml
from bs4 import BeautifulSoup
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from yaml_ld.errors import (
    DocumentIsScalar,
    LoadingDocumentFailed,
    UndefinedAliasFound, MappingKeyError, InvalidEncoding, NoYAMLWithinHTML,
    InvalidScriptElement,
)
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import Document, DocumentType, ExtractAllScripts


HTML_HEADER = '<html'


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

        if fragment is not None and script.get('id') != fragment:
            continue

        yield script.text


def _parse_html(
    html_string: str,
    fragment: str | None,
    extract_all_scripts: ExtractAllScripts = False,
) -> Document:
    """Parse all YAML-LD scripts embedded into HTML."""
    html_yaml_scripts = list(try_extracting_yaml_from_html(
        html_string,
        fragment=fragment,
    ))

    if not html_yaml_scripts:
        if extract_all_scripts:
            return []

        raise NoYAMLWithinHTML()

    if extract_all_scripts:
        return [parse(script) for script in html_yaml_scripts]

    first_script, *_other_scripts = html_yaml_scripts
    try:
        return parse(
            first_script,
            document_type=DocumentType.YAML,
        )
    except LoadingDocumentFailed as err:
        raise InvalidScriptElement from err


def load_yaml_document(
    raw_document,
    extract_all_scripts: ExtractAllScripts = False,
):
    documents_stream = yaml.load_all(  # noqa: S506
        stream=raw_document,
        Loader=YAMLLDLoader,
    )

    if extract_all_scripts:
        return list(documents_stream)

    first_document = funcy.first(documents_stream)

    # We have to parse the second document, at least, otherwise we will
    # miss parsing errors in the beginning of that document,
    # and `html-manifest#tr016` will crash.
    funcy.first(documents_stream)

    return first_document


def parse(   # noqa: WPS238, WPS231, C901
    raw_document: str | bytes | Path | URL,
    extract_all_scripts: ExtractAllScripts = False,
    document_type: DocumentType | None = None,
) -> Document:
    """Parse a YAML-LD document."""
    fragment = None

    if isinstance(raw_document, URL):
        fragment = raw_document.fragment or None
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

    # Now, `raw_document` is a string, let's try guessing its format.
    if (
        document_type is None
        and raw_document.lstrip()[:len(HTML_HEADER)].lower() == HTML_HEADER
    ):
        document_type = DocumentType.HTML

    if document_type == DocumentType.HTML:
        return _parse_html(
            raw_document,
            fragment=fragment,
            extract_all_scripts=extract_all_scripts,
        )

    try:
        document: Document = load_yaml_document(
            raw_document,
            extract_all_scripts=extract_all_scripts,
        )
    except ScannerError as err:
        if document_type != DocumentType.YAML:
            return _parse_html(
                raw_document,
                fragment=fragment,
                extract_all_scripts=extract_all_scripts,
            )

        raise LoadingDocumentFailed() from err

    except ComposerError as err:
        raise UndefinedAliasFound() from err

    except ConstructorError as err:
        if err.problem == 'found unhashable key':
            raise MappingKeyError() from err

        raise

    except ParserError as err:
        raise InvalidScriptElement() from err

    if not isinstance(document, (dict, list)):
        raise DocumentIsScalar(document=document)

    return document
