from dataclasses import dataclass
from pathlib import Path

from yaml_ld.document_loaders.base import (
    DocumentLoader,
    DocumentLoaderOptions,
    PyLDResponse,
)
from yaml_ld.models import URI


@dataclass
class MockLoader(DocumentLoader):
    response: PyLDResponse

    def __call__(
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        """Return the prepared response."""
        return self.response
