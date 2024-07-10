import io
from functools import cached_property

import platformdirs
from requests import Session
from requests_cache import CachedHTTPResponse, CachedSession
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

    def __call__(    # noqa: WPS210
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        """Load documents from HTTP sources."""
        url = URL(str(source))

        response = self.session.get(
            str(url),
            stream=True,
            timeout=DEFAULT_TIMEOUT,
        )

        # This is a hack to support cached responses.
        # Unfortunately, `CachedHTTPResponse.raw.read()` returns empty bytes
        # sequence.
        raw_content = io.BytesIO(response.content) if (
            isinstance(response.raw, CachedHTTPResponse)
        ) else response.raw
        raw_content.decode_content = True

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

        yaml_document = parser(raw_content, str(source), options)

        return {
            'document': yaml_document,
            'documentUrl': str(source),
            'contextUrl': None,
            'contentType': content_type,
        }

    @cached_property
    def session(self) -> Session:
        """HTTP session."""
        return Session()


class HTTPCachedDocumentLoader(HTTPDocumentLoader):
    """HTTP Loader with cache on the filesystem."""

    @cached_property
    def session(self) -> Session:
        """Cached HTTP session."""
        return CachedSession(
            backend='filesystem',
            cache_name=platformdirs.user_cache_dir(
                appname='python-yaml-ld',
                ensure_exists=True,
            ),
        )
