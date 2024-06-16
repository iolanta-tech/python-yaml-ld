from pydantic import validate_call
from pyld import jsonld

import yaml_ld
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import (
    Document, SerializedDocument, BaseOptions, ExtractAllScriptsOptions,
)
from yaml_ld.rdf import Dataset


class ToRDFOptions(BaseOptions, ExtractAllScriptsOptions):
    """Options for converting YAML-LD to RDF."""

    format: str = 'application/n-quads'
    """The format to use to output a string: 'application/n-quads'
    for N-Quads."""

    produce_generalized_rdf: bool = False
    """True to output generalized RDF, false to produce only standard RDF."""

    rdf_direction: str = 'i18n-datatype'
    """Only 'i18n-datatype' supported."""


@validate_call(config=dict(arbitrary_types_allowed=True))
def to_rdf(
    document: SerializedDocument | Document,
    options: ToRDFOptions = ToRDFOptions(),
) -> Dataset:
    """Convert a YAML-LD document to RDF."""
    with except_json_ld_errors():
        return jsonld.to_rdf(
            document,
            options=options.model_dump(
                by_alias=True,
                exclude_defaults=True,
            ),
        )
