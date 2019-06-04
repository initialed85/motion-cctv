#!/usr/bin/env bash

if [[ -d motioneye ]]; then
    cd motioneye
    git pull --all
    git reset --hard
    cd ..
else
    git clone https://github.com/ccrisan/motioneye.git
fi
