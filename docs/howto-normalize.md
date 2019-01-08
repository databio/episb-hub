# How-to normalize interval data


## Why do we need to normalize genome interval data?

In a traditional analysis of epigenome data, the data are produced as genomic intervals. Think of a set of ChIP-seq peaks, for example. We use some type of 'peak caller' to identify particular genomic regions that are of interest.

When it comes time to compare these regions among samples, we are faced with the challenge of comparing sets of hundreds of thousands of intervals which do not match. For example, a particular peak in one sample may not be present in another. Or, the peak in one sample may overlap another sample imperfectly. This leads to a challenge with comparison: how do you determine which of these different annotations refer to the same biological entity, so that you can compare that entity among samples? 

The typical analysis uses an *ad hoc* approach to solve this. Using some type of interval arithmetic, such as merging intervals, testing for overlaps, or such, a set of "master peaks" is constructed, and this peak list is then assessed for signal in each sample. With a common reference, the samples can now be much more easily compared.

However, these "master peak" lists are usually re-created, again and again, for each project. Comparing data across projects, then requires a similar procedure, and 

## What is the alternative?

The episb approach is simple: instead of doing an *ad hoc* peak merging procedure separately for each project, do these based on a well-defined set of pre-defined genome segments. Using these universal identifiers, it becomes much simpler to integrate data across experiments.

## How does episb accomplish this?

Through our *Segmentation match* approach, when presented with a new dataset, we *first* normalize the genomic intervals to an existing `Segmentation`. This dataset is then immediately comparable with *any other dataset that annotates that `Segmentation`*.

