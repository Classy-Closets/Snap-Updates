from os import path
from snap.sn_unit import inch
import math

import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty

from snap import sn_types, sn_utils, sn_unit
from .. import closet_props
from ..common import common_prompts
from ..common import common_parts
from ..common import common_lists
from snap.libraries.closets import closet_paths


ASSEMBLY_DIR = path.join(common_parts.LIBRARY_DATA_DIR, "Assemblies")
PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR, "Part with Edgebanding.blend")
PART_WITH_NO_EDGEBANDING = path.join(ASSEMBLY_DIR, "Part with No Edgebanding.blend")
CORNER_NOTCH_PART = path.join(ASSEMBLY_DIR, "Corner Notch Part.blend")
CHAMFERED_PART = path.join(ASSEMBLY_DIR, "Chamfered Part.blend")
RADIUS_CORNER_PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR, "Radius Corner Part with Edgebanding.blend")
BENDING_PART = path.join(ASSEMBLY_DIR, "Bending Part.blend")


class L_Shelves(sn_types.Assembly):

    """
    This L Shelf Includes a Back Spine for support and is hanging first
    """

    category_name = ""
    type_assembly = "PRODUCT"
    id_prompt = "sn_closets.l_shelves"
    show_in_library = True
    placement_type = 'CORNER'

    def pre_draw(self):
        self.create_assembly()
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth
        self.obj_z.location.z = self.height

        props = bpy.context.scene.sn_closets

        self.add_prompt("Panel Height", 'DISTANCE', sn_unit.millimeter(2003))
        self.add_prompt("Back Inset", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Spine Width", 'DISTANCE', sn_unit.inch(1))
        self.add_prompt("Spine Y Location", 'DISTANCE', sn_unit.inch(2.1))
        self.add_prompt("Cleat Height", 'DISTANCE', sn_unit.inch(3.64))
        self.add_prompt("Left Depth", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Right Depth", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Shelf Quantity", 'QUANTITY', 3)
        self.add_prompt("Add Top KD", 'CHECKBOX', True)  # export=True
        self.add_prompt("Hide Toe Kick", 'CHECKBOX', False)  # export=True
        self.add_prompt("Add Backing", 'CHECKBOX', False)  # export=True
        self.add_prompt("Is Hanging", 'CHECKBOX', False)  # export=True
        self.add_prompt("Remove Left Side", 'CHECKBOX', False)  # export=True
        self.add_prompt("Remove Right Side", 'CHECKBOX', False)  # export=True
        self.add_prompt("Force Double Doors", 'CHECKBOX', False)  # export=True
        self.add_prompt("Door", 'CHECKBOX', False)  # export=True
        self.add_prompt("Door Pull Height", 'DISTANCE', sn_unit.inch(36))
        self.add_prompt("Backing Thickness", 'DISTANCE', sn_unit.inch(0.75))

        self.add_prompt("Door Type", 'COMBOBOX', 0, ["Reach Back", "Lazy Susan"])
        self.add_prompt("Open Door", 'PERCENTAGE', 0)
        self.add_prompt("Door Rotation", 'QUANTITY', 120)
        self.add_prompt("Half Open", 'PERCENTAGE', 0.5)
        self.add_prompt("Pull Type", 'COMBOBOX', 1, ["Base", "Tall", "Upper"])
        self.add_prompt("Pull Location", 'COMBOBOX', 0, ["Pull on Left Door", "Pull on Right Door"])

        self.add_prompt("Add Top Shelf", 'CHECKBOX', False)
        self.add_prompt("Exposed Left", 'CHECKBOX', False)
        self.add_prompt("Exposed Right", 'CHECKBOX', False)
        self.add_prompt("Top Shelf Overhang", 'DISTANCE', sn_unit.inch(0.5))
        self.add_prompt("Extend Left", 'DISTANCE', 0)
        self.add_prompt("Extend Right", 'DISTANCE', 0)

        self.add_prompt("Add Left Filler", 'CHECKBOX', False)
        self.add_prompt("Add Right Filler", 'CHECKBOX', False)
        self.add_prompt("Left Side Wall Filler", 'DISTANCE', 0.0)
        self.add_prompt("Right Side Wall Filler", 'DISTANCE', 0.0)
        self.add_prompt("Add Capping Left Filler", 'CHECKBOX', False)
        self.add_prompt("Add Capping Right Filler", 'CHECKBOX', False)
        self.add_prompt("Left Filler Setback Amount", 'DISTANCE', 0.0)
        self.add_prompt("Right Filler Setback Amount", 'DISTANCE', 0.0)
        self.add_prompt("Edge Bottom of Left Filler", 'CHECKBOX', False)
        self.add_prompt("Edge Bottom of Right Filler", 'CHECKBOX', False)

        for i in range(1, 11):
            self.add_prompt("Shelf " + str(i) + " Height", 'DISTANCE', sn_unit.millimeter(653.034))

        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_door_prompts(self)
        common_prompts.add_door_pull_prompts(self)

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Panel_Height = self.get_prompt('Panel Height').get_var('Panel_Height')
        Left_Depth = self.get_prompt('Left Depth').get_var('Left_Depth')
        Right_Depth = self.get_prompt('Right Depth').get_var('Right_Depth')
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        PT = self.get_prompt('Panel Thickness').get_var("PT")
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Toe_Kick_Setback = self.get_prompt('Toe Kick Setback').get_var('Toe_Kick_Setback')
        Hide_Toe_Kick = self.get_prompt('Hide Toe Kick').get_var('Hide_Toe_Kick')
        Shelf_Quantity = self.get_prompt('Shelf Quantity').get_var('Shelf_Quantity')
        Add_Backing = self.get_prompt('Add Backing').get_var('Add_Backing')
        Back_Inset = self.get_prompt('Back Inset').get_var('Back_Inset')
        DT = self.get_prompt('Door Type').get_var('DT')
        Add_Top = self.get_prompt('Add Top KD').get_var('Add_Top')
        Backing_Thickness = self.get_prompt('Backing Thickness').get_var('Backing_Thickness')
        Is_Hanging = self.get_prompt('Is Hanging').get_var('Is_Hanging')
        RLS = self.get_prompt('Remove Left Side').get_var("RLS")
        RRS = self.get_prompt('Remove Right Side').get_var("RRS")
        Spine_Width = self.get_prompt('Spine Width').get_var('Spine_Width')
        Spine_Y_Location = self.get_prompt('Spine Y Location').get_var('Spine_Y_Location')
        Cleat_Height = self.get_prompt('Cleat Height').get_var('Cleat_Height')
        Door = self.get_prompt('Door').get_var('Door')
        Door_Pull_Height = self.get_prompt('Door Pull Height').get_var('Door_Pull_Height')
        Pull_Location = self.get_prompt("Pull Location").get_var('Pull_Location')
        Open = self.get_prompt("Open Door").get_var('Open')
        Rotation = self.get_prompt("Door Rotation").get_var('Rotation')
        Half = self.get_prompt("Half Open").get_var('Half')
        Pull_Type = self.get_prompt("Pull Type").get_var('Pull_Type')
        Base_Pull_Location = self.get_prompt("Base Pull Location").get_var('Base_Pull_Location')
        Tall_Pull_Location = self.get_prompt("Tall Pull Location").get_var('Tall_Pull_Location')
        Upper_Pull_Location = self.get_prompt("Upper Pull Location").get_var('Upper_Pull_Location')
        World_Z = self.obj_bp.snap.get_var('matrix_world[2][3]', 'World_Z')
        Add_Top_Shelf = self.get_prompt('Add Top Shelf').get_var('Add_Top_Shelf')
        Exposed_Left = self.get_prompt('Exposed Left').get_var('Exposed_Left')
        Exposed_Right = self.get_prompt('Exposed Right').get_var('Exposed_Right')
        Top_Shelf_Overhang = self.get_prompt('Top Shelf Overhang').get_var('Top_Shelf_Overhang')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var('Panel_Thickness')
        Left_Filler_Setback_Amount = self.get_prompt('Left Filler Setback Amount').get_var()
        Edge_Bottom_of_Left_Filler = self.get_prompt("Edge Bottom of Left Filler").get_var()
        Add_Capping_Left_Filler = self.get_prompt("Add Capping Left Filler").get_var()
        Right_Side_Wall_Filler = self.get_prompt('Right Side Wall Filler').get_var('Right_Side_Wall_Filler')
        Right_Filler_Setback_Amount = self.get_prompt('Right Filler Setback Amount').get_var()
        Edge_Bottom_of_Right_Filler = self.get_prompt("Edge Bottom of Right Filler").get_var()
        Add_Capping_Right_Filler = self.get_prompt("Add Capping Right Filler").get_var()
        Extend_Left = self.get_prompt('Extend Left').get_var('Extend_Left')
        Extend_Right = self.get_prompt('Extend Right').get_var('Extend_Right')

        top = common_parts.add_l_shelf(self)
        top.loc_z('(Height+IF(Is_Hanging,0,Toe_Kick_Height))', [Height, Toe_Kick_Height, Is_Hanging])
        top.dim_x('Width-IF(RRS,0,PT)', [Width, RRS, PT])
        top.dim_y('Depth+IF(RLS,0,PT)', [Depth, PT, RLS])
        top.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        top.get_prompt('Left Depth').set_formula('Left_Depth', [Left_Depth])
        top.get_prompt('Right Depth').set_formula('Right_Depth', [Right_Depth])
        top.get_prompt("Is Locked Shelf").set_value(True)
        top.get_prompt('Hide').set_formula('IF(Add_Top,False,True)', [Add_Top])

        left_top_shelf = common_parts.add_plant_on_top(self)
        left_top_shelf.set_name('Topshelf')
        left_top_shelf.loc_y(
            'Depth-Left_Side_Wall_Filler-Extend_Left', [Depth, Left_Side_Wall_Filler, Extend_Left])
        left_top_shelf.loc_z('(Height+IF(Is_Hanging,0,Toe_Kick_Height))+PT', [Height, Toe_Kick_Height, Is_Hanging, PT])
        left_top_shelf.dim_x(
            '(Depth+Right_Depth+Top_Shelf_Overhang-Extend_Left)*-1+Left_Side_Wall_Filler',
            [Right_Depth, RRS, PT, Depth,
             Top_Shelf_Overhang, Left_Side_Wall_Filler, Extend_Left])
        left_top_shelf.dim_y('-Left_Depth-Top_Shelf_Overhang', [Depth, PT, RLS, Left_Depth, Top_Shelf_Overhang])
        left_top_shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        left_top_shelf.rot_z(value=math.radians(90))
        left_top_shelf.get_prompt('Exposed Left').set_formula('Exposed_Left', [Exposed_Left])
        left_top_shelf.get_prompt('Hide').set_formula('IF(Add_Top_Shelf,False,True)', [Add_Top_Shelf])

        right_top_shelf = common_parts.add_plant_on_top(self)
        right_top_shelf.set_name('Topshelf')
        right_top_shelf.loc_z('(Height+IF(Is_Hanging,0,Toe_Kick_Height))+PT', [Height, Toe_Kick_Height, Is_Hanging, PT])
        right_top_shelf.dim_x(
            'Width+Right_Side_Wall_Filler+Extend_Right',
            [Width, RRS, PT, Right_Side_Wall_Filler, Extend_Right])
        right_top_shelf.dim_y('-Right_Depth-Top_Shelf_Overhang', [Right_Depth, PT, RLS, Top_Shelf_Overhang])
        right_top_shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        right_top_shelf.get_prompt('Exposed Right').set_formula('Exposed_Right', [Exposed_Right])
        right_top_shelf.get_prompt('Hide').set_formula('IF(Add_Top_Shelf,False,True)', [Add_Top_Shelf])

        right_top_cleat = common_parts.add_cleat(self)
        right_top_cleat.set_name("Top Cleat")
        right_top_cleat.loc_x('Spine_Width', [Spine_Width])
        right_top_cleat.loc_z('(IF(Add_Top,Height-Shelf_Thickness,Height))+IF(Is_Hanging,0,Toe_Kick_Height)',
                              [Height, Shelf_Thickness, Add_Top, Is_Hanging, Toe_Kick_Height])
        right_top_cleat.rot_x(value=math.radians(-90))
        right_top_cleat.dim_x('Width-Spine_Width-IF(RRS,0,PT)', [RRS, Width, PT, Spine_Width])
        right_top_cleat.dim_y('Cleat_Height', [Cleat_Height])
        right_top_cleat.dim_z('-PT', [PT])
        right_top_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        left_top_cleat = common_parts.add_cleat(self)
        left_top_cleat.set_name("Top Cleat")
        left_top_cleat.loc_y('IF(RLS,Depth,Depth+PT)', [Depth, RLS, PT])
        left_top_cleat.loc_z('(IF(Add_Top,Height-Shelf_Thickness,Height))+IF(Is_Hanging,0,Toe_Kick_Height)', [Height, Shelf_Thickness, Add_Top, Is_Hanging, Toe_Kick_Height])
        left_top_cleat.rot_x(value=math.radians(-90))
        left_top_cleat.rot_z(value=math.radians(90))
        left_top_cleat.dim_x('-Depth-Spine_Width-IF(RLS,0,PT)', [RLS, Depth, PT, Spine_Width])
        left_top_cleat.dim_y('Cleat_Height', [Cleat_Height])
        left_top_cleat.dim_z('-PT', [PT])
        left_top_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        bottom = common_parts.add_l_shelf(self)
        bottom.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Is_Hanging, Height, Panel_Height, Toe_Kick_Height])
        bottom.dim_x('Width-IF(RRS,0,PT)', [Width, RRS, PT])
        bottom.dim_y('Depth+IF(RLS,0,PT)', [Depth, PT, RLS])
        bottom.dim_z('Shelf_Thickness', [Shelf_Thickness])
        bottom.get_prompt('Left Depth').set_formula('Left_Depth', [Left_Depth])
        bottom.get_prompt('Right Depth').set_formula('Right_Depth', [Right_Depth])
        bottom.get_prompt('Is Locked Shelf').set_value(True)

        right_bot_cleat = common_parts.add_cleat(self)
        right_bot_cleat.set_name("Bottom Cleat")
        right_bot_cleat.loc_x('Spine_Width', [Spine_Width])
        right_bot_cleat.loc_z('IF(Is_Hanging,Height-Panel_Height+Shelf_Thickness,Shelf_Thickness+Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Shelf_Thickness, Toe_Kick_Height])
        right_bot_cleat.rot_x(value=math.radians(-90))
        right_bot_cleat.dim_x('Width-Spine_Width-IF(RRS,0,PT)', [RRS, Width, PT, Spine_Width])
        right_bot_cleat.dim_y('-Cleat_Height', [Cleat_Height])
        right_bot_cleat.dim_z('-PT', [PT])
        right_bot_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        left_bot_cleat = common_parts.add_cleat(self)
        left_bot_cleat.set_name("Bottom Cleat")
        left_bot_cleat.loc_y('IF(RLS,Depth,Depth+PT)', [Depth, RLS, PT])
        left_bot_cleat.loc_z('IF(Is_Hanging,Height-Panel_Height+Shelf_Thickness,Shelf_Thickness+Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Shelf_Thickness, Toe_Kick_Height])
        left_bot_cleat.rot_x(value=math.radians(-90))
        left_bot_cleat.rot_z(value=math.radians(90))
        left_bot_cleat.dim_x('-Depth-Spine_Width-IF(RLS,0,PT)', [RLS, Depth, PT, Spine_Width])
        left_bot_cleat.dim_y('-Cleat_Height', [Cleat_Height])
        left_bot_cleat.dim_z('-PT', [PT])
        left_bot_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        left_panel = common_parts.add_panel(self)
        left_panel.loc_y('Depth', [Depth, Add_Backing])
        left_panel.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height])
        left_panel.rot_y(value=math.radians(-90))
        left_panel.rot_z(value=math.radians(-90))
        left_panel.dim_x('Panel_Height', [Panel_Height])
        left_panel.dim_y('Left_Depth', [Left_Depth])
        left_panel.dim_z('PT', [PT])
        left_panel.get_prompt('Left Depth').set_formula('Left_Depth', [Left_Depth])  # Adding this in order to drill the panel on one side
        left_panel.get_prompt('Hide').set_formula('IF(RLS,True,False)', [RLS])

        right_panel = common_parts.add_panel(self)
        right_panel.loc_x('Width-PT', [Width, PT])
        right_panel.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height])
        right_panel.rot_y(value=math.radians(-90))
        right_panel.rot_z(value=math.radians(180))
        right_panel.dim_x('Panel_Height', [Panel_Height])
        right_panel.dim_y('Right_Depth', [Right_Depth])
        right_panel.dim_z('PT', [PT])
        right_panel.get_prompt('Right Depth').set_formula('Right_Depth', [Right_Depth])  # Adding this in order to drill the panel on one side
        right_panel.get_prompt('Hide').set_formula('IF(RRS,True,False)', [RRS])

        right_back = common_parts.add_corner_back(self)
        right_back.set_name("Backing")
        right_back.loc_x('Width-PT', [Width, PT])
        right_back.loc_y('-PT', [PT])
        right_back.loc_z('IF(Is_Hanging,Height-Panel_Height+PT,Toe_Kick_Height+PT)',
                         [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Cleat_Height, Back_Inset, PT])
        right_back.rot_y(value=math.radians(-90))
        right_back.rot_z(value=math.radians(-90))
        right_back.dim_x('Panel_Height-PT-IF(Add_Top,PT,0)', [Panel_Height, Cleat_Height, Back_Inset, PT, Add_Top])
        right_back.dim_y('-Width+(PT*2)', [Width, PT])
        right_back.dim_z('Backing_Thickness', [Backing_Thickness])
        right_back.get_prompt('Hide').set_formula('IF(Add_Backing,False,True)', [Add_Backing])

        left_back = common_parts.add_corner_back(self)
        left_back.loc_y('Depth+PT', [Depth, PT])
        left_back.loc_z('IF(Is_Hanging,Height-Panel_Height+PT,Toe_Kick_Height+PT)',
                        [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Cleat_Height, Back_Inset, PT])
        left_back.rot_y(value=math.radians(-90))
        left_back.rot_z(value=math.radians(-180))
        left_back.dim_x('Panel_Height-PT-IF(Add_Top,PT,0)', [Panel_Height, Cleat_Height, Back_Inset, PT, Add_Top])
        left_back.dim_y('Depth+(PT)', [Depth, PT])
        left_back.dim_z('Backing_Thickness', [Backing_Thickness])
        left_back.get_prompt('Is Left Back').set_value(True)
        left_back.get_prompt('Hide').set_formula('IF(Add_Backing,False,True)', [Add_Backing])

        # Fillers
        create_corner_fillers(self, Panel_Height, Left_Side_Wall_Filler,
                              Panel_Thickness, Left_Depth, Depth,
                              Left_Filler_Setback_Amount, Is_Hanging, Width,
                              Edge_Bottom_of_Left_Filler, self.hide_var,
                              Add_Capping_Left_Filler, Right_Side_Wall_Filler,
                              Right_Filler_Setback_Amount, Toe_Kick_Height,
                              Edge_Bottom_of_Right_Filler, Right_Depth,
                              Add_Capping_Right_Filler)

        spine = common_parts.add_panel(self)
        spine.set_name("Mitered Pard")
        spine.obj_bp["IS_BP_PANEL"] = False
        spine.obj_bp["IS_BP_MITERED_PARD"] = True
        spine.obj_bp.sn_closets.is_panel_bp = False  # TODO: remove
        spine.obj_bp.snap.comment_2 = "1510"
        spine.loc_y("-Spine_Y_Location", [Spine_Y_Location])
        spine.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height])
        spine.rot_y(value=math.radians(-90))
        spine.rot_z(value=math.radians(-45))
        spine.dim_x('Panel_Height', [Panel_Height])
        spine.dim_y(value=sn_unit.inch(2.92))
        spine.dim_z('PT', [PT])
        spine.get_prompt('Hide').set_formula('IF(Add_Backing,True,False)', [Add_Backing])

        # Toe_Kick
        create_corner_toe_kicks(
            self.obj_bp, Left_Depth, Toe_Kick_Setback, Depth,
            PT, Hide_Toe_Kick, Is_Hanging, Toe_Kick_Height,
            Width, Right_Depth)
        # Doors
        # L Reach Back Doors
        l_door_reach_back_left = common_parts.add_door(self)
        l_door_reach_back_left.set_name("Left Door")
        l_door_reach_back_left.loc_x('Left_Depth', [Depth, Left_Depth])
        l_door_reach_back_left.loc_y('Depth+(PT/2)', [Depth, PT])
        l_door_reach_back_left.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness])
        l_door_reach_back_left.rot_x(value=0)
        l_door_reach_back_left.rot_y(value=math.radians(-90))
        l_door_reach_back_left.rot_z("radians(180)-IF(DT==0,IF(Pull_Location==0,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",
                                     [Pull_Location, Open, Rotation, DT, Half])
        l_door_reach_back_left.dim_x('Panel_Height-(Shelf_Thickness)', [Panel_Height, Shelf_Thickness])
        l_door_reach_back_left.dim_y('Depth+Right_Depth+(PT)+IF(Pull_Location==0,INCH(0.62),0)', [Depth, Right_Depth, PT, Pull_Location])
        l_door_reach_back_left.dim_z('PT', [PT])
        l_door_reach_back_left.get_prompt('Hide').set_formula('IF(Door,IF(DT==0,False,True),True)', [Door, DT])

        l_door_reach_back_right = common_parts.add_door(self)
        l_door_reach_back_right.set_name("Right Door")
        l_door_reach_back_right.loc_x('Width-(PT/2)', [Width, PT])
        l_door_reach_back_right.loc_y('-Right_Depth', [Right_Depth])
        l_door_reach_back_right.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness])
        l_door_reach_back_right.rot_x(value=0)
        l_door_reach_back_right.rot_y(value=math.radians(-90))
        l_door_reach_back_right.rot_z("radians(90)+IF(DT==0,IF(Pull_Location==1,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",
                                      [Pull_Location, Open, Rotation, DT, Half])
        l_door_reach_back_right.dim_x('Panel_Height-(Shelf_Thickness)', [Panel_Height, Shelf_Thickness])
        l_door_reach_back_right.dim_y('Width-Left_Depth-(PT)-IF(Pull_Location==1,INCH(0.62),0)', [Width, Left_Depth, PT, Pull_Location])
        l_door_reach_back_right.dim_z('PT', [PT])
        l_door_reach_back_right.get_prompt('Hide').set_formula('IF(Door,IF(DT==0,False,True),True)', [Door, DT])

        # L Doors Lazy Susan
        l_door_lazy_susan_left = common_parts.add_door(self)
        l_door_lazy_susan_left.set_name("Left Door")
        l_door_lazy_susan_left.loc_x(
            'IF(Pull_Location==0,Left_Depth+IF(Open<Half,(Open*((Width-Left_Depth)*(1+(Open*2))-PT-INCH(0.25))),Open*((Width-Left_Depth)*(1+(Open*(3-(Open*2))))-PT-INCH(0.25))-PT*((Open-Half)*2))+PT,Left_Depth)',
            [Depth, Left_Depth, PT, Width, Open, Half, Pull_Location])
        l_door_lazy_susan_left.loc_y(
            'IF(Pull_Location==0,-Right_Depth-PT-(IF(Open<Half,Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(2-(2*Open)),Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(1-((Open-Half)*2))-PT*((Open-Half)*2))),Depth+(PT/2))',
            [Depth, PT, Open, Half, Width, Left_Depth, PT, Right_Depth, Pull_Location])
        l_door_lazy_susan_left.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness])
        l_door_lazy_susan_left.rot_x(value=0)
        l_door_lazy_susan_left.rot_y(value=math.radians(-90))
        l_door_lazy_susan_left.rot_z('IF(Pull_Location==0,(IF(Open>Half,((Open-Half)*2)*radians(45),0)),radians(180)-(Open*radians(180)))', [Open, Half, Pull_Location])
        l_door_lazy_susan_left.dim_x('Panel_Height-(Shelf_Thickness)', [Panel_Height, Shelf_Thickness])
        l_door_lazy_susan_left.dim_y('Depth+Right_Depth+(PT)+INCH(0.25)', [Depth, Right_Depth, PT])
        l_door_lazy_susan_left.dim_z('PT', [PT])
        l_door_lazy_susan_left.get_prompt('Hide').set_formula('IF(Door,IF(DT==1,False,True),True)', [Door, DT])

        l_door_lazy_susan_right = common_parts.add_door(self)
        l_door_lazy_susan_right.set_name("Right Door")
        l_door_lazy_susan_right.loc_x(
            'IF(Pull_Location==0,Width-(PT/2),Left_Depth+PT-(IF(Open<Half,Open*(Depth+Right_Depth+(PT*2))*2*(2-(2*Open)),Open*(Depth+Right_Depth+(PT*2))*2*(1-((Open-Half)*2))+PT*((Open-Half)*2))))',
            [Depth, PT, Open, Half, Width, Left_Depth, PT, Right_Depth, Pull_Location])
        l_door_lazy_susan_right.loc_y(
            'IF(Pull_Location==0,-Right_Depth,-Right_Depth-PT+IF(Open<Half,(Open*(Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*2))),Open*((Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*(3-(Open*2)))))))',
            [Depth, Left_Depth, PT, Width, Open, Half, Pull_Location, Right_Depth])
        l_door_lazy_susan_right.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness])
        l_door_lazy_susan_right.rot_x(value=0)
        l_door_lazy_susan_right.rot_y(value=math.radians(-90))
        l_door_lazy_susan_right.rot_z('IF(Pull_Location==0,radians(90)+(Open*radians(180)),radians(-90)-IF(Open>Half,((Open-Half)*2)*radians(45),0))', [Open, Pull_Location, Half])
        l_door_lazy_susan_right.dim_x('Panel_Height-(Shelf_Thickness)', [Panel_Height, Shelf_Thickness])
        l_door_lazy_susan_right.dim_y('Width-Left_Depth-(PT)-INCH(0.25)', [Width, Left_Depth, PT])
        l_door_lazy_susan_right.dim_z('PT', [PT])
        l_door_lazy_susan_right.get_prompt('Hide').set_formula('IF(Door,IF(DT==1,False,True),True)', [Door, DT])

        # Left L Reachback Pull
        l_door_reachback_left_pull = common_parts.add_drawer_pull(self)
        l_door_reachback_left_pull.set_name("Left Door Pull")
        l_door_reachback_left_pull.loc_x('Left_Depth', [Left_Depth, PT, DT])
        l_door_reachback_left_pull.loc_y('Depth-(PT/2)', [Depth, Right_Depth, DT, PT])
        l_door_reachback_left_pull.dim_y('Depth+Right_Depth+(PT)', [DT, Depth, Right_Depth, PT])
        l_door_reachback_left_pull.dim_z('PT', [DT, PT])
        l_door_reachback_left_pull.loc_z(
            'IF(Pull_Type==2,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Upper_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Base_Pull_Location))',
            [Door_Pull_Height, Pull_Type, Base_Pull_Location, Tall_Pull_Location, Upper_Pull_Location, Height, World_Z, Toe_Kick_Height, Shelf_Thickness, Is_Hanging, Panel_Height])
        l_door_reachback_left_pull.rot_x(value=0)
        l_door_reachback_left_pull.rot_y(value=math.radians(-90))
        l_door_reachback_left_pull.rot_z("radians(180)-IF(DT==0,IF(Pull_Location==0,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",
                                         [Pull_Location, Open, Rotation, DT, Half])
        l_door_reachback_left_pull.get_prompt('Hide').set_formula('IF(Pull_Location==1,True,IF(Door,IF(DT==0,False,True),True))', [Door, Pull_Location, DT])

        # Right L Reachback Pull
        l_door_reachback_right_pull = common_parts.add_drawer_pull(self)
        l_door_reachback_right_pull.set_name("Right Door Pull")
        l_door_reachback_right_pull.loc_x('Width', [Width, DT, Left_Depth, PT])
        l_door_reachback_right_pull.loc_y('-Right_Depth', [Right_Depth])
        l_door_reachback_right_pull.dim_y('Width-Left_Depth-(PT)-INCH(0.62)', [DT, Width, Left_Depth, PT])
        l_door_reachback_right_pull.dim_z('PT', [DT, PT])
        l_door_reachback_right_pull.loc_z(
            'IF(Pull_Type==2,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Upper_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Base_Pull_Location))',
            [Door_Pull_Height, Pull_Type, Base_Pull_Location, Tall_Pull_Location, Upper_Pull_Location, Height, World_Z, Toe_Kick_Height, Shelf_Thickness, Is_Hanging, Panel_Height])
        l_door_reachback_right_pull.rot_x(value=0)
        l_door_reachback_right_pull.rot_y(value=math.radians(-90))
        l_door_reachback_right_pull.rot_z("radians(90)+IF(DT==0,IF(Pull_Location==1,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",
                                          [Pull_Location, Open, Rotation, DT, Half])
        l_door_reachback_right_pull.get_prompt('Hide').set_formula('IF(Pull_Location==0,True,IF(Door,IF(DT==0,False,True),True))', [Door, Pull_Location, DT])

        # L Lazy Susan Left Pull
        l_door_lazy_susan_left_pull = common_parts.add_drawer_pull(self)
        l_door_lazy_susan_left_pull.set_name("Left Door Pull")
        l_door_lazy_susan_left_pull.loc_x(
            'Left_Depth+IF(Open<Half,(Open*((Width-Left_Depth)*(1+(Open*2))-PT-INCH(0.25))),Open*((Width-Left_Depth)*(1+(Open*(3-(Open*2))))-PT-INCH(0.25))-PT*((Open-Half)*2))+PT',
            [Depth, Left_Depth, PT, Width, Open, Half, Pull_Location])
        l_door_lazy_susan_left_pull.loc_y(
            '-Right_Depth+(PT/2)-(IF(Open<Half,Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(2-(2*Open)),Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(1-((Open-Half)*2))-PT*((Open-Half)*2)))',
            [Depth, PT, Open, Half, Width, Left_Depth, PT, Right_Depth, Pull_Location])
        l_door_lazy_susan_left_pull.dim_y('(Depth+Right_Depth+(PT)+INCH(0.25))*-1', [Depth, Right_Depth, PT])
        l_door_lazy_susan_left_pull.dim_z('IF(Open>Half,-PT*((Open-Half)*2),0)', [PT, Open, Half])
        l_door_lazy_susan_left_pull.loc_z(
            'IF(Pull_Type==2,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Upper_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Base_Pull_Location))',
            [Door_Pull_Height, Pull_Type, Base_Pull_Location, Tall_Pull_Location, Upper_Pull_Location, Height, World_Z, Toe_Kick_Height, Shelf_Thickness, Is_Hanging, Panel_Height])
        l_door_lazy_susan_left_pull.rot_x(value=0)
        l_door_lazy_susan_left_pull.rot_y(value=math.radians(-90))
        l_door_lazy_susan_left_pull.rot_z('radians(180)+IF(Open>Half,((Open-Half)*2)*radians(45),0)', [Open, Half, Pull_Location])
        l_door_lazy_susan_left_pull.get_prompt('Hide').set_formula('IF(Pull_Location==1,True,IF(Door,IF(DT==1,False,True),True))', [Door, Pull_Location, DT])

        # L Lazy Suasan Right Pull
        l_door_lazy_susan_right_pull = common_parts.add_drawer_pull(self)
        l_door_lazy_susan_right_pull.set_name("Right Door Pull")
        l_door_lazy_susan_right_pull.loc_x(
            'Left_Depth-(IF(Open<Half,Open*(Depth+Right_Depth+(PT*2))*2*(2-(2*Open)),Open*(Depth+Right_Depth+(PT*2))*2*(1-((Open-Half)*2))+PT*((Open-Half)*2)))',
            [Depth, PT, Open, Half, Width, Left_Depth, PT, Right_Depth, Pull_Location])
        l_door_lazy_susan_right_pull.loc_y(
            '-Right_Depth-PT+IF(Open<Half,(Open*(Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*2))),Open*((Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*(3-(Open*2))))))',
            [Depth, Left_Depth, PT, Width, Open, Half, Pull_Location, Right_Depth])
        l_door_lazy_susan_right_pull.dim_y('(Width-Left_Depth-(PT)-INCH(0.25))*-1', [Width, Left_Depth, PT])
        l_door_lazy_susan_right_pull.dim_z('IF(Open>Half,-PT*((Open-Half)*1.5),0)', [PT, Open, Half])
        l_door_lazy_susan_right_pull.loc_z(
            'IF(Pull_Type==2,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Upper_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Base_Pull_Location))',
            [Door_Pull_Height, Pull_Type, Base_Pull_Location, Tall_Pull_Location, Upper_Pull_Location, Height, World_Z, Toe_Kick_Height, Shelf_Thickness, Is_Hanging, Panel_Height])
        l_door_lazy_susan_right_pull.rot_x(value=0)
        l_door_lazy_susan_right_pull.rot_y(value=math.radians(-90))
        l_door_lazy_susan_right_pull.rot_z('radians(90)-IF(Open>Half,((Open-Half)*2)*radians(45),0)', [Open, Pull_Location, Half])
        l_door_lazy_susan_right_pull.get_prompt('Hide').set_formula('IF(Pull_Location==0,True,IF(Door,IF(DT==1,False,True),True))', [Door, Pull_Location, DT])

        # Shelves
        previous_l_shelf = None
        for i in range(1, 11):
            Shelf_Height = self.get_prompt("Shelf " + str(i) + " Height").get_var('Shelf_Height')

            l_shelf = common_parts.add_l_shelf(self)
            if previous_l_shelf:
                prev_shelf_z_loc = previous_l_shelf.obj_bp.snap.get_var('location.z', 'prev_shelf_z_loc')
                l_shelf.loc_z('prev_shelf_z_loc+Shelf_Height', [prev_shelf_z_loc, Shelf_Height])
            else:
                l_shelf.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+Shelf_Height',
                              [Shelf_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness, Height, Panel_Height])

            l_shelf.loc_x('IF(Add_Backing,Backing_Thickness,0)', [Add_Backing, Backing_Thickness])
            l_shelf.loc_y('IF(Add_Backing,-Backing_Thickness,0)', [Add_Backing, Backing_Thickness])
            l_shelf.rot_x(value=0)
            l_shelf.rot_y(value=0)
            l_shelf.rot_z(value=0)
            l_shelf.dim_x('Width-PT-IF(Add_Backing,Backing_Thickness,0)', [Width, PT, Add_Backing, Backing_Thickness])
            l_shelf.dim_y('Depth+PT+IF(Add_Backing,Backing_Thickness,0)', [Depth, PT, Add_Backing, Backing_Thickness])
            l_shelf.dim_z('Shelf_Thickness', [Shelf_Thickness])
            l_shelf.get_prompt('Left Depth').set_formula('Left_Depth-IF(Add_Backing,Backing_Thickness,0)', [Left_Depth, Add_Backing, Backing_Thickness])
            l_shelf.get_prompt('Right Depth').set_formula('Right_Depth-IF(Add_Backing,Backing_Thickness,0)', [Right_Depth, Add_Backing, Backing_Thickness])
            l_shelf.get_prompt('Hide').set_formula('IF(Shelf_Quantity>' + str(i) + ',False,True)', [Shelf_Quantity])
            previous_l_shelf = l_shelf

    def draw(self):
        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["IS_BP_L_SHELVES"] = True
        self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.update()
        set_tk_id_prompt(self.obj_bp)


