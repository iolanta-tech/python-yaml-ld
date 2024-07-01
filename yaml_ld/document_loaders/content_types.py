from yaml_ld.document_parsers.base import BaseDocumentParser
from yaml_ld.document_parsers.html_parser import HTMLDocumentParser
from yaml_ld.document_parsers.yaml_parser import YAMLDocumentParser


def by_extension(extension: str) -> str | None:
    return {
        '.json': 'application/json',
        '.jsonld': 'application/ld+json',
        '.yaml': 'application/yaml',
        '.yamlld': 'application/ld+yaml',
        '.html': 'text/html',
    }.get(extension)


def parser_by_content_type(content_type: str) -> BaseDocumentParser:
    return {
        'application/json': YAMLDocumentParser,
        'application/ld+json': YAMLDocumentParser,
        'application/yaml': YAMLDocumentParser,
        'application/ld+yaml': YAMLDocumentParser,
        'text/html': HTMLDocumentParser,
    }[content_type]()
