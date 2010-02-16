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
# I confirmed that this works
# MYARCH=-arch i386
# as long as you also call python with VERSIONER_PYTHON_PREFER_32_BIT=yes set
THE_ARCH=-arch x86_64
libosxmidi.dylib: osxmidi.c
	gcc ${THE_ARCH} -fPIC -c osxmidi.c
	ld ${THE_ARCH} -dylib -o libosxmidi.dylib \
	  -framework CoreMIDI -framework CoreAudio -framework CoreFoundation \
	  -lc osxmidi.o

# here is what distutils does.  it creates a .so instead of a .dylib
# and this just fails when it is put in the distribution subdirectory.  Why?
# ...
#    self._handle = _dlopen(self._name, mode)
#OSError: dlopen(/Users/rallen/lib/python/ramu/osxmidi/libosxmidi.so, 6): Symbol not found: ___CFConstantStringClassReference
#  Referenced from: /Users/rallen/lib/python/ramu/osxmidi/libosxmidi.so
#  Expected in: dynamic lookup
libosxmidi.so: osxmidi.c
	gcc -fno-strict-aliasing -Wno-long-double -no-cpp-precomp -mno-fused-madd -fno-common -dynamic -DNDEBUG -g -Os -Wall -Wstrict-prototypes -DMACOSX -I/usr/include/ffi -DENABLE_DTRACE -arch i386 -arch ppc -pipe -I/System/Library/Frameworks/Python.framework/Versions/2.5/include/python2.5 -c osxmidi.c -o osxmidi.o
	gcc -Wl,-F. -bundle -undefined dynamic_lookup -arch i386 -arch ppc ./osxmidi.o -o libosxmidi.so -framework CoreMIDI -framework CoreAudio -framework CoreFoundation

clean:
	rm -f *.dylib *.o *.so *.pyc
