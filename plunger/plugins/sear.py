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
"""The plunger file handler for Sear's static object format.

The module supports export only for now.
"""

import sys
import struct

try:
    from plunger import toolbox
except ImportError:
    sys.path.append("..")
    import toolbox
    sys.path.pop()

format = "sear"
ext = ""
needs_dir = False
does_import = False
does_export = True
version = "1"

class SearObjectHeader:
    def __init__(self):
        self.magic = 'SEARSTAT'
        self.byte_order = 0xFF00
        self.version = 1
        self.num_meshes = 0

    def pack(self):
        return struct.pack("8sHBI", self.magic, self.byte_order, self.version,
                self.num_meshes)

class SearObjectMesh:
    def __init__(self):
        self.mesh_transform = []
        self.texture_transform = []
        self.texture_map = ""
        self.num_vertices = 0
        self.num_faces = 0
        self.ambient = []
        self.diffuse = []
        self.specular = []
        self.emissive = []
        self.shininess
        self.vertices = []
        self.normals = []
        self.texture_coords = []
        self.indices = []

    def pack(self):
        pack_str = ""
        for row in self.mesh_transform:
            for item in row:
                pack_str += struct.pack("B", item)
        for row in self.texture_transform:
            for item in row:
                pack_str += struct.pack("B", item)
        pack_str += struct.pack("265s", self.texture_map)
        pack_str += struct.pack("II", self.num_vertices, self.num_faces)
        pack_str += struct.pack("ffff", self.ambient[0], self.ambient[1],
                self.ambient[2], self.ambient[3])
        pack_str += struct.pack("ffff", self.diffuse[0], self.diffuse[1],
                self.diffuse[2], self.diffuse[3])
        pack_str += struct.pack("ffff", self.specular[0], self.specular[1],
                self.specular[2], self.specular[3])
        pack_str += struct.pack("ffff", self.emissive[0], self.emissive[1],
                self.emissive[2], self.emissive[3])
        pack_str += struct.pack("f", self.shininess)
        for vertex in self.vertices:
            pack_str += struct.pack("f", vertex)
        for normal in self.normals:
            pack_str += struct.pack("f", normal)
        for coord in self.texture_coords:
            pack_str += struct.pack("f", coord)
        for index in self.indices:
            pack_str += struct.pack("I", index)

        return pack_str

class SearObject:
    def __init__(self):
        self.header = SearObjectHeader()
        self.meshes = []

    def pack(self):
        pack_str = ""
        pack_str += self.header.pack()
        for mesh in self.meshes:
            pack_str += mesh.pack()
        return pack_str

def importAsset(model, asset):
    raise NotImplementedError

def exportAsset(model, asset):
    out = toolbox.writeAny(asset)
    sear_object = SearObject()
    sear_object.header.num_meshes = model.getNumMeshes()
    # do more stuff below
    meshes = model.getMeshes()
    for mesh in meshes:
        sear_mesh = SearObjectMesh()
    out.close()
