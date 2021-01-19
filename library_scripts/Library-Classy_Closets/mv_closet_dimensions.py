"""
Microvellum 
Cabinet & Closet Designer
Stores the UI, Properties, and Operators for the cabinet and closet designer panel
the Panel definition is stored in an add-on.
"""

import bpy
import math
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

    def clean_up_scene(self, context):
        label_list = []

        for obj in context.scene.objects:
            props = get_object_dimension_props(obj)
            if props.is_dim_obj:
                label_list.append(obj)

        utils.delete_obj_list(label_list)

    def add_panel_height_annotation(self, assembly):
        dim_from_floor = assembly.obj_bp.matrix_world[2][3]

        dim = self.add_dimension(assembly.obj_bp)
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

        if scene_props.add_closet_height:
            height = self.add_dimension(product.obj_bp)
            height.start_x(value=unit.inch(-6))
            height.end_z(value=-product.obj_bp.location.z)

            height = self.add_dimension(product.obj_bp)
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

                    if scene_props.add_section_widths:
                        section_width = self.add_dimension(closet.obj_bp)
                        section_width.start_x(value=x_loc)
                        section_width.end_x(value=opening_width.value())
                        section_width.start_z(value=- unit.inch(4))

                    # if scene_props.add_section_numbers:
                    #     print("ADDING SECTION NUMBER FOR OPENING",closet_bp)
                    #     section_number = self.add_dimension(closet.obj_bp)
                    #     section_number.start_x(value = x_loc + (opening_width.value()/2))
                    #     section_number.start_z(value = - unit.inch(12))
                    #     section_number.set_label(str(section_number_text))

                    if scene_props.add_closet_height:
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

                if scene_props.add_section_widths:
                    width = self.add_dimension(closet.obj_bp)
                    width.start_x(value=panel_thickness.value())
                    width.end_x(value=closet.obj_x.location.x -
                                panel_thickness.value()*2)
                    width.start_z(value=- dim_from_floor - unit.inch(4))

                # if scene_props.add_section_numbers:
                #     section_number = self.add_dimension(closet.obj_bp)
                #     section_number.start_x(value = x_loc + (closet.obj_x.location.x/2))
                #     section_number.start_z(value = - dim_from_floor - unit.inch(12))
                #     section_number.set_label(str(section_number_text))

                if scene_props.add_closet_height:
                    height = self.add_dimension(closet.obj_bp)
                    height.start_x(value=unit.inch(-6))
                    height.end_z(value=-closet.obj_bp.location.z)

                    height = self.add_dimension(closet.obj_bp)
                    height.start_x(value=unit.inch(-6))
                    height.end_z(value=-closet.obj_bp.location.z)

                section_number_text += 1

    def execute(self, context):
        self.clean_up_scene(context)
        scene_props = get_dimension_props()

        # Set Panel Numbers
#         for wall_bp in common_closet_utils.scene_walls(context):
#             panels = self.get_wall_panels(wall_bp) #GET SORTED LIST OF PANELS
#             for i , panel_bp in enumerate(panels):
#                 panel_bp.mv.opening_name = str(i + 1)
#                 panel_bp.mv.comment_2 = str(i + 1)

        # Set Closet Product Annotations
        for wall_bp in common_closet_utils.scene_walls(context):
            closet_products = self.get_wall_products(wall_bp)
            self.add_closet_annotations(closet_products)

        # Add Part Annotations
        for assembly in common_closet_utils.scene_assemblies(context):

            props = props_closet.get_object_props(assembly.obj_bp)

            if props.is_panel_bp:
                if scene_props.add_panel_height:
                    self.add_panel_height_annotation(assembly)
#             else:
#                 if assembly.obj_bp.mv.opening_name != "":
#                     self.set_section_number(assembly)

            # FIXED SHELF AND ROD ANNOTATIONS
