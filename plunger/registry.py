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

class Registry:
    def __init__(self):
        self.export_formats = {}
        self.import_formats = {}

    def register(self, module, format, does_import=False, does_export=False):
        """Register an import or export module.
        module would be the class that exports/imports data.
        format is a string representation of the format.
        does_import should be set to true of t
        """
        if does_import:
            self.import_formats[format]=module

        if does_export:
            self.export_formats[format]=module

    def getExportFormats(self):
        """Get a list of exportable formats
        """
        return self.export_formats.keys()

    def getImportFormats(self):
        """Get a list of importable formats
        """
        return self.import_formats.keys()

    def getExporter(self, format):
        """Get an exporter for "format"
        """
        return self.export_formats[format]

    def getImporter(self, format):
        """Get an importer for "format"
        """
        return self.import_formats[format]

