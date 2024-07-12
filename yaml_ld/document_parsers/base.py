import io
from abc import abstractmethod

from yaml_ld.document_loaders.base import DocumentLoaderOptions
from yaml_ld.models import JsonLdRecord


class BaseDocumentParser:
    """Parse documents of various types into LD."""

    @abstractmethod
    def __call__(
        self,
        data_stream: io.BytesIO,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse raw data into Linked Data."""
        raise NotImplementedError()
