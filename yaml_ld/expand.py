from pathlib import Path
from typing import Annotated, TypedDict

from pydantic import Field, validate_call
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


class ExpandOptionsDict(TypedDict):
    context: Document | None
    base: str | None
    extract_all_scripts: ExtractAllScripts
    document_loader: DocumentLoader | None


@specified_by(API / '#dom-jsonldprocessor-expand')
@validate_call(config=dict(arbitrary_types_allowed=True))
def expand(   # noqa: C901, WPS211
    document: SerializedDocument | Document,
    options: ExpandOptions = ExpandOptions(),
) -> Document | list[Document]:
    """Expand a YAML-LD document."""
    if isinstance(document, (str, bytes, Path, URL)):
        if isinstance(document, Path) and options.base is None:
            options.base = f'file://{document.parent}/'

        document = parse(
            document,
            extract_all_scripts=options.extract_all_scripts,
        )

    try:
        return jsonld.expand(
            input_=document,
            options=options.model_dump(),
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
