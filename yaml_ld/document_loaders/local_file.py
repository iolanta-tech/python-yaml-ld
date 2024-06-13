from pathlib import Path
from typing import Any

import yaml
from pyld.jsonld import load_html
from urlpath import URL
from yaml.constructor import ConstructorError

from yaml_ld.document_loaders.base import DocumentLoader, PyLDResponse
from yaml_ld.loader import YAMLLDLoader


class LocalFileDocumentLoader(DocumentLoader):
    def __call__(self, source: str, options: dict[str, Any]) -> PyLDResponse:
        path = Path(URL(source).path)

        if path.suffix in {'.yaml', '.yml', '.yamlld', '.json', '.jsonld'}:
            with path.open() as f:
                from yaml_ld.errors import MappingKeyError

                try:
                    yaml_document = yaml.load(  # noqa: S506
                        stream=f.read(),
                        Loader=YAMLLDLoader,
                    )
                except ConstructorError as err:
                    if err.problem == 'found unhashable key':
                        raise MappingKeyError() from err

                    raise

                if not isinstance(yaml_document, (dict, list)):
                    from yaml_ld.errors import DocumentIsScalar
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
                )

            return {
                'document': loaded_html,
                'documentUrl': source,
                'contextUrl': None,
                'contentType': 'application/ld+yaml',
            }

        from yaml_ld.errors import LoadingDocumentFailed
        raise LoadingDocumentFailed()
