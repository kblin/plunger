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
"""The plunger file handler for the Collada format.

The module supports import and export.
"""

try:
    from plunger import toolbox
except ImportError:
    import sys
    sys.path.append("..")
    import toolbox
    sys.path.pop()

from collada_plugin.parser import Parser
from collada_plugin.generator import Generator

format = "collada"
ext = ".dae"
needs_dir = False
does_import = True
does_export = True

def importAsset(model, asset):
    """Import a collada .dae file.
    """
    from xml.dom import minidom
    sock = toolbox.openAny(asset)
    xmldom = minidom.parse(sock)
    sock.close()
    p = Parser(model)
    p.parse(xmldom)

def exportAsset(model, asset):

    g = Generator()
    g.generate(model)

    import sys
    file = None
    try:
        file = toolbox.writeAny(asset)
    except IOError:
        print "Failed to open '%s' for writing" % asset
        sys.exit(1)

    try:
        file.write(g.toxml())
        file.close()
    except IOError:
        print "Writing '%s' failed." % asset
        sys.exit(1)


