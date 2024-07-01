from pathlib import Path
from typing import Any

from urlpath import URL

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse


class HTTPDocumentLoader(DocumentLoader):

    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import LoadingDocumentFailed

        url = URL(source)

        content = url.get(stream=True).raw
        content.decode_content = True

        content_type = content_types.by_extension(url.suffix)
        if content_type is None:
            raise ValueError(f'What content type is extension {url.suffix}?')

        parser = content_types.parser_by_content_type(content_type)
        if parser is None:
            raise LoadingDocumentFailed(path=source)

        yaml_document = parser(content, source, options)

        return {
            'document': yaml_document,
            'documentUrl': str(source),
            'contextUrl': None,
            'contentType': 'application/ld+yaml',
        }
