from pydantic import validate_call
from pyld import jsonld

from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    BaseOptions,
    ExtractAllScriptsOptions,
    JsonLdInput,
    JsonLdRecord,
)


class FlattenOptions(BaseOptions, ExtractAllScriptsOptions):
    """Options to flatten a YAML-LD document."""

    expand_context: JsonLdRecord | None = None
    """A context to expand with."""

    compact_arrays: bool = True
    """Compact arrays to single values when appropriate?"""


@validate_call(config=dict(arbitrary_types_allowed=True))
def flatten(
    document: JsonLdInput,
    ctx: JsonLdRecord | None = None,
    options: FlattenOptions = FlattenOptions(),  # type: ignore
) -> JsonLdRecord:
    """Flatten a document."""
    with except_json_ld_errors():
        return jsonld.flatten(
            input_=str(document),
            ctx=ctx,
            options=options.model_dump(by_alias=True),
        )
