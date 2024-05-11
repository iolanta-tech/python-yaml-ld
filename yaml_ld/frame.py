from enum import StrEnum
from typing import Annotated

from pydantic import validate_call
from pyld import jsonld

from yaml_ld import parse
from yaml_ld.annotations import API, FRAMING
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import Document, SerializedDocument, BaseOptions


class Embed(StrEnum):
    LAST = '@last'
    ALWAYS = '@always'
    NEVER = '@never'
    LINK = '@link'


class FrameOptions(BaseOptions):
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


@validate_call(config=dict(arbitrary_types_allowed=True))
def frame(
    document: SerializedDocument | Document,
    frame: Document,
    options: FrameOptions,
) -> Annotated[Document, FRAMING / '#dom-jsonldprocessor-frame']:
    """Frame a YAML-LD document."""
    if isinstance(document, (str, bytes)):
        document = parse(document)

    with except_json_ld_errors():
        return jsonld.frame(
            input_=document,
            frame=frame,
            options=options.model_dump(by_alias=True),
        )
