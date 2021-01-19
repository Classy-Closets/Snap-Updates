# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

from bpy.app.handlers import persistent
import os
from . import driver_functions
import inspect
import sys
import xml.etree.ElementTree as ET
from mv import utils


@persistent
def update_library_paths(scene=None):
    """ Sets the library paths from the Library XML File
    """
    wm = bpy.context.window_manager.mv
    if os.path.exists(utils.get_library_path_file()):
        tree = ET.parse(utils.get_library_path_file())
        root = tree.getroot()
        for elm in root.findall("LibraryPaths"):
            items = elm.getchildren()
            for item in items:
                if item.tag == "Packages":
                    elm_packages = item.getchildren()
                    for elm_package in elm_packages:
                        package_name = os.path.basename(os.path.normpath(elm_package.attrib["Name"]))
                        if os.path.exists(elm_package.attrib["Name"]) and package_name not in wm.library_packages:
                            package = wm.library_packages.add()
                            package.name = package_name
                            package.lib_path = elm_package.attrib["Name"]
                            package_items = elm_package.getchildren()
                            for pkg_item in package_items:
                                if pkg_item.tag == "Enabled":
                                    package.enabled = True if pkg_item.text == "True" else False
                if item.tag == "Modules":
                    if os.path.exists(str(item.text)):
                        wm.library_module_path = item.text
                    else:
                        wm.library_module_path = ""
                if item.tag == 'Assemblies':
                    if os.path.exists(str(item.text)):
                        wm.assembly_library_path = item.text
                    else:
                        wm.assembly_library_path = ""
                if item.tag == 'Objects':
                    if os.path.exists(str(item.text)):
                        wm.object_library_path = item.text
                    else:
                        wm.object_library_path = ""
                if item.tag == 'Materials':
                    if os.path.exists(str(item.text)):
                        wm.material_library_path = item.text
                    else:
                        wm.material_library_path = ""
                if item.tag == 'Worlds':
                    if os.path.exists(str(item.text)):
                        wm.world_library_path = item.text
                    else:
                        wm.world_library_path = ""

@persistent
def set_default_user_prefs(scene):
    """ Always set specific user preferences
    """
    bpy.context.user_preferences.system.use_scripts_auto_execute = True

@persistent
def load_driver_functions(scene):
    """ Load Default Drivers
    """
    for name, obj in inspect.getmembers(driver_functions):
        if name not in bpy.app.driver_namespace:
            bpy.app.driver_namespace[name] = obj

@persistent
def sync_spec_groups(scene):
    """ Syncs Spec Groups with the current library modules
    """
    bpy.ops.fd_material.reload_spec_group_from_library_modules()

@persistent
def load_library_modules(scene):
    """ Register Every Library Module on Startup
    """
    bpy.ops.snap.load_library_modules()

    if bpy.context.scene.mv.product_library_name not in bpy.context.window_manager.cabinetlib.lib_products:
        bpy.context.scene.mv.product_library_name = bpy.context.window_manager.cabinetlib.lib_products[0].name


# Register Startup Events
bpy.app.handlers.load_post.append(set_default_user_prefs)
bpy.app.handlers.load_post.append(load_driver_functions)
bpy.app.handlers.load_post.append(update_library_paths)
bpy.app.handlers.load_post.append(sync_spec_groups)
bpy.app.handlers.load_post.append(load_library_modules)


def register():
    import sys
    import re
    from . import properties

    #Register All Fluid Properties with Blender
    properties.register()
    
    # Look for eclipse debugging tools
    if os.path.exists(r'C:\Program Files\eclipse\plugins\org.python.pydev_2.8.2.2013090511\pysrc'):
        PYDEV_SOURCE_DIR = r'C:\Program Files\eclipse\plugins\org.python.pydev_2.8.2.2013090511\pysrc'
        if sys.path.count(PYDEV_SOURCE_DIR) < 1:
            sys.path.append(PYDEV_SOURCE_DIR)    
            
    elif os.path.exists(r'C:\Program Files (x86)\eclipse\plugins\org.python.pydev_2.8.2.2013090511\pysrc'):
        PYDEV_SOURCE_DIR = r'C:\Program Files (x86)\eclipse\plugins\org.python.pydev_2.8.2.2013090511\pysrc'
        if sys.path.count(PYDEV_SOURCE_DIR) < 1:
            sys.path.append(PYDEV_SOURCE_DIR) 
    #pydev 4.3, this could be changed to look for any version of pydev        
    elif os.path.exists(r'C:\Program Files\eclipse\plugins\org.python.pydev_4.3.0.201508182223\pysrc'):
        PYDEV_SOURCE_DIR = r'C:\Program Files\eclipse\plugins\org.python.pydev_4.3.0.201508182223\pysrc'
        if sys.path.count(PYDEV_SOURCE_DIR) < 1:
            sys.path.append(PYDEV_SOURCE_DIR)             

    
def unregister():
    pass
