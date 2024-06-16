from pathlib import Path
from typing import Any

import more_itertools
import yaml
from urlpath import URL
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.parser import ParserError

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse
from yaml_ld.load_html import load_html
from yaml_ld.loader import YAMLLDLoader


class HTTPDocumentLoader(DocumentLoader):
    def _parse_script_content(self, content: str):
        return list(
            yaml.load_all(
                content,
                Loader=YAMLLDLoader,
            ),
        )

    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        from yaml_ld.errors import LoadingDocumentFailed, DocumentIsScalar

        url = URL(source)

        if url.suffix in {'.yaml', '.yml', '.yamlld', '.json', '.jsonld'}:
            content = url.get().text

            from yaml_ld.errors import MappingKeyError

            from yaml.scanner import ScannerError
            try:
                yaml_document = more_itertools.first(
                    yaml.load_all(  # noqa: S506
                        stream=content,
                        Loader=YAMLLDLoader,
                    ),
                )
            except ConstructorError as err:
                if err.problem == 'found unhashable key':
                    raise MappingKeyError() from err

                raise

            except ScannerError as err:
                raise LoadingDocumentFailed(path=url) from err

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

        if url.suffix in {'.html', '.xhtml'}:
            content = url.get().text

            loaded_html = load_html(
                input=content.read(),
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

        raise LoadingDocumentFailed(path=url)
