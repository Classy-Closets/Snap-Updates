import os
import math
import time

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

from snap import sn_types, sn_unit
from snap import sn_utils
from .. import closet_props
from ..common import common_parts
from .. import closet_paths
from ..ops.drop_closet import PlaceClosetInsert
from ..data import data_drawers


class SNAP_OT_move_closet(Operator):
    bl_idname = "sn_closets.move_closet"
    bl_label = "Move Closet"

    obj_bp_name: bpy.props.StringProperty(name="Obj Base Point Name")

    closet = None
    selected_closet = None

    calculators = []

    drawing_plane = None

    next_wall = None
    current_wall = None
    previous_wall = None

    starting_point = ()
    placement = ''

    assembly = None
    obj = None
    exclude_objects = []

    class_name = ""

    def reset_selection(self):
        self.current_wall = None
        self.selected_closet = None
        self.next_wall = None
        self.previous_wall = None
        self.placement = ''

    def reset_properties(self):
        self.closet = None
        self.selected_closet = None
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

    def execute(self, context):
        self.reset_properties()
        self.create_drawing_plane(context)
        self.get_closet(context)
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def position_closet(self, mouse_location, selected_obj):
        closet_bp = sn_utils.get_closet_bp(selected_obj)
        if not closet_bp:
            closet_bp = sn_utils.get_appliance_bp(selected_obj)

        wall_bp = sn_utils.get_wall_bp(selected_obj)
        if closet_bp:
            self.selected_closet = sn_types.Assembly(closet_bp)

            sel_closet_world_loc = (self.selected_closet.obj_bp.matrix_world[0][3],
                                     self.selected_closet.obj_bp.matrix_world[1][3],
                                     self.selected_closet.obj_bp.matrix_world[2][3])

            sel_closet_x_world_loc = (self.selected_closet.obj_x.matrix_world[0][3],
                                       self.selected_closet.obj_x.matrix_world[1][3],
                                       self.selected_closet.obj_x.matrix_world[2][3])

            dist_to_bp = sn_utils.calc_distance(mouse_location, sel_closet_world_loc)
            dist_to_x = sn_utils.calc_distance(mouse_location, sel_closet_x_world_loc)
            rot = self.selected_closet.obj_bp.rotation_euler.z
            x_loc = 0
            y_loc = 0
            if wall_bp:
                self.current_wall = sn_types.Assembly(wall_bp)
                rot += self.current_wall.obj_bp.rotation_euler.z      

            if dist_to_bp < dist_to_x:
                self.placement = 'LEFT'
                add_x_loc = 0
                add_y_loc = 0
                # if sel_product.obj_bp.snap.placement_type == 'Corner':
                #     rot += math.radians(90)
                #     add_x_loc = math.cos(rot) * sel_product.obj_y.location.y
                #     add_y_loc = math.sin(rot) * sel_product.obj_y.location.y
                x_loc = self.selected_closet.obj_bp.matrix_world[0][3] - math.cos(rot) * self.closet.obj_x.location.x + add_x_loc
                y_loc = self.selected_closet.obj_bp.matrix_world[1][3] - math.sin(rot) * self.closet.obj_x.location.x + add_y_loc

            else:
                self.placement = 'RIGHT'
                x_loc = self.selected_closet.obj_bp.matrix_world[0][3] + math.cos(rot) * self.selected_closet.obj_x.location.x
                y_loc = self.selected_closet.obj_bp.matrix_world[1][3] + math.sin(rot) * self.selected_closet.obj_x.location.x

            self.closet.obj_bp.rotation_euler.z = rot
            self.closet.obj_bp.location.x = x_loc
            self.closet.obj_bp.location.y = y_loc

        elif wall_bp:
            self.placement = 'WALL'
            self.current_wall = sn_types.Assembly(wall_bp)
            self.closet.obj_bp.rotation_euler = self.current_wall.obj_bp.rotation_euler
            self.closet.obj_bp.location.x = mouse_location[0]
            self.closet.obj_bp.location.y = mouse_location[1]

        else:
            self.closet.obj_bp.location.x = mouse_location[0]
            self.closet.obj_bp.location.y = mouse_location[1]

    def get_closet(self, context):
        obj = bpy.data.objects[self.obj_bp_name]
        obj_bp = sn_utils.get_closet_bp(obj)
        self.closet = sn_types.Assembly(obj_bp)
        self.closet.obj_bp.constraints.clear()
        self.closet.obj_bp.parent = None
        self.set_child_properties(self.closet.obj_bp)

    def set_child_properties(self,obj):
        if obj.name != self.drawing_plane.name:
            self.exclude_objects.append(obj)            
        if obj.type == 'MESH':
            obj.display_type = 'WIRE'          
        for child in obj.children:
            self.set_child_properties(child)         

    def set_placed_properties(self,obj):
        if obj.type == 'MESH':
            obj.display_type = 'TEXTURED'
        for child in obj.children:
            self.set_placed_properties(child) 

    def create_drawing_plane(self,context):
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0, 0, 0)
        self.drawing_plane = context.active_object
        self.drawing_plane.display_type = 'WIRE'
        self.drawing_plane.dimensions = (100, 100, 1)

    def confirm_placement(self, context):
        if self.current_wall:
            x_loc = sn_utils.calc_distance((self.closet.obj_bp.location.x,self.closet.obj_bp.location.y,0),
                                           (self.current_wall.obj_bp.matrix_local[0][3],self.current_wall.obj_bp.matrix_local[1][3],0))

            self.closet.obj_bp.location = (0,0,self.closet.obj_bp.location.z)
            self.closet.obj_bp.rotation_euler = (0,0,0)
            self.closet.obj_bp.parent = self.current_wall.obj_bp
            self.closet.obj_bp.location.x = x_loc

        if self.placement == 'LEFT':
            self.closet.obj_bp.parent = self.selected_closet.obj_bp.parent
            constraint_obj = self.closet.obj_x
            constraint = self.selected_closet.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = False

        if self.placement == 'RIGHT':
            self.closet.obj_bp.parent = self.selected_closet.obj_bp.parent
            constraint_obj = self.selected_closet.obj_x
            constraint = self.closet.obj_bp.constraints.new('COPY_LOCATION')
            constraint.target = constraint_obj
            constraint.use_x = True
            constraint.use_y = True
            constraint.use_z = False

        if hasattr(self.closet, 'pre_draw'):
            self.closet.draw()
        self.set_child_properties(self.closet.obj_bp)
        self.refresh_data(False)

    def modal(self, context, event):
        bpy.ops.object.select_all(action='DESELECT')

        context.area.tag_redraw()

        for calculator in self.calculators:
            calculator.calculate()

        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        self.reset_selection()

        selected_point, selected_obj, _ = sn_utils.get_selection_point(
            context,
            event,
            exclude_objects=self.exclude_objects)

        self.position_closet(selected_point, selected_obj)

        if self.event_is_place_first_point(event):
            self.confirm_placement(context)
            return self.finish(context)

        if self.event_is_cancel_command(event):
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

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

    def position_object(self, selected_point, selected_obj):
        self.closet.obj_bp.location = selected_point

    def cancel_drop(self, context):
        sn_utils.delete_object_and_children(self.drawing_plane)
        return {'CANCELLED'}

    def refresh_data(self, hide=True):
        ''' For some reason matrix world doesn't evaluate correctly
            when placing closets next to this if object is hidden
            For now set x, y, z object to not be hidden.
        '''
        self.closet.obj_x.hide_viewport = hide
        self.closet.obj_y.hide_viewport = hide
        self.closet.obj_z.hide_viewport = hide
        self.closet.obj_x.empty_display_size = .001
        self.closet.obj_y.empty_display_size = .001
        self.closet.obj_z.empty_display_size = .001

    def finish(self, context):
        context.window.cursor_set('DEFAULT')
        if self.drawing_plane:
            sn_utils.delete_obj_list([self.drawing_plane])
        self.set_placed_properties(self.closet.obj_bp) 
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        return {'FINISHED'}


