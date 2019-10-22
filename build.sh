#!/usr/bin/env bash

TAG=motion-cctv

docker build -t ${TAG} .
if [[ ${?} -ne 0 ]]; then
  exit 1
fi

docker run -d --name ${TAG}-build ${TAG} tail -F /dev/null

rm -fr default_configs

mkdir -p default_configs

docker cp ${TAG}-build:/srv/default_etc_motion/motion-dist.conf default_configs/motion.conf
docker cp ${TAG}-build:/srv/default_etc_motion/camera1-dist.conf default_configs/camera1.conf
docker cp ${TAG}-build:/srv/default_etc_motion/camera2-dist.conf default_configs/camera2.conf
docker cp ${TAG}-build:/srv/default_etc_motion/camera3-dist.conf default_configs/camera3.conf
docker cp ${TAG}-build:/srv/default_etc_motion/camera4-dist.conf default_configs/camera4.conf

docker rm -f ${TAG}-build
