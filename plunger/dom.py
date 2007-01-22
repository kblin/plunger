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
        self.collada_xml = None

    def getType(self):
        return self.__class__.__name__

    def getAssetInfo(self, attribute):
        if self.asset:
            return self.asset.getAttribute(attribute)
        else: return ""

class Model:
    def __init__(self):
        self.model_tree_root = None

    def getType(self):
        return self.__class__.__name__

    def getRoot(self):
        return self.model_tree_root

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

class Contributor(PlungerNode):
    def __init__(self):
        self.author = ""
        self.authoring_tool = ""
        self.comment = ""
        self.copyright = ""
        self.source_date = ""

class Extra(PlungerNode):
    pass

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
    pass

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

class Scene(PlungerNode):
    pass

