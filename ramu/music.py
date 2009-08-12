# ramu.music
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
__doc__ = """
Music is made in a hierarchy:
  Starting from a basic tone only with frequency.
  Tones are a way to denote the frequency of the sound
  Scales contain Tones
  Chords are derived from Scales

  Notes are Tones + duration time
  SequenceNotes are Tones + duration + start time
"""
import sets

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# glypho = glyphs + octaves
# Different 'glyphs' to represent notes in a chromatic scale
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# this is a chromatic octave
TONES_PER_CHROMATIC_OCTAVE = 12

chromatic_glyphs = '''\
c c+ d d+ e f f+ g g+ a a+ b \
c d- d e- e f g- g a- a b- b \
c db d eb e f gb g ab a bb b \
c c# d d# e f f# g g# a a# b'''.split()

# a handy little list
# XXX
circle_of_fifths = [
    "c", "g", "d", "a", "e", "b", "g-", "d-", "a-", "e-", "b-", "f"
    ]

# A5 = 440.0 Hz
def chromatic_tone_to_frequency(index):
    """convert chromatic tone index to frequency"""
    return ( 440.0 * 2.0**( (index - 69) / float(TONES_PER_CHROMATIC_OCTAVE)))

def glphyo_to_chromatic_tone_index(glyph,octave):
    assert(glyph.lower() in chromatic_glyphs)
    v = chromatic_glyphs.index( glyph.lower() ) % TONES_PER_CHROMATIC_OCTAVE
    o = octave
    if octave == None:
        o = 0
    return TONES_PER_CHROMATIC_OCTAVE * o + v

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# BasicTone
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class BasicTone(object):
    """Base class for describing the frequency of a sound.
    Not alot here at the moment"""
    def __init__(self,frequency):
        self.frequency = frequency
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Tone
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Tone(BasicTone):
    """Tone is a way to describe the frequency of a sound.used
    in chromatic Western Music.  The  index is an integer where
    * 0 = the lowest note ( glyph C, octave 0 )
    * 60 = middle C       ( glyph C, octave 5 )
    * 69 = A440           ( glyph A, octave 5 )
    This probably wants to be ChromaticTone, but that name is too long.
    If the note is initialized only by a glyph, the Tone is 'canonical'
    or without an octave.  This allows for abstract calculations of
    theory, rather than a Tone that can be played.
    """
    def __init__( self, index_or_glyph, octave=None ):
        """basic way to initialize a class is via an index"""
        if type(index_or_glyph) == type(0):
            assert(octave == None)
            index = index_or_glyph
            self.canonical = (index < TONES_PER_CHROMATIC_OCTAVE)
        else:
            index = glphyo_to_chromatic_tone_index(index_or_glyph,octave)
            self.canonical = (octave == None)
        BasicTone.__init__(self,chromatic_tone_to_frequency(index))
        self._index = index
    @classmethod
    def fromGlypho(cls, glyph, octave=None ):
        """initializes a ChromaticTone from a glyph-octave pair"""
        index = glphyo_to_chromatic_tone_index(glyph,octave)
        return cls(index)
    def get_index(self):
        return self._index
    index = property(get_index)
    def get_glyph( self ):
        """return the glyph (no octave) of index"""
        return chromatic_glyphs[ self._index % TONES_PER_CHROMATIC_OCTAVE ]
    glyph = property(get_glyph)
    def get_octave( self ):
        """return the octave of index"""
        if self.canonical:
            return None
        return int( self.index / TONES_PER_CHROMATIC_OCTAVE )
    octave = property(get_octave)
    def __str__( self ):
        """return glyph + octave as string"""
        if self.canonical:
            octave_str = ""
        else:
            octave_str = str(self.octave)
        return self.glyph + octave_str
    def __repr__( self ):
        return str(self)
    def __hash__(self):
        return hash(self.index)
    def __eq__(self, other):
        return self.index == other.index
    def __ne__(self, other):
        return self.index != other.index
    def __gt__(self, other):
        return self.index > other.index
    def __ge__(self, other):
        return self.index >= other.index
    def __lt__(self, other):
        return self.index < other.index
    def __le__(self, other):
        return self.index <= other.index
    def __add__(self, other):
        if type(other) == type(Tone(0)):
            offset = other.index
        elif type(other) == type(0):
            offset = other
        new_index = self.index + offset
        if self.canonical:
            new_index %= TONES_PER_CHROMATIC_OCTAVE
            return Tone(chromatic_glyphs[new_index])
        return Tone(new_index)
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Note data
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def bpm_to_seconds(bpm):
    return 60.0/bpm

