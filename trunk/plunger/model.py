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
"""The in-memory model for all assets.
This is a Collada DOM for now.
"""

class Model:
    def __init__(self, registry, input_asset, output_asset, input_format,
            output_format):
        self.registry = registry
        self.dom = None

        importer = registry.getImporter(input_format)
        importer.importAsset(self, input_asset)

        exporter = registry.getExporter(output_format)
        exporter.exportAsset(self, output_asset)


