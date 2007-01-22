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
"""Core functionality of the plunger library
Used to provide separation from the text user interface
"""

import registry
import dom

model = dom.getModel()

def loadPlugins(plugindir="plugins"):
    registry.loadPlugins(plugindir)

def getImportFormats():
    return registry.getImportFormats()

def getExportFormats():
    return registry.getExportFormats()

def importAsset(input_asset, input_format):
    importer = registry.getImporter(input_format)
    importer.importAsset(model, input_asset)

def exportAsset(output_asset, output_format):
    exporter = registry.getExporter(output_format)
    exporter.exportAsset(model, output_asset)

def convert(input_asset, input_format, output_asset, output_format):
    importAsset(input_asset, input_format)
    exportAsset(output_asset, output_format)

