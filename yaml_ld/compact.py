from typing import Annotated

from pydantic import validate_call
from pyld import jsonld

from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    BaseOptions,
    ExtractAllScriptsOptions,
    JsonLdInput,
    JsonLdRecord,
)


class CompactOptions(BaseOptions, ExtractAllScriptsOptions):
    """Options to compact a YAML-LD document."""

    compact_arrays: bool = True
    """Compact arrays to single values when appropriate?"""

    graph: bool = False
    """True to always output a top-level graph."""

    expand_context: JsonLdRecord | None = None
    """A context to expand with."""

    skip_expansion: bool = False
    """True to skip the expansion process, False to include it."""


@validate_call(config=dict(arbitrary_types_allowed=True))
def compact(  # noqa: WPS211
    document: JsonLdInput,
    ctx: Annotated[JsonLdRecord | None, 'Context to compact with.'],
    options: CompactOptions = CompactOptions(),
) -> JsonLdRecord | list[JsonLdRecord]:
    """Compact a JSON-LD document."""
    with except_json_ld_errors():
        return jsonld.compact(
            input_=str(document),
            ctx=ctx,
            options=options.model_dump(by_alias=True),
        )
