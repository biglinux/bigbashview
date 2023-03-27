#!/bin/bash

# Open Autodetect and read saved background color
if [ ! -e "$HOME/.config/bigbashview_lightmode" ]; then

  # Read background color
  KDE_BG_COLOR="$(kreadconfig5 --group "Colors:Window" --key BackgroundNormal | sed 's|^|(|g;s|,|+|g;s|$|)/3|g' | bc)"

  # Verify if is light or not
  if [ "$KDE_BG_COLOR" -gt "127" ]; then
    echo '<body class=light-mode>'
  else
    echo '<body>'
  fi

else

  if [ "$(cat "$HOME/.config/bigbashview_lightmode")" = "1" ]; then
    echo '<body class=light-mode>'
  else
    echo '<body>'
  fi
fi
# Close Autodetect and read saved background color
