---
tags: [decision]
supersedes: pyyaml
context:
  rdfs:comment: To parse YAML-LD, we need a YAML library that supports YAML 1.2.2. The previous choice (PyYAML) implements YAML 1.1 only.
  table:columns:
    - table:self
    - $id: yaml-spec
      rdfs:label: YAML 1.2.2 Support
      rdfs:comment: YAML-LD requires YAML 1.2.2 compliance (e.g. no Yes/No/On/Off as booleans, correct octal syntax).
    - $id: supports-anchors
      rdfs:label: Supports Anchors and Aliases
      rdfs:comment: YAML-LD specification mentions anchors and aliases; the library must support them.
    - maintenance
  table:rows:
    - rdfs:label: ruamel.yaml
      schema:url: https://github.com/ruamel/yaml
      yaml-spec: yes
      supports-anchors: yes
      maintenance: Active
    - rdfs:label: py-yaml12
      schema:url: https://github.com/posit-dev/py-yaml12
      yaml-spec: yes
      supports-anchors: yes
      maintenance: New (v0.1.0)
    - rdfs:label: pyyaml-pure
      schema:url: https://github.com/nicksanders/pyyaml-pure
      yaml-spec: yes
      supports-anchors: yes
      maintenance: Alpha
    - rdfs:label: PyYAML
      schema:url: https://github.com/yaml/pyyaml
      yaml-spec: no
      supports-anchors: yes
      maintenance: Slow
    - rdfs:label: strictyaml
      schema:url: https://github.com/crdoconnor/strictyaml
      yaml-spec: N/A
      supports-anchors: no
      maintenance: Slow

decision: ruamel.yaml

consequences:
  pro:
    - title: YAML 1.2.2 compliance
    - title: Full set of YAML features including anchors and aliases
    - title: Actively maintained, production-grade
  contra:
    - title: Different API from PyYAML (not a drop-in replacement)
    - title: PEP 625 may force PyPI package rename in future
---

# Use `{{ page.meta['decision'] }}` as YAML parsing library

This ADR supersedes the previous decision to use PyYAML. PyYAML implements YAML 1.1 only; YAML-LD requires YAML 1.2.2.

**Candidates evaluated:**

- **ruamel.yaml** — YAML 1.2 by default, actively maintained (~152M downloads/month), passes 265/308 yaml-test-suite valid cases. Chosen.
- **py-yaml12** — 100% yaml-test-suite compliant, but too new (v0.1.0, Dec 2025) for production.
- **pyyaml-pure** — Drop-in API, but Alpha stage with minimal adoption.

**Disqualified:** PyYAML (YAML 1.1 only), PyYAML-ft (inherits 1.1), strictyaml (no anchors, restricted subset).
