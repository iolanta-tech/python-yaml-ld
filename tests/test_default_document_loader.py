from requests import Response, Session
from yarl import URL

from yaml_ld.document_loaders import default


class FakeSession(Session):
    def __init__(self, response: Response):
        super().__init__()
        self.response = response

    def get(self, *args, **kwargs):  # noqa: WPS110
        return self.response


class BrokenCachedSession:
    def __init__(self, *args, **kwargs):
        raise OSError("read-only cache")


def _json_ld_response(url: str) -> Response:
    response = Response()
    response.status_code = 200
    response.url = url
    response.headers["Content-Type"] = "application/ld+json"
    response._content = b'{"@id": "https://example.test/alice"}'
    return response


def test_cache_directory_uses_writable_user_cache(monkeypatch, tmp_path):
    user_cache_directory = tmp_path / "user-cache"
    temporary_cache_directory = tmp_path / "temporary-cache"

    monkeypatch.setattr(
        default,
        "_user_cache_directory",
        lambda: user_cache_directory,
    )
    monkeypatch.setattr(
        default,
        "_temporary_cache_directory",
        lambda: temporary_cache_directory,
    )

    assert default._cache_directory() == user_cache_directory
    assert user_cache_directory.is_dir()
    assert not temporary_cache_directory.exists()


def test_cache_directory_falls_back(
    monkeypatch,
    tmp_path,
):
    user_cache_directory = tmp_path / "user-cache"
    temporary_cache_directory = tmp_path / "temporary-cache"

    monkeypatch.setattr(
        default,
        "_user_cache_directory",
        lambda: user_cache_directory,
    )
    monkeypatch.setattr(
        default,
        "_temporary_cache_directory",
        lambda: temporary_cache_directory,
    )
    monkeypatch.setattr(
        default,
        "_is_writable_directory",
        lambda directory: directory != user_cache_directory,
    )

    assert default._cache_directory() == temporary_cache_directory


def test_cached_session_falls_back(monkeypatch, tmp_path):
    monkeypatch.setattr(default, "CachedSession", BrokenCachedSession)

    assert isinstance(default._cached_session(tmp_path), Session)


def test_http_loader_returns_with_fallback(
    monkeypatch,
    tmp_path,
):
    url = "https://example.test/person"
    user_cache_directory = tmp_path / "user-cache"
    temporary_cache_directory = tmp_path / "temporary-cache"
    response = _json_ld_response(url=url)

    monkeypatch.setattr(
        default,
        "_user_cache_directory",
        lambda: user_cache_directory,
    )
    monkeypatch.setattr(
        default,
        "_temporary_cache_directory",
        lambda: temporary_cache_directory,
    )
    monkeypatch.setattr(
        default,
        "_is_writable_directory",
        lambda directory: directory != user_cache_directory,
    )

    assert default._cache_directory() == temporary_cache_directory

    document = default.HTTPDocumentLoader(
        session=FakeSession(response=response),
    )(
        source=URL(url),
        options={
            "base": url,
            "extractAllScripts": False,
            "headers": {},
        },
    )

    assert document["document"] == {"@id": "https://example.test/alice"}
