FROM python:3.5.3
ADD . /shipping

WORKDIR /shipping
RUN chmod +x /shipping/run.sh

RUN apt-get update && apt-get install -y \
  netcat

RUN /bin/bash -c "pip3 install -r /shipping/requirements/base.txt"


