import os
import math
from pathlib import Path

import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import mathutils

from snap import sn_types
from snap import sn_utils


def event_is_place_asset(event):
    if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
        return True
    elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
        return True
    elif event.type == 'RET' and event.value == 'PRESS':
        return True
    else:
        return False


def event_is_cancel_command(event):
    if event.type in {'RIGHTMOUSE', 'ESC'}:
        return True
    else:
        return False


def event_is_pass_through(event):
    if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
        return True
    else:
        return False


class SN_LIB_OT_set_active_library(Operator):
    bl_idname = "sn_library.set_active_library"
    bl_label = "Set Active Library"
    bl_description = "This will set the active library"
    bl_options = {'UNDO'}

    library_name: StringProperty(name="Library Name")

    def execute(self, context):
        snap_wm = context.window_manager.snap
        snap_scene = context.scene.snap
        snap_scene.active_library_name = self.library_name
        lib_names = [lib.name for lib in snap_wm.libraries]

        if self.library_name in lib_names:
            library = snap_wm.libraries[snap_scene.active_library_name]

            if library.lib_type == 'SNAP':
                root_dir = library.thumbnail_dir
                dirs = os.listdir(root_dir)
            else:
                root_dir = library.root_dir
                dirs = os.listdir(root_dir)

            if snap_scene.active_category in dirs:
                path = os.path.join(root_dir, snap_scene.active_category)
            else:
                snap_scene.active_category = dirs[0]
                path = os.path.join(root_dir, snap_scene.active_category)

            if os.path.exists(path):
                sn_utils.update_file_browser_path(context, path)

        context.area.tag_redraw()
        return {'FINISHED'}


class SN_LIB_OT_change_library_category(bpy.types.Operator):
    bl_idname = "sn_library.change_library_category"
    bl_label = "Change Library Category"
    bl_description = "Change Library Category"

    category: StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        wm_props = context.window_manager.snap
        scene_props = context.scene.snap
        active_library = wm_props.libraries[scene_props.active_library_name]
        scene_props.active_category = self.category

        if active_library.lib_type == 'SNAP':
            root_dir = active_library.thumbnail_dir
        else:
            root_dir = active_library.root_dir

        path = os.path.join(root_dir, self.category)

        if os.path.exists(path):
            sn_utils.update_file_browser_path(context, path)

        return {'FINISHED'}


class SN_LIB_OT_open_browser_window(bpy.types.Operator):
    bl_idname = "sn_library.open_browser_window"
    bl_label = "Open Browser Window"
    bl_description = "This will open the active path in your OS file browser"

    path: StringProperty(name="Path", description="Path to Open")

    def execute(self, context):
        import subprocess
        if 'Windows' in str(bpy.app.build_platform):
            subprocess.Popen(r'explorer ' + self.path)
        elif 'Darwin' in str(bpy.app.build_platform):
            subprocess.Popen(['open', os.path.normpath(self.path)])
        else:
            subprocess.Popen(['xdg-open', os.path.normpath(self.path)])
        return {'FINISHED'}


