#!/usr/bin/env bash

ARGS="-n"
if [[ "${1}" == "no_motion" ]]; then
    ARGS="-n -m"
fi

motion ${ARGS}
