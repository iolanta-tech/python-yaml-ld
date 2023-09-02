from typing import Annotated, Any

from pyld import jsonld

from yaml_ld.annotations import Help
from yaml_ld.models import Document, ProcessingMode, ExpandOptions


def expand(
    document: str | Document,
    base: Annotated[str | None, Help('The base IRI to use.')] = None,
    context: Annotated[
        Document | None,
        Help('A context to expand with.'),
    ] = None,
    extract_all_scripts: Annotated[
        bool,
        Help(
            'True to extract all JSON-LD script elements from HTML, '
            'False to extract just the first.'
        ),
    ] = False,
    mode: ProcessingMode = ProcessingMode.JSON_LD_1_1,
    document_loader: Any = None,
):
    return jsonld.expand(
        input_=document,
        options=ExpandOptions(
            base=base,
            context=context,
            extract_all_scripts=extract_all_scripts,
            mode=mode,
            document_loader=document_loader,
        ).model_dump(
            exclude_defaults=True,
            by_alias=True,
        ),
    )
