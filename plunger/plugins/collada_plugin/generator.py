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
"""Generate Collada XML output from a Plunger DOM
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

    def toxml(self):
        return self.out_string

    def generate(self, node, depth=0):
        """Dispatch a function to generate XML for a specific node
        """
        if not node:
            return

        handler_function = getattr(self, "do_%s" % node.getType())
        handler_function(node, depth)

    def do_Model(self, node, depth):
        self.append('<?xml version="1.0"?>\n')
        self.generate(node.model_tree_root, 0)

    def do_COLLADA(self, node, depth):
        self.indent(depth)
        self.append('<COLLADA')
        self.append(' version="%s"' % node.version)
        if node.xmlns:
            self.append(' xmlns="%s"' % node.xmlns)
        if node.base:
            self.append(' base="%s"' % node.base)
        self.append('>\n')

        if node.asset:
            #self.generate(node.asset, depth+1)
            pass
        if node.animations:
            #self.generate(node.animations, depth+1)
            pass
        if node.clips:
            #self.generate(node.clips, depth+1)
            pass
        if node.cameras:
            #self.generate(node.cameras, depth+1)
            pass
        if node.controllers:
            #self.generate(node.controllers, depth+1)
            pass
        if node.effects:
            #self.generate(node.effects, depth+1)
            pass
        if node.force_fields:
            #self.generate(node.force_fields, depth+1)
            pass
        if node.geometries:
            self.generate(node.geometries, depth+1)
            pass
        if node.images:
            #self.generate(node.images, depth+1)
            pass
        if node.lights:
            #self.generate(node.lights, depth+1)
            pass
        if node.materials:
            #self.generate(node.materials, depth+1)
            pass
        if node.nodes:
            #self.generate(node.nodes, depth+1)
            pass
        if node.physics_materials:
            #self.generate(node.physics_materials, depth+1)
            pass
        if node.physics_models:
            #self.generate(node.physics_models, depth+1)
            pass
        if node.physics_scenes:
            #self.generate(node.physics_scenes, depth+1)
            pass
        if node.visual_scenes:
            #self.generate(node.visual_scenes, depth+1)
            pass
        if node.scene:
            #self.generate(node.scene, depth+1)
            pass
        if node.extras:
            self.generate(node.extras, depth+1)
            pass

        self.indent(depth)
        self.append('</COLLADA>\n')

    def do_Asset(self, node, depth):
        self.indent(depth)
        self.append('<asset>\n')

        if node.contributor:
            self.generate(node.contributor, depth+1)
        if node.created:
            self.indent(depth+1)
            self.append('<created>%s</created>\n' % node.created)
        if node.keywords:
            self.indent(depth+1)
            self.append('<keywords>%s</keywords>\n' % " ".join(node.keywords))
        if node.modified:
            self.indent(depth+1)
            self.append('<modified>%s</modified>\n' % node.modified)
        if node.revision:
            self.indent(depth+1)
            self.append('<revision>%s</revision>\n' % node.revision)
        if node.subject:
            self.indent(depth+1)
            self.append('<subject>%s</subject>\n' % node.subject)
        if node.title:
            self.indent(depth+1)
            self.append('<title>%s</title>\n' % node.title)
        if node.unit:
            self.indent(depth+1)
            self.append('<unit')
            if "name" in node.unit:
                self.append(' name="%s"' % node.unit['name'])
            if "meter" in node.unit:
                self.append(' meter="%s"' % node.unit['meter'])
            self.append(' />\n')
        if node.up_axis:
            self.indent(depth+1)
            self.append('<up_axis>%s</up_axis>\n'% node.up_axis)

        self.indent(depth)
        self.append('</asset>\n')

    def do_BoolArray(self, node, depth):
        self.indent(depth)
        self.append('<bool_array count="%s"' % len(node.values))
        if node.id:
            self.append(' id="%s"' % node.id)
        if node.name:
            self.append(' name="%s"' % node.name)
        import string
        self.append('>%s' % " ".join([string.lower("%s" %s) for s in
            node.values]))
        self.append('</bool_array>\n')

    def do_Contributor(self, node, depth):
        self.indent(depth)
        self.append('<contributor>\n')
        if node.author:
            self.indent(depth+1)
            self.append('<author>%s</author>\n' % node.author)
        if node.authoring_tool:
            self.indent(depth+1)
            self.append('<authoring_tool>%s</authoring_tool>\n' % node.authoring_tool)
        if node.comments:
            self.indent(depth+1)
            self.append('<comments>%s</comments>\n' % node.comments)
        if node.copyright:
            self.indent(depth+1)
            self.append('<copyright>%s</copyright>\n' % node.copyright)
        if node.source_data:
            self.indent(depth+1)
            self.append('<source_data>%s</source_data>\n' % node.source_data)

        self.indent(depth)
        self.append('</contributor>\n')

    def do_ConvexMesh(self, node, depth):
        self.indent(depth)
        self.append('<convex_mesh />\n')

    def do_Extras(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_FloatArray(self, node, depth):
        self.indent(depth)
        self.append('<float_array count="%s"' % len(node.values))
        if node.id:
            self.append(' id="%s"' % node.id)
        if node.name:
            self.append(' name="%s"' % node.name)
        import string
        self.append('>%s' % " ".join(["%s" %s for s in node.values]))
        self.append('</float_array>\n')

    def do_Geometry(self, node, depth):
        self.indent(depth)
        self.append('<geometry')
        if node.name:
            self.append(' name="%s"' % node.name)
        if node.id:
            self.append(' id="%s"' % node.id)

        self.append('>\n')

        if node.content:
            self.generate(node.content, depth+1)

        self.indent(depth)
        self.append('</geometry>\n')

    def do_IDREFArray(self, node, depth):
        self.indent(depth)
        self.append('<IDREF_array count="%s"' % len(node.values))
        if node.id:
            self.append(' id="%s"' % node.id)
        if node.name:
            self.append(' name="%s"' % node.name)
        import string
        self.append('>%s' % " ".join(node.values))
        self.append('</IDREF_array>\n')

    def do_Input(self, node, depth):
        """Create Collada <input> tags
        """
        self.indent(depth)
        self.append('<input')
        if node.offset:
            self.append(' offset="%s"' % node.offset)
        if node.semantic:
            self.append(' semantic="%s"' % node.semantic)
        if node.source:
            self.append(' source="%s"' % node.source)
        if node.set:
            self.append(' set="%s"' % node.set)
        self.append(' />\n')

    def do_IntArray(self, node, depth):
        self.indent(depth)
        self.append('<int_array count="%s"' % len(node.values))
        if node.id:
            self.append(' id="%s"' % node.id)
        if node.name:
            self.append(' name="%s"' % node.name)
        import string
        self.append('>%s' % " ".join([string.lower("%s" %s) for s in
            node.values]))
        self.append('</int_array>\n')

    def do_LibraryAnimations(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryAnimationClips(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryCameras(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryControllers(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryEffects(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryForceFields(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryGeometries(self, node, depth):
        self.indent(depth)
        self.append('<libarary_geometries>\n')
        for geometry in node.geometries:
            self.generate(geometry, depth+1)

    def do_LibraryImages(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryLights(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryMaterials(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryNodes(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryPhysicalMaterials(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryPhysicalModels(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryPhysicalScenes(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_LibraryVisualScenes(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_Lines(self, node, depth):
        self.indent(depth)
        self.append('<lines count="%s"' % node.count)
        if node.name:
            self.append(' name="%s"' % node.name)
        if node.material:
            self.append(' material="%s"' % node.material)
        self.append('>\n')

        for prim in node.primitives:
            self.indent(depth+1)
            self.append('<p>%s</p>\n' % " ".join(["%s" % s for s in prim]))
        self.indent(depth)
        self.append('</lines>\n')

    def do_Linestrips(self, node, depth):
        self.indent(depth)
        self.append('<linestrips count="%s"' % node.count)
        if node.name:
            self.append(' name="%s"' % node.name)
        if node.material:
            self.append(' material="%s"' % node.material)
        self.append('>\n')

        for prim in node.primitives:
            self.indent(depth+1)
            self.append('<p>%s</p>\n' % " ".join(["%s" % s for s in prim]))

        self.indent(depth)
        self.append('</linestrips>\n')

    def do_Mesh(self, node, depth):
        self.indent(depth)
        self.append('<mesh>\n')
        for source in node.sources:
            self.generate(source, depth+1)
        for vertex in node.vertices:
            self.generate(vertex, depth+1)
        for line in node.lines:
            self.generate(line, depth+1)
        for strip in node.linestrips:
            self.generate(strip, depth+1)
        for poly in node.polygons:
            self.generate(poly, depth+1)
        for ply in node.polylists:
            self.generate(poly, depth+1)
        for tri in node.triangles:
            self.generate(tri, depth+1)
        for tri in node.trifans:
            self.generate(tri, depth+1)
        for tri in node.tristrips:
            self.generate(tri, depth+1)

        self.indent(depth)
        self.append('</mesh>\n')

    def do_NameArray(self, node, depth):
        self.indent(depth)
        self.append('<Name_array count="%s"' % len(node.values))
        if node.id:
            self.append(' id="%s"' % node.id)
        if node.name:
            self.append(' name="%s"' % node.name)
        import string
        self.append('>%s' % " ".join(node.values))
        self.append('</Name_array>\n')

    def do_Scene(self, node, depth):
        self.indent(depth)
        self.append(node.collada_xml)

    def do_Source(self, node, depth):
        self.indent(depth)
        self.append('<source id="%s"' % node.id)
        if node.name:
            self.append(' name="%s"' % node.name)
        self.append(' >\n')
        if node.asset:
            self.generate(node.asset, depth+1)
        if node.content_array:
            self.generate(node.content_array, depth+1)

        self.indent(depth)
        self.append('</source>\n')

    def do_Vertices(self, node, depth):
        """Create Collada tags for the vertices
        """
        self.indent(depth)
        self.append('<vertices id="%s"'% node.id)
        if node.name:
            self.append(' name="%s"' %node.name)
        self.append('>\n')
        for input in node.inputs:
            self.generate(input, depth+1)
        self.indent(depth)
        self.append('</vertices>\n')
