FROM python:2.7.7

MAINTAINER mamachanko

ADD . /inbound

WORKDIR /inbound/

RUN pip install -r requirements.txt

CMD PYTHONPATH=. lymph node --guess-external-ip
