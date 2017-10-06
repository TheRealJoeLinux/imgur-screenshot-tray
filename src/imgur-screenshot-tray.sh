#!/bin/bash

# name
APP_NAME=imgur-screenshot-tray

# available system notifier
NOTIFY_BIN=$(which notify-send)
if [ -z $NOTIFY_BIN ]; then
    ZENITY=$(which zenity)
    if [ ! -z $ZENITY ]; then
        NOTIFY_BIN="${ZENITY} --info --text"
    else
        # we have nothing, just print
        NOTIFY_BIN=$(which echo)
    fi
fi

# look for python3
PYBIN=$(which python3)
if [ ! -f $PYBIN ]; then
    version=$(python -c "import sys; print(sys.version)" | head -1 | awk -F. '{print $1}')
    if [ $version -lt 3 ]; then
        $NOTIFY_BIN "You must have Python 3+ installed for this application to work."
        exit 1
    else
        PYBIN=$(which python)
    fi
fi

# find the python script
IMGUR_PY=$HOME/.local/bin/${APP_NAME}.py
if [ ! -f $IMGUR_PY ]; then
    IMGUR_PY=/usr/local/bin/${APP_NAME}.py
    [ ! -f $IMGUR_PY ] && $NOTIFY_BIN "Could not find ${APP_NAME}.py. Did you install it?" && exit 1
fi

$PYBIN $IMGUR_PY
