#!/usr/bin/env python
# scale_similarities - Given a scale, report the similarities to other scales,
# sorting by the most similar scales.
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
from ramu.music import *

def usage():
    print "scale_similarities.py scale [name]"
    sys.exit(1)

if len(sys.argv) < 2:
    usage()
base = sys.argv[1]
if len(sys.argv) == 3:
    name = sys.argv[2]
else:
    name = 'major'
    
s0 = Scale(Tone(base),name)
similarities = []
for i in range(12):
   s1 = Scale(Tone(base)+i,name)
   l = s0.intersect(s1)
   similarities.append((len(l),l,s1.tonic))

for s in reversed(sorted(similarities)):
   print "%2s %d %s" % (s[2],s[0],s[1])
    
