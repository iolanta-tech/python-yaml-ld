from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypedDict, Any

PyLDResponse = TypedDict(
    'PyLDResponse', {
        'contentType': str,
        'contextUrl': str | None,
        'documentUrl': str,
        'document': dict[str, Any],
    },
)


class DocumentLoader(ABC):
    @abstractmethod
    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        raise NotImplementedError()
