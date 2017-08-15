FROM python:3.5.3
ADD requirements /shipping/requirements
ADD db /shipping/db
ADD config /shipping/config
ADD integration /shipping/integration

COPY config/config.yml /shipping/config/config.yml
COPY rpc /shipping/rpc
COPY run.sh /shipping
WORKDIR /shipping
RUN chmod +x /shipping/run.sh
COPY __init__.py /shipping
RUN apt-get update && apt-get install -y \
  netcat
#RUN easy_install requests
#RUN easy_install mock

RUN /bin/bash -c "pip3 install -r /shipping/requirements/base.txt"
CMD /shipping/run.sh
#CMD ["nameko","run" "/service/rpc/service_hello"]
