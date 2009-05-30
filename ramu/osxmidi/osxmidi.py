#!/usr/bin/env python
#
# ramu.osxmidi - connect python to mac midi
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
import os
import math
from ctypes import *
from .. import channel

# ======================================================================
# hook up our library.  it's sitting right next to this file
pth = os.path.dirname(__file__)
lm = cdll.LoadLibrary(pth+'/libosxmidi.dylib')
# experimented with the setup.py way of doing things & this failed.
#lm = cdll.LoadLibrary(pth+'/libosxmidi.so')
# create our prototypes
#   now()
lm.now.restype = c_ulonglong
now = lm.now
#   send_midi_event()
prototype = CFUNCTYPE(c_void_p,c_ulonglong,c_ubyte,c_ubyte,c_ubyte,c_ubyte)
paramflags = (1,"time",0), (1,"note",0), (1,"channel",0), (1,"data0",0), (1,"data1",0)
send_midi_event = prototype(("send_midi_event",lm),paramflags)

# ======================================================================
# constants of interest
one_s = 1000000000L
# http://www.onicos.com/staff/iz/formats/midi-event.html
MIDI_NOTE_OFF = 0x80
MIDI_NOTE_ON = 0x90
MIDI_POLY_AFTERTOUCH = 0xa0
MIDI_CONTROL_MODE = 0xa0
MIDI_PROGRAM = 0xc0
MIDI_CHANNEL_AFTERTOUCH = 0xd0
MIDI_PITCH_WHEEL = 0xe0
MIDI_SYSTEM_EXCLUSIVE = 0xf0
# http://www.onicos.com/staff/iz/formats/midi-cntl.html
MIDI_CONTROL_ALL_NOTES_OFF = 0x7b

# ======================================================================
class MidiChannel(channel.Channel):
    def __init__(self,midi_channel_id=0,rhythm=None):
        #super(MidiChannel,self).__init__(rhythm)
        channel.Channel.__init__(self,rhythm)
        self._midi_channel_id = midi_channel_id
        #self.default_strength = default_strength
        self.one_second = one_s
        self.ulp = 1L

    def note_on(self,time,tone,strength):
        #if strength == None:
        #    strength = self.default_strength
        channel.Channel.note_on(self,time,tone,strength)
        assert(0.0<=strength<=1.0)
        velocity = int(127*strength)
        send_midi_event(time,MIDI_NOTE_ON,self._midi_channel_id,tone.index,velocity)
    def note_off(self,time,tone,strength):
        #if strength == None:
        #    strength = self.default_strength
        assert(0.0<=strength<=1.0)
        velocity = int(127*strength)
        send_midi_event(time,MIDI_NOTE_OFF,self._midi_channel_id,tone.index,velocity)
    def note(self,seqnote):
        self.note_on(long(self.beat_to_time(seqnote.beat)),
                     seqnote.tone,
                     seqnote.strength)
        self.note_off(long(self.beat_to_time(seqnote.beat + seqnote.duration)),
                      seqnote.tone,
                      seqnote.strength)
        
    def get_now(self):
        return now()
    now = property(get_now)
        
# ======================================================================
# XXX part of channel?
def all_notes_off():
    send_midi_event(now(),MIDI_CONTROL_MODE,0,MIDI_CONTROL_ALL_NOTES_OFF,0)

# cause initialization
all_notes_off()
