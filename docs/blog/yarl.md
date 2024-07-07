---
title: urlpath → yarl as URL manipulation library
date: 2024-07-07
tags: [decision]
hide: [toc]
---

# `urlpath` → `yarl` as URL manipulation library

## Context

We use `URL` class from `urlpath` library a lot. It automates URL manipulations.

```bash title="grep --include '*.py' -R URL yaml_ld | head"
yaml_ld/string_as_url_or_path.py:from urlpath import URL
yaml_ld/string_as_url_or_path.py:def as_url_or_path(raw: str) -> URL | Path:
yaml_ld/string_as_url_or_path.py:    """Interpret a raw string as a URL or a local disk path."""
yaml_ld/string_as_url_or_path.py:    if (url := URL(raw)).scheme:
yaml_ld/models.py:from urlpath import URL
yaml_ld/models.py:    JsonLdRecord | Sequence[JsonLdRecord] | str | Path | URL | RemoteDocument
yaml_ld/models.py:    expand_context: JsonLdRecord | str | Path | URL | None = None
yaml_ld/document_loaders/choice_by_scheme.py:from urlpath import URL
yaml_ld/document_loaders/choice_by_scheme.py:    Cannot choose the loader by URL protocol.
yaml_ld/document_loaders/choice_by_scheme.py:    * URL: `{self.url}`
```

But, [last PyPI release](https://pypi.org/project/urlpath/) of `urlpath` has been published on 2021-11-12, which is also the date of the last commit at [the project GitHub repository](https://github.com/brandonschabell/urlpath). That is the reason why `urlpath` [is incompatible](https://github.com/brandonschabell/urlpath/issues/6) with Python 3.12. 

### Alternatives

<table>
    <thead>
        <tr>
            <th>Library</th>
            <th>Stars</th>
            <th>Last Release</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>
                <a href="https://github.com/aio-libs/yarl">yarl</a>
            </th>
            <td>1.3k</td>
            <td>
                <a href="https://pypi.org/project/yarl/">2023-12-06</a>
            </td>
        </tr>
        <tr>
            <th>
                <a href="https://github.com/gruns/furl">furl</a>
            </th>
            <td>2.6k</td>
            <td>
                <a href="https://pypi.org/project/furl/">2021-09-28</a>
            </td>
        </tr>
    </tbody>
</table>

## Decision

Use `yarl` as a library that's current and regularly updated.
