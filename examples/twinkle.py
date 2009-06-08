#!/usr/bin/env python
#
# play "Twinkle Twinkle Little Star"
#
import sys
# uncomment to work with local directory
sys.path.insert(0,"..")
from ramu.music import *

def usage():
    print "twinkle.py stdout|midi"

def waitfor(s):
    print s
    sys.stdin.readline()

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

# twinkle's sequence of notes
sub_seq = [ 'c4 c4 g4 g4 a4 a4 gg4'.split(),
            'f4 f4 e4 e4 d4 d4 cc4'.split(),
            'g4 g4 f4 f4 e4 e4 dd4'.split() ]
full_seq =  sub_seq[0] + sub_seq[1] + sub_seq[2]*2 + sub_seq[0] + sub_seq[1]
seq = Sequence(Rhythm(144))
seq.set_sequence(mk_seq_notes(full_seq))
seq.play(chn.now,chn)

if do_midi:
    waitfor("hit return after the song is done (otherwise you'll mess up Garageband)")