class Delete_Closet_Assembly(Operator):

    obj_bp = None

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label(text="'{}'".format(self.obj_bp.snap.name_object))
        col.label(text="Are you sure you want to delete this?")

class SNAP_OT_delete_closet(Delete_Closet_Assembly):
    bl_idname = "sn_closets.delete_closet"
    bl_label = "Delete Closet"

    def invoke(self, context, event):
        self.obj_bp = sn_utils.get_closet_bp(context.object)
        return super().invoke(context, event)

    def execute(self, context):
        has_bool = 'IS_BP_WINDOW' in self.obj_bp or 'IS_BP_ENTRY_DOOR' in self.obj_bp
        wall = self.obj_bp.parent
        sn_utils.delete_object_and_children(self.obj_bp)

        # if it is an entry window or door, we need to remove the bool modifier
        if wall and has_bool:
            wall_mesh = None
            for child in wall.children:
                if 'Wall' in child.name and child.type == 'MESH':
                    wall_mesh = child
                    break
            if wall_mesh:
                for mod in wall_mesh.modifiers:
                    if mod.type == 'BOOLEAN' and mod.object is None:
                        wall_mesh.modifiers.remove(mod)

        return {'FINISHED'}


class SNAP_OT_delete_closet_insert(Delete_Closet_Assembly):
    bl_idname = "sn_closets.delete_closet_insert"
    bl_label = "Delete Insert"

    @classmethod
    def poll(cls, context):
        insert_bp = sn_utils.get_bp(context.object, 'INSERT')
        if insert_bp:
            return True
        else:
            return False

    def invoke(self, context, event):
        self.obj_bp = sn_utils.get_bp(context.object, 'INSERT')
        return super().invoke(context, event)

    def make_opening_available(self, obj_bp):
        insert = sn_types.Assembly(obj_bp)
        if obj_bp.parent:
            for child in obj_bp.parent.children:
                if child.snap.type_group == 'OPENING' and insert.obj_bp.location.x == child.location.x:
                    if insert.obj_bp.snap.placement_type == 'SPLITTER':
                        child.snap.interior_open = True
                        child.snap.exterior_open = True
                        break
                    if insert.obj_bp.snap.placement_type == 'INTERIOR':
                        child.snap.interior_open = True
                        break
                    if insert.obj_bp.snap.placement_type == 'EXTERIOR':
                        if insert.obj_bp.get('IS_BP_DOOR_INSERT'):
                            child.snap.interior_open = True
                        child.snap.exterior_open = True
                        break

    def execute(self, context):
        start_time = time.perf_counter()
        insert_name = self.obj_bp.snap.name_object
        self.make_opening_available(self.obj_bp)
        obs = len(bpy.data.objects)
        vis_obs = len([ob for ob in bpy.context.view_layer.objects if ob.visible_get()])
        sn_utils.delete_object_and_children(self.obj_bp)

        print("{}: ({}) --- {} seconds --- Objects in scene: {} ({} visible)".format(
            self.bl_idname,
            insert_name,
            round(time.perf_counter() - start_time, 8),
            obs,
            vis_obs))

        return {'FINISHED'}


class SNAP_OT_delete_part(Operator):
    bl_idname = "sn_closets.delete_part"
    bl_label = "Delete Closet"

    def execute(self, context):
        obj_bp = sn_utils.get_assembly_bp(context.object)
        sn_utils.delete_object_and_children(obj_bp)
        return {'FINISHED'}


class SNAP_OT_part_prompts(Operator):
    bl_idname = "sn_closets.part_prompts"
    bl_label = "Delete Closet"

    assembly = None

    def invoke(self,context,event):
        bp = sn_utils.get_assembly_bp(context.object)
        self.assembly = sn_types.Assembly(bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=350)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        self.assembly.obj_prompts.snap.draw_prompts(box)

    def execute(self, context):
        return {'FINISHED'}


class SNAP_OT_update_prompts(Operator):
    bl_idname = "sn_closets.update_prompts"
    bl_label = "Update Prompts"

    def execute(self, context):
        return {'FINISHED'}


class SNAP_OT_hardlock_part_size(Operator):
    bl_idname = "sn_closets.hardlock_part_size"
    bl_label = "Hardlock Part Size"

    @classmethod
    def poll(cls, context):
        obj_bp = sn_utils.get_assembly_bp(context.object)
        if obj_bp:
            for child in obj_bp.children:
                if child.type == 'MESH':
                    for mod in child.modifiers:
                        if mod.type == 'HOOK':
                            return True
        return False

    def execute(self, context):
        obj_bps = []
        for obj in context.selected_objects:
            obj_bp = sn_utils.get_assembly_bp(obj)
            if obj_bp is not None and obj_bp not in obj_bps:
                obj_bps.append(obj_bp)

        for obj_bp in obj_bps:
            for child in obj_bp.children:
                if child.type == 'MESH':
                    sn_utils.apply_hook_modifiers(context,child)
        return {'FINISHED'}


class SNAP_OT_copy_product(Operator):
    bl_idname = "sn_closets.copy_product"
    bl_label = "Copy Product"

    obj_bp_name: bpy.props.StringProperty(name="Obj Base Point Name")

    @classmethod
    def poll(cls, context):
        obj_bp = sn_utils.get_closet_bp(context.object)
        if obj_bp:
            return True
        else:
            return False

    def mute_hide_viewport_driver(self, obj, mute=True):
        if obj.animation_data:
            for driver in obj.animation_data.drivers:
                if driver.data_path == "hide_viewport":
                    driver.mute = mute

    def select_obj_and_children(self, obj):
        self.mute_hide_viewport_driver(obj, mute=True)
        obj.hide_viewport = False
        obj.hide_set(False)
        obj.select_set(True)
        for child in obj.children:
            obj.hide_viewport = False
            obj.hide_set(False)
            child.select_set(True)
            self.select_obj_and_children(child)

    def hide_empties_and_boolean_meshes(self, obj):
        if obj.type == 'EMPTY' or obj.hide_render:
            obj.hide_viewport = True
            self.mute_hide_viewport_driver(obj, mute=False)
        for child in obj.children:
            self.hide_empties_and_boolean_meshes(child)

    def execute(self, context):
        obj = context.object
        obj_bp = sn_utils.get_closet_bp(obj)
        closet = sn_types.Assembly(obj_bp)
        bpy.ops.object.select_all(action='DESELECT')
        self.select_obj_and_children(closet.obj_bp)
        bpy.ops.object.duplicate_move()
        self.hide_empties_and_boolean_meshes(closet.obj_bp)

        obj = context.object
        new_obj_bp = sn_utils.get_closet_bp(obj)
        new_closet = sn_types.Assembly(new_obj_bp)
        self.hide_empties_and_boolean_meshes(new_closet.obj_bp)

        bpy.ops.sn_closets.move_closet(obj_bp_name=new_closet.obj_bp.name)

        return {'FINISHED'}


