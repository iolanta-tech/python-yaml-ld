from abc import ABC
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
    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        raise NotImplementedError()