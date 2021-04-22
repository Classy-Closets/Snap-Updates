"""
Microvellum
Cabinet & Closet Designer
Stores the UI, Properties, and Operators for the cabinet and closet designer panel
the Panel definition is stored in an add-on.
"""

import bpy
import math
import mathutils
from snap_db.fd_2dviews import opengl_dim
from mv import fd_types, unit, utils
from bpy.app.handlers import persistent
from . import mv_closet_defaults as props_closet
from . import common_closet_utils
from . import common_lists
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

DIMENSION_PROPERTY_NAMESPACE = "mv_closet_dimensions"


def get_dimension_props():
    """
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("bpy.context.scene." + DIMENSION_PROPERTY_NAMESPACE)
    return props


def get_object_dimension_props(obj):
    """
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("obj." + DIMENSION_PROPERTY_NAMESPACE)
    return props


def scene_assemblies(context):
    for obj in bpy.context.scene.objects:
        if obj.mv.type == 'BPASSEMBLY':
            assembly = fd_types.Assembly(obj)
            if common_closet_utils.part_is_not_hidden(assembly):
                yield assembly


def scene_label_props(scenes, option):
    for scene in scenes:
        scene.mv_closet_dimensions.ceiling_height = option
        scene.mv_closet_dimensions.countertop = option
        scene.mv_closet_dimensions.ct_overhang = option
        scene.mv_closet_dimensions.filler = option
        scene.mv_closet_dimensions.framing_height = option
        scene.mv_closet_dimensions.fullback = option
        scene.mv_closet_dimensions.kds = option
        scene.mv_closet_dimensions.partition_depths = option
        scene.mv_closet_dimensions.partition_height = option
        scene.mv_closet_dimensions.section_depths = option
        scene.mv_closet_dimensions.section_widths = option
        scene.mv_closet_dimensions.toe_kick_height = option
        scene.mv_closet_dimensions.top_shelf_depth = option
        scene.mv_closet_dimensions.variable = option
        scene.mv_closet_dimensions.capping_bottom = option
        scene.mv_closet_dimensions.flat_crown = option
        scene.mv_closet_dimensions.blind_corner_panel_labels = option
        scene.mv_closet_dimensions.light_rails = option
        scene.mv_closet_dimensions.valances = option
        scene.mv_closet_dimensions.door_face_height = option
        scene.mv_closet_dimensions.label_drawer_front_height = option
        scene.mv_closet_dimensions.file_drawers = option
        scene.mv_closet_dimensions.label_hamper_type = option
        scene.mv_closet_dimensions.glass_shelves = option
        scene.mv_closet_dimensions.l_shelves = option
        scene.mv_closet_dimensions.corner_shelves = option
        scene.mv_closet_dimensions.shelf_setback = option
        scene.mv_closet_dimensions.slanted_shoe_shelves = option
        scene.mv_closet_dimensions.double_jewelry = option
        scene.mv_closet_dimensions.locks = option


class OPERATOR_Select_All(bpy.types.Operator):
    bl_idname = DIMENSION_PROPERTY_NAMESPACE + ".select_all"
    bl_label = "Select All Dimension Options"
    bl_description = "This will select all existing labeling options"
    bl_options = {'UNDO'}

    def execute(self, context):
        scene_label_props(bpy.data.scenes, True)
        return {'FINISHED'}


class OPERATOR_Deselect_All(bpy.types.Operator):
    bl_idname = DIMENSION_PROPERTY_NAMESPACE + ".deselect_all"
    bl_label = "Select All Dimension Options"
    bl_description = "This will select all existing labeling options"
    bl_options = {'UNDO'}

    def execute(self, context):
        scene_label_props(bpy.data.scenes, False)
        return {'FINISHED'}


class OPERATOR_Cleanup(bpy.types.Operator):
    bl_idname = DIMENSION_PROPERTY_NAMESPACE + ".remove_labels"
    bl_label = "Remove Labels"
    bl_description = "This will remove any existing label"
    bl_options = {'UNDO'}

    def clean_up_scene(self, context):
        label_list = []

        for obj in context.scene.objects:
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
        utils.delete_obj_list(label_list)
        # bpy.ops.outliner.purge()

    def execute(self, context):
        self.clean_up_scene(context)
        return {'FINISHED'}


class MENU_label_option(bpy.types.Menu):
    bl_label = "Label Options"

    def draw(self, context):
        layout = self.layout
        layout.operator(DIMENSION_PROPERTY_NAMESPACE + ".select_all",
                        text="Select All", icon='CHECKBOX_HLT')
        layout.operator(DIMENSION_PROPERTY_NAMESPACE + ".deselect_all",
                        text="Deselect All", icon='CHECKBOX_DEHLT')
        layout.separator()
        layout.operator(DIMENSION_PROPERTY_NAMESPACE + ".remove_labels",
                        icon='X')


