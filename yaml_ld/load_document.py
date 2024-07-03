from pydantic import validate_call
from pyld import jsonld

from yaml_ld.models import BaseOptions


@validate_call(config=dict(arbitrary_types_allowed=True))
def load_document(
    url,
    base=None,
    profile=None,
    requestProfile=None,
    options: BaseOptions = BaseOptions(),   # type: ignore
):
    return jsonld.load_document(
        url=url,
        options=options.model_dump(
            by_alias=True,
            exclude_defaults=True,
        ),
        base=base,
        profile=profile,
        requestProfile=requestProfile,
    )
