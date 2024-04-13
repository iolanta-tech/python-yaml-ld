---
hide: [toc]
---

# :material-arrow-expand-all: `expand()`

!!! info "Specified by: [JSON-LD API]({{ yaml_ld.expand.specified_by }})"

::: yaml_ld.expand.expand

## Input & output

|               | Type                                       | Default | Description |
|-----------------------|---------------------------------------------|-------------|---|
| `document`            | [SerializedDocument](/types/serialized-document/) \| [Document](/types/document/) |  | Document to expand.         |
| `base`                | `str | None`      | | The base IRI to use. |
| `context`             | [Document](/types/document/) \| `None` | | A context to expand with. |
| `extract_all_scripts` | `bool` | :x: `False` | Will we extract all scripts, or all documents in a YAML stream? |
| `mode`                | [`ProcessingMode`](/types/processing-mode/) | JSON-LD 1.1 | JSON-LD version to use. |
| `document_loader`     | `DocumentLoader`                           | `None` | Document Loader. |
| :material-arrow-right-bottom-bold: **Returns** | [Document](/types/document/) \| list[[Document](/types/document/)] | | Expanded document |

