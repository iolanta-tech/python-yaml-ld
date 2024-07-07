from pathlib import Path

from yarl import URL


def as_url_or_path(raw: str) -> URL | Path:
    """Interpret a raw string as a URL or a local disk path."""
    if (url := URL(raw)).scheme:
        return url

    return Path(raw)
