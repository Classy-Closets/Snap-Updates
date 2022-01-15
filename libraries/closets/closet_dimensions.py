from numpy.lib.function_base import diff
import bpy
import math
import mathutils
from snap.views import opengl_dim
from snap.views.view_ops import hide_dim_handles
from snap import sn_types, sn_unit, sn_utils
from snap.libraries.closets.data import data_drawers
from bpy.app.handlers import persistent
from bpy.utils import register_class, unregister_class
from . import closet_props as props_closet
from .common import common_lists
from bpy.types import Menu, PropertyGroup, Panel, Operator
from bpy.props import (BoolProperty,
                       PointerProperty,
                       EnumProperty)


from .data import data_closet_splitters


tagged_sss_list = []


def spread(arg):
    ret = []
    for i in arg:
        ret.extend(i) if isinstance(i, list) else ret.append(i)
    return ret

def to_inch(measure):
    return round(measure / sn_unit.inch(1), 2)

def get_dimension_props():
    """
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("bpy.context.scene.snap_closet_dimensions")
    return props


def get_object_dimension_props(obj):
    """ 
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("obj.snap_closet_dimensions")
    return props


def scene_assemblies(context):
    for obj in bpy.data.objects:
        if obj.get("IS_BP_ASSEMBLY"):
            assembly = sn_types.Assembly(obj)
            if props_closet.part_is_not_hidden(assembly):
                yield assembly


def scene_walls(context):
    ''' Generator that Returns a List of all of the wall base point objects
    '''
    for obj in context.scene.collection.objects:
        if obj.get('IS_BP_WALL'):
            yield obj


def scene_label_props(scenes, option):
    for scene in scenes:
        scene.snap_closet_dimensions.ceiling_height = option
        scene.snap_closet_dimensions.countertop = option
        scene.snap_closet_dimensions.ct_overhang = option
        scene.snap_closet_dimensions.filler = option
        scene.snap_closet_dimensions.framing_height = option
        scene.snap_closet_dimensions.fullback = option
        scene.snap_closet_dimensions.kds = option
        scene.snap_closet_dimensions.partition_depths = option
        scene.snap_closet_dimensions.partition_height = option
        scene.snap_closet_dimensions.corner_shelves_l_shelves = option
        scene.snap_closet_dimensions.section_depths = option
        scene.snap_closet_dimensions.section_widths = option
        scene.snap_closet_dimensions.toe_kicks = option
        scene.snap_closet_dimensions.toe_kick_height = option
        scene.snap_closet_dimensions.garage_legs = option
        scene.snap_closet_dimensions.toe_kick_skins = option
        scene.snap_closet_dimensions.top_shelf_depth = option
        scene.snap_closet_dimensions.variable = option
        scene.snap_closet_dimensions.capping_bottom = option
        scene.snap_closet_dimensions.flat_crown = option
        scene.snap_closet_dimensions.bc_panels = option
        scene.snap_closet_dimensions.light_rails = option
        scene.snap_closet_dimensions.valances = option
        scene.snap_closet_dimensions.door_face_height = option
        scene.snap_closet_dimensions.label_drawer_front_height = option
        scene.snap_closet_dimensions.file_drawers = option
        scene.snap_closet_dimensions.label_hamper_type = option
        scene.snap_closet_dimensions.glass_shelves = option
        scene.snap_closet_dimensions.shelf_setback = option
        scene.snap_closet_dimensions.slanted_shoe_shelves = option
        scene.snap_closet_dimensions.double_jewelry = option
        scene.snap_closet_dimensions.locks = option
        scene.snap_closet_dimensions.dog_ear = option
        scene.snap_closet_dimensions.walk_space = option
        scene.snap_closet_dimensions.third_line_holes = option
        scene.snap_closet_dimensions.wall_cleats = option

def clear_labels_lists():
    tagged_sss_list.clear()

class SNAP_OT_Select_All(Operator):
    bl_idname = "snap_closet_dimensions.select_all"
    bl_label = "Select All Dimension Options"
    bl_description = "This will select all existing labeling options"
    bl_options = {'UNDO'}

    def execute(self, context):
        scene_label_props(bpy.data.scenes, True)
        return {'FINISHED'}


class SNAP_OT_Deselect_All(Operator):
    bl_idname = "snap_closet_dimensions.deselect_all"
    bl_label = "Select All Dimension Options"
    bl_description = "This will select all existing labeling options"
    bl_options = {'UNDO'}

    def execute(self, context):
        scene_label_props(bpy.data.scenes, False)
        return {'FINISHED'}


class SNAP_OT_Cleanup(Operator):
    bl_idname = "snap_closet_dimensions.remove_labels"
    bl_label = "Remove Labels"
    bl_description = "This will remove any existing label"
    bl_options = {'UNDO'}

    def clean_up_scene(self, context):
        label_list = []
        for obj in context.scene.collection.objects:
            props = get_object_dimension_props(obj)
            if props.is_dim_obj:
                label_list.append(obj)
        scene_label_props(bpy.data.scenes, False)
        for item in bpy.data.objects:
            if item.type == 'FONT':
                text_measure = '\"' in item.data.body.lower()
                if text_measure:
                    label_list.append(item)
            if 'hashmark' in item.name.lower():
                label_list.append(item)
        sn_utils.delete_obj_list(label_list)
        for obj in bpy.data.objects:
            if obj.get('IS_VISDIM_A') or obj.get('IS_VISDIM_B'):
                bpy.data.objects.remove(obj, do_unlink=True)

    def execute(self, context):
        self.clean_up_scene(context)
        return {'FINISHED'}


class SNAP_MT_label_option(Menu):
    bl_label = "Label Options"

    def draw(self, context):
        layout = self.layout
        layout.operator("snap_closet_dimensions.select_all",
                        text="Select All", icon='CHECKBOX_HLT')
        layout.operator("snap_closet_dimensions.deselect_all",
                        text="Deselect All", icon='CHECKBOX_DEHLT')
        layout.separator()
        layout.operator("snap_closet_dimensions.remove_labels",
                        icon='X')


