---
hide: [toc]
---

::: yaml_ld.expand.expand


!!! info "Specified by: [JSON-LD API]({{ yaml_ld.expand.__annotations__.return.__metadata__|first }})"


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
