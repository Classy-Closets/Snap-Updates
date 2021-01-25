
bl_info = {
    "name": "SNaP",
    "author": "Ryan Montes",
    "version": (1, 2, 3),
    "blender": (2, 7, 8),
    "location": "Tools Shelf",
    "description": "SNaP",
    "warning": "",
    "wiki_url": "",
    "category": "SNaP"
}


import bpy
import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import os
import shutil
import stat
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
from . import room_builder
from . import snap_ops
from . import fd_projects
from . import lib_manager
from . import fd_2dviews

# - FOR CUSTOM PROGRESS BAR
# from tkinter import *
# from tkinter import ttk


BL_DIR = os.path.dirname(bpy.app.binary_path)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(DIR_PATH, "Snap.db")
MATERIALS_DIR = os.path.join(DIR_PATH, "materials")
CSV_DIR_PATH = os.path.join(DIR_PATH, "db_init")
CSV_PATH = os.path.join(CSV_DIR_PATH, "CCItems.csv")
EDGE_TYPES_CSV_PATH = os.path.join(CSV_DIR_PATH, "EdgeTypes.csv")
MAT_TYPES_CSV_PATH = os.path.join(CSV_DIR_PATH, "MaterialTypes.csv")
OS_MAT_COLORS_CSV_PATH = os.path.join(CSV_DIR_PATH, "OversizeMaterialColors.csv")
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
UPDATE_USER = "CCDevNelson"
UPDATE_REPO = "Snap-Updates"
DEV_TOOLS_AVAILABLE = False
INFO_SITE_URL = "https://ccdevnelson.github.io/SNaP-Dev/"

try:
    from . import developer_utils
    DEV_TOOLS_AVAILABLE = True    
except ImportError:
    pass
else:
    pass


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


class OBJECT_PT_UpdaterPanel(bpy.types.Panel):
    """Panel to demo popup notice and ignoring functionality"""
    bl_label = "SNaP Updater"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80) else 'UI'
    bl_context = "objectmode"
    bl_category = "SNaP"

    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='LOAD_FACTORY')        

    def draw(self, context):
        layout = self.layout

        # Call to check for update in background
        # note: built-in checks ensure it runs at most once
        # and will run in the background thread, not blocking
        # or hanging blender
        # Internally also checks to see if auto-check enabled
        # and if the time interval has passed
        # addon_updater_ops.check_for_update_background()
        box = layout.box()     
        box.label("SNaP Version: {}.{}.{}".format(bl_info['version'][0], bl_info['version'][1], bl_info['version'][2]))
        addon_updater_ops.update_notice_box_ui(self, context)


class PREFS_Snap(bpy.types.AddonPreferences):
    bl_idname = __name__

    debug_mode = bpy.props.BoolProperty(
        name="Debug Mode",
        description="If enabled, run in debug mode",
        default=False,
    )

    debug_updater = bpy.props.BoolProperty(
        name="Debug Updater",
        description="If enabled, run updater in debug mode",
        default=False
    )

    debug_export = bpy.props.BoolProperty(
        name="Debug XML Export",
        description="If enabled, run XML export in debug mode",
        default=False,
    )

    expand_dev_panel = bpy.props.BoolProperty(
        name="Expand Development Panel",
        description="Expand Development panel for advanced options",
        default=False,
    )

    use_adv_options = bpy.props.BoolProperty(
        name="SNaP Advanced options",
        description="Use advanced options",
        default=False,
    )

    fake_install = bpy.props.BoolProperty(
        name="Updater - Fake Install",
        description="For debugging, 'pretend' to install an update to test reloading conditions",
        default=False,
    )

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
        default=0,
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

    location_code = bpy.props.EnumProperty(
        name="Location Code",
        items=closet_materials.enum_location_code
    )

    enable_lib_manager = bpy.props.BoolProperty(
        name="Enable Library Manager",
        description="If enabled, show library manager panel",
        default=False,
    )    

    def draw(self, context):
        project_prefs = bpy.context.user_preferences.addons["fd_projects"].preferences
        layout = self.layout

        box = layout.box()
        row = box.row()
        split = row.split(percentage=0.5)
        row = split.row()
        row.label("Location Code:")
        row.prop(self, "location_code", text="")
        row = split.row()
        row.label("Designer ID:")
        row.prop(project_prefs, "designer_id", text="")
        box.prop(project_prefs, "project_dir", text="Projects Directory")

        row = layout.row(align=True)
        row.prop(
            self,
            "expand_dev_panel",
            text="",
            icon='TRIA_DOWN' if self.expand_dev_panel else 'TRIA_RIGHT',
            emboss=False)
        row.prop(self, "use_adv_options", text="")
        row.label("SNaP Advanced options")

        if self.expand_dev_panel:
            box = layout.box()
            box.label(text="Library Manager")
            box.enabled = self.use_adv_options
            row = box.row()
            row.prop(self, "enable_lib_manager")

            if DEV_TOOLS_AVAILABLE:
                box = layout.box()
                box.label(text="Debug Settings")                
                box.enabled = self.use_adv_options
                row = box.row()
                row.prop(self, "debug_mode")
                row.prop(self, "debug_updater")
                row.prop(self, "fake_install")
             
            addon_updater_ops.update_settings_ui(self,context)