class SNAP_OT_Auto_Dimension(Operator):
    bl_idname = "snap_closet_dimensions.auto_dimension"
    bl_label = "Label Parts"
    bl_description = "This will assign names to all parts"
    bl_options = {'UNDO'}

    def add_dimension(self, parent):
        dim = sn_types.Dimension()
        anchor_props = get_object_dimension_props(dim.anchor)
        end_point_props = get_object_dimension_props(dim.end_point)
        anchor_props.is_dim_obj = True
        end_point_props.is_dim_obj = True
        dim.anchor.parent = parent
        return dim

    def add_tagged_dimension(self, parent):
        dim = self.add_dimension(parent)
        dim.anchor.snap.comment = "render"
        dim.end_point.snap.comment = "render"
        return dim

    def clean_up_scene(self, context):
        label_list = []

        for item in bpy.data.objects:
            if item.get('IS_VISDIM_A') or item.get('IS_VISDIM_B'):
                if sn_utils.get_obstacle_bp(item) or "IS_ANNOTATION" in item:
                    continue
                else:
                    bpy.data.objects.remove(item, do_unlink=True)

        for obj in context.scene.collection.objects:
            props = get_object_dimension_props(obj)
            if props.is_dim_obj:
                label_list.append(obj)

        sn_utils.delete_obj_list(label_list)

    def add_panel_height_annotation(self, assembly):
        dim_from_floor = assembly.obj_bp.matrix_world[2][3]

        dim = self.add_tagged_dimension(assembly.obj_bp)
        dim.start_x(value=- dim_from_floor - sn_unit.inch(8))
        dim.start_y(value=0)
        dim.start_z(value=assembly.obj_z.location.z / 2)
        dim.set_label(
            str(opengl_dim.format_distance(assembly.obj_x.location.x)))

    def set_section_number(self, assembly):
        """
            Set Section Number for Assembly
            This collects the products on a wall and loops through the
            products increasing the count of the number of openings found.
            Then assigns the number to comment 2 of the part
            This can only be set for parts that have a integer assigned for the snap.opening_name property
        """
        wall_bp = sn_utils.get_wall_bp(assembly.obj_bp)
        product_bp = sn_utils.get_bp(assembly.obj_bp, 'PRODUCT')
        if wall_bp:
            products = self.get_wall_products(wall_bp)
            adjusted_opening_number = 0
            for product in products:
                if product == product_bp:
                    assembly.obj_bp.snap.comment_2 = str(
                        int(assembly.obj_bp.snap.opening_name) + adjusted_opening_number)
                    break
                else:
                    adjusted_opening_number += int(product.snap.opening_name)

    def get_wall_products(self, wall_bp):
        """
            Get Sorted List of Products on a Wall
        """
        products = []
        for child in wall_bp.children:
            props = child.sn_closets
            if props.is_closet or props.is_fixed_shelf_and_rod_product_bp:
                child.snap.comment = wall_bp.snap.name_object
                products.append(child)
        products.sort(key=lambda obj: obj.location.x, reverse=False)
        return products

    def get_product_panels(self, product_bp, panel_list):
        """
            Get Sorted List of Panels in a product
        """
        for child in product_bp.children:
            props = child.sn_closets
            if props.is_panel_bp:
                assembly = sn_types.Assembly(child)
                if props_closet.part_is_not_hidden(assembly):
                    panel_list.append(child)
            self.get_product_panels(child, panel_list)
        panel_list.sort(key=lambda obj: obj.location.x, reverse=False)
        return panel_list

    def get_wall_panels(self, wall_bp):
        """
            Get Sorted List of Panels for a wall
            Returns List of Base Points
        """
        wall_panels = []
        products = self.get_wall_products(wall_bp)
        for product in products:
            product_panel_list = self.get_product_panels(product, [])
            for product_panel in product_panel_list:
                wall_panels.append(product_panel)
        return wall_panels

    def add_fixed_shelf_and_rod_annotations(self, product):
        scene_props = get_dimension_props()

        dim_from_floor = product.obj_bp.matrix_world[2][3]

        left_fin_end = product.get_prompt("Left Fin End")
        right_fin_end = product.get_prompt("Right Fin End")

        if left_fin_end.get_value():
            left_fe = self.add_dimension(product.obj_bp)
            left_fe.start_x(value=sn_unit.inch(-2))
            left_fe.set_label("Triangle")

        if right_fin_end.get_value():
            right_fe = self.add_dimension(product.obj_bp)
            right_fe.start_x(value=product.obj_x.location.x + sn_unit.inch(2))
            right_fe.set_label("Triangle")

        # CLOSET LEFT GAP DIM
        left_x = product.get_collision_location('LEFT')
        dist_l = math.fabs(product.obj_bp.location.x - left_x)
        if dist_l > 0:
            left_dim = self.add_dimension(product.obj_bp)
            left_dim.start_x(value=0)
            left_dim.end_x(value=-dist_l)
            left_dim.start_z(value=- dim_from_floor - sn_unit.inch(4))

        # CLOSET RIGHT GAP DIM
        right_x = product.get_collision_location('RIGHT')
        dist_r = math.fabs(product.obj_bp.location.x +
                           product.obj_x.location.x - right_x)
        if dist_r > 0:
            right_dim = self.add_dimension(product.obj_bp)
            right_dim.start_x(value=product.obj_x.location.x)
            right_dim.end_x(value=dist_r)
            right_dim.start_z(value=- dim_from_floor - sn_unit.inch(4))

        # WIDTH
        width = self.add_dimension(product.obj_bp)
        width.start_x(value=0)
        width.end_x(value=product.obj_x.location.x)
        width.start_z(value=- dim_from_floor - sn_unit.inch(4))

        if scene_props.framing_height:
            height = self.add_tagged_dimension(product.obj_bp)
            height.start_x(value=sn_unit.inch(-6))
            height.end_z(value=-product.obj_bp.location.z)

            height = self.add_tagged_dimension(product.obj_bp)
            height.start_x(value=sn_unit.inch(-6))
            height.end_z(value=-product.obj_bp.location.z)

    def add_closet_annotations(self, closets):
        scene_props = get_dimension_props()

        section_number_text = 1
        hanging_heights = []
        for closet_bp in closets:
            wall_bp = sn_utils.get_wall_bp(closet_bp)
            wall = sn_types.Assembly(wall_bp)
            closet = sn_types.Assembly(closet_bp)
            dim_from_floor = closet.obj_bp.matrix_world[2][3]

            # CLOSET LEFT GAP DIM
            left_x = closet.get_collision_location('LEFT')
            dist_l = math.fabs(closet.obj_bp.location.x - left_x)
            if dist_l > 0:
                left_dim = self.add_dimension(closet.obj_bp)
                left_dim.start_x(value=0)
                left_dim.end_x(value=-dist_l)
                left_dim.start_z(value=- dim_from_floor - sn_unit.inch(4))

            # CLOSET RIGHT GAP DIM
            right_x = closet.get_collision_location('RIGHT')
            dist_r = math.fabs(closet.obj_bp.location.x +
                              closet.obj_x.location.x - right_x)
            if dist_r > 0:
                dim_start_location = closet.obj_bp.location.x + closet.obj_x.location.x
                if dim_start_location < wall.obj_x.location.x:  # FIX FOR ADDING DIMS PAST WALLS
                    right_dim = self.add_dimension(closet.obj_bp)
                    right_dim.start_x(value=closet.obj_x.location.x)
                    right_dim.end_x(value=dist_r)
                    right_dim.start_z(value=- dim_from_floor - sn_unit.inch(4))

            # LEFT FILLER
            left_wall_filler = closet.get_prompt("Left Side Wall Filler")
            if left_wall_filler and left_wall_filler.get_value() > 0:
                left_f_dim = self.add_dimension(closet.obj_bp)
                left_f_dim.start_x(value=0)
                left_f_dim.end_x(value=left_wall_filler.get_value())
                left_f_dim.start_z(value=- sn_unit.inch(4))

            # RIGHT FILLER
            right_wall_filler = closet.get_prompt("Right Side Wall Filler")
            if right_wall_filler and right_wall_filler.get_value() > 0:
                right_f_dim = self.add_dimension(closet.obj_bp)
                right_f_dim.start_x(value=closet.obj_x.location.x)
                right_f_dim.end_x(value=-right_wall_filler.get_value())
                right_f_dim.start_z(value=- sn_unit.inch(4))

            left_side_thickness = closet.get_prompt("Left Side Thickness")
            cleat_thickness = closet.get_prompt("Cleat Thickness")
            if left_wall_filler and left_side_thickness:
                x_loc = left_side_thickness.get_value() + left_wall_filler.get_value()  # CLOSET OPENINGS
            elif cleat_thickness:
                x_loc = cleat_thickness.get_value()  # FIXED SHELF AND ROD
            else:
                x_loc = 0

            for i in range(1, 10):
                opening_height = closet.get_prompt(
                    "Opening " + str(i) + " Height")
                opening_width = closet.get_prompt(
                    "Opening " + str(i) + " Width")
                panel_thickness = closet.get_prompt("Panel Thickness")
                if opening_height and opening_width and panel_thickness:

                    if scene_props.framing_height:
                        if closet.obj_z.location.z not in hanging_heights:
                            hanging_height = self.add_dimension(
                               closet.obj_bp.parent)
                            hanging_height.start_x(
                               value=sn_unit.inch(-6) * (len(hanging_heights) + 1))
                            hanging_height.start_z(value=0)
                            hanging_height.end_z(value=closet.obj_z.location.z)
                            hanging_heights.append(closet.obj_z.location.z)

                    section_number_text += 1
                    x_loc += opening_width.get_value() + panel_thickness.get_value()

            props = closet.obj_bp.sn_closets
            if props.is_fixed_shelf_and_rod_product_bp:

                dim_from_floor = closet.obj_bp.matrix_world[2][3]

                left_fin_end = closet.get_prompt("Left Fin End")
                right_fin_end = closet.get_prompt("Right Fin End")
                panel_thickness = closet.get_prompt("Panel Thickness")

                if left_fin_end and left_fin_end.get_value():
                    left_fe = self.add_dimension(closet.obj_bp)
                    left_fe.start_x(value=sn_unit.inch(-2))
                    left_fe.set_label("Triangle")

                if right_fin_end and right_fin_end.get_value():
                    right_fe = self.add_dimension(closet.obj_bp)
                    right_fe.start_x(
                        value=closet.obj_x.location.x + sn_unit.inch(2))
                    right_fe.set_label("Triangle")

                if scene_props.framing_height:
                    height = self.add_tagged_dimension(closet.obj_bp)
                    height.start_x(value=sn_unit.inch(-6))
                    height.end_z(value=-closet.obj_bp.location.z)

                    height = self.add_tagged_dimension(closet.obj_bp)
                    height.start_x(value=sn_unit.inch(-6))
                    height.end_z(value=-closet.obj_bp.location.z)

                section_number_text += 1

    def get_object_global_location(self, obj):
        global_vertices = obj.matrix_world
        local_vertices = obj.data.vertices[0].co
        return global_vertices @ local_vertices

    def to_inch(self, measure):
        return round(measure / sn_unit.inch(1), 2)

    def to_inch_str(self, measure):
        return str(self.to_inch(measure))

    def to_inch_lbl(self, measure):
        return self.to_inch_str(measure) + "\""

    def arrayed_shelf_dimension(self, context, cutpart, shelf_bp):
        setback = 0.25
        shelves_qtt = cutpart.modifiers["ZQuantity"].count
        shelves_offset = cutpart.modifiers[
            "ZQuantity"].constant_offset_displace[2]
        section_depth = self.to_inch(
            shelf_bp.location[1])
        shelf_depth = self.to_inch(
            cutpart.dimensions[1])
        depth_part_diff = abs(
            section_depth - shelf_depth)
        label = self.to_inch_lbl(
            cutpart.dimensions[1])
        rotation = (0, math.radians(45), 0)
        width = cutpart.dimensions[0]
        if depth_part_diff != setback and depth_part_diff != 0.0:
            for i in range(shelves_qtt):
                z_offset = shelves_offset + (shelves_offset *
                                             (i - 1))
                location = (width / 2,
                            0,
                            sn_unit.inch(2.12) + z_offset)
                hashmark = self.draw_hashmark(context,
                                              cutpart,
                                              location=location,
                                              rotation=rotation,
                                              length=sn_unit.inch(6))
                dim = self.add_tagged_dimension(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=sn_unit.inch(5))
                dim.set_label(label)

    
    def arrayed_shelves_door_inserts(self, context, item):
        if 'INSERT' in item.name and 'doors' in item.name.lower():
            for k_item in item.children:
                if k_item.sn_closets.is_shelf_bp:
                    for x_item in k_item.children:
                        part_name = x_item.name.lower()
                        if 'cutpart' in part_name and not x_item.hide_viewport:
                            self.arrayed_shelf_dimension(
                                context, x_item, k_item)

    
    def arrayed_hangs_inserts(self, context, item):
        if 'INSERT' in item.name and 'hang' in item.name.lower():
            for k_item in item.children:
                if k_item.sn_closets.is_shelf_bp:
                    for x_item in k_item.children:
                        part_name = x_item.name.lower()
                        if 'cutpart' in part_name and not x_item.hide_viewport:
                            self.arrayed_shelf_dimension(
                                context, x_item, k_item)

    
    def arrayed_hamper_doors_inserts(self, context, item):
        if 'INSERT' in item.name and 'hamper' in item.name.lower():
            for k_item in item.children:
                if 'INSERT' in k_item.name and 'doors' in k_item.name.lower():
                    for x_item in k_item.children:
                        if x_item.sn_closets.is_shelf_bp:
                            for y_item in x_item.children:
                                part_name = y_item.name.lower()
                                if 'cutpart' in part_name and not y_item.hide_viewport:
                                    self.arrayed_shelf_dimension(
                                        context, y_item, x_item)

    
    def arrayed_shelves_section_depth_dimension(self, context, item):
        for n_item in item.children:
            self.arrayed_shelves_door_inserts(context, n_item)
            self.arrayed_hangs_inserts(context, n_item)
            self.arrayed_hamper_doors_inserts(context, n_item)

    
    def chk_shelf_cutpart(self, cutpart, shelf_bp):
        setback = 0.25
        shelf_depth = self.to_inch(shelf_bp.location.y)
        shelf_cutpart = self.to_inch(cutpart.dimensions.y)
        depth_part_diff = abs(shelf_depth - shelf_cutpart)
        if depth_part_diff != setback and depth_part_diff != 0.0:
            return True
        else:
            return False

    def setback_std_shelf_dim(self, cutpart, shelf_bp):
        setback = 0.25
        shelf_depth = self.to_inch(shelf_bp.location.y)
        shelf_cutpart = self.to_inch(cutpart.dimensions.y)
        width = cutpart.dimensions.x
        depth_part_diff = abs(shelf_depth - shelf_cutpart)
        rotation = (0, 45, 0)
        label = ""
        if depth_part_diff != setback and depth_part_diff != 0.0:
            label = self.to_inch_lbl(cutpart.dimensions.y)
        else:
            label = self.to_inch_lbl(shelf_bp.location.y)
        hashmark = sn_types.Line(sn_unit.inch(6), rotation)
        hashmark.parent(cutpart)
        hashmark.start_x(value=width / 2)
        dim = self.add_tagged_dimension(hashmark.end_point)
        dim.start_z(value=sn_unit.inch(2))
        dim.set_label(label)

    def stack_shelves_setback(self, item):
        stacks = [o for o in item.children if 'shelf stack' in o.name.lower()]

        for stack in stacks:
            assy = data_closet_splitters.Shelf_Stack(stack)
            default_depth = assy.obj_y.location.y
            assy_width = assy.obj_x.location.x
            indv_shelf_setbacks = assy.get_prompt("Individual Shelf Setbacks")
            adj_shelf_setback = assy.get_prompt("Adj Shelf Setback")

            for i, shelf in enumerate(assy.splitters):
                setback = assy.get_prompt(f'Shelf {i+1} Setback').get_value()
                is_locked_shelf = shelf.get_prompt("Is Locked Shelf").get_value()
                if indv_shelf_setbacks and adj_shelf_setback:
                    if not indv_shelf_setbacks.get_value():
                        setback = adj_shelf_setback.get_value()

                # Only add set back label if shelf is not locked and setback is greater then 0.25"
                if not is_locked_shelf and sn_unit.meter_to_inch(setback) > 0.25:
                    pos_z = shelf.obj_bp.location.z
                    setback_lbl = self.to_inch_lbl(default_depth - setback)
                    hashmark = sn_types.Line(sn_unit.inch(6), (-45, 0, 90))
                    hashmark.parent(stack)
                    hashmark.anchor.location = (
                        assy_width / 2,
                        default_depth,
                        pos_z)
                    hashmark.anchor.rotation_euler = (
                        math.radians(-45),
                        0,
                        math.radians(-90))
                    setback_dim = sn_types.Dimension()
                    setback_dim.parent(hashmark.end_point)
                    setback_dim.start_z(value=sn_unit.inch(2))
                    setback_dim.set_label(setback_lbl)

    def place_setbacks(self, hang_data):
        related_shelf = hang_data['related_shelf']
        offset = hang_data['offset']
        quantity = hang_data['quantity']
        assy_width = hang_data['assy_width']
        default_depth = hang_data['default_depth']
        setback = hang_data['setback']
        thickness = sn_unit.inch(0.75)
        if setback > 0:
            for i in range(quantity):
                pos_y = (default_depth - setback) * -1
                pos_z = 0
                if quantity > 1:
                    pos_z = (i * offset) + thickness
                setback_in = self.to_inch(default_depth - setback)
                default_depth_in = self.to_inch(default_depth)
                if setback_in != default_depth_in:
                    setback_lbl = self.to_inch_lbl(default_depth - setback)
                    hashmark = sn_types.Line(sn_unit.inch(6), (-45, 0, 90))
                    hashmark.parent(related_shelf)
                    hashmark.anchor.location = (assy_width / 2, 
                                                pos_y, 
                                                pos_z)
                    hashmark.anchor.rotation_euler = (math.radians(-45),
                                                    0,
                                                    math.radians(-90))
                    setback_dim = sn_types.Dimension()
                    setback_dim.parent(hashmark.end_point)
                    setback_dim.start_z(value=sn_unit.inch(2))
                    setback_dim.set_label(setback_lbl)
    
    def hangers_setback(self, item):
        for obj in item.children:
            # Hang Short and Hang Short Tall
            hang_short = 'Short Hang' in obj.name
            hang_short_tall = 'Short Tall Hang' in obj.name
            # Hang Long and Hang Medium
            hang_long = 'Long Hang' in obj.name
            hang_medium = 'Medium Hang' in obj.name
            # Hang Double and Hang Double Tall
            hang_double = 'Double Hang' in obj.name
            hang_double_tall = 'Double Tall Hang' in obj.name
            if hang_short or hang_short_tall:
                self.fetch_all_shelves_setbacks(obj)
            if hang_long or hang_medium:
                self.fetch_all_shelves_setbacks(obj)
            if hang_double or hang_double_tall:
                self.fetch_all_shelves_setbacks(obj)

    def fetch_all_shelves_setbacks(self, hang):
        hang_assy = sn_types.Assembly(hang)
        default_depth = hang_assy.obj_y.location.y
        assy_width = hang_assy.obj_x.location.x
        for shelf in hang.children:
            is_shelf = 'shelf' in shelf.name.lower()
            not_empty = 'empty' not in shelf.name.lower()
            if is_shelf and not_empty:
                sh_assy = sn_types.Assembly(shelf)
                hidden = sh_assy.get_prompt("Hide").get_value()
                adj_setback_pmpt = sh_assy.get_prompt("Adj Shelf Setback")
                sh_qty = sh_assy.get_prompt("Z Quantity").get_value()
                sh_offset = sh_assy.get_prompt("Z Offset").get_value()
                if not hidden:
                    std_shelf_setback = adj_setback_pmpt.get_value()
                    mesh_depth = abs(sh_assy.obj_y.location.y)
                    setback_sum = mesh_depth + std_shelf_setback
                    setback = default_depth - setback_sum
                    if setback > 0:
                        result = {}
                        result['related_shelf'] = shelf
                        result['offset'] = sh_offset
                        result['quantity'] = sh_qty
                        result['assy_width']  = assy_width 
                        result['default_depth'] = default_depth
                        result['setback'] = setback
                        self.place_setbacks(result)

    
    def setback_standard_shelf(self, item):
        # We add dimensions for shelves that differs
        # from the section depth + default cutpart (1/4")
        for n_item in item.children:
            item_is_top_bp = n_item.sn_closets.is_closet_top_bp
            item_is_shelf = 'shelf' in n_item.name.lower()

            if item_is_shelf and not item_is_top_bp:
                shelves = []
                for k_item in n_item.children:
                    if k_item.sn_closets.is_shelf_bp:
                        for x_item in k_item.children:
                            if 'part' in x_item.name.lower():
                                shelves.append(self.chk_shelf_cutpart(x_item,
                                                                      k_item))
                if any(shelves):
                    for k_item in n_item.children:
                        if k_item.sn_closets.is_shelf_bp:
                            for x_item in k_item.children:
                                if 'part' in x_item.name.lower():
                                    self.setback_std_shelf_dim(x_item, k_item)

    def find_partition_order(self, partition):
        partitions = []
        section = partition.parent
        is_hanging = 'section' in section.name.lower()
        if is_hanging:
            for item in section.children:
                if item.sn_closets.is_panel_bp:
                    item_pos = item.location.x
                    partitions.append((item_pos, item))
        partitions = sorted(partitions, key=lambda tup: tup[0])
        for i, (pos, item) in enumerate(partitions):
            if item == partition:
                return i

    def get_partition_list(self, product):
        partition_list = []
        for item in product.children:
            panel = item.sn_closets.is_panel_bp
            if panel:
                for cutpart in item.children:
                    has_cutpart = cutpart.type == "MESH"
                    if has_cutpart and not cutpart.hide_viewport:
                        part_assy = sn_types.Assembly(item)
                        hang_opng_x_pos = item.location.x
                        x_pos = hang_opng_x_pos + item.location.x
                        x_pos_inch = self.to_inch(x_pos)
                        z_pos_inch = self.to_inch(item.location.z)
                        partition_list.append((x_pos_inch,
                                               z_pos_inch,
                                               cutpart,
                                               part_assy))
        return partition_list

    def get_partition_height_list(self, wall_bp):
        partition_list = []
        for product in wall_bp.children:
            is_lsh = 'l shelves' in product.name.lower()
            is_csh = 'corner shelves' in product.name.lower()
            if is_lsh or is_csh:
                continue
            elif not is_lsh and not is_csh:
                for item in product.children:
                    if item.sn_closets.is_panel_bp:
                        for cutpart in item.children:
                            has_cutpart = cutpart.type == "MESH"
                            if has_cutpart and not cutpart.hide_viewport:
                                part_assy = sn_types.Assembly(item)
                                hang_opng_x_pos = product.location.x
                                x_pos = hang_opng_x_pos + item.location.x
                                x_pos_inch = self.to_inch(x_pos)
                                z_pos_inch = self.to_inch(item.location.z)
                                partition_list.append((x_pos_inch,
                                                       z_pos_inch,
                                                       cutpart,
                                                       part_assy))
        return partition_list

    def partition_height(self, wall_bp):
        partition_list = self.get_partition_height_list(wall_bp)
        overlaps = self.find_partitions_overlapping(partition_list)
        if overlaps is None: 
            for _, _, mesh, _ in partition_list:
                self.apply_partition_height_label(mesh)
        elif overlaps is not None:
            for _, _, mesh, _ in partition_list:
                skip = []
                for overlap in overlaps:
                    partition = mesh.parent
                    order = self.find_partition_order(partition)
                    if mesh.name == overlap.name:
                        skip.append(mesh)
                        if order == 0:
                            self.apply_partition_height_label(mesh, "right")
                        if order != 0:
                            self.apply_partition_height_label(mesh, "left")
                if mesh not in skip:
                    self.apply_partition_height_label(mesh)
    
    def corner_shelves_l_shelves(self, item):
        assy = sn_types.Assembly(item)
        has_top_kd = assy.get_prompt("Add Top KD").get_value()
        if has_top_kd:
            self.csh_lsh_top_kd_lbl(item, assy)
        self.csh_lsh_botom_kd_lbl(item, assy)
        right_depth_pmpt = assy.get_prompt("Right Depth")
        right_depth = right_depth_pmpt.distance_value
        self.csh_lsh_width(item, assy)
        self.csh_lsh_depth(item, right_depth)
        self.csh_lsh_right_partition(item, assy)

    def csh_lsh_right_partition(self, item, assy):
        for partition in item.children:
            props = partition.sn_closets
            mitered = 'mitered' in partition.name.lower()
            if props.is_panel_bp and not mitered:
                if abs(partition.location[0]) > 0:
                    height = assy.obj_z.location.z
                    label = self.to_inch_str(height)
                    dim = self.add_tagged_dimension(partition)
                    dim.anchor.rotation_euler.y = math.radians(-90)
                    dim.anchor.name = 'CSHLSH'
                    dim.end_point.name = 'CSHLSH'
                    dim.start_x(value=height/2)
                    dim.start_y(value=sn_unit.inch(-2))
                    dim.start_z(value=sn_unit.inch(-2))
                    dim.set_label(label)

    def csh_lsh_top_kd_lbl(self, item, assy):
        tks = [tk for tk in item.children if 'toe kick' in tk.name.lower()]
        if len(tks) == 0:
            return
        the_tk = tks[0]
        tk_height = 0
        tk_assy = sn_types.Assembly(the_tk)
        tk_height = tk_assy.obj_z.location.z
        width = assy.obj_x.location.x
        height = (assy.obj_z.location.z + tk_height) - sn_unit.inch(0.5)
        dim = self.add_tagged_dimension(item)
        dim.start_x(value=width/2)
        dim.start_y(value=0)
        dim.start_z(value=height)
        dim.set_label("KD")


    def csh_lsh_botom_kd_lbl(self, item, assy):
        tks = [tk for tk in item.children if 'toe kick' in tk.name.lower()]
        if len(tks) == 0:
            return
        the_tk = tks[0]
        tk_height = 0
        tk_assy = sn_types.Assembly(the_tk)
        tk_height = tk_assy.obj_z.location.z
        width = assy.obj_x.location.x
        height = tk_height
        dim = self.add_tagged_dimension(item)
        dim.start_x(value=width/2)
        dim.start_y(value=0)
        dim.start_z(value=height)
        dim.set_label("KD")


    def csh_lsh_width(self, item, assy):
        width = assy.obj_x.location.x
        discount = sn_unit.inch(0.75)
        label = self.to_inch_lbl(width - discount)
        dim = self.add_tagged_dimension(item)
        dim.start_x(value=width/2)
        dim.start_y(value=0)
        dim.start_z(value=sn_unit.inch(-3))
        dim.set_label(label)

    def csh_lsh_depth(self, item, right_depth):
        correct_ptt = []
        for partition in item.children:
            is_partition = 'partition' in partition.name.lower()
            is_right_ptt = partition.location[0] != 0
            if is_partition and is_right_ptt:
                for mesh in partition.children:
                    if mesh.type == 'MESH':
                        correct_ptt.append(partition)
        for part in correct_ptt:
            st_assy = sn_types.Assembly(part)
            depth = st_assy.obj_y.location.y 
            label = self.to_inch_lbl(right_depth)
            rotation = (0, 135, 0)
            hashmark = sn_types.Line(sn_unit.inch(6), rotation)
            hashmark.parent(part)
            hashmark.start_x(value=sn_unit.inch(0.75))
            hashmark.start_y(value=depth)
            hashmark.start_z(value=0)
            dim = self.add_tagged_dimension(hashmark.end_point)
            dim.start_z(value=sn_unit.inch(2))
            dim.set_label(label)

    def find_partitions_overlapping(self, partition_list):
        partition_list = sorted(partition_list, key=lambda tup: tup[0])
        overlaps = []
        partition_overlaps = []
        tolerance = sn_unit.inch(1)
        for partition in partition_list:
            for other_partition in partition_list:
                x_a_pos_offset = other_partition[0] + tolerance
                x_a_neg_offset = other_partition[0] - tolerance
                near_same_x = x_a_neg_offset <= partition[0] <= x_a_pos_offset
                same_cpart = partition[2] == other_partition[2]
                cpart_a_length = partition[3].obj_x.location.x
                cpart_b_length = other_partition[3].obj_x.location.x
                existing = [True for a, b in overlaps if a ==
                            other_partition[2] and b == partition[2]]
                if any(existing):
                    continue
                if near_same_x and not same_cpart:
                    if cpart_a_length > cpart_b_length:
                        overlaps.append((partition[2], other_partition[2]))
                    elif cpart_a_length < cpart_b_length:
                        overlaps.append((other_partition[2], partition[2]))
                    partition_overlaps.append(other_partition[2])
                    partition_overlaps.append(partition[2])
        if len(partition_overlaps) > 0:
            return list(set(partition_overlaps))
        return None
    
    def apply_partition_height_label(self, partition, displacement=None):
        label = self.to_inch_str(partition.dimensions[0])
        dim = self.add_tagged_dimension(partition)
        dim.anchor.rotation_euler.y = math.radians(-90)
        dim.start_z(value=sn_unit.inch(-1))
        dim.start_x(value=(partition.dimensions[0] / 2) - sn_unit.inch(2))
        if displacement == "left":
            dim.start_z(value=sn_unit.inch(3))
        if displacement == "right":
            dim.start_z(value=sn_unit.inch(-2.25))
        dim.start_y(value=0)
        dim.anchor.name = 'PARTHGT'
        dim.end_point.name = 'PARTHGT'
        dim.set_label(label)

    def ceiling_height_dimension(self, item, bheight_offset):
        wall_height = item.dimensions.z
        dim = self.add_tagged_dimension(item.parent)
        dim.start_x(value=sn_unit.inch(-1) + bheight_offset)
        dim.start_y(value=sn_unit.inch(-1) + bheight_offset)
        dim.start_z(value=0)
        dim.end_z(value=wall_height)
        dim.set_label(self.to_inch_lbl(wall_height))

    def wall_width_dimension(self, wall_bp):
        assembly = sn_types.Assembly(wall_bp)
        has_entry = any('Door Frame' in e.name for c in wall_bp.children
                        for e in c.children)
        if not has_entry:
            dim = self.add_tagged_dimension(wall_bp)
            label = self.to_inch_lbl(assembly.obj_x.location.x)
            dim.parent(wall_bp)
            dim.start_y(value=assembly.obj_y.location.y)
            dim.start_z(value=assembly.obj_z.location.z + sn_unit.inch(4))
            dim.end_x(value=assembly.obj_x.location.x)
            dim.set_label(label)

    def section_width_apply_lbl(self, opening, position):
        if position != "up" and position != "down":
            return
        label_height = 0
        lower_offset = sn_unit.inch(-3)
        upper_offset = sn_unit.inch(15)
        opening_assembly = sn_types.Assembly(opening)
        product_assembly = sn_types.Assembly(sn_utils.get_closet_bp(opening))
        opening_width = product_assembly.get_prompt("Opening " + opening.sn_closets.opening_name + " Width")
        width = opening_width.get_value()
        if width == 0:
            cage = opening_assembly.get_cage()
            if cage:
                width = cage.dimensions.x
                cage.hide_viewport = True
            else:
                return
        depth = abs(opening_assembly.obj_y.location.y)
        width_str = self.to_inch_lbl(width)
        parent_assembly = sn_types.Assembly(opening.parent)
        parent_height = parent_assembly.obj_z.location.z
        label_height = (opening.location[2] / -1) + lower_offset
        if position == "up":
            label_height += (parent_height + upper_offset)
        dim = self.add_tagged_dimension(opening)
        dim.start_x(value=width/2)
        dim.start_y(value=depth)
        dim.start_z(value=label_height)
        dim.set_label(width_str)

    def get_partition_props(self, wall, partition, opening):
        if wall:
            opng_bp_height = opening.location[2]
            wall_height = sn_types.Assembly(wall).obj_z.location.z
            part_height = partition.dimensions[0]
            part_height_midpoint = part_height / 2
            wall_half = wall_height / 2
            part_midpoint_height = part_height_midpoint + opng_bp_height
            is_upper = part_midpoint_height >= wall_half
            is_lower = part_midpoint_height < wall_half
            is_full_upper = opening.location[2] > wall_half
            return ((is_upper, is_full_upper, is_lower))
        return None

    def find_matching_partition_cutpart(self, opening):
        tolerance = sn_unit.inch(6)
        hanging_opening = opening.parent
        for item in hanging_opening.children:
            if 'partition' in item.name.lower():
                opng_pos = opening.location[0]
                item_pos = item.location[0]
                lower_end = round((opng_pos - tolerance), 2)
                upper_end = round((opng_pos + tolerance), 2)
                if lower_end <= item_pos <= upper_end:
                    for cutpart in item.children:
                        is_cutpart = cutpart.type == 'MESH'
                        hidden = cutpart.hide_viewport
                        if is_cutpart and not hidden:
                            return cutpart

    def query_openings_data(self, context, wall_bp):
        wall_dict = {}
        for obj in wall_bp.children:
            section = 'section' in obj.name.lower()
            opng_dict = {}
            if section:
                openings = []
                sorted_openings = []
                for op in obj.children:
                    inner_opng = 'opening' in op.name.lower()
                    if inner_opng:
                        x_loc = self.to_inch(op.location[0])
                        openings.append((x_loc, op))
                sorted_openings = sorted(openings, key=lambda tup: tup[0])
                filtered_openings = []
                for sorted_opng in sorted_openings:
                    if sn_types.Assembly(sorted_opng[1]).obj_x is not None:
                        filtered_openings.append(sorted_opng)
                obj_assy = sn_types.Assembly(obj)
                hang_opng_width = obj_assy.obj_x.location.x
                start_point = obj.location[0]
                end_point = start_point + hang_opng_width
                for i in range(1, 10):
                    floor_pmpt_query = "Opening " + str(i) + " Floor Mounted"
                    height_pmpt_query = "Opening " + str(i) + " Height"
                    floor_mounted = obj_assy.get_prompt(floor_pmpt_query)
                    opng_height_pmpt = obj_assy.get_prompt(height_pmpt_query)
                    has_floor_value = floor_mounted is not None
                    if has_floor_value:
                        opng_props = None
                        is_floor = floor_mounted.get_value()
                        opng_height = opng_height_pmpt.get_value()
                        matching_opng = filtered_openings[i-1]
                        opng = matching_opng[1]
                        matching = self.find_matching_partition_cutpart(opng)
                        if matching is not None:
                            opng_props = self.get_partition_props(wall_bp,
                                                                  matching,
                                                                  opng)
                        elif matching is None:
                            opng_props = (False, False, True)

                        opening_width = obj_assy.get_prompt("Opening " + str(i) + " Width")
                        opng_width = self.to_inch(opening_width.get_value())
                        opng_height_meas = self.to_inch(opng_height)
                        opng_x_loc = matching_opng[0]
                        opng_dict[opng] = {
                            "width": opng_width,
                            "height": opng_height_meas,
                            "x_loc": opng_x_loc,
                            "is_floor": is_floor,
                            "is_upper": opng_props[0],
                            "is_full_upper": opng_props[1],
                            "is_lower": opng_props[2]
                        }
                result = sorted(opng_dict.items(), key=lambda x: x[1]["x_loc"])
                wall_dict[obj] = {"start": round(start_point, 4),
                                  "end": round(end_point, 4),
                                  "openings": result}
        return wall_dict

    def one_hanging_opening(self, opng_data):
        openings = []
        for key, value in opng_data.items():
            for opening in value["openings"]:
                opng_object = opening[0]
                openings.append(opng_object)
        for each in openings:
            self.section_width_apply_lbl(each, "down")

    def get_lower_openings_for_matching(self, opng_data):
        hang_opngs_dict = {}
        hang_opngs_list = [op for op in opng_data.keys()]
        for hang_opng in hang_opngs_list:
            height_metric = sn_types.Assembly(hang_opng).obj_z.location.z
            height = self.to_inch(height_metric)
            hang_opngs_dict[height] = hang_opng
        lowest = min(hang_opngs_dict.keys())
        result = hang_opngs_dict[lowest]
        return result

    def get_upper_openings_for_matching(self, opng_data):
        hang_opngs_dict = {}
        hang_opngs_list = [op for op in opng_data.keys()]
        for hang_opng in hang_opngs_list:
            height_metric = sn_types.Assembly(hang_opng).obj_z.location.z
            height = self.to_inch(height_metric)
            hang_opngs_dict[height] = hang_opng
        highest = max(hang_opngs_dict.keys())
        result = hang_opngs_dict[highest]
        return result

    def overlapping_different_hang_opng_count(self, opng_data):
        hang_opng_count = []
        hang_opngs = [obj for obj in opng_data.keys()]
        hang_opngs_starts = [obj["start"] for obj in opng_data.values()]
        hang_opngs_ends = [obj["end"] for obj in opng_data.values()]
        for hang in hang_opngs:
            op_count = 0
            for op in hang.children:
                if 'opening' in op.name.lower():
                    op_count += 1
            hang_opng_count.append(op_count)
        # Rules to deal with most cases, where the openings overlaps each other
        # but have different quantities
        openings_count = len(list(set(hang_opng_count)))
        hang_opng_count_check = openings_count > 1
        starts_check = len(list(set(hang_opngs_starts))) == 1
        end_check = len(list(set(hang_opngs_ends))) == 1
        if hang_opng_count_check and starts_check and end_check:
            return True
        return False

    def overlapping_hang_opng_count(self, opng_data):
        hang_opng_count = []
        hang_opngs = [obj for obj in opng_data.keys()]
        for hang in hang_opngs:
            op_count = 0
            for op in hang.children:
                if 'opening' in op.name.lower():
                    op_count += 1
            hang_opng_count.append(op_count)
        openings_count = len(list(set(hang_opng_count)))
        hang_opng_count_check = openings_count > 1
        if hang_opng_count_check:
            return True
        return False
    
    def overlapping_diff_hang_opng_only_one(self, opng_data):
        hang_opng_count = []
        hang_opngs = [obj for obj in opng_data.keys()]
        hang_opngs_starts = [obj["start"] for obj in opng_data.values()]
        hang_opngs_ends = [obj["end"] for obj in opng_data.values()]
        starts_qty = len(list(set(hang_opngs_starts)))
        ends_qty = len(list(set(hang_opngs_ends)))
        for hang in hang_opngs:
            op_count = 0
            for op in hang.children:
                if 'opening' in op.name.lower():
                    op_count += 1
            hang_opng_count.append(op_count)
        openings_count = len(list(set(hang_opng_count)))
        really_one = list(set(hang_opng_count))[0] == 1
        if openings_count == 1 and starts_qty >= 1 and ends_qty >= 1 and really_one:
            return True
        return False

    def overlapping_near_match_hang_opng_count(self, opng_data):
        hang_opng_count = []
        hang_opngs = [obj for obj in opng_data.keys()]
        hang_opngs_starts = [obj["start"] for obj in opng_data.values()]
        hang_opngs_ends = [obj["end"] for obj in opng_data.values()]
        for hang in hang_opngs:
            op_count = 0
            for op in hang.children:
                if 'opening' in op.name.lower():
                    op_count += 1
            hang_opng_count.append(op_count)
        # Rules to deal with most cases, where the openings overlaps each other
        # but have different quantities
        openings_count = len(list(set(hang_opng_count)))
        hang_opng_count_check = openings_count == 1
        starts_check = len(list(set(hang_opngs_starts))) == 1
        end_check = len(list(set(hang_opngs_ends))) == 1
        if hang_opng_count_check and starts_check and end_check:
            return True
        return False

    def has_matching_opngs_while_overlapping(self, opng_data):
        opng_qty_list = []
        openings_count = 0
        for hang_opng in opng_data.values():
            opng_qty = len(hang_opng['openings'])
            opng_qty_list.append(opng_qty)
        openings_count = len(list(set(opng_qty_list)))
        if openings_count > 1:
            return False
        elif openings_count == 1:
            measures = []
            start_list = []
            for openings in opng_data.values():
                opengs_list = openings["openings"]
                positions = []
                for opng in opengs_list:
                    x_loc = opng[1]["x_loc"]
                    positions.append(x_loc)
                measures.append(positions)
                start_list.append(openings["start"])
            number_diff_measures = len(list(set(spread(measures))))
            number_diff_startings = len(list(set(start_list)))
            opening_count_set = list(set(opng_qty_list))[0]
            opng_meas_rule = opening_count_set == number_diff_measures
            start_loc_rule = number_diff_startings > 1
            if opng_meas_rule and not start_loc_rule:
                return True
            elif not opng_meas_rule or start_loc_rule:
                return False

    def has_overlapping_hanging_opening(self, opng_data):
        intervals = []
        overlapping = False
        for key, value in opng_data.items():
            intervals.append((value["start"], value["end"]))
        intervals = sorted(intervals, key=lambda tup: tup[0])
        for each in range(1, len(intervals)):
            start = intervals[each - 1][1]
            end = intervals[each][0]
            if start > end:
                overlapping = True
        return overlapping

    def has_overlapping_lower(self, upper_opening, lower_list):
        overlaps = []
        upper_hang_opng_start = upper_opening[0].parent.location[0]
        upper_start = (upper_opening[2] * sn_unit.inch(1))
        upper_width = (upper_opening[1] * sn_unit.inch(1))
        upper_end = upper_hang_opng_start + upper_start + upper_width
        for lower in lower_list:
            lower_hang_opng_start = lower[0].parent.location[0]
            lower_start = lower_hang_opng_start + (lower[2] * sn_unit.inch(1))
            lower_width = (lower[1] * sn_unit.inch(1))
            lower_end = lower_start + lower_width
            if lower_end < upper_start and lower_end < upper_end:
                continue
            if lower_start > upper_start and lower_start > upper_end:
                continue
            if lower_start > upper_start and lower_start < upper_end:
                overlaps.append(True)
                continue
            if lower_end > upper_start and lower_end < upper_end:
                overlaps.append(True)
                continue
        if any(overlaps):
            return True
        elif not any(overlaps):
            return False
    
    def opening_absolute_start_end(self, opening):
        opng_width = to_inch(sn_types.Assembly(opening).obj_x.location.x)
        opng_start = to_inch(opening.location[0])
        section_start = to_inch(opening.parent.location[0])
        actual_start = opng_start + section_start
        opng_end = actual_start + opng_width
        return (actual_start, opng_end)

    def has_occluding_opening(self, opening, opng_data):
        opngs_at_wall = []
        querying_opng = opening[0]
        op_start, op_end = self.opening_absolute_start_end(querying_opng)
        tolrnc = 2 # 2 inches
        for value in opng_data.values():
            openings = value["openings"]
            for item in openings:
                curr_opng = item[0]
                already_in = curr_opng not in opngs_at_wall
                not_same = curr_opng != querying_opng
                not_same_parent = curr_opng.parent != querying_opng.parent
                if already_in and not_same and not_same_parent:
                    opngs_at_wall.append(curr_opng)
        for item in opngs_at_wall:
            oth_start, oth_end = self.opening_absolute_start_end(item)
            match_end = oth_end - tolrnc <= op_end <= oth_end + tolrnc
            match_start = oth_start - tolrnc <= op_start <= oth_start + tolrnc
            if match_start and match_end:
                return True
        return False

    def many_hanging_openings(self, opng_data):
        overlapping = self.has_overlapping_hanging_opening(opng_data)
        if not overlapping:
            for key, value in opng_data.items():
                for opening in value["openings"]:
                    self.section_width_apply_lbl(opening[0], "down")
        elif overlapping:
            matching = self.has_matching_opngs_while_overlapping(opng_data)
            different = self.overlapping_different_hang_opng_count(opng_data)
            only_one = self.overlapping_diff_hang_opng_only_one(opng_data)
            near_match = self.overlapping_near_match_hang_opng_count(opng_data)
            if matching or different:
                self.apply_labels_grouped_up_down(opng_data)
            elif only_one and not matching and not different:
                for key, value in opng_data.items():
                    for opening in value["openings"]:
                        if opening[1]["is_upper"]:
                            self.section_width_apply_lbl(opening[0], "up")
                        if opening[1]["is_lower"]:
                            self.section_width_apply_lbl(opening[0], "down")
            elif near_match and not only_one and not matching and not different:
                self.apply_labels_grouped_up_down(opng_data)
            else:
                for key, value in opng_data.items():
                    for opening in value["openings"]:
                        if opening[1]["is_upper"]:
                            occlusion = self.has_occluding_opening(
                                opening, opng_data)
                            if occlusion:
                                self.section_width_apply_lbl(
                                    opening[0], "up")
                            elif not occlusion:
                                self.section_width_apply_lbl(
                                    opening[0], "down")
                        if opening[1]["is_lower"]:
                            self.section_width_apply_lbl(
                                opening[0], "down")

    def apply_labels_grouped_up_down(self, opng_data):
        lowest = self.get_lower_openings_for_matching(opng_data)
        desired_lowers = opng_data[lowest]['openings']
        for desired_low in desired_lowers:
            self.section_width_apply_lbl(desired_low[0], "down")
        highest = self.get_upper_openings_for_matching(opng_data)
        desired_uppers = opng_data[highest]['openings']
        for desired_high in desired_uppers:
            self.section_width_apply_lbl(desired_high[0], "up")


    def section_widths(self, context, wall_bp):
        opng_data = self.query_openings_data(context, wall_bp)
        if len(opng_data) == 1:
            self.one_hanging_opening(opng_data)
        elif len(opng_data) > 1:
            self.many_hanging_openings(opng_data)

    def draw_hashmark(self, context, parent,
                      location=(sn_unit.inch(1.06), 0, sn_unit.inch(1.06)),
                      rotation=(0, math.radians(45), 0),
                      length=sn_unit.inch(3)):
        # The following creates a Poly NURBS curve that looks like a dash/line
        # Create a curve and define its rendering settings
        hashmark_n = 'Hashmark'
        line = bpy.data.curves.new(hashmark_n, 'CURVE')
        line.dimensions = '3D'
        line.fill_mode = 'HALF'
        line.bevel_resolution = 0
        line.bevel_depth = sn_unit.inch(0.1)

        # Create a straight line spline for the curve and adjust its points' properties
        spline = line.splines.new(type='POLY')
        spline.points.add(1)
        spline.points[0].co = (0, 0, -0.5 * length, 1)
        spline.points[1].co = (0, 0, 0.5 * length, 1)
        spline.points[0].tilt = math.radians(90)
        spline.points[1].tilt = math.radians(90)

        # Create the hashmark object that contains the curve and spline data
        hashmark_obj = bpy.data.objects.new(hashmark_n, line)
        hashmark_obj.parent = parent
        hashmark_obj.location = location
        hashmark_obj.rotation_euler = rotation
        hashmark_obj.snap.comment = "render"
        context.scene.collection.objects.link(hashmark_obj)
        return hashmark_obj

    def apply_file_drawer_labels(self, label_dict):
        for part, info in label_dict.items():
            label, part_dims = info
            # 2nd line -> Type: F2B or LAT
            dim_label = ''
            box_label = ' '
            f2b_file_drawer = label[0] == 0
            lat_file_drawer = label[0] == 1
            letter = label[1] == 0
            legal = label[1] == 1
            if f2b_file_drawer:
                dim_label = 'F2B '
            elif lat_file_drawer:
                dim_label = 'Lat. '
            if letter:
                dim_label += 'Letter'
            elif legal:
                dim_label += 'Legal'

            # 3rd line -> Drawer box size
            if lat_file_drawer and letter:
                box_label = '14" D box'
            elif lat_file_drawer and legal:
                box_label = '17" D box'

            dim = self.add_tagged_dimension(part)
            dim.start_x(value=(part_dims[0] / 2) - sn_unit.inch(2.25))
            dim.start_y(value=(part_dims[1] / 2) + sn_unit.inch(0.75))
            dim.set_label(f'FILE|{dim_label}|{box_label}')

    def file_drawer_labeling(self, drw_stck_assy):
        file_drawer_info = {}

        drw_faces = [obj for obj in drw_stck_assy.obj_bp.children
                     if obj.sn_closets.is_drawer_front_bp]
        drw_faces.sort(key=lambda x: x.location.z)

        drw_boxes = [obj for obj in drw_stck_assy.obj_bp.children
                     if obj.sn_closets.is_drawer_box_bp]

        for face in drw_faces:
            boxes = []
            face_assy = sn_types.Assembly(face)
            face_x = face_assy.obj_x.location.x
            face_y = face_assy.obj_y.location.y
            face_z = face_assy.obj_z.location.z
            face_dims = (face_x, face_y, face_z)

            face_loc_z = face.location.z
            face_top = face_loc_z + face_x

            for box in drw_boxes:
                if face_loc_z <= box.location.z <= face_top:
                    boxes.append(box)

            if len(boxes) == 1:
                [sgl_box] = boxes
                box_assy = sn_types.Assembly(sgl_box)
                file_rail = box_assy.get_prompt('Use File Rail').get_value()

                if file_rail:
                    type_pmt = box_assy.get_prompt('File Rail Type')
                    dir_pmt = box_assy.get_prompt('File Rail Direction')
                    rail_type = type_pmt.get_value()
                    rail_direction = dir_pmt.get_value()
                    rail_info = (rail_direction, rail_type)
                    file_drawer_info[face] = (rail_info, face_dims)

        self.apply_file_drawer_labels(file_drawer_info)

    def apply_topshelf_exposed_lbl(self, topshelf_obj, location):
        topshelf_assy = sn_types.Assembly(topshelf_obj)
        width = topshelf_assy.obj_x.location.x
        depth = topshelf_assy.obj_y.location.y
        height = abs(topshelf_assy.obj_z.location.z)
        loc_x, loc_z = 0, 0
        rotation = (0, 0, 0)

        if topshelf_obj.parent.sn_closets.is_closet_top_bp:
            if location == 'LEFT':
                loc_x, loc_z = 0, -height
                rotation = (0, 225, 0)
            elif location == 'RIGHT':
                loc_x, loc_z = width, -height
                rotation = (0, 135, 0)
            elif location == 'BACK':
                loc_x, loc_z = width / 2, -height
                rotation = (0, 225, 0)
        else:
            if location == 'LEFT':
                loc_x, loc_z = 0, -height
                rotation = (0, -45, 0)
            elif location == 'RIGHT':
                loc_x, loc_z = width, -height
                rotation = (0, 45, 0)

        hashmark = sn_types.Line(sn_unit.inch(6), rotation)
        hashmark.start_x(value=loc_x)
        hashmark.start_z(value=loc_z)
        hashmark.parent(topshelf_obj)
        dim = self.add_tagged_dimension(hashmark.end_point)
        dim.start_x(value=0)
        dim.start_z(value=sn_unit.inch(2))
        dim.set_label("Exp.")

    def topshelf_exposed_labels(self, topshelf_obj):
        topshelf_assy = sn_types.Assembly(topshelf_obj)
        exposed_l_pmt = topshelf_assy.get_prompt("Exposed Left")
        exposed_r_pmt = topshelf_assy.get_prompt("Exposed Right")
        exposed_b_pmt = topshelf_assy.get_prompt("Exposed Back")

        if exposed_l_pmt and exposed_l_pmt.get_value():
            self.apply_topshelf_exposed_lbl(topshelf_obj, 'LEFT')
        if exposed_r_pmt and exposed_r_pmt.get_value():
            self.apply_topshelf_exposed_lbl(topshelf_obj, 'RIGHT')
        if exposed_b_pmt and exposed_b_pmt.get_value():
            self.apply_topshelf_exposed_lbl(topshelf_obj, 'BACK')

    def topshelf_depth(self, ts_assembly):
        obj_bp = ts_assembly.obj_bp
        ts_width = ts_assembly.obj_x.location.x
        ts_depth = ts_assembly.obj_y.location.y
        ts_height = ts_assembly.obj_z.location.z

        if obj_bp.parent.sn_closets.is_closet_top_bp:
            rotation = (0, 135, 0)
        else:
            rotation = (0, 45, 0)

        offset_x = ts_width / 2
        offset_y = ts_depth / 2
        hashmark = sn_types.Line(sn_unit.inch(6), rotation)
        hashmark.start_x(value=offset_x)
        hashmark.start_y(value=offset_y)
        hashmark.start_z(value=ts_height)
        hashmark.parent(obj_bp)
        dim = self.add_tagged_dimension(hashmark.end_point)
        dim.start_z(value=sn_unit.inch(2))
        dim.set_label(self.to_inch_lbl(abs(ts_depth)))
        self.topshelf_exposed_labels(obj_bp)

    def is_labeled_toe_kick(self, toe_kick_assy):
        toe_kick = toe_kick_assy.obj_bp
        parent_obj = toe_kick.parent
        grandparent_obj = parent_obj.parent
        if not toe_kick.sn_closets.is_toe_kick_skin_bp:
            hanging_tk = (grandparent_obj and
                          'section' in grandparent_obj.name.lower() and
                          'front' in toe_kick.name.lower())

            corner_tk = 'angle' in toe_kick.name.lower()

            lshelf_tk = (grandparent_obj and
                         'l shelves' in grandparent_obj.name.lower()
                         and not ('stringer' in toe_kick.name.lower()
                                  or 'back' in toe_kick.name.lower()))

            island_tk = (parent_obj.sn_closets.is_island and
                         'front' in toe_kick.name.lower())

            tk_options = {'hanging_tk': hanging_tk,
                          'corner_tk': corner_tk,
                          'lshelf_tk': lshelf_tk,
                          'island_tk': island_tk}

            for key, value in tk_options.items():
                if value:
                    return key

        else:
            return None

    def toe_kick_label(self, toe_kick_assy, tk_type):
        toe_kick = toe_kick_assy.obj_bp
        parent_obj = toe_kick.parent
        parent_assy = sn_types.Assembly(parent_obj)
        lbl_text = 'TK'
        lbl_tgt = toe_kick
        skin_pmt = parent_assy.get_prompt('Add TK Skin')
        toe_kick_x = toe_kick_assy.obj_x
        toe_kick_y = toe_kick_assy.obj_y

        width = toe_kick_x.location.x
        height = toe_kick_y.location.y

        lbl_loc = (width / 2, height / 2, 0)

        if tk_type == 'lshelf_tk':
            wall = sn_utils.get_parent_assembly_bp(toe_kick)
            wall_assy = sn_types.Assembly(wall)
            wall_obj_x = wall_assy.obj_x

            wall_a_x, wall_a_y = wall.matrix_world.translation[:2]
            wall_b_x, wall_b_y = wall_obj_x.matrix_world.translation[:2]

            dx_wall = wall_b_x - wall_a_x
            dy_wall = wall_b_y - wall_a_y
            vec_wall = mathutils.Vector((dx_wall, dy_wall))

            tk_a_x, tk_a_y = toe_kick.matrix_world.translation[:2]
            tk_b_x, tk_b_y = toe_kick_x.matrix_world.translation[:2]

            dx_tk = tk_b_x - tk_a_x
            dy_tk = tk_b_y - tk_a_y
            vec_tk = mathutils.Vector((dx_tk, dy_tk))

            cross_prod = round(vec_wall.cross(vec_tk), 2)

            if cross_prod != 0:
                return

        if tk_type == 'island_tk':
            skin_pmt = parent_assy.get_prompt('Add TK Skin')
            lbl_tgt = parent_obj
            island_w = parent_assy.obj_x.location.x
            island_d = parent_assy.obj_y.location.y
            lbl_x = island_w / 2
            lbl_y = island_d / 2
            lbl_loc = (lbl_x, lbl_y, -height / 2)

        if skin_pmt and skin_pmt.get_value():
            lbl_text += ' + 1/4" Skin'

        lbl = self.add_tagged_dimension(lbl_tgt)
        lbl.anchor.location = lbl_loc
        lbl.set_label(lbl_text)

    def toe_kick_garage_leg_dimension(self, assembly):
        assy_bp = assembly.obj_bp
        wall_bp = sn_utils.get_parent_assembly_bp(assy_bp)
        dim_name = 'TKGL_HGT'
        dim_exists = any([dim_name in c.name for c in wall_bp.children])

        if not dim_exists:
            assy_height = assembly.obj_z.location.z
            label = self.to_inch_lbl(assy_height)
            dim = self.add_tagged_dimension(wall_bp)
            dim.anchor.name = dim_name
            dim.start_x(value=-sn_unit.inch(2))
            dim.end_z(value=assy_height)
            dim.set_label(' ')
            text = self.add_tagged_dimension(dim.anchor)
            text.start_x(value=-sn_unit.inch(3))
            text.start_z(value=assy_height / 2)
            text.set_label(label)

    def toe_kick_skins_label(self, assembly):
        tk_skin = assembly.obj_bp
        lbl_x = assembly.obj_x.location.x / 2
        lbl_y = assembly.obj_y.location.y / 2
        lbl = self.add_tagged_dimension(tk_skin)
        lbl.set_label('1/4" TK Skin')
        lbl.start_x(value=lbl_x)
        lbl.start_y(value=lbl_y)

    def fullback_labeling(self, assembly):
        fullback_obj = assembly.obj_bp
        fullback_x = assembly.obj_x.location.x
        fullback_y = assembly.obj_y.location.y
        full_back_size = abs(self.to_inch(assembly.obj_z.location.z))
        fullback_props = fullback_obj.sn_closets
        use_unique_mat = fullback_props.use_unique_material
        label = ''

        if full_back_size == 0.25:
            label = 'F/B|1/4'
        if full_back_size == 0.75:
            label = 'F/B|3/4'

        if use_unique_mat:
            mat_type = fullback_props.unique_mat_types
            if mat_type == 'MELAMINE':
                label += f'|{fullback_props.unique_mat_mel}'
            elif mat_type == 'TEXTURED_MELAMINE':
                label += f'|{fullback_props.unique_mat_tex_mel}'
            elif mat_type == 'VENEER':
                veneer_mat = fullback_props.unique_mat_veneer
                veneer_txt = veneer_mat.split()[0]
                label += f'|{veneer_txt.lower().capitalize()}'

        lbl_x = fullback_x / 2 + sn_unit.inch(2)
        lbl_y = fullback_y / 2
        dim = self.add_tagged_dimension(fullback_obj)
        dim.start_x(value=lbl_x)
        dim.start_y(value=lbl_y)
        dim.set_label(label)

    
    def slanted_shoes_shelves(self, item):
        if item in tagged_sss_list:
            return
        sss_assembly = sn_types.Assembly(item)
        shelf_lip_prompt = sss_assembly.get_prompt("Shelf Lip Type")
        shelf_qty_prompt = sss_assembly.get_prompt("Adj Shelf Qty")
        shelf_offset_prompt = sss_assembly.get_prompt(
            "Distance Between Shelves")
        shf_lip_val = shelf_lip_prompt.get_value()
        shelf_lip = shelf_lip_prompt.combobox_items[shf_lip_val].name
        shelf_offset = float(shelf_offset_prompt.get_value())
        shelf_qty = int(shelf_qty_prompt.get_value())
        z_offset = (shelf_qty - 1) * shelf_offset
        width = sss_assembly.obj_x.location.x
        x_offset = width / 2
        label = "SSS"
        # Skip adding shelf lip type for now. Currently slanted shoe shelf lip options are inaccurate.
        # label = f'SSS {shelf_lip} Lip'
        rotation = (0, 45, 0)
        hashmark = sn_types.Line(sn_unit.inch(6), rotation)
        hashmark.parent(item)
        hashmark.start_x(value=x_offset)
        hashmark.start_z(value=z_offset)
        dim = self.add_tagged_dimension(hashmark.end_point)
        dim.start_z(value=sn_unit.inch(2))
        dim.set_label(label)
        tagged_sss_list.append(item)
    
    def apply_drawer_lbl(self, drawer_stack, drawer_num, label):
        drawer_front = drawer_stack.get_drawer_front(drawer_num)
        hshmk_x = drawer_front.obj_x.location.x / 2
        hshmk_len = sn_unit.inch(4)
        hshmk = sn_types.Line(hshmk_len, (90, 45, 0))
        hshmk.parent(drawer_front.obj_bp)
        hshmk.start_x(value=hshmk_x)
        hshmk.end_y(value=-hshmk_len)
        lbl = self.add_tagged_dimension(hshmk.anchor)
        lbl.set_label(label)
        lbl.start_x(value=sn_unit.inch(2))
        lbl.start_y(value=-hshmk_len * 2)
        lbl.start_z(value=sn_unit.inch(8))

    def query_velvet_liner(self, drawer_stack, drawer_num):
        width_in = round(sn_unit.meter_to_inch(drawer_stack.obj_x.location.x))
        insert_width = 0
        vl18 = [3,4,5]
        vl21 = [4,5,6]
        vl24 = [4,5,6]
        if 18 <= width_in < 21:
            insert_width = 18
        elif 21 <= width_in < 24:
            insert_width = 21
        elif 24 <= width_in:
            insert_width = 24

        insert_type_ppt = drawer_stack.get_prompt(f'Jewelry Insert Type {drawer_num}')

        if insert_type_ppt:
            insert_type = insert_type_ppt.get_value()
            # Double Jewelry
            if insert_type == 0:
                upper = f'Upper Jewelry Insert Velvet Liner {insert_width}in {drawer_num}'
                lower = f'Lower Jewelry Insert Velvet Liner {insert_width}in {drawer_num}'
                u_choice = drawer_stack.get_prompt(upper).get_value()
                l_choice = drawer_stack.get_prompt(lower).get_value()
                if insert_width == 18 and (u_choice in vl18 or l_choice in vl18):
                    return True
                elif insert_width == 21 and (u_choice in vl21 or l_choice in vl21):
                    return True
                elif insert_width == 24 and (u_choice in vl24 or l_choice in vl24):
                    return True
            # STD Insert
            elif insert_type == 1:
                jwl_ins = f'Jewelry Insert {insert_width}in {drawer_num}'
                sld_ins = f'Sliding Insert {insert_width}in {drawer_num}'
                j_choice = drawer_stack.get_prompt(jwl_ins).get_value()
                s_choice = drawer_stack.get_prompt(sld_ins).get_value()
                drawer_stack.get_prompt(sld_ins)
                if insert_width == 18 and (j_choice in vl18 or s_choice in vl18):
                    return True
                elif insert_width == 21 and (j_choice in vl21 or s_choice in vl21):
                    return True
                elif insert_width == 24 and (j_choice in vl24 or s_choice in vl24):
                    return True
            # Non-STD Insert GT 16
            elif insert_type == 2:
                lower = f'Lower Jewelry Insert Velvet Liner {insert_width}in {drawer_num}'
                l_choice = drawer_stack.get_prompt(lower).get_value()
                if insert_width == 18 and l_choice in vl18:
                    return True
                elif insert_width == 21 and l_choice in vl21:
                    return True
                elif insert_width == 24 and l_choice in vl24:
                    return True
            # Non-STD Insert LT 16
            elif insert_type == 3:
                return True
        return False

    def jewelry_drawer_labeling(self, assembly):
        drawer_stack = data_drawers.Drawer_Stack(assembly.obj_bp)
        drawer_quantity = drawer_stack.get_prompt("Drawer Quantity")

        for drawer_num in range(1, drawer_quantity.get_value()):
            has_velvet_liner = False
            use_dbl_drawer = drawer_stack.get_prompt("Use Double Drawer " + str(drawer_num))
            is_dbl_drawer = use_dbl_drawer.get_value()
            has_jwl_insert_pmpt = drawer_stack.get_prompt(f'Has Jewelry Insert {drawer_num}')
            has_sld_insert_pmpt = drawer_stack.get_prompt(f'Has Sliding Insert {drawer_num}')
            has_velvet_liner = self.query_velvet_liner(drawer_stack, drawer_num)

            if has_jwl_insert_pmpt and has_sld_insert_pmpt:
                has_jwl_insert = has_jwl_insert_pmpt.get_value()
                has_sld_insert = has_sld_insert_pmpt.get_value()

                if is_dbl_drawer and not has_velvet_liner:
                    self.apply_drawer_lbl(drawer_stack, drawer_num, 'Db Jwlry')
                elif not is_dbl_drawer and not has_velvet_liner:
                    if has_jwl_insert and not has_sld_insert:
                        self.apply_drawer_lbl(drawer_stack, drawer_num, 'Jwlry')
                    elif not has_jwl_insert and has_sld_insert:
                        self.apply_drawer_lbl(drawer_stack, drawer_num, 'SLD')
                    elif has_jwl_insert and has_sld_insert:
                        self.apply_drawer_lbl(drawer_stack, drawer_num, 'Jwlry + SLD')
                elif has_velvet_liner:
                    self.apply_drawer_lbl(drawer_stack, drawer_num, 'VL')

    def lock_labeling(self, assembly):
        lock_obj = assembly.obj_bp
        prnt_assy = sn_types.Assembly(lock_obj.parent)
        lbl_str = ''
        lbl_x = 0
        lbl_y = 0
        lbl_loc = (0, 0, 0)
        lbl_rot = (135, 0, 0)
        add_hsh = False
        lbl_prnt = lock_obj
        hsh_len = sn_unit.inch(5)

        if prnt_assy.obj_bp.sn_closets.is_drawer_stack_bp:
            pmt_val = ''
            # Get placement value of each lock
            for d in lock_obj.animation_data.drivers:
                d_vars = d.driver.variables
                var = None
                for v in d_vars:
                    if v.name == 'Lock_Drawer':
                        var = v
                if var:
                    dp = var.targets[0].data_path
                    pmt_name = dp.split('"')[1]
                    src_pmt = prnt_assy.get_prompt(pmt_name)
                    pmt_num = src_pmt.get_value()
            pmt_val = src_pmt.combobox_items[pmt_num].name
            if pmt_val != '' and pmt_val != 'None':
                if pmt_val == 'Top':
                    lbl_x = -sn_unit.inch(5.5)
                    lbl_loc = (lbl_x, 0, lbl_y)
                    lbl_str = 'Top Lock'
                else:
                    add_hsh = True
                    lbl_y = hsh_len + sn_unit.inch(1.5)
                    lbl_loc = (0, lbl_x, lbl_y)
                    lbl_str = f'{pmt_val[0]} Lock'

        elif prnt_assy.obj_bp.sn_closets.is_door_insert_bp:
            lck_pnl = prnt_assy.get_prompt('Lock to Panel')
            doors = [d for d in prnt_assy.obj_bp.children if
                     d.sn_closets.is_door_bp and
                     props_closet.part_is_not_hidden(sn_types.Assembly(d))]

            if lck_pnl and lck_pnl.get_value():
                for d in doors:
                    if 'left door' in d.name.lower():
                        lbl_str = 'R Panel|Lock'
                    elif 'right door' in d.name.lower():
                        lbl_str = 'L Panel|Lock'
                add_hsh = True
                hsh_len = sn_unit.inch(2)
                lbl_y = hsh_len + sn_unit.inch(3)
                lbl_loc = (0, lbl_x, lbl_y)
                lbl_rot = (45, 0, 0)

            else:
                lbl_str = 'Lock'
                lbl_x = -sn_unit.inch(5.5)
                if len(doors) == 2:
                    lbl_loc = (0, lbl_y, lbl_x)
                else:
                    lbl_loc = (lbl_x, 0, lbl_y)

        if add_hsh:
            hshmk = sn_types.Line(hsh_len, lbl_rot)
            hshmk.parent(lock_obj)
            lbl_prnt = hshmk.anchor

        lbl = self.add_tagged_dimension(lbl_prnt)
        lbl.anchor.location = lbl_loc
        lbl.set_label(lbl_str)

    def filler_labeling(self, filler, position='down'):
        filler_assy = sn_types.Assembly(filler)
        filler_bp = filler_assy.obj_bp
        filler_measure = filler_assy.obj_y.location.y
        filler_amount = self.to_inch_lbl(abs(filler_measure))
        z_offset = 0
        if position == 'down':
            z_offset = -(filler_bp.location.z + sn_unit.inch(4.5))
        elif position == 'up':
            z_offset = filler_assy.obj_x.location.x + sn_unit.inch(4.5)
        lbl_txt = f'{filler_amount}|Filler'
        # Filler Measure
        # NOTE to change Z-position change X values
        #      to change X-position change Y values
        filler_lbl = self.add_tagged_dimension(filler_bp)
        filler_lbl.start_x(value=z_offset)
        filler_lbl.start_y(value=filler_measure / 2)
        filler_lbl.set_label(lbl_txt)

    def upper_lower_filler_labeling(self, wall_bp):
        MAX_FILLERS = 2
        left_fillers = []
        right_fillers = []
        tag = 'section'
        sections = (sec for sec in wall_bp.children if tag in sec.name.lower())
        for section in sections:
            for filler in section.children:
                is_filler = filler.sn_closets.is_filler_bp
                not_capping = 'capping' not in filler.name.lower()
                left = 'left' in filler.name.lower()
                right = 'right' in filler.name.lower()
                if is_filler and not_capping:
                    z_loc = filler.location[2]
                    width = abs(sn_types.Assembly(filler).obj_y.location.y)
                    width_in = self.to_inch(width)
                    if left and width_in > 0:
                        left_fillers.append((z_loc, width_in, filler))
                    elif right and width_in > 0:
                        right_fillers.append((z_loc, width_in, filler))
        fillers_list = [left_fillers, right_fillers]
        for fillers in fillers_list:
            fillers = sorted(fillers, key=lambda tup: tup[0])
            fillers_meas_qty = len(list(set([fil[1] for fil in fillers])))
            if fillers_meas_qty == 1:
                # apply just the first one as they are the same
                desired_filler = fillers[0][2]
                self.filler_labeling(desired_filler, 'down')
            elif fillers_meas_qty > 1:
                lower, upper = fillers[:MAX_FILLERS]
                self.filler_labeling(lower[2], 'down')
                self.filler_labeling(upper[2], 'up')


    def capping_bottom_label(self, assembly):
        assy_bp = assembly.obj_bp
        [cp_btm_bp] = [obj for obj in assy_bp.children
                       if obj.get('IS_BP_ASSEMBLY')]

        # Main capping bottom label
        cp_btm_assy = sn_types.Assembly(cp_btm_bp)
        exp_l = cp_btm_assy.get_prompt('Exposed Left')
        exp_r = cp_btm_assy.get_prompt('Exposed Right')
        cp_btm_width = cp_btm_assy.obj_x.location.x
        cp_btm_depth = cp_btm_assy.obj_y.location.y

        hshmk_size = sn_unit.inch(2)
        label_off = sn_unit.inch(2.5)
        hshmk_rot = (0, -45, 0)
        hshmk = sn_types.Line(hshmk_size, hshmk_rot)
        hshmk.parent(cp_btm_bp)
        hshmk.start_x(value=cp_btm_width / 2)
        label_str = f'Cap. Bttm {self.to_inch_lbl(cp_btm_depth)}'

        label = self.add_tagged_dimension(hshmk.end_point)
        label.start_z(value=label_off)
        label.set_label(label_str)

        # Exposed edges labels
        if exp_l and exp_l.get_value():
            hshmk_exp_l = sn_types.Line(hshmk_size, hshmk_rot)
            hshmk_exp_l.parent(cp_btm_bp)
            label_exp_l = self.add_tagged_dimension(hshmk_exp_l.end_point)
            label_exp_l.start_z(value=label_off)
            label_exp_l.set_label('Exp.')

        if exp_r and exp_r.get_value():
            hshmk_exp_r = sn_types.Line(hshmk_size, (0, 45, 0))
            hshmk_exp_r.parent(cp_btm_bp)
            hshmk_exp_r.start_x(value=cp_btm_width)
            label_exp_r = self.add_tagged_dimension(hshmk_exp_r.end_point)
            label_exp_r.start_z(value=label_off)
            label_exp_r.set_label('Exp.')

    def add_glass_cutpart_dim(self, assembly, part, thickness):
        setback = 0.25
        z_qty = part.modifiers["ZQuantity"]
        section_depth = self.to_inch(assembly.location[1])
        shelf_depth = self.to_inch(part.dimensions[1])
        depth_part_diff = abs(section_depth - shelf_depth)
        shelves_qtt = z_qty.count
        shelves_offset = z_qty.constant_offset_displace[2]
        width = part.dimensions[0]
        # For cutparts that differs from the section depth minus setback (0.25)
        if depth_part_diff != setback and depth_part_diff != 0.0:
            label = self.to_inch_lbl(part.dimensions[1])
        else:
            label = self.to_inch_lbl(assembly.location[1])
        label += f' Glass {thickness}'
        for i in range(shelves_qtt):
            z_offset = shelves_offset + (shelves_offset * (i - 1))
            hshmk_size = sn_unit.inch(5)
            rotation = (0, 45, 0)
            hashmark = sn_types.Line(hshmk_size, rotation)
            hashmark.parent(part)
            hashmark.start_x(value=width / 2)
            hashmark.start_z(value=z_offset)
            dim = self.add_tagged_dimension(hashmark.end_point)
            dim.start_z(value=sn_unit.inch(2))
            dim.set_label(label)

    def glass_shelves(self, item):
        shelves = item.parent
        thickness_dict = {
            0: '1/4"',
            1: '3/8"',
            2: '1/2"'
        }
        assy = sn_types.Assembly(shelves)
        glass_prompt_th = assy.get_prompt("Glass Shelf Thickness")
        thickness = thickness_dict[glass_prompt_th.get_value()]
        for child in shelves.children:
            glass = 'glass' in child.name.lower()
            shf = 'shelf' in child.name.lower()
            for shelf in child.children:
                if shelf.type == "MESH" and glass and shf:
                    self.add_glass_cutpart_dim(child, shelf, thickness)

    # Its to figure out if has variable children
    variable_sections_list = []

    def has_variable_descendants(self, item):
        opn = item.sn_closets.opening_name
        if opn:
            crcss_assy = sn_types.Assembly(item.parent)
            var_sect = crcss_assy.get_prompt(f'CTF Opening {opn}').get_value()
            if var_sect:
                self.variable_sections_list.append(opn)
            if len(item.children) > 0:
                for i in item.children:
                    self.has_variable_descendants(i)

    def variable_opening_label(self, item):
        for n_item in item.children:
            if n_item.snap.type_group == 'OPENING':
                self.has_variable_descendants(n_item)
                variable_sections = set(self.variable_sections_list)
                self.variable_sections_list = []
                if len(variable_sections) > 0:
                    section_width = sn_types.Assembly(n_item).obj_x.location.x
                    dim = self.add_tagged_dimension(n_item)
                    dim.start_x(value=section_width / 2)
                    dim.start_y(value=section_width / 2)
                    dim.start_z(value=-sn_unit.inch(7) - n_item.location.z)
                    dim.set_label("Var.")

    def valances_labeling(self, assembly):
        valance_obj = assembly.obj_bp
        width = assembly.obj_x.location.x
        height = assembly.get_prompt('Molding Height').get_value()
        location = assembly.get_prompt('Molding Location').get_value()
        x_offset = width / 2
        z_offset = -(abs(height) + abs(location))
        rotation = (135, 0, 90)
        label = f'Valance {self.to_inch_lbl(abs(height))}'
        hashmark = sn_types.Line(sn_unit.inch(2), rotation)
        hashmark.parent(valance_obj)
        hashmark.start_x(value=x_offset)
        hashmark.start_z(value=z_offset)
        dim = self.add_tagged_dimension(hashmark.end_point)
        dim.start_z(value=sn_unit.inch(2))
        dim.set_label(label)

    def blind_corner_panel_labels(self, bcp):
        bcp_obj = bcp.obj_bp
        siblings = bcp_obj.parent.children
        opns = [sn_types.Assembly(obj) for obj in siblings if
                obj.snap.type_group == 'OPENING']

        is_l_bcp = bcp.get_prompt('Is Left Blind Corner Panel')
        is_r_bcp = bcp.get_prompt('Is Right Blind Corner Panel')
        bcp_x = bcp.obj_bp.location.x
        bcp_y = bcp.obj_bp.location.y
        bcp_z = bcp.obj_bp.location.z
        bcp_w = bcp.obj_y.location.y
        bcp_h = bcp.obj_x.location.x
        bcp_d = bcp.obj_z.location.z

        bcp_str = f'{self.to_inch_lbl(bcp_w)} BCP'
        bcp_lbl_x = bcp_h * 0.55
        bcp_lbl_y = bcp_w * 0.5
        bcp_lbl = self.add_tagged_dimension(bcp_obj)
        bcp_lbl.set_label(bcp_str)
        bcp_lbl.start_x(value=bcp_lbl_x)
        bcp_lbl.start_y(value=bcp_lbl_y)

        for opn in opns:
            opn_x = opn.obj_bp.location.x
            opn_y = opn.obj_bp.location.y
            opn_z = opn.obj_bp.location.z
            opn_w = opn.obj_x.location.x
            opn_h = opn.obj_z.location.z

            match_x, match_y, match_z = False, False, False

            if is_l_bcp and is_l_bcp.get_value():
                bcp_dx = bcp_x + bcp_d
                bcp_dy = bcp_y + bcp_d
                bcp_dz = bcp_z + (bcp_h - opn_h) * 0.5

                match_x = math.isclose(bcp_dx, opn_x, abs_tol=1e-3)
                match_y = math.isclose(bcp_dy, opn_y, abs_tol=1e-3)
                match_z = math.isclose(bcp_dz, opn_z, abs_tol=1e-3)

            elif is_r_bcp and is_r_bcp.get_value():
                opn_dx = opn_x + opn_w + bcp_d
                bcp_dz = bcp_z + (bcp_h - opn_h) * 0.5

                match_x = math.isclose(bcp_x, opn_dx, abs_tol=1e-3)
                match_y = math.isclose(bcp_y, opn_y, abs_tol=1e-3)
                match_z = math.isclose(bcp_dz, opn_z, abs_tol=1e-3)

            if match_x and match_y and match_z:
                gap_w = opn_w - bcp_w
                gap_str = f'{self.to_inch_lbl(gap_w + bcp_d)} Open'
                gap_lbl_x = -sn_unit.inch(3)
                gap_lbl_y = opn_w - gap_w * 0.5
                gap_lbl = self.add_tagged_dimension(bcp_obj)
                gap_lbl.set_label(gap_str)
                gap_lbl.start_x(value=gap_lbl_x)
                gap_lbl.start_y(value=gap_lbl_y)

    def flat_crown(self, item):
        wall = sn_types.Assembly(item.parent.parent)
        assy = sn_types.Assembly(item.parent)
        hang_h = assy.obj_z.location.z
        tkd_vo = assy.get_prompt('Top KD 1 Vertical Offset')
        labels = []
        tkh_str = ''
        fc_prod = sn_types.Assembly(item)
        ext_ceil = fc_prod.get_prompt('Extend To Ceiling')
        tkh = fc_prod.get_prompt('Top KD Holes Down')
        if ext_ceil and ext_ceil.get_value() and tkh and tkd_vo:
            if tkh.get_value() == 1:
                tkh_str = 'Top KD|Down 1 Hole'
            elif tkh.get_value() == 2:
                tkh_str = 'Top KD|Down 2 Holes'
            hang_h -= tkd_vo.get_value()
        for a in item.children:
            if a.get("IS_BP_ASSEMBLY") and 'Flat Crown' in a.name:
                fc_assy = sn_types.Assembly(a)
                fc_h = fc_assy.obj_y.location.y
                fc_str = 'Flat Crown %s' % self.to_inch_lbl(fc_h)
                labels.append((fc_str, fc_h))

        labels = list(dict.fromkeys(labels))
        if tkh_str:
            labels.append((tkh_str, -sn_unit.inch(3)))

        for l in labels:
            lbl = self.add_tagged_dimension(wall.obj_bp)
            lbl.set_label(l[0])
            lbl_z = hang_h + (l[1] * 0.5)
            lbl.start_x(value=sn_unit.inch(-20))
            lbl.start_z(value=lbl_z)

    def light_rails_labeling(self, assembly):
        light_rail_obj = assembly.obj_bp
        width = assembly.obj_x.location.x
        height = assembly.get_prompt('Molding Height').get_value()
        location = assembly.get_prompt('Molding Location').get_value()
        x_offset = width / 2
        z_offset = -(abs(height) + abs(location))
        rotation = (135, 0, 90)
        label = f'Light Rails {self.to_inch_lbl(abs(height))}'
        hashmark = sn_types.Line(sn_unit.inch(2), rotation)
        hashmark.parent(light_rail_obj)
        hashmark.start_x(value=x_offset)
        hashmark.start_z(value=z_offset)
        dim = self.add_tagged_dimension(hashmark.end_point)
        dim.start_z(value=sn_unit.inch(2))
        dim.set_label(label)

    def wall_cleat_dimensions(self, assy):
        obj = assy.obj_bp
        labeled_cleat = None
        width = 0
        height = 0
        all_cleats = [sn_types.Assembly(c) for c in obj.children
                      if 'cleat' in c.name.lower()]

        for cleat_assy in all_cleats:
            hide_pmt = cleat_assy.get_prompt('Hide')
            if hide_pmt and not hide_pmt.get_value():
                labeled_cleat = cleat_assy

        if labeled_cleat: 
            dim_offset = -sn_unit.inch(3)
            cleat_aff_dist = labeled_cleat.obj_bp.matrix_world.translation.z
            width = labeled_cleat.obj_x.location.x
            height = labeled_cleat.obj_y.location.y
            dim_w_anchor_loc = (0, height + dim_offset, 0)
            dim_h_end_loc = (0, height, 0)
            aff_dim_anchor_loc = (0, 0, 0)
            aff_dim_end_loc = (0, cleat_aff_dist, 0)

            # Width dimension
            dim_w = self.add_tagged_dimension(labeled_cleat.obj_bp)
            dim_w.set_horizontal_line_txt_pos('BOTTOM')
            lbl_w = self.to_inch_lbl(width)
            dim_w.anchor.location = dim_w_anchor_loc 
            dim_w.end_x(value=width)
            dim_w.set_label(" ")
            width_lbl = self.add_tagged_dimension(labeled_cleat.obj_bp)
            width_lbl.anchor.location = (
                width / 2, height + dim_offset + sn_unit.inch(-2), 0)
            width_lbl.set_label(lbl_w)

            # Cleat height dimension
            dim_h = self.add_tagged_dimension(labeled_cleat.obj_bp)
            lbl_h = self.to_inch_lbl(abs(height))
            dim_h.start_x(value=dim_offset)
            dim_h.end_point.location = dim_h_end_loc
            dim_h.set_label(lbl_h)

            # Height above the floor dimension
            aff_dim = self.add_tagged_dimension(labeled_cleat.obj_bp)
            aff_dim.anchor.location = aff_dim_anchor_loc
            aff_dim.end_point.location = aff_dim_end_loc
            aff_dim.set_label(self.to_inch_lbl(cleat_aff_dist))

    def ts_support_corbel_dimensions(self, assy):
        width = assy.obj_x.location.x
        wall_bp = sn_utils.get_wall_bp(assy.obj_bp)
        wall_assy = sn_types.Assembly(wall_bp)
        fills_wall = False

        if wall_assy:
            wall_width = round(wall_assy.obj_x.location.x, 2)
            ts_width = round(assy.obj_x.location.x, 2)
            if wall_width == ts_width:
                fills_wall = True

        if not fills_wall:
            # Width dimension
            dim_w = self.add_tagged_dimension(assy.obj_bp)
            dim_w.set_horizontal_line_txt_pos('BOTTOM')
            lbl_w = self.to_inch_lbl(width)
            dim_w.anchor.location.z = sn_unit.inch(3)
            dim_w.end_x(value=width)
            dim_w.set_label(" ")
            width_lbl = self.add_tagged_dimension(assy.obj_bp)
            width_lbl.anchor.location = (width / 2, 0, sn_unit.inch(6))
            width_lbl.set_label(lbl_w)

    def countertop_hashmark(self, context, item):
        material_name = ""
        material_dict = {
            0: 'Melamine',
            1: 'HPL',
            2: 'Granite'
        }
        ctop_assembly = sn_types.Assembly(item)
        ctop_mat_pmpt = ctop_assembly.get_prompt("Countertop Type")
        ctop_mat_option = ctop_mat_pmpt.get_value()
        material_str = material_dict.get(ctop_mat_option)
        width = abs(ctop_assembly.obj_x.location.x)
        counter_top_width = 0
        counter_top_depth = 0
        counter_top_height = 0
        # item is at CTOP INSERT level
        for k_item in item.children:
            for x_item in k_item.children:
                if not x_item.hide_viewport and 'hashmark' not in x_item.name.lower():
                    for sibling in x_item.parent.children:
                        if sibling.get("obj_x"):
                            counter_top_width = abs(sibling.location.x)
                        if sibling.get("obj_y"):
                            counter_top_depth = abs(sibling.location.y)
                        if sibling.get("obj_z"):
                            counter_top_height = abs(sibling.location.z)
        context_material = material_name
        material = ""
        if material_str is not None:
            material += material_str
        if not None:
            material += context_material
        material += " "
        for spec_group in context.scene.snap.spec_groups:
            material += spec_group.materials["Countertop_Surface"].item_name
        x_offset = width / 2
        z_offset = counter_top_height
        hashmark = sn_types.Line(sn_unit.inch(3), (0, 45, 0))
        hashmark.parent(item)
        hashmark.start_x(value=x_offset)
        hashmark.start_z(value=z_offset)
        counter_top_width_str = self.to_inch_lbl(counter_top_width)
        counter_top_depth_str = self.to_inch_lbl(counter_top_depth)
        # Countertop Dimensions
        label = (material + " C.T. " + counter_top_width_str +
                    " x " + counter_top_depth_str)
        ctop_dim = self.add_tagged_dimension(hashmark.end_point)
        ctop_dim.start_z(value=sn_unit.inch(2))
        ctop_dim.set_label(label)

    def ctop_exposed_dim(self, parent, location, rotation):
        mark = sn_types.Line(sn_unit.inch(3), rotation)
        mark.parent(parent)
        mark.anchor.location = location
        dim = self.add_tagged_dimension(mark.end_point)
        dim.start_z(value=sn_unit.inch(2))
        dim.set_label("Exp.")

    def countertop_exposed_label(self, item):
        ctop_assembly = sn_types.Assembly(item)
        ctop_exposed_left = ctop_assembly.get_prompt("Exposed Left")
        ctop_exposed_right = ctop_assembly.get_prompt("Exposed Right")
        ctop_exposed_back = ctop_assembly.get_prompt("Exposed Back")
        extended_left = ctop_assembly.get_prompt("Extend Left Amount")
        extended_right = ctop_assembly.get_prompt(
            "Extend Right Amount")
        width = abs(ctop_assembly.obj_x.location.x)
        counter_top_height = 0
        # item is at CTOP INSERT level
        for k_item in item.children:
            for x_item in k_item.children:
                if not x_item.hide_viewport and 'hashmark' not in x_item.name.lower():
                    for sibling in x_item.parent.children:
                        if sibling.get("obj_z"):
                            counter_top_height = abs(
                                sibling.location.z)
        z_offset = counter_top_height
        if ctop_exposed_left.get_value() is True:
            extension = 0
            if extended_left is not None:
                extension = extended_left.get_value()
            offset = -extension
            location = (offset, 0, z_offset)
            rotation = (0, -45, 0)
            self.ctop_exposed_dim(item, location, rotation)
        if ctop_exposed_right.get_value() is True:
            extension = 0
            if extended_right is not None:
                extension = extended_right.get_value()
            offset = width + extension
            location = (offset, 0, z_offset)
            rotation = (0, 45, 0)
            self.ctop_exposed_dim(item, location, rotation)
        if ctop_exposed_back.get_value() is True:
            offset = width / 4
            location = (offset, 0, z_offset)
            rotation = (0, -45, 0)
            self.ctop_exposed_dim(item, location, rotation)

    def ct_overhang_label(self, assembly):
        obj_bp = assembly.obj_bp
        hsh_len = sn_unit.inch(5.5)
        lbl_off = sn_unit.inch(2)
        labels = []

        # Labeling overhangs for islands
        if obj_bp.sn_closets.is_island:
            no_ct = assembly.get_prompt('No Countertop')
            use_ct = no_ct and not no_ct.get_value()

            if use_ct:
                isl_w = assembly.obj_x.location.x
                isl_d = assembly.obj_y.location.y
                isl_h = assembly.obj_z.location.z
                toe_kick_h = assembly.get_prompt('Toe Kick Height').get_value()
                ct_loc_z = isl_h + toe_kick_h

                deck_overhang_pmt = assembly.get_prompt('Deck Overhang')
                if deck_overhang_pmt:
                    deck_overhang = deck_overhang_pmt.get_value()

                sides_overhang_pmt = assembly.get_prompt('Side Deck Overhang')
                if sides_overhang_pmt:
                    sides_overhang = sides_overhang_pmt.get_value()

                l_to_wall_pmt = assembly.get_prompt('Left Against Wall')
                if l_to_wall_pmt:
                    l_to_wall = l_to_wall_pmt.get_value()

                r_to_wall_pmt = assembly.get_prompt('Right Against Wall')
                if r_to_wall_pmt:
                    r_to_wall = r_to_wall_pmt.get_value()

                if deck_overhang > 0:
                    # Front label
                    labels.append(dict(
                        ext=deck_overhang,
                        hshmk_rot=(0, -135, 90),
                        hsh_st_x=isl_w * 0.25,
                        hsh_st_y=isl_d - deck_overhang,
                        hsh_st_z=ct_loc_z))

                    # Back label
                    labels.append(dict(
                        ext=deck_overhang,
                        hshmk_rot=(0, -135, -90),
                        hsh_st_x=isl_w * 0.25,
                        hsh_st_y=deck_overhang,
                        hsh_st_z=ct_loc_z))

                if sides_overhang > 0:
                    # Left label
                    if not l_to_wall:
                        labels.append(dict(
                            ext=sides_overhang,
                            hshmk_rot=(0, -135, 0),
                            hsh_st_x=-sides_overhang,
                            hsh_st_y=isl_d * 0.25,
                            hsh_st_z=ct_loc_z))

                    # Right label
                    if not r_to_wall:
                        labels.append(dict(
                            ext=sides_overhang,
                            hshmk_rot=(0, 135, 0),
                            hsh_st_x=isl_w + sides_overhang,
                            hsh_st_y=isl_d * 0.25,
                            hsh_st_z=ct_loc_z))

        # Labeling overhangs for countertop inserts
        elif obj_bp.sn_closets.is_counter_top_insert_bp:
            ctop_w = assembly.obj_x.location.x
            ctop_d = assembly.obj_y.location.y

            left_overhang_pmt = assembly.get_prompt('Extend Left Amount')
            if left_overhang_pmt:
                left_overhang = left_overhang_pmt.get_value()

            right_overhang_pmt = assembly.get_prompt('Extend Right Amount')
            if right_overhang_pmt:
                right_overhang = right_overhang_pmt.get_value()

            # Left label
            if left_overhang > 0:
                labels.append(dict(
                    ext=left_overhang,
                    hshmk_rot=(0, -135, 0),
                    hsh_st_x=-left_overhang,
                    hsh_st_y=ctop_d * 0.5,
                    hsh_st_z=0))

            # Right label
            if right_overhang > 0:
                labels.append(dict(
                    ext=right_overhang,
                    hshmk_rot=(0, 135, 0),
                    hsh_st_x=ctop_w + right_overhang,
                    hsh_st_y=ctop_d * 0.5,
                    hsh_st_z=0))

        for info in labels:
            hshmk = sn_types.Line(hsh_len, info['hshmk_rot'])
            hshmk.parent(obj_bp)
            hshmk.start_x(value=info['hsh_st_x'])
            hshmk.start_y(value=info['hsh_st_y'])
            hshmk.start_z(value=info['hsh_st_z'])

            lbl = self.add_tagged_dimension(hshmk.end_point)
            lbl_str = f'{self.to_inch_lbl(info["ext"])} Overhang'
            lbl.set_label(lbl_str)
            lbl.start_z(value=lbl_off)


    def section_bh(self, bh_dims, item):
        build_height_dim = 0
        countertop_height = 0
        ctop_thickness = 0
        topshelf_thickness = 0
        hanging_assy = sn_types.Assembly(item)
        hanging_height = 0
        if hasattr(hanging_assy.obj_z, 'location'):
            hanging_height = hanging_assy.obj_z.location.z
            for n_item in item.children:
                if 'counter top' in n_item.name.lower():
                    countertop_height = n_item.location[2]
                    for k_item in n_item.children:
                        for x_item in k_item.children:
                            if not x_item.hide_viewport:
                                ctop_thickness = abs(x_item.dimensions[2])

                if 'top shelf' in n_item.name.lower():
                    for k_item in n_item.children:
                        if 'topshelf' in k_item.name.lower():
                            for f_item in k_item.children:
                                if f_item.type == "MESH":
                                    assy = sn_types.Assembly(k_item)
                                    topshelf_thickness = abs(
                                                assy.obj_z.location.z)

        # Get world location z from each partition obj_x
        obj_bp = hanging_assy.obj_bp
        partitions = [sn_types.Assembly(obj) for obj in obj_bp.children if obj.sn_closets.is_panel_bp]
        partition_world_heights = [p.obj_x.matrix_world.translation.z for p in partitions]
        tallest_partition_height = max(partition_world_heights)

        hanging = hanging_height > 0
        ctop = ctop_thickness == 0
        tshelf = topshelf_thickness == 0
        if hanging and ctop and tshelf:
            build_height_dim = tallest_partition_height
        elif ctop_thickness > 0:
            build_height_dim = (countertop_height + ctop_thickness)
        elif topshelf_thickness > 0:
            build_height_dim = (tallest_partition_height + topshelf_thickness)
        bh_dims.append(build_height_dim)


    def strict_corner_bh(self, bh_dims, item):
        tk_height = 0
        tsh_height = 0
        for tk in item.children:
            if 'toe kick' in tk.name.lower():
                tk_assy = sn_types.Assembly(tk)
                tk_height = tk_assy.obj_z.location.z
        lsh_assy = sn_types.Assembly(item)
        tsh = lsh_assy.get_prompt("Add Top Shelf").get_value()
        if tsh:
            tsh_height += sn_unit.inch(0.75)
        lsh_height = lsh_assy.obj_z.location.z
        bh_dims.append(lsh_height + tk_height + tsh_height)

    def ts_support_corbel_bh(self, bh_dims, item):
        product = sn_types.Assembly(item)
        bh_dims.append(product.obj_bp.location.z)

    def build_height_dimension(self, wall_bp):
        bh_dims = []
        for item in wall_bp.children:
            if 'section' in item.name.lower():
                self.section_bh(bh_dims, item)
            if 'corner shelves' in item.name.lower():
                self.strict_corner_bh(bh_dims, item)
            if 'l shelves' in item.name.lower():
                self.strict_corner_bh(bh_dims, item)
            if 'IS_TOPSHELF_SUPPORT_CORBELS' in item:
                self.ts_support_corbel_bh(bh_dims, item)
        bh_dims = [round(dim, 4) for dim in bh_dims]
        bh_dims = list(set(bh_dims))
        bh_dims = sorted(bh_dims)
        for i, value in enumerate(bh_dims):
            self.apply_build_height_label(wall_bp, value, i)
        dims_offset = (sn_unit.inch(-4) * len(bh_dims))
        max_offset = sn_unit.inch(-7) + dims_offset
        return max_offset


    def apply_build_height_label(self, wall_bp, position, multiplier):
        offset = sn_unit.inch(-7) + (sn_unit.inch(-4) * multiplier)
        dim = self.add_tagged_dimension(wall_bp)
        dim.start_x(value=offset)
        dim.start_y(value=offset)
        dim.start_z(value=0)
        dim.end_z(value=position)
        label = self.to_inch_lbl(position)
        dim.set_label(label)

    def section_depths(self, wall_bp):
        wall = wall_bp.children
        candidates = [item for item in wall if item.get("IS_BP_ASSEMBLY")]
        n_openings = [[item for item in obj.children if 'opening' in
                       item.name.lower()] for obj in candidates]
        for openings in n_openings:
            for opening in openings:
                depth = abs(opening.location[1])
                hashmark = sn_types.Line(sn_unit.inch(6), (0, 45, 0))
                hashmark.parent(opening)
                dim = self.add_tagged_dimension(hashmark.end_point)
                dim.start_z(value=sn_unit.inch(2))
                dim.set_label(self.to_inch_lbl(depth))

    def get_door_size(self, door_height_metric):
        label = ""
        door_height = self.to_inch_str(door_height_metric)
        if door_height in common_lists.DOOR_SIZES_DICT.keys():
            label = common_lists.DOOR_SIZES_DICT[door_height]
        else:
            qry_result = False
            tolerance = 0.25 
            for key, value in common_lists.DOOR_SIZES_DICT.items():
                if abs(float(key) - float(door_height)) <= tolerance:
                    qry_result = True
                    label = value
            if not qry_result:
                label = str(opengl_dim.format_distance(float(door_height)))
        return label

    def get_drawer_size_by_dim(self, drawer_height):
        drawer_h_query = str(round(drawer_height * 1000, 3))
        drawer_h_number = common_lists.DRAWER_SIZES_DICT[drawer_h_query]
        return drawer_h_number

    def place_drawer_front_labels(self, drawer_assy, dims_list):
        dims_list.reverse()
        width = drawer_assy.obj_x.location.x
        parent = drawer_assy.obj_bp
        start_loc = 0
        for drw_face_dim in dims_list:
            vert_loc = 0
            idx, face_height, label = drw_face_dim
            curr_idx = len(dims_list) - idx
            z_offset = curr_idx * sn_unit.inch(0.1)
            if face_height <= 0.3:
                vert_loc = start_loc + (face_height / 2) + z_offset
            elif face_height > 0.3:
                vert_loc = start_loc + ((face_height / 4) * 3) + z_offset
            dim = self.add_tagged_dimension(parent)
            dim.start_x(value=(width / 4) * 3)
            dim.start_z(value=vert_loc)
            dim.set_label(label)
            start_loc += face_height

    def has_obj_mesh(self, assembly):
        children = assembly.obj_bp.children
        obj_users = 0
        for child in children:
            is_mesh = "mesh" in child.name.lower()
            if "obj" in child.name.lower():
                obj_users = child.users
            elif is_mesh and child.users >= obj_users:
                return True
        return False

    def opening_panels(self, section):
        """
        Returns a dictionary of openings and their adjacent panels,
        sorted left to right.
        """
        opns_sides = {}
        panels = [c for c in section.children if c.sn_closets.is_panel_bp and
                  not c.sn_closets.is_blind_corner_panel_bp]
        opns = [c for c in section.children if c.snap.type_group == 'OPENING']

        opns.sort(key=lambda x: x.location.x)
        panels.sort(key=lambda x: x.location.x)

        for i, opn in enumerate(opns):
            l_panel = panels[i]
            if i + 1 != len(opns):
                r_panel = panels[i + 1]
            else:
                r_panel = panels[-1]
            opns_sides[opn] = [l_panel, r_panel]

        return opns_sides

    def extra_drilling_labeling(self, section):
        opns_sides = self.opening_panels(section)

        for opening, sides in opns_sides.items():
            opn_assy = sn_types.Assembly(opening)
            opn_w = opn_assy.obj_x.location.x
            opn_h = opn_assy.obj_z.location.z

            panel_l, panel_r = sides
            holes_l = False
            holes_r = False

            for side in sides:
                panel_part = sn_types.Part(side)
                [cutpart] = panel_part.get_cutparts()
                mach_tks = cutpart.snap.mp.machine_tokens

                if side == panel_l:
                    holes_l = any(['Mid Right' in m.name for m in mach_tks])
                if side == panel_r:
                    holes_r = any(['Mid Left' in m.name for m in mach_tks])

            if holes_l and holes_r:
                lbl = self.add_tagged_dimension(opening)
                lbl.start_x(value=opn_w/2)
                lbl.start_z(value=opn_h/2)
                lbl.anchor.rotation_euler.y = -math.radians(45)
                lbl.set_label('3 Lines of Holes')

    def add_dog_ear_label(self, closet):
        closet_assembly = sn_types.Assembly(obj_bp=closet)
        active_prompt = closet_assembly.get_prompt("Dog Ear Active")
        if not active_prompt:
            return
        if not active_prompt.get_value():
            return
        partition_list = self.get_partition_list(closet)
        dog_ear_depth =\
            closet_assembly.get_prompt(
                "Front Angle Depth").get_value()
        for _, _, panel, _ in partition_list:
            if round(abs(panel.dimensions[1]), 2) <= round(dog_ear_depth, 2):
                continue
            x_loc = panel.dimensions[0] + 0.1
            dim = self.add_tagged_dimension(panel)
            dim.start_x(value=x_loc)
            dim.start_y(value=0)
            dim.start_z(value=0)
            dim.anchor.name = 'PARTHGT'
            dim.end_point.name = 'PARTHGT'
            dim.set_label("DE")
            hashmark = sn_types.Line(0.065, (0, 90, 0))
            hashmark.parent(panel)
            hashmark.start_x(value=abs(panel.dimensions[0]))
            hashmark.start_y(value=0)
            hashmark.start_z(value=0)
            hashmark.anchor.name = 'PARTHGT'
            hashmark.end_point.name = 'PARTHGT'
    
    def door_has_pointers(self, door_parent):
        door_parent_pointers = []
        for door_obj in door_parent.children:
            if door_obj.sn_closets.is_door_bp:
                door_mesh = [d for d in door_obj.children if d.type == 'MESH'][0]
                pointers = [s.pointer_name for s in door_mesh.snap.material_slots]
                pointers = [p for p in pointers if p != '']
                door_parent_pointers += pointers
        pointers_qty = len(list(set(door_parent_pointers)))
        if pointers_qty > 0:
            return True
        return False

    def execute(self, context):
        self.clean_up_scene(context)
        scene_props = get_dimension_props()
        self.font = opengl_dim.get_custom_font()
        self.font_bold = opengl_dim.get_custom_font_bold()

        # Set Closet Product Annotations
        for wall_bp in scene_walls(context):
            bheight_offset = 0
            if scene_props.framing_height:
                bheight_offset = self.build_height_dimension(wall_bp)
            if scene_props.section_depths:
                self.section_depths(wall_bp)
            if scene_props.section_widths:
                self.section_widths(context, wall_bp)
            if scene_props.partition_height:
                self.partition_height(wall_bp)
            if scene_props.filler:
                self.upper_lower_filler_labeling(wall_bp)
            for child in wall_bp.children:
                if child.snap.is_wall_mesh and scene_props.ceiling_height:
                    self.ceiling_height_dimension(child, bheight_offset)

                if child.get("IS_BP_ASSEMBLY"):
                    # Shelves Options
                    if scene_props.shelf_setback:
                        self.stack_shelves_setback(child)
                        self.hangers_setback(child)
                        # self.setback_standard_shelf(child)
                        # self.arrayed_shelves_section_depth_dimension(context,
                                                                    #  child)

                    # General Options
                    if scene_props.variable:
                        self.variable_opening_label(child)
                    if (scene_props.third_line_holes and
                       'section' in child.name.lower()):
                        self.extra_drilling_labeling(child)

                    # Dog Ear
                    if scene_props.dog_ear:
                        self.add_dog_ear_label(child)

            self.wall_width_dimension(wall_bp)

        # Add Part Annotations
        for assembly in scene_assemblies(context):

            props = assembly.obj_bp.sn_closets

            # SHELF LABEL
            if props.is_shelf_bp:
                is_locked_shelf = assembly.get_prompt("Is Locked Shelf")
                has_obj_mesh = self.has_obj_mesh(assembly)

                if is_locked_shelf and is_locked_shelf.get_value() and scene_props.kds and has_obj_mesh:  # noqa E501
                    shelf_label = self.add_tagged_dimension(assembly.obj_bp)
                    shelf_label.start_x(value=assembly.obj_x.location.x / 2)
                    shelf_label.start_y(value=0)
                    shelf_label.start_z(
                        value=-math.fabs(assembly.obj_z.location.z / 2))
                    shelf_label.set_label("KD")

            # DOOR HEIGHT LABEL
            if props.is_door_bp and scene_props.door_face_height:
                door_obj = assembly.obj_bp
                has_pointers = self.door_has_pointers(door_obj.parent)
                door_assy = sn_types.Assembly(door_obj)
                door_height = door_assy.obj_x.location.x
                if not has_pointers:
                    y_offset = (assembly.obj_y.location.y / 5) * 4
                    if 'left' in door_obj.name.lower():
                        y_offset = (assembly.obj_y.location.y / 5) * 4
                    elif 'right' in door_obj.name.lower():
                        y_offset = (assembly.obj_y.location.y / 5) * 1
                    label = self.get_door_size(door_height)
                    dim = self.add_tagged_dimension(door_obj)
                    dim.start_x(
                        value=(assembly.obj_x.location.x / 5) * 4)
                    dim.start_y(value=y_offset)
                    dim.set_label(label)
                elif has_pointers:
                    label = self.get_door_size(door_height)
                    dim = self.add_tagged_dimension(door_obj)
                    dim.start_x(
                        value=(assembly.obj_x.location.x / 5) * 4)
                    dim.start_y(value=assembly.obj_y.location.y / 2)
                    dim.set_label(label)

            # DRAWER FRONT HEIGHT LABEL
            parent = assembly.obj_bp.parent
            in_island = False
            if parent:
                in_island = assembly.obj_bp.parent.sn_closets.is_island

            label_faces = (props.is_drawer_stack_bp and
                           scene_props.label_drawer_front_height and not
                           in_island)

            label_file_drawers = (props.is_drawer_stack_bp and
                                  scene_props.file_drawers and not
                                  in_island)

            if label_faces:  # noqa E501
                drw_front_pmpt = None
                drw_assy = sn_types.Assembly(assembly.obj_bp)
                drawer_qty = drw_assy.get_prompt("Drawer Quantity").get_value()
                drw_front_list = []
                for child in assembly.obj_bp.children:
                    if "OBJ_PROMPTS_Drawer_Fronts" in child.name:
                        drw_front_pmpt = child
                if drw_front_pmpt is not None:
                    for i in range(1, drawer_qty):
                        drw_str = "Drawer " + str(i) + " Height"
                        pmpt_query = drw_front_pmpt.snap.get_prompt(drw_str)
                        drw_face_height = pmpt_query.get_value()
                        h_number = self.get_drawer_size_by_dim(drw_face_height)
                        drw_front_list.append((i, drw_face_height, h_number))
                self.place_drawer_front_labels(drw_assy, drw_front_list)

            # File Drawer Label
            if label_file_drawers:
                self.file_drawer_labeling(assembly)

            # HAMPER TYPE LABEL
            if props.is_hamper_insert_bp and scene_props.label_hamper_type:
                hamper_insert = sn_types.Assembly(assembly.obj_bp)
                hamper_type = hamper_insert.get_prompt("Hamper Type")
                hamper_height = hamper_insert.get_prompt("Hamper Height")

                if hamper_type and hamper_height:
                    """
                    TODO: Implement complete hamper type labeling when
                    prompts are fully updated
                    type_index = hamper_type.get_value()
                    type_name = hamper_type.combobox_items[type_index].name
                    dim_slide.set_label(f'Hamper|{type_name}')
                    """
                    dim_slide = self.add_tagged_dimension(assembly.obj_bp)
                    dim_slide.start_x(value=hamper_insert.obj_x.location.x / 2)
                    dim_slide.start_z(value=hamper_height.get_value() / 2)
                    dim_slide.set_label('Hamper')

                    dim_hole_number = self.add_tagged_dimension(
                        assembly.obj_bp)
                    dim_hole_number.start_x(
                        value=(hamper_insert.obj_x.location.x / 4) * 3)
                    dim_hole_number.start_z(
                        value=(hamper_height.get_value() / 4) * 3)
                    dim_hole_number.start_y(value=sn_unit.inch(100))
                    dim_hole_number.set_label(
                        common_lists.HAMPER_SIZES_DICT[str(round(hamper_height.get_value() * 1000, 3))])

            # Locks Labels
            if scene_props.locks and 'lock' in assembly.obj_bp.name.lower():
                self.lock_labeling(assembly)

            # Jewelry Drawer Labels
            if scene_props.double_jewelry and props.is_drawer_stack_bp:
                self.jewelry_drawer_labeling(assembly)

            # Countertop Insert Overhang Labels
            if scene_props.ct_overhang and props.is_counter_top_insert_bp:
                self.ct_overhang_label(assembly)

            # Blind Corner Panel Labels
            if scene_props.bc_panels and props.is_blind_corner_panel_bp:
                self.blind_corner_panel_labels(assembly)

            # Toe Kick Height Dimension
            if scene_props.toe_kick_height and props.is_toe_kick_insert_bp:
                self.toe_kick_garage_leg_dimension(assembly)

            is_garage_leg = 'garage leg' in assembly.obj_bp.name.lower()
            if scene_props.garage_legs and is_garage_leg:
                self.toe_kick_garage_leg_dimension(assembly)

            # Toe Kick Labels
            if props.is_toe_kick_bp:
                tk_type = self.is_labeled_toe_kick(assembly)
                if scene_props.toe_kicks and tk_type:
                    self.toe_kick_label(assembly, tk_type)

            # Fullback labels
            is_backing = (props.is_back_bp or
                          props.is_top_back_bp or
                          props.is_bottom_back_bp)

            if scene_props.fullback and is_backing:
                self.fullback_labeling(assembly)

            # Labels for assemblies in islands
            if props.is_island:
                if scene_props.ct_overhang:
                    self.ct_overhang_label(assembly)

            # Wall cleats dimensions
            accy_cleat = (props.is_accessory_bp and
                          any(['cleat' in c.name.lower()
                              for c in assembly.obj_bp.children]))
            wall_cleat = 'wall cleat' in assembly.obj_bp.name.lower()

            if scene_props.wall_cleats and (accy_cleat or wall_cleat):
                self.wall_cleat_dimensions(assembly)

            # Topshelf support corbel dimensions
            if assembly.obj_bp.get("IS_TOPSHELF_SUPPORT_CORBELS"):
                self.ts_support_corbel_dimensions(assembly)

            # Top Shelf labeling
            is_top_shelf = 'IS_BP_PLANT_ON_TOP' in assembly.obj_bp
            if scene_props.top_shelf_depth and is_top_shelf:
                self.topshelf_depth(assembly)

            # SSS labeling
            if scene_props.slanted_shoe_shelves and props.is_slanted_shelf_bp:
                self.slanted_shoes_shelves(assembly.obj_bp.parent)

            # Glass Shelves
            if scene_props.glass_shelves and props.is_glass_shelf_bp:
                self.glass_shelves(assembly.obj_bp)

            # Countertop
            if scene_props.countertop and props.is_counter_top_insert_bp:
                self.countertop_hashmark(context, assembly.obj_bp)
                self.countertop_exposed_label(assembly.obj_bp)

            # Filler
            # if scene_props.filler and props.is_filler_bp:
            #     self.filler_labeling(assembly)

            # Flat Crown
            not_none_parent = assembly.obj_bp.parent is not None
            flat_crown = scene_props.flat_crown and props.is_flat_crown_bp
            if flat_crown and not_none_parent:
                self.flat_crown(assembly.obj_bp)

            # Capping Bottom Labeling
            if scene_props.capping_bottom and props.is_closet_bottom_bp:
                self.capping_bottom_label(assembly)

            # Valances Labeling
            is_valance = ('valance' in assembly.obj_bp.name.lower() and
                          'flat' not in assembly.obj_bp.name.lower())
            if scene_props.valances and is_valance:
                self.valances_labeling(assembly)

            # Light Rails Labeling
            is_light_rail = 'light rail' in assembly.obj_bp.name.lower()
            if scene_props.light_rails and is_light_rail:
                self.light_rails_labeling(assembly)

            # Partition Height
            # if scene_props.partition_height and props.is_panel_bp:
            #     self.partition_height(assembly.obj_bp)

            # Corner Shelves and L-shelves
            is_lsh = 'l shelves' in assembly.obj_bp.name.lower()
            is_csh = 'corner shelves' in assembly.obj_bp.name.lower()
            if scene_props.corner_shelves_l_shelves and (is_lsh or is_csh):
                self.corner_shelves_l_shelves(assembly.obj_bp)

        if scene_props.walk_space:
            bpy.ops.sn_2d_views.draw_walk_space("INVOKE_DEFAULT")

        hide_dim_handles()
        clear_labels_lists()
        bpy.ops.sn_closets.update_drawer_boxes(add=False)

        return {'FINISHED'}


