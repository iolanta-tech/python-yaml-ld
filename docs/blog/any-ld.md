---
title: Use ＊-LD to denote any JSON-LD derived standard
tags: [decision]
---

## Context

`python-yaml-ld`, despite the name, supports multiple LD standards:

* JSON-LD,
* YAML-LD,
* and, potentially in the future, CBOR-LD, TOML-LD, and more.

Thus, it would be unfair to say that [`expand()`](/expand/) can only work on JSON-LD or YAML-LD documents.

## Decision

Use ＊-LD (pronounced: *Any-LD*) notation to describe all JSON-LD inspired standards/formats.
