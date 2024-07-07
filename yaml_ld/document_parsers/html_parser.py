import io
from dataclasses import dataclass
from typing import Iterable

import lxml  # noqa: S410
import yaml
from pyld.jsonld import JsonLdError, parse_url, prepend_base

from yaml_ld.document_loaders import content_types
from yaml_ld.document_loaders.content_types import ParserNotFound
from yaml_ld.document_parsers.base import (
    BaseDocumentParser,
    DocumentLoaderOptions,
)
from yaml_ld.errors import DocumentIsScalar
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import JsonLdRecord


@dataclass
class Script:
    """HTML <script> tag."""

    content_type: str
    content: str


class HTMLDocumentParser(BaseDocumentParser):
    """Parse HTML documents, specifically their <script> tags."""

    def _parse_script_content(self, content: str):
        return list(
            yaml.load_all(
                content,
                Loader=YAMLLDLoader,
            ),
        )

    def extract_script_tags(   # noqa: C901
        self,
        input,
        url,
        profile,
        options,
    ) -> Iterable[Script]:
        """Load one or more script tags from an HTML source."""
        document = lxml.html.fromstring(input)
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
            id = url_elements.fragment
            element = document.xpath('//script[@id="%s"]' % id)
            if not element:
                raise JsonLdError(
                    'No script tag found for id.',
                    'jsonld.LoadDocumentError',
                    {'id': id}, code='loading document failed',
                )

            yield Script(
                content_type=element[0].xpath('@type')[0],
                content=element[0].text_content(),
            )

        elements = document.xpath('//script')

        if options.get('extractAllScripts'):
            for element in elements:
                yield Script(
                    content_type=element.xpath('@type')[0],
                    content=element.text_content(),
                )

    def __call__(
        self,
        data_stream: io.TextIOBase,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse HTML with LD in <script> tags."""
        scripts = self.extract_script_tags(
            input=data_stream.read(),
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
            raise ValueError(f'No script tags found for {source}')

    def parsed_documents_stream(
        self,
        scripts: Iterable[Script],
        source: str,
        options: DocumentLoaderOptions,
    ) -> Iterable[JsonLdRecord]:
        """Parse each of the given scripts and emit a stream of LD documents."""
        for script in scripts:
            try:
                parser = content_types.parser_by_content_type(
                    script.content_type,
                )
            except ParserNotFound:
                continue

            stream = io.StringIO(script.content)
            document_or_array = parser(stream, source, options)

            match document_or_array:
                case list() as array:
                    yield from array

                case dict() as mapping:
                    yield mapping

                case scalar:
                    raise DocumentIsScalar(scalar)
