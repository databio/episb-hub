# How to add an experiment using the episb API #

The discussion below makes the following assumptions:

<ul>
<li>Annotations cannot exist independently in the system - they must be connected to existing segments withni segmentations</li>
<li>The user of the "add experiment" API "knows" the name of the segmentation to use</li>
<li>Right now, for each chr/start/stop (range) associated with an annotation value, only an **exact** match within a segmentation can be used (in other words, the system still does not know how to make partial matches)</li>
</ul>

With the above being said, the REST API point to use is:

```
/experiments/add/preformatted/:experimentName/:segmentationName
```

where 
<ul>
<li>"experimentName" is the desired name of the experiment</li>
<li>"segmentationName" is the name of the segmentation to search for matches</li>
</ul>

The above is a POST multi-form method that expects within its body the following:
```
annotation value\<tab\>segmentID
```

Another useful REST API point to use when adding an experiment is:
```
/segments/get/BySegmentationName/:segmentationName
```

where "segmentationName" is the name of the segmentation to get all the segments for (with associated IDs, chr, start and stop information).

The full workflow to add an experiment, therefor is:

<ul>
<li>Use "/segments/get/BySegmentationName/:segmentationName" to "pull in" all the segments for a segmentation</li>
<li>Read experiment BED file and extract chr/start/stop/annotation_value information from it</li>
<li>Search all downloaded segments for an exact match</li>
<ul>
<li>if a match is found, add annotation_value\<tab\>segmentID to body of the POST form to use next</li>
<li>if a match is NOT found, either skip adding annotation or add "dummy" annotation</li>
</ul>
<li>When the whole experiment BED file is processed, use resulting multi-form and /experiments/add/preformatted/:experimentName/:segmentationName to add annotations to episb-system</li>
<li>Finally, we need to "officialize" the addition of the experiment by adding a "design interface" to the system, describing the experiment/segmentation pairing (see below)</li>
</ul>

The REST API point to add the design interface is:
```
/segmentations/update
```
It is a POST method where the request body contains JSON formatted as described [here](http://code.databio.org/episb/data-organization/#design-interface)

The episb code base already contains a program that will perform the above task. To use it, do the following:

```
git clone https://github.com/databio/episb-provider.git
cd episb-provider/episb-utils
```

The actual code to run would be:
```
SBT_OPTS="-Xmx16G" sbt "runMain com.github.oddodaoddo.sheffieldapp.ProcessAnnotationNonHeadered --segname="segmentation name" --expname="my experiment name" --readfrom=/home/ognen/"bed file containing experiment" --writeto=/tmp/output.txt --column=<column to get annotation value from>"
```

For example, to load an experiment that lives /home/ognen/wgEncodeBroadHmmGm12878HMM.bed, using the "encodebroadhmm" segmentation, run:
```
SBT_OPTS="-Xmx16G" sbt "runMain com.github.oddodaoddo.sheffieldapp.ProcessAnnotationNonHeadered --segname=encodebroadhmm --expname="EncodeBroadExperiment" --readfrom=/home/ognen/wgEncodeBroadHmmGm12878HMM.bed --writeto=/tmp/output.txt --column=4"
```

The /tmp/output.txt is where the annotation/segmentID pairings will be accumulated, in order to create the multi-form necessary for the usage of the APIs. The file can be perused to verify contents and can be discarded after the program has finished running.
