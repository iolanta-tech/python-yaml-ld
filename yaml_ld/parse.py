import yaml
from yaml.scanner import ScannerError

from yaml_ld.errors import LoadingDocumentFailed, DocumentIsScalar
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import Document


def parse(yaml_string: str) -> Document:
    try:
        document = yaml.load(
            stream=yaml_string,
            Loader=YAMLLDLoader,
        )
    except ScannerError as err:
        raise LoadingDocumentFailed() from err

    if not isinstance(document, dict | list):
        raise DocumentIsScalar(document=document)

    return document
