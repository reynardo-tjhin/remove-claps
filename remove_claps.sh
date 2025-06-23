#!/bin/bash

FILENAME=$1

if [ -z "$FILENAME" ]
then
    echo 'Please provide an MP3 filename to remove the claps'
    exit
fi

python ./src/remove_claps.py -f $FILENAME