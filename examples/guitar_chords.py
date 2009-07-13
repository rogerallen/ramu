#!/usr/bin/env python
#
# guitar_chords.py - strum 3 chords on the guitar
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
sys.path.insert(0,"..")
from ramu.instruments import guitar
from ramu.music import *

def usage():
    print "guitar_chords.py stdout|midi"

def waitfor(s):
    print s
    sys.stdin.readline()

def MajChord(x):
    return Chord(Scale(Tone(x)))

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
    
chn = Channel()

if do_midi:
    waitfor("You should see Garageband notify you of a midi device. Hit return to continue.")

gtr = guitar.Guitar(chn)

t = chn.now
i = 0
for c in [MajChord(x) for x in "E A D".split()]:
    gtr.press_chord(t,c)
    direction = guitar.STRUM_DOWN
    start_string = 0
    if i % 2:
        direction = guitar.STRUM_UP
        start_string = 5
    gtr.strum(t,1.0/16,direction,start_string)
    t += 1.0
    i += 1
gtr.silence(t)

if do_midi:
    waitfor("hit return after the song is done (otherwise you'll mess up Garageband)")



