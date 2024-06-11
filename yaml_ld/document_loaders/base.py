from typing import TypedDict, Any

PyLDResponse = TypedDict(
    'PyLDResponse', {
        'contentType': str,
        'contextUrl': str | None,
        'documentUrl': str,
        'document': dict[str, Any],
    },
)


class DocumentLoader:
    ...
