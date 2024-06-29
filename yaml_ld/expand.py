import contextlib
from json import JSONDecodeError
from pathlib import Path

from pydantic import validate_call
from pyld import jsonld
from pyld.jsonld import load_html
from urlpath import URL

from yaml_ld.errors import (
    CycleDetected, MappingKeyError,
    LoadingRemoteContextFailed, PyLDError, InvalidScriptElement,
    InvalidJSONLiteral,
)
from yaml_ld.models import (
    Document, BaseOptions, SerializedDocument, ExtractAllScriptsOptions,
)
from yaml_ld.parse import parse  # noqa: WPS347


class ExpandOptions(BaseOptions, ExtractAllScriptsOptions):
    """Options for `jsonld.expand()`."""

    expand_context: Document | None = None
    """A context to expand with."""


@contextlib.contextmanager
def except_json_ld_errors():
    """Convert pyld errors to typed YAML-LD exceptions."""
    try:
        yield
    except TypeError as err:
        raise MappingKeyError() from err
    except RecursionError as err:
        raise CycleDetected() from err
    except JSONDecodeError as err:
        raise InvalidScriptElement() from err
    except jsonld.JsonLdError as err:
        # We need to drill down; for instance, `to_rdf()` raises an error which
        # contains an actual error from `expand()` in its `.cause` field.
        err = err.cause or err

        if isinstance(err, JSONDecodeError):
            raise InvalidJSONLiteral() from err

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


def construct_base_by_document(document: str) -> str | None:
    if isinstance(document, list | str):
        return None

    if isinstance(document, str):
        document = URL(document)

    if isinstance(document, URL):
        document = Path(document.path)

    if isinstance(document, Path):
        return f'file://{document.parent}/'


@validate_call(config=dict(arbitrary_types_allowed=True))
def expand(   # noqa: C901, WPS211
    document: SerializedDocument | Document,
    options: ExpandOptions = ExpandOptions(),
) -> Document | list[Document]:
    """Expand a YAML-LD document."""
    if not options.base:
        options.base = construct_base_by_document(document)

    with except_json_ld_errors():
        return jsonld.expand(
            input_=str(document) if (
                isinstance(document, (Path, URL))
            ) else document,
            options=options.model_dump(
                by_alias=True,
                # exclude_defaults=True,
            ),
        )
