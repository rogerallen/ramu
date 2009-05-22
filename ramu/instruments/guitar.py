# ramu.instruments.guitar
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
from .. import music

# constants
STRUM_UP   = 0
STRUM_DOWN = 1

# A dictionary of chords & string+fret positions
# -1 = don't play, 0 = open
# chord : [ string0, string1, ... string5 ]
chord_strings = {
    "none": [ -1, -1, -1, -1, -1, -1 ],
    "C"   : [ -1,  3,  2,  0,  1,  0 ],
    "F"   : [ -1, -1,  3,  2,  1,  1 ],
    "G"   : [  3,  2,  0,  0,  0,  3 ],
    "G'"  : [  3,  5,  5,  4,  3,  3 ],
    "D"   : [ -1, -1,  0,  2,  3,  2 ],
    "A"   : [  0,  0,  2,  2,  2,  0 ],
    "A''" : [  5,  7,  7,  6,  5,  5 ],
    "E"   : [  0,  2,  2,  1,  0,  0 ],
    "Bb"  : [ -1, -1,  3,  3,  3,  1 ],
    "Eb"  : [ -1, -1,  5,  3,  4,  3 ],
    "Ab"  : [ -1, -1,  6,  5,  4,  4 ],
    "Db"  : [ -1, -1,  3,  1,  2,  1 ],
    "Gb"  : [ -1, -1,  4,  2,  1,  1 ],
    "B"   : [ -1, -1,  4,  4,  4,  2 ],

    "Cm"  : [ -1, -1,  5,  5,  4,  3 ],
    "Fm"  : [ -1, -1,  3,  1,  1,  1 ],
    "Gm"  : [ -1, -1,  5,  3,  3,  3 ],
    "Dm"  : [ -1,  0,  0,  2,  3,  1 ],
    "Am"  : [  0,  0,  2,  2,  1,  0 ],
    "Em"  : [  0,  2,  2,  0,  0,  0 ],
    "Bbm" : [ -1, -1,  3,  3,  2,  1 ],
    "Ebm" : [ -1, -1,  4,  3,  4,  2 ],
    "Abm" : [ -1, -1,  6,  4,  4,  4 ],
    "Dbm" : [ -1, -1,  2,  1,  2,  0 ],
    "Gbm" : [ -1, -1,  4,  2,  2,  2 ],
    "Bm"  : [ -1, -1,  4,  4,  3,  2 ],

    "C7"  : [ -1,  3,  2,  3,  1, -1 ],
    "F7"  : [ -1, -1,  1,  2,  1,  1 ],
    "G7"  : [  3,  2,  0,  0,  0,  1 ],
    "D7"  : [ -1, -1,  0,  2,  1,  2 ],
    "A7"  : [ -1, -1,  2,  2,  2,  3 ],
    "E7"  : [  0,  2,  0,  1,  0,  0 ],
    "Bb7" : [ -1, -1,  3,  3,  3,  4 ],
    "Eb7" : [ -1, -1,  1,  3,  2,  3 ],
    "Ab7" : [ -1, -1,  1,  1,  1,  2 ],
    "Db7" : [ -1, -1,  3,  4,  2,  4 ],
    "Gb7" : [ -1, -1,  4,  3,  2,  0 ],
    "B7"  : [ -1,  2,  1,  2,  0,  2 ],

    "Ddim"  : [ -1, -1,  0,  1,  0,  1 ], # Ab-, B-, F-
    "Ebdim" : [ -1, -1,  1,  2,  1,  2 ], # A-, C-, Gb-
    "Edim"  : [ -1, -1,  2,  3,  2,  3 ], # Bb-, Db-, G-
    "Eaug"  : [ -1, -1,  2,  1,  1,  0 ], # Ab+, C+
    "Faug"  : [ -1, -1,  3,  2,  2,  1 ], # A+, Db+
    "Gaug"  : [ -1, -1,  5,  4,  4,  3 ], # G+, B+, Eb+

    "C9"  : [  3, -1,  2,  3,  3,  3 ],
    "F9"  : [ -1,  3, -1,  2,  4,  3 ],
    "G9"  : [ -1, -1,  0,  2,  0,  1 ],
    "D9"  : [ -1, -1,  4,  2,  1,  0 ],
    "A9"  : [  0,  0,  2,  4,  2,  3 ],
    "E9"  : [  0,  2,  0,  1,  3,  2 ],
    "Bb9" : [ -1, -1,  0,  1,  1,  1 ],
    "Eb9" : [ -1, -1,  1,  0,  2,  1 ],
    "Ab9" : [ -1, -1,  1,  3,  1,  2 ],
    "Db9" : [  4, -1,  3,  4,  4,  4 ],
    "Gb9" : [ -1,  4, -1,  3,  5,  4 ],
    "B9"  : [  2, -1,  1,  2,  2,  2 ],

    }

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
class FrettedString:
    """A class representing a fretted string.
    You press() a fret and then pluck() it to make a sound
    to silence a string, press it, stop it or use a negative fret value
    """
    def __init__(self, base_note, channel):
        self.base_note = base_note # the "open" or fret 0 string
        self.channel   = channel   # the midi channel this string drives
        self.fret      = 0         # the fret that is currently pressed
        self.moving    = False     # have we been plucked?
    def __del__(self):
        self.silence(0)
    def press(self, time, fret):
        """press the given fret, turning off the current note."""
        self.silence(time)
        self.fret = fret
    def silence(self, time):
        """stop the current note on this string."""
        if self.moving:
            self.channel.note_off(time,
                                  music.Tone(self.base_note.index + self.fret),
                                  0)
        self.moving = False
    def pluck(self, time, strength ):
        """pluck the string, stopping the last note & sending the current note"""
        self.silence(time-1L)
        if self.fret >= 0:
            self.channel.note_on(time,
                                 music.Tone(self.base_note.index + self.fret),
                                 strength)
            self.moving = True
        else:
            self.fret = 0

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
class Guitar:
    # strings E, A, D, G, B, E
    string_notes = [ music.Tone('E',3),
                     music.Tone('A',4),
                     music.Tone('D',4),
                     music.Tone('G',4),
                     music.Tone('B',5),
                     music.Tone('E',5) ]
    def __init__(self, channel):
        """a guitar has 6 FrettedStrings and plays to a osxmidi.Channel"""
        self.channel = channel
        self.strings = [FrettedString(note,channel) for note in self.string_notes]
    def press_fret(self, time, string_index, fret):
        """press a fret on a string"""
        self.strings[string_index].press(time, fret)
    def press_frets(self, time, frets):
        """press the all the frets in the list"""
        assert(len(frets) == 6)
        for i in range(len(self.strings)):
            self.press_fret(time, i, frets[i])
    def press_chord(self, time, chord):
        """press the frets for a chord"""
        self.press_frets(time, chord_strings[chord])
    def silence(self, time):
        self.press_frets(time,[-1,-1,-1,-1,-1,-1])
    def strum(self, time, time_per_string, direction=STRUM_DOWN,
              start_string=0, num_strings=6, strength=0.80 ):
        """strum the guitar at a given time, moving up or down,
        starting at a certain string index, travelling for a certain
        number of strings total.  Each string is played for a certain
        duration in seconds, with a certain 'strength' 0-1.
        """
        start_string = max(0, min(start_string, 5))
        end_string = start_string + num_strings
        incr = 1
        if direction == STRUM_UP:
            end_string = start_string - num_strings
            incr = -1
        end_string = max(-1, min(end_string, 6))
        for i in range(start_string,end_string,incr):
            self.strings[i].pluck(time, strength)
            time += time_per_string
