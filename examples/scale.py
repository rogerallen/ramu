#!/usr/bin/env python
#
# play and manipulate a scale
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
from copy import deepcopy
# uncomment to work with local directory
sys.path.insert(0,"..")
from ramu.music import *

def usage():
    print "playscale.py stdout|midi"

def waitfor(s):
    print s
    sys.stdin.readline()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if len(sys.argv) != 2 or not sys.argv[1] in ["stdout", "midi"]:
    usage()
    exit()

do_midi = sys.argv[1] == "midi"

if do_midi:
    waitfor("Make sure GarageBand is running, then hit return")
    from ramu.osxmidi.channel import Channel
else:
    from ramu.channel import Channel

with Channel() as chn:
    if do_midi:
        waitfor("You should see Garageband notify you of a midi device. Hit return to continue.")

    the_notes = [ Note(t,.5) for t in Scale(Tone('c',4),'dorian').tones ]
    seq = Sequence(Rhythm(192))
    for t in the_notes:
        seq.append(t)
    rseq = deepcopy(seq)
    rseq.reverse()
    seq.append(Note(Tone('c',5),4))
    seq.play_and_wait(chn.now,chn)
    rseq.play_and_wait(chn.now,chn)
