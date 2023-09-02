from enum import Enum
from typing import Any

Document = dict[str, Any]


class ProcessingMode(str, Enum):
    JSON_LD_1_0 = 'json-ld-1.0'
    JSON_LD_1_1 = 'json-ld-1.1'


class ExpandOptions(BaseModel):
    ...