def set_tk_id_prompt(obj_bp):
    children = obj_bp.children
    for child in children:
        if "Toe Kick" in child.name:
            set_obj_tk_id_prompt(child)
            child['IS_BP_ASSEMBLY'] = True
            child.snap.type_group = 'INSERT'


def set_obj_tk_id_prompt(obj):
    obj["ID_PROMPT"] = "sn_closets.toe_kick_prompts"
    children = obj.children
    for child in children:
        set_obj_tk_id_prompt(child)


def create_corner_toe_kicks(obj_bp, Left_Depth, Toe_Kick_Setback, Depth,
                            PT, Hide_Toe_Kick, Is_Hanging, Toe_Kick_Height,
                            Width, Right_Depth):
    tk_path = path.join(
        closet_paths.get_library_path(),
        "/Products - Basic/Toe Kick.png")
    wm_props = bpy.context.window_manager.snap

    left_tk = wm_props.get_asset(tk_path)
    left_tk.draw()
    left_tk.obj_bp.parent = obj_bp
    left_tk.obj_bp["ID_PROMPT"] = left_tk.id_prompt
    left_tk.obj_bp.snap.comment_2 = "1034"
    left_tk.loc_x(
        'Left_Depth - Toe_Kick_Setback',
        [Left_Depth, Toe_Kick_Setback])
    left_tk.loc_x('0', [])
    left_tk.loc_y('Depth', [Depth])
    left_tk.rot_x(value=math.radians(0))
    left_tk.rot_z(value=math.radians(90))
    left_tk.dim_x('-Depth + PT/2', [Depth, PT])
    left_tk.dim_y(
        '-Left_Depth + Toe_Kick_Setback',
        [Left_Depth, Toe_Kick_Setback])
    left_tk.get_prompt('Hide').set_formula(
        'IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,False))',
        [Hide_Toe_Kick, Is_Hanging])
    left_tk.get_prompt('Toe Kick Height').set_formula(
        'Toe_Kick_Height', [Toe_Kick_Height])
    set_tk_hide(left_tk)
    left_depth_amount =\
        left_tk.get_prompt(
            "Extend Depth Amount").get_var(
                "left_depth_amount")

    right_tk = wm_props.get_asset(tk_path)
    right_tk.draw()
    right_tk.obj_bp.parent = obj_bp
    right_tk.obj_bp.snap.comment_2 = "1034"
    right_tk.rot_x(value=0)
    right_tk.rot_z(value=0)
    right_tk.loc_x(
        'Left_Depth - Toe_Kick_Setback - PT/2 + left_depth_amount',
        [Left_Depth, Toe_Kick_Setback, PT, left_depth_amount])
    right_tk.loc_y('0', [])
    right_tk.dim_x(
        'Width - Left_Depth + Toe_Kick_Setback + PT/2- left_depth_amount',
        [Width, Left_Depth, Toe_Kick_Setback, PT, left_depth_amount])
    right_tk.dim_y(
        '-Right_Depth + Toe_Kick_Setback',
        [Right_Depth, Toe_Kick_Setback])
    right_tk.get_prompt('Hide').set_formula(
        'IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,False))',
        [Hide_Toe_Kick, Is_Hanging])
    right_tk.get_prompt('Toe Kick Height').set_formula(
        'Toe_Kick_Height', [Toe_Kick_Height])
    set_tk_hide(right_tk)


