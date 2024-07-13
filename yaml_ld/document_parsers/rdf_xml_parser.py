import io

from rdflib import Graph
from rdflib_pyld_compat import pyld_jsonld_from_rdflib_graph

from yaml_ld.document_parsers.base import (
    BaseDocumentParser,
    DocumentLoaderOptions,
)
from yaml_ld.models import JsonLdRecord


class RDFXMLParser(BaseDocumentParser):
    """Parse RDF/XML documents."""

    def __call__(   # noqa: WPS238, WPS231, WPS225, C901
        self,
        data_stream: io.BytesIO,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse YAML document stream into LD."""
        graph = Graph().parse(data_stream, format='xml')
        return pyld_jsonld_from_rdflib_graph(graph)
