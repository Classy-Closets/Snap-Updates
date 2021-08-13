import math

import os

import bpy

from bpy.types import Operator
from snap import sn_types, sn_unit, sn_utils
from ..common import common_parts
from ..common import common_lists
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props


class Vertical_Splitters(sn_types.Assembly):

    type_assembly = "INSERT"
    id_prompt = "sn_closets.vertical_splitters"
    drop_id = "sn_closets.insert_vertical_splitters_drop"
    placement_type = "SPLITTER"
    show_in_library = True
    category_name = "Closet Products - Shelves"
    mirror_y = False
    calculator = None

    def add_prompts(self):
        for i in range(1, 17):  # 16 Openings
            self.add_prompt("Opening " + str(i) + " Height", 'DISTANCE', sn_unit.millimeter(76.962))
        for i in range(1, 16):  # 15 Shelves
            self.add_prompt("Shelf " + str(i) + " Setback", 'DISTANCE', 0)

        self.add_prompt("Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Left Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Right Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Top Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Bottom Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Extend Top Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Extend Bottom Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Remove Bottom Shelf", 'CHECKBOX', True)
        self.add_prompt("Shelf Quantity", 'QUANTITY', 5)
        self.add_prompt("Evenly Spaced Shelves", 'CHECKBOX', True)
        self.add_prompt("Shelf Backing Setback", 'DISTANCE', 0)
        self.add_prompt("Parent Has Bottom KD", 'CHECKBOX', False)
        self.add_prompt('Hide', 'CHECKBOX', False)

    def add_insert(self, insert, index, z_loc_vars=[], z_loc_expression=""):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        open_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Height')".format(str(index)))
        open_var = eval("open_prompt.get_var(self.calculator.name, 'Opening_{}_Height')".format(str(index)))
        z_dim_expression = "Opening_" + str(index) + "_Height"

        if insert:
            if not insert.obj_bp:
                insert.draw()
            insert.obj_bp.parent = self.obj_bp

            if index == self.vertical_openings:
                insert.loc_z(z_loc_expression, z_loc_vars)

            insert.dim_x('Width', [Width])
            insert.dim_y('Depth', [Depth])
            insert.dim_z(z_dim_expression, [open_var])

            if index == 1:
                # ALLOW DOOR TO EXTEND TO TOP OF VALANCE
                extend_top_amount = insert.get_prompt("Extend Top Amount")
                if extend_top_amount:
                    Extend_Top_Amount = self.get_prompt("Extend Top Amount")
                    Extend_Top_Amount.set_formula('Extend_Top_Amount', [Extend_Top_Amount])

            if index == self.vertical_openings:
                # ALLOW DOOR TO EXTEND TO BOTTOM OF VALANCE
                extend_bottom_amount = insert.get_prompt("Extend Bottom Amount")
                if extend_bottom_amount:
                    Extend_Bottom_Amount = self.get_prompt("Extend Bottom Amount")
                    Extend_Bottom_Amount.set_formula('Extend_Bottom_Amount', [Extend_Bottom_Amount])

    def get_opening(self, index):
        opening = common_parts.add_opening(self)
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))

        if interior:
            opening.obj_bp.snap.interior_open = False

        if exterior:
            opening.obj_bp.snap.exterior_open = False

        return opening

    def add_splitters(self):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Thickness = self.get_prompt('Thickness').get_var("Thickness")
        Remove_Bottom_Shelf = self.get_prompt('Remove Bottom Shelf').get_var("Remove_Bottom_Shelf")
        Shelf_Quantity = self.get_prompt('Shelf Quantity').get_var("Shelf_Quantity")
        Shelf_Backing_Setback = self.get_prompt('Shelf Backing Setback').get_var("Shelf_Backing_Setback")
        Parent_Has_Bottom_KD = self.get_prompt('Parent Has Bottom KD').get_var("Parent_Has_Bottom_KD")
        parent_hide = self.get_prompt('Hide').get_var()
        previous_splitter = None

        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.loc_y('Depth', [Depth])

        bottom_shelf.dim_x('Width', [Width])
        bottom_shelf.dim_y('-Depth', [Depth])
        bottom_shelf.dim_z('-Thickness', [Thickness])
        hide = bottom_shelf.get_prompt("Hide")
        hide.set_formula('IF(Parent_Has_Bottom_KD,True,IF(Remove_Bottom_Shelf,True,False)) or Hide', [Remove_Bottom_Shelf, Parent_Has_Bottom_KD, parent_hide])
        is_locked_shelf = bottom_shelf.get_prompt("Is Locked Shelf")
        is_locked_shelf.set_value(True)

        for i in range(1, 16):
            Opening_Height = self.get_prompt("Opening " + str(i) + " Height").get_var("Opening_Height")

            if previous_splitter:
                Previous_Z_Loc = previous_splitter.obj_bp.snap.get_var("location.z", "Previous_Z_Loc")

            splitter = common_parts.add_shelf(self)
            Is_Locked_Shelf = splitter.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
            Adj_Shelf_Setback = splitter.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
            Locked_Shelf_Setback = splitter.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
            Adj_Shelf_Clip_Gap = splitter.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')
            Shelf_Setback = self.get_prompt("Shelf " + str(i) + " Setback").get_var('Shelf_Setback')

            splitter.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
            splitter.loc_y('Depth-Shelf_Backing_Setback', [Depth, Shelf_Backing_Setback])
            if previous_splitter:
                splitter.loc_z('Previous_Z_Loc+Opening_Height', [Opening_Height, Previous_Z_Loc])
            else:
                splitter.loc_z('Opening_Height+INCH(0.58)', [Opening_Height])

            splitter.dim_x(
                'Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
            splitter.dim_y(
                '-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Shelf_Setback+Shelf_Backing_Setback',
                [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, Shelf_Setback, Shelf_Backing_Setback])
            splitter.dim_z('-Thickness', [Thickness])
            splitter.get_prompt("Hide").set_formula('IF(Shelf_Quantity+1>' + str(i) + ',False,True) or Hide', [Shelf_Quantity, parent_hide])

            opening = common_parts.add_opening(self)
            opening.obj_bp.sn_closets.opening_name = str(i)
            opening.loc_x(value=0)
            opening.loc_y(value=0)
            if previous_splitter:
                opening_z_loc = previous_splitter.obj_bp.snap.get_var("location.z", "opening_z_loc")
                opening.loc_z('opening_z_loc', [opening_z_loc])
                opening.dim_z('Opening_Height-Thickness', [Opening_Height, Thickness])
            else:
                opening.loc_z(value=0)
                opening.dim_z('Opening_Height-Thickness+INCH(0.58)', [Opening_Height, Thickness])
            opening.dim_x('Width', [Width])
            opening.dim_y('Depth', [Depth])
            previous_splitter = splitter

    def update(self):
        super().update()
        self.obj_bp.snap.export_as_subassembly = True

        self.obj_bp['IS_BP_SPLITTER'] = True
        props = self.obj_bp.sn_closets
        props.is_splitter_bp = True  # TODO: remove

        # calculator = self.get_calculator('Opening Heights')
        # if calculator:
        #     calculator.calculate()
        #     bpy.context.area.tag_redraw()

    def draw(self):
        self.create_assembly()
        self.add_prompts()
        self.add_splitters()
        self.update()

    # def draw(self):
    #     calculator = self.get_calculator('Opening Heights')
    #     if calculator:
    #         calculator.calculate()
    #         bpy.context.area.tag_redraw()


class Horizontal_Splitters(sn_types.Assembly):

    type_assembly = "INSERT"
    id_prompt = "sn_closets.horizontal_splitters"
    drop_id = "sn_closets.drop_insert"
    placement_type = "SPLITTER"
    show_in_library = True
    category_name = "Closet Products - Shelves"
    mirror_y = False
    calculator = None

    ''' Number of openings to create for this splitter
    '''
    horizontal_openings = 2  # 1-10

    ''' Override the default width for the openings
        0 will make the opening calculate equally
    '''
    opening_1_width = 0
    opening_2_width = 0
    opening_3_width = 0
    opening_4_width = 0
    opening_5_width = 0
    opening_6_width = 0
    opening_7_width = 0
    opening_8_width = 0
    opening_9_width = 0
    opening_10_width = 0

    ''' sn_types.Assembly to put into the interior
        or exterior of the opening
    '''
    interior_1 = None
    exterior_1 = None
    interior_2 = None
    exterior_2 = None
    interior_3 = None
    exterior_3 = None
    interior_4 = None
    exterior_4 = None
    interior_5 = None
    exterior_5 = None
    interior_6 = None
    exterior_6 = None
    interior_7 = None
    exterior_7 = None
    interior_8 = None
    exterior_8 = None
    interior_9 = None
    exterior_9 = None
    interior_10 = None
    exterior_10 = None
    interior_11 = None
    exterior_11 = None

    def add_prompts(self):
        calc_distance_obj = self.add_empty('Calc Distance Obj')
        calc_distance_obj.empty_display_size = .001
        self.add_prompt("Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.calculator = self.obj_prompts.snap.add_calculator(
            "Opening Widths",
            calc_distance_obj)

        for i in range(1, self.horizontal_openings + 1):
            size = eval("self.opening_" + str(i) + "_width")
            calc_prompt = self.calculator.add_calculator_prompt("Opening " + str(i) + " Width")
            calc_prompt.equal = True if size == 0 else False

        Thickness = self.get_prompt('Thickness').get_var()
        width = self.obj_x.snap.get_var('location.x', 'width')
        self.calculator.set_total_distance(
            "width-Thickness*(" + str(self.horizontal_openings) + "-1)",
            [width, Thickness])

    def add_insert(self, insert, index, x_loc_vars=[], x_loc_expression=""):
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        open_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(index)))
        open_var = eval("open_prompt.get_var(self.calculator.name, 'Opening_{}_Width')".format(str(index)))
        x_dim_expression = "Opening_" + str(index) + "_Width"

        if insert:
            if not insert.obj_bp:
                insert.draw()

            insert.obj_bp.parent = self.obj_bp
            if index == 1:
                insert.loc_x(value=0)
            else:
                insert.loc_x(x_loc_expression, x_loc_vars)

            insert.dim_x(x_dim_expression, [open_var])
            insert.dim_y('Depth',[Depth])
            insert.dim_z('Height',[Height])

    def get_opening(self, index):
        opening = common_parts.add_opening(self)
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))

        if interior:
            opening.obj_bp.snap.interior_open = False

        if exterior:
            opening.obj_bp.snap.exterior_open = False

        return opening

    def add_splitters(self):
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Thickness = self.get_prompt('Thickness').get_var()
        previous_splitter = None

        for i in range(1, self.horizontal_openings):
            x_loc_vars = []
            open_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
            open_var = eval("open_prompt.get_var(self.calculator.name, 'Opening_{}_Width')".format(str(i)))
            x_loc_vars.append(open_var)

            if previous_splitter:
                x_loc = previous_splitter.obj_bp.snap.get_var("location.x", "Splitter_X_Loc")
                x_loc_vars.append(x_loc)
                x_loc_vars.append(Thickness)

            splitter = common_parts.add_division(self)
            if previous_splitter:
                splitter.loc_x("Splitter_X_Loc+Thickness+Opening_" + str(i) + "_Width",x_loc_vars)
            else:
                splitter.loc_x("Opening_" + str(i) + "_Width",[open_var])

            splitter.loc_y('Depth', [Depth])
            splitter.rot_y(value=math.radians(-90))
            splitter.dim_x('Height', [Height])
            splitter.dim_y('-Depth', [Depth])
            splitter.dim_z('-Thickness', [Thickness])

            previous_splitter = splitter

            exterior = eval('self.exterior_' + str(i))
            self.add_insert(exterior, i, x_loc_vars, "Splitter_X_Loc+Thickness")

            interior = eval('self.interior_' + str(i))
            self.add_insert(interior, i, x_loc_vars, "Splitter_X_Loc+Thickness")

            opening = self.get_opening(i)
            self.add_insert(opening, i, x_loc_vars, "Splitter_X_Loc+Thickness")

        insert_x_loc_vars = []
        insert_x_loc = previous_splitter.obj_bp.snap.get_var("location.x", "Splitter_X_Loc")
        insert_x_loc_vars.append(insert_x_loc)
        insert_x_loc_vars.append(Thickness)

        # ADD LAST INSERT
        last_exterior = eval('self.exterior_' + str(self.horizontal_openings))
        self.add_insert(last_exterior, self.horizontal_openings, insert_x_loc_vars, "Splitter_X_Loc+Thickness")

        last_interior = eval('self.interior_' + str(self.horizontal_openings))
        self.add_insert(last_interior, self.horizontal_openings, insert_x_loc_vars, "Splitter_X_Loc+Thickness")

        last_opening = self.get_opening(self.horizontal_openings)
        self.add_insert(last_opening, self.horizontal_openings, insert_x_loc_vars, "Splitter_X_Loc+Thickness")

    def update(self):
        super().update()
        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp['IS_BP_SPLITTER'] = True
        props = self.obj_bp.sn_closets
        props.is_splitter_bp = True  # TODO: remove

    def pre_draw(self):
        self.create_assembly()
        self.add_prompts()
        self.add_splitters()
        self.update()


