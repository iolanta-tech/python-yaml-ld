from typing import Annotated

from pyld import jsonld

import yaml_ld
from yaml_ld.annotations import Help
from yaml_ld.expand import DocumentLoader
from yaml_ld.models import Document
from yaml_ld.rdf import Dataset


def to_rdf(
    document: str | bytes | Document,
    base: Annotated[str | None, Help('The base IRI to use.')] = None,
    document_loader: DocumentLoader | None = None,
) -> Dataset:
    """Convert a YAML-LD document to RDF."""
    expanded_document = yaml_ld.expand(
        document=document,
        document_loader=document_loader,
    )

    return jsonld.to_rdf(
        expanded_document,
    )
