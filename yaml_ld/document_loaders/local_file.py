from pathlib import Path

from urlpath import URL

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.base import (
    DocumentLoader,
    DocumentLoaderOptions,
    PyLDResponse,
)
from yaml_ld.errors import LoadingDocumentFailed, NotFound


class LocalFileDocumentLoader(DocumentLoader):
    """Load documents from a local file system."""

    def __call__(
        self,
        source: str | Path,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        """Load documents from a local file system."""
        path = Path(URL(source).path)

        content_type = content_types.by_extension(path.suffix)
        if content_type is None:
            raise ValueError(f'What content type is extension {path.suffix}?')

        parser = content_types.parser_by_content_type(content_type)
        if parser is None:
            raise LoadingDocumentFailed(path=path)

        try:
            with path.open() as f:
                yaml_document = parser(f, str(source), options)
        except FileNotFoundError as file_not_found:
            raise NotFound(path) from file_not_found

        return {
            'document': yaml_document,
            'documentUrl': str(source),
            'contextUrl': None,
            'contentType': content_type,
        }
