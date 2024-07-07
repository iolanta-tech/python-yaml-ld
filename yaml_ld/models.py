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


JsonLdInput = (
    JsonLdRecord | Sequence[JsonLdRecord] | str | Path | URL | RemoteDocument
)
"""
Input for `expand()`, `compact()` and other functions.

[Specification](https://w3c.github.io/json-ld-api/#dom-jsonldrecord)
"""

JsonLdContext = JsonLdRecord | list[JsonLdRecord | str] | str
"""
The `JsonLdContext` interface is used to refer to a value that may be a
`JsonLdRecord`, a sequence of `JsonLdRecord`-s, or a string representing an IRI,
which can be dereferenced to retrieve a valid JSON document.

[Specification](https://w3c.github.io/json-ld-api/#dom-jsonldcontext)
"""


ExtractAllScripts = Annotated[
    bool,
    'Extract all JSON-LD script elements, as opposed to only the first one.',
]


class ExtractAllScriptsOptions(BaseModel):    # type: ignore
    """Options flag to extract all scripts or not."""

    extract_all_scripts: bool = False
    """
    True to extract all YAML-LD script elements from HTML, False to extract just
    the first.
    """


class ExpandContextOptions(BaseModel):    # type: ignore
    """Options flag to extract all scripts or not."""

    expand_context: JsonLdRecord | str | Path | URL | None = None
    """A context to expand with."""

    model_config = ConfigDict(arbitrary_types_allowed=True)


def _default_document_loader():
    from yaml_ld.document_loaders.default import (  # noqa: WPS433
        DEFAULT_DOCUMENT_LOADER,
    )
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


DEFAULT_VALIDATE_CALL_CONFIG = ConfigDict(arbitrary_types_allowed=True)