class SNAP_OT_copy_insert(Operator):
    bl_idname = "sn_closets.copy_insert"
    bl_label = "Copy Insert"

    @classmethod
    def poll(cls, context):
        insert_bp = sn_utils.get_bp(context.object, 'INSERT')
        if insert_bp:
            return True
        else:
            return False

    def clear_drivers(self, assembly):
        assembly.obj_bp.parent = None
        assembly.obj_bp.driver_remove('location', 0)
        assembly.obj_bp.driver_remove('location', 1)
        assembly.obj_bp.driver_remove('location', 2)
        assembly.obj_x.driver_remove('location', 0)
        assembly.obj_y.driver_remove('location', 1)
        assembly.obj_z.driver_remove('location', 2)

    def execute(self, context):
        obj_bp = sn_utils.get_bp(context.object, 'INSERT')
        opening = obj_bp.sn_closets.opening_name
        closet_origin = obj_bp.parent
        closet_origin_assembly = sn_types.Assembly(obj_bp=closet_origin)
        bottom_shelf =\
            closet_origin_assembly.get_prompt(
                'Remove Bottom Hanging Shelf ' + str(opening))
        top_shelf =\
            closet_origin_assembly.get_prompt(
                'Remove Top Shelf ' + str(opening))
        if bottom_shelf and top_shelf:
            bottom_shelf_value = bottom_shelf.get_value()
            top_shelf_value = top_shelf.get_value()
        else:
            bottom_shelf_value = False
            top_shelf_value = False

        if obj_bp:
            obj_list = []
            obj_list = sn_utils.get_child_objects(obj_bp, obj_list)
            bpy.ops.object.select_all(action='DESELECT')

            for obj in obj_list:
                if obj.type == 'EMPTY':
                    obj.hide_select = False
                    obj.hide_viewport = False
                obj.hide_set(False)
                obj.select_set(True)

            bpy.ops.object.duplicate()

            for obj in context.selected_objects:
                if obj.type == 'EMPTY':
                    obj.hide_set(True)
                    obj.hide_select = True
                    obj.hide_viewport = True

            for obj in obj_list:
                if obj.type == 'EMPTY':
                    obj.hide_set(True)
                if obj.get('IS_BP_ASSEMBLY'):
                    obj.hide_set(True)
                obj.location = obj.location

            bpy.ops.object.select_all(action='DESELECT')
            obj_bp.select_set(True)
            context.view_layer.objects.active = obj_bp

            insert = sn_types.Assembly(obj_bp=obj_bp)

            self.clear_drivers(insert)

            if 'ID_DROP' in obj_bp:
                custom_drop_id = [
                    "sn_closets.top_shelf_drop",  # Top shelf
                    "sn_closets.bottom_capping_drop",  # Bottom capping
                    "sn_closets.place_countertop",  # Countertop
                    "sn_closets.top_drop",  # Flat crown, light rail, valence
                    "sn_closets.place_base_assembly",  # Toe kick
                    "sn_closets.place_single_part"]  # Slanted shoe shelf

                id_drop = obj_bp.get('ID_DROP')
                if id_drop in custom_drop_id:
                    eval('bpy.ops.{}("INVOKE_DEFAULT", obj_bp_name=obj_bp.name)'.format(id_drop))
                    return {'FINISHED'}

            bpy.ops.sn_closets.copy_insert_drop(
                "EXEC_DEFAULT",
                obj_bp_name=insert.obj_bp.name,
                origin_top_shelf=top_shelf_value,
                origin_bottom_shelf=bottom_shelf_value)

        return {'FINISHED'}


class SNAP_OT_Assembly_Copy_Drop(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.copy_insert_drop"
    bl_label = "Drag and drop for copied assemblies"
    bl_description = "This places a copy of an assembly"
    bl_options = {'UNDO'}

    insert = None
    origin_top_shelf: bpy.props.BoolProperty(name="Origin Top Shelf", default=False)  # noqa F722
    origin_bottom_shelf: bpy.props.BoolProperty(name="Origin Bottom Shelf", default=False)  # noqa F722

    def modal(self, context, event):
        self.run_asset_calculators()
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        self.reset_selection()

        if len(self.openings) == 0:
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT',
                message="There are no openings in this scene.")
            context.area.header_text_set(None)
            return self.cancel_drop(context)
        self.selected_point, self.selected_obj, ignore =\
            sn_utils.get_selection_point(
                context, event,
                objects=self.include_objects,
                exclude_objects=self.exclude_objects)
        self.position_asset(context)

        if self.event_is_place_first_point(event) and self.selected_opening:
            self.confirm_placement(context)
            self.set_top_bottom_KD()
            return self.finish(context)
        if self.event_is_cancel_command(event):
            return self.cancel_drop(context)
        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.insert = self.asset
        return super().execute(context)

    def set_top_bottom_KD(self):
        closet_copy = self.insert.obj_bp.parent
        closet_copy_assembly = sn_types.Assembly(obj_bp=closet_copy)
        copy_opening =\
            self.insert.obj_bp.sn_closets.opening_name
        bottom_shelf_cp =\
            closet_copy_assembly.get_prompt(
                'Remove Bottom Hanging Shelf ' + str(copy_opening))
        top_shelf_cp =\
            closet_copy_assembly.get_prompt(
                'Remove Top Shelf ' + str(copy_opening))
        if bottom_shelf_cp and top_shelf_cp:
            bottom_shelf_cp.set_value(self.origin_bottom_shelf)
            top_shelf_cp.set_value(self.origin_top_shelf)


class SNAP_OT_update_closet_section_height(Operator):
    bl_idname = "sn_closets.update_closet_section_height"
    bl_label = "Update Closet Section Height"
    bl_description = "Update the Closet Section Height"
    bl_options = {'UNDO'}

    update_hanging: bpy.props.BoolProperty(name="Update Hanging")

    def execute(self, context):
        scene_props = bpy.context.scene.sn_closets

        for obj in context.scene.objects:
            obj_props = obj.sn_closets
            if obj_props.is_closet:
                closet = sn_types.Assembly(obj)

                for i in range(1, 10):
                    opening_height = closet.get_prompt("Opening " + str(i) + " Height")
                    floor_mounted = closet.get_prompt("Opening " + str(i) + " Floor Mounted")

                    if opening_height and floor_mounted:
                        if self.update_hanging:
                            if not floor_mounted.get_value():
                                opening_height.set_value(
                                    sn_unit.millimeter(float(scene_props.closet_defaults.hanging_panel_height)))
                        else:
                            if floor_mounted.get_value():
                                opening_height.set_value(
                                    sn_unit.millimeter(float(scene_props.closet_defaults.panel_height)))

                # FORCE REFRESH
                closet.obj_bp.location = closet.obj_bp.location

        return {'FINISHED'}


