import bpy
import os
from bpy.app.handlers import persistent
import xml.etree.ElementTree as ET
from . import pm_utils


@persistent
def create_project_path(scene):
    # Can't use in register function, as context is _RestrictContext until addons loaded
    addon_prefs = bpy.context.preferences.addons[__name__.split(".")[0]].preferences

    if not os.path.exists(addon_prefs.project_dir):
        os.makedirs(addon_prefs.project_dir)


@persistent
def load_projects(scene=None):
    """ Loads all projects.
    """
    pm_utils.load_projects()


def register():
    bpy.app.handlers.load_post.append(load_projects)
    bpy.app.handlers.load_post.append(create_project_path)


def unregister():
    bpy.app.handlers.load_post.remove(load_projects)
    bpy.app.handlers.load_post.remove(create_project_path)
