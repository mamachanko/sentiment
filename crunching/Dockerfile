FROM docker.lab38:5000/delivero/lymph-base

MAINTAINER mamachanko

ADD . /crunching

WORKDIR crunching/

RUN pip install -r requirements.txt

CMD lymph node --guess-external-ip
