#! /usr/bin/env python2

order = ("artist", "album", "track", "title", "file")


import mpdclient2


def get_tracks(x, y):
    if "/" in x:
        x = x.split("/")[0]
    if "/" in y:
        y = y.split("/")[0]
    try:
        tmpx = int(x)
        tmpy = int(y)
        x = tmpx
        y = tmpy
    except ValueError:
        pass
    return x, y

def sort(x, y):
    for key in order:
        if x.has_key(key) and y.has_key(key):
            xitem = x[key].lower()
            yitem = y[key].lower()
            if key == "track":
                xitem, yitem = get_tracks(xitem, yitem)
            diff = cmp(xitem, yitem)
        else:
            diff = cmp(x.has_key(key), y.has_key(key))
        if diff != 0:
            return diff
    return 0


conn = mpdclient2.connect()
playlist = conn.playlistinfo()
playlist.sort(sort)
conn = mpdclient2.connect()
conn.clear()
for song in playlist:
    conn.add(song.file)


# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