class OPERATOR_Auto_Dimension(bpy.types.Operator):
    bl_idname = DIMENSION_PROPERTY_NAMESPACE + ".auto_dimension"
    bl_label = "Label Parts"
    bl_description = "This will assign names to all parts"
    bl_options = {'UNDO'}

    def add_dimension(self, parent):
        dim = fd_types.Dimension()
        anchor_props = get_object_dimension_props(dim.anchor)
        end_point_props = get_object_dimension_props(dim.end_point)
        anchor_props.is_dim_obj = True
        end_point_props.is_dim_obj = True
        dim.anchor.parent = parent
        return dim

    def add_tagged_dimension(self, parent):
        dim = self.add_dimension(parent)
        dim.anchor.mv.comment = "render"
        dim.end_point.mv.comment = "render"
        return dim

    def clean_up_scene(self, context):
        label_list = []

        for obj in context.scene.objects:
            props = get_object_dimension_props(obj)
            if props.is_dim_obj:
                label_list.append(obj)

        utils.delete_obj_list(label_list)

    def add_panel_height_annotation(self, assembly):
        dim_from_floor = assembly.obj_bp.matrix_world[2][3]

        dim = self.add_tagged_dimension(assembly.obj_bp)
        dim.start_x(value=- dim_from_floor - unit.inch(8))
        dim.start_y(value=0)
        dim.start_z(value=assembly.obj_z.location.z/2)
        dim.set_label(
            str(opengl_dim.format_distance(assembly.obj_x.location.x)))

    def set_section_number(self, assembly):
        """
            Set Section Number for Assembly
            This collects the products on a wall and loops through the
            products increasing the count of the number of openings found.
            Then assigns the number to comment 2 of the part

            This can only be set for parts that have a integer assigned for the mv.opening_name property
        """
        wall_bp = utils.get_wall_bp(assembly.obj_bp)
        product_bp = utils.get_bp(assembly.obj_bp, 'PRODUCT')
        if wall_bp:
            products = self.get_wall_products(wall_bp)
            adjusted_opening_number = 0
            for product in products:
                if product == product_bp:
                    assembly.obj_bp.mv.comment_2 = str(
                        int(assembly.obj_bp.mv.opening_name) + adjusted_opening_number)
                    break
                else:
                    adjusted_opening_number += int(product.mv.opening_name)

    def get_wall_products(self, wall_bp):
        """
            Get Sorted List of Products on a Wall
        """
        products = []
        for child in wall_bp.children:
            props = props_closet.get_object_props(child)
            if props.is_closet or props.is_fixed_shelf_and_rod_product_bp:
                child.mv.comment = wall_bp.mv.name_object
                products.append(child)
        products.sort(key=lambda obj: obj.location.x, reverse=False)
        return products

    def get_product_panels(self, product_bp, panel_list):
        """
            Get Sorted List of Panels in a product
        """
        for child in product_bp.children:
            props = props_closet.get_object_props(child)
            if props.is_panel_bp:
                assembly = fd_types.Assembly(child)
                if common_closet_utils.part_is_not_hidden(assembly):
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

        if left_fin_end.value():
            left_fe = self.add_dimension(product.obj_bp)
            left_fe.start_x(value=unit.inch(-2))
            left_fe.set_label("Triangle")

        if right_fin_end.value():
            right_fe = self.add_dimension(product.obj_bp)
            right_fe.start_x(value=product.obj_x.location.x + unit.inch(2))
            right_fe.set_label("Triangle")

        # CLOSET LEFT GAP DIM
        left_x = product.get_collision_location('LEFT')
        dist_l = math.fabs(product.obj_bp.location.x - left_x)
        if dist_l > 0:
            left_dim = self.add_dimension(product.obj_bp)
            left_dim.start_x(value=0)
            left_dim.end_x(value=-dist_l)
            left_dim.start_z(value=- dim_from_floor - unit.inch(4))

        # CLOSET RIGHT GAP DIM
        right_x = product.get_collision_location('RIGHT')
        dist_r = math.fabs(product.obj_bp.location.x +
                           product.obj_x.location.x - right_x)
        if dist_r > 0:
            right_dim = self.add_dimension(product.obj_bp)
            right_dim.start_x(value=product.obj_x.location.x)
            right_dim.end_x(value=dist_r)
            right_dim.start_z(value=- dim_from_floor - unit.inch(4))

        # WIDTH
        width = self.add_dimension(product.obj_bp)
        width.start_x(value=0)
        width.end_x(value=product.obj_x.location.x)
        width.start_z(value=- dim_from_floor - unit.inch(4))

        if scene_props.framing_height:
            height = self.add_tagged_dimension(product.obj_bp)
            height.start_x(value=unit.inch(-6))
            height.end_z(value=-product.obj_bp.location.z)

            height = self.add_tagged_dimension(product.obj_bp)
            height.start_x(value=unit.inch(-6))
            height.end_z(value=-product.obj_bp.location.z)

    def add_closet_annotations(self, closets):
        scene_props = get_dimension_props()

        section_number_text = 1
        hanging_heights = []
        for closet_bp in closets:
            wall_bp = utils.get_wall_bp(closet_bp)
            wall = fd_types.Assembly(wall_bp)
            closet = fd_types.Assembly(closet_bp)
            dim_from_floor = closet.obj_bp.matrix_world[2][3]

            # CLOSET LEFT GAP DIM
            left_x = closet.get_collision_location('LEFT')
            dist_l = math.fabs(closet.obj_bp.location.x - left_x)
            if dist_l > 0:
                left_dim = self.add_dimension(closet.obj_bp)
                left_dim.start_x(value=0)
                left_dim.end_x(value=-dist_l)
                left_dim.start_z(value=- dim_from_floor - unit.inch(4))

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
                    right_dim.start_z(value=- dim_from_floor - unit.inch(4))

            # LEFT FILLER
            left_wall_filler = closet.get_prompt("Left Side Wall Filler")
            if left_wall_filler and left_wall_filler.value() > 0:
                left_f_dim = self.add_dimension(closet.obj_bp)
                left_f_dim.start_x(value=0)
                left_f_dim.end_x(value=left_wall_filler.value())
                left_f_dim.start_z(value=- unit.inch(4))

            # RIGHT FILLER
            right_wall_filler = closet.get_prompt("Right Side Wall Filler")
            if right_wall_filler and right_wall_filler.value() > 0:
                right_f_dim = self.add_dimension(closet.obj_bp)
                right_f_dim.start_x(value=closet.obj_x.location.x)
                right_f_dim.end_x(value=-right_wall_filler.value())
                right_f_dim.start_z(value=- unit.inch(4))

            left_side_thickness = closet.get_prompt("Left Side Thickness")
            cleat_thickness = closet.get_prompt("Cleat Thickness")
            if left_wall_filler and left_side_thickness:
                x_loc = left_side_thickness.value() + left_wall_filler.value()  # CLOSET OPENINGS
            elif cleat_thickness:
                x_loc = cleat_thickness.value()  # FIXED SHELF AND ROD
            else:
                x_loc = 0

            for i in range(1, 10):
                opening_height = closet.get_prompt(
                    "Opening " + str(i) + " Height")
                opening_width = closet.get_prompt(
                    "Opening " + str(i) + " Width")
                panel_thickness = closet.get_prompt("Panel Thickness")
                if opening_height and opening_width and panel_thickness:

                    # if scene_props.add_section_widths:
                    #     section_width = self.add_dimension(closet.obj_bp)
                    #     section_width.start_x(value=x_loc)
                    #     section_width.end_x(value=opening_width.value())
                    #     section_width.start_z(value=- unit.inch(4))

                    # if scene_props.add_section_numbers:
                    #     print("ADDING SECTION NUMBER FOR OPENING",closet_bp)
                    #     section_number = self.add_dimension(closet.obj_bp)
                    #     section_number.start_x(value = x_loc + (opening_width.value()/2))
                    #     section_number.start_z(value = - unit.inch(12))
                    #     section_number.set_label(str(section_number_text))

                    if scene_props.framing_height:
                        if closet.obj_z.location.z not in hanging_heights:
                            hanging_height = self.add_dimension(
                                closet.obj_bp.parent)
                            hanging_height.start_x(
                                value=unit.inch(-6) * (len(hanging_heights) + 1))
                            hanging_height.start_z(value=0)
                            hanging_height.end_z(value=closet.obj_z.location.z)
                            hanging_heights.append(closet.obj_z.location.z)

                    section_number_text += 1
                    x_loc += opening_width.value() + panel_thickness.value()

            props = props_closet.get_object_props(closet.obj_bp)
            if props.is_fixed_shelf_and_rod_product_bp:

                dim_from_floor = closet.obj_bp.matrix_world[2][3]

                left_fin_end = closet.get_prompt("Left Fin End")
                right_fin_end = closet.get_prompt("Right Fin End")
                panel_thickness = closet.get_prompt("Panel Thickness")

                if left_fin_end and left_fin_end.value():
                    left_fe = self.add_dimension(closet.obj_bp)
                    left_fe.start_x(value=unit.inch(-2))
                    left_fe.set_label("Triangle")

                if right_fin_end and right_fin_end.value():
                    right_fe = self.add_dimension(closet.obj_bp)
                    right_fe.start_x(
                        value=closet.obj_x.location.x + unit.inch(2))
                    right_fe.set_label("Triangle")

                # if scene_props.add_section_widths:
                #     width = self.add_dimension(closet.obj_bp)
                #     width.start_x(value=panel_thickness.value())
                #     width.end_x(value=closet.obj_x.location.x -
                #                 panel_thickness.value()*2)
                #     width.start_z(value=- dim_from_floor - unit.inch(4))

                # if scene_props.add_section_numbers:
                #     section_number = self.add_dimension(closet.obj_bp)
                #     section_number.start_x(value = x_loc + (closet.obj_x.location.x/2))
                #     section_number.start_z(value = - dim_from_floor - unit.inch(12))
                #     section_number.set_label(str(section_number_text))

                if scene_props.framing_height:
                    height = self.add_tagged_dimension(closet.obj_bp)
                    height.start_x(value=unit.inch(-6))
                    height.end_z(value=-closet.obj_bp.location.z)

                    height = self.add_tagged_dimension(closet.obj_bp)
                    height.start_x(value=unit.inch(-6))
                    height.end_z(value=-closet.obj_bp.location.z)

                section_number_text += 1

    def get_object_global_location(self, obj):
        return obj.matrix_world * obj.data.vertices[0].co

    def to_inch(self, measure):
        return round(measure / unit.inch(1), 2)

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
                location = (width/2,
                            0,
                            unit.inch(2.12) + z_offset)
                hashmark = self.draw_hashmark(context,
                                              cutpart,
                                              location=location,
                                              rotation=rotation,
                                              length=unit.inch(6))
                dim = self.add_tagged_dimension(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(5))
                dim.set_label(label)

    def arrayed_shelves_door_inserts(self, context, item):
        if 'INSERT' in item.name and 'doors' in item.name.lower():
            for k_item in item.children:
                if k_item.lm_closets.is_shelf_bp:
                    for x_item in k_item.children:
                        part_name = x_item.name.lower()
                        if 'cutpart' in part_name and not x_item.hide:
                            self.arrayed_shelf_dimension(
                                context, x_item, k_item)

    def arrayed_hangs_inserts(self, context, item):
        if 'INSERT' in item.name and 'hang' in item.name.lower():
            for k_item in item.children:
                if k_item.lm_closets.is_shelf_bp:
                    for x_item in k_item.children:
                        part_name = x_item.name.lower()
                        if 'cutpart' in part_name and not x_item.hide:
                            self.arrayed_shelf_dimension(
                                context, x_item, k_item)

    def arrayed_hamper_doors_inserts(self, context, item):
        if 'INSERT' in item.name and 'hamper' in item.name.lower():
            for k_item in item.children:
                if 'INSERT' in k_item.name and 'doors' in k_item.name.lower():
                    for x_item in k_item.children:
                        if x_item.lm_closets.is_shelf_bp:
                            for y_item in x_item.children:
                                part_name = y_item.name.lower()
                                if 'cutpart' in part_name and not y_item.hide:
                                    self.arrayed_shelf_dimension(
                                        context, y_item, x_item)

    def arrayed_shelves_section_depth_dimension(self, context, item):
        # if 'hanging' in item.name.lower():
        for n_item in item.children:
            self.arrayed_shelves_door_inserts(context, n_item)
            self.arrayed_hangs_inserts(context, n_item)
            self.arrayed_hamper_doors_inserts(context, n_item)

    def chk_shelf_cutpart(self, context, cutpart, shelf_bp):
        setback = 0.25
        shelf_depth = self.to_inch(
            shelf_bp.location[1])
        shelf_cutpart = self.to_inch(
            cutpart.dimensions[1])
        depth_part_diff = abs(
            shelf_depth - shelf_cutpart)
        if depth_part_diff != setback and depth_part_diff != 0.0:
            return True
        else:
            return False

    def setback_std_shelf_dim(self, context, cutpart, shelf_bp):
        setback = 0.25
        shelf_depth = self.to_inch(shelf_bp.location[1])
        shelf_cutpart = self.to_inch(cutpart.dimensions[1])
        width = cutpart.dimensions[0]
        depth_part_diff = abs(shelf_depth - shelf_cutpart)
        location = ((width / 2),
                    0,
                    unit.inch(2.12))
        rotation = (0, math.radians(45), 0)
        label = ""
        if depth_part_diff != setback and depth_part_diff != 0.0:
            label = self.to_inch_lbl(cutpart.dimensions[1])
        else:
            label = self.to_inch_lbl(shelf_bp.location[1])
        hashmark = self.draw_hashmark(context,
                                      cutpart,
                                      location=location,
                                      rotation=rotation,
                                      length=unit.inch(6))
        dim = self.add_tagged_dimension(hashmark)
        dim.start_x(value=0)
        dim.start_y(value=0)
        dim.start_z(value=unit.inch(5))
        dim.set_label(label)

    def setback_standard_shelf(self, context, item):
        # We add dimensions for shelves that differs
        # from the section depth + default cutpart (1/4")
        for n_item in item.children:
            item_is_top_bp = n_item.lm_closets.is_closet_top_bp
            item_is_shelf = 'shelf' in n_item.name.lower()
            item_is_insert = 'INSERT' in n_item.name

            if item_is_insert and item_is_shelf and not item_is_top_bp:
                shelves = []
                for k_item in n_item.children:
                    if k_item.lm_closets.is_shelf_bp:
                        for x_item in k_item.children:
                            if 'cutpart' in x_item.name.lower():
                                shelves.append(self.chk_shelf_cutpart(context,
                                                                      x_item,
                                                                      k_item))
                if any(shelves):
                    for k_item in n_item.children:
                        if k_item.lm_closets.is_shelf_bp:
                            for x_item in k_item.children:
                                if 'cutpart' in x_item.name.lower():
                                    self.setback_std_shelf_dim(context,
                                                               x_item,
                                                               k_item)

    def ceiling_height_dimension(self, context, item, bheight_offset):
        dim = self.add_tagged_dimension(item.parent)
        dim.start_x(value=unit.inch(-1) + bheight_offset)
        dim.start_y(value=unit.inch(-1) + bheight_offset)
        dim.start_z(value=0)
        dim.end_z(value=item.dimensions[2])
        wall_height = self.to_inch_lbl(item.dimensions[2])
        dim.set_label(" ")
        bpy.ops.object.text_add()
        text = context.active_object
        text.parent = item
        text.rotation_euler.x = math.radians(0)
        text.rotation_euler.y = math.radians(-90)
        text.rotation_euler.z = math.radians(90)
        text.location.x = unit.inch(-2) + bheight_offset
        text.location.y = 0
        text.location.z = (item.dimensions[2] / 2)
        text.data.align_x = 'CENTER'
        text.data.size = .1
        text.data.body = wall_height
        text.data.font = self.font

    def wall_width_dimension(self, wall_bp):
        assembly = fd_types.Assembly(wall_bp)
        has_entry = any('Entry' in c.mv.class_name for c in wall_bp.children)
        if not has_entry:
            dim = self.add_tagged_dimension(wall_bp)
            label = self.to_inch_lbl(assembly.obj_x.location.x)
            dim.parent(wall_bp)
            dim.start_y(value=assembly.obj_y.location.y)
            dim.start_z(value=assembly.obj_z.location.z + unit.inch(4))
            dim.end_x(value=assembly.obj_x.location.x)
            dim.set_label(label)

    def get_partition_props(self, wall, partition, opening):
        if wall:
            opng_bp_height = self.get_object_global_location(opening)[2]
            wall_height = fd_types.Assembly(wall).obj_z.location.z
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
        tolerance = unit.inch(0.75)
        hanging_opening = opening.parent
        for item in hanging_opening.children:
            is_partition = 'partition' in item.name.lower()
            match_item = item.location[0] == opening.location[0]
            near_match_pos = item.location[0] + tolerance
            near_match_item = round(near_match_pos, 2) == round(
                opening.location[0], 2)
            partition_match = is_partition and match_item
            near_partition_match = is_partition and near_match_item
            if partition_match or near_partition_match:
                for cutpart in item.children:
                    is_cutpart = 'cutpart' in cutpart.name.lower()
                    hidden = cutpart.hide
                    if is_cutpart and not hidden:
                        return cutpart

    def section_width_apply_lbl(self, opening, position):
        if position != "up" and position != "down":
            return
        label_height = 0
        lower_offset = unit.inch(-3)
        upper_offset = unit.inch(15)
        opening_assembly = fd_types.Assembly(opening)
        width = opening_assembly.obj_x.location.x
        width_str = self.to_inch_lbl(width)
        parent_assembly = fd_types.Assembly(opening.parent)
        parent_height = parent_assembly.obj_z.location.z
        label_height = (opening.location[2] / -1) + lower_offset
        if position == "up":
            label_height += (parent_height + upper_offset)
        dim = self.add_tagged_dimension(opening)
        dim.start_x(value=width/2)
        dim.start_y(value=0)
        dim.start_z(value=label_height)
        dim.set_label(width_str)

    def query_openings_data(self, context, wall_bp):
        wall_dict = {}
        for obj in wall_bp.children:
            hanging = 'hanging' in obj.name.lower()
            opening = 'opening' in obj.name.lower()
            opng_dict = {}
            if hanging and opening:
                openings = []
                sorted_openings = []
                for op in obj.children:
                    inner_opng = 'OPENING' in op.name
                    if inner_opng:
                        x_loc = self.to_inch(op.location[0])
                        openings.append((x_loc, op))
                sorted_openings = sorted(openings, key=lambda tup: tup[0])
                obj_assy = fd_types.Assembly(obj)
                if obj_assy.obj_x is None:
                    continue
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
                        is_floor = floor_mounted.value()
                        opng_height = opng_height_pmpt.value()
                        matching_opng = sorted_openings[i-1]
                        opng = matching_opng[1]
                        matching = self.find_matching_partition_cutpart(opng)
                        opng_props = self.get_partition_props(wall_bp,
                                                              matching,
                                                              opng)
                        opng_assy = fd_types.Assembly(opng)
                        opng_width = self.to_inch(opng_assy.obj_x.location.x)
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
        upper_start = (upper_opening[2] * unit.inch(1))
        upper_width = (upper_opening[1] * unit.inch(1))
        upper_end = upper_hang_opng_start + upper_start + upper_width
        for lower in lower_list:
            lower_hang_opng_start = lower[0].parent.location[0]
            lower_start = lower_hang_opng_start + (lower[2] * unit.inch(1))
            lower_width = (lower[1] * unit.inch(1))
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

    def many_hanging_openings(self, opng_data):
        overlapping = self.has_overlapping_hanging_opening(opng_data)
        if not overlapping:
            for key, value in opng_data.items():
                for opening in value["openings"]:
                    self.section_width_apply_lbl(opening[0], "down")
        elif overlapping:
            uppers = []
            lowers = []
            for key, value in opng_data.items():
                for opening in value["openings"]:
                    is_upper = opening[1]["is_upper"]
                    is_lower = opening[1]["is_lower"]
                    width = opening[1]["width"]
                    location = opening[1]["x_loc"]
                    if is_upper:
                        uppers.append((opening[0], width, location))
                    if is_lower:
                        lowers.append((opening[0], width, location))
            if len(uppers) == len(lowers):
                for i, lower in enumerate(lowers):
                    upper_width = uppers[i][1]
                    uppper_location = uppers[i][2]
                    lower_width = lowers[i][1]
                    lower_location = lowers[i][2]
                    same_width = upper_width == lower_width
                    same_location = uppper_location == lower_location
                    if same_width and same_location:
                        self.section_width_apply_lbl(lower[0], "down")
                    elif not same_width or not same_location:
                        self.section_width_apply_lbl(uppers[i][0], "up")
                        self.section_width_apply_lbl(lower[0], "down")
            elif len(uppers) != len(lowers):
                for upper in uppers:
                    overlap_lower = self.has_overlapping_lower(upper,
                                                               lowers)
                    if overlap_lower:
                        self.section_width_apply_lbl(upper[0], "up")
                    elif not overlap_lower:
                        self.section_width_apply_lbl(upper[0], "down")
                for lower in lowers:
                    self.section_width_apply_lbl(lower[0], "down")

    def section_widths(self, context, wall_bp):
        opng_data = self.query_openings_data(context, wall_bp)
        if len(opng_data) == 1:
            self.one_hanging_opening(opng_data)
        elif len(opng_data) > 1:
            self.many_hanging_openings(opng_data)

    def l_shelves(self, context, wall_bp):
        for item in wall_bp.children:
            l_shelf = 'l shelves' in item.name.lower()
            if l_shelf:
                l_shelf_assy = fd_types.Assembly(item)
                # print(item.name, l_shelf_assy)
                # shelves_pmpt = l_shelf_assy.get_prompt("Shelf Quantity")
                # double_doors = l_shelf_assy.get_prompt(
                #     "Force Double Doors").value()
                # shelves_qty = shelves_pmpt.value()
                # has_door = l_shelf_assy.get_prompt("Door").value()
                width = l_shelf_assy.obj_x.location.x
                depth = l_shelf_assy.obj_y.location.y
                height = l_shelf_assy.obj_z.location.z
                # Width
                width_dim = self.add_tagged_dimension(item)
                width_dim.start_x(value=0)
                width_dim.start_y(value=0)
                width_dim.start_z(value=height)
                width_dim.end_x(value=width)
                width_dim.set_label(self.to_inch_lbl(abs(width)))
                # Depth
                depth_dim = self.add_tagged_dimension(item)
                depth_dim.start_x(value=0)
                depth_dim.start_y(value=0)
                depth_dim.start_z(value=height)
                depth_dim.end_y(value=depth)
                depth_dim.set_label(self.to_inch_lbl(abs(depth)))
                # Height
                height_dim = self.add_tagged_dimension(item)
                height_dim.end_z(value=height)
                height_dim.start_x(value=0)
                height_dim.start_y(value=0)
                height_dim.end_y(value=0)
                height_dim.set_label(self.to_inch_lbl(abs(height)))

    def corner_shelves(self, context, wall_bp):
        for item in wall_bp.children:
            corner_shelf = 'corner shelves' in item.name.lower()
            if corner_shelf:
                shelves_qty = 0
                has_door = False
                corner_shelf_assy = fd_types.Assembly(item)
                shelves_pmpt = corner_shelf_assy.get_prompt("Shelf Quantity")
                if shelves_pmpt:
                    shelves_qty = shelves_pmpt.value()
                    has_door = corner_shelf_assy.get_prompt("Door").value()

    def draw_hashmark(self, context, parent,
                      location=(unit.inch(1.06), 0, unit.inch(1.06)),
                      rotation=(0, math.radians(45), 0),
                      length=unit.inch(3)):
        # The following creates a Poly NURBS curve that looks like a dash/line
        # Create a curve and define its rendering settings
        hashmark_n = 'Hashmark'
        line = bpy.data.curves.new(hashmark_n, 'CURVE')
        line.dimensions = '3D'
        line.fill_mode = 'HALF'
        line.bevel_resolution = 0
        line.bevel_depth = unit.inch(0.1)

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
        hashmark_obj.mv.comment = "render"
        context.scene.objects.link(hashmark_obj)
        # self.hashmarks.append(hashmark_obj)
        return hashmark_obj

    def apply_file_drawer_labels(self, label_dict):
        for part, label in label_dict.items():
            part_dims = part.dimensions
            # 1st line -> Type: F2B or LAT
            dim_label = ""
            box_label = None
            f2b_file_drawer = label[0] == "Front to Back"
            lat_file_drawer = label[0] == "Lateral"
            if f2b_file_drawer:
                dim_label = "F2B "
            elif lat_file_drawer:
                dim_label = "Lat. "
            dim_label += label[1]
            if lat_file_drawer and label[1] == "Letter":
                box_label = "14\" D box"
            elif lat_file_drawer and label[1] == "Legal":
                box_label = "17\" D box"
            dim = self.add_tagged_dimension(part)
            dim.start_x(value=(part_dims[0] / 2))
            dim.start_y(value=(part_dims[1] / 2) + unit.inch(0.75))
            dim.start_z(value=0)
            dim.set_label("FILE")
            # 2nd line -> Size: Legal or Letter
            dim = self.add_tagged_dimension(part)
            dim.start_x(value=(part_dims[0] / 2) - unit.inch(2))
            dim.start_y(value=(part_dims[1] / 2) + unit.inch(0.75))
            dim.start_z(value=0)
            dim.set_label(dim_label)
            # 3rd line -> Drawer box size
            if box_label is not None:
                dim = self.add_tagged_dimension(part)
                dim.start_x(value=(part_dims[0] / 2) - unit.inch(4))
                dim.start_y(value=(part_dims[1] / 2) + unit.inch(0.75))
                dim.start_z(value=0)
                dim.set_label(box_label)

    def file_drawer_labeling(self, context, item):
        drawer_data_dict = {}
        candidate_cutparts = {}
        join_dict = {}
        for drawers in item.children:
            if drawers.lm_closets.is_drawer_stack_bp:
                drawer_data_dict[drawers.name] = {}
                candidate_cutparts[drawers.name] = {}
                drwr_ins_dict = drawer_data_dict[drawers.name]
                assembly = fd_types.Assembly(drawers)
                drawer_qty = fd_types.Assembly(
                    drawers).get_prompt("Drawer Quantity").value()
                any_file_rail = False
                for i in range(1, drawer_qty):
                    has_file_rail = assembly.get_prompt(
                        "Use File Rail " + str(i)).value()
                    if has_file_rail:
                        any_file_rail = True
                        rail_type = assembly.get_prompt(
                            "File Rail Type " + str(i)).value()
                        rail_direction = assembly.get_prompt(
                            "File Rail Direction " + str(i)).value()
                        drwr_ins_dict[i] = (
                            rail_direction, rail_type)
            for face_bp in drawers.children:
                if 'BPASSEMBLY' and 'Face' in face_bp.name and any_file_rail:
                    for face in face_bp.children:
                        if 'CUTPART' and not face.hide:
                            face_height = self.get_object_global_location(face)[
                                2]
                            face_height = self.to_inch(face_height)
                            candidate_cutparts[drawers.name][face_height] = face
            if drawers.name in candidate_cutparts:
                candidate_cutparts[drawers.name] = sorted(
                    candidate_cutparts[drawers.name].items(), reverse=True)
        if len(drawer_data_dict) > 0:
            for dd_key, dd_value in drawer_data_dict.items():
                for d_key, d_value in dd_value.items():
                    ins_drw = candidate_cutparts[dd_key]
                    match_cpart_tuple = ins_drw[d_key - 1]
                    match_cpart = match_cpart_tuple[1]
                    join_dict[match_cpart] = d_value
        self.apply_file_drawer_labels(join_dict)

    def apply_partition_height_label(self, partition, displacement=None):
        label = self.to_inch_str(partition.dimensions[0])
        dim = self.add_tagged_dimension(partition)
        dim.anchor.rotation_euler.y = math.radians(-90)
        dim.start_z(value=unit.inch(-1))
        dim.start_x(value=(partition.dimensions[0] / 2) - unit.inch(2))
        if displacement == "left":
            dim.start_z(value=unit.inch(-1))
        if displacement == "right":
            dim.start_z(value=unit.inch(-7))
        dim.start_y(value=0)
        dim.anchor.name = 'PARTHGT'
        dim.end_point.name = 'PARTHGT'
        dim.set_label(label)

    def find_partitions_overlapping(self, partition_list):
        partition_list = sorted(partition_list, key=lambda tup: tup[0])
        overlaps = []
        partition_overlaps = []
        tolerance = unit.inch(1)
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
            return partition_overlaps
        return None

    def find_partition_order(self, partition):
        partitions = []
        hanging_opening = partition.parent
        is_hanging = 'hanging' in hanging_opening.name.lower()
        is_opening = 'opening' in hanging_opening.name.lower()
        if is_hanging and is_opening:
            for item in hanging_opening.children:
                is_partition = 'partition' in item.name.lower()
                if is_partition:
                    item_pos = item.location[0]
                    partitions.append((item_pos, item))
        partitions = sorted(partitions, key=lambda tup: tup[0])
        for i, (pos, item) in enumerate(partitions):
            if item == partition:
                return i

    def partition_height(self, context, wall_bp):
        partition_list = []
        for item in wall_bp.children:
            if item.mv.type == "BPASSEMBLY":
                for partition in item.children:
                    if partition.lm_closets.is_panel_bp:
                        for cutpart in partition.children:
                            has_cutpart = "cutpart" in cutpart.name.lower()
                            if has_cutpart and not cutpart.hide:
                                part_assy = fd_types.Assembly(partition)
                                hang_opng_x_pos = item.location[0]
                                x_pos = hang_opng_x_pos + partition.location[0]
                                x_pos_inch = self.to_inch(x_pos)
                                z_pos_inch = self.to_inch(
                                    partition.location[2])
                                partition_list.append((x_pos_inch,
                                                       z_pos_inch,
                                                       cutpart,
                                                       part_assy))
        overlaps = self.find_partitions_overlapping(partition_list)
        if overlaps is None:
            for x, z, cutpart, assy in partition_list:
                self.apply_partition_height_label(cutpart)
        elif overlaps is not None:
            for i, (x, z, cutpart, assy) in enumerate(partition_list):
                skip = []
                for overlap in overlaps:
                    order = self.find_partition_order(cutpart.parent)
                    if cutpart.name == overlap.name:
                        skip.append(cutpart)
                        if order == 0:
                            self.apply_partition_height_label(cutpart, "right")
                        if order != 0:
                            self.apply_partition_height_label(cutpart, "left")
                if cutpart not in skip:
                    self.apply_partition_height_label(cutpart)

    def topshelf_depth(self, context, item):
        for n_item in item.children:
            if n_item.lm_closets.is_closet_top_bp:
                for k_item in n_item.children:
                    if k_item.mv.type == 'BPASSEMBLY':
                        ts_assembly = fd_types.Assembly(k_item)
                        ts_width = ts_assembly.obj_x.location.x
                        ts_depth = ts_assembly.obj_y.location.y
                        ts_height = ts_assembly.obj_z.location.z
                        offset = ts_width / 2
                        location = (unit.inch(
                            1.06) + offset, 0, unit.inch(-1.06) + ts_height)
                        rotation = (0, math.radians(-45), 0)
                        hashmark = self.draw_hashmark(context, k_item,
                                                      location=location,
                                                      rotation=rotation,
                                                      length=unit.inch(3))
                        dim = self.add_tagged_dimension(hashmark)
                        dim.start_x(value=0)
                        dim.start_y(value=0)
                        dim.start_z(value=unit.inch(-4))
                        dim.set_label(self.to_inch_lbl(ts_depth))
    
    def apply_toe_kick_label(self, context, wall_bp, tk_list):
        for i, tk in enumerate(tk_list):
            label = str(tk) + "\""
            offset = ((i * unit.inch(7)) + unit.inch(2)) * -1
            txt_offset = offset - unit.inch(3)
            dim = self.add_tagged_dimension(wall_bp)
            dim.start_x(value=offset)
            dim.start_y(value=0)
            dim.start_z(value=0)
            dim.end_z(value=unit.inch(tk))
            dim.set_label(" ")
            bpy.ops.object.text_add()
            text = context.active_object
            text.parent = wall_bp
            text.rotation_euler.x = math.radians(90)
            text.rotation_euler.y = math.radians(0)
            text.rotation_euler.z = math.radians(0)
            text.location.x = txt_offset
            text.location.y = 0
            text.location.z = unit.inch(tk) / 2 - unit.inch(0.5)
            text.data.align_x = 'CENTER'
            text.data.size = .07
            text.data.body = label
            text.data.font = self.font

    toe_kick_dim_list = []
    
    def toe_kick_dimension(self, context, item, wall_bp):
        existing_toe_kicks_dict = {}
        for n_item in item.children:
            toe_kick = 'toe' in n_item.name.lower()
            hanging_opng = 'hanging opening' in item.name.lower()
            corner_shelves = 'corner shelves' in item.name.lower()
            has_tk_entry = n_item.name in existing_toe_kicks_dict.keys()
            l_shelves = 'l shelves' in item.name.lower()
            if hanging_opng and toe_kick and not has_tk_entry:
                existing_toe_kicks_dict[item.name] = n_item
                hang_opng_tk = fd_types.Assembly(n_item).obj_z.location.z
                self.toe_kick_dim_list.append(self.to_inch(hang_opng_tk))
            if corner_shelves and toe_kick and not has_tk_entry:
                existing_toe_kicks_dict[item.name] = n_item
                corner_shelf_tk = fd_types.Assembly(n_item).obj_y.location.y
                self.toe_kick_dim_list.append(self.to_inch(corner_shelf_tk))
            if l_shelves and toe_kick and not has_tk_entry:
                existing_toe_kicks_dict[item.name] = n_item
                l_shelf_tk = fd_types.Assembly(n_item).obj_y.location.y
                self.toe_kick_dim_list.append(self.to_inch(l_shelf_tk))

    def fullback_labeling(self, context, item):
        for n_item in item.children:
            if 'backing' in n_item.name.lower():
                show_fullback = False
                label = ""
                fullback_dimensions = object
                offset = -2
                for k_item in n_item.children:
                    if 'cutpart' in k_item.name.lower() and not k_item.hide:
                        show_fullback = True
                        fullback_dimensions = k_item.dimensions
                if show_fullback:
                    full_back_size = abs(self.to_inch(fullback_dimensions[2]))
                    if full_back_size == 0.25:
                        label = ["F/B", "1/4"]
                    if full_back_size == 0.75:
                        label = ["F/B", "3/4"]
                    for lbl in label:
                        offset += 1
                        x = (fullback_dimensions[0] /
                             2) + (unit.inch(2) * offset)
                        y = (fullback_dimensions[1] / 2)
                        dim = self.add_tagged_dimension(n_item)
                        dim.start_x(value=x)
                        dim.start_y(value=y)
                        dim.start_z(value=0)
                        dim.set_label(lbl)

    def slanted_shoes_shelves(self, context, item):
        for candidate in item.children:
            candidate_name = candidate.name.lower()
            insert = 'insert' in candidate_name
            slanted = 'slanted' in candidate_name
            shoe = 'shoe' in candidate_name
            shelf = 'shelf' in candidate_name
            if insert and slanted and shoe and shelf:
                sss_assembly = fd_types.Assembly(candidate)
                #
                shelf_lip_prompt = sss_assembly.get_prompt("Shelf Lip Type")
                shelf_qty_prompt = sss_assembly.get_prompt("Adj Shelf Qty")
                shelf_offset_prompt = sss_assembly.get_prompt(
                    "Distance Between Shelves")
                shelf_lip = shelf_lip_prompt.value()
                shelf_offset = float(shelf_offset_prompt.value())
                shelf_qty = int(shelf_qty_prompt.value())
                #
                z_offset = (shelf_qty - 1) * shelf_offset
                width = sss_assembly.obj_x.location.x
                x_offset = width / 2
                label = "SSS " + shelf_lip + " Lip"
                location = (unit.inch(2.12) + x_offset,
                            0,
                            unit.inch(2.12) + z_offset)
                rotation = (0, math.radians(45), 0)
                hashmark = self.draw_hashmark(context,
                                              candidate,
                                              location=location,
                                              rotation=rotation,
                                              length=unit.inch(6))
                dim = self.add_tagged_dimension(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(5))
                dim.set_label(label)

    def jewelry_drawer_labeling(self, item):
        def get_inserts(obj):
            if obj.lm_closets.is_drawer_stack_bp:
                hier = [obj]
            else:
                hier = []
            if len(obj.children) > 0:
                for c in obj.children:
                    hier.extend(get_inserts(c))
            return hier
        inserts = get_inserts(item)
        drwr_boxes = [c for i in inserts for c in i.children if (
            c.lm_closets.is_drawer_box_bp and
            fd_types.Assembly(c).get_prompt('Hide') and not
            fd_types.Assembly(c).get_prompt('Hide').value())]

        for b in drwr_boxes:
            assy = fd_types.Assembly(b)
            prnt_assy = fd_types.Assembly(b.parent)
            lbl_x = prnt_assy.obj_x.location.x + unit.inch(5)
            lbl_y = assy.obj_z.location.z
            pmt_val = False
            for d in b.animation_data.drivers:
                d_vars = d.driver.variables
                var = None
                for v in d_vars:
                    if v.name == 'UDD':
                        var = v
                if var:
                    dp = var.targets[0].data_path
                    pmt_val = eval('%s.%s' % (repr(prnt_assy.obj_bp), dp))
            if pmt_val:
                lbl = self.add_tagged_dimension(b)
                lbl.set_label('Db Jwlry')
                lbl_loc = (lbl_x, 0, lbl_y)
                self.copy_world_loc(b, lbl.anchor, lbl_loc)
                # Draw an hashmark using OpenGL dimensions
                hshmk = self.add_tagged_dimension(lbl.anchor)
                hshmk.opengl_dim.line_only = True
                hshmk.opengl_dim.gl_width = 2
                hshmk.anchor.rotation_euler.y = math.radians(135)
                hshmk.start_x(value=-unit.inch(2.5))
                hshmk.start_z(value=-unit.inch(0.5))
                hshmk.end_x(value=unit.inch(4))

    def lock_labeling(self, item):
        def get_inserts(obj):
            if (obj.lm_closets.is_drawer_stack_bp or
                    obj.lm_closets.is_door_insert_bp):
                hier = [obj]
            else:
                hier = []
            if len(obj.children) > 0:
                for c in obj.children:
                    hier.extend(get_inserts(c))
            return hier

        inserts = get_inserts(item)

        locks = [c for i in inserts for c in i.children if ('Lock' in c.name and
                                                            c.mv.type == 'BPASSEMBLY' and
                                                            fd_types.Assembly(c).get_prompt('Hide') and not
                                                            fd_types.Assembly(c).get_prompt('Hide').value())]

        for l in locks:
            prnt_assy = fd_types.Assembly(l.parent)
            lbl_str = ''
            lbl_x = 0
            lbl_y = 0
            lbl_loc = (0, 0, 0)
            add_hsh = False
            hsh_len = 0

            if prnt_assy.obj_bp.lm_closets.is_drawer_stack_bp:
                pmt_val = ''
                # Get placement value of each lock
                for d in l.animation_data.drivers:
                    d_vars = d.driver.variables
                    var = None
                    for v in d_vars:
                        if v.name == 'Lock_Drawer':
                            var = v
                    if var:
                        dp = var.targets[0].data_path
                        dp = dp.replace('EnumIndex', 'value()')
                pmt_val = eval('%s.%s' % (repr(prnt_assy.obj_bp), dp))
                if pmt_val != '' and pmt_val != 'None':
                    if pmt_val == 'Top':
                        lbl_x = -unit.inch(5.5)
                        lbl_y = -unit.inch(0.5)
                        lbl_loc = (lbl_x, 0, lbl_y)
                        lbl_str = 'Top Lock'
                    else:
                        if pmt_val == 'Left':
                            x_off = 3.5
                        elif pmt_val == 'Right':
                            x_off = 2.5
                        add_hsh = True
                        hsh_len = unit.inch(5)
                        lbl_x = -hsh_len / math.sqrt(2) - unit.inch(x_off)
                        lbl_y = hsh_len / math.sqrt(2) + unit.inch(0.5)
                        lbl_loc = (0, lbl_x, lbl_y)
                        lbl_str = '{} Lock'.format(pmt_val[0])

            elif prnt_assy.obj_bp.lm_closets.is_door_insert_bp:
                lck_pnl = prnt_assy.get_prompt('Lock to Panel')
                fdd = prnt_assy.get_prompt('Force Double Doors')

                if lck_pnl and lck_pnl.value():
                    for d in prnt_assy.obj_bp.children:
                        if (d.lm_closets.is_door_bp and
                            fd_types.Assembly(d).get_prompt('Hide') and not
                                fd_types.Assembly(d).get_prompt('Hide').value()):
                            if 'Left Door' in d.name:
                                lbl_str = 'R Panel|Lock'
                                x_off = 2
                            elif 'Right Door' in d.name:
                                lbl_str = 'L Panel|Lock'
                                x_off = 3
                    add_hsh = True
                    hsh_len = unit.inch(2)
                    lbl_x = -hsh_len / math.sqrt(2) - unit.inch(x_off)
                    lbl_y = hsh_len / math.sqrt(2) + unit.inch(2)
                    lbl_loc = (0, lbl_x, lbl_y)

                else:
                    lbl_str = 'Lock'
                    if fdd and fdd.value():
                        lbl_x = -unit.inch(4)
                        lbl_y = -unit.inch(0.5)
                        lbl_loc = (0, lbl_y, lbl_x)
                    else:
                        lbl_x = unit.inch(5)
                        lbl_loc = (lbl_x, 0, lbl_y)

            lbl = self.add_tagged_dimension(l)
            lbl.set_label(lbl_str)

            if add_hsh:
                # Using a dimension as a hashmark
                hshmk = self.add_tagged_dimension(l)
                hshmk.opengl_dim.line_only = True
                hshmk.opengl_dim.gl_width = 2
                hshmk.end_y(value=hsh_len)
                self.copy_world_loc(l, hshmk.anchor)
                self.copy_world_rot(l, hshmk.anchor, (135, 0, 0))
            self.copy_world_loc(l, lbl.anchor, lbl_loc)
            self.copy_world_rot(l, lbl.anchor)

    def filler_labeling(self, context, item):
        for child in item.children:
            if 'filler' in child.name.lower():
                for cc in child.children:
                    if 'cutpart' in cc.name.lower() and not cc.hide:
                        filler_assy = fd_types.Assembly(child)
                        filler_measure = filler_assy.obj_y.location.y
                        filler_amount = self.to_inch_lbl(abs(filler_measure))
                        z_offset = child.location[2] + unit.inch(3)
                        # Filler Measure
                        # NOTE to change Z-position change X values
                        #      to change X-position change Y values
                        filler_dim = self.add_tagged_dimension(child)
                        filler_dim.start_x(value=0 - z_offset)
                        filler_dim.start_y(value=filler_measure / 2)
                        filler_dim.start_z(value=0)
                        filler_dim.set_label(filler_amount)
                        # Filler Label
                        filler_lbl = self.add_tagged_dimension(child)
                        filler_lbl.start_x(value=0 - z_offset - unit.inch(3))
                        filler_lbl.start_y(value=filler_measure / 2)
                        filler_lbl.start_z(value=0)
                        filler_lbl.set_label("Filler")

    def txt_label(self, body, font, size, align_x, align_y, context):
        label_curve = bpy.data.curves.new(type='FONT', name=body)
        label_curve.fill_mode = 'FRONT'
        label_curve.body = body
        label_curve.font = font
        label_curve.size = size
        label_curve.align_x = align_x
        label_curve.align_y = align_y
        label = bpy.data.objects.new('LABEL.' + body, label_curve)
        context.scene.objects.link(label)
        return label

    def capping_bottom_label(self, item):
        for n_item in item.children:
            if n_item.lm_closets.is_closet_bottom_bp:
                cp_btm_insert = fd_types.Assembly(n_item)
                exp_l = cp_btm_insert.get_prompt('Exposed Left')
                exp_r = cp_btm_insert.get_prompt('Exposed Right')
                cp_btm_bp = [obj for obj in n_item.children
                             if obj.mv.type == 'BPASSEMBLY'][0]

                # Main capping bottom label
                cp_btm_assy = fd_types.Assembly(cp_btm_bp)
                cp_btm_width = cp_btm_assy.obj_x.location.x
                cp_btm_depth = cp_btm_assy.obj_y.location.y
                hshmk_size = unit.inch(2)
                label_off = unit.inch(2.5)
                hshmk_rot = (0, math.radians(-45), 0)
                hshmk = self.add_tagged_dimension(cp_btm_bp)
                hshmk.opengl_dim.line_only = True
                hshmk.opengl_dim.gl_width = 2
                hshmk.start_x(value = cp_btm_width / 2)
                hshmk.end_z(value = hshmk_size)
                hshmk.anchor.rotation_euler = hshmk_rot
                label_str = 'Cap. Bttm {}'.format(self.to_inch_lbl(cp_btm_depth))
                label = self.add_tagged_dimension(hshmk.end_point)
                label.start_z(value = label_off)
                label.set_label(label_str)

                # Exposed edges labels
                if exp_l and exp_l.value():
                    hshmk_exp_l = self.add_tagged_dimension(cp_btm_bp)
                    hshmk_exp_l.opengl_dim.line_only = True
                    hshmk_exp_l.opengl_dim.gl_width = 2
                    hshmk_exp_l.end_z(value = hshmk_size)
                    hshmk_exp_l.anchor.rotation_euler = hshmk_rot
                    label_exp_l = self.add_tagged_dimension(hshmk_exp_l.end_point)
                    label_exp_l.start_z(value = label_off)
                    label_exp_l.set_label('Exp.')

                if exp_r and exp_r.value():
                    hshmk_exp_r = self.add_tagged_dimension(cp_btm_bp)
                    hshmk_exp_r.opengl_dim.line_only = True
                    hshmk_exp_r.opengl_dim.gl_width = 2
                    hshmk_exp_r.start_x(value = cp_btm_width)
                    hshmk_exp_r.end_z(value = hshmk_size)
                    hshmk_exp_r.anchor.rotation_euler = (0, math.radians(45), 0)
                    label_exp_r = self.add_tagged_dimension(hshmk_exp_r.end_point)
                    label_exp_r.start_z(value = label_off)
                    label_exp_r.set_label('Exp.')

    def add_glass_cutpart_dim(self, context, assembly, cutpart, thickness):
        setback = 0.25
        section_depth = self.to_inch(
            assembly.location[1])
        shelf_depth = self.to_inch(
            cutpart.dimensions[1])
        depth_part_diff = abs(
            section_depth - shelf_depth)
        shelves_qtt = cutpart.modifiers["ZQuantity"].count
        shelves_offset = cutpart.modifiers[
            "ZQuantity"].constant_offset_displace[2]
        width = cutpart.dimensions[0]
        # For cutparts that differs from the section depth minus setback (0.25)
        if depth_part_diff != setback and depth_part_diff != 0.0:
            label = self.to_inch_lbl(
                cutpart.dimensions[1])
        else:
            label = self.to_inch_lbl(
                assembly.location[1])
        label += " Glass "
        label += thickness
        for i in range(shelves_qtt):
            z_offset = shelves_offset + (shelves_offset *
                                         (i - 1))
            location = (width/2,
                        0,
                        unit.inch(2.12) + z_offset)
            rotation = (0, math.radians(45), 0)
            hashmark = self.draw_hashmark(context,
                                          cutpart,
                                          location=location,
                                          rotation=rotation,
                                          length=unit.inch(6))
            dim = self.add_tagged_dimension(hashmark)
            dim.start_x(value=0)
            dim.start_y(value=0)
            dim.start_z(value=unit.inch(5))
            dim.set_label(label)

    def glass_shelves(self, context, item):
        for candidate in item.children:
            candidate_lowername = candidate.name.lower()
            insert = 'insert' in candidate_lowername
            shelves = 'shelves' in candidate_lowername
            glass = 'glass' in candidate_lowername
            if insert and shelves and glass:
                insert_assembly = fd_types.Assembly(candidate)
                glass_prompt = insert_assembly.get_prompt(
                    "Glass Shelf Thickness")
                glass_thickness = glass_prompt.value()
                for assem_candidate in candidate.children:
                    if assem_candidate.lm_closets.is_glass_shelf_bp:
                        for cutpart_candidate in assem_candidate.children:
                            if 'cutpart' in cutpart_candidate.name.lower():
                                self.add_glass_cutpart_dim(context,
                                                           assem_candidate,
                                                           cutpart_candidate,
                                                           glass_thickness)
    # Its to figure out if has variable children
    variable_sections_list = []

    def has_variable_descendants(self, item):
        if item.mv.opening_name:
            carcass_bp = utils.get_parent_assembly_bp(item)
            carcass_assembly = fd_types.Assembly(carcass_bp)
            variable_section = carcass_assembly.get_prompt(
                "CTF Opening {}".format(item.mv.opening_name)).value()
            if variable_section:
                self.variable_sections_list.append(item.mv.opening_name)
        if len(item.children) > 0:
            for i in item.children:
                self.has_variable_descendants(i)

    def variable_opening_label(self, context, item):
        for n_item in item.children:
            if 'OPENING' in n_item.name:
                self.has_variable_descendants(n_item)
                variable_sections = set(self.variable_sections_list)
                self.variable_sections_list = []
                if len(variable_sections) > 0:
                    section_width = 0
                    for k_item in n_item.children:
                        if k_item.mv.type == 'VPDIMX':
                            section_width = k_item.location[0]
                    dim = self.add_tagged_dimension(n_item)
                    dim.start_x(value=section_width / 2)
                    dim.start_y(value=section_width / 2)
                    dim.start_z(value=unit.inch(-7) +
                                (n_item.location[2] / -1))
                    dim.set_label("Var.")

    def valances(self, context, item):
        for candidate in item.children:
            product = 'product' in candidate.name.lower()
            valance = 'valance' in candidate.name.lower()
            if product and valance:
                valance_assembly = fd_types.Assembly(candidate)
                width = valance_assembly.obj_x.location.x
                height = valance_assembly.get_prompt(
                    "Molding Height").value()
                location = valance_assembly.get_prompt(
                    "Molding Location").value()
                x_offset = width / 2 + unit.inch(0.68)
                z_offset = (abs(height) + abs(location) + unit.inch(0.68)) * -1
                hashmark_location = (x_offset,
                                     0,
                                     z_offset)
                rotation = (math.radians(135), 0, math.radians(90))
                label = "Valance " + self.to_inch_lbl(abs(height))
                hashmark = self.draw_hashmark(context,
                                              candidate,
                                              location=hashmark_location,
                                              rotation=rotation,
                                              length=unit.inch(2))
                dim = self.add_tagged_dimension(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(4))
                dim.set_label(label)

    def copy_world_loc(self, source, target, offset=(0, 0, 0)):
        off_mtx = mathutils.Matrix.Translation(mathutils.Vector(offset))
        result_loc = (source.matrix_world * off_mtx).to_translation()
        target.matrix_world.translation = result_loc

    def copy_world_rot(self, source, target, offset=(0, 0, 0)):
        off_rad = [math.radians(o) for o in offset]
        off_mtx = mathutils.Euler(off_rad, source.rotation_mode).to_matrix()
        result_rot = source.matrix_world.to_3x3().normalized() * off_mtx
        target.matrix_world *= result_rot.to_4x4()

    def blind_corner_panel_labels(self, context, item):
        bcps = []
        opns = []

        for n_item in item.children:
            assy = fd_types.Assembly(n_item)
            hide = assy.get_prompt('Hide')
            is_bcp = n_item.lm_closets.is_blind_corner_panel_bp
            if is_bcp and hide and not hide.value():
                bcps.append(assy)
            elif n_item.mv.type_group == 'OPENING':
                opns.append(assy)

        for bcp in bcps:
            is_l_bcp = bcp.get_prompt('Is Left Blind Corner Panel')
            is_r_bcp = bcp.get_prompt('Is Right Blind Corner Panel')
            bcp_x = bcp.obj_bp.location.x
            bcp_y = bcp.obj_bp.location.y
            bcp_z = bcp.obj_bp.location.z
            bcp_w = bcp.obj_y.location.y
            bcp_h = bcp.obj_x.location.x
            bcp_d = bcp.obj_z.location.z

            bcp_str = '%s BCP' % self.to_inch_lbl(bcp_w)
            bcp_lbl_x = bcp_h * 0.55
            bcp_lbl_y = bcp_w * 0.5
            bcp_lbl_loc = (bcp_lbl_x, bcp_lbl_y, 0)
            bcp_lbl = self.add_tagged_dimension(item.parent)
            bcp_lbl.set_label(bcp_str)
            self.copy_world_loc(bcp.obj_bp, bcp_lbl.anchor, bcp_lbl_loc)

            for opn in opns:
                opn_y = opn.obj_bp.location.y
                opn_z = opn.obj_bp.location.z
                opn_w = opn.obj_x.location.x
                opn_h = opn.obj_z.location.z
                opn_x = opn.obj_bp.location.x

                match_x, match_y, match_z = False, False, False

                if is_l_bcp and is_l_bcp.value():
                    match_x = math.isclose(bcp_x + bcp_d, opn_x, abs_tol=1e-3)
                    match_y = math.isclose(bcp_y + bcp_d, opn_y, abs_tol=1e-3)
                    match_z = math.isclose(bcp_z + (bcp_h - opn_h) * 0.5,
                                           opn_z, abs_tol=1e-3)

                elif is_r_bcp and is_r_bcp.value():
                    match_x = math.isclose(
                        bcp_x, opn_x + opn_w + bcp_d, abs_tol=1e-3)
                    match_y = math.isclose(bcp_y, opn_y, abs_tol=1e-3)
                    match_z = math.isclose(bcp_z + (bcp_h - opn_h) * 0.5,
                                           opn_z, abs_tol=1e-3)

                if match_x and match_y and match_z:
                    gap_w = opn_w - bcp_w
                    gap_str = '%s Open' % self.to_inch_lbl(gap_w + bcp_d)
                    gap_lbl_x = -unit.inch(3)
                    gap_lbl_y = opn_w - gap_w * 0.5
                    gap_lbl_loc = (gap_lbl_x, gap_lbl_y, 0)
                    gap_lbl = self.add_tagged_dimension(item.parent)
                    gap_lbl.set_label(gap_str)
                    self.copy_world_loc(
                        bcp.obj_bp, gap_lbl.anchor, gap_lbl_loc)

    def flat_crown(self, context, item):
        wall = fd_types.Assembly(item.parent)
        assy = fd_types.Assembly(item)
        hang_h = assy.obj_z.location.z
        tkd_vo = assy.get_prompt('Top KD 1 Vertical Offset')
        labels = []
        tkh_str = ''
        for p in item.children:
            if p.lm_closets.is_flat_crown_bp and p.mv.type_group == 'INSERT':
                fc_prod = fd_types.Assembly(p)
                ext_ceil = fc_prod.get_prompt('Extend To Ceiling')
                tkh = fc_prod.get_prompt('Top KD Holes Down')
                if ext_ceil and ext_ceil.value() and tkh and tkd_vo:
                    if tkh.value() == 'One':
                        tkh_str = 'Top KD|Down 1 Hole'
                    elif tkh.value() == 'Two':
                        tkh_str = 'Top KD|Down 2 Holes'
                    hang_h -= tkd_vo.value()
                for a in p.children:
                    if a.mv.type == 'BPASSEMBLY' and 'Flat Crown' in a.name:
                        fc_assy = fd_types.Assembly(a)
                        fc_h = fc_assy.obj_y.location.y
                        fc_str = 'Flat Crown %s' % self.to_inch_lbl(fc_h)
                        labels.append((fc_str, fc_h))
        labels = list(dict.fromkeys(labels))
        if tkh_str:
            labels.append((tkh_str, -unit.inch(3)))

        for l in labels:
            lbl = self.add_tagged_dimension(wall.obj_bp)
            lbl.set_label(l[0])
            lbl_z = hang_h + (l[1] * 0.5)
            lbl.start_x(value=unit.inch(-20))
            lbl.start_z(value=lbl_z)

    def light_rails(self, context, item):
        for candidate in item.children:
            product = 'product' in candidate.name.lower()
            light = 'light' in candidate.name.lower()
            rail = 'rail' in candidate.name.lower()
            if product and light and rail:
                light_rail_assembly = fd_types.Assembly(candidate)
                width = light_rail_assembly.obj_x.location.x
                height = light_rail_assembly.get_prompt(
                    "Molding Height").value()
                location = light_rail_assembly.get_prompt(
                    "Molding Location").value()
                x_offset = width / 2 + unit.inch(0.68)
                z_offset = (abs(height) + abs(location) + unit.inch(0.68)) * -1
                hashmark_location = (x_offset,
                                     0,
                                     z_offset)
                rotation = (math.radians(135), 0, math.radians(90))
                label = "Light Rails " + self.to_inch_lbl(abs(height))
                hashmark = self.draw_hashmark(context,
                                              candidate,
                                              location=hashmark_location,
                                              rotation=rotation,
                                              length=unit.inch(2))
                dim = self.add_tagged_dimension(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(4))
                dim.set_label(label)

    def countertop_hashmark(self, context, item):
        material_name = ""
        for n_item in item.children:
            if n_item.lm_closets.is_counter_top_insert_bp:
                ctop_assembly = fd_types.Assembly(n_item)
                width = abs(ctop_assembly.obj_x.location.x)
                counter_top_width = 0
                counter_top_depth = 0
                counter_top_height = 0
                # n_item is at CTOP INSERT level
                for k_item in n_item.children:
                    for x_item in k_item.children:
                        if not x_item.hide and 'hashmark' not in x_item.name.lower():
                            # HACK to display the material correctly
                            # Until the context materials get fixed
                            if 'hpl' in x_item.name.lower():
                                material_name = "HPL"
                            elif 'melamine' in x_item.name.lower():
                                material_name = "Mel."
                            elif 'granite' in x_item.name.lower():
                                material_name = "Gran."
                            for sibling in x_item.parent.children:
                                if sibling.mv.type == 'VPDIMX':
                                    counter_top_width = abs(
                                        sibling.location[0])
                                if sibling.mv.type == 'VPDIMY':
                                    counter_top_depth = abs(
                                        sibling.location[1])
                                if sibling.mv.type == 'VPDIMZ':
                                    counter_top_height = abs(
                                        sibling.location[2])
                context_material = material_name
                material = ""
                if not None:
                    material += context_material
                material += " "
                for spec_group in context.scene.mv.spec_groups:
                    material += spec_group.materials["Countertop_Surface"].item_name
                x_offset = width / 2
                z_offset = counter_top_height + unit.inch(1.06)
                location = (unit.inch(1.06) + x_offset, 0, z_offset)
                rotation = (0, math.radians(45), 0)
                hashmark = self.draw_hashmark(context, n_item, location,
                                              rotation,
                                              length=unit.inch(3))
                counter_top_width_str = self.to_inch_lbl(counter_top_width)
                counter_top_depth_str = self.to_inch_lbl(counter_top_depth)
                counter_top_height_str = self.to_inch_lbl(
                    counter_top_height)
                # Countertop Dimensions
                label = (material + " C.T. " + counter_top_width_str +
                         " x " + counter_top_depth_str)
                ctop_dim = self.add_tagged_dimension(hashmark)
                ctop_dim.start_x(value=unit.inch(-2.12))
                ctop_dim.start_y(value=0)
                ctop_dim.start_z(value=unit.inch(3))
                ctop_dim.set_label(label)

    def ctop_exposed_dim(self, context, parent, location, rotation):
        mark = self.draw_hashmark(context, parent,
                                  location=location,
                                  rotation=rotation,
                                  length=unit.inch(3))
        dim = self.add_tagged_dimension(mark)
        dim.start_x(value=0)
        dim.start_y(value=0)
        dim.start_z(value=unit.inch(4))
        dim.set_label("Exp.")

    def countertop_exposed_label(self, context, item):
        for n_item in item.children:
            if n_item.lm_closets.is_counter_top_insert_bp:
                ctop_assembly = fd_types.Assembly(n_item)
                ctop_exposed_left = ctop_assembly.get_prompt("Exposed Left")
                ctop_exposed_right = ctop_assembly.get_prompt("Exposed Right")
                ctop_exposed_back = ctop_assembly.get_prompt("Exposed Back")
                extended_left = ctop_assembly.get_prompt("Extend Left Amount")
                extended_right = ctop_assembly.get_prompt(
                    "Extend Right Amount")
                width = abs(ctop_assembly.obj_x.location.x)
                counter_top_height = 0
                # n_item is at CTOP INSERT level
                for k_item in n_item.children:
                    for x_item in k_item.children:
                        if not x_item.hide and 'hashmark' not in x_item.name.lower():
                            for sibling in x_item.parent.children:
                                if sibling.mv.type == 'VPDIMZ':
                                    counter_top_height = abs(
                                        sibling.location[2])
                z_offset = counter_top_height + unit.inch(1.06)
                if ctop_exposed_left.value() is True:
                    extension = 0
                    if extended_left is not None:
                        extension = extended_left.value()
                    offset = 0 - extension
                    location = (unit.inch(-1.06) + offset, 0, z_offset)
                    rotation = (0, math.radians(-45), 0)
                    self.ctop_exposed_dim(context, n_item, location, rotation)
                if ctop_exposed_right.value() is True:
                    extension = 0
                    if extended_right is not None:
                        extension = extended_right.value()
                    offset = width + extension
                    location = (unit.inch(1.06) + offset, 0, z_offset)
                    rotation = (0, math.radians(45), 0)
                    self.ctop_exposed_dim(context, n_item, location, rotation)
                if ctop_exposed_back.value() is True:
                    offset = width / 4
                    location = (unit.inch(-1.06) + offset, 0, z_offset)
                    rotation = (0, math.radians(-45), 0)
                    self.ctop_exposed_dim(context, n_item, location, rotation)

    def ct_overhang_label(self, obj_bp):
        hsh_len = unit.inch(5.5)
        hsh_off = hsh_len / math.sqrt(2)
        sides = []

        # Labeling overhangs for island
        if obj_bp.lm_closets.is_island:
            isl_assy = fd_types.Assembly(obj_bp)
            no_ct = isl_assy.get_prompt('No Countertop')
            overhang = isl_assy.get_prompt('Side Deck Overhang')
            use_ct = no_ct and not no_ct.value()

            if use_ct and overhang and overhang.value() > 0:
                isl_w = isl_assy.obj_x.location.x
                isl_h = isl_assy.obj_z.location.z
                toe_kick_h = isl_assy.get_prompt('Toe Kick Height').value()
                ct_loc_z = isl_h + toe_kick_h

                # Left side label
                sides.append(dict(
                    prnt = obj_bp,
                    ext = overhang.value(),
                    hshmk_rot = math.radians(135),
                    hsh_st_x = -overhang.value(),
                    hsh_st_z = ct_loc_z,
                    lbl_x = - hsh_off - overhang.value(),
                    lbl_y = ct_loc_z - hsh_off - unit.inch(2),
                    tgt_obj = obj_bp))

                # Right side label
                sides.append(dict(
                    prnt = obj_bp,
                    ext = overhang.value(),
                    hshmk_rot = math.radians(45),
                    hsh_st_x = isl_w + overhang.value(),
                    hsh_st_z = ct_loc_z,
                    lbl_x = hsh_off + overhang.value(),
                    lbl_y = ct_loc_z - hsh_off - unit.inch(2),
                    tgt_obj = isl_assy.obj_x))

        else:
            for item in obj_bp.children:
                if item.lm_closets.is_counter_top_insert_bp:
                    ctop_assy = fd_types.Assembly(item)
                    ctop_w = ctop_assy.obj_x.location.x
                    overhang_l = ctop_assy.get_prompt('Extend Left Amount')
                    overhang_r = ctop_assy.get_prompt('Extend Right Amount')

                    if overhang_l and overhang_l.value() > 0:
                        sides.append(dict(
                            prnt = item,
                            ext = overhang_l.value(),
                            hshmk_rot = math.radians(135),
                            hsh_st_x = -overhang_l.value(),
                            hsh_st_z = 0,
                            lbl_x = -hsh_off - overhang_l.value(),
                            lbl_y = -hsh_off - unit.inch(2),
                            tgt_obj = item))

                    if overhang_r and overhang_r.value() > 0:
                        sides.append(dict(
                            prnt = item,
                            ext = overhang_r.value(),
                            hshmk_rot = math.radians(45),
                            hsh_st_x = ctop_w + overhang_r.value(),
                            hsh_st_z = 0,
                            lbl_x = hsh_off + overhang_r.value(),
                            lbl_y = -hsh_off - unit.inch(2),
                            tgt_obj = ctop_assy.obj_x))

        for s in sides:
            hshmk = self.add_tagged_dimension(s['prnt'])
            hshmk.opengl_dim.line_only = True
            hshmk.opengl_dim.gl_width = 2
            hshmk.start_x(value = s['hsh_st_x'])
            hshmk.start_z(value = s['hsh_st_z'])
            hshmk.end_x(value = hsh_len)
            hshmk.anchor.rotation_euler.y = s['hshmk_rot']
            lbl = self.add_tagged_dimension(s['prnt'])
            lbl_str = '{} Overhang'.format(self.to_inch_lbl(s['ext']))
            lbl_loc = (s['lbl_x'], 0, s['lbl_y'])
            lbl.set_label(lbl_str)
            self.copy_world_loc(s['tgt_obj'], lbl.anchor, lbl_loc)
            
    def apply_build_height_label(self, context, wall_bp, position, multiplier):
        offset = unit.inch(-7) + (unit.inch(-4) * multiplier)
        dim = self.add_tagged_dimension(wall_bp)
        dim.start_x(value=offset)
        dim.start_y(value=offset)
        dim.start_z(value=0)
        dim.end_z(value=position)
        label = self.to_inch_lbl(position)
        dim.set_label(" ")
        bpy.ops.object.text_add()
        text = context.active_object
        text.parent = wall_bp
        text.rotation_euler.x = math.radians(0)
        text.rotation_euler.y = math.radians(-90)
        text.rotation_euler.z = math.radians(90)
        text.location.x = offset - unit.inch(1)
        text.location.y = 0
        text.location.z = ((position / 2))
        text.data.align_x = 'CENTER'
        text.data.size = .1
        text.data.body = label
        text.data.font = self.font

    def build_height_dimension(self, context, wall_bp):
        build_height_dims_list = []
        for item in wall_bp.children:
            if 'hanging' in item.name.lower():
                build_height_dim = 0
                countertop_height = 0
                ctop_thickness = 0
                topshelf_thickness = 0
                hanging_assy = fd_types.Assembly(item)
                hanging_height = 0
                if hasattr(hanging_assy.obj_z, 'location'):
                    hanging_height = hanging_assy.obj_z.location.z
                    for n_item in item.children:
                        if n_item.lm_closets.is_counter_top_insert_bp:
                            countertop_height = n_item.location[2]
                            for k_item in n_item.children:
                                for x_item in k_item.children:
                                    if not x_item.hide:
                                        ctop_thickness = abs(x_item.dimensions[2])

                        if n_item.lm_closets.is_closet_top_bp:
                            for k_item in n_item.children:
                                if k_item.mv.type == 'BPASSEMBLY':
                                    for f_item in k_item.children:
                                        if f_item.mv.type == 'VPDIMZ':
                                            topshelf_thickness = abs(
                                                f_item.location[2])
                hanging = hanging_height > 0
                ctop = ctop_thickness == 0
                tshelf = topshelf_thickness == 0
                if hanging and ctop and tshelf:
                    build_height_dim = hanging_height
                elif ctop_thickness > 0:
                    build_height_dim = (countertop_height + ctop_thickness)
                elif topshelf_thickness > 0:
                    build_height_dim = (hanging_height + topshelf_thickness)
                build_height_dims_list.append(build_height_dim)
        build_height_dims_list = list(set(build_height_dims_list))
        build_height_dims_list = sorted(build_height_dims_list)
        for i, value in enumerate(build_height_dims_list):
            self.apply_build_height_label(context,
                                          wall_bp,
                                          value, i)
        dims_offset = (unit.inch(-4) * len(build_height_dims_list))
        max_offset = unit.inch(-7) + dims_offset
        return max_offset

    def section_depths(self, context, wall_bp):
        wall = wall_bp.children
        candidates = [item for item in wall if item.mv.type == 'BPASSEMBLY']
        n_openings = [[item for item in obj.children if 'OPENING' in item.name]
                      for obj in candidates]
        for openings in n_openings:
            for opening in openings:
                opening_assembly = fd_types.Assembly(opening)
                depth = opening_assembly.obj_y.location.y
                hashmark = self.draw_hashmark(context, opening,
                                              location=(
                                                  unit.inch(2.12),
                                                  0,
                                                  unit.inch(2.12)),
                                              rotation=(
                                                  0, math.radians(45), 0),
                                              length=unit.inch(6))
                dim = self.add_tagged_dimension(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(5))
                dim.set_label(self.to_inch_str(depth) + "\"")

    def execute(self, context):
        self.clean_up_scene(context)
        scene_props = get_dimension_props()
        self.font = opengl_dim.get_custom_font()
        self.font_bold = opengl_dim.get_custom_font_bold()

        isls = [a.obj_bp for a in common_closet_utils.scene_assemblies(context)
                        if a.obj_bp.lm_closets.is_island]

        # Set Island Product Annotations
        for isl in isls:
            if scene_props.ct_overhang:
                self.ct_overhang_label(isl)

        # Set Panel Numbers
        # for wall_bp in common_closet_utils.scene_walls(context):
        #     panels = self.get_wall_panels(wall_bp) #GET SORTED LIST OF PANELS
        #     for i , panel_bp in enumerate(panels):
        #         panel_bp.mv.opening_name = str(i + 1)
        #         panel_bp.mv.comment_2 = str(i + 1)

        # Set Closet Product Annotations
        for wall_bp in common_closet_utils.scene_walls(context):
            bheight_offset = 0
            # closet_products = self.get_wall_products(wall_bp)
            # self.add_closet_annotations(closet_products)
            if scene_props.framing_height:
                bheight_offset = self.build_height_dimension(context, wall_bp)
            if scene_props.section_depths:
                self.section_depths(context, wall_bp)
            if scene_props.section_widths:
                self.section_widths(context, wall_bp)
            if scene_props.l_shelves:
                self.l_shelves(context, wall_bp)
            if scene_props.corner_shelves:
                self.corner_shelves(context, wall_bp)
            if scene_props.partition_height:
                self.partition_height(context, wall_bp)
            for child in wall_bp.children:
                if child.mv.is_wall_mesh and scene_props.ceiling_height:
                    self.ceiling_height_dimension(context, child,
                                                  bheight_offset)

                if child.mv.type == "BPASSEMBLY":
                    # Shelves Options
                    if scene_props.slanted_shoe_shelves:
                        self.slanted_shoes_shelves(context, child)
                    if scene_props.glass_shelves:
                        self.glass_shelves(context, child)
                    if scene_props.shelf_setback:
                        self.setback_standard_shelf(context, child)
                        self.arrayed_shelves_section_depth_dimension(context,
                                                                     child)

                    # Doors and Drawers Options
                    if scene_props.double_jewelry:
                        self.jewelry_drawer_labeling(child)
                    if scene_props.file_drawers:
                        self.file_drawer_labeling(context, child)
                    if scene_props.locks:
                        self.lock_labeling(child)

                    # Molding Options
                    if scene_props.valances:
                        self.valances(context, child)
                    if scene_props.light_rails:
                        self.light_rails(context, child)
                    if scene_props.flat_crown:
                        self.flat_crown(context, child)
                    if scene_props.blind_corner_panel_labels:
                        self.blind_corner_panel_labels(context, child)
                    if scene_props.capping_bottom:
                        self.capping_bottom_label(child)
                    # if scene_props.traditional_crown:
                    #     print("traditional_crown")

                    # General Options
                    if scene_props.toe_kick_height:
                        self.toe_kick_dimension(context, child, wall_bp)
                    if scene_props.top_shelf_depth:
                        self.topshelf_depth(context, child)
                    if scene_props.filler:
                        self.filler_labeling(context, child)
                    if scene_props.countertop:
                        self.countertop_hashmark(context, child)
                        self.countertop_exposed_label(context, child)
                    if scene_props.ct_overhang:
                        self.ct_overhang_label(child)
                    if scene_props.fullback:
                        self.fullback_labeling(context, child)
                    if scene_props.variable:
                        self.variable_opening_label(context, child)
            self.wall_width_dimension(wall_bp)
            if len(self.toe_kick_dim_list) > 0:
                tk_dims = sorted(list(set(self.toe_kick_dim_list)))
                self.apply_toe_kick_label(context, wall_bp, tk_dims)
            self.toe_kick_dim_list = []

        # Add Part Annotations
        for assembly in common_closet_utils.scene_assemblies(context):

            props = props_closet.get_object_props(assembly.obj_bp)

            # self.toe_kick_dimension(context, item, assembly)

            # if props.is_panel_bp:
            #     if scene_props.framing_height:
            #         self.add_panel_height_annotation(assembly)