class SNAP_OT_update_closet_hanging_height(Operator):
    bl_idname = "sn_closets.update_closet_hanging_height"
    bl_label = "Update Closet Height"
    bl_description = "Update Closet Height"
    bl_options = {'UNDO'}

    def execute(self, context):
        scene_props = bpy.context.scene.sn_closets

        for obj in context.scene.objects:
            obj_props = obj.sn_closets
            if obj_props.is_closet:
                closet = sn_types.Assembly(obj)
                closet.obj_z.location.z = scene_props.closet_defaults.hanging_height

        return {'FINISHED'}


class SNAP_OT_combine_parts(Operator):
    bl_idname = "sn_closets.combine_parts"
    bl_label = "Combine Parts"
    bl_options = {'UNDO'}
    bl_description = """
    This will combine the length of all of the selected parts.
    (This is mainly used when the Use Plant on Top option is turned on
    and you want to join specific tops for cutlist purposes)
    """

    assemblies = []

    def invoke(self, context, event):
        self.assemblies = []
        for obj in context.selected_objects:
            assembly = sn_utils.get_assembly_bp(obj)
            if assembly not in self.assemblies:
                self.assemblies.append(assembly)

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(380))

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to combine these parts:")
        for part in self.assemblies:
            layout.label(text="Part Name: " + part.snap.name_object)

    def execute(self, context):
        self.assemblies.sort(key=lambda obj: obj.location.x, reverse=False)
        first_assembly = sn_types.Assembly(self.assemblies.pop(0))
        first_assembly.obj_x.driver_remove('location', 0)
        obj_list = []
        for assembly in self.assemblies:
            assembly = sn_types.Assembly(assembly)
            first_assembly.obj_x.location.x += assembly.obj_x.location.x
            obj_list = sn_utils.get_child_objects(assembly.obj_bp, obj_list)

        sn_utils.delete_obj_list(obj_list)
        return {'FINISHED'}


class SNAP_OT_update_pull_selection(Operator):
    bl_idname = "sn_closets.update_pull_selection"
    bl_label = "Change Pulls"
    bl_description = "This will update all of the door pulls that are currently selected"
    bl_options = {'UNDO'}

    update_all: bpy.props.BoolProperty(name="Update All", default=False)

    def execute(self, context):
        props = bpy.context.scene.sn_closets.closet_options
        pulls = []

        if self.update_all:
            for obj in context.scene.objects:
                if obj.snap.is_cabinet_pull:
                    pulls.append(obj)
        else:
            for obj in context.selected_objects:
                if obj.snap.is_cabinet_pull:
                    pulls.append(obj)

        for pull in pulls:
            pull_assembly = sn_types.Assembly(pull.parent)
            pull_assembly.set_name(props.pull_name)
            pull_length = pull_assembly.get_prompt("Pull Length")
            new_pull = sn_utils.get_object(
                os.path.join(
                    os.path.dirname(__file__),
                    closet_paths.get_root_dir(),
                    closet_props.PULL_FOLDER_NAME,
                    props.pull_category,
                    props.pull_name + ".blend"))
            new_pull.snap.is_cabinet_pull = True
            new_pull.snap.type_mesh = 'HARDWARE'
            new_pull.snap.name_object = props.pull_name
            new_pull.snap.comment = props.pull_name
            new_pull.parent = pull.parent
            new_pull.location = pull.location
            new_pull.rotation_euler = pull.rotation_euler
            active_layer = context.view_layer.active_layer_collection
            active_layer.collection.objects.link(new_pull)

            if len(new_pull.snap.material_slots) < 1:
                bpy.ops.sn_material.add_material_pointers(object_name=new_pull.name)
            for slot in new_pull.snap.material_slots:
                slot.category_name = "Finished Metals"
                slot.item_name = props.pull_category
            sn_utils.assign_materials_from_pointers(new_pull)

            pull_length.set_value(new_pull.dimensions.x)
            sn_utils.copy_drivers(pull, new_pull)

        sn_utils.delete_obj_list(pulls)

        return {'FINISHED'}


