from typing import Annotated

from pydantic import validate_call
from pyld import jsonld

from yaml_ld import parse
from yaml_ld.annotations import API, FRAMING
from yaml_ld.expand import except_json_ld_errors
from yaml_ld.models import Document, SerializedDocument, BaseOptions


class FrameOptions(BaseOptions):
    ...


@validate_call(config=dict(arbitrary_types_allowed=True))
def frame(
    document: SerializedDocument | Document,
    frame: Document,
    options: FrameOptions,
) -> Annotated[Document, FRAMING / '#dom-jsonldprocessor-frame']:
    """Frame a YAML-LD document."""
    if isinstance(document, (str, bytes)):
        document = parse(document)

    with except_json_ld_errors():
        return jsonld.frame(
            input_=document,
            frame=frame,
            options=options.model_dump(by_alias=True),
        )
