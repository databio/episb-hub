# FAQ

### What kind of data is served by the *epigenome switchboard*?

> The data is anything that can be represented as collections of genomic regions. Each hub can connect to one or more data providers, which can mix both public and private data sources, enabling users to integrate data from multiple sources and to place internal data in the context of public resources for analysis.



### What is the difference between a `Segment` and a `Region`?

> A `Segment` is simply a `Region` that belongs to a `Segmentation`. In the back-end of the segmentation provider, it is assigned a `SegmentID` and can be used to [Normalize raw genome intervals](/normalize.md) into a Segmentation.

### What is a `Segmentation`?

> A `Segmentation` is a [SO::sequence_collection](http://www.sequenceontology.org/browser/current_svn/term/SO:0001260) with an additional constraint: there are *no overlapping `Region`s*. We use this to refer to a division of the genome into parts, but the segments need not cover 100% of the genome (though they may).

### What is the difference between a *segmentation provider* and a *data provider*?

> An `episb-provider` server may or may not provide segmentations. If it does, it is called a *segmentation provider*. We can consider a *segmentation provider* to be a *data provider* that happens to provide data of type `Segmentation` (and `Segment`).

> Why is the distinction important? Because ideally, most data providers will *not* provide `Segmentations` but will simply re-use those provided by a *segmentation provider*. So, there will be many fewer segmentation providers than data providers, and they are likely to be more centralized and more used. They need to be more inter-connectable and may provide different query optimization.

