#!/usr/bin/env python
import sys
# uncomment to work with local directory
sys.path.insert(0,"..")
from ramu.instruments import guitar
from ramu.music import *

from ramu.channel import Channel
chan = Channel()
g = guitar.Guitar(chan)

def MajChord(x): return Chord(Scale(Tone(x)))

t = chan.now
t += chan.one_second
i = 0
for c in [MajChord(x) for x in "E A D".split()]:
    g.press_chord(t,c)
    direction = guitar.STRUM_DOWN
    start_string = 0
    if i % 2:
        direction = guitar.STRUM_UP
        start_string = 5
    g.strum(t,1.0/32,direction,start_string)
    t += chan.one_second
    i += 1
g.silence(t)
