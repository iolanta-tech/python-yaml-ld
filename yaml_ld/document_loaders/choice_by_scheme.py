from typing import Any

from urlpath import URL

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse


class ChoiceBySchemeDocumentLoader(DocumentLoader):
    loaders: dict[str, DocumentLoader]

    def __init__(self, **loaders: DocumentLoader) -> None:
        self.loaders = loaders

    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        url = URL(source)
        return self.loaders[url.scheme](source, options)