#             if props.is_fixed_shelf_and_rod_product_bp:
#                 self.add_fixed_shelf_and_rod_annotations(assembly)

            # SHELF LABEL
            if props.is_shelf_bp:
                is_locked_shelf = assembly.get_prompt("Is Locked Shelf")

                if is_locked_shelf and is_locked_shelf.value() and scene_props.label_lock_shelves:
                    shelf_label = self.add_dimension(assembly.obj_bp)
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
            if props.is_door_bp and scene_props.label_door_height:
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
                dim_df_height = self.add_dimension(assembly.obj_bp)

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
                    dim_df_height = self.add_dimension(assembly.obj_bp)
                    dim_df_height.start_x(
                        value=(assembly.obj_x.location.x / 2) - unit.inch(1))
                    dim_df_height.start_y(value=assembly.obj_y.location.y / 4)
                    dim_df_height.set_label(label)
                else:
                    dim_df_height = self.add_dimension(assembly.obj_bp)
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
                    dim_slide = self.add_dimension(assembly.obj_bp)
                    dim_slide.start_x(value=hamper_insert.obj_x.location.x/2)
                    dim_slide.start_z(value=hamper_height.value()/2)
                    dim_slide.start_y(value=unit.inch(100))
                    dim_slide.set_label("Hamper")
                    # dim_slide.set_label(hamper_type.value())

                    dim_hole_number = self.add_dimension(assembly.obj_bp)
                    dim_hole_number.start_x(
                        value=(hamper_insert.obj_x.location.x/4) * 3)
                    dim_hole_number.start_z(
                        value=(hamper_height.value()/4) * 3)
                    dim_hole_number.start_y(value=unit.inch(100))
                    dim_hole_number.set_label(
                        common_lists.HAMPER_SIZES_DICT[str(round(hamper_height.value() * 1000, 3))])

        return {'FINISHED'}


class PROPS_2D_Dimensions(bpy.types.PropertyGroup):

    auto_add_on_save = BoolProperty(name="Auto Add On Save",
                                    default=False,
                                    description="Automatically add annotations and dimensions to scene")

    add_panel_height = BoolProperty(name="Add Panel Height",
                                    default=True,
                                    description="This will add an annotation to the elevation for the panel height")

    add_section_widths = BoolProperty(name="Add Section Widths",
                                      default=True,
                                      description="This will add an section width dimensions to the elevation")

    # add_section_numbers = BoolProperty(name="Add Section Numbers",
    #                                 default=True,
    #                                 description="This will add a section number to the elevation")

    add_closet_height = BoolProperty(name="Add Closet Height",
                                     default=True,
                                     description="This will add an annotation to the elevation for the closet height")

    label_door_height = BoolProperty(name="Label Door Height",
                                     default=True,
                                     description="This will put the door height at the bottom of the door")

    label_drawer_front_height = BoolProperty(name="Label Drawer Front Height",
                                             default=True,
                                             description="This will put the door height at the bottom of the door")

    label_lock_shelves = BoolProperty(name="Label Lock Shelves",
                                      default=True,
                                      description="This will label each lock shelf with LS")

    label_adj_shelves = BoolProperty(name="Label Adj Shelves",
                                     default=True,
                                     description="This will label each adj shelf with ADJ")

    label_hamper_type = BoolProperty(name="Label Hamper Type",
                                     default=True,
                                     description="This will label the type of hamper that is used")

    number_closet_sections = BoolProperty(name="Number Closet Sections",
                                          default=True,
                                          description="This will number each closet section on the wall")

    def draw(self, layout):
        main_box = layout.box()

        row = main_box.row()
        row.scale_y = 1.3
        row.operator(DIMENSION_PROPERTY_NAMESPACE +
                     ".auto_dimension", icon='FILE_TICK')
        row.prop(self, 'auto_add_on_save', text="Auto Add on Save")

        main_col = main_box.column(align=True)

        box = main_col.box()
        box.label("General:")
        # box.prop(self,'add_section_numbers')
        box.prop(self, 'add_panel_height')
        box.prop(self, 'add_closet_height')
        box.prop(self, 'add_section_widths')

        box = main_col.box()
        box.label("Doors and Drawers:")
        box.prop(self, 'label_door_height')
        box.prop(self, 'label_drawer_front_height')
        box.prop(self, 'label_hamper_type')

        box = main_col.box()
        box.label("Shelves:")
        box.prop(self, 'label_lock_shelves')
        box.prop(self, 'label_adj_shelves')


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


@bpy.app.handlers.persistent
def add_annotations_and_dimensions(scene=None):
    props = get_dimension_props()
    if props.auto_add_on_save:
        print('AUTOADDDIMS', "bpy.ops." +
              DIMENSION_PROPERTY_NAMESPACE + ".auto_dimension")
        exec("bpy.ops." + DIMENSION_PROPERTY_NAMESPACE + ".auto_dimension()")


bpy.app.handlers.save_pre.append(add_annotations_and_dimensions)

bpy.utils.register_class(PANEL_Closet_2D_Setup)
bpy.utils.register_class(OPERATOR_Auto_Dimension)
