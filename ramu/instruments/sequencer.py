# ramu.instruments.sequencer
#
# Copyright (C) 2009-2010 Roger Allen (rallen@gmail.com)
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
__doc__ = """
ramu.instruments.sequencer contains the code to play SequenceNotes and Sequences.

SequenceNotes - a Note with a starting time.

Sequence - a series of notes that can be played and manipulated.
"""
from ..music import *
from time import sleep

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# SequenceNote class
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class SequenceNote(object):
    """A SequenceNote is a Note that has a start time in beats from the
    start and a note.duration is measured in beats, not seconds."""
    def __init__(self, beat, note):
        self.beat = float(beat)
        self.note = note
    def __cmp__(self,other):
        return cmp(self.beat,other.beat) or cmp(self.note,other.note)

def cmp_by_beat(a,b):
        return cmp(a.beat,b.beat)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Sequence - a sequence of notes
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Sequence(object):
    """A Sequence is a container for ordered notes with an associated
    description of the tempo and time signature
    """
    def __init__(self,rhythm=None):
        self.seq = []
        self.rhythm = rhythm
    def append(self,note_or_seq):
        """Append a Note to the end of the current sequence"""
        if(type(note_or_seq) == type(Note(Tone(0)))):
            try:
                next_beat = self.seq[-1].beat + self.seq[-1].note.duration
            except IndexError:
                next_beat = 0
            seq_note = SequenceNote(next_beat,note_or_seq)
            self.seq.append(seq_note)
        else:
            assert(type(note_or_seq) == type(Sequence()))
            other = note_or_seq
            rhythm_ratio = self.rhythm.beats_per_second / other.rhythm.beats_per_second
            try:
                next_beat = self.seq[-1].beat + self.seq[-1].note.duration*rhythm_ratio
            except IndexError:
                next_beat = 0
            for seqnote in note_or_seq.seq:
                new_note = SequenceNote(next_beat,Note(seqnote.note.tone,seqnote.note.duration*rhythm_ratio))
                self.seq.append(new_note)
                next_beat += new_note.note.duration
    def insert(self,seqnote):
        """Insert a SequenceNote to the proper point"""
        assert(type(seqnote) == type(SequenceNote(0.,Note(Tone(0)))))
        self.seq.append(seqnote)
        self.seq.sort(cmp_by_beat)
    def play(self,start_time,channel):
        # XXX can this be a variant of play_and_wait?
        """play this sequence through the channel asynchronously.  Send
        the notes and return."""
        for seq_note in self.seq:
            start = start_time + seq_note.beat/self.rhythm.beats_per_second
            end   = start_time + (seq_note.beat + seq_note.note.duration)/self.rhythm.beats_per_second
            channel.play_note(start, end,
                              seq_note.note.tone, seq_note.note.strength)
    def play_and_wait(self,start_time,channel):
        """play this sequence through the channel, return when it finishes."""
        dt = 1 # pass as parameter?
        processing_time = 0.1
        t1 = channel.now + dt - processing_time
        for seq_note in self.seq:
            start = start_time + seq_note.beat/self.rhythm.beats_per_second
            end   = start_time + (seq_note.beat + seq_note.note.duration)/self.rhythm.beats_per_second
            channel.play_note(start, end,
                              seq_note.note.tone, seq_note.note.strength)
            if end > t1:
                delta = float(t1 - channel.now)
                if delta > 0:
                    sleep(delta)
                t1 = channel.now + dt - processing_time
        # remember to not return until that final note has finished
        delta = float(end - channel.now)
        if delta > 0:
            sleep(delta)
    def reverse(self):
        tmax = self.seq[-1].beat
        for n in self.seq:
            n.beat = tmax - n.beat
        self.seq.sort(cmp_by_beat)
    def flip(self,scale=Scale(Tone('c',0),"chromatic",12)):
        highest_tone = reduce(max,[x.note.tone for x in self.seq])
        lowest_tone = reduce(min,[x.note.tone for x in self.seq])
        max_index = scale.tones.index(highest_tone)
        min_index = scale.tones.index(lowest_tone)
        #print "highest",highest_tone,max_index
        for i,sn in enumerate(self.seq):
            new_index = max_index - scale.tones.index(sn.note.tone) + min_index
            new_tone = scale.tones[new_index]
            self.seq[i].note.tone = new_tone
            
