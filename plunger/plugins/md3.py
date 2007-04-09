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
import struct

try:
    from plunger import toolbox
except ImportError:
    import sys
    sys.path.append('..')
    import toolbox
    sys.path.pop()

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

class Md3Frame:
    def __init__(self):
        self.min_bounds = [0,0,0]
        self.max_bounds = [0,0,0]
        self.local_origin = [0,0,0]
        self.radius = 0.0
        self.name = ""
        self.fmt = "fff fff fff f 8s"

    def packSize(self):
        return struct.calcsize(self.fmt)

    def pack(self):
        pack_str = ""
        pack_str += struct.pack("fff", self.min_bounds.split())
        pack_str += struct.pack("fff", self.max_bounds.split())
        pack_str += struct.pack("fff", self.local_origin.split())
        pack_str += struct.pack("f", self.radius)
        pack_str += struct.pack("8s", self.name)
        return pack_str

class Md3Tag:
    def __init__(self):
        self.name = ""
        self.origin = [0,0,0]
        self.axis = [[1,0,0], [0,1,0], [0,0,1]]
        self.fmt = "64s fff fff fff fff"

    def packSize(self):
        return struct.calcsize(self.fmt)

    def pack(self):
        pack_str = ""
        pack_str += struct.pack("64s", self.name)
        pack_str += struct.pack("fff", self.origin.split())
        for row in self.axis:
            pack_str += struct.pack("fff", row.split())
        return pack_str

class Md3Shader:
    def __init__(self):
        self.name = ""
        self.index = 0
        self.fmt = "64s i"

    def packSize(self):
        return struct.calcsize(self.fmt)

    def pack(self):
        pack_str = ""
        pack_str += struct.pack("64s", self.name)
        pack_str += struct.pack("i", self.index)

class Md3Triangle:
    def __init__(self):
        self.indices = [0,0,0]
        self.fmt = "iii"

    def packSize(self):
        return struct.calcsize(self.fmt)

    def pack(self):
        return struct.pack("iii", self.indices.split())

class Md3TexCoord:
    def __init__(self):
        self.uv_coords = [0,0]
        self.fmt = "ff"

    def packSize(self):
        return struct.calcsize(self.fmt)

    def pack(self):
        return struct.pack(self.fmt, self.uv_coords.split())

class Md3Vertex:
    def __init__(self):
        self.coord = [0,0,0]
        self.normal = [0,0]
        self.factor = 1.0 / 64
        self.fmt = "hhh BB"

    def packSize(self):
        return struct.calcsize(self.fmt)

    def pack(self):
        pack_str = ""
        pack_str += struct.pack("hhh", self.coord.split())
        pack_str += struct.pack("BB", self.normal.split())
        return pack_str

    def scaleDown(self, coords):
        return [i * self.factor for i in coords]

class Md3Surface:
    def __init__(self):
        self.ident = MD3_IDENT
        self.name = ""
        self.num_frames = 0
        self.num_shaders = 0
        self.num_verts = 0
        self.num_triangles = 0
        self.shaders = []
        self.triangles = []
        self.uv_coords = []
        self.vertices = []
        self.fmt = "4s 68s iiiiiiiii"

    def packSize(self):
        size = struct.calcsize(self.fmt) 
        size += len(self.shaders) * Md3Shader().packSize()
        size += len(self.triangles) * Md3Triangle().packSize()
        size += len(self.uv_coords) * Md3TexCoord().packSize()
        size += len(self.vertices) * Md3Vertex().packSize()
        return size

    def pack(self):
        pack_str = ""
        pack_str += struct.pack("4s", self.ident)
        pack_str += struct.pack("68s", self.name)
        pack_str += struct.pack("ii", self.num_frames, self.num_shaders)
        pack_str += struct.pack("ii", self.num_verts, self.num_triangles)
        ofs_shaders = struct.calcsize(self.fmt)
        ofs_triangles = ofs_shaders + len(self.shaders) * Md3Shader().packSize()
        ofs_uv_coords = ofs_triangles + len(self.triangles) * Md3Triangle().packSize()
        ofs_vertices = ofs_uv_coords + len(self.uv_coords) * Md3TexCoord().packSize()
        ofs_end = ofs_vertices + len(self.vertices) * Md3Vertex().packSize()
        pack_str += struct.pack("ii", ofs_triangles, ofs_shaders)
        pack_str += struct.pack("iii", ofs_uv_coords, ofs_vertices, ofs_end)
        for shader in self.shaders:
            pack_str += shader.pack()
        for tri in self.triangles:
            pack_str += tri.pack()
        for texcoord in self.uv_coords:
            pack_str += texcoord.pack()
        for vert in self.vertices:
            pack_str += vert.pack()

class MD3Object:
    def __init__(self):
        self.ident = MD3_IDENT
        self.version = MD3_VERSION
        self.name = ""
        self.num_frames = 0
        self.num_tags = 0
        self.num_surfaces = 0
        self.num_skins = 0
        self.frames = []
        self.tags = []
        self.surfaces = []

    def pack(self):
        pack_str = ""
        fmt = "4si68siiiiiiii"
        pack_str += struct.pack("4s", self.ident)
        pack_str += struct.pack("i", self.version)
        pack_str += struct.pack("68s", self.name)
        pack_str += struct.pack("i", self.num_frames)
        pack_str += struct.pack("i", self.num_tags)
        pack_str += struct.pack("i", self.num_surfaces)
        pack_str += struct.pack("i", self.num_skins)
        ofs_frames = struct.calcsize(fmt)
        ofs_tags = ofs_frames + len(self.frames) * Md3Frame().packSize()
        ofs_surfaces = ofs_tags + len(self.tags) * Md3Tag().packSize()
        ofs_eof = ofs_surfaces + len(self.surfaces) * Md3Surface().packSize()
        pack_str += struct.pack("i", ofs_frames)
        pack_str += struct.pack("i", ofs_tags)
        pack_str += struct.pack("i", ofs_surfaces)
        pack_str += struct.pack("i", ofs_eof)
        for frame in self.frames:
            pack_str += frame.pack()
        for tag in self.tags:
            pack_str += tag.pack()
        for surface in self.surfaces:
            pack_str += surface.pack()
        return pack_str

def importAsset(model, asset):
    raise NotImplementedError

def exportAsset(model, asset):
    out = toolbox.writeAny(asset)
    md3_object = MD3Object()
    meshes = model.getMeshes()
    #TODO: Put stuff into the MD3Object here()
    out.write(md3_object.pack())
    out.close()

def encodeNormal(x,y,z):
    """Returns (azimuth, zenith) angles of the normal vector
    """
    azimuth = math.atan2(y, x) * 255 / (2 * math.pi)
    zenith = math.acos(z) * 255 / (2 * math.pi)
    return (azimuth, zenith)
