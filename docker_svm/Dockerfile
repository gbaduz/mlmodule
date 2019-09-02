FROM ubuntu

RUN apt-get -y update

RUN apt-get -y install python-pip python-dev 

RUN pip install dpkt

RUN pip install python-memcached

RUN pip install -U scikit-learn

RUN pip install pandas

RUN pip install cvxopt


RUN apt-get -y install vim

RUN apt-get -y install unzip

ADD https://github.com/seperman/python-statlib/archive/master.zip /usr/src
WORKDIR /usr/src
RUN unzip master.zip

WORKDIR /usr/src/python-statlib-master/

RUN python setup.py install

WORKDIR /workspace

RUN apt-get -y install software-properties-common

RUN apt-get update

RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN apt-get update
RUN apt-get -y install openjdk-8-jre











