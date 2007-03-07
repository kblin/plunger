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
"""The Plunger Document Object Model, based on the Collada DOM
"""

model = None

def getModel():
    global model
    if not model:
        model = Model()
    return model

class PlungerNode:
    def __init__(self):
        self.parent = None
        self.children = []
        self.attributes = {}
        self.asset = None
        self.collada_xml = ""
        self.extra = None

    def getType(self):
        return self.__class__.__name__

    def getAssetInfo(self, attribute):
        if self.asset:
            return self.asset.getAttribute(attribute)
        else: return ""

    def getModel(self):
        return self.model

class Model:
    def __init__(self):
        self.meshes = None
        self.idmap = {}
        # Cheat and store the full collada xml text if available
        self.collada_xml = None

    def getType(self):
        return self.__class__.__name__

    def getNumMeshes(self):
        if self.meshes:
            return self.meshes.getNumMeshes()
        return 0

    def getMeshes(self):
        if self.meshes:
            return self.meshes.getMeshes()
        return []

    def registerId(self, id, node):
        self.idmap[id] = node

    def getNodeById(self, id):
        return self.idmap[id]

class Meshes(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.meshes = []

    def getNumMeshes(self):
        return len(self.meshes)

    def getMeshes(self):
        return self.meshes

class Mesh(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.faces = None
        self.vertices = None
        self.materials = None

    def getNumFaces(self):
        if self.faces:
            return self.faces.getNumFaces()
        return 0

    def getFaces(self):
        if self.faces:
            return self.faces.getFaces()
        return []

    def getNumVertices(self):
        if self.vertices:
            return self.vertices.getNumVertices()
        return 0

    def getVertices(self):
        if self.vertices:
            return self.vertices.getVertices()
        return []

    def getNumMaterials(self):
        if self.materials:
            return self.materials.getNumMaterials()
        return 0

    def getMaterials(self):
        if self.materials:
            return self.materials.getMaterials()
        return []

class Faces(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.faces = []

    def getNumFaces(self):
        return len(self.faces)

    def getFaces(self):
        faces = []
        for face in self.faces:
            faces.append(face.getFace())
        return faces

class Vertices(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.vertices = []

    def getNumVertices(self):
        return len(self.vertices)

    def getVertices(self):
        return self.vertices

class Materials(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.materials = []

    def getNumMaterials(self):
        return len(self.materials)

    def getMaterials(self):
        return self.materials

class Face(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.vertex_list = []

    def getFace(self):
        return self.vertex_list

class Vertex(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.position = []
        self.normals = []
        self.uv_coords = []

    def getPosition(self):
        return self.position

    def getNormals(self):
        return self.normals

    def getUVCoords(self):
        if self.uv_coords:
            return self.uv_coords

class Material(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.path = ""

    def getPath(self):
        return self.path

