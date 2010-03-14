# ramu.channel
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
ramu.channel contains the Channel class.  This module is intended
for diagnostic usage when a real channel is not available.
"""

class Channel:
    """Channel is a container that takes in tones and timing
    information and produces output.  Normally, it would produce
    musical output via a MIDI channel or synthesizer.  In this case it
    is just a simple-stupid way to see notes printed to stdout.
    Normally, you would override for actual use.
    """
    def __init__(self):
        """Create the channel and initialize the values of
        Channel.one_second and Channel.ulp.

        Channel.now -- a value that is updated whenever a time value
        is passed into the class.  Normally it would continuously
        update to be the current time.

        Channel._one_second -- a conversion helps convert
        floating-point time where 1 second === 1.0 to the channel's
        preferred accounting.

        Channel._ulp -- unit-of-least-precision.  Any times smaller
        than that value are 'too small to be measured'.
        """
        self._now = 0.0
        self._one_second = 1.0
        self._ulp = 1/1000.0 # tiny number

    def start_note(self,time,tone,strength):
        """Start playing a note.

        Keyword arguments:
        time     -- time to start playing in seconds.  1.0 === 1 second
        tone     -- the tone to play
        strength -- strength to apply to playing the note [0.0,1.0]
        """
        assert(0.0<=strength<=1.0)
        localtime = float(time*self._one_second)
        print "%f start_note %d %f" % (localtime,tone.index,strength)
        self._now = time

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
        localtime = float(time*self._one_second) - self._ulp
        print "%f stop_note  %d %f" % (localtime,tone.index,strength)
        self._now = time

    def play_note(self,start,stop,tone,strength):
        """Play a note.

        Keyword arguments:
        start    -- time to start playing in seconds.  1.0 === 1 second
        stop     -- time to stop playing in seconds. 1.0 === 1 second
        tone     -- the tone to play
        strength -- strength to apply to playing the note [0.0,1.0]
        """
        self.start_note(start,tone,strength)
        self.stop_note(stop,tone,strength)

    def get_now(self):
        """return current time. Normally you should use the now property"""
        return self._now
    now = property(get_now)

    def all_notes_off(self):
        """turn off all notes"""
        pass # NOP in this channel

    # ======================================================================
    # allow the with statement
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        return False
