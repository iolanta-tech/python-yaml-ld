---
tags: [decision]
context:
  rdfs:comment: To parse YAML-LD, we need to choose a YAML library from ones available.
  table:columns:
    - table:self
    - github-stars
    - $id: supports-anchors
      rdfs:label: Supports Anchors and Aliases
      rdfs:comment: YAML-LD specification does mention anchors and aliases, and I would not want at this point to start a discussion to ban them from the spec. Thus we need the YAML library of choice to support those.
  table:rows:
    - rdfs:label: strictyaml
      schema:url: https://github.com/crdoconnor/strictyaml
      github-stars: 1.3k
      supports-anchors: no
    - rdfs:label: poyo
      schema:url: https://github.com/hackebrot/poyo
      github-stars: 135
      supports-anchors: no

decision: pyyaml

consequences:
  pro:
    - title: We get full set of YAML features
  contra:
    - title: We might be affected by security issues present in YAML
---

# Use `{{ page.meta['decision'] }}` as YAML parsing library

!!! info
    Please see the source code of this page. I just wrote down the decision in YAML front matter but at this point I do not have the code to visualize it properly. I will get back to this later.
