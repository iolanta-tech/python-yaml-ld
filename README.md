# python-yaml-ld

<!--
![Build Status](https://github.com/iolanta-tech/python-yaml-ld/actions/workflows/main.yml/badge.svg)
![License](https://img.shields.io/github/license/iolanta-tech/python-yaml-ld.svg)
![Version](https://img.shields.io/pypi/v/python-yaml-ld.svg)
![Downloads](https://img.shields.io/pypi/dm/python-yaml-ld.svg)
-->

![](docs/logos/python-yaml-ld.png)

A Python implementation for handling YAML-LD documents.

## What is YAML-LD?

YAML-LD is a YAML-based serialization for Linked Data, drawing inspiration from [JSON-LD](https://json-ld.org/). It aims to bring the ease of YAML along with the structured linked data principles of JSON-LD. The [YAML-LD specification](https://json-ld.github.io/yaml-ld/spec/) provides detailed information on the structure and usage of YAML-LD.

## Installation

```shell
pip install python-yaml-ld
```

## Functions

### `yaml_ld.expand`

Expands a given YAML-LD document into a standardized, expanded form following the [JSON-LD Expansion algorithm](https://www.w3.org/TR/json-ld11-api/#expansion).

- **Parameters**:
  - `document` (str | bytes | Document): The YAML-LD document to expand.
  - `base` (str | None): The base IRI to use.
  - `context` (Document | None): A context to expand with.
  - `extract_all_scripts` (bool): True to extract all JSON-LD script elements from HTML, False to extract just the first.
  - `mode` (ProcessingMode): The JSON-LD processing mode (defaults to JSON-LD 1.1).
  - `document_loader` (DocumentLoader | None): The document loader to use.

### `yaml_ld.to_rdf`

Converts the YAML-LD document to RDF (quads) form, enabling interoperability with other RDF tools and systems.

- **Parameters**:
  - `document` (str | bytes | Document): The YAML-LD document to convert.
  - `base` (str | None): The base IRI to use.
  - `document_loader` (DocumentLoader | None): The document loader to use.

## Development

* Clone the repository
* Set up a Python virtual environment
* Install Poetry:

```shell
pip install -U pip poetry
```

* Install the project:

```shell
poetry install
```

* Retrieve submodules:

```shell
j update-submodule
```
