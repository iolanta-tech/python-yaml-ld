from pydantic import validate_call
from pyld import jsonld

from yaml_ld.document_loaders.base import PyLDResponse
from yaml_ld.document_loaders.default import DEFAULT_DOCUMENT_LOADER
from yaml_ld.models import DEFAULT_VALIDATE_CALL_CONFIG
from yaml_ld.options import BaseOptions

DEFAULT_BASE_OPTIONS = BaseOptions()


@validate_call(config=DEFAULT_VALIDATE_CALL_CONFIG)
def load_document(
    url,
    base=None,
    profile=None,
    requestProfile=None,
    options: BaseOptions = DEFAULT_BASE_OPTIONS,
) -> PyLDResponse:
    """Load document from the given source."""
    dict_options = options.model_dump(by_alias=True, exclude_none=True)
    dict_options.setdefault('documentLoader', DEFAULT_DOCUMENT_LOADER)

    return jsonld.load_document(
        url=url,
        options=dict_options,
        base=base,
        profile=profile,
        requestProfile=requestProfile,
    )