class PROMPTS_Vertical_Splitter_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.vertical_splitters"
    bl_label = "Shelf Prompts"
    bl_description = "This shows all of the available vertical splitter options"
    bl_options = {'UNDO'}

    object_name: bpy.props.StringProperty(name="Object Name")

    Opening_1_Height: bpy.props.EnumProperty(name="Opening 1 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_2_Height: bpy.props.EnumProperty(name="Opening 2 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_3_Height: bpy.props.EnumProperty(name="Opening 3 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_4_Height: bpy.props.EnumProperty(name="Opening 4 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_5_Height: bpy.props.EnumProperty(name="Opening 5 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_6_Height: bpy.props.EnumProperty(name="Opening 6 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_7_Height: bpy.props.EnumProperty(name="Opening 7 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_8_Height: bpy.props.EnumProperty(name="Opening 8 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_9_Height: bpy.props.EnumProperty(name="Opening 9 Height",
                                             items=common_lists.OPENING_HEIGHTS)

    Opening_10_Height: bpy.props.EnumProperty(name="Opening 10 Height",
                                              items=common_lists.OPENING_HEIGHTS)

    Opening_11_Height: bpy.props.EnumProperty(name="Opening 11 Height",
                                              items=common_lists.OPENING_HEIGHTS)

    Opening_12_Height: bpy.props.EnumProperty(name="Opening 12 Height",
                                              items=common_lists.OPENING_HEIGHTS)

    Opening_13_Height: bpy.props.EnumProperty(name="Opening 13 Height",
                                              items=common_lists.OPENING_HEIGHTS)

    Opening_14_Height: bpy.props.EnumProperty(name="Opening 14 Height",
                                              items=common_lists.OPENING_HEIGHTS)

    Opening_15_Height: bpy.props.EnumProperty(name="Opening 15 Height",
                                              items=common_lists.OPENING_HEIGHTS)

    Opening_16_Height: bpy.props.EnumProperty(name="Opening 16 Height",
                                              items=common_lists.OPENING_HEIGHTS)

    shelf_quantity: bpy.props.EnumProperty(name="Shelf Quantity",
                                           items=[('1', "1", '1'),
                                                  ('2', "2", '2'),
                                                  ('3', "3", '3'),
                                                  ('4', "4", '4'),
                                                  ('5', "5", '5'),
                                                  ('6', "6", '6'),
                                                  ('7', "7", '7'),
                                                  ('8', "8", '8'),
                                                  ('9', "9", '9'),
                                                  ('10', "10", '10'),
                                                  ('11', "11", '11'),
                                                  ('12', "12", '12'),
                                                  ('13', "13", '13'),
                                                  ('14', "14", '14'),
                                                  ('15', "15", '15')],
                                           default='5')

    assembly = None
    cur_shelf_height = None

    def check(self, context):
        self.update_openings()
        self.set_prompts_from_properties()

        opening = self.assembly.obj_bp.sn_closets.opening_name
        parent_obj = self.assembly.obj_bp.parent
        parent_assembly = sn_types.Assembly(parent_obj)
        parent_remove_bottom_shelf = parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(opening))
        floor = parent_assembly.get_prompt("Opening " + str(opening) + " Floor Mounted")
        remove_bottom_shelf = self.assembly.get_prompt("Remove Bottom Shelf")
        parent_has_bottom_kd = self.assembly.get_prompt("Parent Has Bottom KD")
        prompts = [parent_remove_bottom_shelf, remove_bottom_shelf, floor, parent_has_bottom_kd]

        if all(prompts):
            parent_has_bottom_kd.set_value(True)
            if floor.get_value():
                remove_bottom_shelf.set_value(False)
            elif remove_bottom_shelf.get_value():
                parent_remove_bottom_shelf.set_value(False)
            else:
                parent_remove_bottom_shelf.set_value(True)

        sn_utils.run_calculators(self.assembly.obj_bp)
        closet_props.update_render_materials(self, context)
        return True

    def update_openings(self):
        '''This should be called in the check function before set_prompts_from_properties
           updates which openings are available based on the value of shelf_quantity
        '''
        shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
        if (shelf_quantity):
            if shelf_quantity.get_value() != int(self.shelf_quantity):
                for child in self.assembly.obj_bp.children:
                    if child.snap.type_group == 'OPENING':
                        if int(child.sn_closets.opening_name) > int(self.shelf_quantity) + 1:
                            child.snap.interior_open = False
                            child.snap.exterior_open = False
                        else:
                            shares_location = False
                            for cchild in self.assembly.obj_bp.children:
                                if cchild.snap.type_group != 'OPENING':
                                    if cchild.location == child.location:
                                        shares_location = True
                            if not shares_location:
                                child.snap.interior_open = True
                                child.snap.exterior_open = True

    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''
        shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
        if shelf_quantity:
            shelf_quantity.set_value(int(self.shelf_quantity))
        carcass_height = self.assembly.obj_z.location.z
        height_prompt = sn_types.Assembly(self.assembly.obj_bp.parent).get_prompt("Opening " + self.assembly.obj_bp.sn_closets.opening_name + " Height")
        if height_prompt:
            carcass_height = height_prompt.get_value()
        evenly_spaced_shelves = self.assembly.get_prompt("Evenly Spaced Shelves")
        prompts = [evenly_spaced_shelves]

        for i in range(1, int(self.shelf_quantity) + 2):
            opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
            if opening:
                exec("self.cur_shelf_height = float(self.Opening_" + str(i) + "_Height)/1000")  # If Shelf was Just Moved
                if(sn_unit.meter_to_inch(opening.get_value()) != sn_unit.meter_to_inch(self.cur_shelf_height)):
                    # Get the height of the previous shelves
                    total_shelf_height = 0
                    for ii in range(1, i + 1):
                        exec("self.cur_shelf_height = float(self.Opening_" + str(ii) + "_Height)/1000")
                        total_shelf_height = total_shelf_height + self.cur_shelf_height

                    # Adjust All Shelves above shelf that was just moved to evenly space themselves in the remaining space
                    for iii in range(i + 1, int(self.shelf_quantity) + 2):
                        next_opening = self.assembly.get_prompt("Opening " + str(iii) + " Height")
                        if all(prompts):
                            if(not evenly_spaced_shelves.get_value()):
                                hole_count = 0
                                hole_count = math.ceil(((carcass_height - total_shelf_height) * 1000) / 32)
                                holes_per_shelf = round(hole_count / (int(self.shelf_quantity) + 1 - i))
                                if(holes_per_shelf >= 3):
                                    next_opening.set_value(float(common_lists.OPENING_HEIGHTS[holes_per_shelf - 3][0]) / 1000)
                                    exec("self.Opening_" + str(iii) + "_Height = common_lists.OPENING_HEIGHTS[holes_per_shelf-3][0]")
                                else:
                                    next_opening.set_value(float(common_lists.OPENING_HEIGHTS[0][0]) / 1000)
                                    exec("self.Opening_" + str(iii) + "_Height = common_lists.OPENING_HEIGHTS[0][0]")

                    exec("opening.set_value(sn_unit.inch(float(self.Opening_" + str(i) + "_Height) / 25.4))")

                if all(prompts):
                    if(evenly_spaced_shelves.get_value()):
                        hole_count = math.ceil((carcass_height * 1000) / 32)

                        holes_per_shelf = round(hole_count / (int(self.shelf_quantity) + 1))
                        remainder = hole_count - (holes_per_shelf * (int(self.shelf_quantity)))

                        if(i <= remainder):
                            holes_per_shelf = holes_per_shelf + 1
                        if(holes_per_shelf >= 3):
                            opening.set_value(float(common_lists.OPENING_HEIGHTS[holes_per_shelf - 3][0]) / 1000)
                            exec("self.Opening_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[holes_per_shelf-3][0]")
                        else:
                            opening.set_value(float(common_lists.OPENING_HEIGHTS[0][0]) / 1000)
                            exec("self.Opening_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[0][0]")

    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        for i in range(1, 17):
            opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
            if opening:
                value = round(opening.distance_value * 1000, 3)
                for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        exec("self.Opening_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[max(index - 1, 0)][0]")
                        break
        shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
        if shelf_quantity:
            self.shelf_quantity = str(shelf_quantity.get_value())

    def get_splitter(self, obj_bp):
        ''' Gets the splitter based on selection
        '''
        props = self.obj_bp.sn_closets
        if props.is_splitter_bp:
            return sn_types.Assembly(obj_bp)
        if obj_bp.parent:
            return self.get_splitter(obj_bp.parent)

    def invoke(self, context, event):
        self.assembly = self.get_insert()
        self.set_properties_from_prompts()

        opening = self.assembly.obj_bp.sn_closets.opening_name
        parent_obj = self.assembly.obj_bp.parent
        parent_assembly = sn_types.Assembly(parent_obj)
        parent_remove_bottom_shelf = parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(opening))
        floor = parent_assembly.get_prompt("Opening " + str(opening) + " Floor Mounted")
        remove_bottom_shelf = self.assembly.get_prompt("Remove Bottom Shelf")
        parent_has_bottom_kd = self.assembly.get_prompt("Parent Has Bottom KD")
        prompts = [parent_remove_bottom_shelf, floor, remove_bottom_shelf, parent_has_bottom_kd]

        if all(prompts):
            parent_has_bottom_kd.set_value(True)
            if floor.get_value() or parent_remove_bottom_shelf.get_value():
                remove_bottom_shelf.set_value(False)
            else:
                remove_bottom_shelf.set_value(True)

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                row = box.row()
                shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
                if shelf_quantity:
                    col = box.column(align=True)
                    row = col.row()
                    row.label(text="Qty:")
                    row.prop(self, "shelf_quantity", expand=True)
                row = box.row()
                evenly_spaced_shelves = self.assembly.get_prompt('Evenly Spaced Shelves')
                if evenly_spaced_shelves:
                    evenly_spaced_shelves.draw(box)

                for i in range(1, 17):
                    opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
                    setback = self.assembly.get_prompt("Shelf " + str(i) + " Setback")
                    if int(self.shelf_quantity) >= i:
                        if opening:
                            row = box.row()
                            row.label(text="Opening " + str(i) + " Height:")
                            if(evenly_spaced_shelves.get_value()):
                                row.label(text=str(math.ceil((opening.get_value() * 1000) / 32)) + "H-" + str(round(sn_unit.meter_to_inch(opening.get_value() + sn_unit.inch(0.58)), 3)) + '"')
                            else:
                                row.prop(self, 'Opening_' + str(i) + '_Height', text="")

                        if setback:
                            row = box.row()
                            row.label(text="Shelf " + str(i) + " Setback")
                            row.prop(setback, 'distance_value', text="")

                remove_bottom_shelf = self.assembly.get_prompt('Remove Bottom Shelf')
                if remove_bottom_shelf:
                    box.prop(remove_bottom_shelf, "checkbox_value", text=remove_bottom_shelf.name)


class PROMPTS_Horizontal_Splitter_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.horizontal_splitters"
    bl_label = "Horizontal Splitter Prompts"
    bl_description = "This shows all of the available horizontal splitter options"
    bl_options = {'UNDO'}

    object_name: bpy.props.StringProperty(name="Object Name")

    assembly = None

    def check(self, context):
        sn_utils.run_calculators(self.assembly.obj_bp)
        return True

    def get_splitter(self, obj_bp):
        ''' Gets the splitter based on selection
        '''
        props = self.obj_bp.sn_closets
        if props.is_splitter_bp:
            return sn_types.Assembly(obj_bp)
        if obj_bp.parent:
            return self.get_splitter(obj_bp.parent)        

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        self.assembly = self.get_insert()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                for i in range(1,10):
                    opening = self.assembly.get_prompt("Opening " + str(i) + " Width")
                    if opening:
                        row = box.row()
                        row.label(text="Opening " + str(i) + " Width:")
                        if opening.equal:
                            row.label(text=str(sn_unit.meter_to_active_unit(opening.distance_value)) + '"')
                            row.prop(opening,'equal',text="")
                        else:
                            row.prop(opening,'distance_value',text="")
                            row.prop(opening,'equal',text="")  


class OPERATOR_Vertical_Splitters_Drop(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.insert_vertical_splitters_drop"
    bl_label = "Custom drag and drop for vertical_splitters insert"
    bl_description = "This places a shelf stack."
    bl_options = {'UNDO'}

    insert = None

    def execute(self, context):
        self.insert = self.asset
        return super().execute(context)

    def insert_drop(self, context, event):
        bpy.ops.object.select_all(action='DESELECT')
        if self.selected_opening:
            for child in self.insert.obj_bp.children:
                if child.snap.type_group == 'OPENING':
                    if int(child.sn_closets.opening_name) >= 7:
                        child.snap.interior_open = False
                        child.snap.exterior_open = False
            for i in range(1, 6):
                hole_count = math.ceil(((self.selected_opening.obj_z.location.z + sn_unit.inch(1.5)) * 1000) / 32)
                holes_per_shelf = round(hole_count / 6)
                remainder = hole_count - (holes_per_shelf * 5)
                shelf = self.insert.get_prompt("Opening " + str(i) + " Height")
                if shelf:
                    if(i <= remainder):
                        holes_per_shelf = holes_per_shelf + 1
                    if(holes_per_shelf >= 3):
                        shelf.set_value(float(common_lists.OPENING_HEIGHTS[holes_per_shelf - 3][0]) / 1000)
                    else:
                        shelf.set_value(float(common_lists.OPENING_HEIGHTS[0][0]) / 1000)
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                context.scene.objects.active = self.insert.obj_bp

                parent_obj = self.insert.obj_bp.parent
                parent_assembly = sn_types.Assembly(parent_obj)
                parent_remove_bottom_shelf = parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(self.insert.obj_bp.sn_closets.opening_name))
                remove_bottom_shelf = self.insert.get_prompt("Remove Bottom Shelf")
                parent_has_bottom_kd = self.insert.get_prompt("Parent Has Bottom KD")
                prompts = [parent_remove_bottom_shelf, remove_bottom_shelf, parent_has_bottom_kd]
                if all(prompts):
                    parent_has_bottom_kd.set_value(True)
                    if remove_bottom_shelf.get_value():
                        parent_remove_bottom_shelf.set_value(False)
                    else:
                        parent_remove_bottom_shelf.set_value(True)

                # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
                sn_utils.run_calculators(self.insert.obj_bp)
                sn_utils.run_calculators(self.insert.obj_bp)
                # TOP LEVEL PRODUCT RECAL
                sn_utils.run_calculators(sn_utils.get_parent_assembly_bp(self.insert.obj_bp))
                sn_utils.run_calculators(sn_utils.get_parent_assembly_bp(self.insert.obj_bp))

                bpy.context.window.cursor_set('DEFAULT')

                self.assembly.obj_bp.select_set(True)
                return self.finish(context)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        self.run_asset_calculators()
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        self.reset_selection()

        if len(self.openings) == 0:
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT', message="There are no openings in this scene.")
            context.area.header_text_set(None)
            return self.cancel_drop(context)

        self.selected_point, self.selected_obj, ignore = sn_utils.get_selection_point(
            context,
            event,
            objects=self.include_objects,
            exclude_objects=self.exclude_objects)

        self.position_asset(context)

        if self.event_is_place_first_point(event) and self.selected_opening:
            self.confirm_placement(context)
            return self.finish(context)

        if self.event_is_cancel_command(event):
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return self.insert_drop(context, event)


bpy.utils.register_class(PROMPTS_Vertical_Splitter_Prompts)
bpy.utils.register_class(PROMPTS_Horizontal_Splitter_Prompts)
bpy.utils.register_class(OPERATOR_Vertical_Splitters_Drop)
