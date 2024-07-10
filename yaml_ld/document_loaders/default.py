from yaml_ld.document_loaders.choice_by_scheme import (
    ChoiceBySchemeDocumentLoader,
)
from yaml_ld.document_loaders.http import (
    HTTPCachedDocumentLoader,
)
from yaml_ld.document_loaders.local_file import LocalFileDocumentLoader

http_loader = HTTPCachedDocumentLoader()

DEFAULT_DOCUMENT_LOADER = ChoiceBySchemeDocumentLoader(
    file=LocalFileDocumentLoader(),
    http=http_loader,
    https=http_loader,
)
