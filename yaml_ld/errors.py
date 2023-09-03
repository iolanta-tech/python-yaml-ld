from dataclasses import dataclass
from typing import Any

from documented import DocumentedError


class YAMLLDError(DocumentedError):
    ...


@dataclass
class LoadingDocumentFailed(YAMLLDError):
    """
    Document content MUST be sequence or mapping.

    Instead, `{self.document_type_name}` found.
    """

    document: Any
    code: str = 'loading document failed'

    @property
    def document_type_name(self):
        return type(self.document).__name__


@dataclass
class MappingKeyError(YAMLLDError):
    """A mapping key MUST be a string."""

    code: str = 'mapping-key-error'


@dataclass
class InvalidEncoding(YAMLLDError):
    """A YAML-LD document MUST be encoded in UTF-8, to ensure interoperability with [[JSON]]."""

    code: str = 'invalid encoding'
