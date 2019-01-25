# How to query existing data

***NB**: We have a different document that explains [how to use EPISB provider API](http://code.databio.org/episb/howto-use-episb-API-calls/) from software*

You can find our prototype hub at [episb.org](http://episb.org), which will allow you to query various public data providers using several different query options. Any of these queries can be done either via the web using the [main episb.org hub](http://episb.org), or via programmatic API. For discussion on different query types, see the `query-type` issues: [https://github.com/databio/episb-hub/issues](https://github.com/databio/episb-hub/issues). 

## Query: Retrieve regions

Given `chr`, `start` and `stop` values, the hub returns any overlapping genomic regions. 

Via API:[http://episb.org/region/1/54321/500000](http://episb.org/region/1/54321/500000).

JSON results can also be retrieved like so: [http://episb.org/api/v1/region/1/54321/500000](http://episb.org/api/v1/region/1/54321/500000).

**Biological application**. Given a query genomic region or set of regions, or a particular experiment or set of experiments, the system will be able to return a filtered set of genomic segments that link to the given inputs. For example, a user may wish to query the set of TAD boundaries (found in a particular segmentation provider) associated with an input set of transcription factor binding sites.

## Query: Segmentation filter


One  query type is a *segmentation filter*. The goal of this query type is to return a subset of a given segmentation, as determined by user-given conditions. For instance, we may want the subset of ~segments~ *regions* that have biological properties *x*, *y*, and *z*. 

To create this kind of query, the Hub UI provides a dynamic series of HTML input widgets that populate as information is added. We need to select a segmentation that the user wants to filter. One way this could work is: first, the user restricts the segmentation to those on the reference genome assembly of interest. The web GUI renders a dropdown, `Select genome`. User selects, *e.g.* `hg38`. This populates a second dropdown, `Select segmentation`. This is populated from the list of segmentations this hub knows about that segment the given reference assembly.

Once we have selected a single segmentation, we have narrowed down the data we can consider to the set of experiments that annotate that particular segmentation (which is specified in the provider design interface). We then show the user an "add condition" interface (similar to what you would see when building an email inbox filter rule). This interface is populated based on the available experiments defined in the design interface. The user can then specify any number of conditions, which can be things like:

- Value of ranged experiment `experiment1` must be "greater than 500".
- Value of binary experiment `experiment3` must be "True"

When the user is done assembling the desired list of conditions, she clicks `submit`. Conditions are translated into a query, which returns **the set of ~segments~ *regions* that meet all conditions**.

Ideally, this *segmentation filter* query is also possible to construct via a *POST* of a *json* document, so that someone could be an R/python interface to pull down the same queries. The result should be returnable either in [BED format](https://genome.ucsc.edu/FAQ/FAQformat.html#format1) or as a `JSON`.

**Biological application**. This query type can be thought of as translating annotation limits into region sets (Retrieving integrated region sets). For example, give me the set of regions with annotation values above *x* in cell-type *y* but below *a* in cell-types *b*, *c*, and *d*. A more complicated example: a user could request that the system return the set of genomic regions that are annotated as filling the following four critera: First, they have open chromatin in macrophages, but not in other hematopoietic cell types, as defined by the ENCODE cross cell-type chromatin analysis; second, they have H3K27ac in M1 macrophages but not in M2 macrophages, as defined by the BLUEPRINT project data; third, they are polycomb repressed in hematopoietic stem cells, as defined by data from the Roadmap Epigenomics project; and fourth, they are within a set of regions defined as CRISPR-targetable in private lab-specific experimental results.

## Query: Segmentation Match

Given a set of "regions", we need to convert these into "Segmentation Regions" (normalized regions).

## Query: Annotations

Given a query region, retrieve experimental annotations. For example, entering something like *DHS::9ff55240-9dd1-42ed-a963-98b127d09793* should bring up all the annotations from all the experiments currently stored within the provider that are linked with the DHS segmentation and the particular region within it.

Via API: [http://episb.org/annotations/DHS::9ff55240-9dd1-42ed-a963-98b127d09793](http://episb.org/annotations/DHS::9ff55240-9dd1-42ed-a963-98b127d09793)

JSON results can also be retrieved by going to [http://episb.org/api/v1/annotations/DHS::9ff55240-9dd1-42ed-a963-98b127d09793](http://episb.org/api/v1/annotations/DHS::9ff55240-9dd1-42ed-a963-98b127d09793)).

**Biological application**. given a set of genetic variants from a GWAS study, return the functional annotations across data providers for each disease-associated SNP.
