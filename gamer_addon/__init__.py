# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 08:37:50 2012

@author: Tom Bartol <bartol@salk.edu>
"""

bl_info = {
    "name": "GAMer_2",
    "description": "GAMer: Geometry-preserving Adaptive Mesher",
    "author": "Zeyun Yu, Michael Holst, Johan Hake, and Tom Bartol",
    "version": (0,1,0),
    "blender": (2, 7, 5),
    "api": 55057,
    "location": "View3D > Add > Mesh",
    "warning": "",
    "wiki_url": "http://www.fetk.org/codes/gamer",
    "tracker_url": "https://github.com/mcellteam/gamer/issues",
    "category": "Mesh"}

# -------------------------------------------------------------------------- 
# ***** BEGIN GPL LICENSE BLOCK ***** 
# 
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; either version 2 
# of the License, or (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software Foundation, 
# Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA. 
# 
# ***** END GPL LICENCE BLOCK ***** 
# -------------------------------------------------------------------------- 

# from . import gamer_gui

if "bpy" in locals():
    print("Reloading GAMer")
    import imp
    imp.reload(gamer_gui)
else:
    print("Importing GAMer")
    from . import gamer_gui

# General import
import bpy
import sys
import os

def register():
    print("Registering GAMer...")
    bpy.utils.register_module(__name__)

    # Unregister and re-register panels to display them in order
    bpy.types.Scene.gamer = bpy.props.PointerProperty(
        type=gamer_gui.GAMerPropertyGroup)

    print("GAMer registered")


def unregister():
    bpy.utils.unregister_module(__name__)
    print("GAMer unregistered")


# for testing
if __name__ == '__main__':
    register()
