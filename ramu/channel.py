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
    def __init__(self):
        pass

    def note_on(self,time,tone,strength):
        print "note_on %f %d %f" % (time,tone.index,strength)

    def note_off(self,time,tone,strength):
        print "note_off %f %d %f" % (time,tone.index,strength)

    def note(self,seqnote):
        self.note_on(seqnote.time,
                     seqnote.tone.index,
                     seqnote.strength)
        self.note_off(seqnote.time + seqnote.duration,
                      seqnote.tone.index,
                      seqnote.strength)
