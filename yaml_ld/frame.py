from pydantic import validate_call
from pyld import jsonld

from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    BaseOptions,
    ExpandContextOptions,
    ExtractAllScriptsOptions,
    JsonLdInput,
    JsonLdRecord,
)


class FrameOptions(   # type: ignore
    BaseOptions,
    ExtractAllScriptsOptions,
    ExpandContextOptions,
):
    """Options for YAML-LD framing."""

    embed: bool = True
    """
    Sets the value object embed flag used in the Framing Algorithm. A boolean
    value of true sets the flag to @once, while a value of false sets the flag
    to @never.
    """

    explicit: bool = False
    """Default `@explicit` flag."""

    omit_default: bool = False
    """Default `@omit_default` flag."""

    prune_blank_node_identifiers: bool = True
    """Remove unnecessary blank node identifiers."""

    require_all: bool = False
    """Default `@require_all` flag."""

    frame_default: bool = False
    """Instead of framing a merged graph, frame only the default graph."""


@validate_call(config=dict(arbitrary_types_allowed=True))
def frame(
    document: JsonLdInput,
    frame: JsonLdRecord,
    options: FrameOptions = FrameOptions(),   # type: ignore
) -> JsonLdRecord:
    """Frame a YAML-LD document."""
    with except_json_ld_errors():
        return jsonld.frame(
            input_=str(document),
            frame=frame,
            options=options.model_dump(by_alias=True),
        )
