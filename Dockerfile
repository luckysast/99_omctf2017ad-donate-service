#!/usr/bin/docker build -t omctf-donat .

FROM resin/rpi-raspbian:latest
LABEL Description="omctf-2017-donat-service" Author="LSD"

RUN apt-get update && apt-get install -y \
	python-pip

RUN pip install flask \
	flask-appconfig \
	flask-bootstrap \
	flask-debug \
	flask-nav \
	flask-paginate \
	flask-pymongo \
	flask-wtf \
	pymodm 

RUN mkdir /home/donat
ADD v1.12.tgz /home/donat/
#RUN tar -xzf /home/donat/omctf2017-donat.tar.gz -C /home/donat/
RUN chmod +x /home/donat/donat.py

WORKDIR /home/donat

EXPOSE 31415 
ENTRYPOINT /home/donat/donat.py
