# Epigenome switchboard

The epigenome switchboard is a loosely coupled collection of web servers and data resources that together form a network for analysis of epigenome data. The data contained in the network is anything that can be represented as collections of genomic regions. The switchboard provides hubs that allow users to interact with the data through RESTful API endpoints, or via interactive web interface. Each hub can connect to one or more data providers, which can mix both public and private data sources, enabling users to integrate data from multiple sources and to place internal data in the context of public resources for analysis.


## Project components

To build an `epigenome switchboard` requires 3 components:

### 1. A vocabulary server

The vocabulary server provides common terms so that distributed data sources can be integrated. There need only be a single vocabulary server for any number of instances of the other servers. It simply provides a permanent, static URL for common terms so that we can use [json-ld](https://json-ld.org/) to integrate data from multiple sources. Our vocabulary server buildes heavily on existing ontologies and vocabularies, including the [Sequence Ontology](http://www.sequenceontology.org/) for genomic sequence terms, [Schema.org](http://schema.org) for generic data terms, and others.

- URL: http://bioterms.org
- Github: https://github.com/databio/bioterms


### 2. One or more data providers (could be called a `spoke` ?)

The data provider is a generic server that hosts actual epigenome data. The data is stored as *regions* (*a.k.a.* segments, or genomic intervals). This is a RESTful server that provides access to the raw data via the *Data provider API* (which is still under development). There will be many data providers, and we aim to provide a packaged system so that a third party with either public or private data could fit that data into a data provider instance that would integrate with the epigenome switchboard.

Our protoype data provider is housed here:

- URL: (currently internal only, hosted via `localhost` on our dev machine)
- Github: https://github.com/databio/episb-provider

### 3. The hub, or query overlay server

The *hub* links together data providers. A hub provides 2 things: a web interface for user-friendly data queries, and a documented API for programmatic access to integrated data. A hub connects any number of public or private data providers. Furthermore, there could be several hubs, each one connecting a different set of data providers. For example, a given hub may  focus on private data, or a certain species or data type, etc.

Our protoype hub is housed here:

- URL: http://episb.org
- Github: https://github.com/databio/episb-hub


## Interfaces

In addition to the 3 primary server components, we must formalize the relationships between those components. 

### 1. Data provider API

The data provider API will describe the link between a *provider* and a *hub*. One aspect of this will be the `provider design interface`. Discussion on this interface can be found in this issue: https://github.com/databio/episb-provider/issues/6

### 2. User-facing hub API

We also need a documented API for users to interact with the hub. We will ultimately build R/python packages to query these servers, so we need a standard API to do so.

# Epigenome switchboard hub

The hub code itself it hosted in this repository. It is a simple Flask web application to interact with the data provider.

## Search

Current functionality is to search by START and STOP values. Results can be searched by hand from the home page episb.org or passed as URL parameters:

    http://episb.org/segment/54321/500000

JSON results can also be retrieved, add `/json/` to the endpoint:

    http://episb.org/segment/json/54321/500000

Additional queries will be added in the near future.


## Example queries for user-facing query API

For discussion on different query types, see the `query-type` issues: https://github.com/databio/episb-hub/issues

1. Translating annotation limits into region sets (Retrieving integrated region sets). For example, give me the set of regions with annotation values above *x* in cell-type *y* but below *a* in cell-types *b*, *c*, and *d*. A more complicated example: a user could request that the system return the set of genomic regions that are annotated as filling the following four critera: First, they have open chromatin in macrophages, but not in other hematopoietic cell types, as defined by the ENCODE cross cell-type chromatin analysis; second, they have H3K27ac in M1 macrophages but not in M2 macrophages, as defined by the BLUEPRINT project data; third, they are polycomb repressed in hematopoietic stem cells, as defined by data from the Roadmap Epigenomics project; and fourth, they are within a set of regions defined as CRISPR-targetable in private lab-specific experimental results.

2. Retrieving segmentations. Given a query genomic region or set of regions, or a particular experiment or set of experiments, the system will be able to return a filtered set of genomic segments that link to the given inputs. For example, a user may wish to query the set of TAD boundaries (found in a particular segmentation provider) associated with an input set of transcription factor binding sites.

3. Retrieving annotations for a given region or region set. For example, the user provides a set of genomic regions and wants to retrieve all annotations for those regions. Biological use cases: given a set of genetic variants from a GWAS study, return the functional annotations across data providers for each disease-associated SNP.


# Running the app for development

```
FLASK_APP="main.py" flask run
```

Point browser to http://localhost:5000


# Running the app in a container

To build the episb-hub container locally and test, follow these steps:

1. In the same directory as the `Dockerfile`:

```
$ docker build -t <docker image>:<tag optional> .
```

2. Run the container from the image you just built:

```
$ docker run -d -p 80:80 <docker image>:<tag>
```

3. Interact with and preview the site: http://localhost/ 
