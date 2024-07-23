from typing import Annotated

from pydantic import validate_call
from pyld import jsonld

from yaml_ld.document_loaders.content_types import DEFAULT_ACCEPT_HEADER
from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    DEFAULT_VALIDATE_CALL_CONFIG,
    JsonLdContext,
    JsonLdInput,
    JsonLdRecord,
    ensure_string_or_document,
)
from yaml_ld.options import (
    BaseOptions,
    ExpandContextOptions,
    ExtractAllScriptsOptions,
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


DEFAULT_COMPACT_OPTIONS = CompactOptions()


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def compact(  # noqa: WPS211
    document: JsonLdInput,
    ctx: Annotated[JsonLdContext | None, 'Context to compact with.'] = None,
    options: CompactOptions = DEFAULT_COMPACT_OPTIONS,
) -> JsonLdRecord | list[JsonLdRecord]:
    """
    Compact a [＊-LD](/blog/any-ld/) document.

    Replace full IRIs with shorter terms and compact IRIs using a context,
    making the document more human-readable while preserving its original
    structure and semantics.
    """
    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)
    dict_options.setdefault('headers', {'Accept': DEFAULT_ACCEPT_HEADER})

    with except_json_ld_errors():
        return jsonld.compact(
            input_=ensure_string_or_document(document),
            ctx=ctx or {},
            options=dict_options,
        )
