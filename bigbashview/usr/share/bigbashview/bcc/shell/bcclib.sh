#!/usr/bin/env bash
#shellcheck disable=SC2155,SC2034
#shellcheck source=/dev/null

#  bcclib.sh
#  Description: Control Center to help usage of BigLinux
#
#  Created: 2022/02/28
#  Altered: 2023/08/07
#
#  Copyright (c) 2023-2023, Vilmar Catafesta <vcatafesta@gmail.com>
#                2022-2023, Bruno Gonçalves <www.biglinux.com.br>
#                2022-2023, Rafael Ruscher <rruscher@gmail.com>
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

APP="${0##*/}"
_VERSION_="1.0.0-20230807"
BOOTLOG="/tmp/bigcontrolcenter-$USER-$(date +"%d%m%Y").log"
LOGGER='/dev/tty8'

red=$(tput setaf 124)
green=$(tput setaf 2)
pink=$(tput setaf 129)
reset=$(tput sgr0)

function sh_diahora {
	DIAHORA=$(date +"%d%m%Y-%T" | sed 's/://g')
	printf "%s\n" "$DIAHORA"
}
export -f sh_diahora

function sh_debug {
	export PS4='${red}${0##*/}${green}[$FUNCNAME]${pink}[$LINENO]${reset} '
	set -x
	#set -e
	#shopt -s extglob
	#Only to debug
	#rm -R "$HOME/.config/bigcontrolcenter/"
	#Don't group windows
	#xprop -id "$(xprop -root '\t$0' _NET_ACTIVE_WINDOW | cut -f 2)" -f WM_CLASS 8s -set WM_CLASS "$$"
}

