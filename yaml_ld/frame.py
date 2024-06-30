from enum import StrEnum, Enum
from typing import Annotated

from pydantic import validate_call, Field, field_serializer
from pyld import jsonld

from yaml_ld import parse
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    Document, SerializedDocument, BaseOptions,
    ExtractAllScriptsOptions,
)


class Embed(StrEnum):
    LAST = '@last'
    ALWAYS = '@always'
    NEVER = '@never'
    LINK = '@link'


class FrameOptions(BaseOptions, ExtractAllScriptsOptions):
    """Options for YAML-LD framing."""

    expand_context: Document | None = None
    """A context to expand with."""

    embed: Embed = Embed.LAST
    """Default `@embed` flag."""

    explicit: bool = False
    """Default `@explicit` flag."""

    omit_default: bool = False
    """Default `@omit_default` flag."""

    prune_blank_node_identifiers: bool = True
    """Remove unnecessary blank node identifiers."""

    require_all: bool = False
    """Default `@require_all` flag."""

    @field_serializer('embed')
    def serialize_embed(self, embed: Embed) -> str:
        return embed.value


@validate_call(config=dict(arbitrary_types_allowed=True))
def frame(
    document: SerializedDocument | Document,
    frame: Document,
    options: FrameOptions,
) -> Document:
    """Frame a YAML-LD document."""
    with except_json_ld_errors():
        return jsonld.frame(
            input_=str(document),
            frame=frame,
            options=options.model_dump(by_alias=True),
        )
