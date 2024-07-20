from pydantic import validate_call
from pyld import jsonld

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
    # FIXME
    #   - I've copied it over from pyld;
    #   - It is hard-coded, I think I should handle it dynamically depending on
    #     whatever parsers are available.
    headers = {
        'Accept': (
            'application/ld+json, '
            'application/rdf+xml;q=0.8, '
            'application/json;q=0.5, '
            'text/html;q=0.8, '
            'application/xhtml+xml;q=0.8'
        ),
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
