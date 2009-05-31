#!/usr/bin/env python
import sys
# uncomment to work with local directory
sys.path.insert(0,"..")
from ramu.instruments import guitar
from ramu.music import *

def waitfor(s):
    print s
    sys.stdin.readline()

def MajChord(x):
    return Chord(Scale(Tone(x)))

waitfor("Make sure GarageBand is running, then hit return")
from ramu.osxmidi.channel import Channel
chan = Channel()
g = guitar.Guitar(chan)

waitfor("You should see Garageband notify you of a midi device. Hit return to continue.")

t = chan.now
t += 1.0
i = 0
for c in [MajChord(x) for x in "E A D".split()]:
    g.press_chord(t,c)
    direction = guitar.STRUM_DOWN
    start_string = 0
    if i % 2:
        direction = guitar.STRUM_UP
        start_string = 5
    g.strum(t,1.0/16,direction,start_string)
    t += 1.0
    i += 1
g.silence(t)

waitfor("hit return when you want to quit")
#g.silence(now())


