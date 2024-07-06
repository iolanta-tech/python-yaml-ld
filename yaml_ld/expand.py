import contextlib
from json import JSONDecodeError
from pathlib import Path

from pydantic import validate_call
from pyld import jsonld
from urlpath import URL

from yaml_ld.errors import (
    CycleDetected,
    InvalidJSONLiteral,
    InvalidScriptElement,
    LoadingRemoteContextFailed,
    MappingKeyError,
    PyLDError,
)
from yaml_ld.models import (
    BaseOptions,
    ExtractAllScriptsOptions,
    JsonLdInput,
    JsonLdRecord, ExpandContextOptions,
)


class ExpandOptions(   # type: ignore
    BaseOptions,
    ExtractAllScriptsOptions,
    ExpandContextOptions,
):
    """Options for `jsonld.expand()`."""


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


@validate_call(config=dict(arbitrary_types_allowed=True))
def expand(   # noqa: C901, WPS211
    document: JsonLdInput,
    options: ExpandOptions = ExpandOptions(),  # type: ignore
) -> list[JsonLdRecord]:
    """Expand a YAML-LD document."""
    with except_json_ld_errors():
        return jsonld.expand(
            input_=str(document) if isinstance(document, (URL, Path)) else document,
            options=options.model_dump(
                by_alias=True,
                exclude_none=True,
            ),
        )
