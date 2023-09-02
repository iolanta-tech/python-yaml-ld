from dataclasses import dataclass

from documented import Documented


@dataclass
class Help(Documented):
    """{self.message}"""

    message: str