#             else:
#                 if assembly.obj_bp.mv.opening_name != "":
#                     self.set_section_number(assembly)

            # FIXED SHELF AND ROD ANNOTATIONS
#             if props.is_fixed_shelf_and_rod_product_bp:
#                 self.add_fixed_shelf_and_rod_annotations(assembly)

            # SHELF LABEL
            if props.is_shelf_bp:
                is_locked_shelf = assembly.get_prompt("Is Locked Shelf")

                if is_locked_shelf and is_locked_shelf.value() and scene_props.kds:
                    shelf_label = self.add_tagged_dimension(assembly.obj_bp)
                    shelf_label.start_x(value=assembly.obj_x.location.x/2)
                    shelf_label.start_y(value=0)
                    shelf_label.start_z(
                        value=-math.fabs(assembly.obj_z.location.z/2))
                    shelf_label.set_label("KD")

#                 if is_locked_shelf and is_locked_shelf.value() == False and scene_props.label_adj_shelves:
#                     shelf_label = self.add_dimension(assembly.obj_bp)
#                     shelf_label.start_x(value = assembly.obj_x.location.x/2)
#                     shelf_label.start_y(value = 0)
#                     shelf_label.start_z(value = math.fabs(assembly.obj_z.location.z))
#                     shelf_label.set_label("ADJ")

            # DOOR HEIGHT LABEL
            # fill opening for doors is weird and to make use of hole number
            # we need to look for the nearest match if it's under a 0.25 inch tolerance.
            # if it is beyond the tolerance it will be labeled as decimal.
            #
            # We also label the doors once, if there is a left and right door, labeling the right one
            # To find if a door is left or right you look at it's assembly depth (VPDIMY)
            if props.is_door_bp and scene_props.door_face_height:
                doors_toggles = {"left": False, "right": False}

                for obj in assembly.obj_bp.parent.children:
                    if obj.lm_closets.is_door_bp:
                        door_depth = 0
                        door_exists = False
                        for n_obj in obj.children:
                            if n_obj.mv.type == 'VPDIMY':
                                door_depth = n_obj.location[1]
                            if not n_obj.hide:
                                door_exists = True
                        if door_exists and door_depth < 0:
                            doors_toggles["left"] = True
                        elif door_exists and door_depth > 0:
                            doors_toggles["right"] = True

                is_right_door = [
                    obj.location[1] > 0 for obj in assembly.obj_bp.children if obj.mv.type == 'VPDIMY'][:1][0]

                label = ""
                door_size = str(
                    round(assembly.obj_x.location.x/unit.inch(1), 2))
                if door_size in common_lists.DOOR_SIZES_DICT.keys():
                    label = common_lists.DOOR_SIZES_DICT[door_size]
                else:
                    qry_result = False
                    tolerance = 0.25
                    for key, value in common_lists.DOOR_SIZES_DICT.items():
                        if abs(float(key) - float(door_size)) <= tolerance:
                            qry_result = True
                            label = value
                    if not qry_result:
                        label = str(opengl_dim.format_distance(
                            assembly.obj_x.location.x))
                dim_df_height = self.add_tagged_dimension(assembly.obj_bp)

                if doors_toggles["left"] and doors_toggles["right"] and is_right_door:
                    dim_df_height.start_x(
                        value=(assembly.obj_x.location.x/5) * 4)
                    dim_df_height.start_y(value=assembly.obj_y.location.y/2)
                    dim_df_height.set_label(label)
                if not doors_toggles["left"] or not doors_toggles["right"]:
                    dim_df_height.start_x(
                        value=(assembly.obj_x.location.x/5) * 4)
                    dim_df_height.start_y(value=assembly.obj_y.location.y/4)
                    dim_df_height.set_label(label)

            # DRAWER FRONT HEIGHT LABEL
            if props.is_drawer_front_bp and scene_props.label_drawer_front_height:
                label = common_lists.DRAWER_SIZES_DICT[str(
                    round(assembly.obj_x.location.x * 1000, 3))]
                # Check if drawer is smaller than 10H
                # One positioning for 3H to 9H and another to 10H and beyond
                if assembly.obj_x.location.x < 0.3:
                    dim_df_height = self.add_tagged_dimension(assembly.obj_bp)
                    dim_df_height.start_x(
                        value=(assembly.obj_x.location.x / 2) - unit.inch(1))
                    dim_df_height.start_y(value=assembly.obj_y.location.y / 4)
                    dim_df_height.set_label(label)
                else:
                    dim_df_height = self.add_tagged_dimension(assembly.obj_bp)
                    dim_df_height.start_x(
                        value=((assembly.obj_x.location.x / 3) * 2) - unit.inch(1))
                    dim_df_height.start_y(value=assembly.obj_y.location.y / 4)
                    dim_df_height.set_label(label)
                # dim_df_height.start_y(value = assembly.obj_y.location.y - unit.inch(5))
                # dim_df_height.start_y(value = assembly.obj_y.location.y)
                # dim_df_height.set_label(str(opengl_dim.format_distance(assembly.obj_x.location.x)))

            # HAMPER TYPE LABEL
            if props.is_hamper_insert_bp and scene_props.label_hamper_type:
                hamper_insert = fd_types.Assembly(assembly.obj_bp)
                hamper_type = hamper_insert.get_prompt("Hamper Type")
                hamper_height = hamper_insert.get_prompt("Hamper Height")

                if hamper_type and hamper_height:
                    dim_slide = self.add_tagged_dimension(assembly.obj_bp)
                    dim_slide.start_x(value=hamper_insert.obj_x.location.x/2)
                    dim_slide.start_z(value=hamper_height.value()/2)
                    dim_slide.start_y(value=unit.inch(100))
                    dim_slide.set_label("Hamper")
                    # dim_slide.set_label(hamper_type.value())

                    dim_hole_number = self.add_tagged_dimension(
                        assembly.obj_bp)
                    dim_hole_number.start_x(
                        value=(hamper_insert.obj_x.location.x/4) * 3)
                    dim_hole_number.start_z(
                        value=(hamper_height.value()/4) * 3)
                    dim_hole_number.start_y(value=unit.inch(100))
                    dim_hole_number.set_label(
                        common_lists.HAMPER_SIZES_DICT[str(round(hamper_height.value() * 1000, 3))])

        return {'FINISHED'}


