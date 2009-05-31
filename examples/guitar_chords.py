#!/usr/bin/env python
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



