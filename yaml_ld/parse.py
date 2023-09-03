import yaml

from yaml_ld.errors import LoadingDocumentFailed
from yaml_ld.models import Document


def parse(yaml_string: str) -> Document:
    document = yaml.load(
        stream=yaml_string,
        Loader=yaml.SafeLoader,
    )

    if not isinstance(document, dict | list):
        raise LoadingDocumentFailed(document=document)

    return document
