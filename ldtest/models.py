from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestCase:
    test: str
    input: Path
    result: Path | Exception
    req: str
