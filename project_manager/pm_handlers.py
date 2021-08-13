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
    bl_path = bpy.data.filepath.split(os.path.sep)
    current_project_name = ''
    if bl_path[0] != '' and bl_path[-3] == 'SNaP Projects':
        current_project_name = bl_path[-2]
    project_index = 0

    wm = bpy.context.window_manager.sn_project
    proj_dir = pm_utils.get_project_dir()
    if os.path.exists(proj_dir):
        for dir_entry in os.scandir(proj_dir):
            if dir_entry.is_dir():
                for ndir_entry in os.scandir(dir_entry.path):
                    if ndir_entry.is_file():
                        _, ext = os.path.splitext(ndir_entry)
                        if ext == ".ccp":
                            tree = ET.parse(ndir_entry.path)
                            root = tree.getroot()

                            for elm in root.findall("ProjectInfo"):
                                items = list(elm)

                                for item in items:
                                    if item.tag == 'name':
                                        proj_name = item.text

                            proj = wm.projects.add()
                            proj.init(proj_name)
                            if proj_name == current_project_name:
                                wm.project_index = project_index
                                

                            for elm in root.findall("Rooms"):
                                for sub_elm in elm:
                                    rel_path = os.path.join(*sub_elm.get("path").split(os.sep)[-2:])
                                    proj_dir = pm_utils.get_project_dir()
                                    room_filepath = os.path.join(proj_dir, rel_path)
                                    if(sub_elm.get("category")):
                                        proj.add_room_from_file(sub_elm.get("name"),
                                                                sub_elm.get("category"),
                                                                room_filepath, project_index=project_index)
                                    else:
                                        proj.add_room_from_file(sub_elm.get("name"),
                                                                "No Category Selected",
                                                                room_filepath, project_index=project_index)
                            
                            project_index += 1


def register():
    bpy.app.handlers.load_post.append(load_projects)
    bpy.app.handlers.load_post.append(create_project_path)


def unregister():
    bpy.app.handlers.load_post.remove(load_projects)
    bpy.app.handlers.load_post.remove(create_project_path)
