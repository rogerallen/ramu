#!/usr/bin/env python
#
# ramu.osxmidi.channel - connect python to mac midi
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
ramu.osxmidi.channel contains the Channel class and other midi
information for use as a virtual midi channel on an Mac OS X machine.

ramu.osxmidi.channel.now() -- returns a long integer of the current
time in nanoseconds.

ramu.osxmidi.send_midi_event() -- sends a midi event onto the virtual channel.
  time       -- long time to send event in nanoseconds
  event      -- byte event type
  channel_id -- byte midi channel id
  event1     -- byte additional midi event info
  event2     -- byte additional midi event info

"""
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
class Channel(channel.Channel):
    """Channel is a container that takes in tones and timing
    information and produces output on a Mac OS X virtual midi interface.
    """
    def __init__(self,midi_channel_id=0):
        """Initialize the Channel by sending an innocuous event.
        """
        #super(MidiChannel,self).__init__(rhythm) XXX
        channel.Channel.__init__(self)
        self._midi_channel_id = midi_channel_id
        self._one_second       = one_s
        self._ulp              = 1L
        send_midi_event(now(),
                        MIDI_NOTE_OFF,
                        self._midi_channel_id,
                        0,
                        0)

    def start_note(self,time,tone,strength):
        """Start playing a note.

        Keyword arguments:
        time     -- time to start playing in seconds.  1.0 === 1 second
        tone     -- the tone to play
        strength -- strength to apply to playing the note [0.0,1.0]
        """
        assert(0.0<=strength<=1.0)
        velocity = int(127*strength)
        localtime = long(time * self._one_second)
        print "%d start_note %d %f" % (localtime,tone.index,strength)
        send_midi_event(localtime,
                        MIDI_NOTE_ON,
                        self._midi_channel_id,
                        tone.index,
                        velocity)

    def stop_note(self,time,tone,strength):
        """Stop playing a note.

        Keyword arguments:
        time     -- time to stop playing in seconds.  1.0 === 1 second
                    this time is reduced 1 ulp to keep it clear when
                    a note ends and when another begins in the channel.
        tone     -- the tone to play
        strength -- strength to apply to stopping the note [0.0,1.0]
        """
        assert(0.0<=strength<=1.0)
        velocity = int(127*strength)
        localtime = long(time*self._one_second) - self._ulp
        print "%d stop_note  %d %f" % (localtime,tone.index,strength)
        send_midi_event(localtime,
                        MIDI_NOTE_OFF,
                        self._midi_channel_id,
                        tone.index,
                        velocity)

    def get_now(self):
        """return the current time where 1.0 == 1 second"""
        return float(now()*1.0/self._one_second)
    now = property(get_now)
        
    def all_notes_off(self):
        """turn off all notes"""
        send_midi_event(now(),MIDI_CONTROL_MODE,0,MIDI_CONTROL_ALL_NOTES_OFF,0)
