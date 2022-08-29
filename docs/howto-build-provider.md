# How to build a data provider

## Purpose ##

The purpose of the episb-provider is to serve the API for the episb server. The code is written in Scala, using the Scalatra framework. In (this) testing/development phase, the server runs on port 8080 and must be run from the command line like so:

## Build & Run ##

Assumptions: you have [sbt installed](https://www.scala-sbt.org/1.0/docs/Setup.html) or you will be using [Tomcat](http://tomcat.apache.org/).

### To run the provider using sbt: ###

```sh
$ git clone https://github.com/databio/episb-provider.git
$ cd episb-provider/episb-provider
$ sbt
> jetty:start
```

*The URL where all the requests are served from in this method would be http://localhost:8080/*

### To run the provider using Tomcat: ###

The included script [restart_tomcat.sh](https://github.com/databio/episb-provider/blob/master/episb-provider/restart_tomcat.sh) is provided if you choose to run the provider in a more robust (production) fashion. Instead of using the jetty engine included with the Scalatra framework (using the above sbt method), this approach relies on a local install of Tomcat. In particular, the location where the app will be "exploded" (Tomcat terminology that roughly means "unpacked and installed") is assumed to be the /usr/share/tomcat/webapps/ directory. If your installation of Tomcat has a different webapps directory please adjust accordingly. The included script will simply package a "war" file from the code (you will still require an installation of sbt to do this!) and copy this war file under the name /usr/share/tomcat/webapps/episb-provider.war. Tomcat will sense that this file is there, automatically "explode" it and serve whatever Java application is in this file at the http://localhost:8080/episb-provider/ path. Note that the "localhost" in the abovementioned URL is only valied with a default install of Tomcat.

*The URL where all the requests are served from in this method would be http://localhost:8080/episb-provider/*

For more Tomcat configuration, the files usually reside in a location such as /etc/tomcat (but can vary with Linux or BSD flavors). This is the official [guide to configuring Tomcat](https://tomcat.apache.org/tomcat-8.5-doc/index.html).

**New!**: You can now also run the provider as a Docker container!

```sh
$ git clone https://github.com/databio/episb-provider.git
$ cd episb-provider/episb-provider
$ ./docker_build.sh
$ docker run -d --rm -p 8080:8080 episb-provider:latest
```

*The URL where all the requests are served from in this method would be http://localhost:8080/episb-provider/*

## Test install ##

After the above steps are completed, launch a browser and point it to localhost:8080/list (if you ran it via the SBT route above) or localhost:8080/episb-provider/list (if you ran it using the restart_tomcat.sh script above).

*NB: Going to url:8080/"type anything here" as in the above "localhost:8080/episb-provider/list" will make the server list all the "paths" it is listening to (effectively listing all the REST API points it knows).*

## Dependencies ##

The REST API code depends on a running local instance of [Elasticsearch](https://www.elastic.co/products/elasticsearch). This is where all the queries are performed in the background and results served back to the client. Currently we depend on Elasticsearch 6.4.2. Usually Elastic can be installed using whatever facilities the underlying operating system provides (yum for Redhat derivatives, apt for Debian variants, pkg install for BSD variants, so on and so on).

Configuring elasticsearch for optimal use is beyond the scope of this document. We are including a [Docker compose file](https://github.com/databio/episb-provider/tree/master/episb-provider/elastic) that will allow you to run elasticsearch as a collection of container instances.  Do note that this particular docker-compose file will spin off five Docker containers each running elastic, each with a heap size of 32Gb! They will all run on a single machine as well, meaning that you should plan on this machine having ample memory. If Docker is not applicable to your setup - elasticsearch is happy to run as a basic install as mentioned above. We are including an elasticsearch.yml file to be used for a basic elastic install by way of copying it into /etc/elasticsearch/ (or /usr/local/etc/elasticsearch on FreeBSD, for example).

In order to check what is stored/indexed by Elasticsearch, a developer concole called [Kibana](https://www.elastic.co/products/kibana) is used (however, Elastic supports access via the http protocol so a basic "curl" will do as well!). It is beyond the scope of this document to provide instruction on Elasticsearch query DSL/APIs or Kibana.

## Status ##

There are a lot of "FIXME" and configuration issues to get the project to production quality stage. Bear with us :-)

## Data stored in Elasticsearch ##

Before we discuss the provided REST API points, read more on [how data is organized](http://code.databio.org/episb/data-organization/) in the episb-provider's Elasticsearch backend.

## REST API POINTS ##

We provide more in-depth information on [how to use the episb-provider programmatically](http://code.databio.org/episb/provider-api/).

## Future ##

The proper way to run the code is to build it into a .war file (which is built every time a "package") command is run from sbt. The .war artifact can then be copied into a directory of a running Tomcat server, which will in turn "explode" the .war file and serve it immediately.

See this Scalatra doc for production deployment: http://scalatra.org//guides/2.6/deployment/servlet-container.html
