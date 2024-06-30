from pathlib import Path
from typing import Any

import more_itertools
import yaml
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader


class LocalFileDocumentLoader(DocumentLoader):
    def _parse_script_content(self, content: str):
        return list(
            yaml.load_all(
                content,
                Loader=YAMLLDLoader,
            ),
        )

    def __call__(self, source: str | Path, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import DocumentIsScalar, LoadingDocumentFailed

        path = Path(URL(source).path)

        if path.suffix in {'.yaml', '.yml', '.yamlld', '.json', '.jsonld'}:
            try:
                with path.open() as f:
                    from yaml_ld.errors import MappingKeyError

                    try:
                        stream = f.read()
                    except UnicodeDecodeError as unicode_decode_error:
                        from yaml_ld.errors import InvalidEncoding
                        raise InvalidEncoding()

                    try:
                        yaml_documents_stream = yaml.load_all(  # noqa: S506
                            stream=stream,
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
                        raise LoadingDocumentFailed(path=path) from err

                    except ComposerError as err:
                        from yaml_ld.errors import UndefinedAliasFound
                        raise UndefinedAliasFound() from err

                    except ParserError as err:
                        from yaml_ld.errors import InvalidScriptElement
                        raise InvalidScriptElement() from err

                    if not isinstance(yaml_document, (dict, list)):
                        raise DocumentIsScalar(yaml_document)

                    return {
                        'document': yaml_document,
                        'documentUrl': source,
                        'contextUrl': None,
                        'contentType': 'application/ld+yaml',
                    }
            except FileNotFoundError as file_not_found:
                from yaml_ld.errors import NotFound
                raise NotFound(path) from file_not_found

        if path.suffix in {'.html', '.xhtml'}:
            with path.open() as f:
                loaded_html = load_html(
                    input=f.read(),
                    url=source,
                    profile=None,
                    options=options,
                    content_type='application/ld+yaml',
                    parse_script_content=self._parse_script_content,
                )

                if isinstance(loaded_html, str):
                    raise DocumentIsScalar(loaded_html)

            return {
                'document': loaded_html,
                'documentUrl': source,
                'contextUrl': None,
                'contentType': 'application/ld+yaml',
            }

        raise LoadingDocumentFailed(path=path)
