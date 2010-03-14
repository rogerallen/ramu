#!/usr/bin/env python
#
# Copyright (C) 2010 Roger Allen (rallen@gmail.com)
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
sys.path.insert(0,"../../examples")
sys.path.insert(0,"../..")

import circle_of_fifths
circle_of_fifths.main()

import guitar_chords
guitar_chords.main(['guitar_chords.py','stdout'])

import scale
scale.main(['scale.py','stdout'])

import scale_similarities
scale_similarities.main(['scale_similarities.py','a','minor'])

import twinkle
twinkle.main(['twinkle.py','stdout'])

