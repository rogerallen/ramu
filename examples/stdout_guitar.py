#!/usr/bin/env python
import sys
sys.path.append("..")
from ramu.instruments import guitar
from ramu import channel
from ramu.music import *
c = channel.Channel()
g = guitar.Guitar(c)

def MajChord(x): return Chord(Scale(Tone(x)))

t = 0.0
t += 1.0
i = 0
for c in [MajChord(x) for x in "E A D".split()]:
    g.press_chord(t,c)
    direction = guitar.STRUM_DOWN
    start_string = 0
    if i % 2:
        direction = guitar.STRUM_UP
        start_string = 5
    g.strum(t+1,1.0/32,direction,start_string)
    t += 1.0
    i += 1

