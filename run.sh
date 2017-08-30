#!/bin/bash

# Check if rabbit and redis are up and running before starting the service.

echo ${RABBIT_HOST}
until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    echo "${RABBIT_HOST}- waiting rabbitmq from host...."
    echo ${PYTHONPATH}
    sleep 1
done

# Run the service
echo ${PYTHONPATH}
nameko run --config /shipping/config/config.yml rpc.shipping
