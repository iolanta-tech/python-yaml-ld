from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

Document = dict[str, Any]


class ProcessingMode(str, Enum):
    JSON_LD_1_0 = 'json-ld-1.0'
    JSON_LD_1_1 = 'json-ld-1.1'


class ExpandOptions(BaseModel):
    base: str | None = Field(default=None)
    context: Document | None = Field(default=None, alias='expandContext')
    extract_all_scripts: bool = Field(default=False, alias='extractAllScripts')
    mode: ProcessingMode = Field(
        default=ProcessingMode.JSON_LD_1_1,
        alias='processingMode',
    )
    document_loader: Any = Field(default=None, alias='documentLoader')

