#!/usr/bin/env python
import sys
sys.path.append("..")
from ramu.instruments.guitar import *
from ramu.music import *

def waitfor(s):
    print s
    sys.stdin.readline()
    
waitfor("Make sure GarageBand is running, then hit return")
from ramu.osxmidi.osxmidi import *
c = MidiChannel()
g = Guitar(c)

waitfor("You should see Garageband notify you of a midi device. Hit return to continue.")

def MajChord(x): return Chord(Scale(Tone(x)))
t = now()
t += one_s/4
i = 0
for c in [MajChord(x) for x in "E A D".split()]:
    g.press_chord(t,c)
    direction = STRUM_DOWN
    start_string = 0
    if i % 2:
        direction = STRUM_UP
        start_string = 5
    g.strum(t+1,one_s/32,direction,start_string)
    t += one_s
    i += 1

waitfor("hit return when you want to quit")
g.silence(now())


