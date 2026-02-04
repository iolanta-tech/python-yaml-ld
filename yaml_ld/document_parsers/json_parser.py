import io
import json

from yaml_ld.document_parsers.base import (
    BaseDocumentParser,
    DocumentLoaderOptions,
)
from yaml_ld.errors import (
    DocumentIsScalar,
    InvalidEncoding,
    LoadingDocumentFailed,
)
from yaml_ld.models import JsonLdRecord


def ensure_not_scalar(document) -> JsonLdRecord | list[JsonLdRecord]:
    """Ensure document is not a scalar value."""
    if not isinstance(document, (dict, list)):
        raise DocumentIsScalar(document)

    return document


class JSONDocumentParser(BaseDocumentParser):
    """Parse JSON and JSON-LD documents."""

    def __call__(
        self,
        data_stream: io.BytesIO,
        source: str,
        options: DocumentLoaderOptions,
    ) -> JsonLdRecord | list[JsonLdRecord]:
        """Parse JSON document into LD."""
        try:
            text = data_stream.read().decode('utf-8')
        except UnicodeDecodeError as unicode_decode_error:
            raise InvalidEncoding() from unicode_decode_error

        try:
            document = json.loads(text)
        except json.JSONDecodeError as json_error:
            raise LoadingDocumentFailed(path=source) from json_error

        return ensure_not_scalar(document)
