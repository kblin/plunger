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
        self.model_tree_root = None
        self.idmap = {}

    def getType(self):
        return self.__class__.__name__

    def getRoot(self):
        return self.model_tree_root

    def getNumMeshes(self):
        if self.model_tree_root and self.model_tree_root.geometries:
            lg = self.model_tree_root.geometries
            return lg.getNumMeshes()
        return 0

    def getMeshes(self):
        if self.model_tree_root and self.model_tree_root.geometries:
            lg = self.model_tree_root.geometries
            return lg.getMeshes()
        return []

    def registerId(self, id, node):
        self.idmap[id] = node

    def getNodeById(self, id):
        return self.idmap[id]

def getModel():
    global model
    if not model:
        model = Model()
    return model

class COLLADA(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.version = "0.0.0"
        self.xmlns = None
        self.base = None
        self.animations = None
        self.clips = None
        self.cameras = None
        self.controllers = None
        self.effects = None
        self.extras = None
        self.force_fields = None
        self.geometries = None
        self.images = None
        self.lights = None
        self.materials = None
        self.nodes = None
        self.physics_materials = None
        self.physics_models = None
        self.physics_scenes = None
        self.visual_scenes = None
        self.scene = None

class Accessor(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.params = []
        self.count = 0
        self.offset = 0
        self.source = ""
        self.stride = 1

class Asset(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.contributor = None
        self.created = ""
        self.keywords = []
        self.modified = ""
        self.revision = ""
        self.subject = ""
        self.title = ""
        self.unit = {}
        self.up_axis = ""

    def getAttribute(self, attribute):
        if attribute == "author":
            if self.contributor:
                return self.contributor.author
            else: return ""
        elif attribute == "copyright":
            if self.contributor:
                return self.contributor.copyright
            else: return ""
        elif attribute == "title":
            return self.title
        elif attribute == "keywords":
            return " ".join(self.keywords)
        else:
            return "Invalid attribute '%s'" % attribute

class BoolArray(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.values = []
        self.count = 0
        self.id = ""
        self.name = ""

class Contributor(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.author = ""
        self.authoring_tool = ""
        self.comment = ""
        self.copyright = ""
        self.source_date = ""

class ConvexMesh(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.convex_hull_of = ""
        self.sources = []
        self.vertices = []
        self.lines = []
        self.linestrips = []
        self.polygons = []
        self.polylists = []
        self.triangles = []
        self.trifans = []
        self.tristrips = []

class Extra(PlungerNode):
    pass

class FloatArray(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.count = 0
        self.values = []
        self.id = ""
        self.name = ""
    def getStride(self):
        if self.parent.technique_common:
            if self.parent.technique_common.child_element:
                return self.parent.technique_common.child_element.stride
            else:
                return 1
        else:
            return 1

class Geometry(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.name = ""
        self.id = ""
        self.content = None

class IDREFArray(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.count = 0
        self.values = []
        self.id = ""
        self.name = ""

class Input(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.offset = 0
        self.semantic = ""
        self.source = ""
        self.set = 0

class IntArray(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.values = []
        self.count = 0
        self.id = ""
        self.name = ""
        self.defaultMin = -2147483648
        self.defaultMax =  2147483647
        self.minInclusive = self.defaultMin
        self.maxInclusive = self.defaultMax

class LibraryAnimations(PlungerNode):
    pass

class LibraryAnimationClips(PlungerNode):
    pass

class LibraryCameras(PlungerNode):
    pass

class LibraryControllers(PlungerNode):
    pass

class LibraryEffects(PlungerNode):
    pass

class LibraryForceFields(PlungerNode):
    pass

class LibraryGeometries(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.geometries = []

    def getNumMeshes(self):
        return len(self.getMeshes())

    def getMeshes(self):
        meshes = []
        for geo in self.geometries:
            if geo.content and geo.content.getType() == "Mesh":
                meshes.append(geo.content)
        return meshes

class LibraryImages(PlungerNode):
    pass

class LibraryLights(PlungerNode):
    pass

class LibraryMaterials(PlungerNode):
    pass

class LibraryNodes(PlungerNode):
    pass

class LibraryPhysicsMaterials(PlungerNode):
    pass

class LibraryPhysicsModels(PlungerNode):
    pass

class LibraryPhysicsScenes(PlungerNode):
    pass

class LibraryVisualScenes(PlungerNode):
    pass

class Lines(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.primitives = []
        self.name = ""
        self.material = ""

class LineStrips(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.primitives = []
        self.name = ""
        self.material = ""

class Mesh(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.sources = []
        self.vertices = []
        self.lines = []
        self.linestrips = []
        self.polygons = []
        self.polylists = []
        self.triangles = []
        self.trifans = []
        self.tristrips = []

    def getNumVertices(self):
        vcount = 0
        for vertex in self.vertices:
            pass #FIXME: fix this.
        return vcount


class NameArray(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.values = []
        self.count = 0
        self.id = ""
        self.name = ""

class Param(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.name = ""
        self.sid = ""
        self.type = ""
        self.semantic = ""

class Polygons(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.primitives = []
        self.name = ""
        self.material = ""
        self.polyholes = []

class PolyHoles(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.holes = []
        self.primitives = []

class Polylist(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.primitives = []
        self.name = ""
        self.material = ""
        self.vcount = []

class Scene(PlungerNode):
    pass

class Source(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.array_content = None
        self.id = ""
        self.name = ""
        self.technique = None
        self.technique_common = None

class Spline(PlungerNode):
    pass

class TechniqueCommon(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.child_element = None

class Triangles(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.primitives = []
        self.count = 0
        self.name = ""
        self.material = ""

class TriFans(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.primitives = []
        self.count = 0
        self.name = ""
        self.material = ""

class TriStrips(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.primitives = []
        self.count = 0
        self.name = ""
        self.material = ""

class Vertices(PlungerNode):
    def __init__(self):
        PlungerNode.__init__(self)
        self.inputs = []
        self.id = ""
        self.name = ""