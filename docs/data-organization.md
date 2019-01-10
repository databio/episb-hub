# A few notes on how data is organized in episb-provider / Elasticsearch #

Several key concepts and data structures we implement are: Segment (region), Segmentation (list of regions), Annotation. There are others (such as Experiment, Study and Author) but we will focus on the first three below.

## Segment (region) ##

A region is characterized by a Segment ID, the chromosome it is on, the start and end of the portion of the chromosome.

The JSON "view" of an example region structure is as follows:

```
{
   "segID": "testsegmentation::6299bb3d-9d07-4b45-94ae-79c3f96ef6e9",
   "segChr": "1",
   "segStart": 12137,
   "segEnd": 14537
}
```

The segID field above is a combination of the segmentation this segment belongs to (portion before "::") and a UUID randomly assigned to the segment at the time it was entered into the database (or in other words, "created"). We can then easily deduce the segmentation this segment belongs to from the segment ID.

Segments live in the "segments" index in Elastic.

## Segmentation ##

is simply a list of Segments. It is committed in Elastic like so:

```
{
    "segmentationName": "testsegmentation",
    "segmentList": [
        "testsegmentation::15f8c527-5591-4f63-8f4e-cb2ead16bb76",
        "testsegmentation::8b74bed5-c001-4cd5-aa3f-aa07e2bdfdc0",
        "testsegmentation::3fd741e5-6790-4ce4-9a97-19c8a76780f1",
        "testsegmentation::23107b1c-050d-4620-a9e5-9c6e116b01de"
    ]
}
```

Segmentations live in the "segmentations" index in Elastic.

## Annotation ##

One of the main concepts of this project is to separate annotations from the segment information. In other words, we can try and provide more "universal" segmentations (lists of segments) that hopefully, experiments can "subscribe to" and use. An annotation is then a value (as arrived at by an experiment - could be an integer, a categorical value or a float, for example) and a segment ID from a particular segmentation.

For example,

```
{
    "segmentID": "testsegmentation::8b74bed5-c001-4cd5-aa3f-aa07e2bdfdc0",
    "annValue": "0",
    "experiment": {
        "experimentName": "testexperiment",
        "experimentProtocol": "",
        "experimentCellType": "",
        "experimentSpecies": "",
        "experimentTissue": "",
        "experimentAntibody": "",
        "experimentTreatment": "",
        "experimentDescription": "Loaded from preformatted file"
    },
    "study": {
        "studyAuthor": {
            "familyName": "episb",
            "givenName": "default",
            "email": "info@episb.org"
        },
        "studyManuscript": "",
        "studyDescription": "",
        "studyDate": ""
    }
}
```

Annotations like in the "annotations" index in Elastic.
