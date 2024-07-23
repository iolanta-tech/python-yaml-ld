from pydantic import validate_call
from pyld import jsonld

from yaml_ld.document_loaders.content_types import DEFAULT_ACCEPT_HEADER
from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
from yaml_ld.models import DEFAULT_VALIDATE_CALL_CONFIG, RemoteDocument
from yaml_ld.options import BaseOptions

DEFAULT_BASE_OPTIONS = BaseOptions()


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def load_document(
    url,
    base=None,
    profile=None,
    requestProfile=None,
    options: BaseOptions = DEFAULT_BASE_OPTIONS,
) -> RemoteDocument:
    """
    Load an [＊-LD](blog/any-ld/) document.

    The document can be retrieved from local filesystem or from the Web.
    """
    headers = {
        'Accept': DEFAULT_ACCEPT_HEADER,
    }

    if requestProfile:
        headers['Accept'] = (
            f'application/ld+json;profile={requestProfile}, '
        ) + headers['Accept']

    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)
    dict_options.setdefault('headers', headers)

    return jsonld.load_document(
        url=str(url),
        options=dict_options,
        base=base,
        profile=profile,
        requestProfile=requestProfile,
    )
