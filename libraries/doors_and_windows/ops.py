import os
import math

import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from snap import sn_types
from snap import sn_utils


def update_doors_and_windows_id_props(obj, parent_obj):
    if "ID_PROMPT" in parent_obj:
        obj["ID_PROMPT"] = parent_obj["ID_PROMPT"]
    if "MENU_ID" in parent_obj:
        obj["MENU_ID"] = parent_obj["MENU_ID"]


class PlaceDoorsAndWindowsAsset():
    filepath: StringProperty(name="Filepath", default="Error")
    object_name: bpy.props.StringProperty(name="Object Name")

    asset = None
    selected_asset = None

    calculators = []

    drawing_plane = None
    next_wall = None
    current_wall = None
    previous_wall = None

    starting_point = ()
    placement = ''

    assembly = None
    obj = None
    include_objects = []
    exclude_objects = []
    selected_obj = None
    selected_point = None
    mouse_x = 0
    mouse_y = 0
    header_text = ""

    class_name = ""

    def invoke(self, context, event):
        self.reset_properties()
        self.get_asset(context)

        if self.asset:
            return self.execute(context)
        else:
            return self.cancel_drop(context)

    def reset_selection(self):
        self.current_wall = None
        self.selected_asset = None
        self.next_wall = None
        self.previous_wall = None
        self.placement = ''

    def reset_properties(self):
        self.asset = None
        self.selected_asset = None
        self.calculators = []
        self.drawing_plane = None
        self.next_wall = None
        self.current_wall = None
        self.previous_wall = None
        self.starting_point = ()
        self.placement = ''
        self.assembly = None
        self.obj = None
        self.exclude_objects = []
        self.class_name = ""

    def set_child_properties(self, obj):

        update_doors_and_windows_id_props(obj, self.asset.obj_bp)
        if obj.type == 'EMPTY':
            obj.hide_viewport = True
        if obj.type == 'MESH':
            obj.display_type = 'WIRE'

        if self.drawing_plane and obj.name != self.drawing_plane.name:
            self.exclude_objects.append(obj)
        for child in obj.children:
            self.set_child_properties(child)

    def set_placed_properties(self, obj):
        if obj.type == 'MESH':
            obj.display_type = 'TEXTURED'
        for child in obj.children:
            self.set_placed_properties(child)

    def set_screen_defaults(self, context):
        context.window.cursor_set('DEFAULT')
        context.area.header_text_set(None)

    def hide_cages(self, context):
        for obj in context.visible_objects:
            if 'IS_CAGE' in obj:
                obj.hide_viewport = True

    def get_asset(self, context):
        wm_props = context.window_manager.snap
        self.asset = wm_props.get_asset(self.filepath)

    def draw_asset(self):
        directory, file = os.path.split(self.filepath)
        filename, ext = os.path.splitext(file)

        if hasattr(self.asset, 'pre_draw'):
            self.asset.pre_draw()
        else:
            self.asset.draw()

        self.asset.set_name(filename)
        self.set_child_properties(self.asset.obj_bp)

    def position_asset(self, context):
        pass

    def confirm_placement(self, context):
        pass

    def run_asset_calculators(self):
        for calculator in self.asset.obj_prompts.snap.calculators:
            calculator.calculate()

    def create_drawing_plane(self, context):
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0, 0, 0)
        self.drawing_plane = context.active_object
        self.drawing_plane.display_type = 'WIRE'
        self.drawing_plane.dimensions = (100, 100, 1)

    def event_is_place_next_point(self, event):
        if self.starting_point == ():
            return False
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
            return True
        elif event.type == 'RET' and event.value == 'PRESS':
            return True
        else:
            return False

    def event_is_place_first_point(self, event):
        if self.starting_point != ():
            return False
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
            return True
        elif event.type == 'RET' and event.value == 'PRESS':
            return True
        else:
            return False

    def event_is_cancel_command(self, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return True
        else:
            return False

    def event_is_pass_through(self, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return True
        else:
            return False

    def cancel_drop(self, context):
        self.set_screen_defaults(context)
        if self.asset:
            sn_utils.delete_object_and_children(self.asset.obj_bp)
        if self.drawing_plane:
            sn_utils.delete_object_and_children(self.drawing_plane)
        self.hide_cages(context)
        return {'CANCELLED'}

    def refresh_data(self, hide=True):
        ''' For some reason matrix world doesn't evaluate correctly
            when placing cabinets next to this if object is hidden
            For now set x, y, z object to not be hidden.
        '''
        self.asset.obj_x.hide_viewport = hide
        self.asset.obj_y.hide_viewport = hide
        self.asset.obj_z.hide_viewport = hide
        self.asset.obj_x.empty_display_size = .001
        self.asset.obj_y.empty_display_size = .001
        self.asset.obj_z.empty_display_size = .001

    def finish(self, context):
        self.set_screen_defaults(context)
        if self.drawing_plane:
            sn_utils.delete_obj_list([self.drawing_plane])
        if self.asset.obj_bp:
            self.set_placed_properties(self.asset.obj_bp)
            context.view_layer.objects.active = self.asset.obj_bp
        self.hide_cages(context)
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        bpy.ops.closet_materials.assign_materials()
        return {'FINISHED'}


class SN_WINDOWS_AND_DOORS_OT_drop(Operator, PlaceDoorsAndWindowsAsset):
    bl_idname = "windows_and_doors.drop"
    bl_label = "Drag and Drop"
    bl_description = "This is called when an asset is dropped from the Product library"
    bl_options = {'UNDO'}

    filepath: StringProperty(name="Library Name")

    def execute(self, context):
        directory, file = os.path.split(self.filepath)
        filename, ext = os.path.splitext(file)

        if hasattr(self.asset, 'drop_id'):
            drop_id = self.asset.drop_id
            eval('bpy.ops.{}("INVOKE_DEFAULT", filepath=self.filepath)'.format(drop_id))
            return {'FINISHED'}

        bpy.ops.windows_and_doors.place_product('INVOKE_DEFAULT', filepath=self.filepath)

        return {'FINISHED'}


class SN_WINDOWS_AND_DOORS_OT_place_product(Operator, PlaceDoorsAndWindowsAsset):
    bl_idname = "windows_and_doors.place_product"
    bl_label = "Place Closet Product"

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

            sel_cabinet_x_world_loc = (self.selected_asset.obj_x.matrix_world[0][3],
                                       self.selected_asset.obj_x.matrix_world[1][3],
                                       self.selected_asset.obj_x.matrix_world[2][3])

            dist_to_bp = sn_utils.calc_distance(self.selected_point, sel_cabinet_world_loc)
            dist_to_x = sn_utils.calc_distance(self.selected_point, sel_cabinet_x_world_loc)
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
                x_loc = sel_asset_loc_x - math.cos(rot) * self.asset.obj_x.location.x + add_x_loc
                y_loc = sel_asset_loc_y - math.sin(rot) * self.asset.obj_x.location.x + add_y_loc

            else:
                self.placement = 'RIGHT'
                x_loc = sel_asset_loc_x + math.cos(rot) * self.selected_asset.obj_x.location.x
                y_loc = sel_asset_loc_y + math.sin(rot) * self.selected_asset.obj_x.location.x

            self.asset.obj_bp.rotation_euler.z = rot
            self.asset.obj_bp.location.x = x_loc
            self.asset.obj_bp.location.y = y_loc

        elif wall_bp:
            self.placement = 'WALL'
            self.current_wall = sn_types.Assembly(wall_bp)
            self.asset.obj_bp.rotation_euler = self.current_wall.obj_bp.rotation_euler
            self.asset.obj_bp.location.x = self.selected_point[0]
            self.asset.obj_bp.location.y = self.selected_point[1]

        else:
            self.asset.obj_bp.location.x = self.selected_point[0]
            self.asset.obj_bp.location.y = self.selected_point[1]

    def confirm_placement(self, context):
        if self.current_wall:
            x_loc = sn_utils.calc_distance(
                (
                    self.asset.obj_bp.location.x,
                    self.asset.obj_bp.location.y,
                    0),
                (
                    self.current_wall.obj_bp.matrix_local[0][3],
                    self.current_wall.obj_bp.matrix_local[1][3],
                    0))

            self.asset.obj_bp.location = (0, 0, self.asset.obj_bp.location.z)
            self.asset.obj_bp.rotation_euler = (0, 0, 0)
            self.asset.obj_bp.parent = self.current_wall.obj_bp
            self.asset.obj_bp.location.x = x_loc

        if self.placement == 'LEFT':
            self.asset.obj_bp.parent = self.selected_asset.obj_bp.parent
            constraint_obj = self.asset.obj_x
            constraint = self.selected_asset.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = False

        if self.placement == 'RIGHT':
            self.asset.obj_bp.parent = self.selected_asset.obj_bp.parent
            constraint_obj = self.selected_asset.obj_x
            constraint = self.asset.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = False

        if hasattr(self.asset, 'pre_draw'):
            self.asset.draw()
        self.set_child_properties(self.asset.obj_bp)

        for cal in self.calculators:
            cal.calculate()

        self.refresh_data(False)

    def execute(self, context):
        self.create_drawing_plane(context)
        self.draw_asset()
        self.run_asset_calculators()
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def assign_boolean(self, obj):
        if obj:
            objs = sn_utils.get_child_objects(self.asset.obj_bp)
            for obj_bool in objs:
                if obj_bool.get('use_as_bool_obj'):
                    mod = obj.modifiers.new(obj_bool.name, 'BOOLEAN')
                    mod.object = obj_bool
                    mod.operation = 'DIFFERENCE'

    def modal(self, context, event):
        self.run_asset_calculators()
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        self.reset_selection()

        self.selected_point, self.selected_obj, _ = sn_utils.get_selection_point(
            context,
            event,
            objects=self.include_objects,
            exclude_objects=self.exclude_objects)

        self.position_asset(context)

        if self.event_is_place_first_point(event):
            self.confirm_placement(context)
            self.assign_boolean(self.selected_obj)
            return self.finish(context)

        if self.event_is_cancel_command(event):
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


classes = (
    SN_WINDOWS_AND_DOORS_OT_drop,
    SN_WINDOWS_AND_DOORS_OT_place_product
)

register, unregister = bpy.utils.register_classes_factory(classes)
