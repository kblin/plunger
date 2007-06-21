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
"""A place where all the exporters and importers register.

The plunger main program will load all plugins and register them using
the register() function.
"""

import os
import sys

export_formats = {}
import_formats = {}

def register(module, format, does_import=False, does_export=False):
    """Register an import or export module.
    module would be the class that exports/imports data.
    format is a string representation of the format.
    does_import should be set to true of t
    """
    if does_import:
        import_formats[format]=module

    if does_export:
        export_formats[format]=module

def getExportFormats():
    """Get a list of exportable formats
    """
    return export_formats.keys()

def getImportFormats():
    """Get a list of importable formats
    """
    return import_formats.keys()

def getExporter(format):
    """Get an exporter for "format"
    """
    return export_formats[format]

def getImporter(format):
    """Get an importer for "format"
    """
    return import_formats[format]

def loadPlugins(plugin_dir):
    plugins = []
    for filename in os.listdir(plugin_dir):
        name, ext = os.path.splitext(filename)
        if ext == ".py" and name != "__init__":
            plugins.append(name)

    sys.path.append(plugin_dir)

    for plugin in plugins:
        module = __import__(plugin)
        register(module, module.format, module.does_import, module.does_export)

    sys.path.pop()
