---
hide: [toc]
---

# :material-graph: `to_rdf()`

!!! info "Specified by: [JSON-LD API]({{ yaml_ld.to_rdf.__annotations__.return.__metadata__|first }})"

::: yaml_ld.to_rdf.to_rdf

## Input & output


|               | Type                                       | Default | Description |
|-----------------------|---------------------------------------------|-------------|---|
| `document`            | [SerializedDocument](/types/serialized-document/) \| [Document](/types/document/) |  | Document to expand.         |
| `options`                | `ToRDFOptions | ToRDFOptionsDict`      | | Options |
| :material-arrow-right-bottom-bold: **Returns** | [RDFDataset](/types/rdf-dataset/) | | RDF Dataset |

## `ToRDFOptions` | `ToRDFOptionsDict`

| `ToRDFOptions` | `ToRDFOptionsDict` | Type                                       | Default | Description |
|-----|------------------|---------------------------------------------|-------------|---|
| `context` | `context`            | [Document](/types/document/) \| `None` | `None` | A context to expand with. |
| `extract_all_scripts` | `extractAllScripts` | `bool` | :x: `False` | Will we extract all scripts, or all documents in a YAML stream? |
| `document_loader` | `documentLoader`     | `DocumentLoader`                           | `None` | Document Loader. |
