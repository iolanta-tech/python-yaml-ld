from typing import TypedDict, Literal

TermType = Literal['IRI', 'blank node', 'literal']


class Term(TypedDict):
    """RDF Term."""

    type: TermType
    value: str
    datatype: str | None


class Triple(TypedDict):
    """RDF Triple."""

    subject: Term
    predicate: Term
    object: Term


Graph = list[Triple]
Dataset = dict[str, Graph]