class SNAP_OT_place_applied_panel(Operator):
    bl_idname = "sn_closets.place_applied_panel"
    bl_label = "Place Applied Panel"
    bl_description = "This will allow you to place the active panel on cabinets and closets for an applied panel"
    bl_options = {'UNDO'}

    # READONLY
    filepath: bpy.props.StringProperty(name="Material Name")
    type_insert: bpy.props.StringProperty(name="Type Insert")

    item_name = None
    dir_name = ""

    assembly = None
    selected_obj = None
    selected_point = None
    sel_product_bp = None
    sel_panel = None
    panel_bps = []

    def update_door_children_properties(self, obj, id_prompt, door_style):
        obj["ID_PROMPT"] = id_prompt
        if obj.type == 'EMPTY':
            obj.hide_set(True)
        if obj.type in ('MESH', 'CURVE'):
            self.set_door_material_pointers(obj)
            obj.display_type = 'TEXTURED'
            obj.snap.comment = door_style
            sn_utils.assign_materials_from_pointers(obj)
        if obj.get('IS_CAGE') is True:
            obj.hide_set(True)
        for child in obj.children:
            self.update_door_children_properties(
                child, id_prompt, door_style)

    def get_panel(self, context):
        props = bpy.context.scene.sn_closets.closet_options
        bp = sn_utils.get_group(
            os.path.join(
                closet_paths.get_asset_folder_path(),
                closet_props.DOOR_FOLDER_NAME,
                props.door_category,
                props.door_style + ".blend"))

        self.assembly = sn_types.Assembly(bp)
        self.assembly.obj_bp["ALLOW_PART_DELETE"] = True
        self.assembly.set_name(props.door_style)

    def set_door_material_pointers(self, obj):
        for index, slot in enumerate(obj.snap.material_slots):
            if slot.name == 'Moderno':
                slot.pointer_name = "Moderno_Door"
            if slot.name == 'Glass Panel':
                slot.pointer_name = "Glass"
            if slot.name == 'Door Panel':
                slot.pointer_name = "Wood_Door_Surface"

    def set_wire_and_xray(self, obj, turn_on):
        if turn_on:
            obj.display_type = 'WIRE'
        else:
            obj.display_type = 'TEXTURED'
        obj.show_in_front = turn_on
        for child in obj.children:
            self.set_wire_and_xray(child, turn_on)

    def invoke(self, context, event):
        self.get_panel(context)
        context.window.cursor_set('PAINT_BRUSH')
        context.view_layer.update()  # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self, context, event):
        if self.assembly:
            sn_utils.delete_object_and_children(self.assembly.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def add_to_left(self, part):
        self.assembly.obj_bp.parent = part.obj_bp
        self.assembly.obj_bp.location.y = part.obj_y.location.y
        self.assembly.obj_y.location.y = math.fabs(part.obj_y.location.y)
        self.assembly.obj_x.location.x = part.obj_x.location.x

    def add_to_right(self, part):
        self.assembly.obj_bp.parent = part.obj_bp
        self.assembly.obj_bp.rotation_euler.x = math.radians(-180)
        self.assembly.obj_y.location.y = math.fabs(part.obj_y.location.y)
        self.assembly.obj_x.location.x = part.obj_x.location.x

    def add_to_back(self, part, product):
        self.assembly.obj_bp.parent = product.obj_bp

        toe_kick_height = 0
        if product.get_prompt('Toe Kick Height'):
            toe_kick_height = product.get_prompt('Toe Kick Height')

        if product.obj_z.location.z > 0:
            self.assembly.obj_bp.location = (0, 0, toe_kick_height)
        else:
            self.assembly.obj_bp.location = (0, 0, product.obj_z.location.z)

        self.assembly.obj_bp.rotation_euler = (
            0, math.radians(-90), math.radians(-90))
        self.assembly.obj_x.location.x = math.fabs(
            product.obj_z.location.z) - toe_kick_height
        self.assembly.obj_y.location.y = product.obj_x.location.x

    def is_first_panel(self, panel):
        if panel.obj_z.location.z < 0:
            return True
        else:
            return False

    def is_last_panel(self, panel):
        self.get_panels()
        last_panel_bp = self.panel_bps[-1]
        if panel.obj_bp is last_panel_bp:
            return True
        else:
            return False

    def get_panels(self):
        self.panel_bps.clear()
        for child in self.sel_product_bp.children:
            if 'IS_BP_PANEL' in child and 'PARTITION_NUMBER' in child:
                self.panel_bps.append(child)
        self.panel_bps.sort(key=lambda a: int(a['PARTITION_NUMBER']))

    def door_panel_drop(self, context, event):
        props = context.scene.sn_closets.closet_options
        self.sel_product_bp = sn_utils.get_bp(self.selected_obj, 'PRODUCT')
        sel_assembly_bp = sn_utils.get_assembly_bp(self.selected_obj)

        if sel_assembly_bp and self.sel_product_bp:
            sel_assembly = sn_types.Assembly(sel_assembly_bp)
            if sel_assembly and 'Door' not in sel_assembly.obj_bp.snap.name_object:
                if sel_assembly.obj_bp.sn_closets.is_panel_bp:
                    self.sel_panel = sel_assembly
                    self.assembly.obj_bp.parent = None
                    self.assembly.obj_bp.location = (0, 0, 0)
                    self.assembly.obj_bp.rotation_euler = (0, 0, 0)

                    if self.is_first_panel(sel_assembly):
                        self.add_to_left(sel_assembly)
                    if self.is_last_panel(sel_assembly):
                        self.add_to_right(sel_assembly)
        else:
            self.assembly.obj_bp.parent = None
            self.assembly.obj_bp.location = self.selected_point

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if not sel_assembly_bp:
                self.cancel_drop(context, event)
                return {'FINISHED'}
            self.set_wire_and_xray(self.assembly.obj_bp, False)
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = self.assembly.obj_bp
            self.assembly.obj_bp.select_set(True)
            self.update_door_children_properties(self.assembly.obj_bp, sel_assembly_bp["ID_PROMPT"], props.door_style)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        context.area.tag_redraw()
        bpy.ops.object.select_all(action='DESELECT')
        self.selected_point, self.selected_obj, _ = sn_utils.get_selection_point(context, event)

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel_drop(context, event)
            return {'FINISHED'}

        return self.door_panel_drop(context, event)


class SNAP_OT_update_door_selection(Operator):
    bl_idname = "sn_closets.update_door_selection"
    bl_label = "Update Door Selection"
    bl_description = "This will change the selected door with the active door"
    bl_options = {'UNDO'}

    cabinet_type: bpy.props.StringProperty(name="Cabinet Type")

    def update_door_children_properties(self, obj, id_prompt, door_style):
        obj["ID_PROMPT"] = id_prompt
        if obj.type == 'EMPTY':
            obj.hide_set(True)
        if obj.type in ('MESH', 'CURVE'):
            self.set_door_material_pointers(obj)
            obj.display_type = 'TEXTURED'
            obj.snap.comment = door_style
            sn_utils.assign_materials_from_pointers(obj)
        if obj.get('IS_CAGE') is True:
            obj.hide_set(True)
        for child in obj.children:
            self.update_door_children_properties(
                child, id_prompt, door_style)

    def set_door_material_pointers(self, obj):
        for index, slot in enumerate(obj.snap.material_slots):
            if slot.name == 'Moderno':
                slot.pointer_name = "Moderno_Door"
            if slot.name == 'Glass Panel':
                slot.pointer_name = "Glass"
            if slot.name == 'Door Panel':
                slot.pointer_name = "Wood_Door_Surface"

    def get_door_assembly(self, obj):
        is_door = obj.get("IS_DOOR")
        is_bp_drawer_front = obj.get("IS_BP_DRAWER_FRONT")
        if is_door or is_bp_drawer_front:
            return obj
        else:
            if obj.parent:
                return self.get_door_assembly(obj.parent)

    def execute(self, context):
        door_bps = []
        props = bpy.context.scene.sn_closets.closet_options
        for obj in context.selected_objects:
            door_bp = self.get_door_assembly(obj)
            if door_bp and door_bp not in door_bps:
                door_bps.append(door_bp)

        for obj_bp in door_bps:
            door_assembly = sn_types.Assembly(obj_bp)

            if props.door_category == "Slab Door":
                new_door = common_parts.add_door(sn_types.Assembly(obj_bp.parent))
                new_door.obj_bp.snap.name_object = door_assembly.obj_bp.snap.name_object
                new_door.obj_bp.name = door_assembly.obj_bp.name
                new_door.obj_bp.location = door_assembly.obj_bp.location
                new_door.obj_bp.rotation_euler = door_assembly.obj_bp.rotation_euler
                new_door.obj_bp.sn_closets.use_unique_material = False
                for child in new_door.obj_bp.children:
                    if child.type == 'MESH':
                        child.snap.type_mesh = 'CUTPART'

            else:
                group_bp = sn_utils.get_group(
                    os.path.join(closet_paths.get_asset_folder_path(),
                                 closet_props.DOOR_FOLDER_NAME,
                                 props.door_category,
                                 props.door_style + ".blend"))

                new_door = sn_types.Assembly(group_bp)

                if props.door_category == '5 Piece Doors':
                    new_door.obj_bp.snap.comment_2 == '1111'
                if props.door_category == 'Deco Panels':
                    new_door.obj_bp.snap.comment_2 == '2222'

                new_door.obj_bp.snap.name_object = door_assembly.obj_bp.snap.name_object
                if "left" in door_assembly.obj_bp.name.lower():
                    new_door.obj_bp.name = "Left " + new_door.obj_bp.name
                if "right" in door_assembly.obj_bp.name.lower():
                    new_door.obj_bp.name = "Right " + new_door.obj_bp.name
                new_door.obj_bp.parent = door_assembly.obj_bp.parent
                new_door.obj_bp.location = door_assembly.obj_bp.location
                new_door.obj_bp.rotation_euler = door_assembly.obj_bp.rotation_euler
                for child in new_door.obj_bp.children:
                    if child.type == 'MESH':
                        child.snap.type_mesh = 'BUYOUT'

            id_prompt = door_assembly.obj_bp.get("ID_PROMPT")

            sn_utils.copy_assembly_prompts(door_assembly, new_door)
            sn_utils.copy_drivers(door_assembly.obj_bp, new_door.obj_bp)
            sn_utils.copy_prompt_drivers(door_assembly.obj_bp, new_door.obj_bp)
            sn_utils.copy_drivers(door_assembly.obj_x, new_door.obj_x)
            sn_utils.copy_drivers(door_assembly.obj_y, new_door.obj_y)
            sn_utils.copy_drivers(door_assembly.obj_z, new_door.obj_z)

            obj_props = new_door.obj_bp.sn_closets
            obj_props.is_door_bp = door_assembly.obj_bp.sn_closets.is_door_bp
            obj_props.is_drawer_front_bp = door_assembly.obj_bp.sn_closets.is_drawer_front_bp
            obj_props.is_hamper_front_bp = door_assembly.obj_bp.sn_closets.is_hamper_front_bp
            obj_props.opening_name = door_assembly.obj_bp.sn_closets.opening_name
            new_door.obj_bp.snap.comment = door_assembly.obj_bp.snap.comment
            new_door.obj_bp.snap.comment_2 = door_assembly.obj_bp.snap.comment_2

            new_door.obj_bp["ID_PROMPT"] = id_prompt

            if obj_props.is_door_bp:
                new_door.obj_bp['IS_DOOR'] = True
            if obj_props.is_drawer_front_bp:
                new_door.obj_bp['DRAWER_NUM'] = door_assembly.obj_bp.get("DRAWER_NUM")
                new_door.obj_bp['IS_BP_DRAWER_FRONT'] = True
            if obj_props.is_hamper_front_bp:
                new_door.obj_bp['IS_BP_HAMPER_FRONT'] = True

            sn_utils.delete_obj_list(sn_utils.get_child_objects(door_assembly.obj_bp, []))

            parent_assembly = sn_types.Assembly(new_door.obj_bp.parent)
            parent_door_style = parent_assembly.get_prompt("Door Style")
            new_door.add_prompt("Door Style", 'TEXT', "Slab Door")
            door_style = new_door.get_prompt("Door Style")
            if(door_style):
                door_style.set_value(props.door_style)
            if(parent_door_style):
                parent_door_style.set_value(props.door_style)
            self.update_door_children_properties(new_door.obj_bp, id_prompt, props.door_style)

        return {'FINISHED'}


class SNAP_OT_Auto_Add_Molding(Operator):
    bl_idname = "sn_closets.auto_add_molding"
    bl_label = "Add Molding"
    bl_options = {'UNDO'}

    molding_type: bpy.props.StringProperty(name="Molding Type")
    crown_to_ceiling: bpy.props.BoolProperty(name="Crown To Ceiling", default=False)

    crown_profile = None
    base_profile = None

    tall_cabinet_switch = sn_unit.inch(60)

    def get_profile(self):
        props = bpy.context.scene.sn_closets.closet_options
        if self.molding_type == 'Base':
            self.profile = sn_utils.get_object(
                os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    closet_props.BASE_MOLDING_FOLDER_NAME,
                    props.base_molding_category,
                    props.base_molding + ".blend"))
        else:
            self.is_crown = True
            self.profile = sn_utils.get_object(
                os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    closet_props.CROWN_MOLDING_FOLDER_NAME,
                    props.crown_molding_category,
                    props.crown_molding + ".blend"))

        self.profile['IS_MOLDING_PROFILE'] = True
        bpy.context.scene.collection.objects.link(self.profile)


    def get_products(self):
        products = []
        for obj in bpy.context.scene.objects:
            if obj.get('product_type') == "Closet":
                product = sn_types.Assembly(obj)
                products.append(product)
        return products

    def create_extrusion(self, points, is_crown=True, product=None):
        if self.profile is None:
            self.get_profile()

        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False)
        obj_curve = bpy.context.active_object
        obj_curve.modifiers.new("Edge Split", type='EDGE_SPLIT')
        obj_props = obj_curve.sn_closets
        if is_crown:
            obj_props.is_crown_molding = True
        else:
            obj_props.is_base_molding = True
        obj_curve.data.splines.clear()
        spline = obj_curve.data.splines.new('BEZIER')
        spline.bezier_points.add(count=len(points) - 1)
        obj_curve.data.bevel_object = self.profile
        if hasattr(obj_curve.data, 'bevel_mode'):
            obj_curve.data.bevel_mode = 'OBJECT'
        obj_curve.snap.spec_group_index = product.obj_bp.snap.spec_group_index

        bpy.ops.sn_object.add_material_slot(object_name=obj_curve.name)
        bpy.ops.sn_material.sync_material_slots(object_name=obj_curve.name)
        obj_curve.snap.material_slots[0].pointer_name = "Molding"

        obj_curve.location = (0, 0, 0)

        for i, point in enumerate(points):
            obj_curve.data.splines[0].bezier_points[i].co = point

        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.ops.object.editmode_toggle()
        obj_curve.data.dimensions = '2D'
        obj_curve.data.use_fill_caps = True

        active_specgroup = bpy.context.scene.snap.spec_groups[bpy.context.scene.snap.spec_group_index]
        pointer = active_specgroup.materials["Molding"]

        surface_material = sn_utils.get_material(pointer.category_name, pointer.item_name)

        for index, slot in enumerate(obj_curve.snap.material_slots):
            obj_curve.material_slots[index].material = surface_material
        return obj_curve

    def clean_up_room(self):
        """ Removes all of the Dimensions and other objects
            That were added to the scene from this command
            We dont want multiple objects added on top of each other
            So we must clean up the scene before running this command
        """
        is_crown = True if self.molding_type == 'Crown' else False
        objs = []
        for obj in bpy.data.objects:
            obj_props = obj.sn_closets

            if obj.type == 'CURVE':
                if is_crown:
                    if obj_props.is_crown_molding:
                        objs.append(obj)
                else:
                    if obj_props.is_base_molding:
                        objs.append(obj)
        sn_utils.delete_obj_list(objs)

    def set_curve_location(self, product, curve, is_crown):
        curve.parent = product.obj_bp
        if is_crown and curve.type == 'CURVE':
            if product.obj_z.location.z < 0:
                curve.location.z = 0
            else:
                curve.location.z = product.obj_z.location.z

    def add_molding(self, product, is_crown=True):
        thickness = product.get_prompt("Panel Thickness")
        left_end_condition = product.get_prompt("Left End Condition")
        right_end_condition = product.get_prompt("Right End Condition")
        toe_kick_height = product.get_prompt('Toe Kick Height')
        if left_end_condition and right_end_condition:
            start_x = 0
            for i in range(1, 10):
                points = []
                width = product.get_prompt("Opening " + str(i) + " Width")

                if width:
                    next_width = product.get_prompt("Opening " + str(i + 1) + " Width")
                    height = product.get_prompt("Opening " + str(i) + " Height")
                    depth = product.get_prompt("Opening " + str(i) + " Depth")
                    floor = product.get_prompt("Opening " + str(i) + " Floor Mounted")

                    if floor:
                        if is_crown and height.get_value() < sn_unit.inch(50) and floor and floor.get_value():
                            continue  # DONT ADD MOLDING TO UNITS SMALLER THAN 50"

                        if not is_crown and floor and not floor.get_value():
                            start_x += width.get_value()
                            if left_end_condition and left_end_condition.get_value() != 'OFF':
                                start_x += thickness.get_value()
                            continue

                        if i == 1:  # FIRST
                            left_side_wall_filler = product.get_prompt(
                                "Left Side Wall Filler")

                            next_height = product.get_prompt("Opening " + str(i + 1) + " Height")
                            next_depth = product.get_prompt("Opening " + str(i + 1) + " Depth")

                            if left_side_wall_filler and left_side_wall_filler.get_value() > 0:
                                points.append((0, -depth.get_value(), 0))

                            else:
                                if left_end_condition.get_value() == 0:
                                    points.append((0, 0, 0))
                                    points.append((0, -depth.get_value(), 0))
                                else:
                                    points.append((0, -depth.get_value(), 0))

                            if next_height:

                                if (height.get_value() > next_height.get_value()) or (depth.get_value() > next_depth.get_value()):
                                    left_side_thickness = product.get_prompt(
                                        "Left Side Thickness")
                                    start_x = width.get_value() + left_side_thickness.get_value() + \
                                        thickness.get_value() + left_side_wall_filler.get_value()
                                    points.append((start_x, -depth.get_value(), 0))
                                    points.append((start_x, 0, 0))
                                else:
                                    left_side_thickness = product.get_prompt("Left Side Thickness")
                                    start_x = width.get_value() + left_side_thickness.get_value() + left_side_wall_filler.get_value()
                                    points.append((start_x, -depth.get_value(), 0))

                            else:  # USED ONLY WHEN A SINGLE OPENING IS BEING CREATED

                                right_side_wall_filler = product.get_prompt("Right Side Wall Filler")

                                if right_side_wall_filler and right_side_wall_filler.get_value() > 0:
                                    start_x += width.get_value() + thickness.get_value() + right_side_wall_filler.get_value()
                                    points.append((start_x, -depth.get_value(), 0))
                                else:

                                    if right_end_condition.get_value() == 0:
                                        start_x += width.get_value() + (thickness.get_value() * 2)
                                        points.append(
                                            (start_x, -depth.get_value(), 0))
                                        points.append((start_x, 0, 0))
                                    else:
                                        start_x += width.get_value() + (thickness.get_value() * 2)
                                        points.append(
                                            (start_x, -depth.get_value(), 0))
                        # MIDDLE
                        elif next_width:
                            prev_height = product.get_prompt("Opening " + str(i - 1) + " Height")
                            prev_depth = product.get_prompt("Opening " + str(i - 1) + " Depth")
                            next_height = product.get_prompt("Opening " + str(i + 1) + " Height")
                            next_depth = product.get_prompt("Opening " + str(i + 1) + " Depth")

                            if (height.get_value() > prev_height.get_value()) or (depth.get_value() > prev_depth.get_value()):
                                points.append((start_x, 0, 0))
                                points.append((start_x, -depth.get_value(), 0))
                                start_x += thickness.get_value()
                            else:
                                points.append((start_x, -depth.get_value(), 0))
                                start_x += thickness.get_value()

                            if (height.get_value() > next_height.get_value()) or (depth.get_value() > next_depth.get_value()):
                                start_x += width.get_value() + thickness.get_value()
                                points.append((start_x, -depth.get_value(), 0))
                                points.append((start_x, 0, 0))
                            else:
                                start_x += width.get_value()
                                points.append((start_x, -depth.get_value(), 0))

                        else:  # LAST
                            right_side_wall_filler = product.get_prompt("Right Side Wall Filler")
                            right_end_condition = product.get_prompt("Right End Condition")
                            prev_height = product.get_prompt("Opening " + str(i - 1) + " Height")
                            prev_depth = product.get_prompt("Opening " + str(i - 1) + " Depth")

                            if (height.get_value() > prev_height.get_value()) or (depth.get_value() > prev_depth.get_value()):
                                points.append((start_x, 0, 0))
                                points.append((start_x, -depth.get_value(), 0))
                                start_x += thickness.get_value()
                            else:
                                points.append((start_x, -depth.get_value(), 0))
                                start_x += thickness.get_value()

                            if right_side_wall_filler and right_side_wall_filler.get_value() > 0:
                                start_x += width.get_value() + thickness.get_value() + right_side_wall_filler.get_value()
                                points.append((start_x, -depth.get_value(), 0))
                            else:

                                if right_end_condition.get_value() == 0:
                                    start_x += width.get_value()
                                    points.append((start_x, -depth.get_value(), 0))
                                    points.append((start_x, 0, 0))
                                else:
                                    start_x += width.get_value() + thickness.get_value()
                                    points.append((start_x, -depth.get_value(), 0))

                        empty_assembly = sn_types.Assembly()
                        empty_assembly.create_assembly()
                        empty_assembly.obj_bp.snap.type_mesh = 'CUTPART'
                        empty_assembly.obj_x.hide_set(True)
                        empty_assembly.obj_y.hide_set(True)
                        empty_assembly.obj_z.hide_set(True)

                        curve = self.create_extrusion(points, is_crown, product)
                        curve.parent = empty_assembly.obj_bp
                        curve['ID_PROMPT'] = product.obj_bp.get('ID_PROMPT')

                        empty_assembly.obj_bp.parent = product.obj_bp

                        length = 0
                        if(len(curve.data.splines[0].bezier_points) == 3):
                            x1 = curve.data.splines[0].bezier_points[0].co[0]
                            x2 = curve.data.splines[0].bezier_points[1].co[0]
                            x3 = curve.data.splines[0].bezier_points[2].co[0]
                            y1 = curve.data.splines[0].bezier_points[0].co[1]
                            y2 = curve.data.splines[0].bezier_points[1].co[1]
                            y3 = curve.data.splines[0].bezier_points[2].co[1]
                            if(x1 == x2):
                                length += abs(x1 - x3)
                            if(x1 == x3):
                                length += abs(x1 - x2)
                            if(x2 == x3):
                                length += abs(x3 - x1)
                            if(y1 == y2):
                                length += abs(y1 - y3)
                            if(y1 == y3):
                                length += abs(y1 - y2)
                            if(y2 == y3):
                                length += abs(y3 - y1)

                        else:
                            x1 = curve.data.splines[0].bezier_points[0].co[0]
                            x2 = curve.data.splines[0].bezier_points[1].co[0]
                            y1 = curve.data.splines[0].bezier_points[0].co[1]
                            y2 = curve.data.splines[0].bezier_points[1].co[1]
                            length += abs(x1 - x2)
                            length += abs(y1 - y2)

                        empty_assembly.obj_x.location.x = length
                        empty_assembly.obj_z.location.z = sn_unit.inch(3)

                        obj_props = empty_assembly.obj_bp.sn_closets
                        props = bpy.context.scene.sn_closets.closet_options
                        obj_props.is_empty_molding = True
                        if is_crown:
                            obj_props.is_crown_molding = True
                            empty_assembly.obj_bp.snap.name_object = props.crown_molding
                            empty_assembly.add_prompt("Crown To Ceiling", 'CHECKBOX', self.crown_to_ceiling)

                            if floor.get_value():
                                curve.location.z = height.get_value()
                                if toe_kick_height:
                                    curve.location.z += toe_kick_height.get_value()
                            else:
                                curve.location.z = product.obj_z.location.z
                        else:
                            obj_props.is_base_molding = True
                            empty_assembly.obj_bp.snap.name_object = props.base_molding

    def add_hutch_molding(self, product, is_crown=True):
        points = []
        current_x = 0

        thickness = product.get_prompt("Panel Thickness")

        for i in range(1, 10):
            width = product.get_prompt("Opening " + str(i) + " Width")
            double_panel = product.get_prompt("Double Center Panel " + str(i))

            if width:
                depth = product.get_prompt("Opening " + str(i) + " Depth")
                next_depth = product.get_prompt("Opening " + str(i + 1) + " Depth")

                # FIRST POINT ON OPENING
                points.append((current_x, -depth.get_value(), 0))

                if i == 1:
                    current_x += thickness.get_value()
                    # LEFT SIDE THICKNESS
                    points.append((current_x, -depth.get_value(), 0))

                current_x += width.get_value()
                # WIDTH OF OPENING
                points.append((current_x, -depth.get_value(), 0))

                if next_depth:
                    if next_depth.get_value() > depth.get_value():

                        if double_panel and double_panel.get_value():
                            current_x += thickness.get_value()
                            # DOUBLE PANEL THICKNESS
                            points.append((current_x, -depth.get_value(), 0))

                        # NEXT DEPTH
                        points.append((current_x, -next_depth.get_value(), 0))
                        current_x += thickness.get_value()

                    elif next_depth.get_value() < depth.get_value():
                        current_x += thickness.get_value()
                        # NEXT DEPTH
                        points.append((current_x, -depth.get_value(), 0))
                        # NEXT DEPTH
                        points.append((current_x, -next_depth.get_value(), 0))

                        if double_panel and double_panel.get_value():
                            current_x += thickness.get_value()
                            # DOUBLE PANEL THICKNESS
                            points.append((current_x, -next_depth.get_value(), 0))

                    else:
                        current_x += thickness.get_value()

                        if double_panel and double_panel.get_value():
                            current_x += thickness.get_value()
                            # DOUBLE PANEL THICKNESS
                            points.append((current_x, -depth.get_value(), 0))

                else:
                    current_x += thickness.get_value()
                    # RIGHT SIDE THICKNESS
                    points.append((current_x, -depth.get_value(), 0))

        curve = self.create_extrusion(points, is_crown, product)
        curve.parent = product.obj_bp
        curve['ID_PROMPT'] = product.obj_bp.get('ID_PROMPT')
        curve.location.z = product.obj_z.location.z

    def add_island_molding(self, product):
        width = product.obj_x.location.x
        depth = product.obj_y.location.y

        points = []
        points.append((width / 2, 0, 0))
        points.append((0, 0, 0))
        points.append((0, depth, 0))
        points.append((width, depth, 0))
        points.append((width, 0, 0))
        points.append((width / 2, 0, 0))

        curve = self.create_extrusion(points, False, product)
        curve.parent = product.obj_bp
        curve['ID_PROMPT'] = product.obj_bp.get('ID_PROMPT')
        curve.location.z = 0

    # TODO: 2.1.0 Fix crown to ceiling option
    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     if self.molding_type == 'Crown':
    #         return wm.invoke_props_dialog(self, width=400)
    #     else:
    #         return self.execute(context)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Crown to Ceiling ")
        row.prop(self, 'crown_to_ceiling', text="")

    def execute(self, context):
        self.clean_up_room()
        self.profile = None
        products = self.get_products()
        for product in products:
            obj_props = product.obj_bp.sn_closets
            if obj_props.is_hutch and self.molding_type == 'Crown':
                self.add_hutch_molding(product)
            elif obj_props.is_island and self.molding_type == 'Base':
                self.add_island_molding(product)
            else:
                self.add_molding(product, True if self.molding_type == 'Crown' else False)
        return {'FINISHED'}