class PROPS_2D_Dimensions(bpy.types.PropertyGroup):

    main_tabs = EnumProperty(name="Main Tabs",
                             items=[('GENERAL', "Defaults", 'Show the general defaults.'),
                                    ('MOLDING', "Molding",
                                     'Show the molding options.'),
                                    ('DOORS', "Doors and Drawers",
                                     'Show the wood panel style options.'),
                                    ('SHELVES', "Shelves", 'Show the hardware options.')],
                             default='GENERAL')

    auto_add_on_save = BoolProperty(name="Auto Add On Save",
                                    default=False,
                                    description="Automatically add annotations and dimensions to scene")
    
    include_accordions = BoolProperty(name="Incl. Accordions",
                                      default=False,
                                      description="Include Accordion Elevations on 2D Views")

    # General
    ceiling_height = BoolProperty(name="Add Ceiling Height",
                                  default=True,
                                  description="")

    countertop = BoolProperty(name="Add Countertops",
                              default=True,
                              description="")

    ct_overhang = BoolProperty(name="Add CT Overhang",
                               default=True,
                               description = "Annotate Countertop Overhang")

    filler = BoolProperty(name="Add Fillers",
                          default=True,
                          description="")

    framing_height = BoolProperty(name="Add Framing Height",
                                  default=True,
                                  description="")

    fullback = BoolProperty(name="Add Fullback",
                            default=True,
                            description="")

    kds = BoolProperty(name="Add KD\'s",
                       default=True,
                       description="")

    partition_height = BoolProperty(name="Add Partition Height",
                                    default=True,
                                    description="")

    partition_depths = BoolProperty(name="Add Partition Depths",
                                    default=True,
                                    description="")

    section_depths = BoolProperty(name="Add Section Depths",
                                  default=True,
                                  description="Add to each opening it\'s section depth")

    section_widths = BoolProperty(name="Add Section Widths",
                                  default=True,
                                  description="This will add an section width dimensions to the elevation")

    toe_kick_height = BoolProperty(name="Add Toe Kick Heights",
                                   default=True,
                                   description="")

    top_shelf_depth = BoolProperty(name="Add Top Shelf Depth",
                                   default=True,
                                   description="")

    variable = BoolProperty(name="Add Variable Openings",
                            default=True,
                            description="")

    # add_closet_height = BoolProperty(name="Add Closet Height",
    #                                  default=True,
    #                                  description="This will add an annotation to the elevation for the closet height")
    # label_adj_shelves = BoolProperty(name="Add Label Adj Shelves",
    #                                  default=True,
    #                                  description="This will label each adj shelf with ADJ")
    # number_closet_sections = BoolProperty(name="Add Number Closet Sections",
    #                                       default=True,
    #                                       description="This will number each closet section on the wall")
    # add_panel_height = BoolProperty(name="Add Panel Height",
    #                                 default=True,
    #                                 description="This will add an annotation to the elevation for the panel height")
    # add_section_numbers = BoolProperty(name="Add Section Numbers",
    #                                 default=True,
    #                                 description="This will add a section number to the elevation")
    # label_lock_shelves = BoolProperty(name="Add Label Lock Shelves",
    #                                   default=True,
    #                                   description="This will label each lock shelf with LS")

    # Shelves

    l_shelves = BoolProperty(name="Add L Shelves",
                             default=True,
                             description="")

    corner_shelves = BoolProperty(name="Add Corner Shelves",
                                  default=True,
                                  description="")

    glass_shelves = BoolProperty(name="Add Glass Shelves",
                                 default=True,
                                 description="")

    shelf_setback = BoolProperty(name="Add Shelves Setback",
                                 default=True,
                                 description="")

    slanted_shoe_shelves = BoolProperty(name="Add Slanted Shoe Shelves",
                                        default=True,
                                        description="")

    # Doors and Drawers
    door_face_height = BoolProperty(name="Add Door Face Height",
                                    default=True,
                                    description="This will put the door height at the top right of the door")

    label_drawer_front_height = BoolProperty(name="Add Drawer Face Height",
                                             default=True,
                                             description="This will put the door height at the bottom of the door")

    file_drawers = BoolProperty(name="Add File Drawers",
                                default=True,
                                description="This will label file drawers ")

    label_hamper_type = BoolProperty(name="Add Hamper",
                                     default=True,
                                     description="This will label the type of hamper that is used")

    double_jewelry = BoolProperty(name="Add Double Jewelry Drawers",
                                  default=True,
                                  description="This will label double jewelry drawers ")

    locks = BoolProperty(name="Add Locks",
                         default=True,
                         description="This will label the type of hamper that is used")

    # drawer_face_height = BoolProperty(name="Add Drawer Face Height",
    #                                default=True,
    #                                description="")
    # hampers = BoolProperty(name="Add Hampers",
    #                                default=True,
    #                                description="")

    # Molding
    capping_bottom = BoolProperty(name="Add Capping Bottom",
                                  default=True,
                                  description="")

    flat_crown = BoolProperty(name="Add Flat Crown",
                              default=True,
                              description="")

    blind_corner_panel_labels = BoolProperty(name="Add Blind Corner Panels",
                                             default=True,
                                             description="")

    light_rails = BoolProperty(name="Add Light Rails",
                               default=True,
                               description="")

    valances = BoolProperty(name="Add Valance",
                            default=True,
                            description="")

    # traditional_crown = BoolProperty(name="Add Traditional Crown",
    #                                default=True,
    #                                description="")

    def draw_general_options(self, layout):
        general_box = layout.box()
        general_box.prop(self, 'blind_corner_panel_labels')
        general_box.prop(self, 'ceiling_height')
        general_box.prop(self, 'countertop')
        general_box.prop(self, 'ct_overhang')
        general_box.prop(self, 'filler')
        general_box.prop(self, 'framing_height')
        general_box.prop(self, 'fullback')
        general_box.prop(self, 'partition_depths')
        general_box.prop(self, 'partition_height')
        general_box.prop(self, 'section_depths')
        general_box.prop(self, 'section_widths')
        general_box.prop(self, 'toe_kick_height')
        general_box.prop(self, 'variable')
        # general_box.prop(self, 'add_panel_height')
        # general_box.prop(self, 'add_closet_height')

    def draw_molding_options(self, layout):
        molding_box = layout.box()
        molding_box.prop(self, 'flat_crown')
        molding_box.prop(self, 'light_rails')
        molding_box.prop(self, 'valances')
        # molding_box.prop(self, 'traditional_crown')

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
        shelves_box.prop(self, 'kds')
        shelves_box.prop(self, 'l_shelves')
        shelves_box.prop(self, 'shelf_setback')
        shelves_box.prop(self, 'slanted_shoe_shelves')
        shelves_box.prop(self, 'top_shelf_depth')

    def draw(self, layout):
        main_box = layout.box()

        box = layout.box()
        row = main_box.row(align=True)
        row.scale_y = 1.3
        row.operator(DIMENSION_PROPERTY_NAMESPACE +
                     ".auto_dimension", icon='FILE_TICK')
        row.menu('MENU_label_option',
                 text="", icon='DOWNARROW_HLT')
        row = main_box.row(align=True)
        row.prop(self, 'auto_add_on_save', text="Auto Add on Save")
        row.prop(self, 'include_accordions', text="Include Accordions")
        # row.operator(DIMENSION_PROPERTY_NAMESPACE +
        #              ".remove_labels", icon='X')

        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "main_tabs", 'GENERAL',
                      icon='SCRIPTWIN',  text="General Dimensions")
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


