FROM tiangolo/uwsgi-nginx-flask:python2.7-alpine3.7
MAINTAINER "nem2p@virginia.edu

COPY . /app
RUN pip install -r /app/requirements.txt
