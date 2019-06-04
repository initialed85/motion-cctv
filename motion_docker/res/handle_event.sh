#!/usr/bin/env bash

EVENT_LOG=/srv/target_dir/events.log

INSTANCE_UUID=$(cat /srv/instance.uuid)
RUN_UUID=$(cat /srv/run.uuid)

echo "`date --rfc-3339=ns`,${INSTANCE_UUID},${RUN_UUID},${1},${2},${3},${4} ${5},${6},${7},${8},${9},${10},${11},${12},${13}" >> ${EVENT_LOG}
