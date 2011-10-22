#!/usr/bin/env python2

"""
Scan incoming directory for new music and import them to the library
"""

import argparse
import errno
import os
import sys

import mutagen

class Importer(object):
    def __init__(self, incoming, music_root, unlink_after=False):
        """
        Initialize an Importer object

        incoming is the directory to search for music files.
        music_root is the base directory where music will be imported to.
        unlink_after determines whether or not to remove the files after importing.
        """
        self.incoming = incoming
        self.music_root = music_root
        self.unlink_after = unlink_after

    def run(self):
        """
        Run the importer with the initialized settings

        Python won't allow this to be named 'import'.
        """
        self.import_files(self.incoming, self.music_root, self.unlink_after)

    @classmethod
    def import_files(cls, from_dir, to_dir, unlink_after):
        """
        Import audio files from from_dir into to_dir

        NB: It is assumed that these paths are on the same partition (and it
            supports hard links)
        """
        audio_files = cls.get_filelist(from_dir)

        for audio_file in audio_files:
            from_path = audio_file.filename
            to_path = os.path.join(to_dir, audio_file.destination)

            makedirs(os.path.split(to_path)[0])

            # Hardlink here because we may not have write permission on the
            #  source, so a move would fail, but we still want it put into the library
            try:
                os.link(from_path, to_path)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    print "Warning: Target file already exists: %s. Skipping" % to_path
                else:
                    raise

            if unlink_after:
                try:
                    os.unlink(from_path)
                except OSError as e:
                    print "Warning: Caught error trying to unlink %s: %s. Ignoring" % (from_path, str(e))
                    pass

    @classmethod
    def get_filelist(cls, dir_):
        """
        Construct the list of audio files which should be imported
        """
        all_files = cls.scan_incoming(dir_)
        audio_files = []
        for file_ in all_files:
            mutagen_file = mutagen.File(file_)
            if mutagen_file is None:
                print "Warning: %s cannot be identified." % file_
                continue
            try:
                audio_file = AudioFile(mutagen_file)
            except ValueError as e:
                print "Skipping file: " + str(e)
            audio_files.append(audio_file)

        return audio_files

    @staticmethod
    def scan_incoming(dir_):
        """
        Return a list of files in the incoming directory, recursively
        """
        if not os.path.exists(dir_):
            raise ValueError("Incoming directory '%s' does not exist!" % dir_)
        incoming_files = []
        for root, _, files in os.walk(dir_):
            for file_ in files:
                print "Info: Found %s" % file_
                incoming_files.append(os.path.join(root, file_))

        return incoming_files

class AudioFile(object):
    def __init__(self, mutagen_file):
        """
        Initialize an AudioFile object

        mutagen_file is the underlying mutagen object
        """
        self.mutagen_file = mutagen_file
        try:
            self.destination = self.get_destination(mutagen_file)
        except ValueError as e:
            raise ValueError("Unable to determine destination path: " + str(e))

    @staticmethod
    def get_destination(mutagen_file):
        """
        Return the intended destination for a mutagen file to be imported
        """
        # TODO: Refactor all this
        artist = None
        title = None
        album = None
        track = None
        target_path = ''

        filename = mutagen_file.filename
        # XXX: This is naive and a lookup table keyed off mimetype may be better
        ext = filename.split('.')[-1]

        try:
            artist = mutagen_file['artist'][0]
            title = mutagen_file['title'][0]
        except IndexError:
            raise ValueError("Error reading Artist/Title tags from %s." % filename)
        except KeyError:
            if 'TPE1' in mutagen_file and 'TIT2' in mutagen_file:
                # mp3 bullshit
                artist = str(mutagen_file['TPE1'])
                title = str(mutagen_file['TIT2'])
            else:
                raise ValueError("%s does not have Artist/Title tags set." % filename)

        try:
            album = mutagen_file['album'][0]
            track = mutagen_file['tracknumber'][0]
        except IndexError:
            print "Warning: Error reading Album/Track tags from %s. Continuing anyway" % filename
        except KeyError:
            if 'TALB' in mutagen_file and 'TRCK' in mutagen_file:
                # mp3 bullshit
                album = str(mutagen_file['TALB'])
                track = str(mutagen_file['TRCK'])
            else:
                print "Warning: %s does not have Album/Track tags set. Continuing anyway" % filename

        if track is not None and '/' in track:
            # Some fools tag as x/y where y = total tracks
            track = track.split("/")[0]

        # XXX: Move to either "Artist/Title" or "Artist/Album/Track Title"
        if album is None:
            target_path = os.path.join(artist, "%s.%s" % (title, ext))
        else:
            target_path = os.path.join(artist, album, "%0.2d %s.%s" % (int(track), title, ext))

        return target_path

    @property
    def filename(self):
        """
        Return the filename of the audio file on disk
        """
        return self.mutagen_file.filename

def makedirs(path):
    """
    Make directories recursively.

    A wrapper for os.makedirs that won't raise OSError for existing directories
    Basically is like `mkdir -p'
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Directory already exists
            pass
        else:
            raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import music from one directory into another, sorted by audio metadata')
    parser.add_argument('--from-dir', '-f', dest='from_dir',
                        type=os.path.expanduser, default='~/Dropbox',
                        help='Directory to import music from')
    parser.add_argument('--to-dir', '-t', dest='to_dir',
                        type=os.path.expanduser, default='~/Media/Music',
                        help='Root directory that music gets imported to')
    options = parser.parse_args(sys.argv[1:])

    importer = Importer(options.from_dir, options.to_dir, unlink_after=False)
    importer.run()

