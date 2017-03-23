import bpy
import sys
import string
import struct
import os  # glob
from os import path, name, sep
from math import *
import bmesh
import time
import re


def get_headers(filepath):
    # variables initialization
    size = 0
    xpts = 0
    ypts = 0
    scalx = 0
    scaly = 0
    scalz = 0
    crad = 0
    crvm = 0
    heightscale = 0
    baseheight = 0

    try:
        ter = open(filepath, 'rb')
        print('start...\n')
    except IOError:
        if terfile == "":
            print("Terragen ter file does not exist!")
            Exit()
        else:
            print(terfile + " does not exist!")
    else:

        if ter.read(8).decode() == "TERRAGEN":

            if ter.read(8).decode() == "TERRAIN ":

                print("Terragen terrain file: found -> continue...\n")
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
                    (size,) = struct.unpack('h', ter.read(2))
                    # garbage = ter.read(2).decode()
                    garbage = ter.read(2)
                    print('garbage :', garbage)

                if totest == 'XPTS':
                    print('reading XPTS')
                    (xpts,) = struct.unpack('h', ter.read(2))
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
    return size, xpts, ypts, scalx, scaly, scalz, crad, crvm, heightscale, baseheight, ter


def get_path(filepath, name_file):
    indx_path = filepath.find(name_file)
    path = filepath[:indx_path]
    print('path is: ', path)
    print('filepath is : ', filepath)
    return path
