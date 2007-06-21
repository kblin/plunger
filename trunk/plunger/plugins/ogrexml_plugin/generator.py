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
"""Generate mesh.xml files for Ogre3D.
"""

class Generator:
    def __init__(self, indent_depth=4):
        self.out_string = ""
        self.indent_depth = indent_depth

    def indent(self, depth):
        indent_string = " " * (depth * self.indent_depth)
        self.append(indent_string)

    def append(self, string):
        self.out_string += string

    def appendIfAttr(self, node, attr):
        obj_attr = getattr(node, attr, None)
        if obj_attr:
            self.append(' %s="%s"' % (attr, obj_attr))

    def toxml(self):
        return self.out_string

    def generate(self, node, depth=0):
        if not node:
            return

        handler_function = getattr(self, "do_%s" %node.getType())
        handler_function(node, depth)

    def do_Face(self, node, depth):
        """A Face object maps to a <face> tag
        """
        self.indent(depth)
        self.append('<face v1="%s" v2="%s" v3="%s" />\n' %
                tuple(node.getFace()))

    def do_Faces(self, node, depth):
        """A Faces object maps to a <faces> tag
        """
        self.indent(depth)
        self.append('<faces count="%s">\n' % node.getNumFaces())

        for face in node.faces:
            self.generate(face, depth+1)

        self.indent(depth)
        self.append('</faces>\n')

    def do_Mesh(self, node, depth):
        """A Mesh object maps to a <submesh> tag.
        """
        self.indent(depth)
        self.append("<submesh")
        if node.getNumMaterials()> 0:
            self.append(' material="%s"' % node.getMaterials()[0].getPath())
        self.append(' usesharedvertices="false" use32bitindexes="false"')
        self.append(' operationtype="triangle_list">\n')

        self.generate(node.faces, depth+1)

        self.generate(node.vertices, depth+1)

        self.indent(depth)
        self.append('</submesh>\n')

    def do_Model(self, node, depth):
        """The Model object maps to the <mesh> tag.
        """
        self.indent(depth)
        self.append("<mesh>\n")

        self.indent(depth+1)
        self.append("<submeshes>\n")
        for mesh in node.getMeshes():
            self.generate(mesh, depth+2)
        self.indent(depth+1)
        self.append("</submeshes>\n")

        self.indent(depth)
        self.append("</mesh>\n")

    def do_Vertex(self, node, depth):
        """The Vertex object maps to a <vertex> tag and contains the <position>
        and possibly <normal> and <texcoord> tags.
        Note that plunger uses "y is up" and Ogre uses "z is up".
        """
        self.indent(depth)
        self.append('<vertex>\n')

        self.indent(depth+1)
        self.append('<position x="%s" y="%s" z="%s" />\n' %
                (node.getPosition()[0], node.getPosition()[2], node.getPosition()[1] * -1.0))

        if node.getNormals():
            self.indent(depth+1)
            self.append('<normal x="%s" y="%s" z="%s" />\n' %
                (node.getNormals()[0], node.getNormals()[2], node.getNormals()[1] * -1.0))

        if node.getUVCoords():
            self.indent(depth+1)
            self.append('<texcoord u="%s" v="%s"' % (node.getUVCoords()[0],
                node.getUVCoords()[1]))
            if len(node.getUVCoords()) == 3:
                self.append(' w="%s"'% node.getUVCoords()[2])
            self.append(' />\n')

        self.indent(depth)
        self.append('</vertex>\n')

    def do_Vertices(self, node, depth):
        """The Vertices object contains information for both the <geometry> as
        well as the <vertexbuffer> tag.
        We create only one <vertexbuffer>, which isn't completely valid for
        animated models. However, the OgreXMLConverter takes care of that and
        splits up the vertexbuffers as needed.
        """
        self.indent(depth)
        self.append('<geometry vertexcount="%s">\n' % node.getNumVertices())

        self.indent(depth+1)
        # we know that at least one vertexbuffer needs positions, and we only
        # write one vertexbuffer.
        self.append('<vertexbuffer positions="true"')
        if node.getVertices()[0].getNormals():
            self.append(' normals="true"')
        # This only handles one set of texture coordinates, which probably is
        # fine for now.
        texcoords = node.getVertices()[0].getUVCoords()
        if texcoords:
            self.append(' texture_coord_dimensions_0="%s"' % len(texcoords))
            self.append(' texture_coords="1"')

        self.append('>\n')

        for vertex in node.getVertices():
            self.generate(vertex, depth+2)

        self.indent(depth+1)
        self.append('</vertexbuffer>\n')

        self.indent(depth)
        self.append('</geometry>\n')

