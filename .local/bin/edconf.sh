#!/bin/bash



# Dmenu script for editing some of my more frequently edited config files.

if [ $DESKTOP_SESSION == "bspwm" ] 
then
	declare options=("alias
bash
bspwm
profile
vifm
xinitrc
polybar
st
sxhkd
vim
xprofile
quit")

elif [ $DESKTOP_SESSION == "qtile" ] 
then
	declare options=("alias
bash
qtile
profile
vifm
xinitrc
vim
xprofile
quit")
fi

choice=$(echo -e "${options[@]}" | rofi -dmenu -i -no-custom -p 'Edit a config file: ')

case "$choice" in
	quit)
		echo "Program terminated." && exit 1
	;;
	alias)
		choice="$HOME/.config/aliasrc"
	;;
	bash)
		choice="$HOME/.bashrc"
	;;
	bspwm)
		choice="$HOME/.config/bspwm/bspwmrc"
	;;
	profile)
		choice="$HOME/.profile"
	;;
	vifm)
		choice="$HOME/.config/vifm/vifmrc"
	;;
	xinitrc)
		choice="$HOME/.xinitrc"
	;;
	polybar)
		choice="$HOME/.config/polybar/config"
	;;
	st)
		choice="$HOME/st/config.h"
	;;
	sxhkd)
		choice="$HOME/.config/sxhkd/sxhkdrc"
	;;
	vim)
		choice="$HOME/.vimrc"
	;;
	xprofile)
		choice="$HOME/.xprofile"
	;;
	qtile)
		choice="$HOME/.config/qtile/config.py"
	;;
	*)
		exit 1
	;;
esac

if [ "$(command -v subl3)" !=  "" ]
then
	subl3 -c "$choice"
else
	subl -c "$choice"
fi
