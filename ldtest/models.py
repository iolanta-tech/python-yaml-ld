from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestCase:
    """JSON-LD Test Case."""

    test: str
    input: Path
    result: Path | str | Exception   # noqa: WPS110
    req: str

    @property
    def raw_document(self) -> bytes:
        """Read the raw input document contents."""
        return self.input.read_bytes()

    @property
    def raw_expected_document(self):
        """Text of the expected processed document."""
        if isinstance(path := self.result, Path):
            return path.read_text()

        raise ValueError(f'{self.result} is not a Path.')
