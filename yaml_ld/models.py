from enum import Enum
from typing import Any, Annotated

from pydantic import BaseModel, Field

Document = dict[str, Any]   # type: ignore
DocumentLoader = Any  # type: ignore   # FIXME: This is actually a callable.


ExtractAllScripts = Annotated[
    bool,
    'Extract all JSON-LD script elements, as opposed to only the first one.',
]


class DocumentType(str, Enum):
    """Document type."""

    YAML = 'yaml'
    HTML = 'html'


class ProcessingMode(str, Enum):  # noqa: WPS600
    """JSON-LD API version."""

    JSON_LD_1_0 = 'json-ld-1.0'   # noqa: WPS114, WPS115
    JSON_LD_1_1 = 'json-ld-1.1'   # noqa: WPS114, WPS115


class BaseOptions(BaseModel):
    """Base options shared by all YAML-LD API methods."""

    base: str | None = Field(default=None)
    extract_all_scripts: bool = Field(default=False, alias='extractAllScripts')
    mode: ProcessingMode = Field(
        default=ProcessingMode.JSON_LD_1_1,
        alias='processingMode',
    )
    document_loader: DocumentLoader | None = Field(
        default=None,
        alias='documentLoader',
    )
