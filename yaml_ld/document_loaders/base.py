from abc import ABC, abstractmethod
from pathlib import Path

from typing_extensions import TypedDict

from yaml_ld.models import URI, JsonLdRecord

PyLDResponse = TypedDict(
    'PyLDResponse', {
        'contentType': str,
        'contextUrl': str | None,   # noqa: WPS465
        'documentUrl': str,
        'document': JsonLdRecord | list[JsonLdRecord],
    },
)

DocumentLoaderOptions = TypedDict(
    'DocumentLoaderOptions',
    {
        'extractAllScripts': bool,
    },
)


class DocumentLoader(ABC):
    @abstractmethod
    def __call__(
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        """Load a document."""
        raise NotImplementedError()
