#!/usr/bin/env bash

if [[ -d motion ]]; then
    cd motion
    git pull --all
    git reset --hard
    cd ..
else
    git clone https://github.com/Motion-Project/motion.git
fi
