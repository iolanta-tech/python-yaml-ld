from dataclasses import dataclass
from pathlib import Path

from yaml_ld.document_loaders.base import (
    DocumentLoader,
    DocumentLoaderOptions,
    PyLDResponse,
)


@dataclass
class MockLoader(DocumentLoader):
    response: PyLDResponse

    def __call__(
        self,
        source: str | Path,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        return self.response
