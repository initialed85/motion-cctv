#!/usr/bin/env bash

TAG=motion-cctv

SUFFIX=""
if [[ "$1" != "" ]]; then
    SUFFIX=${1}
fi

docker run -it --name ${TAG}${SUFFIX} ${TAG} /bin/bash

docker rm -f ${TAG}${SUFFIX}
