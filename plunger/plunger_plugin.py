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
"""Protocol for all plugins for Plunger

Plugins are expected to provide the "register" function.
There, they should register with the plugin registry.

If they register themselves as handling import, they need to provide the
importAsset() function.
If they register themselves as handling export, they need to provide the
exportAsset() function.
"""

class NotImplementedException(Exception):
    pass

class PlungerPlugin:
    def register(self, registry):
        """Register the plugin
        """
        raise NotImplementedException

    def importAsset(self, model, asset):
        """Import an asset in the format supported by the plugin
        """
        raise NotImplementedException

    def exportAsset(self, model, asset):
        """Export an asset in the format supported by the plugin
        """
        raise NotImplementedException

