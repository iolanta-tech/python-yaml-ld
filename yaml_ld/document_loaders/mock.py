from dataclasses import dataclass

from yaml_ld.document_loaders.base import DocumentLoader, DocumentLoaderOptions
from yaml_ld.models import URI, RemoteDocument


@dataclass
class MockLoader(DocumentLoader):
    """Mock loader returning the response specified as argument."""

    response: RemoteDocument

    def __call__(
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> RemoteDocument:
        """Return the prepared response."""
        return self.response
