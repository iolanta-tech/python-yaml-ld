import io
from dataclasses import dataclass
from typing import Iterable

import funcy
import lxml  # noqa: S410
from bs4 import BeautifulSoup
from pyld.jsonld import JsonLdError, parse_url, prepend_base

from yaml_ld.document_loaders.content_types import (
    ParserNotFound,
    parser_by_content_type,
)
from yaml_ld.document_loaders.http import (
    LinkHeader,
    maybe_follow_one_of_link_headers,
)
from yaml_ld.document_parsers.base import (
    BaseDocumentParser,
    DocumentLoaderOptions,
)
from yaml_ld.errors import DocumentIsScalar, NoLinkedDataFoundInHTML
from yaml_ld.models import JsonLdRecord


@dataclass
class Script:
    """HTML <script> tag."""

    content_type: str
    content: str   # noqa: WPS110


class HTMLDocumentParser(BaseDocumentParser):
    """Parse HTML documents, specifically their <script> tags."""

    def __call__(
        self,
        data_stream: io.BytesIO,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse HTML with LD in <script> tags."""
        html_content = data_stream.read()
        links = self.extract_link_tags(html_content)

        linked_document = maybe_follow_one_of_link_headers(
            links=links,
            content_type='text/html',
            options=options,
        )

        if linked_document:
            return linked_document

        scripts = self.extract_script_tags(
            html_content=html_content,
            url=source,
            profile=None,
            options=options,
        )

        documents = self.parsed_documents_stream(
            scripts=scripts,
            source=source,
            options=options,
        )

        if options.get('extractAllScripts'):
            return list(documents)

        try:
            return next(iter(documents))
        except StopIteration:
            raise NoLinkedDataFoundInHTML(html=html_content)

    def extract_script_tags(   # noqa: C901, WPS210
        self,
        html_content: bytes,
        url,
        profile,
        options,
    ) -> Iterable[Script]:
        """Load one or more script tags from an HTML source."""
        document = lxml.html.fromstring(html_content)
        # potentially update options[:base]
        html_base = document.xpath('/html/head/base/@href')
        if html_base:
            # use either specified base, or document location
            effective_base = options.get('base', url)
            if effective_base:
                html_base = prepend_base(effective_base, html_base[0])
            options['base'] = html_base

        url_elements = parse_url(url)
        if url_elements.fragment:
            # FIXME: CGI decode
            fragment_id = url_elements.fragment
            singular_element = document.xpath(
                '//script[@id="%s"]' % fragment_id,
            )
            if not singular_element:
                raise JsonLdError(
                    'No script tag found for id.',
                    'jsonld.LoadDocumentError',
                    {'id': fragment_id},
                    code='loading document failed',
                )

            yield Script(
                content_type=singular_element[0].xpath('@type')[0],
                content=singular_element[0].text_content(),
            )

        elements = document.xpath('//script')
        for element in elements:   # noqa: WPS526
            if content_type := funcy.first(element.xpath('@type')):
                yield Script(
                    content_type=content_type,
                    content=element.text_content(),
                )

    def parsed_documents_stream(
        self,
        scripts: Iterable[Script],
        source: str,
        options: DocumentLoaderOptions,
    ) -> Iterable[JsonLdRecord]:
        """Parse each of the given scripts and emit a stream of LD documents."""
        for script in scripts:
            try:
                parser = parser_by_content_type(
                    content_type=script.content_type,
                    uri=source,
                )
            except ParserNotFound:
                continue

            stream = io.BytesIO(script.content.encode())
            document_or_array = parser(
                data_stream=stream,
                source=source,
                options=options,
            )

            match document_or_array:
                case list() as array:
                    yield from array

                case dict() as mapping:
                    yield mapping

                case scalar:
                    raise DocumentIsScalar(scalar)

    @funcy.post_processing(list)
    def extract_link_tags(self, html_content: str) -> Iterable[LinkHeader]:
        """Extract <link> tags."""
        soup = BeautifulSoup(html_content, features='lxml')
        links = soup.find_all('link', attrs={'rel': 'alternate'})
        for link in links:
            content_type = link.get('type')

            if content_type:
                yield LinkHeader(
                    url=link['href'],
                    rel=funcy.first(link['rel']),
                    content_type=content_type,
                    attributes={},
                )
