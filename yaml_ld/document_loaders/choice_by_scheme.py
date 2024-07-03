from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import funcy
from documented import DocumentedError
from pydantic import validate_call
from urlpath import URL

from yaml_ld.document_loaders.base import (
    DocumentLoader,
    DocumentLoaderOptions,
    PyLDResponse,
)


@dataclass
class ProtocolNotFound(DocumentedError):  # type: ignore
    """
    Cannot choose the loader by URL protocol.

    * URL: `{self.url}`
    * Scheme: `{self.formatted_scheme}`
    * Available schemes: {self.formatted_schemes}
    """

    url: URL
    schemes: Iterable[str]

    @property
    def formatted_scheme(self):
        return self.url.scheme or '(empty string)'

    @property
    @funcy.joining(', ')
    def formatted_schemes(self):
        return self.schemes


class ChoiceBySchemeDocumentLoader(DocumentLoader):
    loaders: dict[str, DocumentLoader]

    def __init__(self, **loaders: DocumentLoader) -> None:
        self.loaders = loaders

    def __call__(
        self,
        source: str | Path,
        options: DocumentLoaderOptions,
    ) -> PyLDResponse:
        url = URL(source)

        try:
            loader = self.loaders[url.scheme or 'file']
        except KeyError:
            raise ProtocolNotFound(
                schemes=self.loaders.keys(),
                url=url,
            )

        return loader(source, options)
