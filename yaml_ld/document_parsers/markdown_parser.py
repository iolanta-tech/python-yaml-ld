import io

import frontmatter

from yaml_ld.document_parsers.base import (
    BaseDocumentParser,
    DocumentLoaderOptions,
)
from yaml_ld.document_parsers.yaml_parser import ensure_not_scalar
from yaml_ld.errors import InvalidEncoding, LoadingDocumentFailed
from yaml_ld.models import JsonLdRecord


class MarkdownDocumentParser(BaseDocumentParser):
    """Parse Markdown documents with YAML front matter."""

    def __call__(   # noqa: WPS238, WPS231, WPS225, C901
        self,
        data_stream: io.BytesIO,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse Markdown document with YAML front matter into LD."""
        try:
            markdown_content = data_stream.read().decode('utf-8')
        except UnicodeDecodeError as unicode_decode_error:
            raise InvalidEncoding() from unicode_decode_error

        try:
            metadata, _content = (  # noqa: WPS110
                frontmatter.parse(markdown_content)
            )
        except Exception as parse_error:
            raise LoadingDocumentFailed(path=source) from parse_error

        return ensure_not_scalar(metadata)
