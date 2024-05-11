from dataclasses import dataclass

from documented import Documented
from urlpath import URL

API = URL('https://w3c.github.io/json-ld-api')
FRAMING = URL('https://www.w3.org/TR/json-ld-framing/')


@dataclass
class Help(Documented):  # type: ignore
    """{self.message}"""

    message: str


def specified_by(url: URL):
    """Link to the specification for a function."""
    def _decorate(function):
        function.specified_by = url
        return function

    return _decorate
