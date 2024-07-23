import functools
from dataclasses import dataclass

from documented import DocumentedError

from yaml_ld.document_parsers.base import BaseDocumentParser
from yaml_ld.document_parsers.rdf_xml_parser import RDFXMLParser
from yaml_ld.document_parsers.yaml_parser import YAMLDocumentParser


def by_extension(extension: str) -> str | None:
    return {
        '.json': 'application/json',
        '.jsonld': 'application/ld+json',
        '.jldt': 'application/ld+json',
        '.jldte': 'application/ld+json',
        '.yaml': 'application/yaml',
        '.yamlld': 'application/ld+yaml',
        '.html': 'text/html',
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
        'application/ld+yaml': YAMLDocumentParser,
        'text/html': HTMLDocumentParser,
        'application/rdf+xml': RDFXMLParser,
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
        '; ',
        maxsplit=1,
    )

    try:
        return parser_by_content_type_map()[content_type]()
    except KeyError:
        raise ParserNotFound(content_type=content_type, uri=uri)
