---
hide: [toc]
---

# :material-arrow-expand-all: `expand()`

!!! info "Specified by: [JSON-LD API]({{ yaml_ld.expand.__annotations__.return.__metadata__|first }})"

::: yaml_ld.expand.expand

## Input & output


|               | Type                                       | Default | Description |
|-----------------------|---------------------------------------------|-------------|---|
| `document`            | [SerializedDocument](/types/serialized-document/) \| [Document](/types/document/) |  | Document to expand.         |
| `options`                | `ExpandOptions | ExpandOptionsDict`      | | Options |
| :material-arrow-right-bottom-bold: **Returns** | [Document](/types/document/) \| list[[Document](/types/document/)] | | Expanded document |

## `ExpandOptions` | `ExpandOptionsDict`

| `ExpandOptions` | `ExpandOptionsDict` | Type                                       | Default | Description |
|-----|------------------|---------------------------------------------|-------------|---|
| `context` | `context`            | [Document](/types/document/) \| `None` | `None` | A context to expand with. |
| `extract_all_scripts` | `extractAllScripts` | `bool` | :x: `False` | Will we extract all scripts, or all documents in a YAML stream? |
| `document_loader` | `documentLoader`     | `DocumentLoader`                           | `None` | Document Loader. |

## Examples

=== "`two-documents-in.yamlld`"

    ```yaml
    --8<-- "specifications/yaml-ld/tests/cases/streams/two-documents-in.yamlld"
    ```

=== "Call `yaml_ld.expand()`"

    ```python
    from pathlib import Path
    import pyyaml
    import yaml_ld

    pyyaml.dumps(
        yaml_ld.expand(
            document=Path(
                'specifications/yaml-ld/tests/cases/streams/two-documents-in.yamlld'
            ),
            options=yaml_ld.ExpandOptions(extract_all_scripts=True),   # (1)
        ),
    )
    ```

    1.  Or,
        ```python
        options={'extractAllScripts': True},
        ```
        if you wish to be closer to the letter of the JSON-LD API Specification.

=== "`two-documents-out.yamlld`"

    ```yaml
    --8<-- "specifications/yaml-ld/tests/cases/streams/two-documents-out.yamlld"
    ```
