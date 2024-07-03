import io
from abc import abstractmethod
from typing import Any, TypedDict

from yaml_ld.models import JsonLdRecord


DocumentParserOptions = TypedDict(
    'DocumentParserOptions',
    {}
)


class BaseDocumentParser:
    @abstractmethod
    def __call__(self, data: io.TextIOBase, source: str, options: DocumentParserOptions) -> JsonLdRecord:
        raise NotImplementedError()