bpy.utils.register_class(PREFS_Snap)

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

def del_dir(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

@bpy.app.handlers.persistent
def check_for_update(scene=None):
    source_dir = os.path.join(os.path.dirname(__file__),"snap_db_updater","source")
    staging_dir = os.path.join(os.path.dirname(__file__),"snap_db_updater","update_staging")
    update_dirs = [source_dir, staging_dir]

    for dir_path in update_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path, onerror=del_dir)

    if "snap_db" in bpy.context.user_preferences.addons.keys():
        addon_updater_ops.check_for_update_background()   
 
bpy.app.handlers.load_post.append(check_for_update)

@bpy.app.handlers.persistent
def check_and_remove_prebuilts(scene=None):
    '''Ensure pre-builts have been properly removed.
    '''
    lib_cc_dir = os.path.join(os.path.dirname(__file__),"library_scripts/Library-Classy_Closets/")
    closet_prod_dir = os.path.join(lib_cc_dir, "products/Closets/")

    assembly_paths = [
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","1 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","2 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","3 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","4 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","5 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","6 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","7 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","8 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","9 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Add Pards","9 Hanging Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","1 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","2 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","3 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","4 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","5 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","6 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","7 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","8 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Uppers","9 Upper Opening.blend"),
        os.path.join(closet_prod_dir, "Closet Products - Basic","Toe Kick.blend")
    ]

    for path in assembly_paths:
        if os.path.exists(path):
            os.remove(path)
 
bpy.app.handlers.load_post.append(check_and_remove_prebuilts)

@bpy.app.handlers.persistent
def refresh_filebrowser(scene=None):
    if not bpy.app.background:
        if "snap_db" in bpy.context.user_preferences.addons.keys():
            wm = bpy.context.window_manager
            mv = bpy.context.scene.mv
            lib = wm.cabinetlib.lib_products[mv.product_library_name]
            categories =  os.listdir(lib.lib_path)

            for category in categories:
                cat_path = os.path.join(lib.lib_path,category)
                if os.path.isdir(cat_path):
                    if category == bpy.context.scene.mv.product_category_name:
                        for window in bpy.context.window_manager.windows:
                            screen = window.screen
                            for area in screen.areas:
                                if area.type == 'FILE_BROWSER':
                                    override = bpy.context.copy()
                                    override['window'] = window
                                    override['screen'] = screen
                                    override['area'] = area
                                    bpy.ops.snap.change_category(override,category_name=category)  
 
bpy.app.handlers.load_post.append(refresh_filebrowser)


@persistent
def load_projects(scene=None):
    """ Loads all projects.
    """
    if 'fd_projects' in bpy.context.user_preferences.addons.keys():
        wm = bpy.context.window_manager.fd_project
        proj_dir = bpy.context.user_preferences.addons['fd_projects'].preferences.project_dir

        if os.path.exists(proj_dir):
            for dir_entry in os.scandir(proj_dir):
                if dir_entry.is_dir():
                    for ndir_entry in os.scandir(dir_entry.path):
                        if ndir_entry.is_file():
                            exts = []
                            exts = ndir_entry.name.split(".")
                            #Filter out files with multiple extensions
                            if len(exts) == 2:
                                ext = exts[-1]
                                if ext == "ccp":
                                    tree = ET.parse(ndir_entry.path)
                                    root = tree.getroot()

                                    for elm in root.findall("ProjectInfo"):
                                        items = list(elm)

                                        for item in items:
                                            if item.tag == 'name':
                                                proj_name = item.text
                                    
                                    proj = wm.projects.add()
                                    proj.init(proj_name)

                                    for elm in root.findall("Rooms"):
                                        for sub_elm in elm:
                                            if(sub_elm.get("category")):
                                                proj.add_room_from_file(sub_elm.get("name"),sub_elm.get("category"), sub_elm.get("path"))
                                            else:
                                                proj.add_room_from_file(sub_elm.get("name"),"No Category Selected", sub_elm.get("path"))

bpy.app.handlers.load_post.append(load_projects)


# Register the OpenGL Call back for dims
bpy.types.SpaceView3D.draw_handler_add(fd_2dviews.opengl_dim.draw_opengl, (None, None), 'WINDOW', 'POST_PIXEL')


classes = (
	OBJECT_PT_UpdaterPanel,
)


def register():
    prefs = bpy.context.user_preferences.addons[__name__].preferences
    addon_updater_ops.register(bl_info, UPDATE_USER, UPDATE_REPO, None, prefs.fake_install)
    snap_import.register()
    snap_export.register()
    closet_materials.register()
    closet_materials_ui.register()
    closet_materials_ops.register()
    room_builder.register()
    snap_ops.register()
    fd_projects.register()
    fd_2dviews.register()
    lib_manager.register()

    for cls in classes:
        addon_updater_ops.make_annotations(cls) # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)    


def unregister():
    addon_updater_ops.unregister()
    snap_import.unregister()
    snap_export.unregister()
    closet_materials.unregister()
    closet_materials_ui.unregister()
    closet_materials_ops.unregister()
    room_builder.unregister()
    snap_ops.unregister()
    fd_projects.unregister()
    fd_2dviews.unregister()
    lib_manager.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)    

if __name__ == "__main__":
    register()
