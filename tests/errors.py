import json
from dataclasses import dataclass

from documented import Documented

from ldtest.models import TestCase
from yaml_ld.models import Document


@dataclass
class FailureToFail(Documented):
    """
    YAMLLDError not raised.

    Expected error code: {self.expected_error_code}

    Raw input document (from {self.test_case.input}):
    {self.formatted_raw_document}

    Expanded document:
    {self.formatted_expanded_document}
    """

    test_case: TestCase
    expected_error_code: str
    raw_document: bytes
    expanded_document: Document

    @property
    def formatted_raw_document(self) -> str:
        """Present the raw document."""
        return self.raw_document.decode()

    @property
    def formatted_expanded_document(self) -> str:
        """JSON prettify expanded document for display."""
        return json.dumps(self.expanded_document, indent=2)