def set_tk_hide(toe_kick):
    Hide = toe_kick.get_prompt("Hide").get_var("Hide")
    children = toe_kick.obj_bp.children
    for child in children:
        is_obj = "obj" in child.name.lower()
        is_skin = "skin" in child.name.lower()
        if not is_obj and not is_skin:
            child_assembly =\
                sn_types.Assembly(obj_bp=child)
            child_hide = child_assembly.get_prompt("Hide")
            child_hide.set_formula("Hide", [Hide])


def create_corner_fillers(assemly, Panel_Height, Left_Side_Wall_Filler,
                          Panel_Thickness, Left_Depth, Depth,
                          Left_Filler_Setback_Amount, Is_Hanging, Width,
                          Edge_Bottom_of_Left_Filler, hide_var,
                          Add_Capping_Left_Filler, Right_Side_Wall_Filler,
                          Right_Filler_Setback_Amount, Toe_Kick_Height,
                          Edge_Bottom_of_Right_Filler, Right_Depth,
                          Add_Capping_Right_Filler):

    # Left Filler
    left_filler = common_parts.add_filler(assemly)
    left_filler.set_name("Left Filler")
    left_filler.dim_x(
        'Panel_Height',
        [Panel_Height])
    left_filler.dim_y('-Left_Side_Wall_Filler', [Left_Side_Wall_Filler])
    left_filler.dim_z('Panel_Thickness', [Panel_Thickness])
    left_filler.loc_x(
        'Left_Depth - Left_Filler_Setback_Amount - Panel_Thickness',
        [Left_Depth, Left_Filler_Setback_Amount, Panel_Thickness])
    left_filler.loc_y(
        "Depth-Left_Side_Wall_Filler",
        [Depth, Left_Side_Wall_Filler])
    left_filler.loc_z(
        'IF(Is_Hanging, 0, Toe_Kick_Height)',
        [Toe_Kick_Height, Is_Hanging])
    left_filler.rot_x(value=0)
    left_filler.rot_y(value=math.radians(-90))
    left_filler.rot_z(value=math.radians(180))
    hide = left_filler.get_prompt("Hide")
    hide.set_formula(
        'IF(Left_Side_Wall_Filler==0,True,False) or Hide',
        [Left_Side_Wall_Filler, hide_var])
    left_filler.get_prompt("Exposed Left").set_formula(
        'IF(Edge_Bottom_of_Left_Filler,True,False)',
        [Edge_Bottom_of_Left_Filler])
    left_filler.get_prompt("Exposed Left").set_value(True)
    left_filler.get_prompt("Exposed Right").set_value(True)
    left_filler.get_prompt("Exposed Back").set_value(True)

    # Left Capping Filler
    left_capping_filler = common_parts.add_filler(assemly)
    left_capping_filler.set_name("Left Capping Filler")
    left_capping_filler.dim_x(
        'Panel_Height-INCH(0.91)',
        [Panel_Height])
    left_capping_filler.dim_y(
        '-Left_Side_Wall_Filler', [Left_Side_Wall_Filler])
    left_capping_filler.dim_z('Panel_Thickness', [Panel_Thickness])
    left_capping_filler.loc_x(
        'Left_Depth-Left_Filler_Setback_Amount',
        [Left_Depth, Left_Filler_Setback_Amount])
    left_capping_filler.loc_y(
        "Depth-Left_Side_Wall_Filler",
        [Depth, Left_Side_Wall_Filler])
    left_capping_filler.loc_z(
        'IF(Is_Hanging, 0, Toe_Kick_Height)+INCH(0.455)',
        [Toe_Kick_Height, Is_Hanging])
    left_capping_filler.rot_y(value=math.radians(-90))
    left_capping_filler.rot_z(value=math.radians(180))
    left_capping_filler.get_prompt('Hide').set_formula(
        'IF(Add_Capping_Left_Filler,False,True) or Hide',
        [Left_Side_Wall_Filler, Add_Capping_Left_Filler, hide_var])
    left_capping_filler.get_prompt("Exposed Left").set_value(True)
    left_capping_filler.get_prompt("Exposed Right").set_value(True)
    left_capping_filler.get_prompt("Exposed Back").set_value(True)

    # Right Filler
    right_filler = common_parts.add_filler(assemly)
    right_filler.set_name("Right Filler")
    right_filler.dim_x(
        'Panel_Height',
        [Panel_Height])
    right_filler.dim_y('-Right_Side_Wall_Filler', [Right_Side_Wall_Filler])
    right_filler.dim_z('Panel_Thickness', [Panel_Thickness])
    right_filler.loc_x(
        "Width+Right_Side_Wall_Filler",
        [Width, Right_Side_Wall_Filler])
    right_filler.loc_y(
        '-Right_Depth+Right_Filler_Setback_Amount',
        [Right_Depth, Right_Filler_Setback_Amount])
    right_filler.loc_z(
        'IF(Is_Hanging, 0, Toe_Kick_Height)',
        [Toe_Kick_Height, Is_Hanging])
    right_filler.rot_x(value=0)
    right_filler.rot_y(value=math.radians(-90))
    right_filler.rot_z(value=math.radians(-90))
    hide = right_filler.get_prompt("Hide")
    hide.set_formula(
        'IF(Right_Side_Wall_Filler==0,True,False) or Hide',
        [Right_Side_Wall_Filler, hide_var])
    right_filler.get_prompt("Exposed Left").set_formula(
        'IF(Edge_Bottom_of_Right_Filler,True,False)',
        [Edge_Bottom_of_Right_Filler])
    right_filler.get_prompt("Exposed Left").set_value(True)
    right_filler.get_prompt("Exposed Right").set_value(True)
    right_filler.get_prompt("Exposed Back").set_value(True)

    # Right Capping Filler
    right_capping_filler = common_parts.add_filler(assemly)
    right_capping_filler.set_name("Right Capping Filler")
    right_capping_filler.dim_x(
        'Panel_Height-INCH(0.91)',
        [Panel_Height])
    right_capping_filler.dim_y(
        '-Right_Side_Wall_Filler', [Right_Side_Wall_Filler])
    right_capping_filler.dim_z('Panel_Thickness', [Panel_Thickness])
    right_capping_filler.loc_x(
        "Width+Right_Side_Wall_Filler",
        [Width, Right_Side_Wall_Filler])
    right_capping_filler.loc_y(
        '-Right_Depth+Right_Filler_Setback_Amount-Panel_Thickness',
        [Right_Depth, Right_Filler_Setback_Amount, Panel_Thickness])
    right_capping_filler.loc_z(
        'IF(Is_Hanging, 0, Toe_Kick_Height)+INCH(0.455)',
        [Toe_Kick_Height, Is_Hanging])
    right_capping_filler.rot_y(value=math.radians(-90))
    right_capping_filler.rot_z(value=math.radians(-90))
    right_capping_filler.get_prompt('Hide').set_formula(
        'IF(Add_Capping_Right_Filler,False,True) or Hide',
        [Right_Side_Wall_Filler, Add_Capping_Right_Filler, hide_var])
    right_capping_filler.get_prompt("Exposed Left").set_value(True)
    right_capping_filler.get_prompt("Exposed Right").set_value(True)
    right_capping_filler.get_prompt("Exposed Back").set_value(True)


