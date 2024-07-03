import io

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
    MappingKeyError, InvalidScriptElement, UndefinedAliasFound,
)
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import JsonLdRecord


def _ensure_not_scalar(document) -> JsonLdRecord | list[JsonLdRecord]:
    if not isinstance(document, (dict, list)):
        raise DocumentIsScalar(document)

    return document


class YAMLDocumentParser(BaseDocumentParser):
    """Parse YAML documents."""

    def __call__(   # noqa: WPS238, WPS231, WPS225, C901
        self,
        data_stream: io.TextIOBase,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse YAML document stream into LD."""
        yaml_documents_stream = yaml.load_all(  # noqa: S506
            stream=data_stream,
            Loader=YAMLLDLoader,
        )

        try:   # noqa: WPS225
            return _ensure_not_scalar(
                self._yaml_document_from_stream(
                    stream=yaml_documents_stream,
                    extract_all_scripts=options.get('extractAllScripts', False),
                ),
            )

        except UnicodeDecodeError as unicode_decode_error:
            raise InvalidEncoding() from unicode_decode_error

        except ConstructorError as err:
            if err.problem == 'found unhashable key':
                raise MappingKeyError() from err

            raise

        except ScannerError as err:
            raise LoadingDocumentFailed(path=source) from err

        except ComposerError as err:
            raise UndefinedAliasFound() from err

        except ParserError as err:
            raise InvalidScriptElement() from err

    def _yaml_document_from_stream(self, stream, extract_all_scripts: bool):
        if extract_all_scripts:
            return list(stream)

        try:
            return next(stream)
        except StopIteration as stop_iteration:
            raise LoadingDocumentFailed(path='') from stop_iteration
