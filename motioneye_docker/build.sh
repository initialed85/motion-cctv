#!/usr/bin/env bash

TAG=motioneye-cctv

docker build -t ${TAG} .

docker run -d --name ${TAG}-build ${TAG} tail -F /dev/null

docker rm -f ${TAG}-build
