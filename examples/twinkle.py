#!/usr/bin/env python
#
# play "Twinkle Twinkle Little Star"
#
# Copyright (C) 2009 Roger Allen (rallen@gmail.com)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
import sys
# uncomment to work with local directory
#sys.path.insert(0,"..")
from ramu.music import *
from ramu.instruments.sequencer import *

def usage():
    print "twinkle.py stdout|midi"

def waitfor(s):
    print s
    sys.stdin.readline()

def mk_note(g):
    """g is of the form c4 or aa5"""
    octave   = int(g[-1])
    glyph    = g[0]
    duration = (len(g)-1)
    return Note(Tone(glyph,octave),duration)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main(argv):
    if len(argv) != 2 or not argv[1] in ["stdout", "midi"]:
        usage()
        exit()

    do_midi = argv[1] == "midi"

    if do_midi:
        waitfor("Make sure GarageBand is running, then hit return")
        from ramu.osxmidi.channel import Channel
    else:
        from ramu.channel import Channel

    with Channel() as chn:
        if do_midi:
            waitfor("You should see Garageband notify you of a midi device. Hit return to continue.")

        # twinkle's sequence of notes
        sub_seq = [ 'c4 c4 g4 g4 a4 a4 gg4'.split(),
                    'f4 f4 e4 e4 d4 d4 cc4'.split(),
                    'g4 g4 f4 f4 e4 e4 dd4'.split() ]
        the_notes = sub_seq[0] + sub_seq[1] + \
            sub_seq[2]*2 + sub_seq[0] + sub_seq[1]

        seq = Sequence(Rhythm(144))
        for g in the_notes:
            seq.append(mk_note(g))

        seq.play_and_wait(chn.now,chn)

if __name__ == '__main__':
    main(sys.argv)
