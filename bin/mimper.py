#!/usr/bin/env python

"""Scan incoming directory for new music and import them to the library"""

import os
import sys
import errno

import mutagen

# XXX: It is assumed that these paths are on the same partition (and it supports hard links)
incoming_dir = os.path.expanduser('~drew/Musics')
music_library = os.path.expanduser('~/Media/Music')

def scan_incoming(dir_):
    """Return a list of files in the incoming directory, recursively"""
    if not os.path.exists(dir_):
        raise ValueError("Incoming directory '%s' does not exist!" % dir_)
    incoming_files = []
    for root, _, files in os.walk(dir_):
        for file_ in files:
            print "Info: Found %s" % file_
            incoming_files.append(os.path.join(root, file_))

    return incoming_files

def get_metadata(files):
    """Get the audio metadata from a list of files.

    files is a list of file paths

    Returns a list of mutagen objects holding the audio
    metadata. Unidentifiable files will be skipped and have a warning
    printed"""
    metadata = []
    for file_ in files:
        fileinfo = mutagen.File(file_)
        if fileinfo is None:
            print "Warning: %s cannot be identified." % file_
            continue
        metadata.append(fileinfo)

    return metadata

def get_movepaths(files):
    """Find out where the incoming files should be moved to

    files is a list of mutagen objects

    Returns (fileinfo, move_to)"""
    movepaths = []

    for file_ in files:
        artist = None
        title = None
        album = None
        track = None
        target_path = ''

        filename = file_.filename
        # XXX: This is naive and a lookup table keyed off mimetype may be better
        ext = filename.split('.')[-1]

        try:
            artist = file_['artist']
            title = file_['title']
        except KeyError:
            print "Warning: %s does not have Artist/Title tags set. Skipping" % filename
            continue

        try:
            album = file_['album']
            track = file_['tracknumber']
            if '/' in track:
                # Some fools tag as x/y where y = total tracks
                track = track.split("/")[0]
        except KeyError:
            print "Warning: %s does not have Album/Track tags set. Continuing anyway" % filename

        # XXX: Move to either "Artist/Title" or "Artist/Album/Track Title"
        if album is None:
            target_path = os.path.join(artist, "%s.%s" % (title, ext))
        else:
            target_path = os.path.join(artist, album, "%s %s.%s" % (track, title, ext))

        movepaths.append(file_, target_path)

    return movepaths

def makedirs(path):
    """Make directories recursively.

    A wrapper for os.makedirs that won't raise for existing directories
    Basically is like `mkdir -p'"""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Directory already exists
            pass
        else:
            raise

def process_imports(movepaths):
    """Imports files into the music library

    ** Side effects **

    movepaths is a 2-tuple of (from, to) file paths"""
    for from_path, to_file in movepaths:
        to_path = os.path.join(music_library, to_file)

        makedirs(os.path.split(to_path)[0])

        # Hardlink here because we may not have write permission on the
        #  source, so a move would fail, but we still want it put into the library
        os.link(from_path, to_path)
        try:
            os.unlink(from_path)
        except OSError as e:
            print "Warning: Caught error trying to unlink %s: %s. Ignoring" % (from_path, str(e))
            pass

def clean_incoming(incoming_dir):
    """Clean the incoming directory

    ** Side effects **

    incoming_dir is the root directory from which we remove empty subdirectories """
    pass


def main():
    # Wish I had haskell's sweet function composition here: scan_incoming . get_metadata . get_movepaths ...
    incoming_files = scan_incoming(incoming_dir)
    files = get_metadata(incoming_files)
    movepaths = get_movepaths(files)

    process_imports(movepaths)
    clean_incoming(incoming_dir)

if __name__ == '__main__':
    sys.exit(main())
