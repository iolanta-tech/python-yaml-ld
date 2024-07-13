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
    """Cannot find a parser for `{self.content_type}` content type."""

    content_type: str


def parser_by_content_type(content_type: str) -> BaseDocumentParser:
    """Find a parser based on content type."""
    content_type = content_type.removesuffix('; charset=UTF-8')

    try:
        return parser_by_content_type_map()[content_type]()
    except KeyError:
        raise ParserNotFound(content_type)
