import platformdirs
from requests_cache import CachedSession

from yaml_ld.document_loaders.choice_by_scheme import (
    ChoiceBySchemeDocumentLoader,
)
from yaml_ld.document_loaders.http import HTTPDocumentLoader
from yaml_ld.document_loaders.local_file import LocalFileDocumentLoader

CACHE_DIRECTORY = platformdirs.user_cache_dir(
    appname='python-yaml-ld',
    ensure_exists=True,
)

CACHED_SESSION = CachedSession(
    backend='filesystem',
    cache_name=CACHE_DIRECTORY,
)

http_loader = HTTPDocumentLoader(
    session=CACHED_SESSION,
)

DEFAULT_DOCUMENT_LOADER = ChoiceBySchemeDocumentLoader(
    file=LocalFileDocumentLoader(),
    http=http_loader,
    https=http_loader,
)
