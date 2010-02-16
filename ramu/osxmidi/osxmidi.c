/*
 *  osxmidi.c - library for python interaction with midi on the mac
 *
 *  Public Interface is just:
 *    send_midi_event(UInt64 time, Byte event, Byte channel, 
 *                    Byte data0, Byte data1)
 *      Calling this sends the event over a virtual midi device.  It 
 *      initializes a virtual midi device if necessary.
 *    now()
 *      Calling this returns the current time in ns.  
 *      Divide by 1e9 to get seconds.
 *
 * Copyright (C) 2009 Roger Allen (rallen@gmail.com)
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  
 * 02110-1301, USA.
 * 
 */
#include <stdio.h>
#include <CoreMIDI/MIDIServices.h>
#include <CoreAudio/HostTime.h>

//#define DEBUG

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// prototypes
void   _init();                                   // "private"
void   _send(Byte* data, int count, UInt64 time); // "private"
void   send_midi_event(UInt64 time, Byte event, Byte channel, Byte data0, Byte data1);
UInt64 now();

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void 
_init(MIDIEndpointRef *endpoint) {
    // create client and midi ports                                             
    MIDIClientRef midi_client = (MIDIClientRef)(uintptr_t)NULL;
    MIDIClientCreate( CFSTR( "osxmidi" ), NULL, NULL, &midi_client );
    MIDISourceCreate( midi_client, CFSTR("osxmidi output port"), endpoint );
}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void 
_send(Byte* data, int count, UInt64 time) {
    static MIDIEndpointRef endpoint = (MIDIClientRef)(uintptr_t)NULL;
    if(endpoint == (MIDIClientRef)(uintptr_t)NULL) {
        _init(&endpoint);
    }
    Byte buffer[64];  // not quite sure how big this should be, but this works
    MIDIPacketList *packet_list = (MIDIPacketList *)buffer;
    MIDIPacket     *packet      = MIDIPacketListInit(packet_list);
    packet = MIDIPacketListAdd(packet_list, sizeof(buffer), packet,
                               time, count, data);
    // "received" is really "send".
    MIDIReceived( endpoint, packet_list );
}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void 
send_midi_event(UInt64 time, Byte event, Byte channel, Byte data0, Byte data1) {
#ifdef DEBUG
    fprintf(stdout, "midi_event %lld %d %d %d %d\n", 
            time, event, channel, data0, data1);
#endif
    if(channel >= 0xf) {
        fprintf(stderr, "channel (%d) must be less than 16. Dropped\n", 
                channel);
        return;
    }
    Byte data[] = { event | channel, data0, data1 };
    _send(data, sizeof(data), time);        
}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// return the current time in nanoseconds. 
UInt64 
now() {
    return AudioConvertHostTimeToNanos(AudioGetCurrentHostTime());
}

