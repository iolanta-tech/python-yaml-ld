import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import funcy
from documented import DocumentedError
from yarl import URL

from yaml_ld.models import JsonLdRecord


class YAMLLDError(DocumentedError):
    """An error happened while processing YAML-LD data."""


@dataclass
class PyLDError(YAMLLDError):   # type: ignore
    """{self.message}"""   # noqa: D400

    message: str
    code: str


@dataclass
class DocumentIsScalar(YAMLLDError):   # type: ignore
    """
    Document content MUST be sequence or mapping.

    Instead, `{self.document_type_name}` found.
    """

    document: JsonLdRecord
    code: str = 'loading document failed'

    @property
    def document_type_name(self):
        return type(self.document).__name__


@dataclass
class LoadingDocumentFailed(YAMLLDError):   # type: ignore
    """
    Document is not a valid YAML.

    Path: {self.path}
    """

    path: str
    code: str = 'loading document failed'


@dataclass
class NotFound(YAMLLDError):   # type: ignore
    """
    Document has not been found.

    Path: {self.path}
    """

    path: str
    code: str = 'loading document failed'


@dataclass
class InvalidScriptElement(YAMLLDError):   # type: ignore
    """HTML <script> element content is not valid YAML."""

    code: str = 'invalid script element'


@dataclass
class NoLinkedDataFoundInHTML(YAMLLDError):   # type: ignore
    """
    No Linked Data fragments found in an HTML document.

    ```html
    {self.html_text}
    ```
    """

    html: bytes
    code: str = 'loading document failed'

    def _preview_lines(self, html_text: str) -> Iterable[str]:
        lines = iter(html_text.splitlines())
        preview_count = 10

        yield from funcy.take(preview_count, lines)

        tail = list(lines)
        if not tail:
            return

        if len(tail) >= preview_count:
            yield '…'

        yield from tail[-preview_count:]

    @property
    def html_text(self):
        """Format HTML text for printing."""
        max_line_length = 80
        return '\n'.join(
            textwrap.shorten(line, max_line_length)
            for line in self._preview_lines(
                self.html.decode(),
            )
        )


@dataclass
class MappingKeyError(YAMLLDError):   # type: ignore
    """A mapping key MUST be a string."""

    code: str = 'mapping-key-error'


@dataclass
class InvalidJSONLiteral(YAMLLDError):   # type: ignore
    """A mapping key MUST be a string."""

    code: str = 'invalid JSON literal'


@dataclass
class InvalidEncoding(YAMLLDError):   # type: ignore
    """
    A YAML-LD document MUST be encoded in UTF-8.

    To ensure interoperability with [[JSON]].
    """

    code: str = 'invalid encoding'


@dataclass
class CycleDetected(YAMLLDError):   # type: ignore
    """A YAML-LD document MUST NOT contain cycles."""

    code: str = 'loading document failed'


@dataclass
class UndefinedAliasFound(YAMLLDError):   # type: ignore
    """An undefined alias found."""

    code: str = 'loading document failed'


@dataclass
class LoadingRemoteContextFailed(YAMLLDError):   # type: ignore
    """
    Failed to load the context.

    URL of the context: {self.context}
    Reason: {self.reason}
    """

    context: str
    reason: str

    code: str = 'loading remote context failed'


@dataclass
class ContentTypeNotDetermined(YAMLLDError):   # type: ignore
    """
    Content type is not determined.

    Source: {self.source}
    Glimpse of content:

    ```
    {self.head}
    ```
    """

    source: str | URL | Path
    content: str   # noqa: WPS110
    head_length: int = 128

    @property
    def head(self) -> str:
        """Show a piece of the document content."""
        return textwrap.shorten(self.content, self.head_length)
