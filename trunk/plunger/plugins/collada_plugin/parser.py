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

    def do_keywords(self, node, parent):
        """Handle the <keywords> tag
        """
        if node.firstChild:
            parent.created = node.firstChild.nodeValue.split(" ")

    def do_modified(self, node, parent):
        """Handle the <modified> tag
        """
        if node.firstChild:
            parent.modified = node.firstChild.nodeValue

    def do_revision(self, node, parent):
        """Handle the <revision> tag
        """
        if node.firstChild:
            parent.revision = node.firstChild.nodeValue

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




