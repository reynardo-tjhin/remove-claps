#!/bin/bash

LINK=$1
NAME=$2

if [ -z "$LINK"  ]
then
    echo 'Please provide a YouTube link'
    exit
fi

if [ -z "$NAME" ]
then
    echo 'Please provide a name for the audio file'
    exit
fi

python3 ./src/download.py -d $LINK -n $NAME