from pathlib import Path
from typing import Any

import more_itertools
import yaml
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse
from yaml_ld.document_parsers.yaml_parser import YAMLDocumentParser
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader


class HTTPDocumentLoader(DocumentLoader):

    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import DocumentIsScalar, LoadingDocumentFailed

        url = URL(source)

        if url.suffix in {'.yaml', '.yml', '.yamlld', '.json', '.jsonld'}:
            content = url.get(stream=True).raw
            content.decode_content = True
            yaml_document = YAMLDocumentParser()(content, source, options)

            return {
                'document': yaml_document,
                'documentUrl': str(source),
                'contextUrl': None,
                'contentType': 'application/ld+yaml',
            }

        if url.suffix in {'.html', '.xhtml'}:
            content = url.get().text

            loaded_html = load_html(
                input=content.read(),
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

        raise LoadingDocumentFailed(path=url)
