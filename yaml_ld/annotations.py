from dataclasses import dataclass

from documented import Documented


@dataclass
class Help(Documented):  # type: ignore
    """{self.message}"""

    message: str
