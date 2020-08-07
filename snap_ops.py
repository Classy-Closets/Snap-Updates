import bpy, bgl, blf
from bpy.types import Operator
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       EnumProperty,
                       CollectionProperty)

from . import utils as snap_utils
from mv import utils, fd_types, unit
import os


class OPS_change_category(Operator):
    bl_idname = "snap.change_category"
    bl_label = "Change Category"
    
    category_name = StringProperty(name="Category Name")
    
    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        library_tabs = context.scene.mv.ui.library_tabs
        if library_tabs == 'SCENE':
            library_name = context.scene.mv.scene_library_name
            path = os.path.join(utils.get_library_dir("scenes"),library_name,self.category_name)
            context.scene.mv.scene_category_name = self.category_name        
        if library_tabs == 'PRODUCT':
            lib = context.window_manager.cabinetlib.lib_products[context.scene.mv.product_library_name]
            path = os.path.join(lib.lib_path,self.category_name)         
            context.scene.mv.product_category_name = self.category_name
        elif library_tabs == 'INSERT':
            lib = context.window_manager.cabinetlib.lib_inserts[context.scene.mv.insert_library_name]
            path = os.path.join(lib.lib_path,self.category_name)    
            context.scene.mv.insert_category_name = self.category_name
        elif library_tabs == 'ASSEMBLY':
            library_name = context.scene.mv.assembly_library_name
            path = os.path.join(utils.get_library_dir("assemblies"),library_name,self.category_name)
            context.scene.mv.assembly_category_name = self.category_name
        elif library_tabs == 'OBJECT':
            library_name = context.scene.mv.object_library_name
            path = os.path.join(utils.get_library_dir("objects"),library_name,self.category_name)
            context.scene.mv.object_category_name = self.category_name
        elif library_tabs == 'MATERIAL':
            library_name = context.scene.mv.material_library_name
            path = os.path.join(utils.get_library_dir("materials"),library_name,self.category_name)
            context.scene.mv.material_category_name = self.category_name
        elif library_tabs == 'WORLD':
            library_name = context.scene.mv.world_library_name
            path = os.path.join(utils.get_library_dir("worlds"),library_name,self.category_name)
            context.scene.mv.world_category_name = self.category_name
        if os.path.isdir(path):
            snap_utils.update_file_browser_space(context,path)
        else:
            print("ERROR")
        return {'FINISHED'}


class OPS_load_snap_defaults(Operator):
    bl_idname = "fd_general.load_snap_defaults"
    bl_label = "Load SNap Defaults"

    @classmethod
    def poll(cls, context):
        return True

    def init_db(self):
        if "snap_db" in bpy.context.user_preferences.addons.keys():
            import time
            time_start = time.time()
            addon_prefs = bpy.context.user_preferences.addons["snap_db"].preferences
            filename = os.path.basename(addon_prefs.default_csv_path)
            filepath = addon_prefs.default_csv_path

            bpy.ops.snap_db.import_csv('EXEC_DEFAULT', filename=filename, filepath=filepath, rebuild_db=True)
            print("Rebuild Database Finished: %.4f sec" % (time.time() - time_start))        
        
    def execute(self, context):
        import shutil
        path,filename = os.path.split(os.path.normpath(__file__))
        src_userpref_file = os.path.join(path,"config","snap_userpref.blend")
        src_startup_file = os.path.join(path,"config","snap_startup.blend")
        userpath = os.path.join(bpy.utils.resource_path(type='USER'),"config")
        if not os.path.exists(userpath): os.makedirs(userpath)
        dst_userpref_file = os.path.join(userpath,"fd_userpref.blend")
        dst_startup_file = os.path.join(userpath,"fd_startup.blend")
        shutil.copyfile(src_userpref_file,dst_userpref_file)
        shutil.copyfile(src_startup_file,dst_startup_file)
        self.init_db()
        return {'FINISHED'}
        
    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(550))
        
    def draw(self, context):
        layout = self.layout
        layout.label("Are you sure you want to restore the SNap default startup file and user preferences?",icon='QUESTION')
        layout.label("You will need to restart the application for the changes to take effect.",icon='BLANK1')


def register():
    bpy.utils.register_class(OPS_change_category)
    bpy.utils.register_class(OPS_load_snap_defaults)


def unregister():
    bpy.utils.unregister_class(OPS_change_category)
    bpy.utils.unregister_class(OPS_load_snap_defaults)
