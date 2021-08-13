bl_info = {
    "name": "SNaP",
    # "author": "Ryan Montes",
    "version": (2, 0, 0),
    "blender": (2, 93, 0),
    "location": "Tools Shelf",
    "description": "SNaP",
    "warning": "",
    "wiki_url": "",
    "category": "",
}

import os
import sys

from bpy.utils import previews

from . import sn_paths
from . import sn_props
from . import sn_import
from . import sn_handlers
from . import material_manager
from . import room_builder
from . import project_manager
from . import ui
from . import ops
from . import views
from . import library_manager

from snap.libraries import closets
from snap.libraries import doors_and_windows


snap_icons = None
python_lib_path = os.path.join(os.path.dirname(__file__), "python_lib")
sys.path.append(python_lib_path)

modules = (
    sn_handlers,
    sn_props,
    sn_import,
    closets,
    doors_and_windows,
    material_manager,
    room_builder,
    project_manager,
    ui,
    ops,
    views,
    library_manager
)


def register():

    for mod in modules:
        mod.register()

    global snap_icons
    snap_icons = previews.new()
    icons_dir = sn_paths.ICON_DIR

    for icon in os.listdir(icons_dir):
        name, ext = os.path.splitext(icon)
        snap_icons.load(name, os.path.join(icons_dir, icon), 'IMAGE')


def unregister():

    for mod in reversed(modules):
        mod.unregister()

    global snap_icons
    previews.remove(snap_icons)
