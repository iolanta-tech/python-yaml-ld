from typing import Annotated

from pydantic import Field, validate_call
from pyld import jsonld

from yaml_ld.annotations import API
from yaml_ld.errors import MappingKeyError, CycleDetected
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    Document, ProcessingMode, DocumentLoader, BaseOptions, ExtractAllScripts,
    SerializedDocument,
)
from yaml_ld.parse import parse  # noqa: WPS347


class CompactOptions(BaseOptions):
    """Options structure for `jsonld.compact()`."""

    compact_arrays: bool = Field(default=True, alias='compactArrays')
    graph: bool = False
    expand_context: Document | None = Field(default=None, alias='expandContext')
    skip_expansion: bool = Field(default=False, alias='skipExpansion')


@validate_call(config=dict(arbitrary_types_allowed=True))
def compact(  # noqa: WPS211
    document: SerializedDocument | Document,
    ctx: Annotated[Document | None, 'Context to compact with.'],
    options: CompactOptions = CompactOptions(),
) -> Annotated[Document | list[Document], API / '#dom-jsonldprocessor-compact']:
    """Compact a JSON-LD document."""
    if isinstance(document, (str, bytes)):
        document = parse(document)

    with except_json_ld_errors():
        return jsonld.compact(
            input_=document,
            ctx=ctx,
            options=options.model_dump(by_alias=True),
        )
