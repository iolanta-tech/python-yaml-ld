---
title: Home
hide: [toc, navigation]
---

# YAML-LD implementation for Python

![](logos/python-yaml-ld.png)

A Python implementation for handling YAML-LD documents.

## What is YAML-LD?

YAML-LD is a YAML-based serialization for Linked Data, drawing inspiration from [JSON-LD](https://json-ld.org/). It aims to bring the ease of YAML along with the structured linked data principles of JSON-LD. The [YAML-LD specification](https://json-ld.github.io/yaml-ld/spec/) provides detailed information on the structure and usage of YAML-LD.


{% raw %}
```mermaid
graph LR
    Document("Document")
    click Document "/types/document/" "YAML-LD Document"
    class Document type

    subgraph RDF
        DocumentRDF("Document") --> to_rdf{{"to_rdf()"}} --> Dataset("Dataset")
        Dataset --> from_rdf{{"from_rdf()"}} --> DocumentRDF
        click DocumentRDF "/types/document/" "YAML-LD Document"
        class DocumentRDF type
    
        class to_rdf,from_rdf function
        click to_rdf "/to-rdf/" "Convert a YAML-LD Document into an RDF dataset"
        click from_rdf "/from-rdf/" "Convert a RDF dataset into a YAML-LD Document"
    end

    subgraph Expansion
        class Dataset type
        click Dataset "/types/dataset/" "RDF Dataset"
        
        ExpandedDocument("Document\n<em><small>(expanded)</small></em>")
        CompactedDocument("Document\n<em><small>(compacted)</small></em>")
        CompactedDocument --> expand{{"expand()"}} --> ExpandedDocument
        ExpandedDocument --> compact{{"compact()"}} --> CompactedDocument
        
        class ExpandedDocument,CompactedDocument type
        click ExpandedDocument "/types/document/" "YAML-LD Document"
        click CompactedDocument "/types/document/" "YAML-LD Document"
        class expand,compact function
        
        click expand "/expand/" "Expand a YAML-LD Document"
        click compact "/compact/" "Compact a YAML-LD Document"
    end

    subgraph Parsing
        SerializedDocument("SerializedDocument") --> parse{{"parse()"}} --> ParsedDocument("Document")
        
        class SerializedDocument,ParsedDocument type
        class parse function
        
        click SerializedDocument "/types/serialized-document/" "Serialized YAML-LD document, or its location"
        click ParsedDocument "/types/document/" "Parsed YAML-LD document"
        click parse "/parse/" "Parse a YAML-LD Document"
    end
    
    subgraph Framing
        NotFramedDocument("Document\n<em><small>(not framed)</small></em>") --> frame{{"frame()"}} --> FramedDocument("Document\n<em><small>(framed)</small></em>")
        class FramedDocument type
        class NotFramedDocument type
        class frame function
        click frame "/frame/" "Frame a YAML-LD Document"
    end

    ExpandedDocument --"≡"--- Document
    CompactedDocument --"≡"--- Document
    ParsedDocument --"≡"--- Document
    DocumentRDF --"≡"--- Document
    NotFramedDocument --"≡"--- Document
    FramedDocument --"≡"--- Document
    
    classDef type     fill:#ffa724, stroke:#e68a00, stroke-width:2px, color:#fff;
    classDef function fill:#000000de, stroke:#000000de, stroke-width:2px, color:#fff, font-style:italic;
```
{% endraw %}
