#!/usr/bin/env python
#
# play "Twinkle Twinkle Little Star"
#
import sys
# uncomment to work with local directory
sys.path.insert(0,"..")
from ramu.music import *
from ramu.channel import *
sub_seq = [ 'c4 c4 g4 g4 a5 a5 gg4'.split(),
            'f4 f4 e4 e4 d4 d4 cc4'.split(),
            'a5 a5 g4 g4 f4 f4 ee4'.split() ]
full_seq =  sub_seq[0] + sub_seq[1] + sub_seq[2]*2 + sub_seq[0] + sub_seq[1]

def mk_seq_notes(s):
    t = 0.0
    lst = []
    for g in s:
        lst.append(mk_note(t,g))
        t += lst[-1].duration
    return lst

def mk_note(t,g):
    """g is of the form c4 or aa5"""
    octave   = int(g[-1])
    glyph    = g[0]
    duration = (len(g)-1)
    return SequenceNote(Tone(glyph,octave),t,duration)

rh = Rhythm(120)
c = Channel(rh)
for n in mk_seq_notes(full_seq):
    c.note(n)
