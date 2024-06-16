import functools
from pathlib import Path
from typing import Any

import yaml
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader


class LocalFileDocumentLoader(DocumentLoader):
    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import LoadingDocumentFailed, DocumentIsScalar

        path = Path(URL(source).path)

        if path.suffix in {'.yaml', '.yml', '.yamlld', '.json', '.jsonld'}:
            with path.open() as f:
                from yaml_ld.errors import MappingKeyError

                from yaml.scanner import ScannerError
                try:
                    yaml_document = yaml.load(  # noqa: S506
                        stream=f.read(),
                        Loader=YAMLLDLoader,
                    )
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

        if path.suffix in {'.html', '.xhtml'}:
            with path.open() as f:
                loaded_html = load_html(
                    input=f.read(),
                    url=source,
                    profile=None,
                    options=options,
                    parse_script_content=functools.partial(
                        yaml.load,
                        Loader=YAMLLDLoader,
                    ),
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
