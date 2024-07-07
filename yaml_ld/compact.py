from typing import Annotated

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


class CompactOptions(   # type: ignore
    BaseOptions,
    ExtractAllScriptsOptions,
    ExpandContextOptions,
):
    """Options to compact a YAML-LD document."""

    compact_arrays: bool = True
    """Compact arrays to single values when appropriate?"""

    graph: bool = False
    """True to always output a top-level graph."""

    skip_expansion: bool = False
    """True to skip the expansion process, False to include it."""


DEFAULT_COMPACT_OPTIONS = CompactOptions()   # type: ignore


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def compact(  # noqa: WPS211
    document: JsonLdInput,
    ctx: Annotated[JsonLdContext | None, 'Context to compact with.'],
    options: CompactOptions = DEFAULT_COMPACT_OPTIONS,
) -> JsonLdRecord | list[JsonLdRecord]:
    """Compact a JSON-LD document."""
    with except_json_ld_errors():
        return jsonld.compact(
            input_=str(document),
            ctx=ctx,
            options=options.model_dump(by_alias=True),
        )
