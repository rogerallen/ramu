#/usr/bin/env python
from distutils.core import setup
from distutils.extension import Extension

# diy!
import os
os.system("cd ramu/osxmidi; make")

setup(name='ramu',
      version='0.1',
      description='python music library',
      author='Roger Allen',
      author_email='rallen@gmail.com',
      url='http://ramu.googlecode.com/',
      classifiers=[ 'Development Status :: 5 - Alpha',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Musicians',
                    'License :: GPLv2',
                    'Operating System :: MacOS X',
                    'Operating System :: POSIX',
                    'Programming Language :: Python',
                    'Topic :: Computer Music',
                    ],
      platforms=['MacOS X', 'POSIX'],
      packages=['ramu',
                'ramu.instruments',
                'ramu.osxmidi'],
      package_data={ 'ramu.osxmidi': ['libosxmidi.dylib']},
# I want a dylib & this makes a .so
#        ext_modules=[Extension('ramu.osxmidi.libosxmidi',
#                              ['ramu/osxmidi/osxmidi.c'],
#                              extra_link_args=['-framework CoreMIDI',
#                                               '-framework CoreAudio',
#                                               '-framework CoreFoundation'])],
      )
