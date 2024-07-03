from abc import ABC, abstractmethod
from pathlib import Path

from typing_extensions import TypedDict

from yaml_ld.models import JsonLdRecord

PyLDResponse = TypedDict(
    'PyLDResponse', {
        'contentType': str,
        'contextUrl': str | None,
        'documentUrl': str,
        'document': JsonLdRecord,
    },
)

DocumentLoaderOptions = TypedDict(
    'DocumentLoaderOptions',
    {
        'extractAllScripts': bool,
    }
)


class DocumentLoader(ABC):
    @abstractmethod
    def __call__(
        self,
        source: str | Path,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        raise NotImplementedError()
