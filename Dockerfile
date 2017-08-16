FROM python:3.5.3
<<<<<<< HEAD
ADD . /shipping

WORKDIR /shipping
RUN chmod +x /shipping/run.sh
=======
ADD requirements /shipping/requirements
ADD db /shipping/db
ADD config /shipping/config
ADD integration /shipping/integration
>>>>>>> dbd9b8b1311d82172fda847d1ede7c97aff4b423

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
<<<<<<< HEAD


=======
CMD /shipping/run.sh
#CMD ["nameko","run" "/service/rpc/service_hello"]
>>>>>>> dbd9b8b1311d82172fda847d1ede7c97aff4b423
