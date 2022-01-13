import os
import shutil
import stat

import bpy
from bpy.app.handlers import persistent
from snap import sn_utils
from snap import sn_paths
from . import sn_utils
from . import addon_updater_ops

@persistent
def load_driver_functions(scene=None):
    """ Load Default Drivers
    """
    import inspect
    from snap import sn_driver_functions
    for name, obj in inspect.getmembers(sn_driver_functions):
        if name not in bpy.app.driver_namespace:
            bpy.app.driver_namespace[name] = obj


@persistent
def load_materials_from_db(scene=None):
    import time
    time_start = time.time()
    path = os.path.join(sn_paths.CSV_DIR_PATH, "CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location + ".csv")
    filename = os.path.basename(path)
    filepath = path
    bpy.ops.snap.import_csv('EXEC_DEFAULT', filename=filename, filepath=filepath)
    print("load_materials_from_db Finished: %.4f sec" % (time.time() - time_start))


# @persistent
# def load_pointers(scene=None):
#     snap_pointers.write_pointer_files()
#     snap_pointers.update_pointer_properties()


@persistent
def assign_material_pointers(scene=None):
    bpy.ops.closet_materials.assign_materials(only_update_pointers=True)


@persistent
def assign_materials(scene=None):
    bpy.ops.closet_materials.assign_materials()


@persistent
def sync_spec_groups(scene):
    """ Syncs Spec Groups with the current library modules
    """
    bpy.ops.sn_material.reload_spec_group_from_library_modules()


@persistent
def load_libraries(scene=None):
    wm_props = bpy.context.window_manager.snap

    wm_props.add_library(
        name="Product Library",
        lib_type='SNAP',
        root_dir=sn_paths.CLOSET_ROOT,
        thumbnail_dir=sn_paths.CLOSET_THUMB_DIR,
        drop_id='sn_closets.drop',
        use_custom_icon=True,
        icon='closet_lib',
    )

    wm_props.add_library(
        name="Window and Door Library",
        lib_type='SNAP',
        root_dir=sn_paths.DOORS_AND_WINDOWS_ROOT,
        thumbnail_dir=sn_paths.DOORS_AND_WINDOWS_THUMB_DIR,
        drop_id='windows_and_doors.drop',
        use_custom_icon=False,
        icon='MOD_LATTICE'
    )

    wm_props.add_library(
        name="Appliance Library",
        lib_type='SNAP',
        root_dir=sn_paths.APPLIANCE_DIR,
        thumbnail_dir=sn_paths.APPLIANCE_THUMB_DIR,
        drop_id='sn_appliances.drop',
        use_custom_icon=False,
        icon='TOPBAR',
    )

    wm_props.add_library(
        name="Object Library",
        lib_type='STANDARD',
        root_dir=sn_paths.OBJECT_DIR,
        drop_id='sn_library.drop_object_from_library',
        use_custom_icon=False,
        icon='OBJECT_DATA'
    )

    wm_props.add_library(
        name="Material Library",
        lib_type='STANDARD',
        root_dir=sn_paths.MATERIAL_DIR,
        drop_id='sn_library.drop_material_from_library',
        use_custom_icon=False,
        icon='MATERIAL'
    )

    wm_props.get_library_assets()

    path = os.path.join(sn_paths.CLOSET_THUMB_DIR, sn_paths.DEFAULT_CATEGORY)

    if os.path.exists(path):
        sn_utils.update_file_browser_path(bpy.context, path)
        bpy.ops.sn_library.change_library_category(category=sn_paths.DEFAULT_CATEGORY)


@persistent
def load_library_modules(scene):
    """ Register Every Library Module on Startup
    """
    bpy.ops.snap.load_library_modules()


@persistent
def default_settings(scene=None):
    scene = bpy.context.scene
    prefs = bpy.context.preferences
    # Units
    scene.unit_settings.system = 'IMPERIAL'
    scene.unit_settings.length_unit = 'INCHES'
    # Render
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.preview_samples = 0
    scene.cycles.use_preview_denoising = True
    scene.cycles.preview_denoiser = 'AUTO'
    scene.cycles.max_bounces = 6
    scene.cycles.transparent_max_bounces = 6
    scene.cycles.transmission_bounces = 6
    # Prefs
    prefs.use_preferences_save = False  # Disable autosave
    if not bpy.data.is_saved:
        scene.closet_materials.set_defaults()
    else:
        scene.closet_materials.defaults_set = True

@persistent
def init_machining_collection(scene=None):
    mac_col = bpy.data.collections.get("Machining")
    if mac_col:
        for obj in mac_col.objects:
            obj.display_type = 'WIRE'
        mac_col.hide_viewport = True


def del_dir(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


@persistent
def check_for_update(scene=None):
    source_dir = os.path.join(os.path.dirname(__file__), "snap_updater", "source")
    staging_dir = os.path.join(os.path.dirname(__file__), "snap_updater", "update_staging")
    update_dirs = [source_dir, staging_dir]

    for dir_path in update_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path, onerror=del_dir)

    if "snap" in bpy.context.preferences.addons.keys():
        addon_updater_ops.check_for_update_background()


def register():
    bpy.app.handlers.load_post.append(check_for_update)
    bpy.app.handlers.load_post.append(load_driver_functions)
    bpy.app.handlers.load_post.append(load_materials_from_db)
    bpy.app.handlers.load_post.append(sync_spec_groups)
    bpy.app.handlers.load_post.append(default_settings)
    bpy.app.handlers.load_post.append(assign_material_pointers)
    bpy.app.handlers.save_pre.append(assign_materials)
    bpy.app.handlers.load_post.append(load_libraries)
    bpy.app.handlers.load_post.append(load_library_modules)
    bpy.app.handlers.load_post.append(init_machining_collection)


def unregister():
    bpy.app.handlers.load_post.remove(check_for_update)
    bpy.app.handlers.load_post.remove(load_driver_functions)
    bpy.app.handlers.load_post.remove(load_materials_from_db)
    bpy.app.handlers.load_post.remove(sync_spec_groups)
    bpy.app.handlers.load_post.remove(default_settings)
    bpy.app.handlers.load_post.remove(assign_material_pointers)
    bpy.app.handlers.save_pre.remove(assign_materials)
    bpy.app.handlers.load_post.remove(load_libraries)
    bpy.app.handlers.load_post.remove(load_library_modules)
    bpy.app.handlers.load_post.remove(init_machining_collection)