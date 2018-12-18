FROM tiangolo/uwsgi-nginx-flask:python2.7-alpine3.7
MAINTAINER "nem2p@virginia.edu

# Install aws-cli
RUN apk -Uuv add groff less python py-pip
RUN pip install awscli
RUN apk --purge -v del py-pip
RUN rm /var/cache/apk/*

RUN mkdir /root/.aws
COPY .aws/config /root/.aws/config
COPY . /app
RUN pip install -r /app/requirements.txt
