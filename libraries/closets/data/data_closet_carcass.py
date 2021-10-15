import math

import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from snap import sn_types
from snap import sn_unit
from snap import sn_utils
from snap.libraries.closets import closet_utils
from snap.libraries.closets.common import common_parts
from snap.libraries.closets.common import common_prompts


class Closet_Carcass(sn_types.Assembly):

    type_assembly = "PRODUCT"
    property_id = "{}.openings".format(closet_utils.CLOSET_LIB_NAME_SPACE)
    plan_draw_id = "{}.draw_plan".format(closet_utils.CLOSET_LIB_NAME_SPACE)
    show_in_library = True
    category_name = "Closet Products - Partitions"
    opening_qty = 0
    is_hanging = True
    defaults = None
    calculator_name = "Opening Widths Calculator"

    dog_ear_height = sn_unit.inch(8)  # Dog ear height always 8"

    left_filler = None
    right_filler = None
    backing_parts = {}
    backing_inserts = []

    def __init__(self, obj_bp=None):
        super().__init__(obj_bp=obj_bp)
        self.backing_parts = {}
        self.backing_inserts = []

        if obj_bp:
            self.assembly_name = obj_bp.name
            opening_qty = self.get_prompt("Opening Quantity")

            if opening_qty:
                self.opening_qty = opening_qty.get_value()

            for i in range(self.opening_qty):
                self.backing_parts[str(i + 1)] = []

            self.get_backing_parts()

            for child in obj_bp.children:
                if "IS_LEFT_FILLER_BP" in child:
                    self.left_filler = sn_types.Part(child)
                if "IS_RIGHT_FILLER_BP" in child:
                    self.right_filler = sn_types.Part(child)
                # if "IS_COUNTERTOP_BP" in child:
                #     self.countertop = sn_types.Part(child)

        # OLD SNAP
        self.defaults = bpy.context.scene.sn_closets.closet_defaults

        self.width = ((sn_unit.inch(.75) + sn_unit.inch(24)) * self.opening_qty) + sn_unit.inch(.75)

        if self.is_hanging:
            self.height = self.defaults.hanging_height
        else:
            self.height = sn_unit.millimeter(float(self.defaults.panel_height))
        self.depth = self.defaults.panel_depth

    def get_opening_cleats(self, opening_num):
        cleats = []
        for child in self.obj_bp.children:
            if "IS_BACKING_CLEAT" in child:
                continue
            if "IS_CLEAT" in child:
                if int(child.sn_closets.opening_name) == opening_num:
                    cleats.append(sn_types.Assembly(child))
        return cleats

    def update_cleats(self, opening_num, prompt_vars=[]):
        for cleat in self.get_opening_cleats(opening_num):
            hide = cleat.get_prompt('Hide')
            if "Bottom" in cleat.obj_bp.name:
                hide.set_formula(
                    'IF(OR(B_Cleat==False,AND(B_Sections==1,CBT==1,CTR,BIG==0),'
                    'AND(B_Sections>1,AND(BIG==0,OR(AND(IS_SB,CBT==1,BTM),'
                    'AND(IS_SB,CBT==1,BTM,CTR,TOP==False),AND(IS_SB==False,BTM,BBT==1))))),'
                    'True,False) or Hide',
                    prompt_vars)
                use_cleat_cover = cleat.get_prompt('Use Cleat Cover')
                use_cleat_cover.set_formula('IF(OR(BIB>0,BIG>0),False,True)', prompt_vars)
            else:
                hide.set_formula(
                    'IF(OR(Add_Hanging_Rail,AND(B_Sections==1,CBT==1,CTR),'
                    'AND(B_Sections>1,OR(AND(IS_SB,CBT==1,TOP),'
                    'AND(IS_SB,CBT==1,TOP,CTR,BTM==False),'
                    'AND(IS_SB==False,TOP,TBT==1)))),True,False) or Hide',
                    prompt_vars)

    def get_backing_parts(self):
        for child in self.obj_bp.children:
            if child.sn_closets.is_back_bp:
                opening_num = child.sn_closets.opening_name
                if opening_num != '':
                    self.backing_parts[child.sn_closets.opening_name].append(sn_types.Part(child))

    def get_opening_inserts(self, obj_bp, opening_num):
        for child in obj_bp.children:
            props = child.sn_closets
            types = (props.is_door_insert_bp, props.is_hamper_insert_bp, props.is_drawer_stack_bp)
            if any(types) and int(props.opening_name) == opening_num:
                self.backing_inserts.append(sn_types.Assembly(child))
                if child.children:
                    self.get_opening_inserts(child, opening_num)
        return self.backing_inserts

    def update_backing_sections(self, opening_num, backing):
        self.backing_inserts = []

        for insert in self.get_opening_inserts(self.obj_bp, opening_num):
            if insert:
                doors_gap_ppt = insert.get_prompt('Doors Backing Gap')
                drawers_gap_ppt = insert.get_prompt('Drawer Stack Backing Gap')
                hamper_gap_ppt = insert.get_prompt('Hamper Backing Gap')

                if doors_gap_ppt:
                    Doors_Backing_Gap = doors_gap_ppt.get_var()
                    top_insert_backing = backing.get_prompt('Top Insert Backing')
                    top_insert_backing.set_formula('Doors_Backing_Gap', [Doors_Backing_Gap])

                if drawers_gap_ppt:
                    Drawer_Stack_Backing_Gap = drawers_gap_ppt.get_var()
                    bottom_insert_gap = backing.get_prompt('Bottom Insert Gap')
                    bottom_insert_gap.set_formula('Drawer_Stack_Backing_Gap', [Drawer_Stack_Backing_Gap])

                if hamper_gap_ppt:
                    Hamper_Backing_Gap = hamper_gap_ppt.get_var()
                    bottom_insert_backing = backing.get_prompt('Bottom Insert Backing')
                    bottom_insert_backing.set_formula('Hamper_Backing_Gap', [Hamper_Backing_Gap])

    def add_opening_prompts(self):
        calculator = self.get_calculator(self.calculator_name)

        if self.is_hanging:
            floor_mounted = False
            panel_height = self.defaults.hanging_panel_height
        else:
            floor_mounted = True
            panel_height = self.defaults.panel_height

        for i in range(1, self.opening_qty + 1):
            calc_prompt = calculator.add_calculator_prompt("Opening " + str(i) + " Width")
            calc_prompt.equal = True
            self.add_prompt("Opening Quantity", 'QUANTITY', self.opening_qty)
            self.add_prompt("Opening " + str(i) + " Depth", 'DISTANCE', self.depth)
            self.add_prompt("Opening " + str(i) + " Height", 'DISTANCE', sn_unit.millimeter(float(panel_height)))
            self.add_prompt("Opening " + str(i) + " Floor Mounted", 'CHECKBOX', floor_mounted)
            self.add_prompt("Opening " + str(i) + " Top Backing Thickness", 'COMBOBOX', 0, ['1/4"', '3/4"'])
            self.add_prompt("Opening " + str(i) + " Center Backing Thickness", 'COMBOBOX', 0, ['1/4"', '3/4"'])
            self.add_prompt("Opening " + str(i) + " Bottom Backing Thickness", 'COMBOBOX', 0, ['1/4"', '3/4"'])
            self.add_prompt("Opening " + str(i) + " Dog Ear Depth", 'DISTANCE', self.depth)

        for i in range(1, self.opening_qty + 1):
            self.add_prompt("Opening " + str(i) + " Stop LB", 'DISTANCE', 0)
            self.add_prompt("Opening " + str(i) + " Start LB", 'DISTANCE', 0)
            self.add_prompt("Opening " + str(i) + " Add Mid Drilling", 'CHECKBOX', False)
            self.add_prompt("Opening " + str(i) + " Drill Thru Left", 'CHECKBOX', False)
            self.add_prompt("Opening " + str(i) + " Drill Thru Right", 'CHECKBOX', False)
            self.add_prompt("Opening " + str(i) + " Remove Left Drill", 'CHECKBOX', False)
            self.add_prompt("Opening " + str(i) + " Remove Right Drill", 'CHECKBOX', False)

        for i in range(1, self.opening_qty + 2):
            self.add_prompt("Panel " + str(i) + " Exposed Bottom", 'CHECKBOX', False)

    def add_right_filler(self):
        Product_Width = self.obj_x.snap.get_var('location.x', 'Product_Width')
        Product_Height = self.obj_z.snap.get_var('location.z', 'Product_Height')
        Height_Right_Side = self.get_prompt('Height Right Side').get_var('Height_Right_Side')
        Extend_Right_Side = self.get_prompt('Extend Right Side').get_var('Extend_Right_Side')
        Right_Side_Wall_Filler = self.get_prompt('Right Side Wall Filler').get_var('Right_Side_Wall_Filler')
        Right_Side_Thickness = self.get_prompt('Right Side Thickness').get_var('Right_Side_Thickness')
        Loc_Right_Side = self.get_prompt('Loc Right Side').get_var('Loc_Right_Side')
        Last_Height = self.get_prompt('Opening ' + str(self.opening_qty) + ' Height').get_var("Last_Height")
        Last_Depth = self.get_prompt('Opening ' + str(self.opening_qty) + ' Depth').get_var("Last_Depth")
        Last_Floor = self.get_prompt('Opening ' + str(self.opening_qty) + ' Floor Mounted').get_var("Last_Floor")
        # Right_End_Condition = self.get_prompt('Right End Condition').get_var('Right_End_Condition')
        Right_End_Deduction = self.get_prompt('Right End Deduction').get_var('Right_End_Deduction')

        self.right_filler = common_parts.add_filler(self)
        self.right_filler.obj_bp["IS_RIGHT_FILLER_BP"] = True

        self.right_filler.dim_x(
            'IF(Extend_Right_Side,Height_Right_Side,Last_Height)',
            [Last_Height, Height_Right_Side, Extend_Right_Side])
        self.right_filler.dim_y('Right_Side_Wall_Filler', [Right_Side_Wall_Filler])
        self.right_filler.dim_z('Right_Side_Thickness', [Right_Side_Thickness])
        self.right_filler.loc_x(
            'Product_Width-Right_Side_Wall_Filler',
            [Product_Width, Right_Side_Wall_Filler])
        self.right_filler.loc_y(
            "-Last_Depth+Right_End_Deduction",
            [Last_Depth, Right_End_Deduction])
        self.right_filler.loc_z(
            """IF(Extend_Right_Side,
            (Loc_Right_Side-Height_Right_Side),
            IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height))""",
            [
                Loc_Right_Side, Height_Right_Side, Last_Floor, Product_Height,
                Toe_Kick_Height, Last_Height, Extend_Right_Side])
        self.right_filler.rot_x(value=0)
        self.right_filler.rot_y(value=math.radians(-90))
        self.right_filler.rot_z(value=math.radians(-90))

    def add_sides(self):
        Product_Height = self.obj_z.snap.get_var('location.z', 'Product_Height')
        Product_Width = self.obj_x.snap.get_var('location.x', 'Product_Width')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Right_Side_Wall_Filler = self.get_prompt('Right Side Wall Filler').get_var('Right_Side_Wall_Filler')
        Left_Side_Thickness = self.get_prompt('Left Side Thickness').get_var('Left_Side_Thickness')
        Right_Side_Thickness = self.get_prompt('Right Side Thickness').get_var('Right_Side_Thickness')
        Extend_Left_End_Pard_Down = self.get_prompt('Extend Left End Pard Down').get_var()
        Extend_Right_End_Pard_Down = self.get_prompt('Extend Right End Pard Down').get_var()
        Height_Left_Side = self.get_prompt('Height Left Side').get_var('Height_Left_Side')
        Height_Right_Side = self.get_prompt('Height Right Side').get_var('Height_Right_Side')
        Loc_Left_Side = self.get_prompt('Loc Left Side').get_var('Loc_Left_Side')
        Loc_Right_Side = self.get_prompt('Loc Right Side').get_var('Loc_Right_Side')
        Left_Filler_Setback_Amount = self.get_prompt('Left Filler Setback Amount').get_var()
        Right_Filler_Setback_Amount = self.get_prompt('Right Filler Setback Amount').get_var()
        Left_End_Deduction = self.get_prompt('Left End Deduction').get_var('Left_End_Deduction')
        Right_End_Deduction = self.get_prompt('Right End Deduction').get_var('Right_End_Deduction')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Edge_Bottom_of_Left_Filler = self.get_prompt("Edge Bottom of Left Filler").get_var()
        Edge_Bottom_of_Right_Filler = self.get_prompt("Edge Bottom of Right Filler").get_var()
        Depth_1 = self.get_prompt('Opening 1 Depth').get_var('Depth_1')
        Height_1 = self.get_prompt('Opening 1 Height').get_var('Height_1')
        Floor_1 = self.get_prompt('Opening 1 Floor Mounted').get_var('Floor_1')
        Exposed_Bottom_1 = self.get_prompt('Panel 1 Exposed Bottom').get_var('Exposed_Bottom_1')
        Last_Depth = self.get_prompt('Opening ' + str(self.opening_qty) + ' Depth').get_var("Last_Depth")
        Last_Height = self.get_prompt('Opening ' + str(self.opening_qty) + ' Height').get_var("Last_Height")
        Last_Floor = self.get_prompt('Opening ' + str(self.opening_qty) + ' Floor Mounted').get_var("Last_Floor")
        Last_Exposed_Bottom = self.get_prompt('Panel ' + str(self.opening_qty + 1) + ' Exposed Bottom').get_var("Last_Exposed_Bottom")
        # Add_Backing = self.get_prompt('Opening ' + str(1) + ' Add Backing').get_var('Add_Backing')
        Left_End_Condition = self.get_prompt('Left End Condition').get_var('Left_End_Condition')
        Right_End_Condition = self.get_prompt('Right End Condition').get_var('Right_End_Condition')
        Add_Capping_Left_Filler = self.get_prompt("Add Capping Left Filler").get_var()
        Add_Capping_Right_Filler = self.get_prompt("Add Capping Right Filler").get_var()

        # Left side panel is always '1'
        Front_Angle_Height = self.get_prompt('Front Angle ' + str(1) + ' Height').get_var('Front_Angle_Height')
        Front_Angle_Depth = self.get_prompt('Front Angle ' + str(1) + ' Depth').get_var('Front_Angle_Depth')

        Front_Angle_Depth_All = self.get_prompt('Front Angle Depth').get_var('Front_Angle_Depth_All')

        left_filler = common_parts.add_filler(self)
        left_filler.set_name("Left Filler")
        left_filler.dim_x(
            'IF(Extend_Left_End_Pard_Down,Height_1+Height_Left_Side,Height_1)',
            [Height_1, Height_Left_Side, Extend_Left_End_Pard_Down])
        left_filler.dim_y('-Left_Side_Wall_Filler', [Left_Side_Wall_Filler])
        left_filler.dim_z('Left_Side_Thickness', [Left_Side_Thickness])
        left_filler.loc_x('Left_Side_Wall_Filler', [Left_Side_Wall_Filler])
        left_filler.loc_y(
            "-Depth_1-Left_End_Deduction+Left_Filler_Setback_Amount",
            [Depth_1, Left_End_Deduction, Left_Filler_Setback_Amount])
        left_filler.loc_z(
            'IF(Floor_1,Toe_Kick_Height,Product_Height-Height_1-IF(Extend_Left_End_Pard_Down,Height_Left_Side,0))',
            [Loc_Left_Side, Floor_1, Height_Left_Side, Product_Height,
             Height_1, Toe_Kick_Height, Extend_Left_End_Pard_Down])
        left_filler.rot_x(value=0)
        left_filler.rot_y(value=math.radians(-90))
        left_filler.rot_z(value=math.radians(-90))
        hide = left_filler.get_prompt("Hide")
        hide.set_formula(
            'IF(OR(Left_Side_Wall_Filler==0,Left_End_Condition==3),True,False) or Hide',
            [Left_Side_Wall_Filler, Left_End_Condition, self.hide_var])
        left_filler.get_prompt("Exposed Left").set_formula(
            'IF(Edge_Bottom_of_Left_Filler,True,False)', [Edge_Bottom_of_Left_Filler])
        left_filler.get_prompt("Exposed Left").set_value(True)
        left_filler.get_prompt("Exposed Right").set_value(True)
        left_filler.get_prompt("Exposed Back").set_value(True)

        left_capping_filler = common_parts.add_filler(self)
        left_capping_filler.set_name("Left Capping Filler")
        left_capping_filler.dim_x(
            'IF(Extend_Left_End_Pard_Down,Height_1+Height_Left_Side,Height_1-INCH(0.91))',
            [Height_1, Height_Left_Side, Extend_Left_End_Pard_Down])
        left_capping_filler.dim_y(
            '-Left_Side_Wall_Filler-INCH(0.25)', [Left_Side_Wall_Filler])
        left_capping_filler.dim_z('Left_Side_Thickness', [Left_Side_Thickness])
        left_capping_filler.loc_x('Left_Side_Wall_Filler+INCH(0.25)', [Left_Side_Wall_Filler])
        left_capping_filler.loc_y(
            "-Depth_1-Left_End_Deduction+Left_Filler_Setback_Amount-Left_Side_Thickness",
            [Depth_1, Left_End_Deduction, Left_Filler_Setback_Amount, Left_Side_Thickness])
        left_capping_filler.loc_z(
            "IF(Floor_1,Toe_Kick_Height,Product_Height-Height_1"
            "-IF(Extend_Left_End_Pard_Down,Height_Left_Side,0))+INCH(0.455)",
            [Loc_Left_Side, Floor_1, Height_Left_Side, Product_Height, Height_1,
             Toe_Kick_Height, Extend_Left_End_Pard_Down])
        left_capping_filler.rot_y(value=math.radians(-90))
        left_capping_filler.rot_z(value=math.radians(-90))
        left_capping_filler.get_prompt('Hide').set_formula(
            'IF(OR(Left_Side_Wall_Filler==0,Left_End_Condition==3),True,IF(Add_Capping_Left_Filler,False,True)) or Hide',
            [Left_Side_Wall_Filler, Left_End_Condition, Add_Capping_Left_Filler, self.hide_var])
        left_capping_filler.get_prompt("Exposed Left").set_value(True)
        left_capping_filler.get_prompt("Exposed Right").set_value(True)
        left_capping_filler.get_prompt("Exposed Back").set_value(True)

        left_side = common_parts.add_panel(self)
        left_side.obj_bp['PARTITION_NUMBER'] = 0
        left_props = left_side.obj_bp.sn_closets
        left_props.is_left_panel_bp = True
        left_side.dim_x(
            'IF(Extend_Left_End_Pard_Down,Height_1+Height_Left_Side,Height_1)',
            [Height_1, Height_Left_Side, Extend_Left_End_Pard_Down])
        left_side.dim_y('IF(Extend_Left_End_Pard_Down,-Depth_1-Left_End_Deduction,-Depth_1)', [Depth_1, Left_End_Deduction, Extend_Left_End_Pard_Down])
        left_side.dim_z('-Left_Side_Thickness', [Left_Side_Thickness])
        left_side.loc_x('Left_Side_Wall_Filler', [Left_Side_Wall_Filler])
        left_side.loc_z(
            "IF(Extend_Left_End_Pard_Down,(Product_Height-Height_1-Height_Left_Side),"
            "IF(Floor_1,Toe_Kick_Height,Product_Height-Height_1))",
            [Loc_Left_Side, Floor_1, Height_Left_Side, Product_Height,
             Height_1, Toe_Kick_Height, Extend_Left_End_Pard_Down])
        left_side.rot_y(value=math.radians(-90))

        hide = left_side.get_prompt('Hide')
        hide.set_formula('IF(Left_End_Condition==3,True,False) or Hide', [Left_End_Condition, self.hide_var])
        is_left_end_panel = left_side.get_prompt('Is Left End Panel')
        is_left_end_panel.set_formula('IF(Left_End_Condition==0,True,False)', [Left_End_Condition])
        left_side.get_prompt('Right Depth').set_formula('Depth_1', [Depth_1])
        left_side.get_prompt('Place Hanging Hardware On Right').set_value(True)
        Dog_Ear_Active = self.get_prompt('Dog Ear Active').get_var('Dog_Ear_Active')
        left_side.get_prompt("Dog Ear Height").set_value(self.dog_ear_height)
        left_side.get_prompt("Dog Ear Depth").set_formula(
            'IF(Dog_Ear_Active,'
            'IF(Front_Angle_Depth_All<=Depth_1,'
            'Depth_1-Front_Angle_Depth_All, 0),'
            '0)',
            [Dog_Ear_Active, Front_Angle_Depth_All, Depth_1])
        left_side.get_prompt("CatNum").set_formula('IF(Front_Angle_Height>INCH(0),1017,1004)', [Front_Angle_Height])
        left_side.get_prompt("Exposed Bottom").set_formula("Exposed_Bottom_1", [Exposed_Bottom_1])

        # Add_Backing = self.get_prompt('Opening ' + str(self.opening_qty) + ' Add Backing').get_var('Add_Backing')

        right_filler = common_parts.add_filler(self)
        right_filler.set_name("Right Filler")
        right_filler.dim_x(
            'IF(Extend_Right_End_Pard_Down,Last_Height+Height_Right_Side,Last_Height)',
            [Last_Height, Height_Right_Side, Extend_Right_End_Pard_Down])
        right_filler.dim_y('Right_Side_Wall_Filler', [Right_Side_Wall_Filler])
        right_filler.dim_z('Right_Side_Thickness', [Right_Side_Thickness])
        right_filler.loc_x(
            'Product_Width-Right_Side_Wall_Filler',
            [Product_Width, Right_Side_Wall_Filler])
        right_filler.loc_y(
            "-Last_Depth-Right_End_Deduction+Right_Filler_Setback_Amount",
            [Last_Depth, Right_End_Deduction, Right_Filler_Setback_Amount])
        right_filler.loc_z(
            "IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height"
            "-IF(Extend_Right_End_Pard_Down,Height_Right_Side,0))",
            [Loc_Right_Side, Height_Right_Side, Last_Floor, Product_Height,
             Toe_Kick_Height, Last_Height, Extend_Right_End_Pard_Down])
        right_filler.rot_y(value=math.radians(-90))
        right_filler.rot_z(value=math.radians(-90))
        hide = right_filler.get_prompt('Hide')
        hide.set_formula(
            'IF(OR(Right_Side_Wall_Filler==0,Right_End_Condition==3),True,False) or Hide',
            [Right_Side_Wall_Filler, Right_End_Condition, self.hide_var])
        right_filler.get_prompt("Exposed Left").set_formula(
            'IF(Edge_Bottom_of_Right_Filler,True,False)', [Edge_Bottom_of_Right_Filler])
        right_filler.get_prompt("Exposed Left").set_value(True)
        right_filler.get_prompt("Exposed Right").set_value(True)
        right_filler.get_prompt("Exposed Back").set_value(True)

        right_capping_filler = common_parts.add_filler(self)
        right_capping_filler.set_name("Right Capping Filler")
        right_capping_filler.dim_x(
            'IF(Extend_Right_End_Pard_Down,Last_Height+Height_Right_Side,Last_Height)-INCH(0.91)',
            [Last_Height, Height_Right_Side, Extend_Right_End_Pard_Down])
        right_capping_filler.dim_y('Right_Side_Wall_Filler+INCH(0.25)', [Right_Side_Wall_Filler])
        right_capping_filler.dim_z('Right_Side_Thickness', [Right_Side_Thickness])
        right_capping_filler.loc_x(
            'Product_Width-Right_Side_Wall_Filler-INCH(0.25)', [Product_Width, Right_Side_Wall_Filler])
        right_capping_filler.loc_y(
            "-Last_Depth-Right_End_Deduction+Right_Filler_Setback_Amount-Right_Side_Thickness",
            [Last_Depth, Right_End_Deduction, Right_Filler_Setback_Amount, Right_Side_Thickness])
        right_capping_filler.loc_z(
            "IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height"
            "-IF(Extend_Right_End_Pard_Down,Height_Right_Side,0))+INCH(0.455)",
            [Loc_Right_Side, Height_Right_Side, Last_Floor, Product_Height,
             Toe_Kick_Height, Last_Height, Extend_Right_End_Pard_Down])
        right_capping_filler.rot_y(value=math.radians(-90))
        right_capping_filler.rot_z(value=math.radians(-90))
        right_capping_filler.get_prompt('Hide').set_formula(
            'IF(OR(Right_Side_Wall_Filler==0,Right_End_Condition==3),True,IF(Add_Capping_Right_Filler,False,True)) or Hide',
            [Right_Side_Wall_Filler, Right_End_Condition, Add_Capping_Right_Filler, self.hide_var])
        right_capping_filler.get_prompt("Exposed Left").set_value(True)
        right_capping_filler.get_prompt("Exposed Right").set_value(True)
        right_capping_filler.get_prompt("Exposed Back").set_value(True)

        right_side = common_parts.add_panel(self)
        right_side.obj_bp['PARTITION_NUMBER'] = self.opening_qty
        right_props = right_side.obj_bp.sn_closets
        right_props.is_right_panel_bp = True
        right_side.dim_x('IF(Extend_Right_End_Pard_Down,Last_Height+Height_Right_Side,Last_Height)', [
                         Last_Height, Height_Right_Side, Extend_Right_End_Pard_Down, Last_Floor])
        right_side.dim_y('IF(Extend_Right_End_Pard_Down,-Last_Depth-Right_End_Deduction,-Last_Depth)', [
            Last_Depth, Right_End_Deduction, Extend_Right_End_Pard_Down])


        right_side.dim_z('Right_Side_Thickness', [Right_Side_Thickness])
        right_side.loc_x('Product_Width-Right_Side_Wall_Filler',
                         [Product_Width, Right_Side_Wall_Filler])
        right_side.loc_y(value=0)
        right_side.loc_z(
            "IF(Extend_Right_End_Pard_Down,(Product_Height-Last_Height-Height_Right_Side),"
            "IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height))",
            [Loc_Right_Side, Height_Right_Side, Last_Floor, Product_Height,
             Toe_Kick_Height, Last_Height, Extend_Right_End_Pard_Down])
        right_side.rot_y(value=math.radians(-90))
        right_side.get_prompt('Hide').set_formula('IF(Right_End_Condition==3,True,False) or Hide', [Right_End_Condition, self.hide_var])
        right_side.get_prompt('Is Right End Panel').set_formula(
            'IF(Right_End_Condition==0,True,False)', [Right_End_Condition])
        right_side.get_prompt('Left Depth').set_formula('Last_Depth', [Last_Depth])

        # Right side panel is always 'self.opening_qty + 1'
        # (with 4 openings the 5th panel is the right side and last panel)
        Front_Angle_Height = self.get_prompt(
            'Front Angle ' + str(self.opening_qty + 1) + ' Height').get_var('Front_Angle_Height')
        right_side.get_prompt("Dog Ear Height").set_value(self.dog_ear_height)
        right_side.get_prompt("Dog Ear Depth").set_formula(
            'IF(Dog_Ear_Active,'
            'IF(Front_Angle_Depth_All<=Last_Depth,'
            'Last_Depth-Front_Angle_Depth_All,0),'
            '0)',
            [Dog_Ear_Active, Front_Angle_Depth_All, Last_Depth])
        right_side.get_prompt("CatNum").set_formula('IF(Front_Angle_Height>INCH(0),1017,1004)', [Front_Angle_Height])
        right_side.get_prompt("Exposed Bottom").set_formula("Last_Exposed_Bottom", [Last_Exposed_Bottom])

    def add_panel(self, index, previous_panel):
        PH = self.obj_z.snap.get_var('location.z', 'PH')

        calculator = self.get_calculator(self.calculator_name)
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(index - 1)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(index - 1)))

        Depth = self.get_prompt('Opening ' + str(index - 1) + ' Depth').get_var("Depth")
        H = self.get_prompt('Opening ' + str(index - 1) + ' Height').get_var("H")
        Floor = self.get_prompt('Opening ' + str(index - 1) + ' Floor Mounted').get_var("Floor")
        Next_Floor = self.get_prompt('Opening ' + str(index) + ' Floor Mounted').get_var("Next_Floor")
        Next_Depth = self.get_prompt('Opening ' + str(index) + ' Depth').get_var("Next_Depth")
        NH = self.get_prompt('Opening ' + str(index) + ' Height').get_var("NH")
        EB = self.get_prompt('Panel ' + str(index) + ' Exposed Bottom').get_var('EB')

        Panel_Thickness = self.get_prompt('Panel Thickness').get_var('Panel_Thickness')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')

        Dog_Ear_Active = self.get_prompt('Dog Ear Active').get_var('Dog_Ear_Active')

        # In between panels can reference 'index' here
        Front_Angle_Height = self.get_prompt('Front Angle ' + str(index) + ' Height').get_var('Front_Angle_Height')
        Front_Angle_Depth = self.get_prompt('Front Angle ' + str(index) + ' Depth').get_var('Front_Angle_Depth')
        Front_Angle_Depth_All = self.get_prompt('Front Angle Depth').get_var('Front_Angle_Depth_All')

        panel = common_parts.add_panel(self)

        if previous_panel:
            Prev_Panel_X = previous_panel.obj_bp.snap.get_var("location.x", 'Prev_Panel_X')
            panel.loc_x(
                'Prev_Panel_X+Panel_Thickness+opening_{}_width'.format(str(index - 1)),
                [Prev_Panel_X, Panel_Thickness, Width])
        else:
            Left_Side_Thickness = self.get_prompt('Left Side Thickness').get_var('Left_Side_Thickness')
            panel.loc_x(
                'Left_Side_Thickness'
                '+opening_{}_width'
                '+Left_Side_Wall_Filler'
                '+Panel_Thickness'.format(str(index - 1)),
                [Left_Side_Thickness, Width, Left_Side_Wall_Filler, Panel_Thickness])

        panel.loc_y(value=0)
        panel.loc_z(
            """min(IF(Floor,
            Toe_Kick_Height,
            IF(Next_Floor,Toe_Kick_Height,PH-H)),
            IF(Next_Floor,Toe_Kick_Height,IF(Floor,Toe_Kick_Height,PH-NH)))""",
            [Floor, Next_Floor, Toe_Kick_Height, H, PH, NH])
        panel.rot_x(value=0)
        panel.rot_y(value=math.radians(-90))
        panel.rot_z(value=0)
        panel.dim_x(
            'max(IF(Floor,H,IF(Next_Floor,PH-Toe_Kick_Height,H)),IF(Next_Floor,NH,IF(Floor,PH-Toe_Kick_Height,NH)))',
            [Floor, Next_Floor, PH, H, NH, Toe_Kick_Height])
        panel.dim_y('-max(Depth,Next_Depth)', [Depth, Next_Depth])
        panel.dim_z('Panel_Thickness', [Panel_Thickness])

        left_depth = panel.get_prompt("Left Depth")
        left_depth.set_formula('Depth', [Depth])
        right_depth = panel.get_prompt("Right Depth")
        right_depth.set_formula('Next_Depth', [Next_Depth])

        panel.get_prompt('Stop Drilling Bottom Left').set_formula('IF(Floor,0,IF(NH>H,H,0))', [H, NH, Floor])
        panel.get_prompt('Stop Drilling Top Left').set_formula('IF(Floor,IF(NH>H,H,0),0)', [Floor, H, NH])
        panel.get_prompt('Stop Drilling Bottom Right').set_formula('IF(Next_Floor,0,IF(H>NH,NH,0))', [H, NH, Next_Floor])
        panel.get_prompt('Stop Drilling Top Right').set_formula('IF(Next_Floor,IF(H>NH,NH,0),0)', [H, NH, Next_Floor])

        dog_ear_height = panel.get_prompt("Dog Ear Height")
        dog_ear_height.set_value(self.dog_ear_height)

        dog_ear_depth = panel.get_prompt("Dog Ear Depth")
        dog_ear_depth.set_formula(
            'IF(Dog_Ear_Active,'
            'IF(Front_Angle_Depth_All<=max(Depth,Next_Depth),'
            'max(Depth,Next_Depth)-Front_Angle_Depth_All,0),'
            '0)',
            [Dog_Ear_Active, Front_Angle_Depth_All,
             Depth,Next_Depth])

        catnum = panel.get_prompt("CatNum")
        catnum.set_formula('IF(Front_Angle_Height>INCH(0),1017,1004)', [Front_Angle_Height])
        panel.get_prompt("Exposed Bottom").set_formula('EB', [EB])

        return panel

    def add_shelf(self, i, panel, is_top=False):
        calculator = self.get_calculator(self.calculator_name)
        Product_Height = self.obj_z.snap.get_var('location.z', 'Product_Height')
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))
        Depth = self.get_prompt('Opening ' + str(i) + ' Depth').get_var('Depth')
        Height = self.get_prompt('Opening ' + str(i) + ' Height').get_var('Height')
        Floor = self.get_prompt('Opening ' + str(i) + ' Floor Mounted').get_var('Floor')
        Rm_Btm_Hang_Shelf = self.get_prompt('Remove Bottom Hanging Shelf ' + str(i)).get_var('Rm_Btm_Hang_Shelf')
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Front_Angle_Depth = self.get_prompt('Front Angle Depth').get_var('Front_Angle_Depth')
        RN_1_H = self.get_prompt('First Rear Notch Height').get_var('RN_1_H')
        RN_1_D = self.get_prompt('First Rear Notch Depth').get_var('RN_1_D')
        RN_2_H = self.get_prompt('Second Rear Notch Height').get_var('RN_2_H')
        RN_2_D = self.get_prompt('Second Rear Notch Depth').get_var('RN_2_D')
        Left_End_Condition = self.get_prompt('Left End Condition').get_var('Left_End_Condition')
        Right_End_Condition = self.get_prompt('Right End Condition').get_var('Right_End_Condition')
        Shelf_Gap = self.get_prompt('Shelf Gap').get_var('Shelf_Gap')
        Remove_Top_Shelf = self.get_prompt('Remove Top Shelf ' + str(i)).get_var('Remove_Top_Shelf')
        Dog_Ear_Active = self.get_prompt('Dog Ear Active').get_var('Dog_Ear_Active')
        Vertical_Offset = self.get_prompt("Top KD " + str(i) + " Vertical Offset").get_var('Vertical_Offset')

        shelf = common_parts.add_shelf(self)
        shelf.obj_bp.sn_closets.opening_name = str(i)
        is_locked_shelf = shelf.get_prompt("Is Locked Shelf")
        is_locked_shelf.set_value(value=True)

        Is_Locked_Shelf = shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
        Adj_Shelf_Setback = shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
        Locked_Shelf_Setback = shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
        Adj_Shelf_Clip_Gap = shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')

        if panel:  # NOT FIRST SHELF
            X_Loc = panel.obj_bp.snap.get_var('location.x', 'X_Loc')
            shelf.loc_x('X_Loc+IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [X_Loc, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        else:  # FIRST SHELF
            Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            shelf.loc_x(
                "Left_Side_Wall_Filler+X_Loc+IF(Left_End_Condition==3,Shelf_Gap,False)+IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)",
                [Left_Side_Wall_Filler, X_Loc, Is_Locked_Shelf, Adj_Shelf_Clip_Gap, Left_End_Condition, Shelf_Gap])

        if is_top:
            shelf.loc_z(
                'IF(Floor,Height+Toe_Kick_Height,Product_Height)-Vertical_Offset',
                [Floor, Height, Product_Height, Toe_Kick_Height, Vertical_Offset])
            shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness])
            shelf.dim_y("IF(Dog_Ear_Active,-Front_Angle_Depth,-Depth)+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)",
                        [Depth, Dog_Ear_Active, Front_Angle_Depth, Is_Locked_Shelf, Locked_Shelf_Setback, Adj_Shelf_Setback])           
            hide = shelf.get_prompt('Hide')
            hide.set_formula('IF(Remove_Top_Shelf,False,True) or Hide', [Remove_Top_Shelf, self.hide_var])
        else:
            rear_notch_1_inset = "IF(Floor,IF(Toe_Kick_Height<RN_1_H,RN_1_D,0),0)"
            rear_notch_2_inset = "IF(Floor,IF(Toe_Kick_Height<RN_2_H,RN_2_D,0),0)"
            shelf.loc_y(
                rear_notch_1_inset + "-" + rear_notch_2_inset,
                [Floor, Toe_Kick_Height, RN_1_H, RN_2_H, RN_1_D, RN_2_D])
            shelf.loc_z(
                'IF(Floor,Toe_Kick_Height,Product_Height-Height)',
                [Floor, Toe_Kick_Height, Product_Height, Height])
            shelf.dim_z('Shelf_Thickness', [Shelf_Thickness])
            shelf.dim_y("-Depth+" + rear_notch_1_inset + "+" + rear_notch_2_inset + "+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)",
                        [Floor, Depth, Toe_Kick_Height, RN_1_H, RN_2_H, RN_1_D,
                            RN_2_D, Is_Locked_Shelf, Locked_Shelf_Setback, Adj_Shelf_Setback])
            hide = shelf.get_prompt('Hide')
            hide.set_formula('IF(Floor,False,IF(Rm_Btm_Hang_Shelf,False,True)) or Hide', [Floor, Rm_Btm_Hang_Shelf, self.hide_var])

        shelf.rot_x(value=0)
        shelf.rot_y(value=0)
        shelf.rot_z(value=0)

        if i == 1:
            remove_left_holes = shelf.get_prompt("Remove Left Holes")
            remove_left_holes.set_formula('IF(Left_End_Condition==3,True,False)', [Left_End_Condition])
            shelf.dim_x(
                'opening_' + str(i) + '_width'
                '-IF(Left_End_Condition==3,Shelf_Gap,0)'
                '-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                [Width, Left_End_Condition, Shelf_Gap, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])

        elif i == self.opening_qty:
            remove_right_holes = shelf.get_prompt("Remove Right Holes")
            remove_right_holes.set_formula('IF(Right_End_Condition==3,True,False)', [Right_End_Condition])
            shelf.dim_x(
                'opening_{}_width'
                '-IF(Right_End_Condition==3,Shelf_Gap,0)'
                '-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)'.format(str(i)),
                [Width, Right_End_Condition, Shelf_Gap, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        else:
            shelf.loc_x(
                'X_Loc+IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',
                [X_Loc, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
            shelf.dim_x(
                'opening_' + str(i) + '_width'
                '-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])

        if is_top:
            drill_on_top = shelf.get_prompt("Drill On Top")
            drill_on_top.set_value(value=True)
        else:
            drill_on_top = shelf.get_prompt("Drill On Top")
            drill_on_top.set_value(value=False)

    def add_cover_cleat_opening_name(self, assembly, opening_name):
        for child in assembly.obj_bp.children:
            if 'IS_BP_ASSEMBLY' and 'IS_COVER_CLEAT' in child:
                child.sn_closets.opening_name = opening_name

    def add_top_cleat(self, i, panel):
        calculator = self.get_calculator(self.calculator_name)
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))

        Product_Width = self.obj_x.snap.get_var('location.x', 'Product_Width')
        Height = self.get_prompt('Opening ' + str(i) + ' Height').get_var('Height')
        Hanging_Height = self.obj_z.snap.get_var('location.z', 'Hanging_Height')
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        Cut_to_Fit_Amount = self.get_prompt("Cut to Fit Amount").get_var('Cut_to_Fit_Amount')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Add_Hanging_Rail = self.get_prompt('Add Hanging Rail').get_var('Add_Hanging_Rail')
        Floor = self.get_prompt('Opening ' + str(i) + ' Floor Mounted').get_var("Floor")
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Remove_Top_Shelf = self.get_prompt('Remove Top Shelf ' + str(i)).get_var('Remove_Top_Shelf')
        Cleat_Height = self.get_prompt("Cleat Height").get_var('Cleat_Height')
        TKDVO = self.get_prompt("Top KD " + str(i) + " Vertical Offset").get_var('TKDVO')

        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x', 'X_Loc')
        else:
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')

        cleat = common_parts.add_cleat(self)
        cleat.set_name("Top Cleat")
        cleat.obj_bp.sn_closets.opening_name = str(i)
        self.add_cover_cleat_opening_name(cleat, str(i))

        cleat.loc_y(value=0)
        cleat.loc_z(
            "IF(Floor,Height+Toe_Kick_Height,Hanging_Height)-IF(Remove_Top_Shelf,Shelf_Thickness,0)-TKDVO",
            [Remove_Top_Shelf, Shelf_Thickness, Floor, Height, Toe_Kick_Height, Hanging_Height, TKDVO])
        cleat.rot_x(value=math.radians(-90))

        cleat.dim_x('opening_{}_width'.format(str(i)),[Width])
        cleat.dim_y('Cleat_Height', [Cleat_Height])
        cleat.dim_z('-Shelf_Thickness',[Shelf_Thickness])

        if i == 1:
            cleat.loc_x('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler]) #USED TO FIX DRAWER SIDE TOKEN
        elif i == self.opening_qty: #LAST OPENING
            cleat.loc_x('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
        else:
            cleat.loc_x('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN

        hide = cleat.get_prompt('Hide')
        hide.set_formula(
            'Add_Hanging_Rail or Hide',
            [Add_Hanging_Rail, self.hide_var]
        )

    def add_bottom_cleat(self, i, panel):
        Product_Width = self.obj_x.snap.get_var('location.x', 'Product_Width')
        Hanging_Height = self.obj_z.snap.get_var('location.z','Hanging_Height')
        Height = self.get_prompt('Opening ' + str(i) + ' Height').get_var('Height')

        calculator = self.get_calculator(self.calculator_name)
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))

        B_Cleat = self.get_prompt('Add ' + str(i) + ' Bottom Cleat').get_var('B_Cleat')
        Cleat_Location = self.get_prompt('Cleat ' + str(i) + ' Location').get_var('Cleat_Location')
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        Cut_to_Fit_Amount = self.get_prompt("Cut to Fit Amount").get_var('Cut_to_Fit_Amount')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Floor = self.get_prompt('Opening ' + str(i) + ' Floor Mounted').get_var("Floor")
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Rm_Btm_Hang_Shelf = self.get_prompt('Remove Bottom Hanging Shelf ' + str(i)).get_var('Rm_Btm_Hang_Shelf')              

        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
        else:
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')

        cleat = common_parts.add_cleat(self)
        cleat.set_name("Bottom Cleat")
        cleat.obj_bp.sn_closets.opening_name = str(i)
        self.add_cover_cleat_opening_name(cleat, str(i))

        cleat.loc_y(value=0)
        cleat.loc_z('IF(Floor,Toe_Kick_Height+Shelf_Thickness+Cleat_Location,Hanging_Height-Height+Cleat_Location+IF(Rm_Btm_Hang_Shelf,Shelf_Thickness,0))',
                    [Floor,Toe_Kick_Height,Rm_Btm_Hang_Shelf,Shelf_Thickness,Hanging_Height,Height,Cleat_Location])
        cleat.rot_x(value=math.radians(-90))
        cleat.rot_y(value=0)
        cleat.rot_z(value=0)

        cleat.dim_x('opening_{}_width'.format(str(i)),[Width])
        cleat.dim_y(value=sn_unit.inch(-3.64))
        cleat.dim_z('-Shelf_Thickness',[Shelf_Thickness])

        if i == 1:
            cleat.loc_x('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler]) #USED TO FIX DRAWER SIDE TOKEN
        elif i == self.opening_qty: #LAST OPENING
            cleat.loc_x('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
        else:
            cleat.loc_x('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN

        hide = cleat.get_prompt('Hide')
        hide.set_formula('IF(B_Cleat,False,True) or Hide', [B_Cleat, self.hide_var])

    def add_closet_opening(self, i, panel):
        calculator = self.get_calculator(self.calculator_name)        
        Product_Height = self.obj_z.snap.get_var('location.z', 'Product_Height')
        Height = self.get_prompt('Opening ' + str(i) + ' Height').get_var('Height')
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))
        Depth = self.get_prompt('Opening ' + str(i) + ' Depth').get_var('Depth')
        Floor = self.get_prompt('Opening ' + str(i) + ' Floor Mounted').get_var('Floor')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        Opening_Height_Difference = self.get_prompt("Opening Height Difference").get_var('Opening_Height_Difference')
        TKDVO = self.get_prompt("Top KD " + str(i) + " Vertical Offset").get_var('TKDVO')

        opening = common_parts.add_section_opening(self)
        opening.obj_bp.sn_closets.opening_name = str(i)
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x', 'X_Loc')
            opening.loc_x('X_Loc', [X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            opening.loc_x('Left_Side_Wall_Filler+X_Loc',
                          [Left_Side_Wall_Filler, X_Loc])
        opening.loc_y('-Depth', [Depth])
        opening.loc_z('IF(Floor,Toe_Kick_Height+Shelf_Thickness,Product_Height-Height+Shelf_Thickness)',
                      [Floor, Toe_Kick_Height, Shelf_Thickness, Product_Height, Height])

        opening.dim_x('opening_{}_width'.format(str(i)), [Width])
        opening.dim_y("fabs(Depth)", [Depth])
        opening.dim_z('Height-Opening_Height_Difference-TKDVO',
                      [Height, Opening_Height_Difference, TKDVO])

    # def add_inside_dimension(self,i,panel):
        # Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        # Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        
        # if panel:
        #     X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
        # else:
        #     X_Loc = self.get_var('Left Side Thickness','X_Loc')
            
        # dim = sn_types.Dimension()
        # dim.parent(self.obj_bp)
        # dim.start_z(value=sn_unit.inch(-4))
        # dim.start_y(value=sn_unit.inch(4))
        # if panel:
        #     dim.start_x('X_Loc',[X_Loc])
        # else:
        #     dim.start_x('X_Loc+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
        # dim.end_x('Width',[Width])
        # dim.set_color('IF(Width>INCH(42),3,0)',[Width])
    
    def add_backing_cleat(self, i, panel, top_cleat=True, cover_cleat=False):
        Hanging_Height = self.obj_z.snap.get_var('location.z', 'Hanging_Height')
        Height = self.get_prompt('Opening ' + str(i) + ' Height').get_var('Height')
        calculator = self.get_calculator(self.calculator_name)
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))        

        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        Cut_to_Fit_Amount = self.get_prompt("Cut to Fit Amount").get_var('Cut_to_Fit_Amount')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Cleat_Height = self.get_prompt('Cleat Height').get_var( 'Cleat_Height')
        
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
        else:
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.obj_bp["IS_BACKING_CLEAT"] = True
        cleat.set_name("Top Cleat" if top_cleat else "Bottom Cleat")
        cleat.obj_bp.sn_closets.opening_name = str(i)
        self.add_cover_cleat_opening_name(cleat, str(i))

        cleat.rot_x(value=math.radians(-90))

        if top_cleat:
            cleat.dim_y('Cleat_Height', [Cleat_Height])
        else:
            cleat.dim_y('-Cleat_Height', [Cleat_Height])


        cleat.dim_z('-Shelf_Thickness',[Shelf_Thickness])

        if i == 1:
            cleat.loc_x('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler]) #USED TO FIX DRAWER SIDE TOKEN
        elif i == self.opening_qty: #LAST OPENING
            cleat.loc_x('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
        else:
            cleat.loc_x('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
        
        cleat.dim_x('opening_{}_width'.format(str(i)), [Width])        

        return cleat

    def add_backing(self,i,panel):
        parts = []
        calculator = self.get_calculator(self.calculator_name)
        PH = self.obj_z.snap.get_var('location.z', 'PH')
        Height = self.get_prompt('Opening ' + str(i) + ' Height').get_var('Height')
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))
        self.hide_var = self.get_prompt("Hide").get_var()

        Floor = self.get_prompt('Opening ' + str(i) + ' Floor Mounted').get_var('Floor')
        TBT = self.get_prompt('Opening ' + str(i) + ' Top Backing Thickness').get_var('TBT')
        CBT = self.get_prompt('Opening ' + str(i) + ' Center Backing Thickness').get_var('CBT')
        BBT = self.get_prompt('Opening ' + str(i) + ' Bottom Backing Thickness').get_var('BBT')
        B_Cleat = self.get_prompt('Add ' + str(i) + ' Bottom Cleat').get_var('B_Cleat')
        B_Cleat_Loc = self.get_prompt('Cleat ' + str(i) + ' Location').get_var('B_Cleat_Loc')
        CH = self.get_prompt('Cleat Height').get_var('CH')
        TKH = self.get_prompt('Toe Kick Height').get_var('TKH')
        ST = self.get_prompt('Shelf Thickness').get_var('ST')
        T_Shelf = self.get_prompt('Remove Top Shelf ' + str(i)).get_var('T_Shelf')
        B_Shelf = self.get_prompt('Remove Bottom Hanging Shelf ' + str(i)).get_var('B_Shelf')
        TKDVO = self.get_prompt("Top KD " + str(i) + " Vertical Offset").get_var('TKDVO')
      
        backing = common_parts.add_back(self)
        parts.append(backing)
        backing.obj_bp.sn_closets.opening_name = str(i)

        backing.add_prompt("Opening Bottom", 'DISTANCE', 0)
        backing.add_prompt("Top Insert Gap", 'DISTANCE', 0)
        backing.add_prompt("Bottom Insert Gap", 'DISTANCE', 0)
        backing.add_prompt("Backing Inset Amount", 'DISTANCE', sn_unit.inch(0.25))
        backing.add_prompt("3 Section Backing Config", 'COMBOBOX', 0,
            ['Full', 'Top', 'Bottom', 'Center', 'Top & Center', 'Bottom & Center', 'Top & Bottom'])# Fix

        ppt_obj_back_sections = backing.add_prompt_obj("Back_Sections")
        backing_sections = self.add_prompt("Backing Sections", 'QUANTITY', 1, prompt_obj=ppt_obj_back_sections)
        B_Sections = backing_sections.get_var('B_Sections')

        back_offset_ppt_obj = backing.add_prompt_obj("Backing_Offsets")
        backing_top_offset = self.add_prompt("Backing Top Offset", 'DISTANCE', 0, prompt_obj=back_offset_ppt_obj)
        backing_bottom_offset = self.add_prompt("Backing Bottom Offset", 'DISTANCE', 0, prompt_obj=back_offset_ppt_obj)

        ppt_obj_1_sec = backing.add_prompt_obj("1_Section")
        section_1_backing_z = self.add_prompt("1 Section Backing Z Location", 'DISTANCE', 0, prompt_obj=ppt_obj_1_sec)
        section_1_backing_x = self.add_prompt("1 Section Backing X Dimension", 'DISTANCE', 0, prompt_obj=ppt_obj_1_sec)

        ppt_obj_2_sec_config = backing.add_prompt_obj("2_Section_Config")
        section_2_backing_config = self.add_prompt('2 Section Backing Config', 'COMBOBOX', 0, ['Full', 'Top', 'Bottom'], prompt_obj=ppt_obj_2_sec_config)

        ppt_obj_2_sec = backing.add_prompt_obj("2_Section")
        section_2_backing_z_top = self.add_prompt("2 Section Backing Z Location with Top Insert", 'DISTANCE', 0, prompt_obj=ppt_obj_2_sec)
        section_2_backing_x_top = self.add_prompt("2 Section Backing X Dimension with Top Insert", 'DISTANCE', 0, prompt_obj=ppt_obj_2_sec)
        section_2_backing_z_bot = self.add_prompt("2 Section Backing Z Location with Bottom Insert", 'DISTANCE', 0, prompt_obj=ppt_obj_2_sec)
        section_2_backing_x_bot = self.add_prompt("2 Section Backing X Dimension with Bottom Insert", 'DISTANCE', 0, prompt_obj=ppt_obj_2_sec)

        ppt_obj_3_sec = backing.add_prompt_obj("3_Section")
        section_3_backing_z = self.add_prompt("3 Section Backing Z Location", 'DISTANCE', 0, prompt_obj=ppt_obj_3_sec)
        section_3_backing_x = self.add_prompt("3 Section Backing X Dimension", 'DISTANCE', 0, prompt_obj=ppt_obj_3_sec)

        ppt_obj_backing_config = backing.add_prompt_obj("Backing_Config")
        self.add_prompt("Top Section Backing", 'CHECKBOX', False, prompt_obj=ppt_obj_backing_config)
        self.add_prompt("Center Section Backing", 'CHECKBOX', False, prompt_obj=ppt_obj_backing_config)
        self.add_prompt("Bottom Section Backing", 'CHECKBOX', False, prompt_obj=ppt_obj_backing_config)
        self.add_prompt("Single Back", 'CHECKBOX', True, prompt_obj=ppt_obj_backing_config)

        ppt_obj_is_single_back = backing.add_prompt_obj("Is_Single_Back")
        is_single_back = self.add_prompt("Is Single Back", 'CHECKBOX', False, prompt_obj=ppt_obj_is_single_back)

        ppt_obj_insert_backing = backing.add_prompt_obj("Insert_Backing")
        self.add_prompt("Top Insert Backing",'DISTANCE', 0, prompt_obj=ppt_obj_insert_backing)
        self.add_prompt("Bottom Insert Backing", 'DISTANCE', 0, prompt_obj=ppt_obj_insert_backing)

        BTO = backing_top_offset.get_var('BTO')
        BBO = backing_bottom_offset.get_var('BBO')
        BZ1 = section_1_backing_z.get_var('BZ1')
        BX1 = section_1_backing_x.get_var('BX1')
        BC2 = section_2_backing_config.get_var('BC2')
        BZ2T = section_2_backing_z_top.get_var('BZ2T')
        BX2T = section_2_backing_x_top.get_var('BX2T')
        BZ2B = section_2_backing_z_bot.get_var('BZ2B')
        BX2B = section_2_backing_x_bot.get_var('BX2B')
        BZ3 = section_3_backing_z.get_var('BZ3')
        BX3 = section_3_backing_x.get_var('BX3')
        IS_SB = is_single_back.get_var('IS_SB')
        TOP = backing.get_prompt("Top Section Backing").get_var('TOP')
        CTR = backing.get_prompt("Center Section Backing").get_var('CTR')
        BTM = backing.get_prompt("Bottom Section Backing").get_var('BTM')
        SB = backing.get_prompt("Single Back").get_var('SB')
        TIB = backing.get_prompt("Top Insert Backing").get_var('TIB')
        BIB = backing.get_prompt("Bottom Insert Backing").get_var('BIB')
        TIG = backing.get_prompt("Top Insert Gap").get_var('TIG')
        BIG = backing.get_prompt("Bottom Insert Gap").get_var('BIG')
        BIA = backing.get_prompt("Backing Inset Amount").get_var('BIA')
        BC3 = backing.get_prompt("3 Section Backing Config").get_var('BC3')
        OB = backing.get_prompt("Opening Bottom").get_var('OB')

        backing_sections.set_formula('IF(AND(TIB>0,BIB>0),3,IF(OR(TIB>0,BIB>0),2,1))', [TIB, BIB])
        opening_bottom = backing.get_prompt('Opening Bottom')
        opening_bottom.set_formula('IF(Floor,TKH,PH-Height)', [Floor,TKH,PH,Height])

        is_single_back.set_formula(
            'IF(B_Sections==2,IF(AND(SB,TOP,BTM),True,False),IF(B_Sections==3,IF(OR(AND(SB,TOP,CTR,BTM),AND(SB,TOP,CTR),AND(SB,CTR,BTM)),True,False),True))',
            [SB,TOP,CTR,BTM,B_Sections])

        backing_top_offset.set_formula(
            'IF(T_Shelf,ST,0)+IF(OR(AND(B_Sections==1,CTR,CBT==0),AND(B_Sections>1,IS_SB,CBT==0),AND(B_Sections>1,SB==False,TOP,TBT==0)),CH-BIA,0)',
            [T_Shelf,ST,CH,TOP,CTR,BTM,TBT,CBT,SB,BIA,IS_SB,B_Sections])

        backing_bottom_offset.set_formula(
            'IF(AND(BIG>0,BIB==0),BIG,B_Cleat_Loc)'
            '+IF(OR(Floor,B_Shelf),ST,0)'
            '+IF(OR('
            'AND(B_Sections==1,CBT==0,CTR),'
            'AND(B_Sections>1,OR(AND(IS_SB,CBT==0),'
            'AND(IS_SB,CBT==0,BTM,CTR,TOP==False),'
            'AND(IS_SB==False,BTM,BBT==0)))),'
            'CH-BIA,0)',
            [Floor,B_Cleat,B_Cleat_Loc,ST,B_Shelf,CH,BIG,BIB,TOP,CTR,BTM,SB,CBT,BBT,BIA,B_Sections,IS_SB])

        # 1 section
        section_1_backing_z.set_formula(
            'OB+IF(BIG>0,BIG+IF(CBT==0,CH-BIA,0),BBO)',
            [OB,BBO,BIG,CBT,CH,BIA])

        section_1_backing_x.set_formula(
            'Height-IF(TIG>0,TIG,BTO)-IF(BIG>0,BIG+IF(CBT==0,CH-BIA,0),BBO)',
            [Height,BTO,TIG,BBO,BIG,CH,BIA,CBT])

        # 2 section
        section_2_backing_config.set_formula(
            'IF(AND(TOP,BTM),0,IF(TOP,1,IF(BTM,2,0)))',
            [TOP,BTM])

        # Top insert
        section_2_backing_z_top.set_formula(
            'IF(BC2==0,BZ1,'
            'IF(BC2==1,OB+Height-TIB+BIG+ST+IF(TBT==0,CH-BIA,0),'
            'IF(BC2==2,IF(BBT==0,OB+BBO-BIA,BZ1),BZ1)))',
            [Height,OB,BC2,BZ1,TIB,BBO,BIA,CH,ST,TBT,BBT,BIG])

        section_2_backing_x_top.set_formula(
            'IF(BC2==0,BX1,IF(BC2==1,TIB-IF(TBT==0,CH*2+BIA,ST)-IF(T_Shelf,ST,0),IF(BC2==2,Height-TIB-IF(BBT==0,CH*2-BIA*2,0)-B_Cleat_Loc-IF(B_Shelf,ST,0),BX1)))',
            [BC2, Height, TIB, BIB, BX1, BIA, CH, B_Cleat_Loc, T_Shelf, B_Shelf, ST, TBT, BBT])

        # Bottom insert
        section_2_backing_z_bot.set_formula(
            'IF(BC2==0,BZ1,IF(BC2==1,BIB+OB+IF(TBT==0,CH-BIA,0),IF(BC2==2,OB+IF(BBT==0,BBO-BIA,IF(B_Shelf,ST,0)),BZ1)))',
            [OB,BC2,BZ1,BIB,TIB,BBO,BIA,CH,TBT,BBT,B_Shelf,ST])

        section_2_backing_x_bot.set_formula(
            'IF(BC2==0,BX1,IF(BC2==1,Height-BIB-IF(TBT==0,CH*2-BIA*2,0)-IF(T_Shelf,ST,0),IF(BC2==2,BIB-IF(BBT==0,CH*2+BIA-B_Cleat_Loc,ST)-IF(B_Shelf,ST,0),BX1)))',
            [BC2,Height,TIB,BIB,BX1,BIA,CH,B_Cleat_Loc,T_Shelf,B_Shelf,ST,TBT, BBT])

        # 3 section
        # [0:'Full', 1:'Top', 2:'Bottom', 3:'Center', 4:'Top & Center', 5:'Bottom & Center', 6:'Top & Bottom']
        prompt = backing.get_prompt('3 Section Backing Config')
        prompt.set_formula(
            'IF(AND(TOP,CTR,BTM),0,IF(AND(TOP,CTR),4,IF(AND(BTM,CTR),5,IF(AND(TOP,BTM),6,IF(TOP,1,IF(CTR,3,IF(BTM,2,0)))))))',
            [TOP,CTR,BTM])

        section_3_backing_z.set_formula(
            'IF(OR(AND(BC3==0,IS_SB==False),BC3==3,BC3==4,AND(BC3==5,IS_SB==False)),'
            'OB+BIB+IF(BIG>0,BIG+IF(OR(BC3==3,BC3==4,BC3==5,BC3==0),-ST,0),0)+IF(CBT==0,CH-BIA,0)'
            ',BZ1)',
            [OB,BC3,BZ1,BIB,BIG,TIB,BIA,Height,ST,CH,CBT,IS_SB])
        
        section_3_backing_x.set_formula(
            'IF(IS_SB,'
            'IF(BC3==0,BX1,IF(BC3==4,Height-BIB-IF(BIG>0,BIG-ST,0)-BTO-IF(CBT==0,CH-BIA,0),'
            'IF(BC3==5,Height-TIB-BBO-IF(CBT==0,CH-BIA,0),BX1))),'
            'Height-TIB-BIB-IF(BIG>0,BIG-ST,0)-IF(CBT==0,CH*2-BIA*2,0))',
            [BC3,Height,TIB,BIB,BIG,BX1,BIA,CH,B_Cleat_Loc,T_Shelf,B_Shelf,ST,CBT,IS_SB,BBO,BTO])

        #Get X loc from opening panel
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
            backing.loc_x('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            backing.loc_x('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])

        backing.loc_z(
            'IF(B_Sections==1,BZ1,IF(B_Sections==2,IF(TIB>0,BZ2T,IF(BIB>0,BZ2B,0)),IF(B_Sections==3,BZ3,0)))',
            [B_Sections,BZ1,BZ2T,BZ2B,BZ3,TIB,BIB,OB,Height,ST,CBT,CH,BIA]
        )

        backing.rot_x(value=math.radians(-90))
        backing.rot_y(value=math.radians(-90))

        backing.dim_x(
            'IF(B_Sections==1,BX1-TKDVO,IF(B_Sections==2,IF(TIB>0,BX2T,IF(BIB>0,BX2B,0)),IF(B_Sections==3,BX3,0)))',
            [B_Sections,BX1,BX2T,BX2B,BX3,TIB,BIB,Height,CBT,CH,BIA,TKDVO]
        )

        backing.dim_y('opening_{}_width'.format(str(i)), [Width])
        backing.dim_z('IF(OR(AND(B_Sections==1,CBT==0),AND(B_Sections>1,CBT==0)),INCH(-0.25),INCH(-0.75))',[CBT, B_Sections])
        prompt = backing.get_prompt('Hide')
        prompt.set_formula(
            'IF(OR(AND(B_Sections==1,CTR),AND(B_Sections==2,SB,TOP,BTM),AND(B_Sections==3,CTR)),False,True) or Hide',
            [CTR,B_Sections,SB,TOP,BTM, self.hide_var])

        #Top back
        top_backing = common_parts.add_back(self)
        parts.append(top_backing)
        top_backing.obj_bp.sn_closets.opening_name = str(i)
        top_backing.obj_bp.sn_closets.is_back_bp = False
        top_backing.obj_bp.sn_closets.is_top_back_bp = True

        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
            top_backing.loc_x('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            top_backing.loc_x('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])

        top_backing.loc_y(value=0)
        top_backing.loc_z(
            'IF(B_Sections>1,'
            'IF(TIB>0,OB+Height-TIB+ST+IF(TBT==0,CH-BIA,0),'
            'IF(BIB>0,BIB+OB+IF(BIG>0,BIG-ST,0)+IF(TBT==0,CH-BIA,0),0))'
            ',0)',
            [B_Sections,OB,Height,TIB,CH,BIA,ST,TBT,BZ2T,BZ2B,BIB,BIG]
        )

        top_backing.rot_x(value=math.radians(-90))
        top_backing.rot_y(value=math.radians(-90))

        top_backing.dim_x(
            "IF(B_Sections==2,"
            "IF(TIB>0,TIB-IF(TBT==0,CH*2+BIA,ST)"
            "-IF(T_Shelf,ST,0),IF(BIB>0,Height-BIB-IF(BIG>0,BIG-ST,0)-IF(TBT==0,CH*2-BIA*2,0)-IF(T_Shelf,ST,0),0)),"
            "IF(B_Sections==3,TIB-IF(TBT==0,CH*2-BIA*2,0)-ST-IF(T_Shelf,ST,0),0))-TKDVO",
            [B_Sections, BC3, Height, CH, ST, TIB, BIB, BIG,
                BIA, T_Shelf, TBT, BX2T, BX2B, TKDVO]
        )
        top_backing.dim_y('opening_{}_width'.format(str(i)),[Width])
        top_backing.dim_z('IF(TBT==0,INCH(-0.25),INCH(-0.75))',[TBT])
        prompt = top_backing.get_prompt('Hide')
        prompt.set_formula(
            'IF(OR(B_Sections==1,TOP==False,AND(B_Sections>1,IS_SB)),True,False) or Hide',
            [B_Sections,TOP,CTR,BTM,IS_SB, self.hide_var])

        #Bottom back
        bottom_backing = common_parts.add_back(self)
        parts.append(bottom_backing)
        bottom_backing.obj_bp.sn_closets.opening_name = str(i)
        bottom_backing.obj_bp.sn_closets.is_back_bp = False
        bottom_backing.obj_bp.sn_closets.is_bottom_back_bp = True        

        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
            X_Loc = panel.obj_bp.snap.get_var('location.x', 'X_Loc')
            bottom_backing.loc_x('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            bottom_backing.loc_x('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])

        bottom_backing.loc_z(
            'OB+BBO-IF(AND(B_Shelf,BIG>0),ST,0)',
            [OB,ST,BIB,BBO,B_Shelf,BIG]
        )

        bottom_backing.rot_x(value=math.radians(-90))
        bottom_backing.rot_y(value=math.radians(-90))
        bottom_backing.dim_x(
            'IF(B_Sections==3,IF(BBT==0,BIB-CH*2-BIA,BIB-ST),'
            'IF(TIB>0,Height-TIB-IF(BIG>0,BIG,0)+ST,BIB)-IF(BBT==0,CH*2-BIA*2,0)-ST-IF(AND(B_Shelf,BIG==0),ST,0))',
            [B_Sections,Height,CH,ST,TIB,BIB,BIA,T_Shelf,TBT,BX2T,BX2B,BBT,B_Cleat_Loc,B_Shelf,BIG]
        )
        bottom_backing.dim_y('opening_{}_width'.format(str(i)),[Width])
        bottom_backing.dim_z('IF(BBT==0,INCH(-0.25),INCH(-0.75))',[BBT])
        prompt = bottom_backing.get_prompt('Hide')
        prompt.set_formula('IF(OR(B_Sections==1,BTM==False,AND(B_Sections>1,IS_SB)),True,False) or Hide', [B_Sections,TOP,BTM,IS_SB,self.hide_var])                

        #Additional cleats for multi-section backing
        #BC3 - [0:'Full', 1:'Top', 2:'Bottom', 3:'Center', 4:'Top & Center', 5:'Bottom & Center', 6:'Top & Bottom']
        top_sec_bottom_cleat = self.add_backing_cleat(i, panel, top_cleat=False)
        parts.append(top_sec_bottom_cleat)
        prompt = top_sec_bottom_cleat.get_prompt('Hide')
        prompt.set_formula('IF(OR(TBT==1,TOP==False,B_Sections==1,AND(B_Sections>1,IS_SB)),True,False) or Hide',
            [B_Sections,TBT,TOP,BTM,IS_SB, self.hide_var])

        top_sec_bottom_cleat.loc_z('IF(B_Sections==2,IF(TIB>0,OB+Height-TIB+ST,IF(BIB>0,OB+BIB,0)),IF(B_Sections==3,OB+Height-TIB+ST,0))',[Height,OB,TIB,BIB,ST,B_Sections])

        mid_sec_top_cleat = self.add_backing_cleat(i, panel, top_cleat=True)
        parts.append(mid_sec_top_cleat)
        prompt = mid_sec_top_cleat.get_prompt('Hide')
        prompt.set_formula(
            'IF(OR(AND(B_Sections==3,BC3==5,CTR,BTM,CBT==0,IS_SB),AND(B_Sections==3,CTR,CBT==0,IS_SB==False)),False,True) or Hide',
            [B_Sections,CTR,BTM,CBT,IS_SB,BC3, self.hide_var])
        mid_sec_top_cleat.loc_z('OB+Height-TIB', [Height, OB, TIB])

        mid_sec_bottom_cleat = self.add_backing_cleat(i, panel, top_cleat=False)
        parts.append(mid_sec_bottom_cleat)
        prompt = mid_sec_bottom_cleat.get_prompt('Hide')
        prompt.set_formula('IF(AND(B_Sections==3,CTR,CBT==0,IS_SB==False),False,True) or Hide', [B_Sections, CTR, CBT, IS_SB, self.hide_var])
        mid_sec_bottom_cleat.loc_z('OB+BIB', [OB, BIB])

        bottom_sec_top_cleat = self.add_backing_cleat(i, panel, top_cleat=True)
        parts.append(bottom_sec_top_cleat)
        prompt = bottom_sec_top_cleat.get_prompt('Hide')
        prompt.set_formula('IF(OR(BBT==1,BTM==False,B_Sections==1,AND(B_Sections>1,IS_SB)),True,False) or Hide',
            [B_Sections,BBT,TOP,BTM,IS_SB, self.hide_var])

        bottom_sec_top_cleat.loc_z('IF(B_Sections==2,IF(TIB>0,OB+Height-TIB,IF(BIB>0,OB+BIB-ST,0)),IF(B_Sections==3,OB+BIB-ST,0))', [Height, OB, TIB, BIB, ST, B_Sections])
        prompt = bottom_sec_top_cleat.get_prompt('Use Cleat Cover')
        prompt.set_formula('IF(BIB>0,False,True)', [BIB])

        self.backing_parts[str(i)] = parts

        Add_Hanging_Rail = self.get_prompt('Add Hanging Rail').get_var('Add_Hanging_Rail')
        self.update_cleats(i, [B_Cleat, Add_Hanging_Rail, TBT, BIB, BIG, BBT, CBT, B_Sections, TOP, CTR, BTM, IS_SB, self.hide_var])
        self.update_backing_sections(i, backing)

    def add_hutch_backing(self):
        Add_Hutch_Backing = self.get_prompt("Add Hutch Backing").get_var()
        Has_Capping_Bottom = self.get_prompt("Has Capping Bottom").get_var()
        Extend_Left_End_Pard_Down = self.get_prompt("Extend Left End Pard Down").get_var()
        Extend_Right_End_Pard_Down = self.get_prompt("Extend Right End Pard Down").get_var()
        Height_Left_Side = self.get_prompt("Height Left Side").get_var()
        Height_Right_Side = self.get_prompt("Height Right Side").get_var()
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Product_Height = self.obj_z.snap.get_var('location.z','Product_Height')
        Height_1 = self.get_prompt('Opening 1 Height').get_var('Height_1')
        Last_Height = self.get_prompt('Opening ' + str(self.opening_qty) + ' Height').get_var("Last_Height")
        Panel_Thickness = self.get_prompt("Panel Thickness").get_var()

        hutch_backing = common_parts.add_back(self)
        hutch_backing.obj_bp.sn_closets.is_hutch_back_bp = True
        hutch_backing.obj_bp.snap.name_object = "Hutch Backing"
        hutch_backing.loc_x("Panel_Thickness",[Panel_Thickness])
        hutch_backing.loc_z(
            "Product_Height-IF(Height_1>=Last_Height,Height_1,Last_Height)-IF(Has_Capping_Bottom,Panel_Thickness,0)",
            [Product_Height, Height_1, Last_Height, Has_Capping_Bottom, Panel_Thickness])
        hutch_backing.rot_x(value=math.radians(-90))
        hutch_backing.dim_x("Width-(Panel_Thickness*2)",[Width,Panel_Thickness])
        hutch_backing.dim_y(
            "IF(Height_Left_Side>=Height_Right_Side,Height_Left_Side,Height_Right_Side)"
            "-IF(Has_Capping_Bottom,Panel_Thickness,0)",
            [Height_Left_Side, Height_Right_Side, Has_Capping_Bottom, Panel_Thickness])
        hutch_backing.dim_z("-Panel_Thickness", [Panel_Thickness])
        hutch_backing.get_prompt('Hide').set_formula(
            "IF(OR(Extend_Left_End_Pard_Down,Extend_Right_End_Pard_Down),IF(Add_Hutch_Backing,False,True),True) or Hide",
            [Extend_Left_End_Pard_Down, Extend_Right_End_Pard_Down, Add_Hutch_Backing,self.hide_var])

    def add_system_holes(self,i,panel):
        calculator = self.get_calculator(self.calculator_name)
        Product_Height = self.obj_z.snap.get_var('location.z', "Product_Height")
        width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))        
        Height = self.get_prompt('Opening ' + str(i) + ' Height').get_var('Height')
        Depth = self.get_prompt('Opening ' + str(i) + ' Depth').get_var('Depth')
        Floor = self.get_prompt('Opening ' + str(i) + ' Floor Mounted').get_var('Floor')
        self.add_prompt('Opening ' + str(i) + ' Add Backing', 'CHECKBOX', False)
        Add_Backing = self.get_prompt('Opening ' + str(i) + ' Add Backing').get_var('Add_Backing')
        Back_Thickness = self.get_prompt('Back Thickness').get_var('Back_Thickness')
        Left_End_Condition = self.get_prompt('Left End Condition').get_var('Left_End_Condition')
        Right_End_Condition = self.get_prompt('Right End Condition').get_var('Right_End_Condition')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Front_Angle_Height = self.get_prompt('Front Angle Height').get_var('Front_Angle_Height')
        Front_Angle_Depth = self.get_prompt('Front Angle Depth').get_var('Front_Angle_Depth')
        DDFF = self.get_prompt("Drilling Distance From Front").get_var('DDFF')
        DDFR = self.get_prompt("Drilling Distance From Rear").get_var('DDFR')
        Stop_LB = self.get_prompt("Opening " + str(i) + " Stop LB").get_var('Stop_LB')
        Start_LB = self.get_prompt("Opening " + str(i) + " Start LB").get_var('Start_LB')
        Drill_Thru_Left = self.get_prompt("Opening " + str(i) + " Drill Thru Left").get_var('Drill_Thru_Left')
        Drill_Thru_Right = self.get_prompt("Opening " + str(i) + " Drill Thru Right").get_var('Drill_Thru_Right')
        Add_Mid = self.get_prompt("Opening " + str(i) + " Add Mid Drilling").get_var('Add_Mid')
        Remove_Left = self.get_prompt("Opening " + str(i) + " Remove Left Drill").get_var('Remove_Left')
        Remove_Right = self.get_prompt("Opening " + str(i) + " Remove Right Drill").get_var('Remove_Right')
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var('Panel_Thickness')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')        
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x', 'X_Loc')
        else:
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            
        assemblies = []
        
        lfb_holes = common_parts.add_line_bore_holes(self)
        lfb_holes.set_name("Left Front Bottom Holes " + str(i))
        assemblies.append(lfb_holes)
        lrb_holes = common_parts.add_line_bore_holes(self)
        lrb_holes.set_name("Left Rear Bottom Holes " + str(i))
        assemblies.append(lrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Right Front Bottom Holes " + str(i))
        assemblies.append(rfb_holes)
        
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Rear Bottom Holes " + str(i))
        assemblies.append(rrb_holes)
        lfb_holes = common_parts.add_line_bore_holes(self)
        lfb_holes.set_name("Left Front Top Holes " + str(i))
        assemblies.append(lfb_holes)
        lrb_holes = common_parts.add_line_bore_holes(self)
        lrb_holes.set_name("Left Rear Top Holes " + str(i))
        assemblies.append(lrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Right Front Top Holes " + str(i))
        assemblies.append(rfb_holes)
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Rear Top Holes " + str(i))
        assemblies.append(rrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Left Mid Top Holes " + str(i))
        assemblies.append(rfb_holes)
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Mid Top Holes " + str(i))
        assemblies.append(rrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Left Mid Bottom Holes " + str(i))
        assemblies.append(rfb_holes)
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Mid Bottom Holes " + str(i))
        assemblies.append(rrb_holes)
        
        ch_tfl_holes = common_parts.add_line_bore_holes(self)
        ch_tfl_holes.set_name("Chamfer Top Front Left Holes " + str(i))
        ch_tfl_holes.rot_y(value=math.radians(90))
        ch_tfl_holes.rot_z(value=math.radians(180))
        ch_tfl_holes.dim_z('IF(Drill_Thru_Left,Panel_Thickness+INCH(.02),INCH(.2))',[Drill_Thru_Left,Panel_Thickness])
        ch_tfl_holes.loc_y("-Depth-IF(Add_Backing,Back_Thickness,0)+Front_Angle_Depth+DDFF",[Depth,Add_Backing,Front_Angle_Depth,Back_Thickness,DDFF])
        ch_tfl_holes.dim_x('Front_Angle_Height',[Front_Angle_Height])
        ch_tfl_holes.loc_z('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])

        if panel:
            ch_tfl_holes.loc_x('X_Loc+INCH(.01)',[X_Loc])
        else:
            ch_tfl_holes.loc_x('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler])
        
        if i == 1:                  #FIRST OPENING
            ch_tfl_holes.get_prompt('Hide').set_formula('IF(Front_Angle_Height==0,True,IF(Left_End_Condition!=3,IF(Remove_Left,True,False),True))',[Front_Angle_Height,Left_End_Condition,Remove_Left])
        elif i == self.opening_qty: #LAST OPENING
            ch_tfl_holes.get_prompt('Hide').set_formula('IF(Front_Angle_Height==0,True,IF(Right_End_Condition!=3,IF(Remove_Left,True,False),True))',[Front_Angle_Height,Right_End_Condition,Remove_Left])
        else:                       #MIDDLE OPENING
            ch_tfl_holes.get_prompt('Hide').set_formula('IF(Front_Angle_Height==0,True,IF(Remove_Left,True,False)) or Hide',[Front_Angle_Height,Remove_Left, self.hide_var])    
            
        ch_tfr_holes = common_parts.add_line_bore_holes(self)
        ch_tfr_holes.set_name("Chamfer Top Front Right Holes " + str(i))
        ch_tfr_holes.rot_y(value=math.radians(90))
        ch_tfr_holes.rot_z(value=math.radians(180))
        ch_tfr_holes.dim_z('IF(Drill_Thru_Right,-Panel_Thickness-INCH(.02),-INCH(.2))',[Drill_Thru_Right,Panel_Thickness])
        ch_tfr_holes.loc_y("-Depth-IF(Add_Backing,Back_Thickness,0)+Front_Angle_Depth+DDFF",[Depth,Add_Backing,Front_Angle_Depth,Back_Thickness,DDFF])
        ch_tfr_holes.dim_x('Front_Angle_Height',[Front_Angle_Height])
        ch_tfr_holes.loc_z('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])
        
        if panel:
            ch_tfr_holes.loc_x('X_Loc+Width-INCH(.01)',[X_Loc,Width])
        else:
            ch_tfr_holes.loc_x('X_Loc+Left_Side_Wall_Filler+Width-INCH(.01)',[X_Loc,Width,Left_Side_Wall_Filler])        
        
        if i == 1:                  #FIRST OPENING
            ch_tfr_holes.get_prompt('Hide').set_formula('IF(Front_Angle_Height==0,True,IF(Left_End_Condition!=3,IF(Remove_Right,True,False),True))',[Left_End_Condition,Remove_Right,Front_Angle_Height])
        elif i == self.opening_qty: #LAST OPENING
            ch_tfr_holes.get_prompt('Hide').set_formula('IF(Front_Angle_Height==0,True,IF(Right_End_Condition!=3,IF(Remove_Right,True,False),True))',[Right_End_Condition,Remove_Right,Front_Angle_Height])
        else:                       #MIDDLE OPENING
            ch_tfr_holes.get_prompt('Hide').set_formula('IF(Front_Angle_Height==0,True,IF(Remove_Right,True,False)) or Hide',[Remove_Right,Front_Angle_Height, self.hide_var])     
            
        ch_trl_holes = common_parts.add_line_bore_holes(self)
        ch_trl_holes.set_name("Chamfer Top Rear Left Holes " + str(i))
        ch_trl_holes.rot_y(value=math.radians(90))
        ch_trl_holes.rot_z(value=math.radians(180))
        ch_trl_holes.dim_z('IF(Drill_Thru_Left,Panel_Thickness+INCH(.02),INCH(.2))',[Drill_Thru_Left,Panel_Thickness])
        ch_trl_holes.loc_y("-IF(Add_Backing,Back_Thickness,0)-DDFR",[Depth,Add_Backing,Back_Thickness,DDFR])
        ch_trl_holes.dim_x(value=0)
        ch_trl_holes.loc_z('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])

        if panel:
            ch_trl_holes.loc_x('X_Loc+INCH(.01)',[X_Loc])
        else:
            ch_trl_holes.loc_x('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler])
        
        if i == 1:                  #FIRST OPENING
            ch_trl_holes.get_prompt('Hide').set_formula('IF(Left_End_Condition!=3,IF(Remove_Left,True,False),True)',[Left_End_Condition,Remove_Left])
        elif i == self.opening_qty: #LAST OPENING
            ch_trl_holes.get_prompt('Hide').set_formula('IF(Right_End_Condition!=3,IF(Remove_Left,True,False),True)',[Right_End_Condition,Remove_Left])
        else:                       #MIDDLE OPENING
            ch_trl_holes.get_prompt('Hide').set_formula('IF(Remove_Left,True,False) or Hide',[Remove_Left, self.hide_var])    
            
        ch_trr_holes = common_parts.add_line_bore_holes(self)
        ch_trr_holes.set_name("Chamfer Top Rear Right Holes " + str(i))
        ch_trr_holes.rot_y(value=math.radians(90))
        ch_trr_holes.rot_z(value=math.radians(180))
        ch_trr_holes.dim_z('IF(Drill_Thru_Right,-Panel_Thickness-INCH(.02),-INCH(.2))',[Drill_Thru_Right,Panel_Thickness])
        ch_trr_holes.loc_y("-IF(Add_Backing,Back_Thickness,0)-DDFR",[Depth,Add_Backing,Back_Thickness,DDFR])
        ch_trr_holes.dim_x(value=0)
        ch_trr_holes.loc_z('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])
        
        if panel:
            ch_trr_holes.loc_x('X_Loc+Width-INCH(.01)',[X_Loc,Width])
        else:
            ch_trr_holes.loc_x('X_Loc+Left_Side_Wall_Filler+Width-INCH(.01)',[X_Loc,Width,Left_Side_Wall_Filler])        
        
        if i == 1:                  #FIRST OPENING
            ch_trr_holes.get_prompt('Hide').set_formula('IF(Left_End_Condition!=3,IF(Remove_Right,True,False),True)',[Left_End_Condition,Remove_Right])
        elif i == self.opening_qty: #LAST OPENING
            ch_trr_holes.get_prompt('Hide').set_formula('IF(Right_End_Condition!=3,IF(Remove_Right,True,False),True)',[Right_End_Condition,Remove_Right])
        else:                       #MIDDLE OPENING
            ch_trr_holes.get_prompt('Hide').set_formula('IF(Remove_Right,True,False) or Hide',[Remove_Right, self.hide_var])                  

        for assembly in assemblies: 
            assembly.rot_y(value=math.radians(-90))
            shelf_hole_spacing = assembly.get_prompt('Shelf Hole Spacing')
            if shelf_hole_spacing:
                shelf_hole_spacing.set_value(sn_unit.inch(1.2598))
            
            if "Left" in assembly.obj_bp.snap.name_object:
                if panel:
                    assembly.loc_x('X_Loc+INCH(.01)',[X_Loc])
                else:
                    assembly.loc_x('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler])
                assembly.dim_z('IF(Drill_Thru_Left,Panel_Thickness+INCH(.02),INCH(.2))',[Drill_Thru_Left,Panel_Thickness])

                if "Top" in assembly.obj_bp.snap.name_object:
                    if i == 1:                  #FIRST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Left_End_Condition!=3,IF(OR(Remove_Left,Start_LB==0),True,False),True)',[Left_End_Condition,Remove_Left,Start_LB])
                    elif i == self.opening_qty: #LAST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Right_End_Condition!=3,IF(OR(Remove_Left,Start_LB==0),True,False),True)',[Right_End_Condition,Remove_Left,Start_LB])
                    else:                       #MIDDLE OPENING
                        assembly.get_prompt('Hide').set_formula('IF(OR(Remove_Left,Start_LB==0),True,False) or Hide',[Remove_Left,Start_LB, self.hide_var])
                else:
                    if i == 1:                  #FIRST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Left_End_Condition!=3,IF(Remove_Left,True,False),True)',[Left_End_Condition,Remove_Left])
                    elif i == self.opening_qty: #LAST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Right_End_Condition!=3,IF(Remove_Left,True,False),True)',[Right_End_Condition,Remove_Left])
                    else:                       #MIDDLE OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Remove_Left,True,False) or Hide',[Remove_Left, self.hide_var])
            
            if "Right" in assembly.obj_bp.snap.name_object:
                if panel:
                    assembly.loc_x('X_Loc+Width-INCH(.01)',[X_Loc,Width])
                else:
                    assembly.loc_x('X_Loc+Left_Side_Wall_Filler+Width-INCH(.01)',[X_Loc,Width,Left_Side_Wall_Filler])
                assembly.dim_z('IF(Drill_Thru_Right,-Panel_Thickness-INCH(.02),-INCH(.2))',[Drill_Thru_Right,Panel_Thickness])

                if "Top" in assembly.obj_bp.snap.name_object:
                    if i == 1:                  #FIRST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Left_End_Condition!=3,IF(OR(Remove_Right,Start_LB==0),True,False),True)',[Left_End_Condition,Remove_Right,Start_LB])
                    elif i == self.opening_qty: #LAST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Right_End_Condition!=3,IF(OR(Remove_Right,Start_LB==0),True,False),True)',[Right_End_Condition,Remove_Right,Start_LB])
                    else:                       #MIDDLE OPENING
                        assembly.get_prompt('Hide').set_formula('IF(OR(Remove_Right,Start_LB==0),True,False) or Hide',[Remove_Right,Start_LB, self.hide_var])
                else:
                    if i == 1:                  #FIRST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Left_End_Condition!=3,IF(Remove_Right,True,False),True)',[Left_End_Condition,Remove_Right])
                    elif i == self.opening_qty: #LAST OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Right_End_Condition!=3,IF(Remove_Right,True,False),True)',[Right_End_Condition,Remove_Right])
                    else:                       #MIDDLE OPENING
                        assembly.get_prompt('Hide').set_formula('IF(Remove_Right,True,False) or Hide',[Remove_Right, self.hide_var])

            if "Top" in assembly.obj_bp.snap.name_object:
                assembly.rot_y(value=math.radians(90))
                assembly.rot_z(value=math.radians(180))
                assembly.loc_z('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Product_Height,Height])
                assembly.dim_x('Start_LB',[Start_LB])

            if "Bottom" in assembly.obj_bp.snap.name_object:
                assembly.loc_z('IF(Floor,MILLIMETER(9.525)+Toe_Kick_Height,Product_Height-Height+MILLIMETER(9.525))',[Floor,Toe_Kick_Height,Product_Height,Height])
                if "Front" in assembly.obj_bp.snap.name_object:
                    assembly.dim_x('IF(Stop_LB>0,Stop_LB,Height-Front_Angle_Height)',[Height,Stop_LB,Front_Angle_Height])
                if "Rear" in assembly.obj_bp.snap.name_object:
                    assembly.dim_x('IF(Stop_LB>0,Stop_LB,Height)',[Height,Stop_LB])
                    
            if "Front" in assembly.obj_bp.snap.name_object:
                assembly.loc_y("-Depth-IF(Add_Backing,Back_Thickness,0)+DDFF",[Depth,Add_Backing,Back_Thickness,DDFF])
            
            if "Rear" in assembly.obj_bp.snap.name_object:
                assembly.loc_y("-IF(Add_Backing,Back_Thickness,0)-DDFR",[Add_Backing,Back_Thickness,DDFR])
            
            if "Mid" in assembly.obj_bp.snap.name_object:
                assembly.loc_y("-IF(Add_Backing,Back_Thickness,0)-INCH(12)+DDFF",[Add_Backing,Back_Thickness,DDFF])
                if "Left" in assembly.obj_bp.snap.name_object:
                    if "Top" in assembly.obj_bp.snap.name_object:
                        assembly.get_prompt('Hide').set_formula('IF(OR(Remove_Left,Start_LB==0),True,IF(Add_Mid,False,True)) or Hide',[Remove_Left,Start_LB,Add_Mid, self.hide_var])
                    else:
                        assembly.get_prompt('Hide').set_formula('IF(Remove_Left,True,IF(Add_Mid,False,True)) or Hide',[Remove_Left,Add_Mid, self.hide_var])
                if "Right" in assembly.obj_bp.snap.name_object:
                    if "Top" in assembly.obj_bp.snap.name_object:
                        assembly.get_prompt('Hide').set_formula('IF(OR(Remove_Right,Start_LB==0),True,IF(Add_Mid,False,True)) or Hide',[Remove_Right,Start_LB,Add_Mid, self.hide_var])
                    else:
                        assembly.get_prompt('Hide').set_formula('IF(Remove_Right,True,IF(Add_Mid,False,True)) or Hide',[Remove_Right,Add_Mid, self.hide_var]) 

    def add_blind_panel_holes(self, panel):
        Width = panel.obj_x.snap.get_var('location.x','Width')
        Depth = panel.obj_y.snap.get_var("location.y", 'Depth')
        Height = panel.obj_z.snap.get_var("location.z", 'Height')
        DDFF = self.get_prompt("Drilling Distance From Front").get_var('DDFF')
        left_bcp = panel.get_prompt("Is Left Blind Corner Panel")
        right_bcp = panel.get_prompt("Is Right Blind Corner Panel")
        Blind_Corner_Left = self.get_prompt("Blind Corner Left").get_var('Blind_Corner_Left')
        Blind_Corner_Right = self.get_prompt("Blind Corner Right").get_var('Blind_Corner_Right')        

        if left_bcp.get_value():
            rbf_holes = common_parts.add_line_bore_holes(panel)
            rbf_holes.set_name("Right Bottom Front Holes")
            rbf_holes.loc_x('-INCH(0.455)+MILLIMETER(9.5)+MILLIMETER(32)',[Depth, DDFF])
            rbf_holes.loc_y('Depth-DDFF',[Depth, DDFF])
            rbf_holes.loc_z('Height+INCH(0.01)',[Height])
            rbf_holes.rot_x(value=math.radians(180))
            rbf_holes.dim_x('Width+INCH(0.455)-MILLIMETER(9.5)-MILLIMETER(32)',[Width])
            rbf_holes.dim_z(value=sn_unit.inch(0.5))
            rbf_holes.get_prompt("Hide").set_formula("IF(Blind_Corner_Left,False,True) or Hide",[Blind_Corner_Left,self.hide_var])

        if right_bcp.get_value():
            lbf_holes = common_parts.add_line_bore_holes(panel)
            lbf_holes.set_name("Left Bottom Front Holes")
            lbf_holes.loc_x('-INCH(0.455)+MILLIMETER(9.5)+MILLIMETER(32)',[Depth, DDFF])
            lbf_holes.loc_y('Depth-DDFF',[Depth, DDFF])
            lbf_holes.loc_z(value=sn_unit.inch(-0.01))
            lbf_holes.dim_x('Width+INCH(0.455)-MILLIMETER(9.5)-MILLIMETER(32)',[Width])
            lbf_holes.dim_z(value=sn_unit.inch(0.5))
            lbf_holes.get_prompt("Hide").set_formula("IF(Blind_Corner_Right,False,True) or Hide",[Blind_Corner_Right,self.hide_var])

    def add_blind_corners(self):
        Width = self.obj_x.snap.get_var("location.x", 'Width')
        Hanging_Height = self.obj_z.snap.get_var("location.z", 'Hanging_Height')
        Blind_Corner_Left = self.get_prompt("Blind Corner Left").get_var('Blind_Corner_Left')
        Blind_Corner_Left_Depth = self.get_prompt("Blind Corner Left Depth").get_var('Blind_Corner_Left_Depth')
        Blind_Corner_Right = self.get_prompt("Blind Corner Right").get_var('Blind_Corner_Right')
        Blind_Corner_Right_Depth = self.get_prompt("Blind Corner Right Depth").get_var('Blind_Corner_Right_Depth')
        First_Opening_Height = self.get_prompt("Opening 1 Height").get_var("First_Opening_Height")
        Last_Opening_Height = self.get_prompt("Opening " + str(self.opening_qty) + " Height").get_var("Last_Opening_Height")
        First_Opening_Depth = self.get_prompt("Opening 1 Depth").get_var( "First_Opening_Depth")
        Last_Opening_Depth = self.get_prompt("Opening " + str(self.opening_qty) + " Depth").get_var("Last_Opening_Depth")
        First_Floor_Mounted = self.get_prompt('Opening 1 Floor Mounted').get_var('First_Floor_Mounted')
        Last_Floor_Mounted = self.get_prompt('Opening '+ str(self.opening_qty) +' Floor Mounted').get_var('Last_Floor_Mounted')
        Panel_Thickness = self.get_prompt("Panel Thickness").get_var('Panel_Thickness')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        BCHD = self.get_prompt("Blind Corner Height Difference").get_var("BCHD")

        #Left Blind Corner Panel
        left_blind_panel = common_parts.add_panel(self)
        Vertical_Offset_1 = self.get_prompt("Top KD 1 Vertical Offset").get_var('Vertical_Offset')

        left_blind_panel.loc_y("-First_Opening_Depth-Panel_Thickness",[First_Opening_Depth,Panel_Thickness])
        left_blind_panel.loc_z('IF(First_Floor_Mounted,Toe_Kick_Height+(BCHD/2),Hanging_Height-First_Opening_Height+(BCHD/2))',
                                [First_Floor_Mounted,Toe_Kick_Height,BCHD,Hanging_Height,First_Opening_Height])

        left_blind_panel.rot_x(value=math.radians(90))
        left_blind_panel.rot_y(value=math.radians(-90))
        left_blind_panel.rot_z(value=math.radians(180))

        left_blind_panel.dim_x("First_Opening_Height-BCHD-Vertical_Offset",[First_Opening_Height,BCHD,Vertical_Offset_1])
        left_blind_panel.dim_y("Blind_Corner_Left_Depth",[Blind_Corner_Left_Depth])
        left_blind_panel.dim_z("Panel_Thickness", [Panel_Thickness])

        left_blind_panel.get_prompt("Hide").set_formula("IF(Blind_Corner_Left, False, True) or Hide",[Blind_Corner_Left,self.hide_var])
        left_blind_panel.get_prompt("Is Left Blind Corner Panel").set_value(value=True)
        left_blind_panel.get_prompt("CatNum").set_value(value=1004)
        left_blind_panel.obj_bp.snap.name_object = "Blind Corner Panel"
        left_blind_panel.obj_bp.sn_closets.is_panel_bp = False  # TODO: remove
        left_blind_panel.obj_bp['IS_BP_PANEL'] = False
        left_blind_panel.obj_bp.sn_closets.is_blind_corner_panel_bp = True  # TODO: remove
        left_blind_panel.obj_bp['IS_BP_BLIND_CORNER_PANEL'] = True
        self.add_blind_panel_holes(left_blind_panel)

        #Right Blind Corner Panel
        right_blind_panel = common_parts.add_panel(self)
        Vertical_Offset_Last = self.get_prompt("Top KD " + str(self.opening_qty) + " Vertical Offset").get_var('Vertical_Offset')
        right_blind_panel.loc_x("Width",[Width])
        right_blind_panel.loc_y("-Last_Opening_Depth",[Last_Opening_Depth])
        right_blind_panel.loc_z('IF(Last_Floor_Mounted,Toe_Kick_Height+(BCHD/2),Hanging_Height-Last_Opening_Height+(BCHD/2))',
                                [Last_Floor_Mounted,Toe_Kick_Height,BCHD,Hanging_Height,Last_Opening_Height])

        right_blind_panel.rot_x(value=math.radians(90))
        right_blind_panel.rot_y(value=math.radians(-90))

        right_blind_panel.dim_x("Last_Opening_Height-BCHD-Vertical_Offset",[Last_Opening_Height,BCHD,Vertical_Offset_Last])
        right_blind_panel.dim_y("Blind_Corner_Right_Depth",[Blind_Corner_Right_Depth])
        right_blind_panel.dim_z("Panel_Thickness", [Panel_Thickness])

        right_blind_panel.get_prompt("Hide").set_formula("IF(Blind_Corner_Right,False,True) or Hide",[Blind_Corner_Right,self.hide_var])
        right_blind_panel.get_prompt("Is Right Blind Corner Panel").set_value(value=True)
        right_blind_panel.get_prompt("CatNum").set_value(value=1004)
        right_blind_panel.obj_bp.snap.name_object = "Blind Corner Panel"
        right_blind_panel.obj_bp.sn_closets.is_panel_bp = False  # TODO: remove
        right_blind_panel.obj_bp['IS_BP_PANEL'] = False
        right_blind_panel.obj_bp.sn_closets.is_blind_corner_panel_bp = True  # TODO: remove
        right_blind_panel.obj_bp['IS_BP_BLIND_CORNER_PANEL'] = True
        self.add_blind_panel_holes(right_blind_panel)

    def pre_draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.obj_bp['product_type'] = "Closet"

        product_props = self.obj_bp.sn_closets
        product_props.opening_name = str(self.opening_qty)
        self.obj_x.location.x = self.width
        self.obj_z.location.z = self.height
        self.obj_y.location.y = -self.depth        
        
        if self.defaults.export_subassemblies:
            self.obj_bp.snap.export_product_subassemblies = True

        common_prompts.add_thickness_prompts(self)
        common_prompts.add_closet_carcass_prompts(self)
        self.add_opening_prompts()

        self.add_sides()
        panel = None
        self.add_shelf(1, panel, is_top=True)
        self.add_shelf(1, panel, is_top=False)
        # self.add_backing(1, panel)
        self.add_closet_opening(1, panel)
        self.add_hutch_backing()
        # if self.defaults.show_panel_drilling:
        #     self.add_system_holes(1, panel)
        if self.defaults.add_top_cleat:
            self.add_top_cleat(1, panel)
        if self.defaults.add_bottom_cleat:
            self.add_bottom_cleat(1, panel)
        
        # Add partitions
        for i in range(2, self.opening_qty + 1):
            panel = self.add_panel(i, panel)
            panel.obj_bp['PARTITION_NUMBER'] = (i - 1)
            self.add_shelf(i,panel,is_top=True)
            self.add_shelf(i,panel,is_top=False)
            # self.add_backing(i,panel)
            self.add_closet_opening(i,panel)
            # if self.defaults.show_panel_drilling:
            #     self.add_system_holes(i, panel)
            if self.defaults.add_top_cleat:
                self.add_top_cleat(i, panel)
            if self.defaults.add_bottom_cleat:
                self.add_bottom_cleat(i, panel)

        self.add_blind_corners()

    def draw(self):
        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["ID_PROMPT"] = "sn_closets.openings" 
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.update()

        calculator = self.get_calculator('Opening Widths Calculator')
        if calculator:
            calculator.calculate()
            if bpy.context.area:
                bpy.context.area.tag_redraw()

             
class OPERATOR_Closet_Standard_Draw_Plan(Operator):
    bl_idname = "sn_closets.draw_plan"
    bl_label = "Draw Closet Plan View"
    bl_description = "Creates the plan view for closets"
    
    object_name: StringProperty(name="Object Name",default="")
    
    product = None

    def draw_closet_top(self,obj):
        if 'top shelf' in obj.name.lower():
            self.add_applied_top(obj)
        for child in obj.children:
            self.draw_closet_top(child)

    def draw_corner_shelf(self, obj):
        csh_height = sn_types.Assembly(obj).obj_z.location.z
        if 'corner shelves' in obj.name.lower():
            for panel in obj.children:
                if 'left panel' in panel.name.lower():
                    self.copy_kd_part(panel)
            csh_assy = sn_types.Assembly(obj)
            has_top_shelf = csh_assy.get_prompt("Add Top Shelf").get_value()
            if has_top_shelf:
                for tshelf in obj.children:
                    if 'angled top shelf' in tshelf.name.lower():
                        tshelf_assy = sn_types.Assembly(tshelf)
                        t_x_dim = tshelf_assy.obj_x.location.x
                        t_y_dim = tshelf_assy.obj_y.location.y
                        t_z_dim = tshelf_assy.obj_z.location.z
                        t_size = (t_x_dim, t_y_dim, t_z_dim)
                        t_left_depth = tshelf_assy.get_prompt("Left Depth").get_value()
                        t_right_depth = tshelf_assy.get_prompt("Right Depth").get_value()
                        t_chamfer_mesh = sn_utils.create_chamfer_cube_mesh('tsh_mesh',
                                                                           t_size,
                                                                           t_left_depth,
                                                                           t_right_depth)
                        t_chamfer_mesh.parent = obj
                        t_chamfer_mesh.location[2] = csh_height
                        t_chamfer_mesh['IS_CAGE'] = True
            for shelf in obj.children:
                if 'angle shelf' in shelf.name.lower():
                    assy = sn_types.Assembly(shelf)
                    x_dim = assy.obj_x.location.x
                    y_dim = assy.obj_y.location.y
                    z_dim = assy.obj_z.location.z
                    left_depth = assy.get_prompt('Left Depth').get_value()
                    right_depth = assy.get_prompt('Right Depth').get_value()
                    size = (x_dim, y_dim, z_dim)
                    chamfer_mesh = sn_utils.create_chamfer_cube_mesh('csh_mesh', 
                                                                     size, 
                                                                     left_depth, 
                                                                     right_depth)
                    chamfer_mesh.parent = obj
                    chamfer_mesh.location[2] = csh_height + sn_unit.inch(10)
                    chamfer_mesh['IS_CAGE'] = True
                    return


    def copy_kd_part(self, shelf):
        assembly_copy = shelf.copy()
        bpy.context.scene.collection.objects.link(assembly_copy)
        for child in shelf.children:
            child_copy = child.copy()
            child_copy.parent = assembly_copy
            bpy.context.scene.collection.objects.link(child_copy)

    def draw_l_shelf(self, obj):
        lsh_height = sn_types.Assembly(obj).obj_z.location.z
        if 'l shelves' in obj.name.lower():
            lsh_assy = sn_types.Assembly(obj)
            has_top_shelf = lsh_assy.get_prompt("Add Top Shelf").get_value()
            has_top_kd = lsh_assy.get_prompt("Add Top KD").get_value()
            for panel in obj.children:
                if 'left panel' in panel.name.lower():
                    self.copy_kd_part(panel)
            if has_top_shelf:
                assy = sn_types.Assembly(obj)
                t_x_dim = assy.obj_x.location.x
                t_y_dim = assy.obj_y.location.y
                t_z_dim = sn_unit.inch(0.75)
                t_ld_value = assy.get_prompt('Left Depth').get_value()
                t_rd_value = assy.get_prompt('Right Depth').get_value()
                t_left_depth = t_ld_value + sn_unit.inch(0.5)
                t_right_depth = t_rd_value + sn_unit.inch(0.5)
                size = (t_x_dim, t_y_dim, t_z_dim)
                t_mesh = sn_utils.create_pie_cut_mesh('lsh_msh', 
                                                    size, 
                                                    t_left_depth, 
                                                    t_right_depth)
                t_mesh.parent = obj
                t_mesh.location[2] = lsh_height
                t_mesh['IS_CAGE'] = True
            if has_top_kd:
                assy = sn_types.Assembly(obj)
                x_dim = assy.obj_x.location.x - sn_unit.inch(0.75)
                y_dim = assy.obj_y.location.y + sn_unit.inch(0.75)
                z_dim = sn_unit.inch(0.75)
                left_depth_value = assy.get_prompt('Left Depth').get_value()
                right_depth_value = assy.get_prompt('Right Depth').get_value()
                left_depth = left_depth_value
                right_depth = right_depth_value
                size = (x_dim, y_dim, z_dim)
                mesh = sn_utils.create_pie_cut_mesh('lsh_msh', 
                                                    size, 
                                                    left_depth, 
                                                    right_depth)
                mesh.parent = obj
                mesh.location[2] = lsh_height + sn_unit.inch(10)
                mesh['IS_CAGE'] = True
        
    def add_applied_top(self,obj):
        parent_csh = 'corner shelves' in obj.parent.name.lower()
        parent_lsh = 'l shelves' in obj.parent.name.lower()
        if parent_csh or parent_lsh:
            return
        top = sn_types.Assembly(obj)
        
        extend_left = top.get_prompt("Extend To Left Panel")
        extend_right = top.get_prompt("Extend To Right Panel")
        extend_left_amount = top.get_prompt("Extend Left Amount")
        extend_right_amount = top.get_prompt("Extend Right Amount")
        front_overhang = top.get_prompt("Front Overhang")
        panel_thickness = top.get_prompt("Panel Thickness")
        
        overlay_left = 0 if extend_left.get_value() else -(panel_thickness.get_value()/2)
        overlay_right = 0 if extend_right.get_value() else -(panel_thickness.get_value()/2)
        
        length = top.obj_x.location.x + extend_left_amount.get_value() + extend_right_amount.get_value() + overlay_left + overlay_right
        width = -top.obj_y.location.y - front_overhang.get_value()
        
        closet_top = sn_utils.create_cube_mesh(top.obj_bp.snap.name_object,(length,width,panel_thickness.get_value()))
        closet_top.parent = self.product.obj_bp.parent
        closet_top.location = self.product.obj_bp.location
        closet_top.location.x += top.obj_bp.location.x
        closet_top.location.x -= extend_left_amount.get_value() + overlay_left
        closet_top.rotation_euler = self.product.obj_bp.rotation_euler
        closet_top['IS_CAGE'] = True

    def add_parts(self, parts):
        for part in parts:
            assembly = sn_types.Assembly(part)
            object_name = assembly.obj_bp.snap.name_object
            mesh_location = (assembly.obj_x.location.x,
                            assembly.obj_y.location.y,
                            assembly.obj_z.location.z)
            assembly_mesh = sn_utils.create_cube_mesh(object_name,
                                                      mesh_location)
            assembly_mesh.parent = part.parent
            assembly_mesh.location = assembly.obj_bp.location
            assembly_mesh.rotation_euler = assembly.obj_bp.rotation_euler
            assembly_mesh['IS_CAGE'] = True
                
    def execute(self, context):
        obj_bp = bpy.data.objects[self.object_name]
        self.product = sn_types.Assembly(obj_bp)
        a_product_chldrn = self.product.obj_bp.children
        openings = []
        partitions = []
        fillers = []
        self.draw_closet_top(self.product.obj_bp)
        self.draw_corner_shelf(self.product.obj_bp)
        self.draw_l_shelf(self.product.obj_bp)
        for child in a_product_chldrn:
            is_opening = 'opening' in child.name.lower()
            is_partition = 'partition' in child.name.lower()
            is_filler = 'filler' in child.name.lower()
            is_capping_filler = 'capping filler' in child.name.lower()
            is_perpendicular = child.rotation_euler[0] == math.radians(0)
            if is_opening:
                openings.append(child)
            elif is_partition and is_perpendicular:
                partitions.append(child)
            elif is_filler and not is_capping_filler:
                filler_assy = sn_types.Assembly(child)
                filler_size = abs(filler_assy.obj_y.location.y)
                if filler_size > 0:
                    fillers.append(child)
        self.add_parts(openings)
        self.add_parts(partitions)
        self.add_parts(fillers)
        return {'FINISHED'}


bpy.utils.register_class(OPERATOR_Closet_Standard_Draw_Plan)
