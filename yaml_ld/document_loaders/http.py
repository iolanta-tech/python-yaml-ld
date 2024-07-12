import io
from dataclasses import dataclass, field

from requests import Session
from yarl import URL

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.base import (
    DocumentLoader,
    DocumentLoaderOptions,
)
from yaml_ld.errors import LoadingDocumentFailed
from yaml_ld.models import URI, RemoteDocument

# Default `requests` timeout. Chosen arbitrarily.
DEFAULT_TIMEOUT = 30


@dataclass
class HTTPDocumentLoader(DocumentLoader):
    """Load documents from HTTP sources."""

    session: Session = field(default_factory=Session)

    def __call__(    # noqa: WPS210
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> RemoteDocument:
        """Load documents from HTTP sources."""
        url = URL(str(source))

        response = self.session.get(
            str(url),
            timeout=DEFAULT_TIMEOUT,
        )

        content_type = response.headers.get('Content-Type')

        if content_type is None:
            content_type = content_types.by_extension(url.suffix)
            if content_type is None:
                raise ValueError(
                    f'What content type is extension `{url.suffix}`?',
                )

        parser = content_types.parser_by_content_type(content_type)
        if parser is None:
            raise LoadingDocumentFailed(path=source)

        yaml_document = parser(
            data_stream=io.StringIO(response.text),
            source=str(source),
            options=options,
        )

        return {
            'document': yaml_document,
            'documentUrl': str(source),
            'contextUrl': None,
            'contentType': content_type,
        }
