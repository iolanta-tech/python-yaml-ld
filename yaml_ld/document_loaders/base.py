from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TypedDict

from yaml_ld.models import JsonLdRecord

PyLDResponse = TypedDict(
    'PyLDResponse', {
        'contentType': str,
        'contextUrl': str | None,
        'documentUrl': str,
        'document': JsonLdRecord,
    },
)


class DocumentLoader(ABC):
    @abstractmethod
    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        raise NotImplementedError()
