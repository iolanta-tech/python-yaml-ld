from pathlib import Path
from typing import Any

import more_itertools
import yaml
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse
from yaml_ld.document_parsers.html_parser import HTMLDocumentParser
from yaml_ld.document_parsers.yaml_parser import YAMLDocumentParser
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader


class LocalFileDocumentLoader(DocumentLoader):

    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import DocumentIsScalar, LoadingDocumentFailed

        path = Path(URL(source).path)

        if path.suffix in {'.yaml', '.yml', '.yamlld', '.json', '.jsonld'}:
            try:
                with path.open() as f:
                    yaml_document = YAMLDocumentParser()(f, source, options)

                    return {
                        'document': yaml_document,
                        'documentUrl': source,
                        'contextUrl': None,
                        'contentType': 'application/ld+yaml',
                    }
            except FileNotFoundError as file_not_found:
                from yaml_ld.errors import NotFound
                raise NotFound(path) from file_not_found

        if path.suffix in {'.html', '.xhtml'}:
            with path.open() as f:
                loaded_html = HTMLDocumentParser()(f, source, options)

            return {
                'document': loaded_html,
                'documentUrl': source,
                'contextUrl': None,
                'contentType': 'application/ld+yaml',
            }

        raise LoadingDocumentFailed(path=path)
