#!/bin/bash

# We need this for ** to work
shopt -s globstar  || exit 1
# And we need this to properly parse the playlist
perl -MURI::Escape -e '' || exit 1

startdir=$(pwd)
cd ~/Music

# playlist_url="http://www.last.fm/user/Cemetary_walk/library/playlists/304fi_nightjam"
# wget -q "$playlist_url" -O - | grep -A1 'td class="track"' | grep href > playlist.html
cat $startdir/playlist.html | perl -MURI::Escape -ne '
$_ = uri_unescape(uri_unescape($_)); 
$_ =~ tr/+/ /; 
($artist,$track) = $_ =~ m{– <a href="/music/(.*?)/_/(.*?)">}; 
print "$artist\t$track\n"' |
while IFS=$(printf '\t') read artist track; do
	target_track=("$artist"/**/*"$track"*)
	for file in "${target_track[@]}"; do
		if [ -f "$file" ]; then
			echo $file
		else
            [ -d "$file" ] && continue
            #echo "$file" >&2
			echo "# $artist//$track"
		fi
	done
done

