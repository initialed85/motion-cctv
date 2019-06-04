#!/usr/bin/env bash

echo "instance uuid is ${INSTANCE_UUID}"

RUN_UUID=$(uuidgen)

echo "${RUN_UUID}" > /srv/run.uuid

echo "run uuid is ${RUN_UUID}"

motion -n