# determina se o fundo do KDE está em modo claro ou escuro
function sh_getbgcolor {
	local cfile="$HOME/.config/bigbashview_lightmode"
	local lightmode=0
	local result
	local r g b
	local average_rgb

	if [[ -f "$cfile" ]]; then
		lightmode=$(<"$cfile")
	else
		# Read background color RGB values
		if result=$(kreadconfig5 --group "Colors:Window" --key BackgroundNormal) && [[ -n "$result" ]]; then
			r=${result%,*}
			g=${result#*,}
			g=${g%,*}
			b=${result##*,}
			average_rgb=$(((r + g + b) / 3))

			if ((average_rgb > 127)); then
				lightmode=1
			fi
		fi
		echo "$lightmode" >"$cfile"
	fi

	if ((lightmode)); then
		echo '<body class=light-mode>'
	else
		echo '<body>'
	fi
}
export -f sh_getbgcolor

function sh_setbgcolor {
	local cfile="$HOME/.config/bigbashview_lightmode"
	local lightmode=0

	[[ "$1" = "true" ]] && lightmode=1
	echo "$lightmode" >"$cfile"
}
export -f sh_setbgcolor

function sh_lang_he {
	grep ^he <<<"$LANG"
	return "$?"
}
export -f sh_lang_he

function sh_getcpu {
	#awk -F ':' 'NR==1 {print $2}' <<< "$(grep 'model name' /proc/cpuinfo)"
	grep 'model name' /proc/cpuinfo | awk -F ':' 'NR==1 {print $2}'
}
export -f sh_getcpu

function sh_getmemory {
	awk -F' ' 'NR==2 {print $2}' < <(free -h)
}
export -f sh_getmemory

function sh_getvga {
	awk -F: '/VGA/ {print $3}' < <(lspci)
}
export -f sh_getvga

function sh_catecho {
	echo "$(<"$1")"
}
export -f sh_catecho

function sh_catprintf {
	printf "%s" "$(<"$1")"
}
export -f sh_catprintf

function sh_printfile {
	sh_catecho "$1"
}
export -f sh_printfile

function sh_installed_pkgs {
	pacman -Q | cut -f1 -d" "
}
export -f sh_installed_pkgs

function sh_info_msg {
	#  echo -e "\033[1m$*\033[m"
	printf '\033[1m%b\033[m' "$@"
}
export -f sh_info_msg

function sh_get_greeting_message {
	local -i hora_atual
	local greeting_message

	hora_atual=$(date +%k)
	if ((hora_atual >= 6 && hora_atual < 12)); then
		greeting_message=$"Bom dia"
	elif ((hora_atual >= 12 && hora_atual < 18)); then
		greeting_message=$"Boa tarde"
	else
		greeting_message=$"Boa noite"
	fi
	echo "$greeting_message"
}
export -f sh_get_greeting_message

function sh_get_user {
	[[ "$USER" != "biglinux" ]] && echo " $USER"
}
export -f sh_get_user

function sh_get_lang {
	echo "$LANG"
}
export -f sh_get_lang

function sh_get_locale {
	grep _ <(locale -a) | head -1 | cut -c1-5
}
export -f sh_get_locale

function sh_ignore_error {
	"$@" 2>/dev/null
	return 0
}
export -f sh_ignore_error

function sh_div_lang {
	if grep -q ^he <<<"$LANG"; then
		echo '<div class="wrapper" style="flex-direction: row-reverse;">'
	else
		echo '<div class="wrapper">'
	fi
}
export -f sh_div_lang

function info {
	whiptail \
		--fb \
		--clear \
		--backtitle "[debug]$0" \
		--title "[debug]$0" \
		--yesno "${*}\n" \
		0 40
	result=$?
	if ((result)); then
		exit
	fi
	return $result
}
export -f info

function sh_splitarray {
	local str=("$1")
	local pos="$2"
	local sep="${3:-'|'}"
	local array

	[[ $# -eq 3 && "$pos" = "|" && "$sep" =~ ^[0-9]+$ ]] && {
		sep="$2"
		pos="$3"
	}
	[[ $# -eq 2 && "$pos" = "$sep" ]] && {
		sep="$pos"
		pos=1
	}
	[[ $# -eq 1 || ! "$pos" =~ ^[0-9]+$ ]] && { pos=1; }

	IFS="$sep" read -r -a array <<<"${str[@]}"
	echo "${array[pos - 1]}"
}
export -f sh_splitarray

function sh_linuxHardware_run { sh_linuxHardware "$@"; }
function sh_linuxhardware_run { sh_linuxHardware "$@"; }
function sh_linuxhardware { sh_linuxHardware "$@"; }
function sh_linuxHardware {
	if [ $# -gt 0 ]; then
		xdg-open https://linux-hardware.org/?id="$*"
	fi
}
export -f sh_linuxHardware

function sh_replace_variables {
	local text="$1"
	while [[ $text =~ \$([A-Za-z_][A-Za-z_0-9]*) ]]; do
		local variable_name="${BASH_REMATCH[1]}"
		local variable_value="${!variable_name}"
		text="${text/\$$variable_name/$variable_value}"
	done
	echo "$text"
}
export -f sh_replace_variables

function sh_with_echo {
	local HTML_CONTENT="$1"
	local evaluated_text=$(sh_replace_variables "$HTML_CONTENT")
	echo "$evaluated_text"
}
export -f sh_with_echo

function sh_with_read {
	local HTML_CONTENT
	read -d $'' -r HTML_CONTENT <<-EOF
		$1
	EOF
	local evaluated_text=$(sh_replace_variables "$HTML_CONTENT")
	echo "$evaluated_text"
}
export -f sh_with_read

function sh_with_cat {
	cat <<-EOF
		$(sh_replace_variables "$1")
	EOF
}
export -f sh_with_cat

function sh_window_id {
	xprop -root '\t$0' _NET_ACTIVE_WINDOW | cut -f 2
}
export -f sh_window_id

function xdebug {
#	yad --title="[debug]$0" --text="${*}\n" --width=400 --window-icon="$xicon" --button="Sim:1" --button="Não:2"
#	result=$?
#	(( result -eq 2 )) && exit 1
#	return $result
	kdialog --title "[debug]$0" --yesno "\n${*}\n" --icon dialog-information
	result=$?
	((result)) && exit 1
	return $result
}
export -f xdebug

function log_error {
#	printf "%s %-s->%-s->%-s : %s => %s\n" "$(date +"%H:%M:%S")" "$1" "$2" "$3" "$4" "$5" >> "$BOOTLOG"
	printf "%s %-s->%-s->%-s : %s => %s\n" "$(date +"%H:%M:%S")" "$1" "$2" "$3" "$4" "$5" | tee -i -a "$BOOTLOG" >$LOGGER
}
export -f log_error

function cmdlogger {
   local lastcmd="$@"
   local status
   local error_output
   local script_name0="${0##*/}[${FUNCNAME[0]}]:${BASH_LINENO[0]}"
   local script_name1="${0##*/}[${FUNCNAME[1]}]:${BASH_LINENO[1]}"
   local script_name2="${0##*/}[${FUNCNAME[2]}]:${BASH_LINENO[2]}"

	error_output=$( "$@" 2>&1 )
#  status="${PIPESTATUS[0]}"
   status="$?"
   if [ $status -ne 0 ]; then
		error_output=$(echo "$error_output" | cut -d':' -f3-)
		log_error "$script_name2" "$script_name1" "$script_name0" "$lastcmd" "$error_output"
   fi
   return $status
}
export -f cmdlogger

function sh_kscreen_clean {
	local xicon="$1"
	local xtitle=$"Configurações da tela"
	local xmsgbox=$"As configurações da tela foram resetadas."

	cmdlogger rm -Rf ~/.local/share/kscreen
#	kdialog --msgbox "$xmsgbox" --title "$xtitle" --icon "$xicon" &
	yad --title="$xtitle" --text="\n$xmsgbox" --width=400 --window-icon="$xicon" --button="OK:0" &
	sleep 5
	wmctrl -c "$xtitle"
}
export -f sh_kscreen_clean

#sh_debug
