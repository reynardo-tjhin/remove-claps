#!/bin/bash

# LINK="https://www.youtube.com/watch?v=ItSJ_woWnmk&list=RDItSJ_woWnmk&start_radio=1"
# LINK="https://www.youtube.com/watch?v=l4zkc7KEvYM"
LINK="https://www.youtube.com/watch?v=FxhbAGwEYGQ&list=RDFxhbAGwEYGQ"
NAME="test1"

# call the download.py to download and save as mp3
python ./src/download.py -d "$LINK" -n "$NAME"
