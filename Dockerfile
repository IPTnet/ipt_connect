FROM python:2-slim

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

WORKDIR /code/ipt_connect
