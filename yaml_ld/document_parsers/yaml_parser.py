import io

import more_itertools
from typing import Any

import yaml
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from yaml_ld.document_parsers.base import BaseDocumentParser
from yaml_ld.errors import LoadingDocumentFailed, DocumentIsScalar
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import Document


class YAMLDocumentParser(BaseDocumentParser):
    def __call__(self, data: io.TextIOBase, source: str, options: dict[str, Any]) -> Document:

        from yaml_ld.errors import MappingKeyError

        try:
            content = data.read()
        except UnicodeDecodeError as unicode_decode_error:
            from yaml_ld.errors import InvalidEncoding
            raise InvalidEncoding() from unicode_decode_error

        try:
            yaml_documents_stream = yaml.load_all(  # noqa: S506
                stream=content,
                Loader=YAMLLDLoader,
            )

            if options.get('extractAllScripts'):
                yaml_document = list(yaml_documents_stream)
            else:
                yaml_document = more_itertools.first(yaml_documents_stream)
        except ConstructorError as err:
            if err.problem == 'found unhashable key':
                raise MappingKeyError() from err

            raise

        except ScannerError as err:
            raise LoadingDocumentFailed(path=...) from err

        except ComposerError as err:
            from yaml_ld.errors import UndefinedAliasFound
            raise UndefinedAliasFound() from err

        except ParserError as err:
            from yaml_ld.errors import InvalidScriptElement
            raise InvalidScriptElement() from err

        if not isinstance(yaml_document, (dict, list)):
            raise DocumentIsScalar(yaml_document)

        return yaml_document
