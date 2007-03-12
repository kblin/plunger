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
"""Parser for the Collada XML format.
Right now there is incomplete support for the Collada 1.4.2 specification.
"""

try:
    from plunger import dom
except ImportError:
    import sys
    sys.path.append("../..")
    import dom
    sys.path.pop()

def addAttr(obj, node, attr, convert_fun=lambda x: x):
    """Add attribute "attr" to object "obj" if the node "node" has said
    attribute. If convert is set, convert the nodeValue to type.
    """
    if attr in node.attributes.keys():
        setattr(obj, attr, convert_fun(node.attributes[attr].nodeValue))

class Source:
    """Model <source> tags that hold data until it can be stored in the DOM
    """
    def __init__(self):
        self.id = ""
        self.values = []
        self.accessor = {}

class Parser:
    """Parse Collada XML files
    """

    def __init__(self, model):
        self.model = model
        self.known_sources = {}

    def registerId(self, id, object):
        self.known_sources[id] = object

    def lookupId(self, id):
        object = self.model.getNodeById(id)
        if object:
            return object
        if id in self.known_sources.keys():
            return self.known_sources[id]
        return None

    def parse(self, node, parent=None):
        """Dispatch the correct function to parse the node
        """
        parse_function = getattr(self, "parse%s" % node.__class__.__name__)
        parse_function(node, parent)

    def parseChildNodes(self, node, parent):
        for child in node.childNodes:
            self.parse(child, parent)

    def parseComment(self, node, parent):
        """Ignore comments
        """
        pass

    def parseDocument(self, node, parent):
        """Just parse the documentElement
        """
        self.parse(node.documentElement)

    def parseElement(self, node, parent):
        """Parse a tag
        """
        handler_function = getattr(self, "do_%s" % node.tagName, self.do_nyi)
        handler_function(node, parent)

    def parseText(self, node, parent):
        """Parse text
        Silently ignore text.
        """
        pass

    def do_nyi(self, node, parent):
        """Handle all elements that do not have a function yet
        """
        print "WARNING: unimplemented tag %s!" % node.tagName

    def do_COLLADA(self, node, parent):
        """Handle the COLLADA tag
        We're interested in the version and xmlns attributes for now
        """
        self.model.collada_xml = node.toxml()
        self.parseChildNodes(node, self.model)

    def do_accessor(self, node, parent):
        """Handle the <accessor> tag
        """
        keys = node.attributes.keys()

        if "count" in keys:
            parent.accessor["count"] = int(node.attributes["count"].nodeValue)

        if "offset" in keys:
            parent.accessor["offset"] = int(node.attributes["offset"].nodeValue)

        if "source" in keys:
            parent.accessor["source"] = node.attributes["source"].nodeValue

        if "stride" in keys:
            parent.accessor["stride"] = int(node.attributes["stride"].nodeValue)

    def do_asset(self, node, parent):
        """Skip the <asset> tag
        """
        pass

    def do_author(self, node, parent):
        """Handle the <author> tag
        """
        if node.firstChild:
            parent.author = node.firstChild.nodeValue

    def do_authoring_tool(self, node, parent):
        """Handle the <authoring_tool> tag
        """
        if node.firstChild:
            parent.authoring_tool = node.firstChild.nodeValue

    def do_bool_array(self, node, parent):
        """Handle the <bool_array> tag
        """
        bool = dom.BoolArray()
        parent.content_array = bool
        bool.parent = parent

        addAttr(bool, node, "count", int)
        addAttr(bool, node, "name")
        addAttr(bool, node, "id")
        self.model.registerId(bool.id, bool)

        if node.firstChild:
            bool.values = [b == "true" for b in
                node.firstChild.nodeValue.split()[:bool.count]]

    def do_comments(self, node, parent):
        """Handle the <comments> tag
        """
        if node.firstChild:
            parent.comments = node.firstChild.nodeValue

    def do_contributor(self, node, parent):
        """Handle the <contributor> tag
        """
        contributor = dom.Contributor()
        parent.contributor = contributor
        contributor.parent = parent

        self.parseChildNodes(node, contributor)

    def do_copyright(self, node, parent):
        """Handle the <copyright> tag
        """
        if node.firstChild:
            parent.copyright = node.firstChild.nodeValue

    def do_created(self, node, parent):
        """Handle the <created> tag
        """
        if node.firstChild:
            parent.created = node.firstChild.nodeValue

    def do_convex_mesh(self, node, parent):
        """Handle the <convex_mesh> tag
        """
        cm = dom.ConvexMesh()
        cm.parent = parent
        parent.content = cm

        addAttr(cm, node, "convex_hull_of")

        self.parseChildNodes(node, cm)

    def do_extra(self, node, parent):
        """skip the <extra> tag
        """
        pass

    def do_float_array(self, node, parent):
        """Handle the <float_array> tag
        """
        count = 0
        if "count" in node.attributes.keys():
            count = int(node.attributes["count"].nodeValue)

        if node.firstChild:
            parent.values = [float(f) for f in
                node.firstChild.nodeValue.split()[:count]]

    def do_geometry(self, node, parent):
        """Handle the <geometry> tag
        """
        mesh = dom.Mesh()

        for child in node.childNodes:
            if not child.__class__.__name__ == "Element":
                continue

            if child.tagName == "mesh":
                parent.meshes.append(mesh)
                mesh.parent = parent
                self.parse(child, mesh)

    def do_h(self, node, parent):
        """Handle the <h> primitives tag
        """
        if node.firstChild:
            parent.holes.append([ int(i) for i in
                node.firstChild.nodeValue.split()])

    def do_IDREF_array(self, node, parent):
        """Handle the <IDEREF_array> tag
        """
        idref = dom.IDREFArray()
        parent.content_array = idref
        idref.parent = parent

        addAttr(idref, node, "count", int)
        addAttr(idref, node, "name")
        addAttr(idref, node, "id")
        self.model.registerId(idref.id, idref)

        if "count" in node.attributes.keys():
            count = int(node.attributes['count'].nodeValue)
        if node.firstChild:
            idref.values = node.firstChild.nodeValue.split()[:idref.count]

    def do_int_array(self, node, parent):
        """Handle the <int_array> tag
        """
        int_array = dom.IntArray()
        parent.content_array = int_array
        int_array.parent = parent

        addAttr(int_array, node, "count", int)
        addAttr(int_array, node, "name")
        addAttr(int_array, node, "id")
        addAttr(int_array, node, "minInclusive")
        addAttr(int_array, node, "maxInclusive")
        self.model.registerId(int_array.id, int_array)

        if node.firstChild:
            int_array.values = [int(f) for f in
                node.firstChild.nodeValue.split()[:int_array.count]]

    def do_keywords(self, node, parent):
        """Handle the <keywords> tag
        """
        if node.firstChild:
            parent.created = node.firstChild.nodeValue.split(" ")

    def do_library_animations(self, node, parent):
        """skip the <library_animations> tag
        """
        pass

    def do_library_animation_clips(self, node, parent):
        """skip the <library_animation_clips> tag
        """
        pass

    def do_library_cameras(self, node, parent):
        """skip the <library_cameras> tag
        """
        pass

    def do_library_controllers(self, node, parent):
        """skip the <library_controllers> tag
        """
        pass

    def do_library_effects(self, node, parent):
        """skip the <library_effects> tag
        """
        pass

    def do_library_force_fields(self, node, parent):
        """skip the <library_force_fields> tag
        """
        pass

    def do_library_geometries(self, node, parent):
        """handle the <library_geometries> tag
        """
        meshes = dom.Meshes()
        meshes.parent = parent
        parent.meshes = meshes
        self.parseChildNodes(node, meshes)

    def do_library_images(self, node, parent):
        """skip the <library_images> tag
        """
        pass

    def do_library_lights(self, node, parent):
        """skip the <library_lights> tag
        """
        pass

    def do_library_materials(self, node, parent):
        """skip the <library_materials> tag
        """
        pass

    def do_library_nodes(self, node, parent):
        """skip the <library_nodes> tag
        """
        pass

    def do_library_physics_materials(self, node, parent):
        """skip the <library_physics_materials> tag
        """
        pass

    def do_library_physics_models(self, node, parent):
        """skip the <library_physics_models> tag
        """
        pass

    def do_library_physics_scenes(self, node, parent):
        """skip the <library_physics_scenes> tag
        """
        pass

    def do_library_visual_scenes(self, node, parent):
        """skip the <library_effects> tag
        """
        pass

    def do_lines(self, node, parent):
        """Handle the <lines> tag
        """
        lines = dom.Lines()
        lines.parent = parent
        parent.lines.append(lines)

        addAttr(lines, node, "name")
        addAttr(lines, node, "material")
        addAttr(lines, node, "count", int)

        self.parseChildNodes(node, lines)

    def do_linestrips(self, node, parent):
        """Handle the <linestrips> tag
        """
        linestripss = dom.Linestrips()
        linestrips.parent = parent
        parent.linestrips.append(linestrips)

        addAttr(linestrips, node, "name")
        addAttr(linestrips, node, "material")
        addAttr(linestrips, node, "count", int)

        self.parseChildNodes(node, linestrips)


    def do_mesh(self, node, parent):
        """Handle the <mesh> tag
        """
        self.parseChildNodes(node, parent)

    def do_modified(self, node, parent):
        """Handle the <modified> tag
        """
        if node.firstChild:
            parent.modified = node.firstChild.nodeValue

    def do_Name_array(self, node, parent):
        """Handle the <Name_array> tag
        """
        name_array = dom.NameArray()
        parent.content_array = name_array
        name_array.parent = parent

        addAttr(name_array, node, "count", int)
        addAttr(name_array, node, "name")
        addAttr(name_array, node, "id")
        self.model.registerId(name_array.id, name_array)

        if node.firstChild:
            name_array.values = node.firstChild.nodeValue.split()[:name_array.count]

    def do_param(self, node, parent):
        """Handle the <param> tag
        """
        param = dom.Param()
        parent.params.append(param)
        param.parent = parent

        addAttr(param, node, "name")
        addAttr(param, node, "sid")
        addAttr(param, node, "type")
        addAttr(param, node, "semantic")

    def do_ph(self, node, parent):
        """Handle the <ph> tag
        """
        polyhole = dom.PolyHoles()
        polyhole.parent = parent
        parent.polyholes.append(polyhole)

        self.parseChildNodes(node, polyhole)

    def do_polygons(self, node, parent):
        """Handle the <polygons> tag
        """
        poly = dom.Polygons()
        poly.parent = parent
        parent.polygons.append(ploy)

        addAttr(poly, node, "name")
        addAttr(poly, node, "material")
        addAttr(poly, node, "count", int)

        self.parseChildNodes(node, poly)

    def do_polylist(self, node, parent):
        """Handle the <polylist> tag
        """
        poly = dom.Polylist()
        poly.parent = parent
        parent.polylists.append(poly)

        addAttr(poly, node, "name")
        addAttr(poly, node, "material")
        addAttr(poly, node, "count", int)

        self.parseChildNodes(node, poly)

    def do_revision(self, node, parent):
        """Handle the <revision> tag
        """
        if node.firstChild:
            parent.revision = node.firstChild.nodeValue

    def do_scene(self, node, parent):
        """skip the <scene> tag
        """
        pass

    def do_source(self, node, parent):
        """Handle the <source> tag
        """
        source = Source()
        source.parent = parent

        addAttr(source, node, "name")
        addAttr(source, node, "id")
        self.registerId(source.id, source)

        self.parseChildNodes(node, source)

    def do_source_data(self, node, parent):
        """Handle the <source_data> tag
        """
        if node.firstChild:
            parent.source_data = node.firstChild.nodeValue

    def do_subject(self, node, parent):
        """Handle the <subject> tag
        """
        if node.firstChild:
            parent.subject = node.firstChild.nodeValue

    def do_technique(self, node, parent):
        """Handle the <technique> tag
        """
        pass

    def do_technique_common(self, node, parent):
        """Handle the <technique_common> tag
        """
        self.parseChildNodes(node, parent)

    def do_title(self, node, parent):
        """Handle the <title> tag
        """
        if node.firstChild:
            parent.title = node.firstChild.nodeValue

    def do_triangles(self, node, parent):
        """Handle the <triangles> tag
        """
        faces = dom.Faces()
        faces.parent = parent
        parent.faces = faces

        if "count" in node.attributes.keys():
            faces.count = int(node.attributes['count'].nodeValue)

        vertex_offset = 0
        vertex_source = ""
        normal_offset = 0
        normal_source = ""
        semantic = ""
        primitives = []
        max_offset = 0

        for child in node.childNodes:
            if not child.__class__.__name__ == "Element":
                continue

            if child.tagName == "input":
                keys = child.attributes.keys()
                if "semantic" in keys:
                    semantic = child.attributes['semantic'].nodeValue

                if semantic == "VERTEX":
                    if "offset" in keys:
                        vertex_offset = int(child.attributes['offset'].nodeValue)
                        if vertex_offset > max_offset:
                            max_offset = vertex_offset
                    if "source" in keys:
                        vertex_source =\
                            child.attributes['source'].nodeValue.replace('#','')
                elif semantic == "NORMAL":
                    if "offset" in keys:
                        normal_offset = int(child.attributes['offset'].nodeValue)
                        if normal_offset > max_offset:
                            max_offset = normal_offset
                    if "source" in keys:
                        normal_source =\
                            child.attributes['source'].nodeValue.replace('#','')

            elif child.tagName == "p":
                if child.firstChild:
                    primitives = [int(i) for i in
                    child.firstChild.nodeValue.split()]

        normals = self.lookupId(normal_source)

        for i in range(0,len(primitives), (max_offset + 1) * 3 ):
            face = dom.Face()
            face.parent = faces
            faces.faces.append(face)
            if vertex_source:
                vlist = []
                vlist.append(primitives[ i + vertex_offset])
                vlist.append(primitives[ i + vertex_offset + max_offset +1])
                vlist.append(primitives[ i + vertex_offset + (2* (max_offset + 1))])
                face.vertex_list = vlist

            if normals:
                nlist = []
                nlist.append(primitives[ i + normal_offset])
                nlist.append(primitives[ i + normal_offset + max_offset + 1])
                nlist.append(primitives[ i + normal_offset + (2* (max_offset + 1))])
                for item in nlist:
                    face.normals.append(normals.values[item])

        #TODO: calculate vertex normals from face normals
        mesh = faces.parent
        vidx = 0
        for vertex in mesh.getVertices():
            print "TODO: calculate vertex normal for vertex %s" % vidx
            x = 0
            y = 0
            z = 0
            total = 0
            for face in faces.faces:
                if vidx in face.vertex_list:
                    x += face.normals[0]
                    y += face.normals[1]
                    z += face.normals[2]
                    total += 1
            if total:
                x /= total
                y /= total
                z /= total

            import math
            length = math.sqrt(x*x + y*y + z*z)
            if len:
                x /= length
                y /= length
                z /= length

            vertex.normals = [x, y, z]
            vidx += 1

    def do_trifans(self, node, parent):
        """Handle the <trifans> tag
        """
        tri = dom.TriFans()
        tri.parent = parent
        parent.triangles.append(tri)

        addAttr(tri, node, "name")
        addAttr(tri, node, "count", int)
        addAttr(tri, node, "material")

        self.parseChildNodes(node, tri)

    def do_tristrips(self, node, parent):
        """Handle the <tristrips> tag
        """
        tri = dom.TriStrips()
        tri.parent = parent
        parent.triangles.append(tri)

        addAttr(tri, node, "name")
        addAttr(tri, node, "count", int)
        addAttr(tri, node, "material")

        self.parseChildNodes(node, tri)

    def do_unit(self, node, parent):
        """Handle the <unit> tag
        """
        keys = node.attributes.keys()
        if "name" in keys:
            parent.unit['name'] = node.attributes['name'].nodeValue
        if "meter" in keys:
            parent.unit['meter'] = float(node.attributes['meter'].nodeValue)

    def do_up_axis(self, node, parent):
        """Handle the <up_axis> tag
        """
        if node.firstChild:
            parent.up_axis = node.firstChild.nodeValue

    def do_vcount(self, node, parent):
        """Handle the <vcount> tag
        """
        if node.firstChild:
            parent.vcount = [int(i) for i in node.firstChild.nodeValue.split()]

    def do_vertices(self, node, parent):
        """Handle the <vertices> tag
        """
        vertices = dom.Vertices()
        parent.vertices = vertices
        vertices.parent = parent

        if "id" in node.attributes.keys():
            self.model.registerId(node.attributes['id'].nodeValue, vertices)

        offset = 0
        source = ""
        semantic = ""

        for child in node.childNodes:
            if not child.__class__.__name__ == "Element":
                continue

            if child.tagName == "input":
                keys = child.attributes.keys()
                if "semantic" in keys:
                    semantic = child.attributes['semantic'].nodeValue

                if not semantic == "POSITION":
                    print "Looks like an invalid tag, ignoring"
                    return
                else:
                    if "source" in keys:
                        source =\
                            child.attributes['source'].nodeValue.replace('#', '')

        positions = self.lookupId(source)

        if not positions:
            print "Error: could not load source '%s'" % source
            return

        i = 0
        for i in range(0, len(positions.values), 3):
            vertex = dom.Vertex()
            vertex.parent = vertices
            vertices.vertices.append(vertex)

            vertex.position = positions.values[i:i+3]
            vertex.uv_coords = [0,0]