class SNAP_PROPS_2D_Dimensions(PropertyGroup):

    main_tabs: EnumProperty(name="Main Tabs",
                            items=[('GENERAL', "Defaults", 'Show the general defaults.'),
                                   ('MOLDING', "Molding",
                                    'Show the molding options.'),
                                   ('DOORS', "Doors and Drawers",
                                    'Show the wood panel style options.'),
                                   ('SHELVES', "Shelves", 'Show the hardware options.')],
                            default='GENERAL')

    auto_add_on_save: BoolProperty(name="Auto Add On Save",
                                   default=False,
                                   description="Automatically add annotations and dimensions to scene")

    include_accordions: BoolProperty(name="Include Accordions",
                                   default=False,
                                   description="Include Accordion Elevations on 2D Views")

    # General
    ceiling_height: BoolProperty(name="Add Ceiling Height",
                                 default=True,
                                 description="")

    countertop: BoolProperty(name="Add Countertops",
                             default=True,
                             description="")

    ct_overhang: BoolProperty(name="Add CT Overhang",
                               default=True,
                               description="Annotate Countertop Overhang")

    filler: BoolProperty(name="Add Fillers",
                         default=True,
                         description="")

    framing_height: BoolProperty(name="Add Framing Height",
                                 default=True,
                                 description="")

    fullback: BoolProperty(name="Add Fullback",
                           default=True,
                           description="")

    kds: BoolProperty(name="Add KD\'s",
                      default=True,
                      description="")

    partition_height: BoolProperty(name="Add Partition Height",
                                   default=True,
                                   description="")

    partition_depths: BoolProperty(name="Add Partition Depths",
                                   default=True,
                                   description="")

    section_depths: BoolProperty(name="Add Section Depths",
                                 default=True,
                                 description="Add to each opening it\'s section depth")

    section_widths: BoolProperty(name="Add Section Widths",
                                 default=True,
                                 description="This will add an section width dimensions to the elevation")

    toe_kicks: BoolProperty(name="Add Toe Kicks",
                                  default=True,
                                  description="")
    
    garage_legs: BoolProperty(name="Add Garage Legs",
                                  default=True,
                                  description="")

    toe_kick_height: BoolProperty(name="Add Toe Kick Heights",
                                  default=True,
                                  description="")

    top_shelf_depth: BoolProperty(name="Add Top Shelf Depth",
                                  default=True,
                                  description="")

    variable: BoolProperty(name="Add Variable Openings",
                           default=True,
                           description="")

    third_line_holes: BoolProperty(name="Add 3rd Line of Holes",
                                   default=True,
                                   description="")
    wall_cleats: BoolProperty(name="Add Wall Cleats",
                              default=True,
                              description="")

    # Shelves

    glass_shelves: BoolProperty(name="Add Glass Shelves",
                                default=True,
                                description="")

    shelf_setback: BoolProperty(name="Add Shelves Setback",
                                default=True,
                                description="")

    slanted_shoe_shelves: BoolProperty(name="Add Slanted Shoe Shelves",
                                       default=True,
                                       description="")

    corner_shelves_l_shelves: BoolProperty(name="Add Corner Shelves and L-Shelves",
                                           default=True,
                                           description="")

    # Doors and Drawers
    door_face_height: BoolProperty(name="Add Door Face Height",
                                   default=True,
                                   description="This will put the door height at the top right of the door")

    label_drawer_front_height: BoolProperty(name="Add Drawer Face Height",
                                            default=True,
                                            description="This will put the door height at the bottom of the door")

    file_drawers: BoolProperty(name="Add File Drawers",
                               default=True,
                               description="This will label file drawers ")

    label_hamper_type: BoolProperty(name="Add Hamper",
                                    default=True,
                                    description="This will label the type of hamper that is used")

    double_jewelry: BoolProperty(name="Add Double Jewelry Drawers",
                                 default=True,
                                 description="This will label double jewelry drawers ")

    locks: BoolProperty(name="Add Locks",
                        default=True,
                        description="This will label the type of hamper that is used")

    # Molding
    capping_bottom: BoolProperty(name="Add Capping Bottom",
                                 default=True,
                                 description="")

    flat_crown: BoolProperty(name="Add Flat Crown",
                                  default=True,
                                  description="")

    bc_panels: BoolProperty(name="Add Blind Corner Panels",
                                            default=True,
                                            description="")

    light_rails: BoolProperty(name="Add Light Rails",
                              default=True,
                              description="")

    valances: BoolProperty(name="Add Valance",
                           default=True,
                           description="")

    # Dog Ear
    dog_ear: BoolProperty(name="Add Dog Ear",
                          default=True,
                          description="")

    # Walk Space
    walk_space: BoolProperty(name="Add Walk Space W/Island",
                             default=True,
                             description="")

    def draw_general_options(self, layout):
        general_box = layout.box()
        general_box.prop(self, 'bc_panels')
        general_box.prop(self, 'ceiling_height')
        general_box.prop(self, 'countertop')
        general_box.prop(self, 'ct_overhang')
        general_box.prop(self, 'filler')
        general_box.prop(self, 'framing_height')
        general_box.prop(self, 'fullback')
        general_box.prop(self, 'garage_legs')
        general_box.prop(self, 'partition_depths')
        general_box.prop(self, 'partition_height')
        general_box.prop(self, 'section_depths')
        general_box.prop(self, 'section_widths')
        general_box.prop(self, 'toe_kicks')
        general_box.prop(self, 'toe_kick_height')
        general_box.prop(self, 'variable')
        general_box.prop(self, 'dog_ear')
        general_box.prop(self, 'wall_cleats')
        general_box.prop(self, 'walk_space')
        general_box.prop(self, 'third_line_holes')

    def draw_molding_options(self, layout):
        molding_box = layout.box()
        molding_box.prop(self, 'flat_crown')
        molding_box.prop(self, 'light_rails')
        molding_box.prop(self, 'valances')

    def draw_doors_n_drawers_options(self, layout):
        doors_box = layout.box()
        doors_box.prop(self, 'door_face_height')
        doors_box.prop(self, 'double_jewelry')
        doors_box.prop(self, 'label_drawer_front_height')
        doors_box.prop(self, 'file_drawers')
        doors_box.prop(self, 'label_hamper_type')
        doors_box.prop(self, 'locks')

    def draw_shelves_options(self, layout):
        shelves_box = layout.box()
        shelves_box.prop(self, 'capping_bottom')
        shelves_box.prop(self, 'glass_shelves')
        shelves_box.prop(self, 'corner_shelves_l_shelves')
        shelves_box.prop(self, 'kds')
        shelves_box.prop(self, 'shelf_setback')
        shelves_box.prop(self, 'slanted_shoe_shelves')
        shelves_box.prop(self, 'top_shelf_depth')

    def draw(self, layout):
        main_box = layout.box()

        box = layout.box()
        row = main_box.row(align=True)
        row.scale_y = 1.3
        row.operator("snap_closet_dimensions.auto_dimension", icon='FILE_TICK')
        row.menu('SNAP_MT_label_option',
                 text="", icon='DOWNARROW_HLT')
        row = main_box.row(align=True)
        row.prop(self, 'auto_add_on_save', text="Auto Add on Save")

        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "main_tabs", 'GENERAL',
                      icon='PREFERENCES', text="General Dimensions")
        row.prop_enum(self, "main_tabs", 'MOLDING',
                      icon='MOD_PARTICLES', text="Molding")
        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "main_tabs", 'DOORS',
                      icon='UV_ISLANDSEL', text="Doors and Drawers")
        row.prop_enum(self, "main_tabs", 'SHELVES',
                      icon='MOD_ARRAY', text="Shelves")

        if self.main_tabs == 'GENERAL':
            self.draw_general_options(box)
        if self.main_tabs == 'MOLDING':
            self.draw_molding_options(box)
        if self.main_tabs == 'DOORS':
            self.draw_doors_n_drawers_options(box)
        if self.main_tabs == 'SHELVES':
            self.draw_shelves_options(box)

    @classmethod
    def register(cls):
        bpy.types.Scene.snap_closet_dimensions = PointerProperty(type=SNAP_PROPS_2D_Dimensions)

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.snap_closet_dimensions


