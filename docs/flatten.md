---
hide: [toc]
---

# :material-arrow-collapse: `flatten()`

!!! info "Specified by: [JSON-LD API]({{ yaml_ld.flatten.__annotations__.return.__metadata__|first }})"

::: yaml_ld.flatten.flatten

## Input & output

|               | Type                                       | Default | Description |
|-----------------------|---------------------------------------------|-------------|---|
| `document`            | [SerializedDocument](/types/serialized-document/) \| [Document](/types/document/) |  | Document to Flatten.         |
| `ctx`            | [`Document`](/types/document/) |  | Context to Flatten the document with.         |
| `options`                | `FlattenOptions | FlattenOptionsDict`      | | Options |
| :material-arrow-right-bottom-bold: **Returns** | [Document](/types/document/) \| list[[Document](/types/document/)] | | Flattened document |


## `FlattenOptions` | `FlattenOptionsDict`

| `FlattenOptions` | `FlattenOptionsDict` | Type                                       | Default | Description |
|-----|------------------|---------------------------------------------|-------------|---|
| `base` | `base` | `str` \| `None` | `None` | Base URL. |
| `expand_context` | `expandContext`     | [`Document`](/types/document/) \| None  | `None` | Context to expand with before Flattening. |
| `extract_all_scripts` | `extractAllScripts` | `bool` | :x: `False` | Will we extract all scripts, or all documents in a YAML stream? |
| `document_loader` | `documentLoader`     | `DocumentLoader`                           | `None` | Document Loader. |
