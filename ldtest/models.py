from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestCase:
    """JSON-LD Test Case."""

    test: str
    input: Path
    result: Path | str | Exception   # noqa: WPS110
    req: str
