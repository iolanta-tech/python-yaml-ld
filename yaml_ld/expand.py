import contextlib
from json import JSONDecodeError

from pydantic import validate_call
from pyld import jsonld

from yaml_ld.document_loaders.content_types import DEFAULT_ACCEPT_HEADER
from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
from yaml_ld.errors import (
    CycleDetected,
    InvalidJSONLiteral,
    InvalidScriptElement,
    LoadingRemoteContextFailed,
    MappingKeyError,
    PyLDError,
)
from yaml_ld.models import (
    DEFAULT_VALIDATE_CALL_CONFIG,
    JsonLdInput,
    JsonLdRecord,
    ensure_string_or_document,
)
from yaml_ld.options import (
    BaseOptions,
    ExpandContextOptions,
    ExtractAllScriptsOptions,
)


class ExpandOptions(   # type: ignore
    BaseOptions,
    ExtractAllScriptsOptions,
    ExpandContextOptions,
):
    """Options for `jsonld.expand()`."""


DEFAULT_EXPAND_OPTIONS = ExpandOptions()


def except_json_ld_error(err: jsonld.JsonLdError):
    """Handle JsonLdError."""
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


@contextlib.contextmanager
def except_json_ld_errors():   # noqa: WPS238, C901
    """Convert pyld errors to typed YAML-LD exceptions."""
    try:  # noqa: WPS225
        yield
    except TypeError as err:
        if 'not supported between instances of ' in str(err):
            raise MappingKeyError() from err

        raise
    except RecursionError as err:
        raise CycleDetected() from err
    except JSONDecodeError as err:
        raise InvalidScriptElement() from err
    except jsonld.JsonLdError as err:
        except_json_ld_error(err)


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def expand(   # noqa: C901, WPS211
    document: JsonLdInput,
    options: ExpandOptions = DEFAULT_EXPAND_OPTIONS,
) -> list[JsonLdRecord]:
    """
    Expand a [＊-LD](/blog/any-ld/) document.

    Converts all compact IRIs, keywords, and terms into their absolute IRI
    representations.
    """
    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)
    dict_options.setdefault('headers', {'Accept': DEFAULT_ACCEPT_HEADER})

    with except_json_ld_errors():
        jsonld._resolved_context_cache = jsonld.LRUCache(   # noqa: WPS437
            maxsize=jsonld.RESOLVED_CONTEXT_CACHE_MAX_SIZE,
        )
        return jsonld.expand(
            input_=ensure_string_or_document(document),
            options=dict_options,
        )
