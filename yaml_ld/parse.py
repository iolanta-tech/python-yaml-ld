from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.scanner import ScannerError

from yaml_ld.errors import (
    DocumentIsScalar,
    LoadingDocumentFailed,
    UndefinedAliasFound, MappingKeyError, InvalidEncoding,
)
from yaml_ld.loader import YAMLLDLoader
from yaml_ld.models import Document


def try_extracting_yaml_from_html(yaml_string: str) -> str:
    """
    Extract YAML from <script> tags in an HTML page.

    FIXME: Should return a list.
    """
    soup = BeautifulSoup(yaml_string, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if script['type'] in {'application/ld+json', 'application/ld+yaml'}:
            yield script.text


def parse(  # noqa: WPS238, WPS231, C901
    yaml_string: str | bytes | Path,
) -> Document:
    """Parse YAML-LD document."""
    if isinstance(yaml_string, Path):
        yaml_string = yaml_string.read_bytes()

    if isinstance(yaml_string, bytes):
        try:
            yaml_string = yaml_string.decode('utf-8')
        except UnicodeDecodeError as err:
            raise InvalidEncoding() from err

    try:
        document: Document = yaml.load(  # noqa: S506
            stream=yaml_string,
            Loader=YAMLLDLoader,
        )
    except ScannerError:
        html_yaml_scripts = list(try_extracting_yaml_from_html(yaml_string))

        if not html_yaml_scripts:
            return {}

        try:
            [singular_script] = html_yaml_scripts
        except ValueError:
            return [parse(script) for script in html_yaml_scripts]

        return parse(singular_script)

    except ComposerError as err:
        raise UndefinedAliasFound() from err

    except ConstructorError as err:
        if err.problem == 'found unhashable key':
            raise MappingKeyError() from err

        raise

    if not isinstance(document, (dict, list)):
        raise DocumentIsScalar(document=document)

    return document
