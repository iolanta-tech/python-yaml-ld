from pathlib import Path
from typing import Any

import more_itertools
import yaml
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse
from yaml_ld.document_parsers.html_parser import HTMLDocumentParser
from yaml_ld.document_parsers.yaml_parser import YAMLDocumentParser
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader


class LocalFileDocumentLoader(DocumentLoader):

    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import DocumentIsScalar, LoadingDocumentFailed

        path = Path(URL(source).path)

        content_type = content_types.by_extension(path.suffix)

        parser = content_types.parser_by_content_type(content_type)
        if parser is None:
            raise LoadingDocumentFailed(path=path)

        try:
            with path.open() as f:
                yaml_document = parser(f, source, options)
        except FileNotFoundError as file_not_found:
            raise NotFound(path) from file_not_found

        return {
            'document': yaml_document,
            'documentUrl': source,
            'contextUrl': None,
            'contentType': content_type,
        }
