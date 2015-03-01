FROM python:2.7.7

MAINTAINER mamachanko

ADD . /crunching

WORKDIR /crunching/

RUN pip install -r requirements.txt

CMD PYTHONPATH=. lymph node --guess-external-ip
