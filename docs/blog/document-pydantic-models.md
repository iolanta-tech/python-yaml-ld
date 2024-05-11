---
tags: [decision]
title: Document Pydantic models with mkdocstrings
---

## Context

We need to auto document Pydantic models in the library, drawing them as tables.

| Library | Draws tables? | Last Update |
| --- | --- | --- |
| mkdocstrings | No | |
| [mkapi](https://github.com/daizutabi/mkapi) | No | |
| [mkdoxy](https://github.com/JakubAndrysek/MkDoxy) | No | |
| [mkautodoc](https://github.com/tomchristie/mkautodoc) | No | |
| [inari](https://github.com/tkamenoko/inari) | No | |
| [automacdoc](https://github.com/AlexandreKempf/automacdoc) | No | |
| [mkdocs-typedoc](https://github.com/JakubAndrysek/mkdocs-typedoc) | No | |
| [mkdocs-doxygen-plugin](https://github.com/pieterdavid/mkdocs-doxygen-plugin) | No | |
| [yaarg](https://github.com/g6123/mkdocs-yaarg-plugin) | Yes | 2021-03-14 |

## Decision

* Use mkdocstrings for now
* Maybe file an issue about rendering Pydantic models there

