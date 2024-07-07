from pydantic import validate_call
from pyld import jsonld

from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    DEFAULT_VALIDATE_CALL_CONFIG,
    BaseOptions,
    ExpandContextOptions,
    ExtractAllScriptsOptions,
    JsonLdContext,
    JsonLdInput,
    JsonLdRecord,
)


class FlattenOptions(   # type: ignore
    BaseOptions,
    ExtractAllScriptsOptions,
    ExpandContextOptions,
):
    """Options to flatten a YAML-LD document."""

    compact_arrays: bool = True
    """Compact arrays to single values when appropriate?"""


DEFAULT_FLATTEN_OPTIONS = FlattenOptions()   # type: ignore


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def flatten(
    document: JsonLdInput,
    ctx: JsonLdContext | None = None,
    options: FlattenOptions = DEFAULT_FLATTEN_OPTIONS,
) -> JsonLdRecord:
    """Flatten a document."""
    with except_json_ld_errors():
        return jsonld.flatten(
            input_=str(document),
            ctx=ctx,
            options=options.model_dump(by_alias=True),
        )
