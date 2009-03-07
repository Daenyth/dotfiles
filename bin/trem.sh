#!/bin/bash

NET_IP=$(ifconfig | fgrep -A 1 '00:0F:66:78:C1:4D' | tail -n 1 | awk '{print $2}' | sed 's/addr://')
export SDL_VIDEO_X11_DGAMOUSE=0

AWAY_MSG='Playing Tremulous.
Probably as )^(Daenyth'

mpc pause
status=$(purple-remote getstatus)
message=$(purple-remote getstatusmessage)
purple-remote "setstatus?status=away&message=$AWAY_MSG"
xinit /home/Daenyth/games/tremulous/tremulous-mg.x86 +set net_ip $NET_IP $@ -- :1
purple-remote "setstatus?status=$status&message=$message"
