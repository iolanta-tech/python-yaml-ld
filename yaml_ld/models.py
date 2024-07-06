from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Sequence

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing_extensions import TypedDict
from urlpath import URL

JsonLdRecord = dict[str, Any]  # type: ignore


class RemoteDocument(TypedDict):
    contentType: str
    contextUrl: str
    document: Any
    documentUrl: str
    profile: str


JsonLdInput = JsonLdRecord | Sequence[JsonLdRecord] | str | Path | URL | RemoteDocument
"""
Input for `expand()`, `compact()` and other functions.

[Specification](https://w3c.github.io/json-ld-api/#dom-jsonldrecord)
"""


ExtractAllScripts = Annotated[
    bool,
    'Extract all JSON-LD script elements, as opposed to only the first one.',
]


class DocumentType(str, Enum):
    """Document type."""

    YAML = 'yaml'
    HTML = 'html'


class ExtractAllScriptsOptions(BaseModel):    # type: ignore
    """Options flag to extract all scripts or not."""

    extract_all_scripts: bool = False
    """
    True to extract all YAML-LD script elements from HTML, False to extract just
    the first.
    """


def _default_document_loader():
    from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
    return DEFAULT_DOCUMENT_LOADER


class BaseOptions(BaseModel):   # type: ignore
    """Base options shared by all YAML-LD API methods."""

    base: str | Path | None = None
    """The base IRI to use."""

    document_loader: Annotated[  # type: ignore
        Any,
        Field(default_factory=_default_document_loader),
    ]
    """The document loader."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        arbitrary_types_allowed=True,
    )
