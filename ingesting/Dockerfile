FROM python:2.7.7

MAINTAINER mamachanko

ADD . /ingesting

WORKDIR /ingesting/

RUN pip install -r requirements.txt

CMD PYTHONPATH=. lymph node --guess-external-ip
