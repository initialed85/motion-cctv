#!/usr/bin/env bash

EVENT_LOG=/srv/target_dir/events.log

echo "`date +'%Y-%m-%d %H:%M:%S'`,${1},${2},${3},${4},${5},${6},${7},${8},${9},${10},${11}" >> ${EVENT_LOG}