class Corner_Shelves(sn_types.Assembly):

    """
    This Corner Shelf Includes a Back Spine for support and is hanging first
    """

    category_name = ""
    type_assembly = "PRODUCT"
    property_id = "sn_closets.corner_shelves"
    show_in_library = True
    placement_type = 'CORNER'

    def pre_draw(self):
        self.create_assembly()
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth
        self.obj_z.location.z = self.height

        props = bpy.context.scene.sn_closets

        self.add_prompt("Panel Height", 'DISTANCE', sn_unit.millimeter(2003))
        self.add_prompt("Back Inset", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Spine Width", 'DISTANCE', sn_unit.inch(1))
        self.add_prompt("Spine Y Location", 'DISTANCE', sn_unit.inch(2.1))
        self.add_prompt("Cleat Height", 'DISTANCE', sn_unit.inch(3.64))
        self.add_prompt("Left Depth", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Right Depth", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Shelf Quantity", 'QUANTITY', 3)
        self.add_prompt("Add Top KD", 'CHECKBOX', True)  # export=True
        self.add_prompt("Hide Toe Kick", 'CHECKBOX', False)  # export=True
        self.add_prompt("Add Backing", 'CHECKBOX', False)  # export=True
        self.add_prompt("Is Hanging", 'CHECKBOX', False)  # export=True
        self.add_prompt("Remove Left Side", 'CHECKBOX', False)  # export=True
        self.add_prompt("Remove Right Side", 'CHECKBOX', False)  # export=True
        self.add_prompt("Use Left Swing", 'CHECKBOX', False)  # export=True
        self.add_prompt("Force Double Doors", 'CHECKBOX', False)  # export=True
        self.add_prompt("Door", 'CHECKBOX', False)  # export=True
        self.add_prompt("Door Pull Height", 'DISTANCE', sn_unit.inch(36))
        self.add_prompt("Backing Thickness", 'DISTANCE', sn_unit.inch(0.75))

        self.add_prompt("Open Door", 'PERCENTAGE', 0)
        self.add_prompt("Door Rotation", 'QUANTITY', 120)
        self.add_prompt("Half Open", 'PERCENTAGE', 0.5)
        self.add_prompt("Pull Type", 'COMBOBOX', 1, ["Base", "Tall", "Upper"])

        self.add_prompt("Add Top Shelf", 'CHECKBOX', False)
        self.add_prompt("Exposed Left", 'CHECKBOX', False)
        self.add_prompt("Exposed Right", 'CHECKBOX', False)
        self.add_prompt("Top Shelf Overhang", 'DISTANCE', sn_unit.inch(0.5))

        self.add_prompt("Add Left Filler", 'CHECKBOX', False)
        self.add_prompt("Add Right Filler", 'CHECKBOX', False)
        self.add_prompt("Left Side Wall Filler", 'DISTANCE', 0.0)
        self.add_prompt("Right Side Wall Filler", 'DISTANCE', 0.0)
        self.add_prompt("Add Capping Left Filler", 'CHECKBOX', False)
        self.add_prompt("Add Capping Right Filler", 'CHECKBOX', False)
        self.add_prompt("Left Filler Setback Amount", 'DISTANCE', 0.0)
        self.add_prompt("Right Filler Setback Amount", 'DISTANCE', 0.0)
        self.add_prompt("Edge Bottom of Left Filler", 'CHECKBOX', False)
        self.add_prompt("Edge Bottom of Right Filler", 'CHECKBOX', False)

        for i in range(1, 11):
            self.add_prompt("Shelf " + str(i) + " Height", 'DISTANCE', sn_unit.millimeter(653.034))

        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_door_prompts(self)
        common_prompts.add_door_pull_prompts(self)

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Panel_Height = self.get_prompt('Panel Height').get_var('Panel_Height')
        Left_Depth = self.get_prompt('Left Depth').get_var('Left_Depth')
        Right_Depth = self.get_prompt('Right Depth').get_var('Right_Depth')
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        PT = self.get_prompt('Panel Thickness').get_var("PT")
        Toe_Kick_Setback = self.get_prompt('Toe Kick Setback').get_var('Toe_Kick_Setback')
        Hide_Toe_Kick = self.get_prompt('Hide Toe Kick').get_var('Hide_Toe_Kick')
        Shelf_Quantity = self.get_prompt('Shelf Quantity').get_var('Shelf_Quantity')
        Add_Backing = self.get_prompt('Add Backing').get_var('Add_Backing')
        Back_Inset = self.get_prompt('Back Inset').get_var('Back_Inset')
        Add_Top = self.get_prompt('Add Top KD').get_var('Add_Top')
        Backing_Thickness = self.get_prompt('Backing Thickness').get_var('Backing_Thickness')
        Is_Hanging = self.get_prompt('Is Hanging').get_var('Is_Hanging')
        RLS = self.get_prompt('Remove Left Side').get_var("RLS")
        RRS = self.get_prompt('Remove Right Side').get_var("RRS")
        Spine_Width = self.get_prompt('Spine Width').get_var('Spine_Width')
        Spine_Y_Location = self.get_prompt('Spine Y Location').get_var('Spine_Y_Location')
        Cleat_Height = self.get_prompt('Cleat Height').get_var('Cleat_Height')
        Door = self.get_prompt('Door').get_var('Door')
        Door_Pull_Height = self.get_prompt('Door Pull Height').get_var('Door_Pull_Height')
        Use_Left_Swing = self.get_prompt("Use Left Swing").get_var('Use_Left_Swing')
        Force_Double_Doors = self.get_prompt("Force Double Doors").get_var('Force_Double_Doors')
        Open = self.get_prompt("Open Door").get_var('Open')
        Rotation = self.get_prompt("Door Rotation").get_var('Rotation')
        Pull_Type = self.get_prompt("Pull Type").get_var('Pull_Type')
        Base_Pull_Location = self.get_prompt("Base Pull Location").get_var('Base_Pull_Location')
        Tall_Pull_Location = self.get_prompt("Tall Pull Location").get_var('Tall_Pull_Location')
        Upper_Pull_Location = self.get_prompt("Upper Pull Location").get_var('Upper_Pull_Location')
        World_Z = self.obj_bp.snap.get_var('matrix_world[2][3]', 'World_Z')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Add_Top_Shelf = self.get_prompt('Add Top Shelf').get_var('Add_Top_Shelf')
        Top_Shelf_Overhang = self.get_prompt('Top Shelf Overhang').get_var('Top_Shelf_Overhang')
        Left_Side_Wall_Filler = self.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var('Panel_Thickness')
        Left_Filler_Setback_Amount = self.get_prompt('Left Filler Setback Amount').get_var()
        Edge_Bottom_of_Left_Filler = self.get_prompt("Edge Bottom of Left Filler").get_var()
        Add_Capping_Left_Filler = self.get_prompt("Add Capping Left Filler").get_var()
        Right_Side_Wall_Filler = self.get_prompt('Right Side Wall Filler').get_var('Right_Side_Wall_Filler')
        Right_Filler_Setback_Amount = self.get_prompt('Right Filler Setback Amount').get_var()
        Edge_Bottom_of_Right_Filler = self.get_prompt("Edge Bottom of Right Filler").get_var()
        Add_Capping_Right_Filler = self.get_prompt("Add Capping Right Filler").get_var()


        top_angled = common_parts.add_angle_shelf(self)
        top_angled.loc_z('(Height+IF(Is_Hanging,0,Toe_Kick_Height))', [Height, Toe_Kick_Height, Is_Hanging])
        top_angled.dim_x('Width-IF(RRS,0,PT)', [Width, RRS, PT])
        top_angled.dim_y('Depth+IF(RLS,0,PT)', [Depth, PT, RLS])
        top_angled.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        top_angled.get_prompt("Is Locked Shelf").set_value(True)
        top_angled.get_prompt('Left Depth').set_formula('Left_Depth', [Left_Depth])
        top_angled.get_prompt('Right Depth').set_formula('Right_Depth', [Right_Depth])
        top_angled.get_prompt('Hide').set_formula('IF(Add_Top,False,True)', [Add_Top])

        top_shelf_angled = common_parts.add_angle_shelf(self)
        top_shelf_angled.set_name("Corner Top Shelf")
        top_shelf_angled.loc_z('(Height+IF(Is_Hanging,0,Toe_Kick_Height))+Shelf_Thickness', [Height, Toe_Kick_Height, Is_Hanging, Shelf_Thickness])
        top_shelf_angled.dim_x(
            'Width-IF(RRS,0,PT)+PT+Right_Side_Wall_Filler',
            [Width, RRS, PT, Right_Side_Wall_Filler])
        top_shelf_angled.dim_y(
            'Depth+IF(RLS,0,PT)-PT-Left_Side_Wall_Filler',
            [Depth, PT, RLS, Left_Side_Wall_Filler])
        top_shelf_angled.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        top_shelf_angled.get_prompt('Left Depth').set_formula('Left_Depth+Top_Shelf_Overhang', [Left_Depth, Top_Shelf_Overhang])
        top_shelf_angled.get_prompt('Right Depth').set_formula('Right_Depth+Top_Shelf_Overhang', [Right_Depth, Top_Shelf_Overhang])
        top_shelf_angled.get_prompt('Hide').set_formula('IF(Add_Top_Shelf,False,True)', [Add_Top_Shelf])

        right_top_cleat = common_parts.add_cleat(self)
        right_top_cleat.set_name("Top Cleat")
        right_top_cleat.loc_x('Spine_Width', [Spine_Width])
        right_top_cleat.loc_z('(IF(Add_Top,Height-Shelf_Thickness,Height))+IF(Is_Hanging,0,Toe_Kick_Height)', [Height, Shelf_Thickness, Add_Top, Is_Hanging, Toe_Kick_Height])
        right_top_cleat.rot_x(value=math.radians(-90))
        right_top_cleat.dim_x('Width-Spine_Width-IF(RRS,0,PT)', [RRS, Width, PT, Spine_Width])
        right_top_cleat.dim_y('Cleat_Height', [Cleat_Height])
        right_top_cleat.dim_z('-PT', [PT])
        right_top_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        left_top_cleat = common_parts.add_cleat(self)
        left_top_cleat.set_name("Top Cleat")
        left_top_cleat.loc_y('IF(RLS,Depth,Depth+PT)', [Depth, RLS, PT])
        left_top_cleat.loc_z('(IF(Add_Top,Height-Shelf_Thickness,Height))+IF(Is_Hanging,0,Toe_Kick_Height)', [Height, Shelf_Thickness, Add_Top, Is_Hanging, Toe_Kick_Height])
        left_top_cleat.rot_x(value=math.radians(-90))
        left_top_cleat.rot_z(value=math.radians(90))
        left_top_cleat.dim_x('-Depth-Spine_Width-IF(RLS,0,PT)', [RLS, Depth, PT, Spine_Width])
        left_top_cleat.dim_y('Cleat_Height', [Cleat_Height])
        left_top_cleat.dim_z('-PT', [PT])
        left_top_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        bottom_angled = common_parts.add_angle_shelf(self)
        bottom_angled.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Is_Hanging, Height, Panel_Height, Toe_Kick_Height])
        bottom_angled.dim_x('Width-IF(RRS,0,PT)', [Width, RRS, PT])
        bottom_angled.dim_y('Depth+IF(RLS,0,PT)', [Depth, PT, RLS])
        bottom_angled.dim_z('Shelf_Thickness', [Shelf_Thickness])
        bottom_angled.get_prompt('Left Depth').set_formula('Left_Depth', [Left_Depth])
        bottom_angled.get_prompt('Right Depth').set_formula('Right_Depth', [Right_Depth])
        bottom_angled.get_prompt('Is Locked Shelf').set_value(True)

        right_bot_cleat = common_parts.add_cleat(self)
        right_bot_cleat.set_name("Bottom Cleat")
        right_bot_cleat.loc_x('Spine_Width', [Spine_Width])
        right_bot_cleat.loc_z('IF(Is_Hanging,Height-Panel_Height+Shelf_Thickness,Shelf_Thickness+Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Shelf_Thickness, Toe_Kick_Height])
        right_bot_cleat.rot_x(value=math.radians(-90))
        right_bot_cleat.dim_x('Width-Spine_Width-IF(RRS,0,PT)', [RRS, Width, PT, Spine_Width])
        right_bot_cleat.dim_y('-Cleat_Height', [Cleat_Height])
        right_bot_cleat.dim_z('-PT', [PT])
        right_bot_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        left_bot_cleat = common_parts.add_cleat(self)
        left_bot_cleat.set_name("Bottom Cleat")
        left_bot_cleat.loc_y('IF(RLS,Depth,Depth+PT)', [Depth, RLS, PT])
        left_bot_cleat.loc_z('IF(Is_Hanging,Height-Panel_Height+Shelf_Thickness,Shelf_Thickness+Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Shelf_Thickness, Toe_Kick_Height])
        left_bot_cleat.rot_x(value=math.radians(-90))
        left_bot_cleat.rot_z(value=math.radians(90))
        left_bot_cleat.dim_x('-Depth-Spine_Width-IF(RLS,0,PT)', [RLS, Depth, PT, Spine_Width])
        left_bot_cleat.dim_y('-Cleat_Height', [Cleat_Height])
        left_bot_cleat.dim_z('-PT', [PT])
        left_bot_cleat.get_prompt('Hide').set_formula('IF(Add_Backing,True,False) or Hide', [self.hide_var, Add_Backing])

        left_panel = common_parts.add_panel(self)
        left_panel.loc_y('Depth', [Depth, Add_Backing])
        left_panel.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height])
        left_panel.rot_y(value=math.radians(-90))
        left_panel.rot_z(value=math.radians(-90))
        left_panel.dim_x('Panel_Height', [Panel_Height])
        left_panel.dim_y('Left_Depth', [Left_Depth])
        left_panel.dim_z('PT', [PT])
        left_panel.get_prompt('Left Depth').set_formula('Left_Depth', [Left_Depth])  # Adding this in order to drill the panel on one side
        left_panel.get_prompt('Hide').set_formula('IF(RLS,True,False)', [RLS])

        right_panel = common_parts.add_panel(self)
        right_panel.loc_x('Width-PT', [Width, PT])
        right_panel.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height])
        right_panel.rot_y(value=math.radians(-90))
        right_panel.rot_z(value=math.radians(180))
        right_panel.dim_x('Panel_Height', [Panel_Height])
        right_panel.dim_y('Right_Depth', [Right_Depth])
        right_panel.dim_z('PT', [PT])
        right_panel.get_prompt('Right Depth').set_formula('Right_Depth', [Right_Depth])  # Adding this in order to drill the panel on one side
        right_panel.get_prompt('Hide').set_formula('IF(RRS,True,False)', [RRS])

        right_back = common_parts.add_corner_back(self)
        right_back.set_name("Backing")
        right_back.loc_x('Width-PT', [Width, PT])
        right_back.loc_y('-PT', [PT])
        right_back.loc_z('IF(Is_Hanging,Height-Panel_Height+PT,Toe_Kick_Height+PT)',
                         [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Cleat_Height, Back_Inset, PT])
        right_back.rot_y(value=math.radians(-90))
        right_back.rot_z(value=math.radians(-90))
        right_back.dim_x('Panel_Height-PT-IF(Add_Top,PT,0)', [Panel_Height, Cleat_Height, Back_Inset, PT, Add_Top])
        right_back.dim_y('-Width+(PT*2)', [Width, PT])
        right_back.dim_z('Backing_Thickness', [Backing_Thickness])
        right_back.get_prompt('Hide').set_formula('IF(Add_Backing,False,True)', [Add_Backing])

        left_back = common_parts.add_corner_back(self)
        left_back.loc_y('Depth+PT', [Depth, PT])
        left_back.loc_z('IF(Is_Hanging,Height-Panel_Height+PT,Toe_Kick_Height+PT)',
                        [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Cleat_Height, Back_Inset, PT])
        left_back.rot_y(value=math.radians(-90))
        left_back.rot_z(value=math.radians(-180))
        left_back.dim_x('Panel_Height-PT-IF(Add_Top,PT,0)', [Panel_Height, Cleat_Height, Back_Inset, PT, Add_Top])
        left_back.dim_y('Depth+PT', [Depth, PT])
        left_back.dim_z('Backing_Thickness', [Backing_Thickness])
        left_back.get_prompt('Hide').set_formula('IF(Add_Backing,False,True)', [Add_Backing])

        spine = common_parts.add_panel(self)
        spine.set_name("Mitered Pard")
        spine.obj_bp["IS_BP_PANEL"] = False
        spine.obj_bp["IS_BP_MITERED_PARD"] = True
        spine.obj_bp.sn_closets.is_panel_bp = False  # TODO: remove
        spine.obj_bp.snap.comment_2 = "1510"
        spine.loc_y("-Spine_Y_Location", [Spine_Y_Location])
        spine.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height])
        spine.rot_y(value=math.radians(-90))
        spine.rot_z(value=math.radians(-45))
        spine.dim_x('Panel_Height', [Panel_Height])
        spine.dim_y(value=sn_unit.inch(2.92))
        spine.dim_z('PT', [PT])
        spine.get_prompt('Hide').set_formula('IF(Add_Backing,True,False)', [Add_Backing])

        # Toe_Kick
        create_corner_toe_kicks(
            self.obj_bp, Left_Depth, Toe_Kick_Setback, Depth,
            PT, Hide_Toe_Kick, Is_Hanging, Toe_Kick_Height,
            Width, Right_Depth)

        angle_kick = common_parts.add_toe_kick(self)
        angle_kick.set_name("Angle Kick")
        angle_kick.obj_bp.snap.comment_2 = "1034"
        angle_kick.loc_x(
            'Left_Depth-Toe_Kick_Setback-PT+.00635',
            [Left_Depth, Toe_Kick_Setback, PT])
        angle_kick.loc_y('Depth+3*PT/2-.00635', [Depth, PT])
        angle_kick.rot_x(value=math.radians(90))
        angle_kick.rot_z(
            '-atan((Depth+Right_Depth-Toe_Kick_Setback)'
            '/(Width-Left_Depth+Toe_Kick_Setback))',
            [Width, Depth, Right_Depth, Left_Depth, Toe_Kick_Setback])
        angle_kick.dim_x(
            'sqrt((Width-Left_Depth+Toe_Kick_Setback-Shelf_Thickness)**2'
            '+(Depth+Right_Depth-Toe_Kick_Setback)**2)',
            [Width, Depth, Left_Depth, Right_Depth,
             Toe_Kick_Setback, Shelf_Thickness])
        angle_kick.dim_y('Toe_Kick_Height', [Toe_Kick_Height])
        angle_kick.dim_z('PT', [PT])
        angle_kick.get_prompt(
            'Hide').set_formula(
                'IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,False))',
                [Hide_Toe_Kick, Is_Hanging])

        # Fillers
        create_corner_fillers(self, Panel_Height, Left_Side_Wall_Filler,
                              Panel_Thickness, Left_Depth, Depth,
                              Left_Filler_Setback_Amount, Is_Hanging, Width,
                              Edge_Bottom_of_Left_Filler, self.hide_var,
                              Add_Capping_Left_Filler, Right_Side_Wall_Filler,
                              Right_Filler_Setback_Amount, Toe_Kick_Height,
                              Edge_Bottom_of_Right_Filler, Right_Depth,
                              Add_Capping_Right_Filler)
        # Doors
        # Left Angled Door
        angled_door_l = common_parts.add_door(self)
        angled_door_l.set_name("Angled Door Left")
        angled_door_l.loc_x('Left_Depth', [Left_Depth])
        angled_door_l.loc_y('Depth+PT', [Depth, PT])
        angled_door_l.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness])
        angled_door_l.rot_y(value=math.radians(-90))
        angled_door_l.rot_z('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159-radians(Open*Rotation)', [Width, Depth, Right_Depth, Left_Depth, Open, Rotation])
        angled_door_l.dim_x('Panel_Height-(Shelf_Thickness)', [Panel_Height, Shelf_Thickness])
        angled_door_l.dim_y('IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))*-1',
                            [Width, Left_Depth, Depth, Right_Depth, PT, Force_Double_Doors])
        angled_door_l.dim_z('PT', [PT])
        angled_door_l.get_prompt('Hide').set_formula(
            'IF((Door and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Force_Double_Doors),False,IF((Door and Use_Left_Swing),False,IF(Door,True,True))))',
            [Door, Use_Left_Swing, Force_Double_Doors])

        # Right Angled Door
        angled_door_r = common_parts.add_door(self)
        angled_door_r.set_name("Angled Door Right")
        angled_door_r.loc_x('Width-PT', [Width, PT])
        angled_door_r.loc_y('-Right_Depth', [Right_Depth])
        angled_door_r.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)', [Height, Panel_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness])
        angled_door_r.rot_y(value=math.radians(-90))
        angled_door_r.rot_z('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159+radians(Open*Rotation)', [Width, Depth, Right_Depth, Left_Depth, Open, Rotation])
        angled_door_r.dim_x('Panel_Height-(Shelf_Thickness)', [Panel_Height, Shelf_Thickness])
        angled_door_r.dim_y('IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))',
                            [Width, Left_Depth, Depth, Right_Depth, PT, Force_Double_Doors])
        angled_door_r.dim_z('PT', [PT])
        angled_door_r.get_prompt('Hide').set_formula(
            'IF((Door and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Force_Double_Doors),False,IF((Door and Use_Left_Swing),True,IF(Door,False,True))))',
            [Door, Use_Left_Swing, Force_Double_Doors])

        # Left Angled Pull
        angled_door_l_pull = common_parts.add_drawer_pull(self)
        angled_door_l_pull.set_name("Left Door Pull")
        angled_door_l_pull.loc_x('Left_Depth', [Left_Depth])
        angled_door_l_pull.loc_y('Depth+PT', [Depth, PT])
        angled_door_l_pull.loc_z(
            'IF(Pull_Type==2,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Upper_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Base_Pull_Location))',
            [Door_Pull_Height, Pull_Type, Base_Pull_Location, Tall_Pull_Location, Upper_Pull_Location, Height, World_Z, Toe_Kick_Height, Shelf_Thickness, Is_Hanging, Panel_Height])
        angled_door_l_pull.dim_z('PT', [PT])
        angled_door_l_pull.dim_y(
            'IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))*-1+PT',
            [Width, Left_Depth, Depth, Right_Depth, PT, Force_Double_Doors])
        angled_door_l_pull.rot_y(value=math.radians(-90))
        angled_door_l_pull.rot_z('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159-radians(Open*Rotation)', [Width, Depth, Right_Depth, Left_Depth, Open, Rotation])
        angled_door_l_pull.get_prompt('Hide').set_formula(
            'IF((Door and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Force_Double_Doors),False,IF((Door and Use_Left_Swing),False,IF(Door,True,True))))',
            [Door, Use_Left_Swing, Force_Double_Doors])

        # Right Angled Pull
        angled_door_r_pull = common_parts.add_drawer_pull(self)
        angled_door_r_pull.set_name("Right Door Pull")
        angled_door_r_pull.loc_x('Width-PT', [Width, PT])
        angled_door_r_pull.loc_y('-Right_Depth', [Right_Depth])
        angled_door_r_pull.loc_z(
            'IF(Pull_Type==2,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Upper_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Base_Pull_Location))',
            [Door_Pull_Height, Pull_Type, Base_Pull_Location, Tall_Pull_Location, Upper_Pull_Location, Height, World_Z, Toe_Kick_Height, Shelf_Thickness, Is_Hanging, Panel_Height])
        angled_door_r_pull.dim_z('PT', [PT])
        angled_door_r_pull.dim_y(
            'IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))-PT',
            [Width, Left_Depth, Depth, Right_Depth, PT, Force_Double_Doors])
        angled_door_r_pull.rot_y(value=math.radians(-90))
        angled_door_r_pull.rot_z('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159+radians(Open*Rotation)', [Width, Depth, Right_Depth, Left_Depth, Open, Rotation])
        angled_door_r_pull.get_prompt('Hide').set_formula(
            'IF((Door and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Force_Double_Doors),False,IF((Door and Use_Left_Swing),True,IF(Door,False,True))))',
            [Door, Use_Left_Swing, Force_Double_Doors])

        # Shelves
        # Angled Shelves
        previous_angled_shelf = None
        for i in range(1, 11):
            Shelf_Height = self.get_prompt("Shelf " + str(i) + " Height").get_var('Shelf_Height')

            shelf_angled = common_parts.add_angle_shelf(self)

            if previous_angled_shelf:
                prev_shelf_z_loc = previous_angled_shelf.obj_bp.snap.get_var('location.z', 'prev_shelf_z_loc')
                shelf_angled.loc_z('prev_shelf_z_loc+Shelf_Height', [prev_shelf_z_loc, Shelf_Height])
            else:
                shelf_angled.loc_z('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+Shelf_Height+Shelf_Thickness',
                                   [Shelf_Height, Is_Hanging, Toe_Kick_Height, Shelf_Thickness, Panel_Height, Height])

            shelf_angled.loc_x('IF(Add_Backing,Backing_Thickness,0)', [Add_Backing, Backing_Thickness])
            shelf_angled.loc_y('IF(Add_Backing,-Backing_Thickness,0)', [Add_Backing, Backing_Thickness])
            shelf_angled.rot_x(value=0)
            shelf_angled.rot_y(value=0)
            shelf_angled.rot_z(value=0)
            shelf_angled.dim_x('Width-PT-IF(Add_Backing,Backing_Thickness,0)', [Width, PT, Add_Backing, Backing_Thickness])
            shelf_angled.dim_y('Depth+PT+IF(Add_Backing,Backing_Thickness,0)', [Depth, PT, Add_Backing, Backing_Thickness])
            shelf_angled.dim_z('Shelf_Thickness', [Shelf_Thickness])
            shelf_angled.get_prompt('Left Depth').set_formula('Left_Depth-IF(Add_Backing,Backing_Thickness,0)', [Left_Depth, Add_Backing, Backing_Thickness])
            shelf_angled.get_prompt('Right Depth').set_formula('Right_Depth-IF(Add_Backing,Backing_Thickness,0)', [Right_Depth, Add_Backing, Backing_Thickness])
            shelf_angled.get_prompt('Hide').set_formula('IF(Shelf_Quantity>' + str(i) + ',False,True)', [Shelf_Quantity])

            previous_angled_shelf = shelf_angled

    def draw(self):
        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["IS_BP_CORNER_SHELVES"] = True
        self.obj_bp["ID_PROMPT"] = self.property_id
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.update()
        set_tk_id_prompt(self.obj_bp)


