import io
from abc import abstractmethod

from typing_extensions import TypedDict

from yaml_ld.document_loaders.base import DocumentLoaderOptions
from yaml_ld.models import JsonLdRecord


class BaseDocumentParser:
    @abstractmethod
    def __call__(
        self,
        data_stream: io.TextIOBase,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        raise NotImplementedError()
