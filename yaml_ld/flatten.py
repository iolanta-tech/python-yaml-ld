from typing import Annotated

from pydantic import validate_call
from pyld import jsonld

from yaml_ld import parse
from yaml_ld.annotations import API
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import Document, BaseOptions, SerializedDocument


class FlattenOptions(BaseOptions):
    """Options to flatten a YAML-LD document."""

    expand_context: Document | None = None
    """A context to expand with."""


@validate_call(config=dict(arbitrary_types_allowed=True))
def flatten(
    document: SerializedDocument | Document,
    ctx: Document | None = None,
    options: FlattenOptions = FlattenOptions(),
) -> Annotated[Document, API / '#dom-jsonldprocessor-flatten']:
    """Flatten a document."""
    if isinstance(document, (str, bytes)):
        document = parse(document)

    with except_json_ld_errors():
        return jsonld.flatten(
            input_=document,
            ctx=ctx,
            options=options.model_dump(by_alias=True),
        )
