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

def MkChord(t,s,c):
    oct = 1
    if c == "9th":
        oct = 2
    return music.Chord(music.Scale(music.Tone(t),s,oct),c)

# constants
STRUM_UP   = 0
STRUM_DOWN = 1

# A dictionary of chords & string+fret positions
# -1 = don't play, 0 = open
# chord : [ string0, string1, ... string5 ]
chord_strings = {
    None  : [ -1, -1, -1, -1, -1, -1 ],
    MkChord("C","major","5th") : [ -1,  3,  2,  0,  1,  0 ],
    MkChord("F","major","5th")   : [ -1, -1,  3,  2,  1,  1 ],
    MkChord("G","major","5th")   : [  3,  2,  0,  0,  0,  3 ],
    #MkChord("G'","major","5th")  : [  3,  5,  5,  4,  3,  3 ],
    MkChord("D","major","5th")   : [ -1, -1,  0,  2,  3,  2 ],
    MkChord("A","major","5th")   : [  0,  0,  2,  2,  2,  0 ],
    #MkChord("A''","major","5th") : [  5,  7,  7,  6,  5,  5 ],
    MkChord("E","major","5th")   : [  0,  2,  2,  1,  0,  0 ],
    MkChord("Bb","major","5th")  : [ -1, -1,  3,  3,  3,  1 ],
    MkChord("Eb","major","5th")  : [ -1, -1,  5,  3,  4,  3 ],
    MkChord("Ab","major","5th")  : [ -1, -1,  6,  5,  4,  4 ],
    MkChord("Db","major","5th")  : [ -1, -1,  3,  1,  2,  1 ],
    MkChord("Gb","major","5th")  : [ -1, -1,  4,  2,  1,  1 ],
    MkChord("B","major","5th")   : [ -1, -1,  4,  4,  4,  2 ],

    MkChord("C","minor","5th")  : [ -1, -1,  5,  5,  4,  3 ],
    MkChord("F","minor","5th")  : [ -1, -1,  3,  1,  1,  1 ],
    MkChord("G","minor","5th")  : [ -1, -1,  5,  3,  3,  3 ],
    MkChord("D","minor","5th")  : [ -1,  0,  0,  2,  3,  1 ],
    MkChord("A","minor","5th")  : [  0,  0,  2,  2,  1,  0 ],
    MkChord("E","minor","5th")  : [  0,  2,  2,  0,  0,  0 ],
    MkChord("Bb","minor","5th") : [ -1, -1,  3,  3,  2,  1 ],
    MkChord("Eb","minor","5th") : [ -1, -1,  4,  3,  4,  2 ],
    MkChord("Ab","minor","5th") : [ -1, -1,  6,  4,  4,  4 ],
    MkChord("Db","minor","5th") : [ -1, -1,  2,  1,  2,  0 ],
    MkChord("Gb","minor","5th") : [ -1, -1,  4,  2,  2,  2 ],
    MkChord("B","minor","5th")  : [ -1, -1,  4,  4,  3,  2 ],

    MkChord("C","major","7th")  : [ -1,  3,  2,  3,  1, -1 ],
    MkChord("F","major","7th")  : [ -1, -1,  1,  2,  1,  1 ],
    MkChord("G","major","7th")  : [  3,  2,  0,  0,  0,  1 ],
    MkChord("D","major","7th")  : [ -1, -1,  0,  2,  1,  2 ],
    MkChord("A","major","7th")  : [ -1, -1,  2,  2,  2,  3 ],
    MkChord("E","major","7th")  : [  0,  2,  0,  1,  0,  0 ],
    MkChord("Bb","major","7th") : [ -1, -1,  3,  3,  3,  4 ],
    MkChord("Eb","major","7th") : [ -1, -1,  1,  3,  2,  3 ],
    MkChord("Ab","major","7th") : [ -1, -1,  1,  1,  1,  2 ],
    MkChord("Db","major","7th") : [ -1, -1,  3,  4,  2,  4 ],
    MkChord("Gb","major","7th") : [ -1, -1,  4,  3,  2,  0 ],
    MkChord("B","major","7th")  : [ -1,  2,  1,  2,  0,  2 ],

    MkChord("D","major","dim")  : [ -1, -1,  0,  1,  0,  1 ], # Ab-, B-, F-
    MkChord("Eb","major","dim") : [ -1, -1,  1,  2,  1,  2 ], # A-, C-, Gb-
    MkChord("E","major","dim")  : [ -1, -1,  2,  3,  2,  3 ], # Bb-, Db-, G-
    MkChord("E","major","aug")  : [ -1, -1,  2,  1,  1,  0 ], # Ab+, C+
    MkChord("F","major","aug")  : [ -1, -1,  3,  2,  2,  1 ], # A+, Db+
    MkChord("G","major","aug")  : [ -1, -1,  5,  4,  4,  3 ], # G+, B+, Eb+

    MkChord("C","major","9th")  : [  3, -1,  2,  3,  3,  3 ],
    MkChord("F","major","9th")  : [ -1,  3, -1,  2,  4,  3 ],
    MkChord("G","major","9th")  : [ -1, -1,  0,  2,  0,  1 ],
    MkChord("D","major","9th")  : [ -1, -1,  4,  2,  1,  0 ],
    MkChord("A","major","9th")  : [  0,  0,  2,  4,  2,  3 ],
    MkChord("E","major","9th")  : [  0,  2,  0,  1,  3,  2 ],
    MkChord("Bb","major","9th") : [ -1, -1,  0,  1,  1,  1 ],
    MkChord("Eb","major","9th") : [ -1, -1,  1,  0,  2,  1 ],
    MkChord("Ab","major","9th") : [ -1, -1,  1,  3,  1,  2 ],
    MkChord("Db","major","9th") : [  4, -1,  3,  4,  4,  4 ],
    MkChord("Gb","major","9th") : [ -1,  4, -1,  3,  5,  4 ],
    MkChord("B","major","9th")  : [  2, -1,  1,  2,  2,  2 ],

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
        self.silence(self.channel.now)
    def press(self, time, fret):
        """press the given fret, turning off the current note."""
        self.silence(time)
        self.fret = fret
    def silence(self, time):
        """stop the current note on this string."""
        if self.moving:
            self.channel.stop_note(time,
                                   music.Tone(self.base_note.index + self.fret),
                                   0)
        self.moving = False
    def pluck(self, time, strength ):
        """pluck the string, stopping the last note & sending the current note"""
        self.silence(time)
        if self.fret >= 0:
            self.channel.start_note(time,
                                    music.Tone(self.base_note.index + self.fret),
                                    strength)
            self.moving = True

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
class Guitar(object):
    # strings E, A, D, G, B, E
    string_notes = [ music.Tone('E',3),
                     music.Tone('A',3),
                     music.Tone('D',4),
                     music.Tone('G',4),
                     music.Tone('B',4),
                     music.Tone('E',5) ]
    def __init__(self, channel):
        """a guitar has 6 FrettedStrings and plays to a ramu.channel"""
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
        """silence all strings by muting all frets"""
        self.press_frets(time,[-1,-1,-1,-1,-1,-1])
    def mute(self,time):
        """silence, without the permanent effect on frets"""
        cur_frets = [ s.fret for s in self.strings ]
        self.press_frets(time,cur_frets)
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
            if self.strings[i].moving:
                time += time_per_string

class TwelveStringGuitar(object):
    # twelve string guitar has 2nd set of strings, the first 4 being
    # 1 octave higher than the normal guitar strings.  The last 2
    # are in unison
    second_string_notes = [ music.Tone('E',4),
                            music.Tone('A',4),
                            music.Tone('D',5),
                            music.Tone('G',5),
                            music.Tone('B',4),
                            music.Tone('E',5) ]
    def __init__(self, channel):
        """create 2 guitars and override the 2nd guitar's strings"""
        self.guitars = []
        self.guitars.append(Guitar(channel))
        self.guitars.append(Guitar(channel))
        self.guitars[1].strings = [FrettedString(note,channel) for note in self.second_string_notes]
    def press_fret(self, time, string_index, fret):
        for g in self.guitars:
            g.press_fret(time, string_index, fret)
    def press_frets(self, time, frets):
        for g in self.guitars:
            g.press_frets(time, frets)
    def press_chord(self, time, chord):
        for g in self.guitars:
            g.press_chord(time, chord)
    def silence(self, time):
        for g in self.guitars:
            g.silence(time)
    def mute(self,time):
        for g in self.guitars:
            g.mute(time)
    def strum(self, time, time_per_string, direction=STRUM_DOWN,
              start_string=0, num_strings=6, strength=0.80 ):
        for g in self.guitars:
            g.strum(time, time_per_string, direction, start_string, num_strings, strength)
            time += time_per_string/2.0
