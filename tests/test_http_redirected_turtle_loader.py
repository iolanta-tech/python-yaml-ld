from requests import Response, Session
from yarl import URL

from yaml_ld.document_loaders import default


PURL_SOURCE = "http://purl.org/linked-data/cube#"
TURTLE_CONTENT_TYPE = "text/turtle"
TURTLE_URL = "https://raw.githubusercontent.com/example/cube.ttl"
TURTLE_DOCUMENT = b"""
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix qb: <http://purl.org/linked-data/cube#> .

qb:Observation rdfs:label "Observation" .
"""


class FakeSession(Session):
    def __init__(self, response: Response):
        super().__init__()
        self.response = response

    def get(self, *args, **kwargs):  # noqa: WPS110
        return self.response


def _plain_text_turtle_response() -> Response:
    response = Response()
    response.status_code = 200
    response.url = TURTLE_URL
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    response._content = TURTLE_DOCUMENT
    return response


def test_uses_redirected_url_extension_for_turtle():
    remote_document = default.HTTPDocumentLoader(
        session=FakeSession(response=_plain_text_turtle_response()),
    )(
        source=URL(PURL_SOURCE),
        options={
            "base": PURL_SOURCE,
            "extractAllScripts": False,
            "headers": {},
        },
    )

    assert remote_document["contentType"] == TURTLE_CONTENT_TYPE
    assert remote_document["documentUrl"] == TURTLE_URL
    assert remote_document["document"]
