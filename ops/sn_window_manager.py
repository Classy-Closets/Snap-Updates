import os
import shutil

import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from snap import sn_utils
from snap import sn_paths


class SN_WM_OT_message_box(bpy.types.Operator):
    bl_idname = "snap.message_box"
    bl_label = "System Info"

    message: StringProperty(name="Message", description="Message to Display")
    icon: StringProperty(name="Icon", description="Icon name", default='NONE')

    def check(self, context):
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=350)

    def draw(self, context):
        layout = self.layout
        for line in self.message.split('\n'):
            layout.label(text=line, icon=self.icon)

    def execute(self, context):
        return {'FINISHED'}


class SN_WM_OT_snap_drag_drop(Operator):
    bl_idname = "wm.snap_drag_drop"
    bl_label = "Drag and Drop"
    bl_description = "This is a special operator that will be called when an image is dropped from the file browser"

    filepath: StringProperty(name="Message", default="Error")

    def execute(self, context):
        wm_props = context.window_manager.snap
        scene_props = context.scene.snap

        if scene_props.active_library_name in wm_props.libraries:
            lib = wm_props.libraries[scene_props.active_library_name]
            eval('bpy.ops.' + lib.drop_id + '("INVOKE_DEFAULT",filepath=self.filepath)')

        return {'FINISHED'}


class SN_WM_OT_load_snap_defaults(Operator):
    bl_idname = "snap.load_snap_defaults"
    bl_label = "Load SNap Defaults"

    @classmethod
    def poll(cls, context):
        return True

    def init_db(self):
        import time
        time_start = time.time()
        franchise_location = bpy.context.preferences.addons['snap'].preferences.franchise_location
        path = os.path.join(sn_paths.CSV_DIR_PATH, "CCItems_" + franchise_location + ".csv")
        if not os.path.exists(path):
            path = os.path.join(sn_paths.CSV_DIR_PATH, "CCItems_PHX.csv")
        filename = os.path.basename(path)
        filepath = path
        bpy.ops.snap.import_csv('EXEC_DEFAULT', filename=filename, filepath=filepath, rebuild_db=True)
        print("Rebuild Database Finished: %.4f sec" % (time.time() - time_start))

    def copy_config_files(self, path):
        src_userpref_file = sn_paths.PREFS_PATH
        src_startup_file = sn_paths.STARTUP_FILE_PATH

        if not os.path.exists(path):
            os.makedirs(path)

        dst_userpref_file = os.path.join(path, "userpref.blend")
        dst_startup_file = os.path.join(path, "startup.blend")
        shutil.copyfile(src_userpref_file, dst_userpref_file)
        shutil.copyfile(src_startup_file, dst_startup_file)

    def use_auto_set_scripts_dir(self):
        bl_ver = "{}.{}".format(bpy.app.version[0], bpy.app.version[1])
        bl_dir = os.path.dirname(bpy.app.binary_path)
        startup_dir = os.path.join(bl_dir, bl_ver, "scripts", "startup")
        src = os.path.join(sn_paths.SNAP_CONFIG_DIR, "set_scripts_path.py")
        dst = os.path.join(startup_dir, "set_scripts_path.py")
        shutil.copyfile(src, dst)
        print("Found testing environment, using auto-set scripts directory:", dst)

    def remove_old_data(self):
        for subdir, dirs, files in os.walk(sn_paths.CLOSET_THUMB_DIR):
            for dir in dirs:
                if "Closet Products -" in dir:
                    print("Removing:", os.path.join(subdir, dir))
                    shutil.rmtree(os.path.join(subdir, dir))

    def execute(self, context):
        config_path = sn_paths.CONFIG_PATH
        app_template_path = sn_paths.APP_TEMPLATE_PATH
        franchise_location = context.preferences.addons['snap'].preferences.franchise_location
        bpy.ops.script.execute_preset(
            filepath=sn_paths.SNAP_THEME_PATH,
            menu_idname='USERPREF_MT_interface_theme_presets')
        self.copy_config_files(config_path)
        self.copy_config_files(app_template_path)
        self.remove_old_data()
        self.use_auto_set_scripts_dir()
        context.preferences.addons['snap'].preferences.franchise_location = franchise_location
        self.init_db()

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(550))

    def draw(self, context):
        layout = self.layout
        layout.label(
            text="Are you sure you want to restore the SNap default startup file and user preferences?",
            icon='QUESTION')

        layout.label(
            text="You will need to restart the application for the changes to take effect.",
            icon='BLANK1')


classes = (
    SN_WM_OT_message_box,
    SN_WM_OT_snap_drag_drop,
    SN_WM_OT_load_snap_defaults,
)

register, unregister = bpy.utils.register_classes_factory(classes)