class SN_LIB_OT_drop_object_from_library(bpy.types.Operator):
    bl_idname = "sn_library.drop_object_from_library"
    bl_label = "Drop Object From Library"
    bl_description = "This drops an object from the library"

    filepath: bpy.props.StringProperty(name="Filepath", default="Error")

    drawing_plane = None
    obj = None

    placement = ''
    asset = None
    selected_obj = None
    selected_point = None
    selected_asset = None
    current_wall = None

    def execute(self, context):
        self.create_drawing_plane(context)
        self.obj = self.get_object(context)
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def get_object(self, context):
        path, ext = os.path.splitext(self.filepath)
        object_file_path = os.path.join(path + ".blend")

        with bpy.data.libraries.load(object_file_path, False, False) as (data_from, data_to):
            data_to.objects = data_from.objects
        for obj in data_to.objects:
            context.view_layer.active_layer_collection.collection.objects.link(obj)
            return obj

    def create_drawing_plane(self, context):
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0, 0, 0)
        self.drawing_plane = context.active_object
        self.drawing_plane.display_type = 'WIRE'
        self.drawing_plane.dimensions = (100, 100, 1)

    def position_asset(self, context):
        wall_bp = sn_utils.get_wall_bp(self.selected_obj)
        product_bp = sn_utils.get_closet_bp(self.selected_obj)

        if product_bp:
            self.selected_asset = sn_types.Assembly(product_bp)
            sel_asset_loc_x = self.selected_asset.obj_bp.matrix_world[0][3]
            sel_asset_loc_y = self.selected_asset.obj_bp.matrix_world[1][3]
            sel_asset_loc_z = self.selected_asset.obj_bp.matrix_world[2][3]
            sel_cabinet_world_loc = (sel_asset_loc_x,
                                     sel_asset_loc_y,
                                     sel_asset_loc_z)
            sel_cabinet_x_world_loc =\
                (self.selected_asset.obj_x.matrix_world[0][3],
                 self.selected_asset.obj_x.matrix_world[1][3],
                 self.selected_asset.obj_x.matrix_world[2][3])
            dist_to_bp = sn_utils.calc_distance(
                self.selected_point, sel_cabinet_world_loc)
            dist_to_x = sn_utils.calc_distance(
                self.selected_point, sel_cabinet_x_world_loc)
            rot = self.selected_asset.obj_bp.rotation_euler.z
            x_loc = 0
            y_loc = 0

            if wall_bp:
                self.current_wall = sn_types.Assembly(wall_bp)
                rot += self.current_wall.obj_bp.rotation_euler.z

            if dist_to_bp < dist_to_x:
                self.placement = 'LEFT'
                add_x_loc = 0
                add_y_loc = 0
                x_loc =\
                    sel_asset_loc_x - math.cos(rot) * self.obj.location.x + add_x_loc  # noqa: E501
                y_loc =\
                    sel_asset_loc_y - math.sin(rot) * self.obj.location.x + add_y_loc  # noqa: E501

            else:
                self.placement = 'RIGHT'
                x_loc =\
                    sel_asset_loc_x + math.cos(rot) * self.selected_asset.obj_x.location.x  # noqa: E501
                y_loc =\
                    sel_asset_loc_y + math.sin(rot) * self.selected_asset.obj_x.location.x  # noqa: E501

            self.obj.rotation_euler.z = rot
            self.obj.location.x = x_loc
            self.obj.location.y = y_loc

        elif wall_bp:
            self.placement = 'WALL'
            self.current_wall = sn_types.Assembly(wall_bp)
            self.obj.rotation_euler = self.current_wall.obj_bp.rotation_euler
            self.obj.location.x = self.selected_point[0]
            self.obj.location.y = self.selected_point[1]

        else:
            self.obj.location.x = self.selected_point[0]
            self.obj.location.y = self.selected_point[1]

    def confirm_placement(self, context):
        if self.current_wall:
            x_loc = sn_utils.calc_distance(
                (
                    self.obj.location.x,
                    self.obj.location.y,
                    0),
                (
                    self.current_wall.obj_bp.matrix_local[0][3],
                    self.current_wall.obj_bp.matrix_local[1][3],
                    0))
            self.obj.location = (0, 0, self.obj.location.z)
            self.obj.rotation_euler = (0, 0, 0)
            self.obj.parent = self.current_wall.obj_bp
            self.obj.location.x = x_loc

        if self.placement == 'LEFT':
            self.obj.parent = self.selected_asset.obj_bp.parent
            constraint_obj = self.asset.obj_x
            constraint =\
                self.selected_asset.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = False

        if self.placement == 'RIGHT':
            self.obj.parent = self.selected_asset.obj_bp.parent
            constraint_obj = self.selected_asset.obj_x
            constraint = self.obj.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = False

    def modal(self, context, event):
        context.area.tag_redraw()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y

        self.selected_point, self.selected_obj, selected_normal = sn_utils.get_selection_point(context, event, exclude_objects=[self.obj])
        if self.obj.get('addt_z_rot') is None:
            self.obj['addt_z_rot'] = 0

        obj_path = self.filepath
        split_path = obj_path.split("\\")
        category = split_path[-2:-1][0]

        if category == "Outlets and Switches":
            self.position_asset(context)

        if event.ctrl:
            if event.mouse_y > event.mouse_prev_y:
                self.obj['addt_z_rot'] += .1
            else:
                self.obj['addt_z_rot'] -= .1
        elif event.type == 'LEFT_ARROW' and event.value == 'PRESS':
            self.obj['addt_z_rot'] += math.radians(90)
        elif event.type == 'RIGHT_ARROW' and event.value == 'PRESS':
            self.obj['addt_z_rot'] -= math.radians(90)
        else:
            self.position_object(self.selected_point, self.selected_obj, selected_normal)

        if event_is_place_asset(event):
            return self.finish(context)

        if event_is_cancel_command(event):
            return self.cancel_drop(context)

        if event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def position_object(self, selected_point, selected_obj, selected_normal):
        self.obj.location = selected_point
        forward_axis = mathutils.Vector([0.0, -1.0, 0.0])
        if self.obj.get('follow_normal_on_drop'):
            angle = selected_normal.angle(forward_axis, 0)
            axis = forward_axis.cross(selected_normal)
            euler = mathutils.Matrix.Rotation(angle, 4, axis).to_euler()
            euler[2] += self.obj['addt_z_rot']
            self.obj.rotation_euler = euler

    def cancel_drop(self, context):
        obj_list = []
        obj_list.append(self.drawing_plane)
        obj_list.append(self.obj)
        sn_utils.delete_obj_list(obj_list)
        return {'CANCELLED'}

    def finish(self, context):
        context.window.cursor_set('DEFAULT')
        if self.drawing_plane:
            sn_utils.delete_obj_list([self.drawing_plane])
        bpy.ops.object.select_all(action='DESELECT')
        self.obj.select_set(True)
        obj_path = self.filepath
        split_path = obj_path.split("\\")
        category = split_path[-2:-1][0]
        if category == "Outlets and Switches":
            self.confirm_placement(context)
        self.obj.name = category + "." + self.obj.name
        bpy.ops.wm.popup_props('INVOKE_DEFAULT')
        context.view_layer.objects.active = self.obj
        context.area.tag_redraw()
        return {'FINISHED'}


