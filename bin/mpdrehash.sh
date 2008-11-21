#!/bin/bash
#MPD_HOST="localhost"
#MPD_PASS="pass"
#MPD_PORT=6600
playlist='main'

mpd_update () {
	echo "Updating the Database. This may take a moment."
	#mpd --create-db > /dev/null
	mpc --no-status update
	while mpc | grep -q '^Updating DB '; do sleep "0.1s"; done
}

mkplaylist () {
	echo "Remaking playlist."
	mpc --no-status clear
	mpc --no-status ls | mpc --no-status add >/dev/null
}

sortplaylist () {
	echo "Sorting playlist."
	~/bin/mpdsort.py
}

saveplaylist () {
	echo "Saving as playlist '$playlist'."
	mpc --no-status rm "$playlist" 
	mpc --no-status save "$playlist"
}

mpd_update
mkplaylist
sortplaylist
[ -n "$playlist" ] && saveplaylist
echo "Done."

