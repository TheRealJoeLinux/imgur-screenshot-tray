#!/bin/bash

# look for python3
PYBIN=$(which python3)
if [ ! -f $PYBIN ]; then
    version=$(python -c "import sys; print(sys.version)" | head -1 | awk -F. '{print $1}')
    if [ $version -lt 3 ]; then
        echo "You must have Python 3+ for this application to work."
        exit 1
    else
        PYBIN=$(which python)
    fi
fi

$PYBIN src/imgur.py &
