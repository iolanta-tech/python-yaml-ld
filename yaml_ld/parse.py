import yaml
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.scanner import ScannerError

from yaml_ld.errors import (
    DocumentIsScalar,
    LoadingDocumentFailed,
    UndefinedAliasFound, MappingKeyError,
)
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import Document


def parse(yaml_string: str) -> Document:
    """Parse YAML-LD document."""
    try:
        document: Document = yaml.load(  # noqa: S506
            stream=yaml_string,
            Loader=YAMLLDLoader,
        )
    except ScannerError as err:
        raise LoadingDocumentFailed() from err

    except ComposerError as err:
        raise UndefinedAliasFound() from err

    except ConstructorError as err:
        if err.problem == 'found unhashable key':
            raise MappingKeyError() from err

        raise

    if not isinstance(document, (dict, list)):
        raise DocumentIsScalar(document=document)

    return document
