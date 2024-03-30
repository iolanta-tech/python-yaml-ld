---
tags: [decision]
is-blocked-by: diff-test-results.md
title: Parallelize tests per branch in GitHub actions
---

## Context

Shall we

* Run tests against `main` and against the PR branch within the same Python script,
* Or run them separately using GitHub actions?

## Decision

Use GitHub actions.

## Consequences

* This way, even if `main` and the PR branch have different dependencies they will be correctly configured, and all packages installed in each environment, avoiding conflicts
* We will have to save test results for each run as artifacts.
