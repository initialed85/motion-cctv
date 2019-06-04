#!/usr/bin/env bash

IMAGE=motion-cctv

TAG=${IMAGE}-run

docker run -it --restart=always --log-opt max-size=10m \
    --name ${TAG} \
    -p 8080:8080 \
    -p 8081:8081 \
    -v `pwd`/configs:/etc/motion \
    -v `pwd`/target_dir:/srv/target_dir \
    ${IMAGE}

docker rm -f ${TAG}
