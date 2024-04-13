from pathlib import Path
from typing import Annotated

from pydantic import Field
from pyld import jsonld
from urlpath import URL

from yaml_ld.annotations import Help, specified_by, API
from yaml_ld.errors import (
    CycleDetected, MappingKeyError,
    LoadingRemoteContextFailed, YAMLLDError, PyLDError,
)
from yaml_ld.models import (
    Document, ProcessingMode,
    DocumentLoader, BaseOptions, ExtractAllScripts, SerializedDocument,
)
from yaml_ld.parse import parse  # noqa: WPS347


class ExpandOptions(BaseOptions):
    """Options for `jsonld.expand()`."""

    context: Document | None = Field(default=None, alias='expandContext')


@specified_by(API / '#dom-jsonldprocessor-expand')
def expand(   # noqa: C901, WPS211
    document: SerializedDocument | Document,
    base: Annotated[str | None, Help('The base IRI to use.')] = None,
    context: Annotated[
        Document | None,
        Help('A context to expand with.'),
    ] = None,
    extract_all_scripts: ExtractAllScripts = False,
    mode: ProcessingMode = ProcessingMode.JSON_LD_1_1,
    document_loader: DocumentLoader | None = None,
) -> Document | list[Document]:
    """Expand a YAML-LD document."""
    if isinstance(document, (str, bytes, Path, URL)):
        if isinstance(document, Path) and base is None:
            base = f'file://{document.parent}/'

        document = parse(document, extract_all_scripts=extract_all_scripts)

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
    except jsonld.JsonLdError as err:
        match err.code:
            case LoadingRemoteContextFailed.code:
                raise LoadingRemoteContextFailed(
                    context=err.details['url'],
                    reason=str(err.details['cause']),
                ) from err

            case _:
                raise PyLDError(
                    message=str(err),
                    code=err.code,
                ) from err
