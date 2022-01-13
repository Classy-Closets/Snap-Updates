import bpy
from bpy.types import Operator

from snap import sn_utils

class SN_SCENE_OT_clear_2d_views(Operator):
    bl_idname = "sn_scene.clear_2d_views"
    bl_label = "Delete 2d View Scenes"
    bl_description = "Delete all 2d view scenes"
    bl_options = {'UNDO'}     

    def execute(self, context):

        for scene in bpy.data.scenes:
            is_pv = scene.snap.scene_type == 'PLAN_VIEW'
            is_elv = scene.snap.scene_type == 'ELEVATION'
            is_acc = scene.snap.scene_type == 'ACCORDION'
            is_island = scene.snap.scene_type == 'ISLAND'
            is_virt = scene.snap.scene_type == 'VIRTUAL'
            if is_elv or is_pv or is_acc or is_island or is_virt:
                context.window.scene = scene
                bpy.ops.scene.delete()

        for view in context.window_manager.snap.image_views:
            context.window_manager.snap.image_views.remove(0)

        # we need to remove any orphaned datablocks
        for obj in bpy.data.objects:

            # Profiles have no users, but most be preserved
            if obj.get('IS_MOLDING_PROFILE') is not None:
                continue
            if len(obj.users_scene) == 0:
                # first, remove mesh data, if its sole user is the object
                mesh = obj.data
                if obj.name in bpy.data.objects:
                    bpy.data.objects.remove(obj)

                if isinstance(mesh, bpy.types.Mesh) and mesh.users == 0:
                    bpy.data.meshes.remove(mesh)
                # finally, the object, if it still exists. (for some reason, it doesn't always...)
        return {'FINISHED'}


class SN_SCENE_OT_user_clear_2d_views(Operator):
    bl_idname = "sn_scene.user_clear_2d_views"
    bl_label = "Delete 2d View Scenes"
    bl_description = "Delete all 2d view scenes"
    bl_options = {'UNDO'}     

    def execute(self, context):

        bpy.ops.sn_scene.clear_2d_views()
        for obj in bpy.data.objects:
            if obj.get('IS_VISDIM_A') or obj.get('IS_VISDIM_B'):
                # Preserve wall obstacle annotations
                obstacle_bp = sn_utils.get_obstacle_bp(obj)
                if obstacle_bp:
                    continue
                bpy.data.objects.remove(obj, do_unlink=True)
        return {'FINISHED'}


classes = (
    SN_SCENE_OT_clear_2d_views,
    SN_SCENE_OT_user_clear_2d_views,
)

register, unregister = bpy.utils.register_classes_factory(classes)
