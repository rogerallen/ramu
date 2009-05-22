#!/usr/bin/env python
import sys
import unittest
sys.path.append("..")
from music import *

# ======================================================================
class TestChord(unittest.TestCase):
    def testCMajor(self):
        tst = Chord(Scale(Tone('c')))
        ref = map(Tone,"c e g".split())
        for (t,r) in zip(tst.tones,ref):
            self.assertEqual(t,r)        

    def testCMajor7th(self):
        tst = Chord(Scale(Tone('c')),"7th")
        ref = map(Tone,"c e g b".split())
        for (t,r) in zip(tst.tones,ref):
            self.assertEqual(t,r)        
# XXX test multiple octaves

# ======================================================================
class TestNote(unittest.TestCase):
    def testBasic(self):
        n = Note(Tone('c'),0.5,0.75)
        self.assertEqual(n.tone, Tone('c'))
        self.assertEqual(n.duration, 0.5)
        self.assertEqual(n.strength, 0.75)
# XXX test SeqNote

# ======================================================================
class TestScale(unittest.TestCase):
    def testCMajor(self):
        tst = Scale(Tone('c'))
        ref = map(Tone.fromGlypho,"c d e f g a b".split())
        for (t,r) in zip(tst.tones,ref):
            self.assertEqual(t,r)        

    def testCMinor(self):
        tst = Scale(Tone('c'),"minor")
        ref = map(Tone.fromGlypho,"c d d+ f g g+ a+".split())
        for (t,r) in zip(tst.tones,ref):
            self.assertEqual(t,r)        

# ======================================================================
class TestTone(unittest.TestCase):
    def testBasic(self):
        t = BasicTone(100.0)
        self.assertEqual(100.0,t.frequency)

    def testA440(self):
        t = Tone(69)
        self.assertEqual(440.0,t.frequency)
        self.assertEqual(69,t.index)
        self.assertEqual('a',t.glyph)
        self.assertEqual(5,t.octave)
        self.assertEqual('a5',str(t))

    def testA220(self):
        t = Tone(69-TONES_PER_CHROMATIC_OCTAVE)
        self.assertEqual(220.0,t.frequency)
        self.assertEqual(57,t.index)
        self.assertEqual('a',t.glyph)
        self.assertEqual(4,t.octave)
        self.assertEqual('a4',str(t))

    def testC(self):
        t0 = Tone.fromGlypho('c')
        t1 = Tone.fromGlypho('C',5)
        self.assertEqual(t0,t1)
        t2 = Tone(60)
        self.assertEqual(t0,t2)

    def testCAgain(self):
        t0 = Tone('c')
        t1 = Tone('C',5)
        self.assertEqual(t0,t1)
        t2 = Tone(60)
        self.assertEqual(t0,t2)

    def testBadGlpyh(self):
        self.assertRaises(AssertionError,Tone, 'h')

    def testCmp(self):
        t0 = Tone.fromGlypho("A",4)
        t1 = Tone.fromGlypho("A#",4)
        self.failUnless(t0<t1)

    def testGlyphs(self):
        gstr = "c c+ d d+ e f f+ g g+ a a+ b".split()
        for i in range(12):
            self.assertEqual(Tone(i).glyph, gstr[i])

    def testSets(self):
        # XXX prove that you cannot set index/glyph/tone
        t0 = Tone(60)
        #XXX self.assertRaises(AttributeError, t0.index, 69)

if __name__ == "__main__":
    unittest.main()
