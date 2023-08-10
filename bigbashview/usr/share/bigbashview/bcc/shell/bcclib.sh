#!/usr/bin/env bash
#shellcheck disable=SC2155,SC2034
#shellcheck source=/dev/null

#  bcclib.sh
#  Description: Control Center to help usage of BigLinux
#
#  Created: 2022/02/28
#  Altered: 2023/08/08
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
_VERSION_="1.0.0-20230808"
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
	local script_name0="${0##*/}[${FUNCNAME[0]}]:${BASH_LINENO[0]}"
	local script_name1="${0##*/}[${FUNCNAME[1]}]:${BASH_LINENO[1]}"
	local script_name2="${0##*/}[${FUNCNAME[2]}]:${BASH_LINENO[2]}"
#	kdialog --title "[xdebug (kdialog)]$0" --yesno "\n${*}\n" --icon dialog-information
#	result=$?
#	((result)) && exit 1
#	return $result

	yad --title="[xdebug (yad)]$script_name1"	\
		--text="${*}\n"						\
		--width=400								\
		--window-icon="$xicon"				\
		--button="Sim:1"						\
		--button="Não:2"
	result=$?
	[[ $result -eq 2 ]] && exit 1
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

	error_output=$("$@" 2>&1)
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

function sh_get_current_desktop {
	echo "$XDG_CURRENT_DESKTOP"
}
export -f sh_get_current_desktop

function sh_get_wm {
	local ps_flags=(-e)

	if [[ -O "${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY:-wayland-0}" ]]; then
		if tmp_pid="$(lsof -t "${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY:-wayland-0}" 2>&1)" ||
			tmp_pid="$(fuser "${XDG_RUNTIME_DIR}/${WAYLAND_DISPLAY:-wayland-0}" 2>&1)"; then
			wm="$(ps -p "${tmp_pid}" -ho comm=)"
		else
			# lsof may not exist, or may need root on some systems. Similarly fuser.
			# On those systems we search for a list of known window managers, this can mistakenly
			# match processes for another user or session and will miss unlisted window managers.
			wm=$(ps "${ps_flags[@]}" | grep -m 1 -o -F \
				-e arcan \
				-e asc \
				-e clayland \
				-e dwc \
				-e fireplace \
				-e gnome-shell \
				-e greenfield \
				-e grefsen \
				-e hikari \
				-e kwin \
				-e lipstick \
				-e maynard \
				-e mazecompositor \
				-e motorcar \
				-e orbital \
				-e orbment \
				-e perceptia \
				-e river \
				-e rustland \
				-e sway \
				-e ulubis \
				-e velox \
				-e wavy \
				-e way-cooler \
				-e wayfire \
				-e wayhouse \
				-e westeros \
				-e westford \
				-e weston)
		fi

	elif [[ $DISPLAY && $os != "Mac OS X" && $os != "macOS" && $os != FreeMiNT ]]; then
		# non-EWMH WMs.
		wm=$(ps "${ps_flags[@]}" | grep -m 1 -o \
			-e "[s]owm" \
			-e "[c]atwm" \
			-e "[f]vwm" \
			-e "[d]wm" \
			-e "[2]bwm" \
			-e "[m]onsterwm" \
			-e "[t]inywm" \
			-e "[x]11fs" \
			-e "[x]monad")

		[[ -z $wm ]] && type -p xprop &>/dev/null && {
			id=$(xprop -root -notype _NET_SUPPORTING_WM_CHECK)
			id=${id##* }
			wm=$(xprop -id "$id" -notype -len 100 -f _NET_WM_NAME 8t)
			wm=${wm/*WM_NAME = /}
			wm=${wm/\"/}
			wm=${wm/\"*/}
		}
	fi
	[[ $wm == *WINDOWMAKER* ]] && wm=wmaker
	[[ $wm == *GNOME*Shell* ]] && wm=Mutter
}
export -f sh_get_wm

function sh_get_de {
	sh_get_wm
	# Temporary support for Regolith Linux
	if [[ $DESKTOP_SESSION == *regolith ]]; then
		de=Regolith

	elif [[ $XDG_CURRENT_DESKTOP ]]; then
		de=${XDG_CURRENT_DESKTOP/X\-/}
		de=${de/Budgie:GNOME/Budgie}
		de=${de/:Unity7:ubuntu/}

	elif [[ $DESKTOP_SESSION ]]; then
		de=${DESKTOP_SESSION##*/}

	elif [[ $GNOME_DESKTOP_SESSION_ID ]]; then
		de=GNOME

	elif [[ $MATE_DESKTOP_SESSION_ID ]]; then
		de=MATE

	elif [[ $TDE_FULL_SESSION ]]; then
		de=Trinity
	fi

	[[ $de == "$wm" ]] && {
		unset -v de
		return
	}
	# Fallback to using xprop.
	[[ $DISPLAY && -z $de ]] && type -p xprop &>/dev/null &&
		de=$(xprop -root | awk '/KDE_SESSION_VERSION|^_MUFFIN|xfce4|xfce5/')

	# Format strings.
	case $de in
	KDE_SESSION_VERSION*) de=KDE${de/* = /} ;;
	*xfce4*) de=Xfce4 ;;
	*xfce5*) de=Xfce5 ;;
	*xfce*) de=Xfce ;;
	*mate*) de=MATE ;;
	*GNOME*) de=GNOME ;;
	*MUFFIN*) de=Cinnamon ;;
	esac

	((${KDE_SESSION_VERSION:-0} >= 4)) && de=${de/KDE/Plasma}

	if [[ $de_version == on && $de ]]; then
		case $de in
		Plasma*) de_ver=$(plasmashell --version) ;;
		MATE*) de_ver=$(mate-session --version) ;;
		Xfce*) de_ver=$(xfce4-session --version) ;;
		GNOME*) de_ver=$(gnome-shell --version) ;;
		Cinnamon*) de_ver=$(cinnamon --version) ;;
		Deepin*) de_ver=$(awk -F'=' '/MajorVersion/ {print $2}' /etc/os-version) ;;
		Budgie*) de_ver=$(budgie-desktop --version) ;;
		LXQt*) de_ver=$(lxqt-session --version) ;;
		Lumina*) de_ver=$(lumina-desktop --version 2>&1) ;;
		Trinity*) de_ver=$(tde-config --version) ;;
		Unity*) de_ver=$(unity --version) ;;
		esac

		de_ver=${de_ver/*TDE:/}
		de_ver=${de_ver/tde-config*/}
		de_ver=${de_ver/liblxqt*/}
		de_ver=${de_ver/Copyright*/}
		de_ver=${de_ver/)*/}
		de_ver=${de_ver/* /}
		de_ver=${de_ver//\"/}

		de+=" $de_ver"
	fi

	[[ $de && $WAYLAND_DISPLAY ]] && de+=" (Wayland)"
	echo $de
}
export -f sh_get_de

#sh_debug
