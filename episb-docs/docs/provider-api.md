# Data provider API

The data provider API will describe the link between a *provider* and a *hub*. One aspect of this will be the `provider design interface`. Discussion on this interface can be found in this issue: [https://github.com/databio/episb-provider/issues/6](https://github.com/databio/episb-provider/issues/6)


*/segmentations/get/ByNameWithSegments/:segmentationName?compressed=true/false (GET)*

Returns a segmentation from elastic search (a list of segments with their IDs)

*/experiments/add/preformatted/:experimentName/:segmentationName (POST)*

Takes in a file formatted such as: "annotation_value\<tab\>segmentation_name::segment_id"

Right now we are not verifying much. It is the responsibility of the caller to make sure the segmentation exists.
The file to feed this API point can be produced by running the following from episb-bed-json-converter suite of programs:

cd ../episb-bed-json-converter
SBT_OPTS="-Xmx12G" sbt "runMain com.github.oddodaoddo.sheffieldapp.ProcessAnnotationNonHeadered --segname=name_of_segmentation --expname=name_of_experiment --readfrom=path_to_experiment_bed_file --writeto=path_to_output_file --column=colummn_to_use_for_annotation_value"

the SBT_OPTS above is optional but recommended.

To call the API point, create a following file (e.g. /tmp/multipart-message.data

--a93f5485f279c0
content-disposition: form-data; name="expfile"; filename="exp.out"

Then 'cat path_to_output_file >> /tmp/multipart-message.data'

Then 'echo "--a93f5485f279c0--" >> /tmp/multipart-message.data'

Finally, test the API point by doing the following:

curl http://localhost:8080/experiments/add/preformatted/testexperiment/testsegmentation --data-binary @/tmp/multipart-message.data -X POST -i -H "Content-Type: multipart/form-data; boundary=a93f5485f279c0"

if you have the right segmentation name - it will work.

The way the output file is created is via pulling the entire segmentation into memory and reorganizing it into a hash table indexed by chr (dividing it into chr buckets). The it reads the experiment file into memory and goes through it line by line. For each line it extracts the chr/start/stop components and the annotation value at the "columnt" that was passed to it. It will then search for an EXACT match in the segmentation and if it finds it, it will get the segment ID from the segmentatoon, include the annotation value and that ID into the output file. This is the file you upload to create an experiment.

*/segmentations/update (POST)*

The request body of this API point should contain a design interface describing an experiment served by the server.

