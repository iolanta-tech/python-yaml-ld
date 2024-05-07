---
hide: [toc]
---

# :material-arrow-collapse: `compact()`

!!! info "Specified by: [JSON-LD API]({{ yaml_ld.compact.__annotations__.return.__metadata__|first }})"

::: yaml_ld.compact.compact

## Input & output

|               | Type                                       | Default | Description |
|-----------------------|---------------------------------------------|-------------|---|
| `document`            | [SerializedDocument](/types/serialized-document/) \| [Document](/types/document/) |  | Document to compact.         |
| `ctx`            | [`Document`](/types/document/) |  | Context to compact the document with.         |
| `options`                | `CompactOptions | CompactOptionsDict`      | | Options |
| :material-arrow-right-bottom-bold: **Returns** | [Document](/types/document/) \| list[[Document](/types/document/)] | | Compacted document |


## `CompactOptions` | `CompactOptionsDict`

| `CompactOptions` | `CompactOptionsDict` | Type                                       | Default | Description |
|-----|------------------|---------------------------------------------|-------------|---|
| `compact_arrays` | `compactArrays` | `bool` | :heavy_check_mark: `True` |  |
| `graph` | `graph`     | `bool`           | :x: `False` | Document Loader. |
| `expand_context` | `expandContext`     | [`Document`](/types/document/) \| None  | `None` | Context to expand with before compacting. |
| `skip_expansion` | `skipExpansion` | `bool` | :x: `False` | Skip expansion before compacting? |

