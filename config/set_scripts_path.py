import bpy
import os


def register():
    bl_dir = os.path.dirname(bpy.app.binary_path)
    scripts_dir = os.path.join(bl_dir, "scripts")
    bpy.context.preferences.filepaths.use_scripts_auto_execute = True

    if os.path.exists(scripts_dir):
        bpy.context.preferences.filepaths.script_directory = scripts_dir
        print("Found testing environment, setting scripts directory to: ", scripts_dir)


if __name__ == "__main__":
    register()
