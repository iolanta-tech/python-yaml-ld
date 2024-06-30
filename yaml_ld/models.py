from enum import Enum
from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from urlpath import URL

Document = dict[str, Any] | list[Any]  # type: ignore
DocumentLoader = Any  # type: ignore   # FIXME: This is actually a callable.

SerializedDocument = Annotated[  # type: ignore
    str | bytes | Path | URL,
    (
        'Either a document serialized to a sequence of characters (or bytes) '
        'or a location where one can be found.'
    ),
]

ExtractAllScripts = Annotated[
    bool,
    'Extract all JSON-LD script elements, as opposed to only the first one.',
]


class DocumentType(str, Enum):
    """Document type."""

    YAML = 'yaml'
    HTML = 'html'


class ProcessingMode(str, Enum):  # noqa: WPS600
    """JSON-LD API version."""

    JSON_LD_1_0 = 'json-ld-1.0'  # noqa: WPS114, WPS115
    JSON_LD_1_1 = 'json-ld-1.1'  # noqa: WPS114, WPS115


class ExtractAllScriptsOptions(BaseModel):
    """Options flag to extract all scripts or not."""

    extract_all_scripts: bool = False
    """
    True to extract all YAML-LD script elements from HTML, False to extract just
    the first.
    """

def _default_document_loader():
    from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
    return DEFAULT_DOCUMENT_LOADER


class BaseOptions(BaseModel):
    """Base options shared by all YAML-LD API methods."""

    base: str | Path | None = None
    """The base IRI to use."""

    document_loader: Annotated[
        DocumentLoader,
        Field(default_factory=_default_document_loader),
    ]
    """The document loader."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
