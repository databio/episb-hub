# How to use Episb API calls #

In addition to the user-browsable web interface, data hubs also provide a [RESTful API](/hub-api/) that can be queried programmatically. We encourage interested users to develop tools that operate around this API, and we also and developing a series of packages to make this easier:

## What is covered in this document ##

Below we discuss different scenarios that may come up when writing tools relying on the Episb provider API calls. Through these scenarios, the usage of the API calls is demonstrated.

*A side note:* We are currently developing an R package that will employ the data hub API to provide programmatic access to data from within `R`.

During this discussion a full URL is used where the episb-provider is running by default (http://episb.org:8080/episb-provider). Depending on how an individual installation is set up, this portion of the URL may differ from server to server.

In addition, all of the API calls return either a JsonError or a JsonSuccess object, with a general structure as follows:

JsonError:
```
{
    "result": "None",
    "error" : <error message>
}
```
JsonSuccess:
```
{
    "result": <some result>,
    "error": "None"
}
```

## Getting a list of all segmentations stored in a provider ##

To get all the region IDs belonging to a segmentation the following API call is used:
```
http://episb.org:8080/segmentations/get/all
```
If the call was successful, the following JsonSuccess structure will be returned (for example):

```
{"result":
    [
        {
            "providerName":"episb-provider",
            "providerDescription":"sample segmentation provider",
            "segmentationName":"broadhmm",
            "experimentName":"BroadHMMExperiment",
            "cellType":"sample cell type",
            "description":"sample experiment description",
            "annotationKey":"value",
            "annotationRangeStart":"0",
            "annotationRangeEnd":"0"
        },
        {
            "providerName":"episb-provider",
            "providerDescription":"sample segmentation provider",
            "segmentationName":"testsegmentation",
            "experimentName":"testexperiment",
            "cellType":"sample cell type",
            "description":"sample experiment description",
            "annotationKey":"value",
            "annotationRangeStart":"0",
            "annotationRangeEnd":"0"}]
    ],
    "error":"None"
}
```

A list of segmentation names can be extracted by traversing the JSON list in the "result" field.

## Getting a list of all region IDs within a segmentation ##

Once a segmentation name is known, a list of all region IDs within that segmentation can be obtained by calling:
```
http://episb.org:8080/segmentations/get/ByNameWithSegments/:segName
```
where "segName" is the name of a particular segmentation.

An example result may be:

```
{
    "result": 
        {
            "segmentationName":"BroadHMM",
            "segmentList":
            [
                "BroadHMM::86c7717e-7259-472c-994f-ab24926d7cd2",
                "BroadHMM::ecd009f8-97e7-4d1e-90fc-d9ca607a05af",
                "BroadHMM::c7e8d5c1-040e-4e9b-8e85-57388c690734",
                "BroadHMM::33c8f670-d4bf-4499-a7ca-59a82ca833e7",
                "BroadHMM::ff6f2e56-e309-457a-82c3-9b61d099c2a0",
                "BroadHMM::0087e086-11e3-419f-9550-7b2c3a82e3cc",
                "BroadHMM::0241364a-733d-46ec-8197-341f735a7944"
            ]
        },
    "error": "None"
}            
```

Notice that a segment ID is a concatentation of the name of segmentation_name :: UUID assigned at moment of segment ID creation.

## Getting all the regions (full info - chr/start/stop) within a segmentation ##

To get the full information on all regions within a segmentation (segment ID, chromosome, start and stop position coordinates), the following API may be used:

```
http://episb.org/segments/get/BySegmentationName/:segName
```

where segName is the name of the segmentation.

A successful call will return a structure such as:

```
{
    "result": 
    [
        {
            "segID":"BroadHMM::64443fc1-b098-4f46-9fbf-e58bfbd3fa98",
            "segChr":"X",
            "segStart":153940806,
            "segEnd":153941806
        },
        {
            "segID":"BroadHMM::00402663-7916-4c7f-9a2d-15b7c33fb1d4",
            "segChr":"X",
            "segStart":153941806,
            "segEnd":153943006
        },
        {
            "segID":"BroadHMM::258a0c7d-0070-4c22-8c97-5cb2dc59531e",
            "segChr":"X",
            "segStart":153943006,
            "segEnd":153943206
        }
    ],
    "error": "None"
}       
```

The above call may be of help when adding an experiment to the provider. The algorithm would include pulling in all the regions for a segmentation, reading the experiment .bed file line by line and searching the segmentation for the matching region.

## Getting all the regions that are within a certain coordinate position range on a chromosome ##

To do the above, the following API call may be used:
```
http://episb.org:8080/get/fromSegment/:chr/:start/:end
```
where :chr is the desired chromosome, :start and :end are the range coordinates.

A typical successful reply may be:
```
{
    "result":
    [
        {
            "segID":"TestSegmentation::deba61e4-6cd9-4630-91dc-8c5e8e9b34e6",
            "segChr":"1",
            "segStart":11737,
            "segEnd":11937
        },
        {
            "segID":"TestSegmentation::20d49fb7-df63-46af-aa07-5b9fad7f9f5a",
            "segChr":"1",
            "segStart":20337,
            "segEnd":22137
        },
        {
            "segID":"TestSegmentation::5e106bd4-de35-4f34-b607-d03800b84ab4",
            "segChr":"1",
            "segStart":12137,
            "segEnd":14537
        }
    ]
}
```

## Getting a single region based on a region ID ##

This call would take as a parameter the region ID and return a region's chromosome and positional coordinates.

*to be implemented*

## Getting all annotation values for an experiment ##

*to be implemented*

## Match APIs ##

*to be implemented once matching functionality is well understood and defined*