def bpm_note_divisor_to_seconds(bpm,note_divisor):
    return bpm_to_seconds(bpm)/note_divisor

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Note class
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Note(object):
    """A note is associated with a tone, a duration (in seconds) and
    a strength value (0.0 - 1.0)."""
    def __init__( self, note_tone, duration=0.25, strength=0.75 ):
        assert(type(note_tone) == type(Tone(0)))
        self.tone     = note_tone
        self.duration = float(duration)
        assert(0.0 <= strength <= 1.0)
        self.strength = float(strength)
    def __eq__(self, other):
        return self.tone == other.tone and self.duration == other.duration and self.strength == other.strength
    def __ne__(self, other):
        return not self == other
    def __gt__(self, other):
        return NotImplemented
    def __ge__(self, other):
        return NotImplemented
    def __lt__(self, other):
        return NotImplemented
    def __le__(self, other):
        return NotImplemented

class SequenceNote(object):
    # XXX should derive this from Note
    # XXX beat AND duration? this looks fishy...
    """A SequenceNote is associated with a tone, a start time, a
    duration (in seconds) and a strength value (0.0 - 1.0)."""
    def __init__( self, note_tone, beat=0.0, duration=0.25, strength=0.75 ):
        assert(type(note_tone) == type(Tone(0)))
        self.tone     = note_tone
        self.beat     = float(beat)
        self.duration = float(duration)
        assert(0.0 <= strength <= 1.0)
        self.strength = float(strength)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Scale data
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# name to chromatic index dictionary, one octave's worth of indices
scale_index_offsets = {
    # 12 tones per scale
    "chromatic"  : [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ],
    # 11,10,9,8 tones per scale ?
    # 7 tones per scale
    "major"      : [ 0,    2,    4, 5,    7,    9,     11 ],
    "minor"      : [ 0,    2, 3,    5,    7, 8,    10 ],
    "aeolian"    : [ 0,    2, 3,    5,    7, 8,    10 ],
    # "dorian"     : [], # xxx
    "ionian"     : [ 0,    2,    4, 5,    7,    9,     11 ],
    #"locrian"    : [], # xxx
    #"lydian"     : [], # xxx
    #"mixolydian" : [], # xxx
    #"phrygian"   : [], # xxx
    # 6 notes per scale xxx
    "hexatonic"  : [ 0,    2,    4,    6,   8,     10     ],
    # 5 notes per scale
    "pentatonic" : [ 0,    2,       5,    7,    9 ],
    }

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Scale class
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Scale(object):
    """Scales are made up of tones"""
    def __init__(self, tonic, name="major", octaves=1):
        assert(type(tonic) == type(Tone(0)))
        self.tonic = tonic
        assert(name in scale_index_offsets.keys())
        self.name  = name
        self.tones = []
        self.octaves = octaves
        for j in range(octaves):
            for i in scale_index_offsets[self.name]:
                self.tones.append(self.tonic + j*TONES_PER_CHROMATIC_OCTAVE + i)
    def get_glyphs(self):
        return ([x.glyph for x in self.tones])
    glyphs = property(get_glyphs)
    def intersect(self,other):
        """return the number of notes that are the same in both scales"""
        set0 = sets.Set(self.tones)
        set1 = sets.Set(other.tones)
        return sorted([x for x in set0.intersection(set1)])
    def __str__(self):
        s = str(self.tonic) + "_" + self.name
        if self.octaves > 1:
            s += "_" + str(self.octaves) + "octaves"
        return s
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(hash(self.tonic) + hash(self.name))
    def __eq__(self, other):
        # XXX different octaves
        return self.tonic == other.tonic and self.name == other.name
    def __ne__(self, other):
        return not self == other
    def __gt__(self, other):
        return NotImplemented
    def __ge__(self, other):
        return NotImplemented
    def __lt__(self, other):
        return NotImplemented
    def __le__(self, other):
        return NotImplemented

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def get_scales_with_tones(tones,scale_names=['major','minor']):
    """return a list of all scales that contain the given tones.  Note
    that we compare via glyphs rather than tones in order to avoid
    comparing the octaves.
    
    Keyword arguments:
    tones       -- list of tones to consider
    scale_names -- only look within the scale_names type of scales.
    """
    assert(type(tones)==type(list()))
    assert(type(scale_names)==type(list()))
    scales = []
    toneset = sets.Set(tones)
    for n in scale_names:
        assert(n in scale_index_offsets.keys())
        for i in range(TONES_PER_CHROMATIC_OCTAVE):
            scale = Scale(Tone(i),n)
            scaleset = sets.Set(scale.tones)
            if toneset.intersection(scaleset) == toneset:
               scales.append(scale)
    return scales
        
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
# Chord data
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# name to diatonic index
chord_index_offsets = {
    "3rd"    : [ 0, 2 ],
    "dim"    : [ 0, 2, 3 ],
    "5th"    : [ 0, 2, 4 ],
    "aug"    : [ 0, 2, 5 ],
    "dim7th" : [ 0, 2, 3, 5],
    "7th"    : [ 0, 2, 4, 6],
    "aug7th" : [ 0, 2, 5, 7],
    "9th"    : [ 0, 2, 4, 6, 8 ],
    "11th"   : [ 0, 2, 4, 6, 8, 10]
    }

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Chord class
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Chord(object):
    def __init__( self, chord_scale, name="5th", octaves=1 ):
        assert(type(chord_scale) == type(Scale(Tone.fromGlypho('c'))))
        self.scale  = chord_scale
        assert(name in chord_index_offsets.keys())
        self.name   = name
        self.tones = []
        for j in range(octaves):
            tones_per_octave = len(self.scale.tones)
            #print chord_index_offsets
            #print self.scale.tones
            for i in chord_index_offsets[self.name]:
                #print i
                ii = self.scale.tones[i].index + j*TONES_PER_CHROMATIC_OCTAVE
                self.tones.append(Tone(ii))
    def __hash__(self):
        return hash(hash(self.scale) + hash(self.name))
    def __eq__(self, other):
        # XXX different octaves
        return self.scale == other.scale and self.name == other.name
    def __ne__(self, other):
        return not self == other
    def __gt__(self, other):
        return NotImplemented
    def __ge__(self, other):
        return NotImplemented
    def __lt__(self, other):
        return NotImplemented
    def __le__(self, other):
        return NotImplemented

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Rhythm class XXX TimeSignature ???
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Rhythm(object):
    def __init__(self, beats_per_minute):
        self._beats_per_minute = beats_per_minute
    def get_beats_per_second(self):
        return self._beats_per_minute/60.0
    beats_per_second = property(get_beats_per_second)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Sequence - a sequence of notes
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Sequence(object):
    """A Sequence is a container for ordered notes with an associated
    description of the tempo and time signature
    """
    def __init__(self,rhythm=None):
        self.seq = []
        self._rhythm = rhythm
    def set_sequence(self,sequence):
        self.seq = sequence
    def play(self,start_time,channel):
        """play this sequence through the channel"""
        for note in self.seq:
            start = start_time + note.beat/self._rhythm.beats_per_second
            end   = start_time + (note.beat + note.duration)/self._rhythm.beats_per_second
            channel.play_note(start,end,note.tone,note.strength)

