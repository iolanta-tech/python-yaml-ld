---
title: Diff test results
---

## Context

Current test run for this project outputs:

```
====== 637 failed, 255 passed, 1 xfailed, 10 warnings in 80.24s (0:01:20) ======
```

There is no way all these failing tests can be fixed in one PR; however, it would be preferable NOT to break tests that were not broken in `main` when you're trying to merge your PR.

Is there a Github action that could check for that?

### Alternatives

* [openpgpjs/github-action-pull-request-benchmark](https://github.com/openpgpjs/github-action-pull-request-benchmark) runs tests both in main branch and in PR branch but compares their performance, not results
* Similarly, [jenkinsci/github-pr-coverage-status-plugin](https://github.com/jenkinsci/github-pr-coverage-status-plugin) compares coverage -- but this is a Jenkins plugin, not a GitHub Action

I cannot find anything else.

## Decision

Implement such a script.

## Consequences

It will be easier to develop the project by providing a clear summary of what was fixed and what was newly broken.
