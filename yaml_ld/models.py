from pathlib import Path
from typing import Annotated, Any, Sequence

from pydantic import BaseModel, ConfigDict, Field, alias_generators
from typing_extensions import TypedDict
from yarl import URL

JsonLdRecord = dict[str, Any]  # type: ignore


class RemoteDocument(TypedDict):
    contentType: str
    contextUrl: str
    document: Any
    documentUrl: str
    profile: str


URI = str | URL | Path
"""
A Universal Resource Identifier can be represented as a `Path` or as a `URL`.

Or, it can be a `str`, and we will try to automatically identify what that is.
"""


JsonLdInput = (
    JsonLdRecord | Sequence[JsonLdRecord] | URI | RemoteDocument
)
"""
Input for `expand()`, `compact()` and other functions.

[Specification](https://w3c.github.io/json-ld-api/#dom-jsonldrecord)
"""

JsonLdContext = JsonLdRecord | list[JsonLdRecord | URI] | URI
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

    expand_context: JsonLdRecord | URI | None = None
    """A context to expand with."""

    model_config = ConfigDict(arbitrary_types_allowed=True)


def _default_document_loader():
    from yaml_ld.document_loaders.default import (  # noqa: WPS433
        DEFAULT_DOCUMENT_LOADER,
    )
    return DEFAULT_DOCUMENT_LOADER


class BaseOptions(BaseModel):   # type: ignore
    """Base options shared by all YAML-LD API methods."""

    base: URI | None = None
    """The base IRI to use."""

    document_loader: Annotated[  # type: ignore
        Any,
        Field(default_factory=_default_document_loader),
    ]
    """The document loader."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=alias_generators.to_camel,
        arbitrary_types_allowed=True,
    )


DEFAULT_VALIDATE_CALL_CONFIG = ConfigDict(arbitrary_types_allowed=True)
