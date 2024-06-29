from dataclasses import dataclass
from pathlib import Path

import funcy
from urlpath import URL

from yaml_ld.compact import CompactOptions
from yaml_ld.expand import ExpandOptions
from yaml_ld.flatten import FlattenOptions
from yaml_ld.frame import FrameOptions
from yaml_ld.from_rdf import FromRDFOptions
from yaml_ld.models import Document
from yaml_ld.to_rdf import ToRDFOptions


SPECIFICATIONS_ROOT = Path(__file__).parent.parent / "specifications"


@dataclass
class TestCase:
    """JSON-LD Test Case."""

    test: str
    test_class: str
    input: Path | URL
    result: Path | str | Exception   # noqa: WPS110
    req: str
    ctx: Document | None = None
    frame: Document | None = None
    extract_all_scripts: bool = False
    base: str | None = None
    redirect_to: str | None = None
    base_iri: URL | None = None

    @property
    def specification(self) -> str:
        return self.input_path.relative_to(SPECIFICATIONS_ROOT).parts[0]

    @property
    def input_path(self):
        if isinstance(self.input, Path):
            return self.input

        return Path(self.input.path)

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

    @property
    @funcy.post_processing(dict)
    def kwargs(self):
        if self.ctx is not None:
            yield 'ctx', self.ctx

        if self.frame is not None:
            yield 'frame', self.frame

        options_class = {
            'ToRDFTest': ToRDFOptions,
            'FromRDFTest': FromRDFOptions,
            'CompactTest': CompactOptions,
            'ExpandTest': ExpandOptions,
            'FlattenTest': FlattenOptions,
            'FrameTest': FrameOptions,
        }[self.test_class]

        yield 'options', options_class(
            base=self.base,
            extract_all_scripts=self.extract_all_scripts,
            expand_context=self.ctx,
        ).model_dump(
            by_alias=True,
            exclude_defaults=True,
        )
