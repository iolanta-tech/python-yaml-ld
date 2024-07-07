from pathlib import Path

import requests
from yarl import URL

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.base import (
    DocumentLoader,
    DocumentLoaderOptions,
    PyLDResponse,
)
from yaml_ld.errors import LoadingDocumentFailed
from yaml_ld.models import URI

# Default `requests` timeout. Chosen arbitrarily.
DEFAULT_TIMEOUT = 30


class HTTPDocumentLoader(DocumentLoader):
    """Load documents from HTTP sources."""

    def __call__(
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        """Load documents from HTTP sources."""
        url = URL(str(source))

        raw_content = requests.get(
            str(url),
            stream=True,
            timeout=DEFAULT_TIMEOUT,
        ).raw
        raw_content.decode_content = True

        content_type = content_types.by_extension(url.suffix)
        if content_type is None:
            raise ValueError(f'What content type is extension {url.suffix}?')

        parser = content_types.parser_by_content_type(content_type)
        if parser is None:
            raise LoadingDocumentFailed(path=source)

        yaml_document = parser(raw_content, str(source), options)

        return {
            'document': yaml_document,
            'documentUrl': str(source),
            'contextUrl': None,
            'contentType': 'application/ld+yaml',
        }
