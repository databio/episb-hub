# Epigenome switchboard

## Project components

A complete `epigenome switchboard` consists of 3 different types of servers:

### 1. Vocabulary server

The vocabulary server provides common terms so that distributed data sources can be integrated. There need only be a single vocabulary server for any number of instances of the other servers. It simply provides a permanent, static URL for common terms so that we can use [json-ld](https://json-ld.org/) to integrate data from multiple sources.

- URL: http://bioterms.org
- Github: https://github.com/databio/bioterms


### 2. Data provider (could be called a `spoke` ?)

The data provider is a generic server that hosts actual epigenome data. The data is stored as intervals (*a.k.a.* segments, or genome regions). This is a RESTful server that provides access to the raw data via the *Data provider API* (which is still under development). There will be many data providers, and we aim to provide a packaged system so that a third party with either public or private data could fit that data into a data provider instance that would integrate with the epigenome switchboard.

Our protoype data provider is housed here:

- URL: (currently internal only, hosted via `localhost` on our dev machine)
- Github: https://github.com/databio/episb-provider

### 3. Hub, or query overlay server

The *hub* links together data providers. A hub provides 2 things: a web interface for user-friendly data queries, and a documented API for programmatic access to integrated data. A hub connects any number of public or private data providers. Furthermore, there could be several hubs, each one connecting a different set of data providers. For example, a given hub may  focus on private data, or a certain species or data type, etc.

Our protoype hub is housed here:

- URL: http://episb.org
- Github: https://github.com/databio/episb-hub


## Interfaces

In addition to the 3 primary server components, we must formalize the relationships between those components. 

### 1. Data provider API

The data provider API will describe the link between a *provider* and a *hub*. One aspect of this will be the `provider design interface` (described below).

### 2. User-facing hub API

We also need a documented API for users to interact with the hub. We will ultimately build R/python packages to query these servers, so we need a standard API to do so.

## Provider design interface

In to link a provider to a hub, we must specify an interface for that connection, which we call the `provider design interface` (other suggestions for a name?). Each data provider must provide this `design interface`, which is essentially a summary of what kind of data the provider provides. Here is an example of such an interface, which describes 3 experiments that all subscribe to one segmentation:

```
{ 
	"provider_name": "regdb"
	"provider_description" : "Shefflab Regulatory Elements Data Provider"
	"segmentations": [
		{"@id": "http://episb.org/segmentations/DHS",
			"experiments": [
			{"@id": "experiment1", 
			"celltype: "HUVEC",
			"description": "ChIP-seq in HUVEC cells for factor X", 
			"annotation_key": "value",
			"annotation_range_start": 0,
			"annotation_range_end": 1000}, 
			{"@id": "experiment2", 
			"celltype: "MSC",
			"description": "ChIP-seq in MSC cells for factor Y", 
			"annotation_key": "value",
			"annotation_range_start": 0,
			"annotation_range_end": 1000}, 		
			{"@id": "experiment3", 
			"description": "CpG island annotation", 
			"annotation_key": "value",
			"annotation_range_start": 0,
			"annotation_range_end": 1}, 		
			]
		}]

}

```

## Hub links

The hub needs a way for a user to *link* external data providers by providing this `design interface`. This should just be a text field with a submit button where the user submits a URL (similar to the way UCSC track hubs work). That URL should point to the above `design interface` file (or API point, perhaps?). The hub then parses this information into a form that it knows what data is availble from which provider, and how to query it.

Armed with information from one or more provider design interfaces, the hub is prepared to render a web UI to allow a user to make queries.

## Segmentation filter query

One possible query type could be called a *segmentation filter*. The goal of this query type is to return a subset of a given segmentation, as determined by user-given conditions. For instance, we may want the subset of segments that have biological properties *x*, *y*, and *z*. 

To create this kind of query, the Hub UI provides a dynamic series of HTML input widgets that populate as information is added. We need to select a segmentation that the user wants to filter. One way this could work is: first, the user restricts the segmentation to those on the reference genome assembly of interest. The web GUI renders a dropdown, `Select genome`. User selects, *e.g.* `hg38`. This populates a second dropdown, `Select segmentation`. This is populated from the list of segmentations this hub knows about that segment the given reference assembly.

Once we have selected a single segmentation, we have narrowed down the data we can consider to the set of experiments that annotate that particular segmentation (which is specified in the provider design interface). We then show the user an "add condition" interface (similar to what you would see when building an email inbox filter rule). This interface is populated based on the available experiments defined in the design interface. The user can then specify any number of conditions, which can be things like:

- Value of ranged experiment `experiment1` must be "greater than 500".
- Value of binary experiment `experiment3` must be "True"

When the user is done assembling the desired list of conditions, she clicks `submit`. Conditions are translated into a query, which returns **the set of segments that meet all conditions**.

Ideally, this *segmentation filter* query is also possible to construct via a *POST* of a *json* document, so that someone could be an R/python interface to pull down the same queries. The result should be returnable either in [BED format](https://genome.ucsc.edu/FAQ/FAQformat.html#format1) or as a `JSON`.

# Epigenome switchboard hub

A simple Flask web application to interact with the [episb-rest-server](https://github.com/databio/episb/tree/master/episb-rest-server)

## Search

Current functionality is to search by START and STOP values. Results can be searched by hand from the home page episb.org or passed as URL parameters:

    http://episb.org/segment/54321/500000

JSON results can also be retrieved, add `/json/` to the endpoint:

    http://episb.org/segment/json/54321/500000

Additional queries will be added in the near future.


## Example queries for user-facing query API

1. Translating annotation limits into region sets (Retrieving integrated region sets). For example, give me the set of regions with annotation values above *x* in cell-type *y* but below *a* in cell-types *b*, *c*, and *d*. A more complicated example: a user could request that the system return the set of genomic regions that are annotated as filling the following four critera: First, they have open chromatin in macrophages, but not in other hematopoietic cell types, as defined by the ENCODE cross cell-type chromatin analysis; second, they have H3K27ac in M1 macrophages but not in M2 macrophages, as defined by the BLUEPRINT project data; third, they are polycomb repressed in hematopoietic stem cells, as defined by data from the Roadmap Epigenomics project; and fourth, they are within a set of regions defined as CRISPR-targetable in private lab-specific experimental results.

2. Retrieving segmentations. Given a query genomic region or set of regions, or a particular experiment or set of experiments, the system will be able to return a filtered set of genomic segments that link to the given inputs. For example, a user may wish to query the set of TAD boundaries (found in a particular segmentation provider) associated with an input set of transcription factor binding sites.

3. Retrieving annotations for a given region or region set. For example, the user provides a set of genomic regions and wants to retrieve all annotations for those regions. Biological use cases: given a set of genetic variants from a GWAS study, return the functional annotations across data providers for each disease-associated SNP.

