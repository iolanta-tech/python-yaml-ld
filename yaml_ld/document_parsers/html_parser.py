import io
from typing import Any

import yaml

from yaml_ld.document_parsers.base import (
    BaseDocumentParser,
    DocumentLoaderOptions,
)
from yaml_ld.errors import DocumentIsScalar
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import JsonLdRecord


class HTMLDocumentParser(BaseDocumentParser):

    def _parse_script_content(self, content: str):
        return list(
            yaml.load_all(
                content,
                Loader=YAMLLDLoader,
            ),
        )

    def __call__(
        self,
        data_stream: io.TextIOBase,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse HTML with LD in <script> tags."""
        loaded_html = load_html(
            input=data_stream.read(),
            url=source,
            profile=None,
            options=options,
            content_type='application/ld+yaml',
            parse_script_content=self._parse_script_content,
        )

        if isinstance(loaded_html, str):
            raise DocumentIsScalar(loaded_html)

        return loaded_html