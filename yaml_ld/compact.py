from typing import Annotated

from pydantic import Field
from pyld import jsonld

from yaml_ld.annotations import specified_by, API
from yaml_ld.parse import parse  # noqa: WPS347
from yaml_ld.errors import MappingKeyError, CycleDetected
from yaml_ld.models import (
    Document, ProcessingMode, DocumentLoader, BaseOptions, ExtractAllScripts,
)


class CompactOptions(BaseOptions):
    """Options structure for `jsonld.compact()`."""

    compact_arrays: bool = Field(default=True, alias='compactArrays')
    graph: bool = False
    expand_context: Document | None = Field(default=None, alias='expandContext')
    skip_expansion: bool = Field(default=False, alias='skipExpansion')


@specified_by(API / '#dom-jsonldprocessor-compact')
def compact(  # noqa: WPS211
    document: str | bytes | Document,
    context: Annotated[Document | None, 'Context to compact with.'],
    base: Annotated[str | None, 'The base URL to use.'],
    compact_arrays: Annotated[
        bool,
        'Compact arrays to single values when appropriate?',
    ] = True,
    graph: Annotated[
        bool,
        'Always output a top-level graph.',
    ] = False,
    extract_all_scripts: ExtractAllScripts = False,
    mode: ProcessingMode = ProcessingMode.JSON_LD_1_1,
    document_loader: DocumentLoader | None = None,
    expand_context: Annotated[
        Document | None,
        'Context to expand the input with.',
    ] = None,
    skip_expansion: Annotated[
        bool,
        'Treat the input as already expanded, and do not expand it again.',
    ] = False,
):
    """Compact a JSON-LD document."""
    if isinstance(document, (str, bytes)):
        document = parse(document)

    options = CompactOptions(
        base=base,
        extract_all_scripts=extract_all_scripts,
        mode=mode,
        document_loader=document_loader,
        compact_arrays=compact_arrays,
        graph=graph,
        expand_context=expand_context,
        skip_expansion=skip_expansion,
    ).model_dump(
        exclude_defaults=True,
        by_alias=True,
    )

    try:
        return jsonld.compact(
            input_=document,
            ctx=context,
            options=options,
        )
    except TypeError as err:
        raise MappingKeyError() from err
    except RecursionError as err:
        raise CycleDetected() from err
