from typing import Annotated

from pydantic import validate_call
from pyld import jsonld

from yaml_ld.annotations import API
from yaml_ld.models import BaseOptions, Document
from yaml_ld.rdf import Dataset, Graph


class FromRDFOptions(BaseOptions):
    ...


@validate_call(config=dict(arbitrary_types_allowed=True))
def from_rdf(
    dataset: Dataset,
    options: FromRDFOptions = FromRDFOptions(),
) -> Annotated[Document, API / '#dom-jsonldprocessor-fromrdf']:
    """Convert a RDF dataset to a YAML-LD document."""
    return jsonld.from_rdf(dataset, options.model_dump(by_alias=True))
