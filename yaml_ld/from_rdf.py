from pydantic import validate_call
from pyld import jsonld

from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import BaseOptions, JsonLdRecord


class FromRDFOptions(BaseOptions):   # type: ignore
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
    options: FromRDFOptions = FromRDFOptions(),  # type: ignore
) -> JsonLdRecord:
    """Convert a RDF dataset to a YAML-LD document."""
    with except_json_ld_errors():
        return jsonld.from_rdf(dataset, options.model_dump(by_alias=True))
