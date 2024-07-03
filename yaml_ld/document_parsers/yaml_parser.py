import io
from typing import Any

import more_itertools
import yaml
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from yaml_ld.document_parsers.base import (
    BaseDocumentParser,
    DocumentLoaderOptions,
)
from yaml_ld.errors import (
    DocumentIsScalar,
    InvalidEncoding,
    LoadingDocumentFailed,
    MappingKeyError,
)
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import JsonLdRecord


class YAMLDocumentParser(BaseDocumentParser):
    def __call__(
        self,
        data_stream: io.TextIOBase,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:

        try:
            yaml_documents_stream = yaml.load_all(  # noqa: S506
                stream=data_stream,
                Loader=YAMLLDLoader,
            )

            try:
                if options.get('extractAllScripts'):
                    yaml_document = list(yaml_documents_stream)
                else:
                    try:
                        yaml_document = more_itertools.first(yaml_documents_stream)
                    except ValueError as empty_iterable:
                        if 'first() was called on an empty iterable' in str(empty_iterable):
                            raise LoadingDocumentFailed(
                                path=source,
                            ) from empty_iterable

                        raise
            except UnicodeDecodeError as unicode_decode_error:
                raise InvalidEncoding() from unicode_decode_error
        except ConstructorError as err:
            if err.problem == 'found unhashable key':
                raise MappingKeyError() from err

            raise

        except ScannerError as err:
            raise LoadingDocumentFailed(path=source) from err

        except ComposerError as err:
            from yaml_ld.errors import UndefinedAliasFound
            raise UndefinedAliasFound() from err

        except ParserError as err:
            from yaml_ld.errors import InvalidScriptElement
            raise InvalidScriptElement() from err

        if not isinstance(yaml_document, (dict, list)):
            raise DocumentIsScalar(yaml_document)

        return yaml_document
