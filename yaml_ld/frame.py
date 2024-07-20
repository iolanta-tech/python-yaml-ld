from pydantic import validate_call
from pyld import jsonld

from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    DEFAULT_VALIDATE_CALL_CONFIG,
    JsonLdInput,
    JsonLdRecord,
    ensure_string_or_document,
)
from yaml_ld.options import (
    BaseOptions,
    ExpandContextOptions,
    ExtractAllScriptsOptions,
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


DEFAULT_FRAME_OPTIONS = FrameOptions()


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def frame(
    document: JsonLdInput,
    frame: JsonLdRecord,   # noqa: WPS442
    options: FrameOptions = DEFAULT_FRAME_OPTIONS,
) -> JsonLdRecord:
    """Frame a [＊-LD](/blog/any-ld/) document."""
    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)

    with except_json_ld_errors():
        return jsonld.frame(
            input_=ensure_string_or_document(document),
            frame=frame,
            options=dict_options,
        )
