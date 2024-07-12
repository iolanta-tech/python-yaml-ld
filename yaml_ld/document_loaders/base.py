from abc import ABC, abstractmethod

from typing_extensions import TypedDict

from yaml_ld.models import URI, RemoteDocument

DocumentLoaderOptions = TypedDict(
    'DocumentLoaderOptions',
    {
        'extractAllScripts': bool,
    },
)


class DocumentLoader(ABC):
    @abstractmethod
    def __call__(
        self,
        source: URI,
        options: DocumentLoaderOptions,
    ) -> RemoteDocument:
        """Load a document."""
        raise NotImplementedError()
