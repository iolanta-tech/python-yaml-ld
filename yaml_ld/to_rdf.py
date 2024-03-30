from pathlib import Path
from typing import Annotated

from pyld import jsonld
from urlpath import URL

import yaml_ld
from yaml_ld.annotations import Help
from yaml_ld.models import (
    Document, DocumentLoader, ExtractAllScripts,
    SerializedDocument,
)
from yaml_ld.rdf import Dataset


def to_rdf(
    document: SerializedDocument | Document,
    base: Annotated[str | None, Help('The base IRI to use.')] = None,
    extract_all_scripts: ExtractAllScripts = False,
    document_loader: DocumentLoader | None = None,
) -> Dataset:
    """Convert a YAML-LD document to RDF."""
    expanded_document = yaml_ld.expand(
        document=document,
        document_loader=document_loader,
        extract_all_scripts=extract_all_scripts,
    )

    return jsonld.to_rdf(
        expanded_document,
    )
