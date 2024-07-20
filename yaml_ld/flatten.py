from pydantic import validate_call
from pyld import jsonld

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


class FlattenOptions(   # type: ignore
    BaseOptions,
    ExtractAllScriptsOptions,
    ExpandContextOptions,
):
    """Options to flatten a YAML-LD document."""

    compact_arrays: bool = True
    """Compact arrays to single values when appropriate?"""


DEFAULT_FLATTEN_OPTIONS = FlattenOptions()


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def flatten(
    document: JsonLdInput,
    ctx: JsonLdContext | None = None,
    options: FlattenOptions = DEFAULT_FLATTEN_OPTIONS,
) -> JsonLdRecord:
    """
    Flatten a [＊-LD](/blog/any-ld/) document.

    Outputs a single array containing all nodes, making no assumptions about
    their relationships, to simplify data processing and ensure all referenced
    nodes are included.
    """
    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)

    with except_json_ld_errors():
        return jsonld.flatten(
            input_=ensure_string_or_document(document),
            ctx=ctx,
            options=dict_options,
        )
