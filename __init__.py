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
        maxlen=255)  # Max internal buffer length, longer would be clamped.

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
        from . import ter_importer
        return import_ter(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportTer.bl_idname, text="Terragen (.ter)")


def register():
    bpy.utils.register_class(ImportTer)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportTer)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
