from pathlib import Path
from typing import Annotated

from pydantic import Field
from pyld import jsonld

from yaml_ld.annotations import Help
from yaml_ld.errors import CycleDetected, MappingKeyError
from yaml_ld.models import (
    Document, ProcessingMode,
    DocumentLoader, BaseOptions, ExtractAllScripts,
)
from yaml_ld.parse import parse  # noqa: WPS347


class ExpandOptions(BaseOptions):
    """Options for `jsonld.expand()`."""

    context: Document | None = Field(default=None, alias='expandContext')


def expand(   # noqa: C901, WPS211
    document: str | bytes | Document | Path,
    base: Annotated[str | None, Help('The base IRI to use.')] = None,
    context: Annotated[
        Document | None,
        Help('A context to expand with.'),
    ] = None,
    extract_all_scripts: ExtractAllScripts = False,
    mode: ProcessingMode = ProcessingMode.JSON_LD_1_1,
    document_loader: DocumentLoader | None = None,
):
    """Expand a YAML-LD document."""
    if isinstance(document, (str, bytes, Path)):
        if isinstance(document, Path) and base is None:
            base = f'file://{document.parent}/'

        document = parse(document)

    options = ExpandOptions(
        base=base,
        context=context,
        extract_all_scripts=extract_all_scripts,
        mode=mode,
        document_loader=document_loader,
    ).model_dump(
        exclude_defaults=True,
        by_alias=True,
    )

    try:
        return jsonld.expand(
            input_=document,
            options=options,
        )
    except TypeError as err:
        raise MappingKeyError() from err
    except RecursionError as err:
        raise CycleDetected() from err
