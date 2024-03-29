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
"""The plunger file handler for writing information about the model to stdout.

The module supports export only, as there's no easy way to create a model from a
rough description. This is done by a different component called "artist".
"""

import sys

try:
    from plunger import toolbox
except ImportError:
    sys.path.append("..")
    import toolbox
    sys.path.pop()

format = "info"
ext = ""
needs_dir = False
does_import = False
does_export = True
version = "0.1.0"

def printDelimiter(out):
    begin_delim = "x"
    middle_delim = "-" * 40
    end_delim = "x"
    out.write("%s%s%s\n" % (begin_delim, middle_delim, end_delim))

def importAsset(model, asset):
    raise NotImplementedError

def exportAsset(model, asset):
    out = toolbox.writeAny(asset)
    printDelimiter(out)
    out.write("Plunger Info plugin version %s\n" % version)
    exportMeshInfo(model, out)
    out.close()

def exportMeshInfo(model, out):
    printDelimiter(out)
    out.write("Mesh Information:\n")
    out.write("Number of meshes in this model: %s\n" % model.getNumMeshes())

    i = 0
    for mesh in model.getMeshes():
        out.write("Handling mesh %s.\n" % i)
        out.write("Number of vertices: %s\n" % mesh.getNumVertices())
        for vertex in mesh.getVertices():
            out.write("pos:  point(%s, %s, %s)\n" % tuple(vertex.getPosition()))
            out.write("normal: vec(%s, %s, %s)\n" % tuple(vertex.getNormals()))
            out.write("uv:     vec(%s, %s)\n" % tuple(vertex.getUVCoords()))
            out.write("---\n")
        out.write("Number of faces: %s\n" % mesh.getNumFaces())
        for face in mesh.getFaces():
            out.write("face(%s" % face[0])
            for j in range(1,len(face)):
                out.write(",%s" % face[j])
            out.write(")\n")
        for material in mesh.getMaterials():
            out.write("Material: %s\n" % material.getPath())
        i += 1



