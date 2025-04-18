import functools
from dataclasses import dataclass
from pathlib import Path

from documented import DocumentedError
from yarl import URL

from yaml_ld.document_parsers.base import BaseDocumentParser
from yaml_ld.document_parsers.rdf_xml_parser import RDFXMLParser
from yaml_ld.document_parsers.turtle_parser import TurtleParser
from yaml_ld.document_parsers.yaml_parser import YAMLDocumentParser
from yaml_ld.models import URI

# FIXME
#   - I've copied it over from pyld;
#   - It is hard-coded, I think I should handle it dynamically depending on
#     whatever parsers are available.
DEFAULT_ACCEPT_HEADER = ', '.join([
    'application/ld+json',
    'application/rdf+xml;q=0.8',
    'application/json;q=0.5',
    'text/html;q=0.8',
    'application/xhtml+xml;q=0.8',
])


def construct_accept_header(url: URI) -> str:
    """Construct headers for a URL."""
    match url:
        case URL() as url:
            url = str(url)

        case Path():
            return DEFAULT_ACCEPT_HEADER

    # FIXME: Use JsonLdInput as argument instead of URI type

    # FIXME:
    #    * Make this configurable and extendable
    #    * Maybe move this to pyld, test URL:
    #    ```
    #    https://w3id.org/fair/fip/terms/Knowledge-representation-language
    #    ```
    if url.startswith('https://w3id.org/fair/fip/terms/'):
        # Content negotiation will not work correctly because w3id does not
        # support content type weights. It will return the text/html version.
        return 'application/ld+json'

    return DEFAULT_ACCEPT_HEADER


def by_extension(extension: str) -> str | None:
    """
    Determine a content type by file extension.

    FIXME this is hard coded, we have to generalize.
    """
    return {
        '.json': 'application/json',
        '.jsonld': 'application/ld+json',
        '.jldt': 'application/ld+json',
        '.jldte': 'application/ld+json',
        '.yaml': 'application/yaml',
        '.yamlld': 'application/ld+yaml',
        '.html': 'text/html',
        '.ttl': 'text/turtle',
    }.get(extension)


@functools.cache
def parser_by_content_type_map():
    """
    Map content types to parsers.

    FIXME: Make this dynamic; perhaps a plugin entry point even.
    """
    # This prevents a cyclic import problem.
    from yaml_ld.document_parsers.html_parser import (  # noqa: WPS433
        HTMLDocumentParser,
    )

    return {
        'application/json': YAMLDocumentParser,
        'application/ld+json': YAMLDocumentParser,
        'application/yaml': YAMLDocumentParser,
        'application/x-yaml': YAMLDocumentParser,
        'application/ld+yaml': YAMLDocumentParser,
        'text/html': HTMLDocumentParser,
        'application/rdf+xml': RDFXMLParser,
        'text/turtle': TurtleParser,
    }


@dataclass
class ParserNotFound(DocumentedError):   # type: ignore
    """
    Cannot find a parser for `{self.content_type}` content type.

    Document: {self.uri}
    """

    content_type: str
    uri: str


def parser_by_content_type(
    content_type: str,
    uri: str,
) -> BaseDocumentParser:
    """Find a parser based on content type."""
    # Here, we ignore suffixes like:
    # - `charset=utf8`
    # - `qs=0.9`
    # - …
    content_type, *_parameters = content_type.split(  # noqa: WPS110, WPS472
        ';',
        maxsplit=1,
    )

    try:
        return parser_by_content_type_map()[content_type]()
    except KeyError:
        raise ParserNotFound(content_type=content_type, uri=uri)
