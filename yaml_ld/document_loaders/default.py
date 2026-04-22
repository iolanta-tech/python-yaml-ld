import logging
import platformdirs
import sqlite3
import tempfile
from pathlib import Path

from requests import Session
from requests_cache import CachedSession

from yaml_ld.document_loaders.choice_by_scheme import (
    ChoiceBySchemeDocumentLoader,
)
from yaml_ld.document_loaders.http import HTTPDocumentLoader
from yaml_ld.document_loaders.local_file import LocalFileDocumentLoader

APP_NAME = "python-yaml-ld"
_WRITE_TEST_FILE = ".write-test"
logger = logging.getLogger(__name__)


def _user_cache_directory() -> Path:
    return Path(
        platformdirs.user_cache_dir(
            appname=APP_NAME,
            ensure_exists=False,
        )
    )


def _temporary_cache_directory() -> Path:
    return Path(tempfile.gettempdir()) / APP_NAME


def _write_test_file(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    write_test_path = directory / _WRITE_TEST_FILE
    write_test_path.write_text("", encoding="utf-8")
    write_test_path.unlink(missing_ok=True)


def _is_writable_directory(directory: Path) -> bool:
    try:
        _write_test_file(directory=directory)
    except OSError:
        return False

    return True


def _cache_directory() -> Path:
    user_cache_directory = _user_cache_directory()
    if _is_writable_directory(user_cache_directory):
        return user_cache_directory

    return _temporary_cache_directory()


def _cached_session(cache_directory: Path) -> Session:
    try:
        return CachedSession(
            backend="filesystem",
            cache_name=cache_directory,
        )
    except (OSError, KeyError, sqlite3.Error) as error:
        logger.warning(
            "Cannot use requests cache directory %s: %s",
            cache_directory,
            error,
        )

        return Session()


CACHE_DIRECTORY = _cache_directory()

CACHED_SESSION = _cached_session(
    cache_directory=CACHE_DIRECTORY,
)

http_loader = HTTPDocumentLoader(
    session=CACHED_SESSION,
)

DEFAULT_DOCUMENT_LOADER = ChoiceBySchemeDocumentLoader(
    file=LocalFileDocumentLoader(),
    http=http_loader,
    https=http_loader,
)
