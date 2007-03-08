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
"""Parser for the Ogre3D mesh.xml format.
"""

try:
    from plunger import dom
except ImportError:
    import sys
    sys.path.append("../..")
    import dom
    sys.path.pop()

def addAttr(obj, node, attr, convert_fun=lambda x: x):
    """Add attribute "attr" to object "obj" if it exists in node "node".
    If convert_fun is specified, use it to convert the nodeValue.
    """
    if attr in node.attributes.keys():
        setattr(obj, attr, convert_fun(node.attributes[attr].nodeValue))

class Parser:
    """Parse Ogre3D mesh.xml files
    """

    def __init__(self, model):
        self.model = model

    def parse(self, node, parent=None):
        """Dispatch the correct parser for the node to parse
        """
        parse_fun = getattr(self, "parse%s" % node.__class__.__name__)
        parse_fun(node, parent)

    def parseChildNodes(self, node, parent):
        """Parse all child nodes of the given node
        """
        for child in node.childNodes:
            self.parse(child, parent)

    def parseComment(self, node, parent):
        """Ignore comments
        """
        pass

    def parseDocument(self, node, parent):
        """The document contains a documentElement, so parse that.
        """
        self.parse(node.documentElement)

    def parseElement(self, node, parent):
        """Dispatch a function to handle whatever tag node contains
        """
        handler_fun = getattr(self, "do_%s" % node.tagName, self.do_nyi)
        handler_fun(node, parent)

    def parseText(self, node, parent):
        """Ignore text
        """
        pass

    def do_nyi(self, node, parent):
        """Handle unimplemented functions
        """
        print "WARNING: unimplemented tag %s!" % node.tagName

    def do_mesh(self, node, parent):
        """Handle the <mesh> tag, which is the root node of ogre's mesh.xml
        """
        self.parseChildNodes(node, self.model)

    def do_submeshes(self, node, parent):
        """Handle the <submeshes> tag, which groups all the meshes in the model.
        """
        meshes = dom.Meshes()
        meshes.parent = parent
        parent.meshes = meshes

        self.parseChildNodes(node, meshes)

    def do_submesh(self, node, parent):
        """Handle the <submesh> tag, which contains one mesh for the model.
        """
        mesh = dom.Mesh()
        mesh.parent = parent
        parent.meshes.append(mesh)

        materials = dom.Materials()
        materials.parent = mesh
        mesh.materials = materials

        material = dom.Material()
        material.parent = materials
        materials.materials.append(material)

        if "material" in node.attributes.keys():
            material.path = str(node.attributes["material"].nodeValue)

        self.parseChildNodes(node, mesh)

    def do_faces(self, node, parent):
        """Handle the <faces> tag, which groups the faces for the mesh
        """
        faces = dom.Faces()
        faces.parent = parent
        parent.faces = faces

        self.parseChildNodes(node, faces)

    def do_geometry(self, node, parent):
        """Handle the <geometry> tag, which groups vertex buffers
        """
        self.parseChildNodes(node, parent)

    def do_vertexbuffer(self, node, parent):
        """Handle the <vertexbuffer> tag
        """
        # NOTE: I'll stuff all <vertexbuffer>s into one Vertices object
        vertices = None
        if parent.vertices:
            vertices = parent.vertices
            vertices.initial = False
        else:
            vertices = dom.Vertices()
            parent.vertices = vertices
            vertices.parent = parent
            vertices.initial = True

        #FIXME: figure out how to handle the attributes, maybe
        vertices.vcount = 0

        self.parseChildNodes(node, vertices)

    def do_vertex(self, node, parent):
        """Handle the <vertex> tag
        """
        vertex = None
        if parent.initial:
            vertex = dom.Vertex()
            vertex.parent = parent
            parent.vertices.append(vertex)
        else:
            vertex = parent.vertices[parent.vcount]
            parent.vcount += 1

        self.parseChildNodes(node, vertex)

    def do_position(self, node, parent):
        """Handle the <position> tag
        """
        position = []
        position.append(float(node.attributes['x'].nodeValue))
        position.append(float(node.attributes['y'].nodeValue))
        position.append(float(node.attributes['z'].nodeValue))
        parent.position = position

    def do_normal(self, node, parent):
        """Handle the <normal>
        """
        normal = []
        normal.append(float(node.attributes['x'].nodeValue))
        normal.append(float(node.attributes['y'].nodeValue))
        normal.append(float(node.attributes['z'].nodeValue))
        parent.normals = normal

    def do_texcoord(self, node, parent):
        """Handle the first <texcoord> tag
        """
        #FIXME: This only works if there's one texcoord tag for now
        texcoord = []
        texcoord.append(float(node.attributes['u'].nodeValue))
        texcoord.append(float(node.attributes['v'].nodeValue))
        parent.uv_coords = texcoord

    def do_face(self, node, parent):
        """Handle the <face> tag
        """
        face = dom.Face()
        face.parent = parent
        parent.faces.append(face)

        vlist = []
        vlist.append(int(node.attributes['v1'].nodeValue))
        vlist.append(int(node.attributes['v2'].nodeValue))
        vlist.append(int(node.attributes['v3'].nodeValue))
        face.vertex_list = vlist

