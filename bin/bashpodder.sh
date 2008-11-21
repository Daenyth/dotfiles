#!/bin/bash
# By Linc 10/1/2004
# Find the latest script at http://linc.homeunix.org:8080/scripts/bashpodder
# Revision 1.2 09/14/2006 - Many Contributers!
# If you use this and have made improvements or have comments
# drop me an email at linc dot fessenden at gmail dot com
# I'd appreciate it!
# Revised by Daenyth 2008/03/02

# Print status to STDOUT? -- 1=Print; 0=Don't print
loud=1
if [ -n "$1" ]; then
	case $1 in
		-q) loud=0 ;;
		-v) loud=1 ;;
		*) echo "Error: Unknown parameter '$1'"; exit ;;
	esac
fi

# Where will we keep everything?
bpdir="${HOME}/.bashpodder/"

[[ ! -d $bpdir ]] && mkdir -p "$bpdir"
cd "$bpdir"

# All dirs can be relative to the bp dir
# datadir is the directory you want podcasts saved to:
datadir="podcasts/$(date +%Y-%m-%d)"

conf='bp.conf'
log='podcast.log'

# Delete any temp file:
rm -f temp.log

[[ ! -d $datadir ]] && mkdir -p "$datadir"
# Read the bp.conf file and wget any url not already in the podcast.log file:
while read podcast; do
	[[ $loud -eq 1 ]] && echo "Parsing podcast: $podcast"
	file=$(xsltproc parse_enclosure.xsl $podcast 2> /dev/null || wget -q $podcast -O - | tr '\r' '\n' | tr \' \" | sed -n 's/.*url="\([^"]*\)".*/\1/p')
	for url in $file; do
		if ! grep -q "$url" $log; then
			echo "       Grabbing: $url"
			wget -t 10 -U BashPodder -c -q -O $datadir/$(echo "$url" | awk -F'/' {'print $NF'} | awk -F'=' {'print $NF'} | awk -F'?' {'print $1'}) "$url" \
			&& echo $url >> temp.log # Use && to make sure the log only gets updated on a successful download.
		fi
	done
done < $conf

# Move dynamically created log file to permanent log file:
[[ $loud -eq 1 ]] && echo "Updating Logfile"
cat $log >> temp.log
sort temp.log | uniq > $log
rm temp.log

# Create an m3u playlist:
pods=`ls $datadir | grep -v m3u | wc -l`
if [ $pods -ne 0 ]; then
	if [ $pods -gt 1 ]; then
		[[ $loud -eq 1 ]] && echo "Creating playlist"
		ls $datadir | grep -v m3u > $datadir/podcast.m3u
	fi
else
	rmdir $datadir
fi
