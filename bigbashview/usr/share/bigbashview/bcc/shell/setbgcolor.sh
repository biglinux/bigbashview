#!/bin/bash

if [ "$1" = "true" ]; then
    echo '1' > ~/.config/bigbashview_lightmode
else
    echo '0' > ~/.config/bigbashview_lightmode
fi
