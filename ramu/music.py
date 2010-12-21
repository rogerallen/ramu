# ramu.music
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
ramu.music contains the core of the ramu music library: Tones, Scales,
Chords.

ramu.music follows concepts in music theory and is explicit with
types.  'Explicit is better than implicit.'  

ramu.music's most important types are:

Glyph - a string that denotes a Tone like 'c' or 'f#'.

Octave - an integer

Tone - the pitch or fundamental frequency of a musical note.  Tone
might be more accurately called a 'ChromaticTone' since it assumes a
twelve-step scale.  A Tone is fully specified by a Glyph and Octave.

Scale - a list of Tones that start on the tonic, specified by the name
of the scale.

Chord - a subset of Tones from a Scale, specified by the Chord name.

Note - a Tone that can be played for a certain duration of time and
with a certain strength or loudness.

Rhythm - a class containing beats per second, etc.

"""
from math import floor

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

def glypho_to_chromatic_tone_index(glyph,octave):
    assert(glyph.lower() in chromatic_glyphs)
    v = chromatic_glyphs.index( glyph.lower() ) % TONES_PER_CHROMATIC_OCTAVE
    o = octave
    if octave == None:
        o = 0
    return TONES_PER_CHROMATIC_OCTAVE * o + v

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Tone
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Tone(object):
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
            index = glypho_to_chromatic_tone_index(index_or_glyph,octave)
            self.canonical = (octave == None)
        self.frequency = chromatic_tone_to_frequency(index)
        self._index = index
    @classmethod
    def fromGlypho(cls, glyph, octave=None ):
        """initializes a ChromaticTone from a glyph-octave pair"""
        index = glypho_to_chromatic_tone_index(glyph,octave)
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
    def __cmp__(self,other):
        return cmp(self.index,other.index)
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
    def __cmp__(self,other):
        return cmp(self.tone,other.tone) or cmp(self.duration,other.duration) or cmp(self.strength,other.strength)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Scale data
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# name to chromatic index dictionary, one octave's worth of indices
scale_index_offsets = {
    # 5 notes
    "pelog"                        : [0, 1, 3, 6, 10],

    "balinese"                     : [0, 1, 3, 7, 8],

    "japanese a"                   : [0, 1, 5, 7, 8],

    "hirajoshi"                    : [0, 2, 3, 7, 8],

    "kumoi"                        : [0, 2, 3, 7, 9],

    "chinese mongolian"            : [0, 2, 4, 7, 9],
    "diatonic"                     : [0, 2, 4, 7, 9],

    "japanese b"                   : [0, 2, 5, 7, 8],

    "pentatonic major"             : [0, 2, 5, 7, 9],

    "egyptian"                     : [0, 2, 5, 7, 10],

    "pentatonic minor"             : [0, 3, 5, 7, 10],

    "chinese"                      : [0, 4, 6, 7, 11],

    # 6 notes
    "six tone symmetrical"         : [0, 1, 4, 5, 8, 9],

    "prometheus neopolitan"        : [0, 1, 4, 6, 9, 10],

    "auxiliary augmented"          : [0, 2, 4, 6, 8, 10],
    "whole tone"                   : [0, 2, 4, 6, 8, 10],

    "prometheus"                   : [0, 2, 4, 6, 9, 10],

    "dominant 7th"                 : [0, 2, 5, 7, 9, 10],

    "augmented"                    : [0, 3, 4, 7, 8, 11],

    "blues"                        : [0, 3, 5, 6, 7, 10],

    # 7 notes
    "mela bhavapriya"              : [0, 1, 2, 5, 7, 8, 9],
    "mela kanakangi"               : [0, 1, 2, 5, 7, 8, 9],

    "mela ratnangi"                : [0, 1, 2, 5, 7, 8, 10],

    "mela ganamurti"               : [0, 1, 2, 5, 7, 8, 11],

    "mela vanaspati"               : [0, 1, 2, 5, 7, 9, 10],

    "mela manavati"                : [0, 1, 2, 5, 7, 9, 11],

    "mela tanarupi"                : [0, 1, 2, 5, 7, 10, 11],

    "mela salagam"                 : [0, 1, 2, 6, 7, 8, 9],

    "mela jalarnavam"              : [0, 1, 2, 6, 7, 8, 10],

    "mela jhalavarali"             : [0, 1, 2, 6, 7, 8, 11],

    "mela navanitam"               : [0, 1, 2, 6, 7, 9, 10],

    "mela pavani"                  : [0, 1, 2, 6, 7, 9, 11],
    "mela suvarnangi"              : [0, 1, 2, 6, 7, 9, 11],

    "mela raghupriya"              : [0, 1, 2, 6, 7, 10, 11],

    "diminished whole tone"        : [0, 1, 3, 4, 6, 8, 10],
    "super locrian"                : [0, 1, 3, 4, 6, 8, 10],

    "half diminished"              : [0, 1, 3, 5, 6, 8, 10],
    "locrian"                      : [0, 1, 3, 5, 6, 8, 10],

    "mela senavati"                : [0, 1, 3, 5, 7, 8, 9],

    "bhairavi theta"               : [0, 1, 3, 5, 7, 8, 10],
    "mela hanumattodi"             : [0, 1, 3, 5, 7, 8, 10],
    "neopolitan minor"             : [0, 1, 3, 5, 7, 8, 10],
    "phrygian"                     : [0, 1, 3, 5, 7, 8, 10],

    "mela dhenuka"                 : [0, 1, 3, 5, 7, 8, 11],
    "neopolitan"                   : [0, 1, 3, 5, 7, 8, 11],

    "javaneese"                    : [0, 1, 3, 5, 7, 9, 10],
    "mela natakapriya"             : [0, 1, 3, 5, 7, 9, 10],

    "mela kokilapriya"             : [0, 1, 3, 5, 7, 9, 11],
    "neoploitan major"             : [0, 1, 3, 5, 7, 9, 11],

    "mela rupavati"                : [0, 1, 3, 5, 7, 10, 11],

    "mela gavambodhi"              : [0, 1, 3, 6, 7, 8, 9],

    "mela subhapantuvarali"        : [0, 1, 3, 6, 7, 8, 11],
    "todi theta"                   : [0, 1, 3, 6, 7, 8, 11],

    "mela sadvidhamargini"         : [0, 1, 3, 6, 7, 9, 10],

    "mela divyamani"               : [0, 1, 3, 6, 7, 10, 11],

    "oriental a"                   : [0, 1, 4, 5, 6, 8, 10],

    "persian"                      : [0, 1, 4, 5, 6, 8, 11],

    "oriental b"                   : [0, 1, 4, 5, 6, 9, 10],

    "mela gayakapriya"             : [0, 1, 4, 5, 7, 8, 9],
    "mela mayamalavagaula"         : [0, 1, 4, 5, 7, 8, 9],

    "jewish ahaba rabba"           : [0, 1, 4, 5, 7, 8, 10],
    "mela vakulabharanam"          : [0, 1, 4, 5, 7, 8, 10],
    "spanish gypsy"                : [0, 1, 4, 5, 7, 8, 10],

    "bhairav theta"                : [0, 1, 4, 5, 7, 8, 11],
    "byzantine"                    : [0, 1, 4, 5, 7, 8, 11],
    "double harmonic"              : [0, 1, 4, 5, 7, 8, 11],
    "hungarian gypsy persian"      : [0, 1, 4, 5, 7, 8, 11],

    "mela chakravakam"             : [0, 1, 4, 5, 7, 9, 10],

    "mela suryakantam"             : [0, 1, 4, 5, 7, 9, 11],

    "mela hatakambari"             : [0, 1, 4, 5, 7, 10, 11],

    "mela dhavalambari"            : [0, 1, 4, 6, 7, 8, 9],

    "mela namanarayani"            : [0, 1, 4, 6, 7, 8, 10],

    "mela kamavardhani"            : [0, 1, 4, 6, 7, 8, 11],
    "purvi theta"                  : [0, 1, 4, 6, 7, 8, 11],

    "mela ramapriya"               : [0, 1, 4, 6, 7, 9, 10],

    "marva theta"                  : [0, 1, 4, 6, 7, 9, 11],
    "mela gamanasrama"             : [0, 1, 4, 6, 7, 9, 11],

    "mela visvambari"              : [0, 1, 4, 6, 7, 10, 11],

    "enigmatic"                    : [0, 1, 4, 6, 8, 10, 11],

    "half diminished #2"           : [0, 2, 3, 5, 6, 8, 10],

    "mela jhankaradhvani"          : [0, 2, 3, 5, 7, 8, 9],

    "aeolian"                      : [0, 2, 3, 5, 7, 8, 10],
    "asavari theta"                : [0, 2, 3, 5, 7, 8, 10],
    "ethiopian geez & ezel"        : [0, 2, 3, 5, 7, 8, 10],
    "mela natabhairavi"            : [0, 2, 3, 5, 7, 8, 10],
    "pure minor"                   : [0, 2, 3, 5, 7, 8, 10],
    "melodic down minor"           : [0, 2, 3, 5, 7, 8, 10],
    "minor"                        : [0, 2, 3, 5, 7, 8, 10],

    "harmonic minor"               : [0, 2, 3, 5, 7, 8, 11],
    "mela kiravani"                : [0, 2, 3, 5, 7, 8, 11],
    "mohammedan"                   : [0, 2, 3, 5, 7, 8, 11],

    "dorian"                       : [0, 2, 3, 5, 7, 9, 10],
    "kafi theta"                   : [0, 2, 3, 5, 7, 9, 10],
    "mela kharaharapriya"          : [0, 2, 3, 5, 7, 9, 10],

    "hawaiian"                     : [0, 2, 3, 5, 7, 9, 11],
    "mela gaurimanohari"           : [0, 2, 3, 5, 7, 9, 11],
    "melodic minor"                : [0, 2, 3, 5, 7, 9, 11],
    "melodic up minor"             : [0, 2, 3, 5, 7, 9, 11],

    "mela varunapriya"             : [0, 2, 3, 5, 7, 10, 11],

    "mela syamalangi"              : [0, 2, 3, 6, 7, 8, 9],

    "lydian diminished"            : [0, 2, 3, 6, 7, 8, 10],
    "mela sanmukhapriya"           : [0, 2, 3, 6, 7, 8, 10],

    "hungarian gypsy"              : [0, 2, 3, 6, 7, 8, 11],
    "hungarian minor"              : [0, 2, 3, 6, 7, 8, 11],
    "mela simhendramadhyama"       : [0, 2, 3, 6, 7, 8, 11],

    "mela hemavati"                : [0, 2, 3, 6, 7, 9, 10],
    "roumanian minor"              : [0, 2, 3, 6, 7, 9, 10],

    "mela dharmavati"              : [0, 2, 3, 6, 7, 9, 11],

    "mela nitimati"                : [0, 2, 3, 6, 7, 10, 11],

    "arabian b"                    : [0, 2, 4, 5, 6, 8, 10],
    "major locrian"                : [0, 2, 4, 5, 6, 8, 10],

    "mela mararanjani"             : [0, 2, 4, 5, 7, 8, 9],

    "hindu"                        : [0, 2, 4, 5, 7, 8, 10],
    "hindustan"                    : [0, 2, 4, 5, 7, 8, 10],
    "mela charukesi"               : [0, 2, 4, 5, 7, 8, 10],

    "mela sarasangi"               : [0, 2, 4, 5, 7, 8, 11],

    "khamaj theta"                 : [0, 2, 4, 5, 7, 9, 10],
    "mela harikambhoji"            : [0, 2, 4, 5, 7, 9, 10],
    "mixolydian"                   : [0, 2, 4, 5, 7, 9, 10],

    "bilaval theta"                : [0, 2, 4, 5, 7, 9, 11],
    "ethiopian a raray"            : [0, 2, 4, 5, 7, 9, 11],
    "ionian"                       : [0, 2, 4, 5, 7, 9, 11],
    "major"                        : [0, 2, 4, 5, 7, 9, 11],
    "mela dhirasankarabharana"     : [0, 2, 4, 5, 7, 9, 11],

    "mela naganandini"             : [0, 2, 4, 5, 7, 10, 11],

    "mela kantamani"               : [0, 2, 4, 6, 7, 8, 9],

    "lydian minor"                 : [0, 2, 4, 6, 7, 8, 10],
    "mela risabhapriya"            : [0, 2, 4, 6, 7, 8, 10],

    "mela latangi"                 : [0, 2, 4, 6, 7, 8, 11],

    "mela vaschaspati"             : [0, 2, 4, 6, 7, 9, 10],
    "overtone"                     : [0, 2, 4, 6, 7, 9, 10],
    "overtone dominant"            : [0, 2, 4, 6, 7, 9, 10],

    "kalyan theta"                 : [0, 2, 4, 6, 7, 9, 11],
    "lydian"                       : [0, 2, 4, 6, 7, 9, 11],
    "mela mechakalyani"            : [0, 2, 4, 6, 7, 9, 11],

    "mela chitrambari"             : [0, 2, 4, 6, 7, 10, 11],

    "leading whole tone"           : [0, 2, 4, 6, 8, 9, 10],

    "lydian augmented"             : [0, 2, 4, 6, 8, 9, 11],

    "mela yagapriya"               : [0, 3, 4, 5, 7, 8, 9],

    "mela ragavardhani"            : [0, 3, 4, 5, 7, 8, 10],

    "mela gangeyabhusani"          : [0, 3, 4, 5, 7, 8, 11],

    "mela vagadhisvari"            : [0, 3, 4, 5, 7, 9, 10],

    "mela sulini"                  : [0, 3, 4, 5, 7, 9, 11],

    "mela chalanata"               : [0, 3, 4, 5, 7, 10, 11],

    "mela sucharitra"              : [0, 3, 4, 6, 7, 8, 9],

    "mela jyotisvarupini"          : [0, 3, 4, 6, 7, 8, 10],

    "mela dhatuvardhani"           : [0, 3, 4, 6, 7, 8, 11],

    "hungarian major"              : [0, 3, 4, 6, 7, 9, 10],
    "mela nasikabhusani"           : [0, 3, 4, 6, 7, 9, 10],

    "mela kosalam"                 : [0, 3, 4, 6, 7, 9, 11],

    "mela rasikapriya"             : [0, 3, 4, 6, 7, 10, 11],

    # 8 notes
    "jewish adonai malakh"         : [0, 1, 2, 3, 5, 7, 9, 10],

    "eight tone spanish"           : [0, 1, 3, 4, 5, 6, 8, 10],

    "auxiliary diminished blues"   : [0, 1, 3, 4, 6, 7, 9, 10],

    "jewish magen abot"            : [0, 1, 3, 4, 6, 8, 10, 11],

    "algerian"                     : [0, 2, 3, 5, 6, 7, 8, 11],

    "arabian a"                    : [0, 2, 3, 5, 6, 8, 9, 11],
    "auxiliary diminished"         : [0, 2, 3, 5, 6, 8, 9, 11],
    "diminished"                   : [0, 2, 3, 5, 6, 8, 9, 11],

    "japanese ichikosucho"         : [0, 2, 4, 5, 6, 7, 9, 11],

    # 9 notes
    "nine tone scale"              : [0, 2, 3, 4, 6, 7, 8, 9, 11],

    "japanese taishikicho"         : [0, 2, 4, 5, 6, 7, 9, 10, 11],

    # 12 notes
    "chromatic"                    : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],

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
        return [x.glyph for x in self.tones]
    glyphs = property(get_glyphs)
    def intersect(self,other):
        """return the number of notes that are the same in both scales"""
        set0 = set(self.tones)
        set1 = set(other.tones)
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
    toneset = set(tones)
    for n in scale_names:
        assert(n in scale_index_offsets.keys())
        for i in range(TONES_PER_CHROMATIC_OCTAVE):
            scale = Scale(Tone(i),n)
            scaleset = set(scale.tones)
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
# Rhythm class
#
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
class Rhythm(object):
    def __init__(self, beats_per_minute, beats_per_measure=4):
        self.beats_per_minute = beats_per_minute
        self.beats_per_measure = beats_per_measure
    def get_beats_per_second(self):
        return self.beats_per_minute/60.0
    beats_per_second = property(get_beats_per_second)
    def get_measure(cur_time):
        measure = cur_time / self.beats_per_second / self.beats_per_measure
        return floor(measure)
    def get_beat(cur_time):
        return cur_time/self.beats_per_second

