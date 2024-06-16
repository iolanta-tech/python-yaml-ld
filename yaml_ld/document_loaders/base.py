from abc import ABC, abstractmethod
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
    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        raise NotImplementedError()
