#!/bin/bash


function sh_getbgcolor {
   local cfile="$HOME/.config/bigbashview_lightmode"
   local lightmode=0
   local result
   local status

   # Open Autodetect and read saved background color
   if ! test -s "$cfile"; then
      # Read background color
      if result="$(kreadconfig5 --group "Colors:Window" --key BackgroundNormal)"; then
         if (( -n "$result" )); then
            KDE_BG_COLOR="$(bc | sed 's|^|(|g;s|,|+|g;s|$|)/3|g' <<< "$result")"
            # Verify if is light or not
            if [[ "$KDE_BG_COLOR" -gt "127" ]]; then
               lightmode=1
            fi
         fi
      fi
   else
      lightmode=$(printf "%s" "$(<"$cfile")")
   fi

   if ((lightmode)); then
      echo '<body class=light-mode>'
   else
      echo '<body>'
   fi
}

sh_getbgcolor
