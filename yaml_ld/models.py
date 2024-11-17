from pathlib import Path
from typing import Any, Sequence

from pydantic import ConfigDict
from typing_extensions import TypedDict
from yarl import URL

JsonLdRecord = dict[str, Any]  # type: ignore


class RemoteDocument(TypedDict, total=False):
    """Specification of the remote document."""

    contentType: str
    contextUrl: str | None
    document: JsonLdRecord | list[JsonLdRecord]
    documentUrl: str
    profile: str | None


URI = str | URL | Path
"""
A Universal Resource Identifier can be represented as a `Path` or as a `URL`.

Or, it can be a `str`, and we will try to automatically identify what that is.
"""


JsonLdInput = (
    JsonLdRecord | Sequence[JsonLdRecord] | URI
)
"""
Input for `expand()`, `compact()` and other functions.

[Specification](https://w3c.github.io/json-ld-api/#dom-jsonldrecord)
"""

JsonLdContext = JsonLdRecord | list[JsonLdRecord | URI] | URI
"""
The `JsonLdContext` interface is used to refer to a value that may be a
`JsonLdRecord`, a sequence of `JsonLdRecord`-s, or a string representing an IRI,
which can be dereferenced to retrieve a valid JSON document.

[Specification](https://w3c.github.io/json-ld-api/#dom-jsonldcontext)
"""

DEFAULT_VALIDATE_CALL_CONFIG = ConfigDict(
    arbitrary_types_allowed=True,
    validate_default=False,
)


class Undefined:
    """Undefined."""


def ensure_string_or_document(
    input_: JsonLdInput,
) -> JsonLdRecord | Sequence[JsonLdRecord] | str | RemoteDocument:
    """Prepare `input_` for `pyld` functions."""
    if isinstance(input_, (URL, Path)):
        return str(input_)

    return input_
