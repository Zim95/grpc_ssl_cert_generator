#!/bin/bash

# Image details
IMAGE_NAME=grpc_ssl_generator
IMAGE_TAG=latest
NAMESPACE=browseterm
CERT_DIRECTORY=cert
TIMEOUT=120
SECRET_NAME=grpc_certs


docker container run -d \
    --name grpc_ssl_cert_generator_test \
    -e NAMESPACE=$NAMESPACE \
    -e CERT_DIRECTORY=$CERT_DIRECTORY \
    -e TIMEOUT=$TIMEOUT \
    -e SECRET_NAME=$SECRET_NAME \
    -v ./:/app/ \
    $IMAGE_NAME:$IMAGE_TAG
