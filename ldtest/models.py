from dataclasses import dataclass
from pathlib import Path

from urlpath import URL

from yaml_ld.expand import ExpandOptions
from yaml_ld.models import Document


@dataclass
class TestCase:
    """JSON-LD Test Case."""

    test: str
    input: Path | URL
    result: Path | str | Exception   # noqa: WPS110
    req: str
    ctx: Document | None = None
    frame: Document | None = None
    extract_all_scripts: bool = False
    base: str | None = None

    @property
    def raw_document(self) -> bytes:
        """Read the raw input document contents."""
        path = self.input
        if isinstance(path, URL):
            path = Path(path.path)

        return path.read_bytes()

    @property
    def raw_expected_document(self) -> str:
        """Text of the expected processed document."""
        if isinstance(path := self.result, Path):
            return path.read_text()

        raise ValueError(f'{self.result} is not a Path.')

    def _stream_kwargs(self):
        if self.ctx is not None:
            yield 'ctx', self.ctx

        if self.frame is not None:
            yield 'frame', self.frame

        yield 'options', ExpandOptions(
            base=self.base,
            extract_all_scripts=self.extract_all_scripts,
        ).model_dump(
            by_alias=True,
            exclude_defaults=True,
        )

    @property
    def kwargs(self):
        return dict(self._stream_kwargs())
