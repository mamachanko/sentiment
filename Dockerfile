FROM docker.lab38:5000/delivero/lymph-base

MAINTAINER mamachanko

ADD . /barometer

WORKDIR barometer/

RUN pip install -r requirements.txt

CMD lymph node --guess-external-ip
