import io
import re
from dataclasses import dataclass, field
from typing import Iterable, cast

import funcy
from pyld.jsonld import prepend_base
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

LINK_PATTERN = re.compile(
    '<(?P<relative_link>[^>]+)>; rel="alternate"; '
    'type="(?P<content_type>[^"]+)"',
)


@dataclass
class LinkHeader:
    """Reference from HTTP Link header."""

    url: str
    rel: str
    content_type: str
    attributes: dict[str, str]


@funcy.post_processing(dict)
def _parse_link_attributes(
    raw_attributes: list[str],
) -> Iterable[tuple[str, str]]:
    for pair in raw_attributes:
        match_result = re.match(
            '(?P<attribute_name>[^=]+)="(?P<attribute_value>[^"]+)"',
            pair,
        )

        if match_result:
            yield cast(tuple[str, str], match_result.groups())
        else:
            raise ValueError(f'Cannot parse: {pair}')


def parse_raw_link_header(   # noqa: WPS210
    page_url: str,
    link_header: str,
) -> Iterable[LinkHeader]:
    """Parse Link header into a structure."""
    links = link_header.split(', ')

    for link in links:
        bracketed_url, *raw_attributes = link.split('; ')
        relative_url = bracketed_url.removeprefix('<').removesuffix('>')

        absolute_url = prepend_base(page_url, relative_url)
        attributes: dict[str, str] = _parse_link_attributes(raw_attributes)

        if content_type := attributes.pop('type', None):
            yield LinkHeader(
                url=absolute_url,
                rel=attributes.pop('rel'),
                content_type=content_type,
                attributes=attributes,
            )


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

        if link := response.headers.get('Link'):
            follow_result = self.follow_link_header(
                source=source,
                link_header=link,
                options=options,
            )

            if follow_result:
                return follow_result

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
            data_stream=io.BytesIO(response.content),
            source=str(source),
            options=options,
        )

        return {
            'document': yaml_document,
            'documentUrl': str(source),
            'contextUrl': None,
            'contentType': content_type,
        }

    def follow_link_header(
        self,
        source: URI,
        link_header: str,
        options: DocumentLoaderOptions,
    ) -> RemoteDocument | None:
        """Follow Link header."""
        links = parse_raw_link_header(
            page_url=str(source),
            link_header=link_header,
        )

        links = [
            link
            for link in links
            if link.rel == 'alternate'
        ]

        from yaml_ld.document_loaders.default import (   # noqa: WPS433
            DEFAULT_DOCUMENT_LOADER,
        )

        for link in links:
            try:
                content_types.parser_by_content_type(link.content_type)
            except content_types.ParserNotFound:
                continue

            return DEFAULT_DOCUMENT_LOADER(
                source=link.url,
                options=options,
            )

        return None
