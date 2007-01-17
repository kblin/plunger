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
"""The plunger file handler for the MD3 format.

The module supports export only for now.
"""
format = "md3"
extension = ".md3"
needs_dir = False
does_export = True
does_import = False

# Info from http://icculus.org/homepages/phaethon/q3a/formats/md3format.html
MD3_IDENT = "IDP3"
MD3_VERSION = 15

def importAsset(model, asset):
    raise NotImplementedError

def exportAsset(model, asset):
    print "Not yet implemented, sorry."



