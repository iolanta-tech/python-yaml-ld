from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, alias_generators

from yaml_ld.models import URI, JsonLdRecord

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

    document_loader: Any = None   # type: ignore
    """The document loader."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=alias_generators.to_camel,
        arbitrary_types_allowed=True,
        validate_default=False,
    )
