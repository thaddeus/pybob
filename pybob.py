#!/usr/bin/env python
#
# pybob - Python client library for boblightd
# 
# Copyright (c) 2013, Raphael Michel. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301  USA

import socket

class Boblights:
    """Interface for accessing a boblight server"""

    priority = 128
    socket = None
    server = '127.0.0.1'
    port = 19333
    lights = []

    def __init__(self, server = server, port = port):
        """Initialize a new interface"""
        self.server = server
        self.port = port

    def open(self):
        """Opens up a new connection"""
        if self.socket is not None:
            raise ValueError("Socket is open or was not properly closed")
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server, self.port))
            self.socket.send(b"hello\n")
            answer = self.socket.recv(256)
            if not answer.decode().find("hello") >= 0:
                raise IOException("%s:%d is not a boblightd server or does not respond" % (server, port))
            self.set_priority()
            self._read_lights()

    def _read_lights(self):
        """Retrieves a list of lights from the server. In theory, this should only be called at the start of your program."""
        self.socket.send(b"get lights\n")
        lines = []
        lines.append("")
        while True:
            c = self.socket.recv(1).decode()
            if c == "\n" or c == "":
                if len(lines) == 1:
                    split = lines[-1].split(" ")
                    linenum = int(split[1].strip())
                    lines.append("")
                else:
                    if len(lines)-1 >= linenum:
                        break
                    else:
                        lines.append("")
                continue
            lines[-1] += c
        lines = lines[1:]
        for line in lines:
            split = line.split(" ")
            assert split[0] == "light"
            self.lights.append(split[1])

    def set_priority(self, priority = priority):
        """Sets the priority. Lower is more important, default is 128."""
        self.priority = priority
        self.socket.send(("set priority %d\n" % priority).encode())

    def get_lights(self):
        """Return list of defined light names"""
        return self.lights

    def close(self):
        """Close the connection"""
        self.socket.close()
        self.socket = None

    def set_light(self, light, color='FFFFFF'):
        """Set a light to a color. This is the function you are looking for."""
        if light not in self.lights:
            raise ValueError("Light %s is not registered" % light)
        
        rgb_decimal = self.get_color_string(color, value)

        self.socket.send(("set light %s rgb %s\n" % (light, rgb_decimal)).encode())

    def set_lights(self, color='FFFFFF', value=1.0):
        """Set all lights reported by the server to a specified value."""
        rgb_decimal = self.get_color_string(color, value)
        data = ""
        for light in self.lights:
            data += ("set light %s rgb %s\n" % (light, rgb_decimal))

        self.socket.send(data.encode())

    def set_use(self, light, use):
        """Set the controller to use (or not to) this light for this client. Useful for overlapping patterns."""
        if light not in self.lights:
            raise ValueError("Light %s is not registered" % light)

        if use != "true" and use != "false":
            raise ValueError("Use value is not valid")

        self.socket.send(("set light %s use %s\n" % (light, use)).encode())
    
    def set_speed(self, light, speed):
        """Set the speed at which a light changes to a new color."""
        if light not in self.lights:
            raise ValueError("Light %s is not registered" % light)

        self.socket.send(("set light %s speed %s\n" % (light, speed)).encode())

    def sync(self):
        """Sync settings to the device. This is also a function you are looking for."""
        self.socket.send(b"sync\n")

    def get_color_string(self, color='FFFFFF', value=1.0):
        """Helper function to calculate RGB values from Hex"""
        return str(float(int(color[0:2], 16))/255*value)+' '+str(float(int(color[2:4], 16))/255*value)+' '+str(float(int(color[4:6], 16))/255*value)
