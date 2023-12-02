#!/bin/bash

d=`ls -d day* | tail -n 1 | grep -Eio '[0-9]{2}$' | sed -r 's/^0+//g'`
let d=$d+1
printf -v d "%02d" $d
cp -r skel day$d
