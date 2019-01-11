# Epigenome switchboard

**The epigenome switchboard is a web app that enables scientists to integrate large-scale epigenome data across databases via an API.**

It is made up of a series of *data providers* and *data hubs* that together provide fast web and API access to data from many different public data sources. Via a [subscription interface](/howto-subscribe/), users can add new public or private data providers into their switchboards, enabling them to easily integrate their own data with other curated data resources via the hub.



<div class="image" style="float:right">
<img src="img/database_components.svg" style="width:350px; float:right; margin:20px"><br clear="all"/>
<span class="caption">Components that make up the epigenome switchboard</span>
</div>

## Project components

To build an `epigenome switchboard` requires 3 components:

### 1. A vocabulary server

The vocabulary server provides common terms so that distributed data sources can be integrated. There need only be a single vocabulary server for any number of instances of the other servers. It simply provides a permanent, static URL for common terms so that we can use [json-ld](https://json-ld.org/) to integrate data from multiple sources. Our vocabulary server buildes heavily on existing ontologies and vocabularies, including the [Sequence Ontology](http://www.sequenceontology.org/) for genomic sequence terms, [Schema.org](http://schema.org) for generic data terms, and others.

- URL: [http://bioterms.org](http://bioterms.org)
- Github: [https://github.com/databio/bioterms](https://github.com/databio/bioterms)


### 2. One or more data providers

The data provider is a generic server that hosts actual epigenome data. The data is stored as *regions* (*a.k.a.* segments, or genomic intervals). This is a RESTful server that provides access to the raw data via the [data provider API](/provider-api/) (which is still under development). There will be many data providers, and we aim to provide a packaged system so that a third party with either public or private data could fit that data into a data provider instance that would integrate with the epigenome switchboard.

Our protoype data provider is housed here:

- URL: (currently internal only, hosted via `localhost` on our dev machine)
- Github: [https://github.com/databio/episb-provider](https://github.com/databio/episb-provider)

### 3. The hub, or query overlay server

The *hub* links together data providers. A hub provides 2 things: a [web interface](http://episb.org) for user-friendly data queries, and a documented [hub API for programmatic access](/hub-api/) to integrated data. A hub connects any number of public or private data providers. Furthermore, there could be several hubs, each one connecting a different set of data providers. For example, a given hub may  focus on private data, or a certain species or data type, etc.

Our protoype hub is housed here:

- URL: [http://episb.org](http://episb.org)
- Github: [https://github.com/databio/episb-hub](https://github.com/databio/episb-hub)
