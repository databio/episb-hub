# Data provider API

The data provider API will describe the link between a *provider* and a *hub*. One aspect of this will be the `provider design interface`. Discussion on this interface can be found in this issue: [https://github.com/databio/episb-provider/issues/6](https://github.com/databio/episb-provider/issues/6)

Below we discuss different scenarios that may come up when writing tools relying on the Episb provider API calls. Through these scenarios, the usage of the API calls is demonstrated.

## What is covered in this document ##

During this discussion a full URL is used where the episb-provider is running by default at (*http://provider.episb.org/episb-provider*). 

Depending on how an [individual installation is set up](http://code.databio.org/episb/howto-build-provider/), this URL will differ from server to server.

## Types of results returned ##

All of the API calls to an EPISB provider return either a JsonError or a JsonSuccess object, with general structures as follows:

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

Following are all the REST APIs supported by the provider.

## Getting a list of all design interfaces stored in the provider ##

The following call is used to get all the design interfaces stored in the provider.
```
GET /segmentations/get/all
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

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "episb-provider/segmentations/get/all")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"providerName":"episb-provider","providerDescription":"sample segmentation provider","segmentationName":"testsegmentation","experimentName":"testexperiment","cellType":"sample cell type","description":"sample experiment description","annotationKey":"value","annotationRangeStart":"0","annotationRangeEnd":"0"},{"providerName":"episb-provider","providerDescription":"sample segmentation provider","segmentationName":"broadhmm","experimentName":"BroadHMMExperiment","cellType":"sample cell type","description":"sample experiment description","annotationKey":"value","annotationRangeStart":"0","annotationRangeEnd":"0"}],"error":"None"}'
```

Via API: [http://provider.episb.org/episb-provider/segmentations/get/all](http://provider.episb.org/episb-provider/segmentations/get/all)

## Getting a list of all region IDs within a segmentation ##

Once a segmentation name is known, a list of all region IDs within that segmentation can be obtained by calling:
```
GET /segmentations/get/ByName/:segName
```

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

**Input**: :segName is the name of a particular segmentation, for example "BroadHMM".

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/segmentations/get/ByName/BroadHMM")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"segmentationName":"BroadHMM","segmentList":["BroadHMM::d9d7d23b-658c-43c3-a34a-94939b6403c9","BroadHMM::81f79f42-a06d-44a2-80d1-aed913a7442c","BroadHMM::3433568d-bbb7-4c41-be7e-0b00dd48f096","BroadHMM::365d4660-85af-4841-8643-d2b7f8eb2839","BroadHMM::f9650174-71fa-4df5-944e-9ba9cf6402a8","BroadHMM::525bca34-44df-4c78-be56-558915f603fd","BroadHMM::a0a6d44d-7820-47b1-a70e-f56d0abc0d95","BroadHMM::cef16c99-8d4f-4a92-9a10-0163e38014c3","BroadHMM::177f1523-1e47-47b9-8b11-1f548b7beaa2","BroadHMM::c93addab-a323-456b-990c-9eacdb3b896e","BroadHMM::92034f77-9462-4d23-ae8e-3bacfbcce507","BroadHMM::cf1d7a33-c197-4be8-beff-b317a5234e75","BroadHMM::1dc51ea0-0fea-4ef8-b217-3cc64e98be10","BroadHMM::5acb2c06-fb6d-436f-9894-f339c219241e","BroadHMM::808010d6-6676-4731-9962-3691e6ca392f"]}],"error":"None"}'
```

Via API: [http://provider.episb.org/episb-provider/segmentations/get/ByName/BroadHMM](http://provider.episb.org/episb-provider/segmentations/get/ByName/BroadHMM)

## Getting all the regions (full info - chr/start/stop) within a segmentation ##

To get the full information on all regions within a segmentation (segment ID, chromosome, start and stop position coordinates), the following API may be used:

```
GET /segments/get/BySegmentationName/:segName
```

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

**Input**: :segName is the name of the segmentation. For example, "BroadHMM".

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/segments/get/BySegmentationName/BroadHMM")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"segID":"BroadHMM::3433568d-bbb7-4c41-be7e-0b00dd48f096","segChr":"X","segStart":153889606,"segEnd":153890206},{"segID":"BroadHMM::30f54ade-c14e-43be-b37d-2349f7960809","segChr":"X","segStart":153952006,"segEnd":153953406},{"segID":"BroadHMM::826f9efe-0931-48a5-b2fc-a6117ad69e28","segChr":"X","segStart":153962406,"segEnd":153962606},{"segID":"BroadHMM::6093072b-538b-4668-ab5c-3b9bad6a8ef8","segChr":"X","segStart":153978406,"segEnd":153979206},{"segID":"BroadHMM::be702e3c-f568-47fb-9717-068d4e98fcb4","segChr":"X","segStart":153988606,"segEnd":153989806},{"segID":"BroadHMM::9098ae95-6d7f-42e5-bb0b-872c9fff599b","segChr":"X","segStart":153992406,"segEnd":153992606},{"segID":"BroadHMM::40bd6776-a35b-4c0a-88e2-4a4f5c086d39","segChr":"X","segStart":154012406,"segEnd":154028606},{"segID":"BroadHMM::d7a25dae-3031-4ebf-a70a-9cd6cea196f8","segChr":"X","segStart":154029206,"segEnd":154029806},{"segID":"BroadHMM::12fbd660-eec5-4394-b662-3d37317d8aa8","segChr":"X","segStart":154055406,"segEnd":154055806},{"segID":"BroadHMM::01237fc3-e992-4e88-bb80-a7ec32538b5b","segChr":"X","segStart":154057206,"segEnd":154057806},{"segID":"BroadHMM::85904995-9c0c-4817-8345-142cf4f5dab2","segChr":"X","segStart":154112206,"segEnd":154113006},{"segID":"BroadHMM::8efb2e19-1428-4fdc-8b50-ac48143c6824","segChr":"X","segStart":154113006,"segEnd":154113606}],"error":"None"}'
```

Via API: [http://provider.episb.org/episb-provider/segments/get/BySegmentationName/BroadHMM](http://provider.episb.org/episb-provider/segments/get/BySegmentationName/BroadHMM)

To obtain the same output in BED file format, append ?format=bed to the query. For example: [http://provider.episb.org/episb-provider/segments/get/BySegmentationName/BroadHMM?format=bed](http://provider.episb.org/episb-provider/segments/get/BySegmentationName/BroadHMM?format=bed)

## Getting all the regions that are within a certain coordinate position range on a chromosome ##

To do the above, the following API call may be used:
```
GET /segments/get/fromSegment/:chr/:start/:end
```

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

**Input**:
    :segChr can be something like "chr1" or just "1"
    :start and :stop are integer coordinates, where start<stop

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/segments/get/fromSegment/chr1/20000/40000")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"segID":"testsegmentation::66114507-120a-439c-988b-fe28cdad95f4","segChr":"1","segStart":22137,"segEnd":22937},{"segID":"testsegmentation::f606b4f4-3ffa-4780-89b4-e941b930cf15","segChr":"1","segStart":26937,"segEnd":27537},{"segID":"testsegmentation::fb3a9df2-ab10-449f-b696-d1a10191e647","segChr":"1","segStart":28537,"segEnd":29737},{"segID":"testsegmentation::dd796ae7-4250-44c4-99a3-639ebd156272","segChr":"1","segStart":30137,"segEnd":30337},{"segID":"testsegmentation::7b305233-8a37-4f07-baed-e44e6c610560","segChr":"1","segStart":27537,"segEnd":28537},{"segID":"testsegmentation::fdea5adf-a454-4a5a-a738-8ceb30df7cf7","segChr":"1","segStart":14537,"segEnd":20337},{"segID":"testsegmentation::dd23cff7-02c1-4ed1-b22c-2324fe8c4909","segChr":"1","segStart":29737,"segEnd":30137},{"segID":"testsegmentation::e45e0b9f-0463-45d3-b2b2-d856333e52ba","segChr":"1","segStart":20337,"segEnd":22137},{"segID":"testsegmentation::cd227dea-7247-4add-98e5-b4f94e626bc2","segChr":"1","segStart":22937,"segEnd":26937},{"segID":"testsegmentation::9b34b568-6a6b-4273-b706-9dc71814124c","segChr":"1","segStart":30337,"segEnd":36937}],"error":"None"}'
```

or, this would work equally well:
```
conn.request("GET", "/episb-provider/segments/get/fromSegment/1/20000/40000")
```

Via API: [http://provider.episb.org/episb-provider/segments/get/fromSegment/1/20000/40000](http://provider.episb.org/episb-provider/segments/get/fromSegment/1/20000/40000)

To obtain the same output in BED file format, append ?format=bed to the query. For example: [http://provider.episb.org/episb-provider/segments/get/fromSegment/1/20000/40000?format=bed](http://provider.episb.org/episb-provider/segments/get/fromSegment/1/20000/40000?format=bed)

## Getting a single region based on a region ID ##

This call takes as a parameter the region ID and returns a region's chromosome and positional coordinates.
```
GET /segments/find/BySegmentID/:segmentID
```

A typical reply would be:
```
{
    "result":
        [
            {
                "segID":"TestSegmentation::2a43bb7b-d35d-4193-8941-e8a2d232ee95",
                "segChr":"1",
                "segStart":22137,
                "segEnd":22937
            }
        ],
        "error":"None"
}
```

**Input** :segmentID is something like "TestSegmentation::2a43bb7b-d35d-4193-8941-e8a2d232ee95"

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/segments/find/BySegmentID/testsegmentation::512b13b3-67cd-46ef-87c8-0c7579e2304d")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"segID":"testsegmentation::512b13b3-67cd-46ef-87c8-0c7579e2304d","segChr":"1","segStart":10000,"segEnd":10600}],"error":"None"}'
```

Via API: [http://provider.episb.org/episb-provider/segments/find/BySegmentID/DHS::821fd8a9-1de4-4207-a03d-544f07be4bdd](http://provider.episb.org/episb-provider/segments/find/BySegmentID/DHS::821fd8a9-1de4-4207-a03d-544f07be4bdd)

To obtain the same output in BED file format, append ?format=bed to the query. For example: [http://provider.episb.org/episb-provider/segments/find/BySegmentID/DHS::821fd8a9-1de4-4207-a03d-544f07be4bdd?format=bed](http://provider.episb.org/episb-provider/segments/find/BySegmentID/DHS::821fd8a9-1de4-4207-a03d-544f07be4bdd?format=bed)

## Getting all annotation values for an experiment ##

A user may be interested in obtaining all the annotations committed with an experiment. The following call provides this information:
```
GET /experiments/get/ByName/:expName?op1=operation&val1=value&op2=operation&val2=value
```

The range of annotation values can be restricted/filtered by the use of op1/op2 operations and val1/val2 values.

**Input**: :expName is the name of the experiment, such as "BroadHMM"
           :op1 and op2 are one of [gte,lte,eq]
           :val1 and val2 are values in the range of annotation values for an experiment

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/experiments/get/ByName/BroadHMMExperiment")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"segmentID":"BroadHMM::365d4660-85af-4841-8643-d2b7f8eb2839","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}},{"segmentID":"BroadHMM::826f9efe-0931-48a5-b2fc-a6117ad69e28","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}},{"segmentID":"BroadHMM::4aea194d-8a69-4839-b698-41ec8602662d","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}},{"segmentID":"BroadHMM::4d30c911-54dd-469e-9595-6a7042270d0b","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}}],"error":"None"}'
```

Via API: [http://provider.episb.org/episb-provider/experiments/get/ByName/CLL](http://provider.episb.org/episb-provider/experiments/get/ByName/CLL) or [http://provider.episb.org/episb-provider/experiments/get/ByName/CLL?op1=gte&val1=0.7](http://provider.episb.org/episb-provider/experiments/get/ByName/CLL?op1=gte&val1=0.7) or 

## Getting all annotation values associated with a segmentation ##

A user may be interested in obtaining all the annotations associated with a particular segmentation. Note that annotations from different experiments may use the same segmentation.
```
GET /experiments/get/BySegmentationName/:segName?matrix=true
```

**Input**: :segName is the name of the segmentation, such as "BroadHMM" or "TestSegmentation"
           :if ?matrix=true, return a matrix where each row is a tuple (segmentID, annotationValue)

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/experiments/get/BySegmentationName/BroadHMM")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"segmentID":"BroadHMM::365d4660-85af-4841-8643-d2b7f8eb2839","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}},{"segmentID":"BroadHMM::826f9efe-0931-48a5-b2fc-a6117ad69e28","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}},{"segmentID":"BroadHMM::4aea194d-8a69-4839-b698-41ec8602662d","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}},{"segmentID":"BroadHMM::4d30c911-54dd-469e-9595-6a7042270d0b","annValue":"0","experiment":{"experimentName":"BroadHMMExperiment","experimentProtocol":"","experimentCellType":"","experimentSpecies":"","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":"Loaded from preformatted file"},"study":{"studyAuthor":{"familyName":"episb","givenName":"default","email":"info@episb.org"},"studyManuscript":"","studyDescription":"","studyDate":""}}],"error":"None"}'
```

Via API: [http://provider.episb.org/episb-provider/experiments/get/BySegmentationName/BroadHMM](http://provider.episb.org/episb-provider/experiments/get/BySegmentationName/BroadHMM) or [http://provider.episb.org/episb-provider/experiments/get/BySegmentationName/BroadHMM?matrix=true](http://provider.episb.org/episb-provider/experiments/get/BySegmentationName/BroadHMM?matrix=true)

If using ?matrix=true and if the caller indicates that they can accept compressed results, the API will return a compressed .gz file as a result:

```
curl -H "Accept-Encoding: gzip" http://provider.episb.org/episb-provider/experiments/get/BySegmentationName/broad?matrix=true --output some_file.gz
```

## Getting all annotation values associated with a particular region ID ##

A user may be interested in obtaining all the annotations associated with a particular region ID. Note that the same region ID may be associated with different annotations in different experiments.
```
GET /experiments/get/ByRegionID/:regionID
```

**Input**: :regionID is the id of the region in question, e.g. "BroadHmm::63b4f4bb-f7c0-482a-88a3-875e2356670e"

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/experiments/get/ByRegionID/BroadHmm::63b4f4bb-f7c0-482a-88a3-875e2356670e")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
'{"result":[{"segmentID":"BroadHmm::63b4f4bb-f7c0-482a-88a3-875e2356670e","annValue":0.0,"experiment":{"experimentName":"Gm12878","experimentProtocol":"","experimentCellType":"","experimentSpecies":"Human","experimentTissue":"","experimentAntibody":"","experimentTreatment":"","experimentDescription":""},"study":{"studyAuthor":{"familyName":"Default","givenName":"Author","email":"info@episb.org"},"studyManuscript":"Default Manuscript","studyDescription":"","studyDate":""}}],"error":"None"}'
```

Via API: [http://provider.episb.org/episb-provider/experiments/get/ByRegionID/BroadHmm::63b4f4bb-f7c0-482a-88a3-875e2356670e](http://provider.episb.org/episb-provider/experiments/get/ByRegionID/BroadHmm::63b4f4bb-f7c0-482a-88a3-875e2356670e)

## Getting a list of all segmentation IDs (names) ##

This API point can be used to obtain a list of all the segmentations kept within the provider.
```
GET /segmentations/list/all
```

**Input**: None

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/episb-provider/segmentations/list/all")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
{"result":["testsegmentation","broadhmm"],"error":"None"}
```

Via API: [http://provider.episb.org/episb-provider/segmentations/list/all](http://provider.episb.org/episb-provider/segmentations/list/all)

## Getting a list of all experiment IDs (names) associated with a particular segmentation ##

One of the objectives of EPISB is to separate the implicit pairing of an annotation with a region (as in within a .bed file). EPISB forces this separation and provides the concept of a segmentation (a list of regions) which makes an experiment an explicit pairing between an annotation value and a region ID provided by a segmentation. Use this API call to obtain all the experiment IDs connected with a particular segmentation ID (name).
```
GET /experiments/list/BySegmentationName/:segName
```

**Input**: :segName is the name of the segmentation we are interested in

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/experiments/list/BySegmentationName/broadhmm")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
{"result":["BroadHMMExperiment"],"error":"None"}
```

In this example we have only one experiment that was tied to a segmentation.

Via API: [http://provider.episb.org/episb-provider/experiments/list/BySegmentationName/broadhmm](http://provider.episb.org/episb-provider/experiments/list/BySegmentationName/broadhmm)

## Getting a full description of an experiment associated with a particular segmentation ##

Continuing with the above theme, sometimes we do not want just the list of all the experiment IDs connected with a segmentation. Instead, we want the whole description of the experiment, its annotation value range and key and other pertinent information. The following API point provides this information.

```
GET /experiments/list/full/BySegmentationName/:segName
```

**Input**: segName is the name of the segmentation in question

Example:
```
import httplib
conn = httplib.HTTPConnection("provider.episb.org")
conn.request("GET", "/experiments/list/full/BySegmentationName/broadhmm")
r1 = conn.getresponse()
print(r1.read())
```
would produce something like:
```
{"result":[{"providerName":"episb-provider","providerDescription":"sample segmentation provider","segmentationName":"broadhmm","experimentName":"BroadHMMExperiment","cellType":"sample cell type","description":"sample experiment description","annotationKey":"value","annotationRangeStart":"0","annotationRangeEnd":"1"}],"error":"None"}
```

Via API: [http://provider.episb.org/episb-provider/experiments/list/full/BySegmentationName/broadhmm](http://provider.episb.org/episb-provider/experiments/list/full/BySegmentationName/broadhmm)

## Match APIs ##

*to be implemented once matching functionality is well understood and defined*
