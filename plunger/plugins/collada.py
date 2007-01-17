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
    from plunger_plugin import PlungerPlugin
except ImportError:
    import sys
    sys.path.append("..")
    from plunger_plugin import PlungerPlugin
    sys.path.pop()

def register(registry):
    c = Collada()
    c.register(registry)

class Collada(PlungerPlugin):
    def __init__(self):
        self.format = "collada"
        self.ext = ".dae"
        self.needs_dir = False

    def register(self, registry):
        registry.register(self, self.format, True, True)

    def importAsset(self, model, asset):
        """Import a collada .dae file.
        As this corresponds to the internal data model, nothing much is needed.
        """
        from xml.dom import minidom
        try:
            import toolbox
        except ImportError:
            import sys
            sys.path.append("..")
            import toolbox
            sys.path.pop()

        sock = toolbox.openAny(asset)
        model.dom = minidom.parse(sock)
        sock.close()

    def exportAsset(self, model, asset):
        import sys
        file = None
        try:
            file = open(asset, "w")
        except IOError:
            print "Failed to open '%s' for writing" % asset
            sys.exit(1)

        try:
            file.write(model.dom.toxml())
            file.close()
        except IOError:
            print "Writing '%s' failed." % asset
            sys.exit(1)


