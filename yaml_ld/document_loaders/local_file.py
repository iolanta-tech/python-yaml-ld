from pathlib import Path
from typing import Any

import yaml
from urlpath import URL

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse


class LocalFileDocumentLoader(DocumentLoader):
    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        with Path(URL(source).path).open() as f:
            return {
                'document': yaml.safe_load(f),
                'documentUrl': source,
                'contextUrl': None,
                'contentType': 'application/ld+yaml',
            }