class SNAP_OT_Delete_Molding(Operator):
    bl_idname = "sn_closets.delete_molding"
    bl_label = "Delete Molding"
    bl_options = {'UNDO'}

    molding_type: bpy.props.StringProperty(name="Molding Type")

    def execute(self, context):
        is_crown = True if self.molding_type == 'Crown' else False
        objs = []
        for obj in context.scene.objects:
            obj_props = obj.sn_closets
            if is_crown:
                if obj_props.is_crown_molding:
                    objs.append(obj)
            else:
                if obj_props.is_base_molding:
                    objs.append(obj)
        sn_utils.delete_obj_list(objs)
        return {'FINISHED'}


class SNAP_OT_Update_Drawer_boxes(Operator):
    bl_idname = "sn_closets.update_drawer_boxes"
    bl_label = "Add/Remove Drawer Boxes"

    add: BoolProperty(name="Add Drawers", default=True)

    def execute(self, context):
        drawer_stack_bps = sn_utils.get_drawer_stack_bps()

        for bp in drawer_stack_bps:
            drawer_stack = data_drawers.Drawer_Stack(bp)
            drawer_qty_prompt = drawer_stack.get_prompt("Drawer Quantity")
            six_hole = drawer_stack.get_prompt("Six Hole")
            seven_hole = drawer_stack.get_prompt("Seven Hole")

            if self.add and not drawer_stack.drawer_boxes:
                drawer_stack.add_drawer_boxes()
                for i in range(1, drawer_qty_prompt.get_value()):
                    use_double_drawer = drawer_stack.get_prompt("Use Double Drawer " + str(i))
                    drawer_height = drawer_stack.get_prompt("Drawer " + str(i) + " Height")
                    if drawer_height is not None:
                        dbl_drawer_conditions = [
                            drawer_height.get_value() < six_hole.get_value(),
                            drawer_height.get_value() > seven_hole.get_value(),
                            drawer_stack.obj_y.location.y < sn_unit.inch(15.99)]
                        if any(dbl_drawer_conditions):
                            use_double_drawer.set_value(False)

                        if use_double_drawer.get_value():
                            drawer_stack.add_dbl_drawer_box(i)
                drawer_stack.update()

            elif not self.add and drawer_stack.drawer_boxes:
                for box in drawer_stack.drawer_boxes:
                    sn_utils.delete_object_and_children(box.obj_bp)

                for i in range(1, drawer_qty_prompt.get_value()):
                    dbl_drawer = drawer_stack.get_dbl_drawer_box(i)
                    if dbl_drawer:
                        sn_utils.delete_object_and_children(dbl_drawer.obj_bp)

            bpy.context.view_layer.update()

        return {'FINISHED'}


classes = (
    SNAP_OT_delete_closet,
    SNAP_OT_delete_closet_insert,
    SNAP_OT_delete_part,
    SNAP_OT_part_prompts,
    SNAP_OT_hardlock_part_size,
    SNAP_OT_update_prompts,
    SNAP_OT_move_closet,
    SNAP_OT_copy_product,
    SNAP_OT_copy_insert,
    SNAP_OT_update_closet_section_height,
    SNAP_OT_update_closet_hanging_height,
    SNAP_OT_combine_parts,
    SNAP_OT_update_pull_selection,
    SNAP_OT_place_applied_panel,
    SNAP_OT_update_door_selection,
    SNAP_OT_Auto_Add_Molding,
    SNAP_OT_Delete_Molding,
    SNAP_OT_Assembly_Copy_Drop,
    SNAP_OT_Update_Drawer_boxes
)

register, unregister = bpy.utils.register_classes_factory(classes)
