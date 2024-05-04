FROM ubuntu:22.04

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8

WORKDIR /construction
ADD requirements.txt /construction
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python3 python3-dev python3-pip postgresql-client postgresql-server-dev-14
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# Preperation
COPY . /construction/