class SNAP_PROPS_Object_2D_Dimensions(PropertyGroup):

    is_dim_obj: BoolProperty(name="Is Dimension Object",
                             default=False,
                             description="This determines if the object is a dimension object")

    @classmethod
    def register(cls):
        bpy.types.Object.snap_closet_dimensions = PointerProperty(type=SNAP_PROPS_Object_2D_Dimensions)

    @classmethod
    def unregister(cls):
        del bpy.types.Object.snap_closet_dimensions


class SNAP_PT_Closet_2D_Setup(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "2D Setup"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 5

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='', icon='OPTIONS')

    def draw(self, context):
        props = get_dimension_props()
        props.draw(self.layout)


classes = (
    SNAP_PROPS_2D_Dimensions,
    SNAP_PROPS_Object_2D_Dimensions,
    SNAP_PT_Closet_2D_Setup,
    SNAP_OT_Auto_Dimension,
    SNAP_OT_Cleanup,
    SNAP_OT_Select_All,
    SNAP_OT_Deselect_All,
    SNAP_MT_label_option
)


def register():
    for cls in classes:
        register_class(cls)

    # AUTO CALL OPERATOR ON SAVE
    @persistent
    def add_annotations_and_dimensions(scene=None):
        props = get_dimension_props()
        if props.auto_add_on_save:
            bpy.ops.snap_closet_dimensions.auto_dimension()

    bpy.app.handlers.save_pre.append(add_annotations_and_dimensions)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)