class Corner_Triangle_Shelves(sn_types.Assembly):

    category_name = ""
    type_assembly = "PRODUCT"
    property_id = "sn_closets.outside_corner_shelves"
    show_in_library = True
    placement_type = 'Corner'

    def pre_draw(self):
        self.create_assembly()
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth
        self.obj_z.location.z = self.height        

        self.add_prompt("Left Depth", 'DISTANCE', sn_unit.inch(12))       
        self.add_prompt("Right Depth", 'DISTANCE', sn_unit.inch(12))  
        self.add_prompt("Shelf Quantity", 'QUANTITY', 3) 
 
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Left_Depth = self.get_prompt('Left Depth').get_var('Left_Depth')
        Right_Depth = self.get_prompt('Right Depth').get_var('Right_Depth')
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var('Shelf_Thickness')
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var('Panel_Thickness')
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Toe_Kick_Setback = self.get_prompt('Toe Kick Setback').get_var('Toe_Kick_Setback')
        Shelf_Quantity = self.get_prompt('Shelf Quantity').get_var('Shelf_Quantity')

        self.dim_x('fabs(Depth)',[Depth])
        
        inside_height_empty = self.add_empty("Inside Height")
        inside_height_empty.snap.loc_z('Height-Toe_Kick_Height-(Shelf_Thickness*2)-(Shelf_Thickness*Shelf_Quantity)',[Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        Inside_Height = inside_height_empty.snap.get_var('location.z', 'Inside_Height')
        
        top = common_parts.add_angle_shelf(self)
        top.loc_x('Panel_Thickness',[Panel_Thickness])
        top.loc_y('-Panel_Thickness',[Panel_Thickness])
        top.loc_z('Height',[Height])
        top.dim_x('Width-(Panel_Thickness*2)',[Width,Panel_Thickness])
        top.dim_y('Depth+(Panel_Thickness*2)',[Depth,Panel_Thickness])
        top.dim_z('-Shelf_Thickness',[Shelf_Thickness])
        top.get_prompt('Left Depth').set_value(value=0)
        top.get_prompt('Right Depth').set_value(value=0)
        
        bottom = common_parts.add_angle_shelf(self)
        bottom.loc_x('Panel_Thickness',[Panel_Thickness])
        bottom.loc_y('-Panel_Thickness',[Panel_Thickness])
        bottom.loc_z('Toe_Kick_Height',[Toe_Kick_Height])
        bottom.dim_x('Width-(Panel_Thickness*2)',[Width,Panel_Thickness])
        bottom.dim_y('Depth+(Panel_Thickness*2)',[Depth,Panel_Thickness])
        bottom.dim_z('Shelf_Thickness',[Shelf_Thickness])
        bottom.get_prompt('Left Depth').set_value(value=0)
        bottom.get_prompt('Right Depth').set_value(value=0)
        
        shelf = common_parts.add_angle_shelf(self)
        shelf.loc_x('Panel_Thickness',[Panel_Thickness])
        shelf.loc_y('-Panel_Thickness',[Panel_Thickness])
        shelf.loc_z('Toe_Kick_Height+Shelf_Thickness+(Inside_Height/(Shelf_Quantity+1))',[Height,Inside_Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        shelf.dim_x('Width-(Panel_Thickness*2)',[Width,Panel_Thickness])
        shelf.dim_y('Depth+(Panel_Thickness*2)',[Depth,Panel_Thickness])
        shelf.dim_z('Shelf_Thickness',[Shelf_Thickness])
        shelf.get_prompt('Left Depth').set_value(value=0)
        shelf.get_prompt('Right Depth').set_value(value=0)
        shelf.get_prompt('Hide').set_formula('IF(Shelf_Quantity==0,True,False)',[Shelf_Quantity])
        shelf.get_prompt('Z Quantity').set_formula('Shelf_Quantity',[Shelf_Quantity])
        shelf.get_prompt('Z Offset').set_formula('(Inside_Height/(Shelf_Quantity+1))+Shelf_Thickness',[Inside_Height,Shelf_Quantity,Shelf_Thickness])
        
        wall_panel = common_parts.add_panel(self)
        wall_panel.set_name("Wall Panel")
        wall_panel.rot_y(value=math.radians(-90))
        wall_panel.rot_z(value=math.radians(-90))
        wall_panel.dim_x('Height',[Height])
        wall_panel.dim_y('Width-Panel_Thickness',[Width,Panel_Thickness])
        wall_panel.dim_z(value=sn_unit.inch(-.75))
        
        wall_pane2 = common_parts.add_panel(self)
        wall_pane2.set_name("Wall Panel")
        wall_pane2.rot_y(value=math.radians(-90))
        wall_pane2.dim_x('Height',[Height])
        wall_pane2.dim_y('Depth+Panel_Thickness',[Depth,Panel_Thickness])
        wall_pane2.dim_z(value=sn_unit.inch(-.75))
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.loc_x('Width-(Toe_Kick_Setback*2)',[Width,Toe_Kick_Setback])
        toe_kick.rot_x(value=math.radians(90))
        toe_kick.dim_x('sqrt(((fabs(Depth)-Toe_Kick_Setback)**2.2)+((fabs(Width)-Toe_Kick_Setback)**2.2))*-1',[Width,Depth,Toe_Kick_Setback])
        toe_kick.rot_z('atan((fabs(Depth)+Toe_Kick_Setback)/(fabs(Width)+Toe_Kick_Setback))',[Width,Depth,Toe_Kick_Setback])
        toe_kick.dim_y('Toe_Kick_Height',[Toe_Kick_Height])
        toe_kick.dim_z(value=sn_unit.inch(.75))
        
        # self.update()               

    def draw(self):
        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["ID_PROMPT"] = self.property_id
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.type_group = self.type_assembly


def update_product_height(self, context):
    # THIS IS A HACK!
    # FOR SOME REASON THE FORMULAS IN THE PRODUCT WILL NOT
    # RECALCULATE WHEN THE PANEL HEIGHT IS CHANGED
    obj_product_bp = sn_utils.get_bp(context.active_object,'PRODUCT')
    product = sn_types.Assembly(obj_product_bp)
    if product:
        product.obj_z.location.z = product.obj_z.location.z


class PROMPTS_L_Shelves(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.l_shelves"
    bl_label = "L Shelves Prompts"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name",
                                description="Stores the Base Point Object Name \
                                so the object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    Product_Height: EnumProperty(name="Product Height",
                                 items=common_lists.PANEL_HEIGHTS,
                                 default='2003',
                                 update=update_product_height)

    Door_Type: EnumProperty(name="Door Type",
                            items=[("0", "Reach Back", "Reach Back"),
                                   ("1", "Lazy Susan", "Lazy Susan")],
                            default='0')

    Pull_Location: EnumProperty(name="Pull Location",
                                items=[("0", "Pull on Left Door", "Pull on Left Door"),
                                       ("1", "Pull on Right Door", "Pull on Right Door")],
                                default="0")

    Pull_Type: EnumProperty(name="Pull Type",
                            items=[("0", "Base", "Base"),
                                   ("1", "Tall", "Tall"),
                                   ("2", "Upper", "Upper")],
                            default="1")

    Shelf_1_Height: EnumProperty(name="Shelf 1 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_2_Height: EnumProperty(name="Shelf 2 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_3_Height: EnumProperty(name="Shelf 3 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_4_Height: EnumProperty(name="Shelf 4 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_5_Height: EnumProperty(name="Shelf 5 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_6_Height: EnumProperty(name="Shelf 6 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_7_Height: EnumProperty(name="Shelf 7 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_8_Height: EnumProperty(name="Shelf 8 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_9_Height: EnumProperty(name="Shelf 9 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_10_Height: EnumProperty(name="Shelf 10 Height",
                                  items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    shelf_quantity: EnumProperty(name="Shelf Quantity",
                                 items=[('1', "1", '1'),
                                        ('2', "2", '2'),
                                        ('3', "3", '3'),
                                        ('4', "4", '4'),
                                        ('5', "5", '5'),
                                        ('6', "6", '6'),
                                        ('7', "7", '7'),
                                        ('8', "8", '8'),
                                        ('9', "9", '9'),
                                        ('10', "10", '10')],
                                 default='3')

    product = None
    show_tk_mess = None

    prev_left_wall_filler = 0

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.set_prompts_from_properties()
        self.check_fillers()
        self.set_obj_location()
        closet_props.update_render_materials(self, context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        self.set_properties_from_prompts()
        self.set_filler_values()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))

    def set_obj_location(self):
        right_wall_filler =\
            self.product.get_prompt("Right Side Wall Filler")
        left_wall_filler =\
            self.product.get_prompt("Left Side Wall Filler")
        self.product.obj_y.location.y =\
            -self.depth + left_wall_filler.get_value()
        self.product.obj_x.location.x =\
            self.width - right_wall_filler.get_value()

    def set_filler_values(self):
        left_wall_filler =\
            self.product.get_prompt("Left Side Wall Filler")
        right_wall_filler =\
            self.product.get_prompt("Right Side Wall Filler")
        self.prev_left_wall_filler = left_wall_filler.get_value()
        self.depth =\
            -self.product.obj_y.location.y + left_wall_filler.get_value()
        self.width =\
            self.product.obj_x.location.x + right_wall_filler.get_value()

    def check_fillers(self):
        add_left_filler =\
            self.product.get_prompt("Add Left Filler").get_value()
        add_right_filler =\
            self.product.get_prompt("Add Right Filler").get_value()
        if not add_left_filler:
            left_wall_filler =\
                self.product.get_prompt("Left Side Wall Filler")
            left_filler_setback_amount =\
                self.product.get_prompt("Left Filler Setback Amount")
            edge_bottom_of_left_filler =\
                self.product.get_prompt("Edge Bottom of Left Filler")
            add_capping_left_filler = \
                self.product.get_prompt("Add Capping Left Filler")
            left_wall_filler.set_value(0)
            left_filler_setback_amount.set_value(0)
            edge_bottom_of_left_filler.set_value(False)
            add_capping_left_filler.set_value(False)
            self.prev_left_wall_filler = 0
        if not add_right_filler:
            right_wall_filler =\
                self.product.get_prompt("Right Side Wall Filler")
            right_filler_setback_amount =\
                self.product.get_prompt("Right Filler Setback Amount")
            edge_bottom_of_righ_filler =\
                self.product.get_prompt("Edge Bottom of Right Filler")
            add_capping_righ_filler = \
                self.product.get_prompt("Add Capping Right Filler")
            right_wall_filler.set_value(0)
            right_filler_setback_amount.set_value(0)
            edge_bottom_of_righ_filler.set_value(False)
            add_capping_righ_filler.set_value(False)

    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''
        door_type = self.product.get_prompt('Door Type')
        pull_location = self.product.get_prompt('Pull Location')
        pull_type = self.product.get_prompt('Pull Type')
        is_hanging = self.product.get_prompt("Is Hanging")
        panel_height = self.product.get_prompt("Panel Height")
        shelf_quantity = self.product.get_prompt("Shelf Quantity")
        shelf_thickness = self.product.get_prompt("Shelf Thickness")
        toe_kick_height = self.product.get_prompt("Toe Kick Height")
        if toe_kick_height.distance_value <= inch(3):
            self.product.get_prompt("Toe Kick Height").set_value(inch(3))
            bpy.ops.snap.log_window('INVOKE_DEFAULT',
                                    message="Minimum Toe Kick Height is 3\"",
                                    icon="ERROR")

        prompts = [door_type, pull_location, pull_type, is_hanging, panel_height, shelf_quantity, shelf_thickness, toe_kick_height]
        if all(prompts):
            door_type.set_value(int(self.Door_Type))
            pull_location.set_value(int(self.Pull_Location))
            pull_type.set_value(int(self.Pull_Type))
            if is_hanging.get_value():
                panel_height.set_value(float(self.Product_Height) / 1000)
            else:
                panel_height.set_value(float(self.Product_Height) / 1000)
                self.product.obj_z.location.z = float(self.Product_Height) / 1000

            shelf_quantity.set_value(int(self.shelf_quantity))
            for i in range(1, int(self.shelf_quantity)):
                shelf = self.product.get_prompt("Shelf " + str(i) + " Height")

                hole_count = round(((panel_height.get_value()) * 1000) / 32)
                holes_per_shelf = round(hole_count / int(self.shelf_quantity))
                remainder = hole_count - (holes_per_shelf * (int(self.shelf_quantity)))

                if(i <= remainder):
                    holes_per_shelf = holes_per_shelf + 1
                if(holes_per_shelf >= 3):
                    shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf - 3][0]) / 1000)
                    exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0]")
                else:
                    shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]) / 1000)
                    exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]")

    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        panel_height = self.product.get_prompt("Panel Height")
        door_type = self.product.get_prompt('Door Type')
        pull_location = self.product.get_prompt('Pull Location')
        pull_type = self.product.get_prompt('Pull Type')
        shelf_quantity = self.product.get_prompt("Shelf Quantity")

        prompts = [door_type, pull_location, pull_type, panel_height, shelf_quantity]
        if all(prompts):
            self.Door_Type = str(door_type.get_value())
            self.Pull_Location = str(pull_location.get_value())
            self.Pull_Type = str(pull_type.get_value())
            for index, height in enumerate(common_lists.PANEL_HEIGHTS):
                if not round(panel_height.get_value() * 1000, 0) >= int(height[0]):
                    self.Product_Height = common_lists.PANEL_HEIGHTS[index - 1][0]
                    break

            self.shelf_quantity = str(shelf_quantity.get_value())
            for i in range(1, 11):
                shelf = self.product.get_prompt("Shelf " + str(i) + " Height")
                if shelf:
                    value = round(shelf.get_value() * 1000, 3)
                    for index, height in enumerate(common_lists.SHELF_IN_DOOR_HEIGHTS):
                        if not value >= float(height[0]):
                            exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[index - 1][0]")
                            break

    def draw_product_size(self, layout):
        box = layout.box()
        row = box.row()

        col = row.column(align=True)
        row1 = col.row(align=True)
        row1.label(text='Width:')
        row1.prop(self, 'width', text="")

        row1 = col.row(align=True)
        if sn_utils.object_has_driver(self.product.obj_z):
            row1.label(text='Height: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label(text='Height:')
            row1.prop(self, 'Product_Height', text="")

        row1 = col.row(align=True)
        row1.label(text='Depth:')
        row1.prop(self, 'depth', text="")

        col = row.column(align=True)
        col.label(text="Location X:")
        col.label(text="Location Y:")
        col.label(text="Location Z:")

        col = row.column(align=True)
        col.prop(self.product.obj_bp, 'location', text="")

        Toe_Kick_Height = self.product.get_prompt("Toe Kick Height")

        if Toe_Kick_Height:
            row = box.row()
            row.prop(Toe_Kick_Height, "distance_value", text=Toe_Kick_Height.name)

        is_hanging = self.product.get_prompt("Is Hanging")

        if is_hanging:
            row = box.row()
            row.prop(is_hanging, "checkbox_value", text=is_hanging.name)
            if is_hanging.get_value():
                row.prop(self.product.obj_z, 'location', index=2, text="Hanging Height")

        row = box.row()
        row.label(text='Rotation Z:')
        row.prop(self.product.obj_bp, 'rotation_euler', index=2, text="")

    def draw_filler_options(self, layout):
        add_left_filler = self.product.get_prompt("Add Left Filler")
        add_right_filler = self.product.get_prompt("Add Right Filler")
        left_wall_filler = self.product.get_prompt("Left Side Wall Filler")
        right_wall_filler =\
            self.product.get_prompt("Right Side Wall Filler")
        left_filler_setback_amount =\
            self.product.get_prompt("Left Filler Setback Amount")
        right_filler_setback_amount =\
            self.product.get_prompt("Right Filler Setback Amount")
        add_capping_left_filler =\
            self.product.get_prompt("Add Capping Left Filler")
        add_capping_right_filler =\
            self.product.get_prompt("Add Capping Right Filler")
        edge_bottom_of_left_filler =\
            self.product.get_prompt("Edge Bottom of Left Filler")
        edge_bottom_of_right_filler =\
            self.product.get_prompt("Edge Bottom of Right Filler")

        filler_box = layout.box()
        split = filler_box.split()
        col = split.column(align=True)
        col.label(text="Filler Options:")
        row = col.row()
        row.prop(add_left_filler, 'checkbox_value', text="Add Left Filler")
        row.prop(add_right_filler, 'checkbox_value', text="Add Right Filler")
        row = col.row()
        distance_row = col.row()
        setback_amount_row = col.row()
        capping_filler_row = col.row()
        edge_row = col.row()

        if add_left_filler.get_value():
            distance_row.prop(
                left_wall_filler,
                'distance_value', text="Left Filler Amount")
            setback_amount_row.prop(
                left_filler_setback_amount,
                'distance_value', text="Left Filler Setback Amount")
            capping_filler_row.prop(
                add_capping_left_filler,
                'checkbox_value', text="Add Capping Left Filler")
            edge_row.prop(
                edge_bottom_of_left_filler,
                'checkbox_value', text="Edge Bottom of Left Filler")
        elif add_right_filler.get_value():
            distance_row.label(text="")
            setback_amount_row.label(text="")
            capping_filler_row.label(text="")
            edge_row.label(text="")

        if add_right_filler.get_value():
            distance_row.prop(
                right_wall_filler,
                'distance_value', text="Right Filler Amount")
            setback_amount_row.prop(
                right_filler_setback_amount,
                'distance_value', text="Right Filler Setback Amount")
            capping_filler_row.prop(
                add_capping_right_filler,
                'checkbox_value', text="Add Capping Right Filler")
            edge_row.prop(
                edge_bottom_of_right_filler,
                'checkbox_value', text="Edge Bottom of Right Filler")
        elif add_left_filler.get_value():
            distance_row.label(text="")
            setback_amount_row.label(text="")
            capping_filler_row.label(text="")
            edge_row.label(text="")

    def draw(self, context):
        """ This is where you draw the interface """
        Left_Depth = self.product.get_prompt("Left Depth")
        Right_Depth = self.product.get_prompt("Right Depth")
        Shelf_Quantity = self.product.get_prompt("Shelf Quantity")
        Add_Backing = self.product.get_prompt("Add Backing")
        # Backing_Thickness = self.product.get_prompt("Backing Thickness")
        Add_Top = self.product.get_prompt("Add Top KD")
        Remove_Left_Side = self.product.get_prompt("Remove Left Side")
        Remove_Right_Side = self.product.get_prompt("Remove Right Side")
        Door = self.product.get_prompt("Door")
        Door_Type = self.product.get_prompt("Door Type")
        Open_Door = self.product.get_prompt("Open Door")
        Base_Pull_Location = self.product.get_prompt("Base Pull Location")
        Tall_Pull_Location = self.product.get_prompt("Tall Pull Location")
        Upper_Pull_Location = self.product.get_prompt("Upper Pull Location")
        Add_Top_Shelf = self.product.get_prompt("Add Top Shelf")
        Exposed_Left = self.product.get_prompt("Exposed Left")
        Exposed_Right = self.product.get_prompt("Exposed Right")
        Top_Shelf_Overhang = self.product.get_prompt("Top Shelf Overhang")
        Extend_Left = self.product.get_prompt("Extend Left")
        Extend_Right = self.product.get_prompt("Extend Right")

        layout = self.layout
        self.draw_product_size(layout)
        self.draw_filler_options(layout)

        if Left_Depth:
            box = layout.box()
            row = box.row()
            row.prop(Left_Depth, "distance_value", text=Left_Depth.name)

        if Right_Depth:
            row.prop(Right_Depth, "distance_value", text=Right_Depth.name)

        if Shelf_Quantity:
            col = box.column(align=True)
            row = col.row()
            row.label(text="Qty:")
            row.prop(self, "shelf_quantity", expand=True)
            col.separator()

        if Add_Backing:
            row = box.row()
            row.prop(Add_Backing, "checkbox_value", text=Add_Backing.name)

        # if Backing_Thickness:
        #    if Add_Backing.get_value():
        #        row = box.row()
        #        row.prop(Backing_Thickness, "distance_value", text=Backing_Thickness.name)

        if Add_Top:
            row = box.row()
            row.prop(Add_Top, "checkbox_value", text=Add_Top.name)

        if Add_Top_Shelf:
            row = box.row()
            row.prop(Add_Top_Shelf, "checkbox_value", text=Add_Top_Shelf.name)
            if Add_Top_Shelf.get_value():
                row = box.row()
                row.label(text="Exposed Edges: ")
                row.prop(Exposed_Left, "checkbox_value", text='Left')
                row.prop(Exposed_Right, "checkbox_value", text='Right')
                row = box.row()
                row.prop(Top_Shelf_Overhang, 'distance_value', text=Top_Shelf_Overhang.name)
                row = box.row()
                row.prop(Extend_Left, 'distance_value', text=Extend_Left.name)
                row.prop(Extend_Right, 'distance_value', text=Extend_Right.name)

        if Remove_Left_Side:
            row = box.row()
            row.prop(Remove_Left_Side, "checkbox_value", text=Remove_Left_Side.name)

        if Remove_Right_Side:
            row = box.row()
            row.prop(Remove_Right_Side, "checkbox_value", text=Remove_Right_Side.name)

        row = box.row()
        row.prop(Door, "checkbox_value", text=Door.name)

        if Door.get_value():
            if Door_Type:
                row = box.row()
                row.prop(self, 'Door_Type', text="Door Type")
                row = box.row()
                row.prop(self, 'Pull_Location', text="Pull Location", expand=True)
            row = box.row()
            row.prop(self, 'Pull_Type', text="Pull Type", expand=True)
            row = box.row()
            row.label(text="Pull Location: ")
            if self.Pull_Type == '0':
                row.prop(Base_Pull_Location, "distance_value", text="")
            elif self.Pull_Type == '1':
                row.prop(Tall_Pull_Location, "distance_value", text="")
            else:
                row.prop(Upper_Pull_Location, "distance_value", text="")
            if Open_Door:
                row = box.row()
                row.prop(Open_Door, "factor_value", text=Open_Door.name)


class PROMPTS_Corner_Shelves(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.corner_shelves"
    bl_label = "Corner Shelves Prompts"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name",
                                description="Stores the Base Point Object Name \
                                so the object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    Product_Height: EnumProperty(name="Product Height",
                                 items=common_lists.PANEL_HEIGHTS,
                                 default='2003',
                                 update=update_product_height)

    Pull_Type: EnumProperty(name="Pull Type",
                            items=[("0", "Base", "Base"),
                                   ("1", "Tall", "Tall"),
                                   ("2", "Upper", "Upper")],
                            default="1")

    Shelf_1_Height: EnumProperty(name="Shelf 1 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_2_Height: EnumProperty(name="Shelf 2 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_3_Height: EnumProperty(name="Shelf 3 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_4_Height: EnumProperty(name="Shelf 4 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_5_Height: EnumProperty(name="Shelf 5 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_6_Height: EnumProperty(name="Shelf 6 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_7_Height: EnumProperty(name="Shelf 7 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_8_Height: EnumProperty(name="Shelf 8 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_9_Height: EnumProperty(name="Shelf 9 Height",
                                 items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_10_Height: EnumProperty(name="Shelf 10 Height",
                                  items=common_lists.SHELF_IN_DOOR_HEIGHTS)

    shelf_quantity: EnumProperty(name="Shelf Quantity",
                                 items=[('1', "1", '1'),
                                        ('2', "2", '2'),
                                        ('3', "3", '3'),
                                        ('4', "4", '4'),
                                        ('5', "5", '5'),
                                        ('6', "6", '6'),
                                        ('7', "7", '7'),
                                        ('8', "8", '8'),
                                        ('9', "9", '9'),
                                        ('10', "10", '10')],
                                 default='3')

    product = None

    def check_tk_height(self):
        toe_kick_height =\
            self.product.get_prompt("Toe Kick Height").distance_value
        if toe_kick_height < inch(3):
            self.product.get_prompt("Toe Kick Height").set_value(inch(3))
            bpy.ops.snap.log_window('INVOKE_DEFAULT',
                                    message="Minimum Toe Kick Height is 3\"",
                                    icon="ERROR")

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.check_tk_height()
        self.set_prompts_from_properties()
        self.check_fillers()
        self.set_obj_location()
        closet_props.update_render_materials(self, context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.show_tk_mess = False
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        self.set_properties_from_prompts()
        self.set_filler_values()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))

    def set_filler_values(self):
        left_wall_filler =\
            self.product.get_prompt("Left Side Wall Filler")
        right_wall_filler =\
            self.product.get_prompt("Right Side Wall Filler")
        self.prev_left_wall_filler = left_wall_filler.get_value()
        self.depth =\
            -self.product.obj_y.location.y + left_wall_filler.get_value()
        self.width =\
            self.product.obj_x.location.x + right_wall_filler.get_value()

    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''
        pull_type = self.product.get_prompt('Pull Type')
        is_hanging = self.product.get_prompt("Is Hanging")
        panel_height = self.product.get_prompt("Panel Height")
        shelf_quantity = self.product.get_prompt("Shelf Quantity")
        shelf_thickness = self.product.get_prompt("Shelf Thickness")
        toe_kick_height = self.product.get_prompt("Toe Kick Height")

        prompts = [pull_type, is_hanging, panel_height, shelf_quantity, shelf_thickness, toe_kick_height]
        if all(prompts):
            pull_type.set_value(int(self.Pull_Type))
            if is_hanging.get_value():
                panel_height.set_value(float(self.Product_Height) / 1000)
            else:
                panel_height.set_value(float(self.Product_Height) / 1000)
                self.product.obj_z.location.z = float(self.Product_Height) / 1000

            shelf_quantity.set_value(int(self.shelf_quantity))
            for i in range(1, int(self.shelf_quantity)):
                shelf = self.product.get_prompt("Shelf " + str(i) + " Height")

                hole_count = round(((panel_height.get_value()) * 1000) / 32)
                holes_per_shelf = round(hole_count / int(self.shelf_quantity))
                remainder = hole_count - (holes_per_shelf * (int(self.shelf_quantity)))

                if(i <= remainder):
                    holes_per_shelf = holes_per_shelf + 1
                if(holes_per_shelf >= 3):
                    shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf - 3][0]) / 1000)
                    exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0]")
                else:
                    shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]) / 1000)
                    exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]")

    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        panel_height = self.product.get_prompt("Panel Height")
        pull_type = self.product.get_prompt('Pull Type')
        shelf_quantity = self.product.get_prompt("Shelf Quantity")

        prompts = [pull_type, panel_height, shelf_quantity]
        if all(prompts):
            self.Pull_Type = str(pull_type.get_value())
            for index, height in enumerate(common_lists.PANEL_HEIGHTS):
                if not round(panel_height.get_value() * 1000, 0) >= int(height[0]):
                    self.Product_Height = common_lists.PANEL_HEIGHTS[index - 1][0]
                    break

            self.shelf_quantity = str(shelf_quantity.get_value())
            for i in range(1, 11):
                shelf = self.product.get_prompt("Shelf " + str(i) + " Height")
                if shelf:
                    value = round(shelf.get_value() * 1000, 3)
                    for index, height in enumerate(common_lists.SHELF_IN_DOOR_HEIGHTS):
                        if not value >= float(height[0]):
                            exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[index - 1][0]")
                            break

    def draw_product_size(self, layout):
        box = layout.box()
        row = box.row()

        col = row.column(align=True)
        row1 = col.row(align=True)
        row1.label(text='Width:')
        row1.prop(self, 'width', text="")

        row1 = col.row(align=True)
        if sn_utils.object_has_driver(self.product.obj_z):
            row1.label(text='Height: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label(text='Height:')
            row1.prop(self, 'Product_Height', text="")

        row1 = col.row(align=True)
        row1.label(text='Depth:')
        row1.prop(self, 'depth', text="")

        col = row.column(align=True)
        col.label(text="Location X:")
        col.label(text="Location Y:")
        col.label(text="Location Z:")

        col = row.column(align=True)
        col.prop(self.product.obj_bp, 'location', text="")

        Toe_Kick_Height = self.product.get_prompt("Toe Kick Height")

        if Toe_Kick_Height:
            row = box.row()
            row.prop(Toe_Kick_Height, "distance_value", text=Toe_Kick_Height.name)

        is_hanging = self.product.get_prompt("Is Hanging")

        if is_hanging:
            row = box.row()
            row.prop(is_hanging, "checkbox_value", text=is_hanging.name)
            if is_hanging.get_value():
                row.prop(self.product.obj_z, 'location', index=2, text="Hanging Height")

        row = box.row()
        row.label(text='Rotation Z:')
        row.prop(self.product.obj_bp, 'rotation_euler', index=2, text="")

    def set_obj_location(self):
        right_wall_filler =\
            self.product.get_prompt("Right Side Wall Filler")
        left_wall_filler =\
            self.product.get_prompt("Left Side Wall Filler")
        self.product.obj_y.location.y =\
            -self.depth + left_wall_filler.get_value()
        self.product.obj_x.location.x =\
            self.width - right_wall_filler.get_value()

    def check_fillers(self):
        add_left_filler =\
            self.product.get_prompt("Add Left Filler").get_value()
        add_right_filler =\
            self.product.get_prompt("Add Right Filler").get_value()
        if not add_left_filler:
            left_wall_filler =\
                self.product.get_prompt("Left Side Wall Filler")
            left_filler_setback_amount =\
                self.product.get_prompt("Left Filler Setback Amount")
            edge_bottom_of_left_filler =\
                self.product.get_prompt("Edge Bottom of Left Filler")
            add_capping_left_filler = \
                self.product.get_prompt("Add Capping Left Filler")
            left_wall_filler.set_value(0)
            left_filler_setback_amount.set_value(0)
            edge_bottom_of_left_filler.set_value(False)
            add_capping_left_filler.set_value(False)
            self.prev_left_wall_filler = 0
        if not add_right_filler:
            right_wall_filler =\
                self.product.get_prompt("Right Side Wall Filler")
            right_filler_setback_amount =\
                self.product.get_prompt("Right Filler Setback Amount")
            edge_bottom_of_righ_filler =\
                self.product.get_prompt("Edge Bottom of Right Filler")
            add_capping_righ_filler = \
                self.product.get_prompt("Add Capping Right Filler")
            right_wall_filler.set_value(0)
            right_filler_setback_amount.set_value(0)
            edge_bottom_of_righ_filler.set_value(False)
            add_capping_righ_filler.set_value(False)

    def draw_filler_options(self, layout):
        add_left_filler = self.product.get_prompt("Add Left Filler")
        add_right_filler = self.product.get_prompt("Add Right Filler")
        left_wall_filler = self.product.get_prompt("Left Side Wall Filler")
        right_wall_filler =\
            self.product.get_prompt("Right Side Wall Filler")
        left_filler_setback_amount =\
            self.product.get_prompt("Left Filler Setback Amount")
        right_filler_setback_amount =\
            self.product.get_prompt("Right Filler Setback Amount")
        add_capping_left_filler =\
            self.product.get_prompt("Add Capping Left Filler")
        add_capping_right_filler =\
            self.product.get_prompt("Add Capping Right Filler")
        edge_bottom_of_left_filler =\
            self.product.get_prompt("Edge Bottom of Left Filler")
        edge_bottom_of_right_filler =\
            self.product.get_prompt("Edge Bottom of Right Filler")

        filler_box = layout.box()
        split = filler_box.split()
        col = split.column(align=True)
        col.label(text="Filler Options:")
        row = col.row()
        row.prop(add_left_filler, 'checkbox_value', text="Add Left Filler")
        row.prop(add_right_filler, 'checkbox_value', text="Add Right Filler")
        row = col.row()
        distance_row = col.row()
        setback_amount_row = col.row()
        capping_filler_row = col.row()
        edge_row = col.row()

        if add_left_filler.get_value():
            distance_row.prop(
                left_wall_filler,
                'distance_value', text="Left Filler Amount")
            setback_amount_row.prop(
                left_filler_setback_amount,
                'distance_value', text="Left Filler Setback Amount")
            capping_filler_row.prop(
                add_capping_left_filler,
                'checkbox_value', text="Add Capping Left Filler")
            edge_row.prop(
                edge_bottom_of_left_filler,
                'checkbox_value', text="Edge Bottom of Left Filler")
        elif add_right_filler.get_value():
            distance_row.label(text="")
            setback_amount_row.label(text="")
            capping_filler_row.label(text="")
            edge_row.label(text="")

        if add_right_filler.get_value():
            distance_row.prop(
                right_wall_filler,
                'distance_value', text="Right Filler Amount")
            setback_amount_row.prop(
                right_filler_setback_amount,
                'distance_value', text="Right Filler Setback Amount")
            capping_filler_row.prop(
                add_capping_right_filler,
                'checkbox_value', text="Add Capping Right Filler")
            edge_row.prop(
                edge_bottom_of_right_filler,
                'checkbox_value', text="Edge Bottom of Right Filler")
        elif add_left_filler.get_value():
            distance_row.label(text="")
            setback_amount_row.label(text="")
            capping_filler_row.label(text="")
            edge_row.label(text="")

    def draw(self, context):
        """ This is where you draw the interface """
        Left_Depth = self.product.get_prompt("Left Depth")
        Right_Depth = self.product.get_prompt("Right Depth")
        Shelf_Quantity = self.product.get_prompt("Shelf Quantity")
        Add_Backing = self.product.get_prompt("Add Backing")
        # Backing_Thickness = self.product.get_prompt("Backing Thickness")
        Add_Top = self.product.get_prompt("Add Top KD")
        Remove_Left_Side = self.product.get_prompt("Remove Left Side")
        Remove_Right_Side = self.product.get_prompt("Remove Right Side")
        Door = self.product.get_prompt("Door")
        Use_Left_Swing = self.product.get_prompt("Use Left Swing")
        Force_Double_Doors = self.product.get_prompt("Force Double Doors")
        Open_Door = self.product.get_prompt("Open Door")
        Base_Pull_Location = self.product.get_prompt("Base Pull Location")
        Tall_Pull_Location = self.product.get_prompt("Tall Pull Location")
        Upper_Pull_Location = self.product.get_prompt("Upper Pull Location")
        Add_Top_Shelf = self.product.get_prompt("Add Top Shelf")
        Exposed_Left = self.product.get_prompt("Exposed Left")
        Exposed_Right = self.product.get_prompt("Exposed Right")
        Top_Shelf_Overhang = self.product.get_prompt("Top Shelf Overhang")

        layout = self.layout
        self.draw_product_size(layout)
        self.draw_filler_options(layout)

        if Left_Depth:
            box = layout.box()
            row = box.row()
            row.prop(Left_Depth, "distance_value", text=Left_Depth.name)

        if Right_Depth:
            row.prop(Right_Depth, "distance_value", text=Right_Depth.name)

        if Shelf_Quantity:
            col = box.column(align=True)
            row = col.row()
            row.label(text="Qty:")
            row.prop(self, "shelf_quantity", expand=True)
            col.separator()

        if Add_Backing:
            row = box.row()
            row.prop(Add_Backing, "checkbox_value", text=Add_Backing.name)

        # if Backing_Thickness:
        #    if Add_Backing.get_value():
        #        row = box.row()
        #        row.prop(Backing_Thickness, "distance_value", text=Backing_Thickness.name)

        if Add_Top:
            row = box.row()
            row.prop(Add_Top, "checkbox_value", text=Add_Top.name)

        if Add_Top_Shelf:
            row = box.row()
            row.prop(Add_Top_Shelf, "checkbox_value", text=Add_Top_Shelf.name)
            if Add_Top_Shelf.get_value():
                row = box.row()
                row.label(text="Exposed Edges: ")
                row.prop(Exposed_Left, "checkbox_value", text='Left')
                row.prop(Exposed_Right, "checkbox_value", text='Right')
                row = box.row()
                row.prop(Top_Shelf_Overhang, 'distance_value', text=Top_Shelf_Overhang.name)

        if Remove_Left_Side:
            row = box.row()
            row.prop(Remove_Left_Side, "checkbox_value", text=Remove_Left_Side.name)

        if Remove_Right_Side:
            row = box.row()
            row.prop(Remove_Right_Side, "checkbox_value", text=Remove_Right_Side.name)

        row = box.row()
        row.prop(Door, "checkbox_value", text=Door.name)

        if Door.get_value():
            row = box.row()
            row.prop(self, 'Pull_Type', text="Pull Type", expand=True)
            row = box.row()
            row.label(text="Pull Location: ")
            if self.Pull_Type == '0':
                row.prop(Base_Pull_Location, "distance_value", text="")
            elif self.Pull_Type == '1':
                row.prop(Tall_Pull_Location, "distance_value", text="")
            else:
                row.prop(Upper_Pull_Location, "distance_value", text="")
            if Open_Door:
                row = box.row()
                row.prop(Open_Door, "factor_value", text=Open_Door.name)

            row = box.row()
            row.prop(Use_Left_Swing, "checkbox_value", text=Use_Left_Swing.name)
            row = box.row()
            row.prop(Force_Double_Doors, "checkbox_value", text=Force_Double_Doors.name)


class PROMPTS_Outside_Corner_Shelves(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.outside_corner_shelves"
    bl_label = "Triangle Shelves"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    height: FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth: FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))
        
    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        self.draw_product_size(layout)
        
        Left_Depth = self.product.get_prompt("Left Depth")
        Right_Depth = self.product.get_prompt("Right Depth")
        Shelf_Quantity = self.product.get_prompt("Shelf Quantity")
        
        box = layout.box()
        row = box.row()
        row.prop(Shelf_Quantity, "quantity_value", text=Shelf_Quantity.name)
 
        
