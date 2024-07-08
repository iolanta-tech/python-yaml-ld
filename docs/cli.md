---
title: CLI
hide: [toc, navigation]
---

`python-yaml-ld` exposes a command line interface utility.

```
$ pyld
                                                                                              
 Usage: pyld [OPTIONS] COMMAND [ARGS]...                                                      
                                                                                              
 Command line tool to operate on ⋆-LD data, where ⋆ stands for JSON or YAML.                  
                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --log-level                 [debug|info|error]  Logging level. [default: error]            │
│ --install-completion                            Install completion for the current shell.  │
│ --show-completion                               Show completion for the current shell, to  │
│                                                 copy it or customize the installation.     │
│ --help                                          Show this message and exit.                │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────╮
│ compact    Compact a ⋆-LD document.                                                        │
│ expand     Expand a ⋆-LD document.                                                         │
│ flatten    Flatten a ⋆-LD document.                                                        │
│ from-rdf   Convert an RDF document → ⋆-LD form.                                            │
│ to-rdf     Convert a ⋆-LD document → RDF.                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```