class SN_LIB_OT_drop_material_from_library(bpy.types.Operator):
    bl_idname = "sn_library.drop_material_from_library"
    bl_label = "Drop Material From Library"
    bl_description = "This drops a material from the library"

    filepath: bpy.props.StringProperty(name="Filepath", default="Error")

    mat = None

    @classmethod
    def poll(cls, context):
        if context.object and context.object.mode != 'OBJECT':
            return False
        return True

    def execute(self, context):
        self.mat = self.get_material(context)
        if not self.mat:
            return {'FINISHED'}
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def get_material(self, context):
        mat_path = Path(self.filepath)
        return sn_utils.get_material(mat_path.parent.name, mat_path.stem)

    def modal(self, context, event):
        context.window.cursor_set('PAINT_BRUSH')
        context.area.tag_redraw()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        selected_point, selected_obj, _ = sn_utils.get_selection_point(context, event)
        bpy.ops.object.select_all(action='DESELECT')
        if selected_obj:
            selected_obj.select_set(True)
            context.view_layer.objects.active = selected_obj

            if event_is_place_asset(event):
                if len(selected_obj.data.uv_layers) == 0:
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.uv.smart_project(angle_limit=1.15192)
                    bpy.ops.object.editmode_toggle()

                if len(selected_obj.material_slots) == 0:
                    bpy.ops.object.material_slot_add()

                if len(selected_obj.material_slots) > 1:
                    bpy.ops.sn_material.assign_material_dialog(
                        'INVOKE_DEFAULT',
                        material_name=self.mat.name,
                        object_name=selected_obj.name)
                    return self.finish(context)
                else:
                    for slot in selected_obj.material_slots:
                        slot.material = self.mat

                return self.finish(context)

        if event_is_cancel_command(event):
            return self.cancel_drop(context)

        if event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def cancel_drop(self, context):
        context.window.cursor_set('DEFAULT')
        return {'CANCELLED'}

    def finish(self, context):
        context.window.cursor_set('DEFAULT')
        context.area.tag_redraw()
        return {'FINISHED'}


classes = (
    SN_LIB_OT_change_library_category,
    SN_LIB_OT_set_active_library,
    SN_LIB_OT_open_browser_window,
    SN_LIB_OT_drop_object_from_library,
    SN_LIB_OT_drop_material_from_library,
)

register, unregister = bpy.utils.register_classes_factory(classes)
