---
hide: [toc]
---

# :material-image-frame: `frame()`

!!! info "Specified by: [JSON-LD Framing]({{ yaml_ld.frame.__annotations__.return.__metadata__|first }})"

::: yaml_ld.frame.frame

## Input & output

|               | Type                                       | Default | Description |
|-----------------------|---------------------------------------------|-------------|---|
| `document`            | [SerializedDocument](/types/serialized-document/) \| [Document](/types/document/) |  | Document to Frame.         |
| `frame`            | [`Document`](/types/document/) |  | Frame to process the document with.         |
| `options`                | `FrameOptions | FrameOptionsDict`      | | Options |
| :material-arrow-right-bottom-bold: **Returns** | [Document](/types/document/) \| list[[Document](/types/document/)] | | Framed document |


## `FrameOptions` | `FrameOptionsDict`

| `FrameOptions` | `FrameOptionsDict` | Type                                       | Default | Description |
|-----|------------------|---------------------------------------------|-------------|---|
| `base` | `base` | `str` \| `None` | `None` | Base URL. |
| `expand_context` | `expandContext`     | [`Document`](/types/document/) \| None  | `None` | Context to expand with before Frameing. |
| `extract_all_scripts` | `extractAllScripts` | `bool` | :x: `False` | Will we extract all scripts, or all documents in a YAML stream? |
| `document_loader` | `documentLoader`     | `DocumentLoader`                           | `None` | Document Loader. |
