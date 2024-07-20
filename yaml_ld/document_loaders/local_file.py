from pathlib import Path

from yarl import URL

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.base import DocumentLoader, DocumentLoaderOptions
from yaml_ld.errors import LoadingDocumentFailed, NotFound
from yaml_ld.models import URI, RemoteDocument


class LocalFileDocumentLoader(DocumentLoader):
    """Load documents from a local file system."""

    def __call__(
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> RemoteDocument:
        """Load documents from a local file system."""
        path = Path(URL(str(source)).path)

        content_type = content_types.by_extension(path.suffix)
        if content_type is None:
            raise ValueError(f'What content type is extension {path.suffix}?')

        parser = content_types.parser_by_content_type(
            content_type=content_type,
            uri=str(path),
        )
        if parser is None:
            raise LoadingDocumentFailed(path=path)

        try:
            with path.open(mode='rb') as data_stream:
                yaml_document = parser(
                    data_stream=data_stream,   # type: ignore
                    source=str(source),
                    options=options,
                )
        except FileNotFoundError as file_not_found:
            raise NotFound(path) from file_not_found

        return {
            'document': yaml_document,
            'documentUrl': str(source),
            'contextUrl': None,
            'contentType': content_type,
        }
