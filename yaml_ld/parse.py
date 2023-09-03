import yaml
from yaml.scanner import ScannerError

from yaml_ld.errors import LoadingDocumentFailed
from yaml_ld.models import Document


def parse(yaml_string: str) -> Document:
    try:
        document = yaml.load(
            stream=yaml_string,
            Loader=yaml.SafeLoader,
        )
    except ScannerError as err:
        raise LoadingDocumentFailed(document='') from err

    if not isinstance(document, dict | list):
        raise LoadingDocumentFailed(document=document)

    return document
