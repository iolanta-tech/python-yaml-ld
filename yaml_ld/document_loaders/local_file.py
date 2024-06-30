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
from yaml_ld.document_parsers.yaml_parser import YAMLDocumentParser
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader


class LocalFileDocumentLoader(DocumentLoader):
    def _parse_script_content(self, content: str):
        return list(
            yaml.load_all(
                content,
                Loader=YAMLLDLoader,
            ),
        )

    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import DocumentIsScalar, LoadingDocumentFailed

        path = Path(URL(source).path)

        if path.suffix in {'.yaml', '.yml', '.yamlld', '.json', '.jsonld'}:
            try:
                with path.open() as f:
                    yaml_document = YAMLDocumentParser()(f, options)

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
                loaded_html = load_html(
                    input=f.read(),
                    url=source,
                    profile=None,
                    options=options,
                    content_type='application/ld+yaml',
                    parse_script_content=self._parse_script_content,
                )

                if isinstance(loaded_html, str):
                    raise DocumentIsScalar(loaded_html)

            return {
                'document': loaded_html,
                'documentUrl': source,
                'contextUrl': None,
                'contentType': 'application/ld+yaml',
            }

        raise LoadingDocumentFailed(path=path)
