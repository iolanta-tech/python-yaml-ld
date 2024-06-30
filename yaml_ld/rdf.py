from typing import Literal

from typing_extensions import TypedDict

TermType = Literal['IRI', 'blank node', 'literal']


class IRITerm(TypedDict):
    """RDF Term."""

    type: Literal['IRI']
    value: str   # noqa: WPS110


class BlankTerm(TypedDict):
    """RDF Term."""

    type: Literal['blank node']
    value: str   # noqa: WPS110


class LiteralTerm(TypedDict):
    """RDF Term."""

    type: Literal['literal']
    value: str   # noqa: WPS110
    datatype: str | None


Term = IRITerm | BlankTerm | LiteralTerm


class Triple(TypedDict):
    """RDF Triple."""

    subject: Term
    predicate: Term
    object: Term


Graph = list[Triple]
Dataset = dict[str, Graph]
