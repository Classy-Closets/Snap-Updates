
bl_info = {
    "name": "SNaP",
    "author": "Ryan Montes",
    "version": (0, 0, 2),
    "blender": (2, 7, 8),
    "location": "Tools Shelf",
    "description": "SNaP",
    "warning": "",
    "wiki_url": "",
    "category": "SNaP"
}


import bpy
import sqlite3
from sqlite3 import Error
import os
import pathlib
import time
from bpy.app.handlers import persistent
from . import snap_csv
from . import snap_xml
from . import snap_import
from . import snap_export
from . import closet_materials
from . import closet_materials_ui
from . import closet_materials_ops
from . import addon_updater_ops
# - FOR CUSTOM PROGRESS BAR
# from tkinter import *
# from tkinter import ttk


BL_DIR = os.path.dirname(bpy.app.binary_path)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(DIR_PATH, "Snap.db")
CSV_DIR_PATH = os.path.join(DIR_PATH, "db_init")
CSV_PATH = os.path.join(CSV_DIR_PATH, "CCItems.csv")
EDGE_TYPES_CSV_PATH = os.path.join(CSV_DIR_PATH, "EdgeTypes.csv")
MAT_TYPES_CSV_PATH = os.path.join(CSV_DIR_PATH, "MaterialTypes.csv")
CT_DIR = os.path.join(CSV_DIR_PATH, "Countertops")
GLAZE_COLORS_CSV_PATH = os.path.join(CSV_DIR_PATH, "GlazeColors.csv")
GLAZE_STYLES_CSV_PATH = os.path.join(CSV_DIR_PATH, "GlazeStyles.csv")
DOOR_COLORS_CSV_PATH = os.path.join(CSV_DIR_PATH, "ModernoDoorColors.csv")
GLASS_COLORS_CSV_PATH = os.path.join(CSV_DIR_PATH, "GlassColors.csv")
SLIDE_TYPES_CSV_PATH = os.path.join(CSV_DIR_PATH, "DrawerSlideTypes.csv")
ITEMS_TABLE_NAME = "CCItems"
EDGE_TYPE_TABLE_NAME = "EdgeTypes"
MAT_TYPE_TABLE_NAME = "MaterialTypes"
SLIDE_TYPE_TABLE_NAME = "SlideTypes"
DRAWER_SLIDE_DIR = os.path.join(CSV_DIR_PATH, "Drawer Slides")


def connect_db():
    try:
        conn = sqlite3.connect(DB_PATH)
    except Error as e:
        print(e)
        return{'FINISHED'}

    return conn


def query_db(SQL):

    try:
        conn = connect_db()
    except Error as e:
        print(e)
        return{'FINISHED'}  

    cur = conn.cursor()
    cur.execute(SQL)
    rows = cur.fetchall()
    conn.close()

    return rows


class PREFS_Snap(bpy.types.AddonPreferences):
    bl_idname = __name__

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )

    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )

    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=1,
        min=0,
        max=59
    )

    default_csv_path = bpy.props.StringProperty(
        name="Defalut CSV Filepath",
        subtype='FILE_PATH',
        default=CSV_PATH
    )

    def draw(self, context):
        layout = self.layout

        addon_updater_ops.update_settings_ui(self,context)
        box = layout.box()
        box.prop(self, "default_csv_path", text="Default CSV Filepath")


@bpy.app.handlers.persistent
def load_materials_from_db(scene=None):
    if "snap_db" in bpy.context.user_preferences.addons.keys():
        import time
        time_start = time.time()
        addon_prefs = bpy.context.user_preferences.addons[__name__].preferences
        filename = os.path.basename(addon_prefs.default_csv_path)
        filepath = addon_prefs.default_csv_path
        bpy.ops.snap_db.import_csv('EXEC_DEFAULT', filename=filename, filepath=filepath)
        print("load_materials_from_db Finished: %.4f sec" % (time.time() - time_start))

    
bpy.app.handlers.load_post.append(load_materials_from_db) 

@bpy.app.handlers.persistent
def assign_materials(scene=None):
    bpy.ops.db_materials.assign_materials()

bpy.app.handlers.save_pre.append(assign_materials)       

@bpy.app.handlers.persistent
def assign_material_pointers(scene=None):
    if "snap_db" in bpy.context.user_preferences.addons.keys():
        bpy.ops.db_materials.assign_materials(only_update_pointers=True)   
 
bpy.app.handlers.load_post.append(assign_material_pointers)    


def register():
    addon_updater_ops.register(bl_info)
    bpy.utils.register_class(PREFS_Snap)
    snap_import.register()
    snap_export.register()
    closet_materials.register()
    closet_materials_ui.register()
    closet_materials_ops.register()


def unregister():
    addon_updater_ops.unregister()
    bpy.utils.unregister_class(PREFS_Snap)
    snap_import.unregister()
    snap_export.unregister()
    closet_materials.unregister()
    closet_materials_ui.unregister()
    closet_materials_ops.unregister()

if __name__ == "__main__":
    register()
