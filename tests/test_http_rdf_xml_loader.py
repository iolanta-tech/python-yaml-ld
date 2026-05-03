from requests import Response, Session
from yarl import URL

from yaml_ld.document_loaders import default


IBIS_URL = "https://vocab.methodandstructure.com/ibis#"
ISSUE_COMPONENT_LABEL = "Issue Component"
RDF_XML_CONTENT_TYPE = "application/rdf+xml"

RDF_XML_DOCUMENT = b"""<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
  <rdf:Description
      rdf:about="https://vocab.methodandstructure.com/ibis#IssueComponent">
    <rdfs:label>Issue Component</rdfs:label>
  </rdf:Description>
</rdf:RDF>
"""


class FakeSession(Session):
    def __init__(self, response: Response):
        super().__init__()
        self.response = response

    def get(self, *args, **kwargs):  # noqa: WPS110
        return self.response


def _rdf_xml_response(
    url: str,
    content_type: str | None,
) -> Response:
    response = Response()
    response.status_code = 200
    response.url = url
    if content_type:
        response.headers["Content-Type"] = content_type
    response._content = RDF_XML_DOCUMENT
    return response


def _contains_label(node) -> bool:
    if node == ISSUE_COMPONENT_LABEL:
        return True

    if isinstance(node, list):
        return any(_contains_label(element) for element in node)

    if isinstance(node, dict):
        return any(
            _contains_label(element)
            for element in node.values()
        )

    return False


def _load_response(url: str, response: Response):
    return default.HTTPDocumentLoader(
        session=FakeSession(response=response),
    )(
        source=URL(url),
        options={
            "base": url,
            "extractAllScripts": False,
            "headers": {},
        },
    )


def test_parse_application_xml_rdf():
    remote_document = _load_response(
        url=IBIS_URL,
        response=_rdf_xml_response(
            url=IBIS_URL,
            content_type="application/xml",
        ),
    )

    assert remote_document["contentType"] == "application/xml"
    assert _contains_label(remote_document["document"])


def test_parse_rdf_xml_root_with_newline():
    url = "https://example.test/ibis.rdf"
    remote_document = _load_response(
        url=url,
        response=_rdf_xml_response(
            url=url,
            content_type=RDF_XML_CONTENT_TYPE,
        ),
    )

    assert remote_document["contentType"] == RDF_XML_CONTENT_TYPE
    assert _contains_label(remote_document["document"])


def test_sniff_rdf_xml_root_with_newline():
    url = "https://example.test/ibis"
    remote_document = _load_response(
        url=url,
        response=_rdf_xml_response(
            url=url,
            content_type=None,
        ),
    )

    assert remote_document["contentType"] == RDF_XML_CONTENT_TYPE
    assert _contains_label(remote_document["document"])
