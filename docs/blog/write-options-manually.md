---
tags: [decision]
title: Write options types manually
---

# Write `options` types manually

## Context

`expand()`, `frame()`, and the rest of functions specified by JSON-LD API take `options` argument, described by `JsonLdOptions` interface in the specification.

Some options are only valid for select functions, for instance, `frameExpansion` is only valid for `frame()`.

## Decision

* In Python types, use a separate type for each function's `options` argument
* Write these types manually instead of generating them from IDL.

## Consequences

* Improved typing hints in application code;
* Invalid states made unrepresentable;
* Enhanced development experience.