class PROMPTS_Outside_Corner_Angle_Shelves(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.outside_corner_angle_shelves"
    bl_label = "Outside Corner Angle Shelves Prompts"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    height: FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth: FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))
        
    def draw(self, context):
        """ This is where you draw the interface """
        
        Left_Depth = self.product.get_prompt("Left Depth")
        Right_Depth = self.product.get_prompt("Right Depth")
        Shelf_Quantity = self.product.get_prompt("Shelf Quantity")
                
        layout = self.layout
        self.draw_product_size(layout)
        box = layout.box()
        row = box.row()
        row.prop(Left_Depth, "distance_value", text=Left_Depth.name)
        row.prop(Right_Depth, "distance_value", text=Right_Depth.name)
        box = layout.box()
        row = box.row()
        row.prop(Shelf_Quantity, "quantity_value", text=Shelf_Quantity.name)


class DROP_OPERATOR_Place_L_Shelves(bpy.types.Operator):
    bl_idname = "sn_closets.place_corner_l_shelves"
    bl_label = "Place Valance"
    bl_description = "This places a valance part on a shelf."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name: StringProperty(name="Object Name")
    
    product = None
    
    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.product = sn_types.Assembly(bp)
        self.product.obj_z.location.z = 0
        self.product.obj_x.location.x = 0
        sn_utils.set_wireframe(self.product.obj_bp,True)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        context.area.header_text_set(text="Select first shelf to add backing to.")
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.product:
            sn_utils.delete_object_and_children(self.product.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        context.area.header_text_set()
        return {'FINISHED'}

    def product_drop(self,context,event):
        selected_point, selected_obj = sn_utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        context.area.header_text_set(text="Select shelf to add valance to")
        sel_assembly_bp = sn_utils.get_assembly_bp(selected_obj)
        
        if sel_assembly_bp:
            
            if sel_assembly_bp.lm_cbd.is_shelf_bp:

                #HIGHLIGHT SELCTED ASSEMBLY
                sel_assembly = sn_types.Assembly(sel_assembly_bp)
                selected_obj.select = True                    
                
                #PARENT TO SHELF. THIS CAN BE THE PRODUCT OR INSERT
                self.product.obj_bp.parent = sel_assembly.obj_bp
                self.product.obj_bp.location.y = sel_assembly.obj_y.location.y
                self.product.obj_bp.location.z = sel_assembly.obj_z.location.z
                
                #Set Width of the back to the same as the shelf
                self.product.obj_x.location.x = sel_assembly.obj_x.location.x
                    
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    sn_utils.copy_drivers(sel_assembly.obj_x,self.product.obj_x)
                    
                    sn_utils.set_wireframe(self.product.obj_bp,False)
                    bpy.context.window.cursor_set('DEFAULT')
                    bpy.ops.object.select_all(action='DESELECT')
                    context.scene.objects.active = self.product.obj_bp
                    self.product.obj_bp.select = True
                    context.area.header_text_set()
                    return {'FINISHED'}
            else:
                self.product.obj_x.location.x = 0
        else:
            self.product.obj_x.location.x = 0

        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.product_drop(context,event)      


bpy.utils.register_class(DROP_OPERATOR_Place_L_Shelves)
bpy.utils.register_class(PROMPTS_L_Shelves)
bpy.utils.register_class(PROMPTS_Corner_Shelves)
bpy.utils.register_class(PROMPTS_Outside_Corner_Shelves)
bpy.utils.register_class(PROMPTS_Outside_Corner_Angle_Shelves)
