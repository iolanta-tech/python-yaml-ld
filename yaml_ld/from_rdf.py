from pydantic import validate_call
from pyld import jsonld

from yaml_ld.models import BaseOptions, Document
from yaml_ld.rdf import Dataset


class FromRDFOptions(BaseOptions):
    """Options for converting RDF to YAML-LD."""

    format: str = 'application/n-quads'
    """The format if input is a string: 'application/n-quads' for N-Quads."""

    use_rdf_type: bool = False
    """True to use `rdf:type`, False to use `@type`."""

    use_native_types: bool = False
    """Convert XSD types into native types (boolean, integer, double)?"""


@validate_call(config=dict(arbitrary_types_allowed=True))
def from_rdf(
    dataset: str,
    options: FromRDFOptions = FromRDFOptions(),
) -> Document:
    """Convert a RDF dataset to a YAML-LD document."""
    return jsonld.from_rdf(dataset, options.model_dump(by_alias=True))
