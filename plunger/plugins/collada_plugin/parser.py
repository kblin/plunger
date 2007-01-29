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

def addAttr(obj, node, attr, type=None):
    """Add attribute "attr" to object "obj" if the node "node" has said
    attribute. If type is set, convert the nodeValue to type.
    """
    fun = lambda x : x
    if type:
        fun = getattr(__builtins__, type, fun)

    if attr in node.attributes.keys():
        setattr(obj, attr, fun(node.attributes[attr].nodeValue))

class Parser:
    """Parse Collada XML files
    """

    def __init__(self, model):
        self.model = model
        self.ignore_text = True

    def parse(self, node, parent=None):
        """Dispatch the correct function to parse the node
        """
        parse_function = getattr(self, "parse%s" % node.__class__.__name__)
        parse_function(node, parent)

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
        print "Parsing %s" % node.tagName
        handler_function = getattr(self, "do_%s" % node.tagName, self.do_nyi)
        handler_function(node, parent)

    def parseText(self, node, parent):
        """Parse text
        Silently ignore text unless ignore is set to false.
        """
        if self.ignore_text:
            return

        print "Here, we should handle text."

    def do_nyi(self, node, parent):
        """Handle all elements that do not have a function yet
        """
        pass

    def do_COLLADA(self, node, parent):
        """Handle the COLLADA tag
        We're interested in the version and xmlns attributes for now
        """
        collada = dom.COLLADA()
        self.model.model_tree_root = collada
        attrs = node.attributes.keys()
        if "version" in attrs:
            collada.version = node.attributes['version'].nodeValue
        if "xmlns" in attrs:
            pass
            collada.xmlns = node.attributes['xmlns'].nodeValue
        if "base" in attrs:
            collada.base = node.attributes['base'].nodeValue

        for child in node.childNodes:
            self.parse(child, collada)

    def do_accessor(self, node, parent):
        """Handle the <accessor> tag
        """
        accessor = dom.Accessor()
        parent.child_element = accessor
        accessor.parent = parent

        addAttr(accessor, node, "count", "int")
        addAttr(accessor, node, "offset", "int")
        addAttr(accessor, node, "source")
        addAttr(accessor, node, "stride", "int")

        for child in node.childNodes:
            self.parse(child, accessor)

    def do_asset(self, node, parent):
        """Handle the <asset> tag
        """
        asset = dom.Asset()
        parent.asset = asset
        asset.parent = parent

        for child in node.childNodes:
            self.parse(child, asset)

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
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            bool.name = node.attributes['name'].nodeValue
        if "id" in keys:
            bool.id = node.attributes['id'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)
        if node.firstChild:
            bool.values = [b == "true" for b in
                node.firstChild.nodeValue.split()[:count]]

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

        for child in node.childNodes:
            self.parse(child, contributor)

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

    def do_extras(self, node, parent):
        """handle the <extras> tag
        """
        #cheat and just store the xml code for now
        exras = dom.Extras()
        scenes.collada_xml = node.toxml()
        parent.scenes = scenes

    def do_float_array(self, node, parent):
        """Handle the <float_array> tag
        """
        float_array = dom.FloatArray()
        parent.content_array = float_array
        float_array.parent = parent
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            float_array.name = node.attributes['name'].nodeValue
        if "id" in keys:
            float_array.id = node.attributes['id'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)
        if node.firstChild:
            float_array.values = [float(f) for f in
                node.firstChild.nodeValue.split()[:count]]

    def do_geometry(self, node, parent):
        """Handle the <geometry> tag
        """
        geometry = dom.Geometry()
        parent.geometries.append(geometry)
        geometry.parent = parent
        keys = node.attributes.keys()
        if "name" in keys:
            geometry.name = node.attributes['name'].nodeValue
        if "id" in keys:
            geometry.id = node.attributes['id'].nodeValue

        for child in node.childNodes:
            self.parse(child, geometry)

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
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            idref.name = node.attributes['name'].nodeValue
        if "id" in keys:
            idref.id = node.attributes['id'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)
        if node.firstChild:
            idref.values = node.firstChild.nodeValue.split()[:count]

    def do_input(self, node, parent):
        """Handle the <input> tag
        """
        input = dom.Input()
        parent.inputs.append(input)
        input.parent = parent
        keys = node.attributes.keys()
        if "offset" in keys:
            input.offset = node.attributes['offset'].nodeValue
        if "semantic" in keys:
            input.semantic = node.attributes['semantic'].nodeValue
        if "source" in keys:
            input.source = node.attributes['source'].nodeValue
        if "set" in keys:
            input.offset = node.attributes['set'].nodeValue

    def do_int_array(self, node, parent):
        """Handle the <int_array> tag
        """
        int_array = dom.IntArray()
        parent.content_array = int_array
        int_array.parent = parent
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            int_array.name = node.attributes['name'].nodeValue
        if "id" in keys:
            int_array.id = node.attributes['id'].nodeValue
        if "minInclusive" in keys:
            int_array.minVal = node.attributes['minInclusive'].nodeValue
        if "maxInclusive" in keys:
            int_array.maxVal = node.attributes['maxInclusive'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)
        if node.firstChild:
            int_array.values = [int(f) for f in
                node.firstChild.nodeValue.split()[:count]]

    def do_keywords(self, node, parent):
        """Handle the <keywords> tag
        """
        if node.firstChild:
            parent.created = node.firstChild.nodeValue.split(" ")

    def do_library_animations(self, node, parent):
        """handle the <library_animations> tag
        """
        #cheat and just store the xml code for now
        animations = dom.LibraryAnimations()
        animations.collada_xml = node.toxml()
        parent.animations = animations

    def do_library_animation_clips(self, node, parent):
        """handle the <library_animation_clips> tag
        """
        #cheat and just store the xml code for now
        clips = dom.LibraryAnimationClips()
        clips.collada_xml = node.toxml()
        parent.clips = clips

    def do_library_cameras(self, node, parent):
        """handle the <library_cameras> tag
        """
        #cheat and just store the xml code for now
        cameras = dom.LibraryCameras()
        cameras.collada_xml = node.toxml()
        parent.cameras = cameras

    def do_library_controllers(self, node, parent):
        """handle the <library_controllers> tag
        """
        #cheat and just store the xml code for now
        controllers = dom.LibraryControllers()
        controllers.collada_xml = node.toxml()
        parent.controllers =  controllers

    def do_library_effects(self, node, parent):
        """handle the <library_effects> tag
        """
        #cheat and just store the xml code for now
        effects = dom.LibraryEffects()
        effects.collada_xml = node.toxml()
        parent.effects = effects

    def do_library_force_fields(self, node, parent):
        """handle the <library_force_fields> tag
        """
        #cheat and just store the xml code for now
        force_fields = dom.LibraryForceFields()
        force_fields.collada_xml = node.toxml()
        parent.force_fields = force_fields

    def do_library_geometries(self, node, parent):
        """handle the <library_geometries> tag
        """
        geometries = dom.LibraryGeometries()
        parent.geometries = geometries
        geometries.parent = parent
        for child in node.childNodes:
            self.parse(child, geometries)

    def do_library_images(self, node, parent):
        """handle the <library_images> tag
        """
        #cheat and just store the xml code for now
        images = dom.LibraryImages()
        images.collada_xml = node.toxml()
        parent.images = images

    def do_library_lights(self, node, parent):
        """handle the <library_lights> tag
        """
        #cheat and just store the xml code for now
        lights = dom.LibraryLights()
        lights.collada_xml = node.toxml()
        parent.lights = lights

    def do_library_materials(self, node, parent):
        """handle the <library_materials> tag
        """
        #cheat and just store the xml code for now
        materials = dom.LibraryMaterials()
        materials.collada_xml = node.toxml()
        parent.materials = materials

    def do_library_nodes(self, node, parent):
        """handle the <library_nodes> tag
        """
        #cheat and just store the xml code for now
        nodes = dom.LibraryNodes()
        nodes.collada_xml = node.toxml()
        parent.nodes = nodes

    def do_library_physics_materials(self, node, parent):
        """handle the <library_physics_materials> tag
        """
        #cheat and just store the xml code for now
        physics_materials = dom.LibraryPhysicsMaterials()
        physics_materials.collada_xml = node.toxml()
        parent.physics_materials = physics_materials

    def do_library_physics_models(self, node, parent):
        """handle the <library_physics_models> tag
        """
        #cheat and just store the xml code for now
        physics_models = dom.LibraryPhysicsModels()
        physics_models.collada_xml = node.toxml()
        parent.physics_models = physics_models

    def do_library_physics_scenes(self, node, parent):
        """handle the <library_physics_scenes> tag
        """
        #cheat and just store the xml code for now
        physics_scenes = dom.LibraryPhysicsScenes()
        physics_scenes.collada_xml = node.toxml()
        parent.physics_scenes = physics_scenes

    def do_library_visual_scenes(self, node, parent):
        """handle the <library_effects> tag
        """
        #cheat and just store the xml code for now
        visual_scenes = dom.LibraryVisualScenes()
        visual_scenes.collada_xml = node.toxml()
        parent.visual_scenes = visual_scenes

    def do_lines(self, node, parent):
        """Handle the <lines> tag
        """
        lines = dom.Lines()
        lines.parent = parent
        parent.lines.append(lines)
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            lines.name = node.attributes['name'].nodeValue
        if "material" in keys:
            lines.material = node.attributes['material'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)

        for child in node.childNodes:
            self.parse(child, lines)

    def do_linestrips(self, node, parent):
        """Handle the <linestrips> tag
        """
        linestripss = dom.Linestrips()
        linestrips.parent = parent
        parent.linestrips.append(linestrips)
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            linestrips.name = node.attributes['name'].nodeValue
        if "material" in keys:
            linestrips.material = node.attributes['material'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)

        for child in node.childNodes:
            self.parse(child, linestrips)


    def do_mesh(self, node, parent):
        """Handle the <mesh> tag
        """
        mesh = dom.Mesh()
        mesh.parent = parent
        parent.content = mesh

        for child in node.childNodes:
            self.parse(child, mesh)

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
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            name_array.name = node.attributes['name'].nodeValue
        if "id" in keys:
            name_array.id = node.attributes['id'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)
        if node.firstChild:
            name_array.values = node.firstChild.nodeValue.split()[:count]

    def do_p(self, node, parent):
        """Handle the <p> primitives tag
        """
        if node.firstChild:
            parent.primitives.append([ int(i) for i in
                node.firstChild.nodeValue.split()])

    def do_param(self, node, parent):
        """Handle the <param> tag
        """
        param = dom.Param()
        parent.params.append(param)
        param.parent = parent
        keys = node.attributes.keys()
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

        for child in node.childNodes:
            self.parse(child, polyhole)

    def do_polygons(self, node, parent):
        """Handle the <polygons> tag
        """
        poly = dom.Polygons()
        poly.parent = parent
        parent.polygons.append(ploy)
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            poly.name = node.attributes['name'].nodeValue
        if "material" in keys:
            poly.material = node.attributes['material'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)

        for child in node.childNodes:
            self.parse(child, poly)

    def do_polylist(self, node, parent):
        """Handle the <polylist> tag
        """
        poly = dom.Polylist()
        poly.parent = parent
        parent.polylists.append(poly)
        keys = node.attributes.keys()
        count = 0
        if "name" in keys:
            poly.name = node.attributes['name'].nodeValue
        if "material" in keys:
            poly.material = node.attributes['material'].nodeValue
        if "count" in keys:
            count = int(node.attributes['count'].nodeValue)

        for child in node.childNodes:
            self.parse(child, poly)

    def do_revision(self, node, parent):
        """Handle the <revision> tag
        """
        if node.firstChild:
            parent.revision = node.firstChild.nodeValue

    def do_scene(self, node, parent):
        """handle the <scene> tag
        """
        #cheat and just store the xml code for now
        scene = dom.Scene()
        scene.collada_xml = node.toxml()
        parent.scene = scene

    def do_source(self, node, parent):
        """Handle the <source> tag
        """
        source = dom.Source()
        source.parent = parent
        parent.sources.append(source)
        keys = node.attributes.keys()
        if "id" in keys:
            source.id = node.attributes['id'].nodeValue
        if "name" in keys:
            source.name = node.attributes['name'].nodeValue

        for child in node.childNodes:
            self.parse(child, source)

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
        tc = dom.TechniqueCommon()
        tc.parent = parent
        parent.technique_common = tc

        for child in node.childNodes:
            self.parse(child, tc)

    def do_title(self, node, parent):
        """Handle the <title> tag
        """
        if node.firstChild:
            parent.title = node.firstChild.nodeValue

    def do_unit(self, node, parent):
        """Handle the <unit> tag
        """
        keys = node.attributes.keys()
        if "name" in keys:
            parent.unit['name'] = node.attributes['name'].nodeValue
        if "meter" in keys:
            parent.unit['meter'] = node.attributes['meter'].nodeValue

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
        parent.vertices.append(vertices)
        vertices.parent = parent
        keys = node.attributes.keys()
        if "id" in keys:
            vertices.id = node.attributes['id'].nodeValue
        if "name" in keys:
            vertices.name = node.attributes['name'].nodeValue

        for child in node.childNodes:
            self.parse(child, vertices)


