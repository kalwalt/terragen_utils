'''
Copyright (C) 2017 Walter Perdan
info@kalwaltart.it

Created by WALTER PERDAN

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import bpy
import sys
import string
import struct
import os  # glob
from os import path, name, sep
from math import *
import bmesh
import time
from .ter_utils import get_headers
from .ter_utils import get_path


def import_ter(operator, context, filepath, triangulate, custom_properties,
               custom_scale, baseH, heightS, shiftX, shiftY):
    start_time = time.process_time()

    if filepath:
        args = get_headers(filepath)
        size = args[0]
        xpts = args[1]
        ypts = args[2]
        scalx = args[3]
        scaly = args[4]
        scalz = args[5]
        crad = args[6]
        crvm = args[7]
        heightscale = args[8]
        baseheight = args[9]
        ter = args[10]

        if xpts == 0:
            xpts = size + 1
        if ypts == 0:
            ypts = size + 1

        print('\n-----------------\n')
        print('size is: {0} x {0}'.format(size))
        print('scale is: {0}, {1}, {2}'.format(scalx, scaly, scalz))
        print('number x points are: ', xpts)
        print('number y points are: ', ypts)
        print('baseheight is: ', baseheight)
        print('heightscale is: ', heightscale)
        print('\n-----------------\n')

        terrainName = bmesh.new()
        # Create vertices
        # ---------------
        # read them all...
        x0 = 0.0
        y0 = 0.0
        z0 = 0.0
        for y in range(0, ypts):
            for x in range(0, xpts):
                (h,) = struct.unpack('h', ter.read(2))
                # adding custom values
                if custom_properties is True:
                    x0 = x * custom_scale[0]
                    y0 = y * custom_scale[1]
                    baseheight = baseH
                    heightscale = heightS
                    z0 = custom_scale[2] * (baseheight + (h * heightscale / 65536.0))
                else:
                    # from VTP SetFValue(i, j, scale.z * (BaseHeight + ((float)svalue * HeightScale / 65536.0f)));
                    # see: https://github.com/kalwalt/terragen_utils/issues/2
                    x0 = x * scalx + shiftX
                    y0 = y * scaly + shiftY
                    z0 = scalz * (baseheight + (h * heightscale / 65536.0))

                terrainName.verts.new((x0, y0, z0))

                xmax = x + 1
                ymax = y + 1

        ter.close()

        # Create faces
        # ------------

        for y in range(0, ymax - 1):
            for x in range(0, xmax - 1):

                a = x + y * (ymax)

                terrainName.verts.ensure_lookup_table()

                v1 = terrainName.verts[a]
                v2 = terrainName.verts[a + ymax]
                v3 = terrainName.verts[a + ymax + 1]
                v4 = terrainName.verts[a + 1]

                terrainName.faces.new((v1, v2, v3, v4))

        if triangulate is True:
            args = bmesh.ops.triangulate(terrainName, faces=terrainName.faces)
            print('Terrain mesh triangulated!')

        mesh = bpy.data.meshes.new("Terrain_mesh")
        terrainName.to_mesh(mesh)
        terrainName.free()

        # Add the mesh to the scene
        scene = bpy.context.scene
        obj = bpy.data.objects.new("Terrain_obj", mesh)
        scene.objects.link(obj)
        print('Terrain imported in %.4f sec.' % (time.process_time() - start_time))

    return {'FINISHED'}


def import_multi(operator, context, filepath, num_tiles, name_file):
    start_time = time.process_time()

    if filepath:
        shift = 0.0
        args = get_headers(filepath)
        size = args[0]
        scalx = args[3]
        scaly = args[4]
        scalz = args[5]
        print('scalx is: ', args[3])
        shiftX = 0
        shiftY = 0
        ntiles = 2
        shift = size * scalx
        print('shift before is: ', shift)
        for x in range(0, num_tiles):
            if x == 0:
                shiftX = 0
            else:
                shiftX += shift
            for y in range(0, num_tiles):
                print('shiftX is: ', shiftX)
                if y == 0:
                    shiftY = 0
                else:
                    shiftY += shift
                path = get_path(filepath, name_file)
                final_path = path + str(name_file) + '_x' + str(x) + '_y' + str(y) + '.ter'
                print('final path: ', final_path)
                import_ter(operator, context, final_path, triangulate=False, custom_properties=False,
                       custom_scale=1, baseH=0, heightS=0, shiftX=shiftX, shiftY=shiftY)
                print('shiftY is: ', shiftY)

        print('Terrain imported in %.4f sec.' % (time.process_time() - start_time))
    return {'FINISHED'}

    if __name__ == "__main__":
        register()
