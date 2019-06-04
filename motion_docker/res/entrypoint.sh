#!/usr/bin/env bash

ARGS="-n"
if [[ "${1}" == "no_motion" ]]; then
    ARGS="-n -m"
fi

echo "instance uuid is ${INSTANCE_UUID}"

RUN_UUID=$(uuidgen)

echo "${RUN_UUID}" > /srv/run.uuid

echo "run uuid is ${RUN_UUID}"

motion ${ARGS}
