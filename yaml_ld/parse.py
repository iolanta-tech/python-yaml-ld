import yaml
from yaml.composer import ComposerError
from yaml.scanner import ScannerError

from yaml_ld.errors import (
    DocumentIsScalar, LoadingDocumentFailed,
    UndefinedAliasFound,
)
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import Document


def parse(yaml_string: str) -> Document:
    try:
        document: Document = yaml.load(
            stream=yaml_string,
            Loader=YAMLLDLoader,
        )
    except ScannerError as err:
        raise LoadingDocumentFailed() from err

    except ComposerError as err:
        raise UndefinedAliasFound() from err

    if not isinstance(document, (dict, list)):
        raise DocumentIsScalar(document=document)

    return document
