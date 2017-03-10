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
from .ter_importer import import_ter
# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty
from bpy.types import Operator


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


class ImportTer(Operator, ImportHelper):
    """Operator to import .ter Terragen files into blender as obj"""
    bl_idname = "import_ter.data"
    bl_label = "Import .ter"

    # ImportHelper mixin class uses this
    filename_ext = ".ter"

    filter_glob = StringProperty(
        default="*.ter",
        options={'HIDDEN'},
        maxlen=255)  # Max internal buffer length, longer would be clamped.

    triangulate = BoolProperty(
        name="Triangulate",
        description="triangulate the terrain mesh",
        default=False)

    custom_properties = BoolProperty(
        name="CustomProperties",
        description="set custom properties of the terrain: size, scale,\
        baseheight, heightscale",
        default=False)
    '''
    custom_size = IntProperty(
        name="CustomSize",
        description="set a custom size of the terrain",
        default=128)
    '''
    custom_scale = FloatProperty(
        name="CustomScale",
        description="set a custom scale of the terrain",
        default=128.0)

    baseH = IntProperty(
        name="BaseHeight",
        description="set the baseheight of the terrain",
        default=0)

    heightS = IntProperty(
        name="HeightScale",
        description="set the maximum height of the terrain",
        default=100)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'triangulate')
        layout.prop(self, 'custom_properties')
        if self.custom_properties is True:
            layout.prop(self, 'custom_scale')
            layout.prop(self, 'baseH')
            layout.prop(self, 'heightS')

    def execute(self, context):
        return import_ter(context, self.filepath, self.triangulate,
                          self.custom_properties, self.custom_scale,
                          self.baseH, self.heightS)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportTer.bl_idname, text="Terragen (.ter)")


'''
def menu_func_export(self, context):
    self.layout.operator(ImportTer.bl_idname, text="Terragen (.ter)")
'''


def register():
    bpy.utils.register_class(ImportTer)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
    # bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ImportTer)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    # bpy.types.INFO_MT_file_export.append(menu_func_export)


if __name__ == "__main__":
    register()
