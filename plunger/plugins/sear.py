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

The module supports export and import.
"""

import sys
import struct

try:
    from plunger import toolbox
    from plunger import dom
except ImportError:
    sys.path.append("..")
    import toolbox
    import dom
    sys.path.pop()

format = "sear"
ext = ".sobj"
needs_dir = False
does_import = True
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

    def unpack(self, data, offset=0):
        fmt_string = "8sHBI"
        fmt_string_size = struct.calcsize(fmt_string)
        (self.magic, self.byte_order, self.version, self.num_meshes) =\
            struct.unpack(fmt_string, data[:fmt_string_size])
        return offset + fmt_string_size

class SearObjectMesh:
    def __init__(self):
        self.mesh_transform = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
        self.texture_transform = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
        self.texture_map = "default_texture"
        self.num_vertices = 0
        self.num_faces = 0
        self.ambient = [0,0,0,1]
        self.diffuse = [0,0,0,1]
        self.specular = [0,0,0,1]
        self.emissive = [0,0,0,1]
        self.shininess = 1
        self.vertices = []
        self.normals = []
        self.texture_coords = []
        self.indices = []

    def pack(self):
        pack_str = ""
        for row in self.mesh_transform:
            for item in row:
                pack_str += struct.pack("f", item)
        for row in self.texture_transform:
            for item in row:
                pack_str += struct.pack("f", item)
        pack_str += struct.pack("256s", self.texture_map)
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
            pack_str += struct.pack("fff", vertex[0], vertex[1], vertex[2])
        for normal in self.normals:
            pack_str += struct.pack("fff", normal[0], normal[1], normal[2])
        for coord in self.texture_coords:
            pack_str += struct.pack("ff", coord[0], coord[1])
        for index in self.indices:
            pack_str += struct.pack("III", index[0], index[1], index[2])

        return pack_str

    def unpack(self, data, offset=0):
        fmt = "ffff ffff ffff ffff"
        fmt_size = struct.calcsize(fmt)

        trans = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
        self.mesh_transform = [trans[:4],trans[4:8],trans[8:12],trans[12:]]
        offset += fmt_size

        trans = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
        self.texture_transform = [trans[:4],trans[4:8],trans[8:12],trans[12:]]
        offset += fmt_size

        fmt = "256s"
        fmt_size = struct.calcsize(fmt)
        self.texture_map =\
            struct.unpack(fmt,data[offset:offset+fmt_size])[0].replace('\0', '')
        offset += fmt_size

        fmt = "I I"
        fmt_size = struct.calcsize(fmt)
        (self.num_vertices, self.num_faces) = struct.unpack(fmt,\
            data[offset:offset+fmt_size])
        offset += fmt_size

        fmt = "ffff"
        fmt_size = struct.calcsize(fmt)

        self.ambient = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
        offset += fmt_size

        self.diffuse = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
        offset += fmt_size

        self.specular = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
        offset += fmt_size

        self.emissive = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
        offset += fmt_size

        fmt = "f"
        fmt_size = struct.calcsize(fmt)
        self.shinyness = struct.unpack(fmt, data[offset:offset+fmt_size])
        offset += fmt_size

        fmt = "fff"
        fmt_size = struct.calcsize(fmt)
        for i in range(self.num_vertices):
            vertex = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
            offset += fmt_size
            self.vertices.append(vertex)

        for i in range(self.num_vertices):
            normal = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
            offset += fmt_size
            self.normals.append(normal)

        fmt = "ff"
        fmt_size = struct.calcsize(fmt)

        for i in range(self.num_vertices):
            texcoord = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
            offset += fmt_size
            self.texture_coords.append(texcoord)

        fmt = "III"
        fmt_size = struct.calcsize(fmt)

        for i in range(self.num_faces):
            face = list(struct.unpack(fmt, data[offset:offset+fmt_size]))
            offset += fmt_size
            self.indices.append(face)

        return offset

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

    def unpack(self, data):
        self.header = SearObjectHeader()
        offset = 0
        offset = self.header.unpack(data, offset)
        while offset < len(data):
            mesh = SearObjectMesh()
            offset = mesh.unpack(data, offset)
            self.meshes.append(mesh)

def importAsset(model, asset):
    sock = toolbox.openAny(asset)
    data = sock.read()
    sock.close()

    sear_object = SearObject()
    sear_object.unpack(data)
    #FIXME: put data from sear object into the DOM
    # also, I'm just handling little endian encoded

    model.meshes = dom.Meshes()
    for sear_mesh in sear_object.meshes:
        mesh = dom.Mesh()
        mesh.parent = model.meshes
        model.meshes.meshes.append(mesh)
        mesh.materials = dom.Materials()
        mesh.materials.parent = mesh
        material = dom.Material()
        material.parent = mesh.materials
        mesh.materials.materials.append(material)
        material.path = sear_mesh.texture_map

        mesh.vertices = dom.Vertices()
        mesh.vertices.parent = mesh

        i = 0
        for sear_vertex in sear_mesh.vertices:
            vertex = dom.Vertex()
            vertex.parent = mesh.vertices
            mesh.vertices.vertices.append(vertex)
            vertex.position = sear_vertex
            vertex.normals = sear_mesh.normals[i]
            vertex.uv_coords = sear_mesh.texture_coords[i]
            i+=1

        mesh.faces = dom.Faces()
        mesh.faces.parent = mesh

        for sear_face in sear_mesh.indices:
            face = dom.Face()
            face.parent = mesh.faces
            mesh.faces.faces.append(face)
            face.vertex_list = sear_face

def exportAsset(model, asset):
    out = toolbox.writeAny(asset)
    sear_object = SearObject()
    sear_object.header.num_meshes = model.getNumMeshes()
    meshes = model.getMeshes()

    for mesh in meshes:
        sear_mesh = SearObjectMesh()
        if mesh.getMaterials():
            sear_mesh.texture_map = mesh.getMaterials()[0].getPath()
        sear_mesh.num_vertices = mesh.getNumVertices()
        for vertex in mesh.getVertices():
            sear_mesh.vertices.append(vertex.getPosition())
            sear_mesh.normals.append(vertex.getNormals())
            tex_coords = vertex.getUVCoords()
            sear_mesh.texture_coords.append(tex_coords and tex_coords or [0,0])
        sear_mesh.num_faces = mesh.getNumFaces()
        sear_mesh.indices = mesh.getFaces()
        sear_object.meshes.append(sear_mesh)

    out.write(sear_object.pack())
    out.close()
