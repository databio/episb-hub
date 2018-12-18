#!/usr/bin/bash

/usr/bin/docker build -t databio/episb-hub:tiangolo .
/usr/bin/docker push databio/episb-hub:tiangolo
/usr/bin/docker stop episb-hub
/usr/bin/docker run --name episb-hub -d --rm -p 8888:80 databio/episb-hub:tiangolo
