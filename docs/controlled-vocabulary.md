# Vocabulary server

The vocabulary server provides common terms so that distributed data sources can be integrated. There need only be a single vocabulary server for any number of instances of the other servers. It simply provides a permanent, static URL for common terms so that we can use [json-ld](https://json-ld.org/) to integrate data from multiple sources. Our vocabulary server buildes heavily on existing ontologies and vocabularies, including the [Sequence Ontology](http://www.sequenceontology.org/) for genomic sequence terms, [Schema.org](http://schema.org) for generic data terms, and others.

- URL: [http://bioterms.org](http://bioterms.org)
- Github: [https://github.com/databio/bioterms](https://github.com/databio/bioterms)
