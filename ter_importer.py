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

bl_info = {
    "name": "Terragen utils",
    "description": "addon to import/export .ter files",
    "author": "Walter Perdan",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "File > Import-Export",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Import-Export"}


def import_ter(context, filepath):

    global size

    xpts = 0
    ypts = 0
    scalx = 0
    scaly = 0
    scalz = 0
    crad = 0
    crvm = 0
    heightscale = 0
    baseheight = 0

    size = 0
    try:
        ter = open(filepath, 'rb')
        print('start...')
    except IOError:
        if terfile == "":
            print("Terragen ter file does not exist!")
            Exit()
        else:
            print(terfile + " does not exist!")
    else:

        if ter.read(8).decode() == "TERRAGEN":

            if ter.read(8).decode() == "TERRAIN ":

                print("Terragen terrain file: continue")
            else:
                print("TERRAIN keyword not found")
                return None
        else:
            print("TERRAGEN keyword not found")
            return None

        keys = ['SIZE', 'XPTS', 'YPTS', 'SCAL', 'CRAD', 'CRVM', 'ALTW']

        totest = ter.read(4).decode()

        while 1:
            if totest in keys:
                if totest == "SIZE":
                    print('reading SIZE')
                    # (size,) = struct.unpack('h', ter.read(2))
                    size = struct.unpack('h', ter.read(2))
                    garbage = ter.read(2).decode()

                if totest == 'XPTS':
                    print('reading XPTS')
                    (xpts,) = struct.unpack('h', ter.read(2))
                    # xpts = struct.unpack('h', ter.read(2))
                    garbage = ter.read(2).decode()

                if totest == 'YPTS':
                    print('reading YPTS')
                    (ypts,) = struct.unpack('h', ter.read(2))
                    garbage = ter.read(2).decode()

                if totest == 'SCAL':
                    print('reading SCAL')
                    (scalx,) = struct.unpack('f', ter.read(4))
                    (scaly,) = struct.unpack('f', ter.read(4))
                    (scalz,) = struct.unpack('f', ter.read(4))

                if totest == 'CRAD':
                    print('reading CRAD')
                    (crad,) = struct.unpack('f', ter.read(4))

                if totest == 'CRVM':
                    print('reading CRVM')
                    (crvm,) = struct.unpack('H', ter.read(2))
                    garbage = ter.read(2).decode()

                if totest == 'ALTW':
                    print('reading ALTW')
                    (heightscale,) = struct.unpack('h', ter.read(2))
                    (baseheight,) = struct.unpack('h', ter.read(2))
                    break
                totest = ter.read(4).decode()
            else:
                break

        if xpts == 0:
            xpts = size[0] + 1
        if ypts == 0:
            ypts = size[0] + 1

        print('x points are: ', xpts)
        print('y points are: ', ypts)
        print('baseheight is: ', baseheight)
        print('heightscale is: ', heightscale)

        terrainName = bmesh.new()
        # Create vertices
        # ---------------
        # read them all...
        for y in range(0, ypts):
            for x in range(0, xpts):
                (h,) = struct.unpack('h', ter.read(2))

                z = baseheight + h * heightscale / 65536.0
                terrainName.verts.new((x, y, z))

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

        mesh = bpy.data.meshes.new("Terrain_mesh")
        terrainName.to_mesh(mesh)
        terrainName.free()

        # Add the mesh to the scene
        scene = bpy.context.scene
        obj = bpy.data.objects.new("Terrain_obj", mesh)
        scene.objects.link(obj)
        print('Terrain imported!')

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportTer(Operator, ImportHelper):
    """Operator to import .ter Terragen files into blender as obj"""
    bl_idname = "import_ter.data"
    bl_label = "Import .ter"

    # ImportHelper mixin class uses this
    filename_ext = ".ter"

    filter_glob = StringProperty(
            default="*.ter",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    '''
    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = BoolProperty(
            name="Example Boolean",
            description="Example Tooltip",
            default=True,
            )

    type = EnumProperty(
            name="Example Enum",
            description="Choose between two items",
            items=(('OPT_A', "First Option", "Description one"),
                   ('OPT_B', "Second Option", "Description two")),
            default='OPT_A',
            )
    '''

    def execute(self, context):
        return import_ter(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportTer.bl_idname, text="Terragen Import Operator")


def register():
    bpy.utils.register_class(ImportTer)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportTer)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
