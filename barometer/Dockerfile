FROM python:2.7.7

MAINTAINER mamachanko

ADD . /barometer

WORKDIR /barometer/

RUN pip install -r requirements.txt

CMD PYTHONPATH=. lymph node --guess-external-ip
