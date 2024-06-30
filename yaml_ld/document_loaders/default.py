import functools

from yaml_ld.document_loaders.choice_by_scheme import (
    ChoiceBySchemeDocumentLoader,
)
from yaml_ld.document_loaders.http import HTTPDocumentLoader
from yaml_ld.document_loaders.local_file import LocalFileDocumentLoader

DEFAULT_DOCUMENT_LOADER = ChoiceBySchemeDocumentLoader(
    file=LocalFileDocumentLoader(),
    http=HTTPDocumentLoader(),
    https=HTTPDocumentLoader(),
)
