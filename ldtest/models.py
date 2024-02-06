from dataclasses import dataclass
from pathlib import Path

from urlpath import URL


@dataclass
class TestCase:
    """JSON-LD Test Case."""

    test: str
    input: Path | URL
    result: Path | str | Exception   # noqa: WPS110
    req: str
    extract_all_scripts: bool = False

    @property
    def raw_document(self) -> bytes:
        """Read the raw input document contents."""
        path = self.input
        if isinstance(path, URL):
            path = Path(path.path)

        return path.read_bytes()

    @property
    def raw_expected_document(self):
        """Text of the expected processed document."""
        if isinstance(path := self.result, Path):
            return path.read_text()

        raise ValueError(f'{self.result} is not a Path.')
