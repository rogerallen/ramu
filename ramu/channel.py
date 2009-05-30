# ramu.channel
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

# a simple-stupid way to see notes. Override for actual use
class Channel:
    def __init__(self,rhythm=None):
        self._now = 0.0
        self.one_second = 1.0
        self.ulp = 1/1000.0 # tiny number
        self.set_rhythm(rhythm)

    def set_rhythm(self,rhythm):
        self._rhythm = rhythm
        self._rhythm_start_time = self.now  

    def beat_to_time(self,beat):
        return self._rhythm_start_time + self.one_second*beat/self._rhythm.beats_per_second

    def note_on(self,time,tone,strength):
        print "%f note_on %d %f" % (time,tone.index,strength)
        self._now = time

    def note_off(self,time,tone,strength):
        print "%f note_off %d %f" % (time,tone.index,strength)
        self._now = time

    def note(self,seqnote):
        self._now = self.beat_to_time(seqnote.beat)
        print "%f(%f) note %d %f %f" % (self._now,
                                        seqnote.beat,
                                        seqnote.tone.index,
                                        seqnote.strength,
                                        seqnote.duration)
        self._now += self.beat_to_time(seqnote.beat + seqnote.duration)

    def get_now(self):
        return self._now
    now = property(get_now)

