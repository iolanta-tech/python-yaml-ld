from dataclasses import dataclass
from pathlib import Path
from typing import Any

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse


@dataclass
class MockLoader(DocumentLoader):
    response: PyLDResponse

    def __call__(
        self,
        source: str | Path,
        options: dict[str, Any],
    ) -> PyLDResponse:
        return self.response
