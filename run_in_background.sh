#!/usr/bin/env bash

SUFFIX=""
if [[ "${1}" != "" ]]; then
    SUFFIX="-${1}"
fi

IMAGE=motion-cctv

CONTAINER=${IMAGE}-run${SUFFIX}

docker run -d --restart=always --log-opt max-size=10m \
    --name ${CONTAINER} \
    -p 80:80 \
    -p 8080:8080 \
    -p 8081:8081 \
    -v `pwd`/configs:/etc/motion \
    -v /media/storage/Cameras:/srv/target_dir \
    ${IMAGE} ${2} ${3}
