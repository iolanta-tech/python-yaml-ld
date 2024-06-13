from pathlib import Path
from typing import Any

import yaml
from pyld.jsonld import load_html
from urlpath import URL

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse


class LocalFileDocumentLoader(DocumentLoader):
    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        path = Path(URL(source).path)

        if path.suffix in {'.yaml', '.yml', '.yamlld'}:
            with path.open() as f:
                return {
                    'document': yaml.safe_load(f),
                    'documentUrl': source,
                    'contextUrl': None,
                    'contentType': 'application/ld+yaml',
                }

        if path.suffix in {'.html', '.xhtml'}:
            with path.open() as f:
                return {
                    'document': load_html(
                        input=f.read(),
                        url=source,
                        profile=None,
                        options=options,
                    ),
                    'documentUrl': source,
                    'contextUrl': None,
                    'contentType': 'application/ld+yaml',
                }

        raise ValueError(f'Unknown file type: {source}')
