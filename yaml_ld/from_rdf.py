from pydantic import validate_call
from pyld import jsonld

from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import DEFAULT_VALIDATE_CALL_CONFIG, JsonLdRecord
from yaml_ld.options import BaseOptions


class FromRDFOptions(BaseOptions):   # type: ignore
    """Options for converting RDF to ＊-LD."""

    format: str = 'application/n-quads'
    """The format if input is a string: 'application/n-quads' for N-Quads."""

    use_rdf_type: bool = False
    """True to use `rdf:type`, False to use `@type`."""

    use_native_types: bool = False
    """Convert XSD types into native types (boolean, integer, double)?"""


DEFAULT_FROM_RDF_OPTIONS = FromRDFOptions()


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def from_rdf(
    dataset: str,
    options: FromRDFOptions = DEFAULT_FROM_RDF_OPTIONS,
) -> JsonLdRecord:
    """Convert a RDF dataset to a [＊-LD](/blog/any-ld/) document."""
    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)

    with except_json_ld_errors():
        return jsonld.from_rdf(dataset, dict_options)
