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

    def testEqual(self):
        t0 = Chord(Scale(Tone('a'),'aeolian'),'7th')
        t1 = Chord(Scale(Tone('A'),'aeolian'),'7th')
        self.assertEqual(t0,t1)
        t2 = Chord(Scale(Tone('B'),'aeolian'),'7th')
        self.failUnless(t0 != t2)
        t3 = Chord(Scale(Tone('a'),'major'),'7th')
        self.failUnless(t0 != t3)
        t4 = Chord(Scale(Tone('a'),'aeolian'),'dim7th')
        self.failUnless(t0 != t4)
# XXX test multiple octaves
# XXX test assert <,<=,>,>=

# ======================================================================
class TestNote(unittest.TestCase):
    def testBasic(self):
        n = Note(Tone('c'),0.5,0.75)
        self.assertEqual(n.tone, Tone('c'))
        self.assertEqual(n.duration, 0.5)
        self.assertEqual(n.strength, 0.75)

    def testEqual(self):
        t0 = Note(Tone('c#'))
        t1 = Note(Tone('C+'))
        self.assertEqual(t0,t1)
        t2 = Note(Tone('c'))
        self.failUnless(t0 != t2)
        t3 = Note(Tone('c#'),1.0) # mismatch duration
        self.failUnless(t0 != t3)
        t4 = Note(Tone('c#'),0.25,1.0) # mismatch strength
        self.failUnless(t0 != t4)
# XXX test SeqNote
# XXX test assert <,<=,>,>=

# ======================================================================
class TestScale(unittest.TestCase):
    def testCMajorTones(self):
        tst = Scale(Tone('c'))
        ref = map(Tone.fromGlypho,"c d e f g a b".split())
        for (t,r) in zip(tst.tones,ref):
            self.assertEqual(t,r)        

    def testCMinorTones(self):
        tst = Scale(Tone('c'),"minor")
        ref = map(Tone.fromGlypho,"c d d+ f g g+ a+".split())
        for (t,r) in zip(tst.tones,ref):
            self.assertEqual(t,r)        

    def testEqual(self):
        t0 = Scale(Tone('a'),'major')
        t1 = Scale(Tone('A'),'major')
        self.assertEqual(t0,t1)
        self.failUnless(t0 == t1)
        t2 = Scale(Tone('b'),'major')
        self.failUnless(t0 != t2)
        t3 = Scale(Tone('a'),'minor')
        self.failUnless(t0 != t3)
# XXX multiple octaves
# XXX test assert <,<=,>,>=

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

    def testEqual(self):
        t0 = Tone('c')
        t1 = Tone('C',5)
        self.assertEqual(t0,t1)
        self.failUnless(t0 == t1)
        t2 = Tone(60)
        self.assertEqual(t0,t2)
        t3 = Tone(61)
        self.failUnless(t0 != t3)

    def testBadGlpyh(self):
        self.assertRaises(AssertionError,Tone, 'h')

    def testCmp(self):
        t0 = Tone.fromGlypho("A",4)
        t1 = Tone.fromGlypho("A#",4)
        self.failUnless(t0<t1)
# XXX test <,<=,>,>=

    def testGlyphs(self):
        gstr = "c c+ d d+ e f f+ g g+ a a+ b".split()
        for i in range(12):
            self.assertEqual(Tone(i).glyph, gstr[i])

    def testSets(self):
        # XXX prove that you cannot set index/glyph/tone
        t0 = Tone(60)
        # XXX on my mac, this doesn't seem to work as expected...
        # XXX self.assertRaises(AttributeError, t0.index, 69)

if __name__ == "__main__":
    unittest.main()
