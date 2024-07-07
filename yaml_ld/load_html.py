import json
from typing import Any, Callable

import lxml
from pyld.jsonld import JsonLdError, _is_array, parse_url, prepend_base

from yaml_ld.models import JsonLdRecord


# This function is from pyld. Replaced hard coded `json.loads` with an arg.