bpy.utils.register_class(PROPS_2D_Dimensions)


class PROPS_Object_2D_Dimensions(bpy.types.PropertyGroup):

    is_dim_obj = BoolProperty(name="Is Dimension Object",
                              default=False,
                              description="This determines if the object is a dimension object")


bpy.utils.register_class(PROPS_Object_2D_Dimensions)


class PANEL_Closet_2D_Setup(bpy.types.Panel):
    bl_idname = DIMENSION_PROPERTY_NAMESPACE + "Closet_Price"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Closet 2D Setup"
    bl_category = "SNaP"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        layout.label('', icon='BLANK1')

    def draw(self, context):
        props = get_dimension_props()
        props.draw(self.layout)


exec("bpy.types.Scene." + DIMENSION_PROPERTY_NAMESPACE +
     "= PointerProperty(type = PROPS_2D_Dimensions)")
exec("bpy.types.Object." + DIMENSION_PROPERTY_NAMESPACE +
     "= PointerProperty(type = PROPS_Object_2D_Dimensions)")

# AUTO CALL OPERATOR ON SAVE


@ bpy.app.handlers.persistent
def add_annotations_and_dimensions(scene=None):
    props = get_dimension_props()
    if props.auto_add_on_save:
        print('AUTOADDDIMS', "bpy.ops." +
              DIMENSION_PROPERTY_NAMESPACE + ".auto_dimension")
        exec("bpy.ops." + DIMENSION_PROPERTY_NAMESPACE + ".auto_dimension()")


bpy.app.handlers.save_pre.append(add_annotations_and_dimensions)

bpy.utils.register_class(PANEL_Closet_2D_Setup)
bpy.utils.register_class(OPERATOR_Auto_Dimension)
bpy.utils.register_class(OPERATOR_Cleanup)
bpy.utils.register_class(OPERATOR_Select_All)
bpy.utils.register_class(OPERATOR_Deselect_All)
bpy.utils.register_class(MENU_label_option)
