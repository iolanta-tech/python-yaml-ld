from pathlib import Path
from typing import Annotated

from pydantic import validate_call
from pyld import jsonld
from urlpath import URL

import yaml_ld
from yaml_ld.annotations import Help
from yaml_ld.expand import ExpandOptions, except_json_ld_errors
from yaml_ld.models import (
    Document, DocumentLoader, ExtractAllScripts,
    SerializedDocument, BaseOptions,
)
from yaml_ld.rdf import Dataset


class ToRDFOptions(BaseOptions):
    ...


@validate_call(config=dict(arbitrary_types_allowed=True))
def to_rdf(
    document: SerializedDocument | Document,
    options: ToRDFOptions = ToRDFOptions(),
) -> Dataset:
    """Convert a YAML-LD document to RDF."""
    parsed_document = yaml_ld.parse(
        raw_document=document,
        extract_all_scripts=options.extract_all_scripts,
    )

    with except_json_ld_errors():
        return jsonld.to_rdf(parsed_document)
