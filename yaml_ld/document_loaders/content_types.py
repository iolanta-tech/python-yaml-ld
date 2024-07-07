from dataclasses import dataclass

from documented import DocumentedError

from yaml_ld.document_parsers.base import BaseDocumentParser
from yaml_ld.document_parsers.html_parser import HTMLDocumentParser
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


PARSER_BY_CONTENT_TYPE = {
    'application/json': YAMLDocumentParser,
    'application/ld+json': YAMLDocumentParser,
    'application/yaml': YAMLDocumentParser,
    'application/ld+yaml': YAMLDocumentParser,
    'text/html': HTMLDocumentParser,
}


@dataclass
class ParserNotFound(DocumentedError):   # type: ignore
    """Cannot find a parser for `{self.content_type}` content type."""

    content_type: str


def parser_by_content_type(content_type: str) -> BaseDocumentParser:
    """Find a parser based on content type."""
    try:
        return PARSER_BY_CONTENT_TYPE[content_type]()
    except KeyError:
        raise ParserNotFound(content_type)
