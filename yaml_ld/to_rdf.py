from pydantic import validate_call
from pyld import jsonld

from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import DEFAULT_VALIDATE_CALL_CONFIG, JsonLdInput
from yaml_ld.options import BaseOptions, ExtractAllScriptsOptions
from yaml_ld.rdf import Dataset


class ToRDFOptions(BaseOptions, ExtractAllScriptsOptions):   # type: ignore
    """Options for converting ＊-LD to RDF."""

    format: str | None = None
    """The format to use to output a string: 'application/n-quads'
    for N-Quads."""

    produce_generalized_rdf: bool = False
    """True to output generalized RDF, false to produce only standard RDF."""

    rdf_direction: str = 'i18n-datatype'
    """Only 'i18n-datatype' supported."""


DEFAULT_TO_RDF_OPTIONS = ToRDFOptions()


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def to_rdf(
    document: JsonLdInput,
    options: ToRDFOptions = DEFAULT_TO_RDF_OPTIONS,
) -> Dataset | str:
    """Convert a [＊-LD](/blog/any-ld/) document to RDF."""
    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)

    with except_json_ld_errors():
        return jsonld.to_rdf(
            document,
            options=dict_options,
        )
