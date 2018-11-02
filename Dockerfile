FROM ubuntu:18.04
MAINTAINER "nem2p@virginia.edu

RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -yq install net-tools nginx python-pip

RUN pip install --upgrade pip
RUN pip install uwsgi flask requests

EXPOSE 80

COPY etc/nginx.conf /etc/nginx/sites-enabled/default
CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=app:app
