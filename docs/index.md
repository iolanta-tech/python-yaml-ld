---
title: Home
hide: [toc, navigation]
---

# YAML-LD implementation for Python

![](logos/python-yaml-ld.png)

A Python implementation for handling YAML-LD documents.

!!! info "`python-yaml-ld` is a wrapper on top of [:material-github: digitalbazaar/pyld](https://github.com/digitalbazaar/pyld)."


## What is YAML-LD?

YAML-LD is a YAML-based serialization for Linked Data, drawing inspiration from [JSON-LD](https://json-ld.org/). It aims to bring the ease of YAML along with the structured linked data principles of JSON-LD. The [YAML-LD specification](https://json-ld.github.io/yaml-ld/spec/) provides detailed information on the structure and usage of YAML-LD.

## What does `python-yaml-ld` provide?

=== "Python API"
    `import yaml_ld` provides you with the following functions to operate on [＊-LD](/blog/any-ld/) documents:

    <div class="grid cards" markdown>
    {% for description in functions %}
    -     :{{ description.icon }}:{ .lg .middle } __[`{{ description.function_name }}()`]({{ description.function_url }})__

          ---
          {{ description.function_docstring }}
    {% endfor %}
    </div>

=== "`pyld` CLI"
    `pip install yaml-ld` makes `pyld` executable available, which exposes the functionality of `pyld` library with additions provided by `python-yaml-ld`.

    <div class="grid cards" markdown>
    {% for description in functions %}
    {% if functions.cli %}
    -     :{{ description.icon }}:{ .lg .middle } __[`pyld {{ description.command_name }}`]({{ description.command_url }})__

          ---
          {{ description.function_docstring }}
    {% endif %}
    {% endfor %}
    </div>
