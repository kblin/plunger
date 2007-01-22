#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 by Kai Blin
#
# Plunger is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
"""The plunger file handler for the MD3 format.

The module supports export only for now.
"""

import math

format = "md3"
extension = ".md3"
needs_dir = False
does_export = True
does_import = False

# Info from http://icculus.org/homepages/phaethon/q3a/formats/md3format.html
# Augmented by the libmodelfile headers by Alistair Riddoch, as the specfile
# is kind of inaccurate.
MD3_IDENT = "IDP3"
MD3_VERSION = 15
MD3_MAX_FRAMES = 1024
MD3_MAX_TAGS = 16
MD3_MAX_SURFACES = 32
MD3_MAX_SHADERS = 256
MD3_MAX_VERTS = 4096
MD3_MAX_TRIANGLES = 8192

def importAsset(model, asset):
    raise NotImplementedError

def exportAsset(model, asset):
    print "Not yet implemented, sorry."

def generateMd3File(model):
    pass

def generateMd3Header(model):
    pass

def generateFrames(model):
    pass

def generateTags(model):
    pass

def generateSurfaces(model):
    pass

def generateShader(model):
    pass

def generateTriangles(model):
    pass

def generateTexCoords(model):
    pass

def generateVertices(model):
    pass

def encodeNormal(x,y,z):
    """Returns (azimuth, zenith) angles of the normal vector
    """
    azimuth = math.atan2(y, x) * 255 / (2 * math.pi)
    zenith = math.acos(z) * 255 / (2 * math.pi)
    return (azimuth, zenith)
