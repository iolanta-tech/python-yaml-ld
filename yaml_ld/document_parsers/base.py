import io
from abc import abstractmethod
from typing import Any

from yaml_ld.models import Document


class BaseDocumentParser:
    @abstractmethod
    def __call__(self, data: io.TextIOBase, source: str, options: dict[str, Any]) -> Document:
        raise NotImplementedError()
