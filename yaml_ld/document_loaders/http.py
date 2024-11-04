import io
import logging
import re
from dataclasses import dataclass, field
from typing import Iterable, cast

import funcy
from annotated_types import EllipsisType
from pyld.jsonld import prepend_base
from requests import HTTPError, Session
from yarl import URL

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.base import DocumentLoader, DocumentLoaderOptions
from yaml_ld.errors import (
    ContentTypeNotDetermined,
    LoadingDocumentFailed,
    NotFound,
)
from yaml_ld.models import URI, RemoteDocument

# Default `requests` timeout. Chosen arbitrarily.
DEFAULT_TIMEOUT = 30

LINK_PATTERN = re.compile(
    '<(?P<relative_link>[^>]+)>; rel="alternate"; '
    'type="(?P<content_type>[^"]+)"',
)

CONTENT_TYPE_PREFERENCE_ORDERING = (
    'application/ld+json',
)

logger = logging.getLogger(__name__)


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
            logger.warning(f'Cannot parse: {pair}')


def maybe_follow_one_of_link_headers(
    links: Iterable[LinkHeader],
    content_type: str | None,
    options: DocumentLoaderOptions,
):
    """Resolve the URL found in the given link headers (or not)."""
    from yaml_ld.document_loaders.default import (  # noqa: WPS433
        DEFAULT_DOCUMENT_LOADER,
    )

    link_by_content_type: dict[str, LinkHeader | EllipsisType] = {
        content_type: ...,  # type: ignore
        **{link.content_type: link for link in links},
    }

    ordered_links = [
        # First, let's list the Link headers that we are most interested in.
        *[
            link
            for preferred_content_type   # noqa: WPS361
            in CONTENT_TYPE_PREFERENCE_ORDERING
            if (link := link_by_content_type.pop(preferred_content_type, None))
        ],

        # Now, the rest of the headers. We did not explicitly mentioned them
        # above but maybe one of them is still okay.
        *list(link_by_content_type.values()),
    ]

    for potential_link in ordered_links:
        if potential_link is ...:
            # It seems that the main page, which brought us the headers, is
            # more interesting to us than any of the headers themselves.
            return None

        try:
            content_types.parser_by_content_type(
                content_type=potential_link.content_type,
                uri=potential_link.url,
            )

        except content_types.ParserNotFound:
            continue

        return DEFAULT_DOCUMENT_LOADER(
            source=potential_link.url,
            options=options,
        )

    # None of the links was interesting enough.
    return None


def parse_raw_link_header(   # noqa: WPS210
    page_url: str,
    link_header: str,
) -> Iterable[LinkHeader]:
    """Parse Link header into a structure."""
    links = re.split(', ?', link_header)

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


def _is_content_type_more_preferable(left: str, right: str | None) -> bool:
    """Determine if Left is better than Right."""
    if left == right:
        return False

    if left is not None and right is None:
        # Anything better than nothing
        return True

    return {
        ('application/rdf+xml', 'application/json'): False,
        ('application/rdf+xml', 'application/ld+json'): False,
        ('application/json', 'application/rdf+xml'): True,
        ('application/rdf+xml', 'text/html'): True,
        ('text/html', 'application/ld+json'): False,
        ('text/html', 'application/json'): False,
        ('application/ld+json', 'text/html'): True,
        ('application/json', 'text/html'): True,
        ('application/json', 'application/ld+json'): False,
    }[left, right]


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
        string_source = str(source)
        url = URL(string_source)

        response = self.session.get(
            string_source,
            headers=options.get('headers'),
            timeout=DEFAULT_TIMEOUT,
        )

        try:
            response.raise_for_status()
        except HTTPError as http_error:
            match http_error.response.status_code:
                case 404:   # noqa: WPS432
                    raise NotFound(path=str(http_error.request.url))

            raise

        content_type = response.headers.get('Content-Type')

        if content_type is None:
            content_type = content_types.by_extension(url.suffix)

        if content_type is not None:
            content_type = re.sub(
                pattern='; charset=utf-8',
                repl='',
                string=content_type,
                flags=re.IGNORECASE,
            )

        if link := response.headers.get('Link'):
            follow_result = self.follow_link_header(
                source=source,
                content_type=content_type,
                link_header=link,
                options=options,
            )

            if follow_result:
                return follow_result

        if content_type is None and response.text.startswith('<rdf:RDF'):
            content_type = 'application/rdf+xml'

        if content_type is None:
            raise ContentTypeNotDetermined(
                source=source,
                content=response.text,
            )

        parser = content_types.parser_by_content_type(
            content_type=content_type,
            uri=string_source,
        )
        if parser is None:
            raise LoadingDocumentFailed(path=source)

        yaml_document = parser(
            data_stream=io.BytesIO(response.content),
            source=string_source,
            options=options,
        )

        return {
            'document': yaml_document,
            'documentUrl': string_source,
            'contextUrl': None,
            'contentType': content_type,
        }

    def follow_link_header(
        self,
        source: URI,
        content_type: str | None,
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

        return maybe_follow_one_of_link_headers(
            links=links,
            content_type=content_type,
            options=options,
        )
