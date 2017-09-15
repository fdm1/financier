#! /bin/bash

export TOXENV=$1

docker-compose -f docker-compose.tox.yaml up
