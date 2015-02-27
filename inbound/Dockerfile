FROM docker.lab38:5000/delivero/lymph-base

MAINTAINER mamachanko

ADD . /inbound

WORKDIR inbound/

RUN pip install -r requirements.txt

CMD PYTHONPATH=. lymph node --guess-external-ip
