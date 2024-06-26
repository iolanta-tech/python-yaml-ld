from dataclasses import dataclass
from pathlib import Path

from documented import DocumentedError

from yaml_ld.models import JsonLdRecord


class YAMLLDError(DocumentedError):
    """An error happened while processing YAML-LD data."""


@dataclass
class PyLDError(YAMLLDError):
    """{self.message}"""

    message: str
    code: str


@dataclass
class DocumentIsScalar(YAMLLDError):
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
class LoadingDocumentFailed(YAMLLDError):
    """
    Document is not a valid YAML.

    Path: {self.path}
    """

    path: Path
    code: str = 'loading document failed'


@dataclass
class NotFound(YAMLLDError):
    """
    Document has not been found.

    Path: {self.path}
    """

    path: Path
    code: str = 'loading document failed'


@dataclass
class InvalidScriptElement(YAMLLDError):
    """HTML <script> element content is not valid YAML."""

    code: str = 'invalid script element'


@dataclass
class NoYAMLWithinHTML(YAMLLDError):
    """No YAML-LD fragments found in an HTML document."""

    code: str = 'loading document failed'


@dataclass
class MappingKeyError(YAMLLDError):
    """A mapping key MUST be a string."""

    code: str = 'mapping-key-error'


@dataclass
class InvalidJSONLiteral(YAMLLDError):
    """A mapping key MUST be a string."""

    code: str = 'invalid JSON literal'


@dataclass
class InvalidEncoding(YAMLLDError):
    """
    A YAML-LD document MUST be encoded in UTF-8.

    To ensure interoperability with [[JSON]].
    """

    code: str = 'invalid encoding'


@dataclass
class CycleDetected(YAMLLDError):
    """A YAML-LD document MUST NOT contain cycles."""

    code: str = 'loading document failed'


@dataclass
class UndefinedAliasFound(YAMLLDError):
    """An undefined alias found."""

    code: str = 'loading document failed'


@dataclass
class LoadingRemoteContextFailed(YAMLLDError):
    """
    Failed to load the context.

    URL of the context: {self.context}
    Reason: {self.reason}
    """

    context: str
    reason: str

    code: str = 'loading remote context failed'
