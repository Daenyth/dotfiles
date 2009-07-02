#!/bin/bash

export SDL_VIDEO_X11_DGAMOUSE=0

AWAY_MSG='Gaming'

mpc pause
status=$(purple-remote getstatus)
message=$(purple-remote getstatusmessage)
purple-remote "setstatus?status=away&message=$AWAY_MSG"
xinit /home/Daenyth/games/tremulous/tremulous-mg.x86 $@ -- :1
purple-remote "setstatus?status=$status&message=$message"
