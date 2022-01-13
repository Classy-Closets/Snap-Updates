from os import path
import math
import time

import bpy
from bpy.types import Operator
from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty)

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts
from ..common import common_lists


class Doors(sn_types.Assembly):

    type_assembly = "INSERT"
    id_prompt = "sn_closets.door_prompts"
    drop_id = "sn_closets.insert_doors_drop"
    placement_type = "EXTERIOR"
    show_in_library = True
    category_name = "Products - Basic"
    mirror_y = False

    door_type = ""  # {Base, Tall, Upper, Sink, Suspended}
    striker_depth = sn_unit.inch(3.4)
    striker_thickness = sn_unit.inch(0.75)
    shelf_thickness_ppt_obj = None

    shelves = []
    shelf_z_loc_empties = []

    def __init__(self, obj_bp=None):
        super().__init__(obj_bp=obj_bp)
        self.shelves = []
        self.shelf_z_loc_empties = []
        self.get_shelves()

    def get_shelves(self):
        for child in self.obj_bp.children:
            if child.get("IS_SHELF"):
                shelf = sn_types.Assembly(child)
                is_locked_shelf = shelf.get_prompt("Is Locked Shelf")
                if is_locked_shelf:
                    if not is_locked_shelf.get_value():
                        self.shelves.append(sn_types.Assembly(child))

    def add_common_doors_prompts(self):
        props = bpy.context.scene.sn_closets
        defaults = props.closet_defaults

        common_prompts.add_thickness_prompts(self)
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_door_prompts(self)
        common_prompts.add_door_pull_prompts(self)
        common_prompts.add_door_lock_prompts(self)

        if defaults.use_plant_on_top and self.door_type == 'Upper':
            door_height = sn_unit.millimeter(1184)
        else:
            door_height = sn_unit.millimeter(653.288)

        for i in range(1,16):
            self.add_prompt("Shelf " + str(i) + " Height", 'DISTANCE', sn_unit.millimeter(76.962))
            self.add_prompt("Shelf " + str(i) + " Setback", 'DISTANCE', 0)

        ppt_obj_shelves = self.add_prompt_obj("Shelves")
        self.add_prompt("Shelf Stack Height", 'DISTANCE', 0, prompt_obj=ppt_obj_shelves)
        self.add_prompt("Doors Backing Gap", 'DISTANCE', 0, prompt_obj=ppt_obj_shelves)
        glass_thickness = self.add_prompt("Glass Thickness", 'DISTANCE', sn_unit.inch(0.75), prompt_obj=ppt_obj_shelves)

        self.add_prompt("Fill Opening", 'CHECKBOX', False)
        self.add_prompt("Insert Height", 'DISTANCE', door_height)
        self.add_prompt("Offset For Plant On Top", 'CHECKBOX', defaults.use_plant_on_top)
        self.add_prompt("Add Striker", 'CHECKBOX', False)
        self.add_prompt("Striker Depth", 'DISTANCE', self.striker_depth)
        self.add_prompt("Striker Thickness", 'DISTANCE', self.striker_thickness)
        self.add_prompt("Use Mirror", 'CHECKBOX', False)
        self.add_prompt("Glass Shelves", 'CHECKBOX', False)
        self.add_prompt("Add Shelves", 'CHECKBOX', 0)
        self.add_prompt("Shelf Quantity", 'QUANTITY', 3)
        self.add_prompt("Shelf Backing Setback", 'DISTANCE', 0)

        self.add_prompt("Top KD", 'CHECKBOX', True)
        self.add_prompt("Bottom KD", 'CHECKBOX', True)
        self.add_prompt("Use Bottom KD Setback", 'CHECKBOX', False)
        self.add_prompt("Pard Has Top KD", 'CHECKBOX', False)
        self.add_prompt("Pard Has Bottom KD", 'CHECKBOX', False)
        self.add_prompt("Placed In Invalid Opening", 'CHECKBOX', False)
        self.add_prompt("Has Blind Left Corner", 'CHECKBOX', False)
        self.add_prompt("Has Blind Right Corner", 'CHECKBOX', False)
        self.add_prompt("Left Blind Corner Depth", 'DISTANCE', 0)
        self.add_prompt("Right Blind Corner Depth", 'DISTANCE', 0)

        self.add_prompt("Is Slab Door", 'CHECKBOX', True)
        self.add_prompt("Has Center Rail", 'CHECKBOX', False)
        self.add_prompt("Center Rail Distance From Center", 'DISTANCE', 0)

        self.add_prompt("Full Overlay", 'CHECKBOX', False)
        self.add_prompt("Evenly Space Shelves", 'CHECKBOX', True)
        self.add_prompt("Thick Adjustable Shelves", 'CHECKBOX', bpy.context.scene.sn_closets.closet_defaults.thick_adjustable_shelves)

        self.add_prompt("Glass Shelf Thickness", 'COMBOBOX', 0, ['1/4"', '3/8"', '1/2"'])  # columns=3
        ST = self.get_prompt("Glass Shelf Thickness").get_var("ST")
        glass_thickness.set_formula('IF(ST==0,INCH(0.25),IF(ST==1,INCH(0.375),INCH(0.5)))', [ST])

        front_thickness = self.get_prompt('Front Thickness')
        front_thickness.set_value(sn_unit.inch(0.75))

    def set_door_drivers(self, assembly):
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Door_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_Gap')
        Top_Thickness = self.get_prompt("Top Thickness").get_var('Top_Thickness')
        Bottom_Thickness = self.get_prompt("Bottom Thickness").get_var('Bottom_Thickness')
        Top_Overlay = self.get_prompt("Top Overlay").get_var('Top_Overlay')
        Bottom_Overlay = self.get_prompt("Bottom Overlay").get_var('Bottom_Overlay')
        # TODO: create issue - prompts "Extend Top Amount", "Extend Bottom Amount" do not exist
        # eta = self.get_prompt("Extend Top Amount").get_var('eta')
        # eba = self.get_prompt("Extend Bottom Amount").get_var('eba')
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Insert_Height = self.get_prompt("Insert Height").get_var('Insert_Height')
        Fill_Opening = self.get_prompt("Fill Opening").get_var('Fill_Opening')
        Door_Type = self.get_prompt("Door Type").get_var('Door_Type')

        assembly.loc_y('-Door_Gap', [Door_Gap, Front_Thickness])
        assembly.loc_z(
            'IF(Door_Type==2,IF(Fill_Opening,0,Height-Insert_Height)-Bottom_Overlay,-Bottom_Overlay)',
            [Fill_Opening, Door_Type, Height, Insert_Height, Bottom_Thickness, Bottom_Overlay])
        assembly.rot_y(value=math.radians(-90))
        assembly.dim_x('IF(Fill_Opening,Height,Insert_Height)+Top_Overlay+Bottom_Overlay',
                       [Fill_Opening, Insert_Height, Height, Top_Overlay, Bottom_Overlay, Top_Thickness])
        assembly.dim_z('Front_Thickness', [Front_Thickness])

    def set_pull_drivers(self, assembly):
        self.set_door_drivers(assembly)

        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Pull_Length = assembly.get_prompt("Pull Length").get_var('Pull_Length')
        Pull_From_Edge = self.get_prompt("Pull From Edge").get_var('Pull_From_Edge')
        Base_Pull_Location = self.get_prompt("Base Pull Location").get_var('Base_Pull_Location')
        Tall_Pull_Location = self.get_prompt("Tall Pull Location").get_var('Tall_Pull_Location')
        Upper_Pull_Location = self.get_prompt("Upper Pull Location").get_var('Upper_Pull_Location')

        World_Z = self.obj_bp.snap.get_var('matrix_world[2][3]', 'World_Z')

        Insert_Height = self.get_prompt("Insert Height").get_var('Insert_Height')
        Fill_Opening = self.get_prompt("Fill Opening").get_var('Fill_Opening')
        Door_Type = self.get_prompt("Door Type").get_var('Door_Type')

        pull_loc_x = assembly.get_prompt("Pull X Location")
        pull_loc_x.set_formula('Pull_From_Edge', [Pull_From_Edge])
        pull_loc_z = assembly.get_prompt("Pull Z Location")
        pull_loc_z.set_formula(
            'IF(Door_Type==0,Base_Pull_Location+(Pull_Length/2),'
            'IF(Door_Type==1,IF(Fill_Opening,Height,Insert_Height)-Tall_Pull_Location+(Pull_Length/2)+World_Z,'
            'IF(Fill_Opening,Height,Insert_Height)-Upper_Pull_Location-(Pull_Length/2)))',
            [Door_Type, Base_Pull_Location, Pull_Length, Fill_Opening, Insert_Height, Upper_Pull_Location,
             Tall_Pull_Location, World_Z, Height])

    def add_shelves(self, glass=False, shelf_amt=3):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Shelf_Quantity = self.get_prompt("Shelf Quantity").get_var('Shelf_Quantity')
        Shelf_Backing_Setback = self.get_prompt("Shelf Backing Setback").get_var('Shelf_Backing_Setback')
        ST = self.get_prompt("Shelf Thickness").get_var('ST')
        Insert_Height = self.get_prompt("Insert Height").get_var('Insert_Height')
        Fill_Opening = self.get_prompt("Fill Opening").get_var('Fill_Opening')
        Door_Type = self.get_prompt("Door Type").get_var('Door_Type')
        Door_Hide = self.get_prompt("Hide").get_var("Door_Hide")
        Fill_Opening = self.get_prompt("Fill Opening").get_var('Fill_Opening')
        Door_Type = self.get_prompt("Door Type").get_var('Door_Type')
        Add_Shelves = self.get_prompt("Add Shelves").get_var('Add_Shelves')
        Glass_Shelves = self.get_prompt("Glass Shelves").get_var('Glass_Shelves')
        Glass_Thickness = self.get_prompt("Glass Thickness").get_var('Glass_Thickness')
        TAS = self.get_prompt("Thick Adjustable Shelves").get_var('TAS')

        previous_shelf = None

        for i in range(1, shelf_amt):
            ppt_shelf_height = eval("self.get_prompt('Shelf {} Height')".format(str(i)))
            Shelf_Height = ppt_shelf_height.get_var('Shelf_Height')
            shelf_empty = self.add_empty("Shelf Z Loc Empty")
            self.shelf_z_loc_empties.append(shelf_empty)

            if previous_shelf:
                prev_shelf_z_loc = previous_shelf.obj_bp.snap.get_var('location.z', 'prev_shelf_z_loc')
                shelf_empty.snap.loc_z('prev_shelf_z_loc+Shelf_Height', [prev_shelf_z_loc, Shelf_Height])
            else:
                shelf_empty.snap.loc_z(
                    'IF(Fill_Opening,Shelf_Height,IF(Door_Type!=2,Shelf_Height,Height-Insert_Height+Shelf_Height))',
                    [Fill_Opening, Shelf_Height, Insert_Height, Height, Door_Type])

            sh_z_loc = shelf_empty.snap.get_var('location.z', 'sh_z_loc')

            if not glass:
                shelf = common_parts.add_shelf(self)
                IBEKD = shelf.get_prompt('Is Bottom Exposed KD').get_var('IBEKD')
                shelf.dim_z('IF(AND(TAS,IBEKD==False), INCH(1),ST)', [ST, TAS, IBEKD])
            else:
                shelf = common_parts.add_glass_shelf(self)
                shelf.dim_z('Glass_Thickness', [Glass_Thickness])
                shelf.get_prompt('Hide').set_formula(
                    'IF(Add_Shelves,IF(Glass_Shelves,IF(Shelf_Quantity+1>' + str(i) + ',False,True),True),True)',
                    [Add_Shelves, Shelf_Quantity, Glass_Shelves])

            self.shelves.append(shelf)

            Adj_Shelf_Setback = shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
            Locked_Shelf_Setback = shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
            Adj_Shelf_Clip_Gap = shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')
            Shelf_Setback = self.get_prompt("Shelf " + str(i) + " Setback").get_var('Shelf_Setback')

            if not glass:
                Is_Locked_Shelf = shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')

            shelf.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
            shelf.loc_y('Depth-Shelf_Backing_Setback', [Depth, Shelf_Backing_Setback])
            shelf.loc_z('sh_z_loc', [sh_z_loc])
            shelf.dim_x(
                'Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
            shelf.dim_y(
                "-Depth"
                "+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)"
                "+Shelf_Setback+Shelf_Backing_Setback",
                [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback,
                    Shelf_Setback, Shelf_Backing_Setback])
            shelf.get_prompt('Hide').set_formula("Door_Hide", [Door_Hide])

            previous_shelf = shelf

    def add_glass_shelves(self):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Shelf_Qty = self.get_prompt("Shelf Qty").get_var('Shelf_Qty')
        Glass_Thickness = self.get_prompt("Glass Thickness").get_var('Glass_Thickness')
        Insert_Height = self.get_prompt("Insert Height").get_var('Insert_Height')
        Fill_Opening = self.get_prompt("Fill Opening").get_var('Fill_Opening')
        Door_Type = self.get_prompt("Door Type").get_var('Door_Type')
        Glass_Shelves = self.get_prompt("Glass Shelves").get_var('Glass_Shelves')

        glass_shelf = common_parts.add_glass_shelf(self)
        glass_shelf.draw_as_hidden_line()
        glass_shelf.loc_x(value=0)
        glass_shelf.loc_y('Depth',[Depth])
        glass_shelf.loc_z('IF(Fill_Opening,((Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1)),IF(Door_Type==2,Height-Insert_Height,0)+((Insert_Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1)))',
                        [Fill_Opening,Height,Glass_Thickness,Shelf_Qty,Insert_Height,Door_Type])
        glass_shelf.dim_x('Width',[Width])
        glass_shelf.dim_y('-Depth+.00635',[Depth])
        glass_shelf.dim_z('Glass_Thickness',[Glass_Thickness])

        hide = glass_shelf.get_prompt('Hide')
        hide.set_formula('IF(Glass_Shelves==False,True,IF(Shelf_Qty==0,True,False)) or Hide',[Shelf_Qty,Glass_Shelves,self.hide_var])
        z_qty = glass_shelf.get_prompt('Z Quantity')
        z_qty.set_formula('Shelf_Qty', [Shelf_Qty])

        z_offset = glass_shelf.get_prompt('Z Offset')
        z_offset.set_formula('IF(Fill_Opening,((Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Glass_Thickness,((Insert_Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Glass_Thickness)',
                         [Fill_Opening,Height,Glass_Thickness,Shelf_Qty,Insert_Height])

    def update(self):
        super().update()

        self.obj_bp["IS_BP_DOOR_INSERT"] = True
        self.obj_bp.snap.export_as_subassembly = True

        props = self.obj_bp.sn_closets
        props.is_door_insert_bp = True  # TODO: remove

        self.set_prompts()

        # self.obj_bp["ID_PROMPT"] = "sn_closets.openings"

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.add_common_doors_prompts()

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        LO = self.get_prompt("Left Overlay").get_var('LO')
        RO = self.get_prompt("Right Overlay").get_var('RO')
        Vertical_Gap = self.get_prompt("Vertical Gap").get_var('Vertical_Gap')
        Rotation = self.get_prompt("Door Rotation").get_var('Rotation')
        Open = self.get_prompt("Open").get_var('Open')
        double_door = self.get_prompt("Force Double Doors").get_var('double_door')
        DD = self.get_prompt("Force Double Doors").get_var('DD')
        left_swing = self.get_prompt("Use Left Swing").get_var('left_swing')
        ST = self.get_prompt("Shelf Thickness").get_var( 'ST')
        Insert_Height = self.get_prompt("Insert Height").get_var('Insert_Height')
        Fill_Opening = self.get_prompt("Fill Opening").get_var('Fill_Opening')
        DDAS = self.get_prompt("Double Door Auto Switch").get_var( 'DDAS')
        No_Pulls = self.get_prompt("No Pulls").get_var('No_Pulls')
        Lock_Door = self.get_prompt("Lock Door").get_var('Lock_Door')
        Lock_to_Panel = self.get_prompt("Lock to Panel").get_var('Lock_to_Panel')
        dt = self.get_prompt("Division Thickness").get_var('dt')
        ddl_offset = self.get_prompt("Double Door Lock Offset").get_var('ddl_offset')
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Door_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_Gap')
        Door_Type = self.get_prompt("Door Type").get_var('Door_Type')
        Offset_For_Plant_On_Top = self.get_prompt("Offset For Plant On Top").get_var('Offset_For_Plant_On_Top')
        Add_Striker = self.get_prompt("Add Striker").get_var('Add_Striker')
        Striker_Depth = self.get_prompt("Striker Depth").get_var('Striker_Depth')
        Striker_Thickness = self.get_prompt("Striker Thickness").get_var('Striker_Thickness')
        Glass_Shelves = self.get_prompt("Glass Shelves").get_var('Glass_Shelves')
        Shelf_Backing_Setback = self.get_prompt("Shelf Backing Setback").get_var('Shelf_Backing_Setback')
        Use_Bottom_KD_Setback = self.get_prompt("Use Bottom KD Setback").get_var()

        FO = self.get_prompt("Full Overlay").get_var('FO')
        DDHOD = self.get_prompt("Double Door Half Overlay Difference").get_var('DDHOD')
        DDFOD = self.get_prompt("Double Door Full Overlay Difference").get_var('DDFOD')
        SDFOD = self.get_prompt("Single Door Full Overlay Difference").get_var('SDFOD')

        Top_KD = self.get_prompt("Top KD").get_var('Top_KD')
        Bottom_KD = self.get_prompt("Bottom KD").get_var('Bottom_KD')
        Pard_Has_Top_KD = self.get_prompt("Pard Has Top KD").get_var('Pard_Has_Top_KD')
        Pard_Has_Bottom_KD = self.get_prompt("Pard Has Bottom KD").get_var('Pard_Has_Bottom_KD')
        Placed_In_Invalid_Opening = self.get_prompt("Placed In Invalid Opening").get_var('Placed_In_Invalid_Opening')
        Full_Overlay = self.get_prompt("Full Overlay").get_var('Full_Overlay')
        DDHOD = self.get_prompt("Double Door Half Overlay Difference").get_var('DDHOD')
        DDFOD = self.get_prompt("Double Door Full Overlay Difference").get_var('DDFOD')
        SDFOD = self.get_prompt("Single Door Full Overlay Difference").get_var('SDFOD')

        HBLC = self.get_prompt("Has Blind Left Corner").get_var('HBLC')
        HBRC = self.get_prompt("Has Blind Right Corner").get_var('HBRC')
        LBCD = self.get_prompt("Left Blind Corner Depth").get_var('LBCD')
        RBCD = self.get_prompt("Right Blind Corner Depth").get_var('RBCD')

        TAS = self.get_prompt("Thick Adjustable Shelves").get_var('TAS')

        door_backing_gap = self.get_prompt('Doors Backing Gap')
        door_backing_gap.set_formula('Insert_Height+ST*2', [Insert_Height, ST])  

        sq = self.get_prompt("Shelf Quantity").get_var('sq')
        sf1 = self.get_prompt("Shelf 1 Height").get_var('sf1')
        sf2 = self.get_prompt("Shelf 2 Height").get_var('sf2')
        sf3 = self.get_prompt("Shelf 3 Height").get_var('sf3')
        sf4 = self.get_prompt("Shelf 4 Height").get_var('sf4')
        sf5 = self.get_prompt("Shelf 5 Height").get_var('sf5')
        sf6 = self.get_prompt("Shelf 6 Height").get_var('sf6')
        sf7 = self.get_prompt("Shelf 7 Height").get_var('sf7')
        sf8 = self.get_prompt("Shelf 8 Height").get_var('sf8')
        sf9 = self.get_prompt("Shelf 9 Height").get_var('sf9')
        sf10 = self.get_prompt("Shelf 10 Height").get_var('sf10')
        sf11 = self.get_prompt("Shelf 11 Height").get_var('sf11')
        sf12 = self.get_prompt("Shelf 12 Height").get_var('sf12')
        sf13 = self.get_prompt("Shelf 13 Height").get_var('sf13')
        sf14 = self.get_prompt("Shelf 14 Height").get_var('sf14')
        sf15 = self.get_prompt("Shelf 15 Height").get_var('sf15')

        shelf_stack_height = self.get_prompt('Shelf Stack Height')
        shelf_stack_height.set_formula(
            'sf1+IF(sq>1,sf2,0)+IF(sq>2,sf3,0)+IF(sq>3,sf4,0)+IF(sq>4,sf5,0)+IF(sq>5,sf6,0)+IF(sq>6,sf7,0)+IF(sq>7,sf8,0)+IF(sq>8,sf9,0)+IF(sq>9,sf10,0)+IF(sq>10,sf11,0)+IF(sq>11,sf12,0)+IF(sq>12,sf13,0)+IF(sq>13,sf14,0)+IF(sq>14,sf15,0)', # ? Change height to allow correct door heights
            [sf1, sf2, sf3, sf4, sf5, sf6, sf7, sf8, sf9, sf10, sf11, sf12, sf13, sf14, sf15, sq])

        # STRIKER
        striker = common_parts.add_door_striker(self)
        striker.loc_y('Striker_Depth', [Striker_Depth])
        striker.loc_z('Height+Striker_Thickness', [Height, Striker_Thickness])
        striker.rot_x(value=math.radians(180))
        striker.dim_x('Width', [Width])
        striker.dim_y('Striker_Depth', [Striker_Depth])
        striker.dim_z('ST', [ST])
        hide = striker.get_prompt('Hide')
        hide.set_formula('IF(Add_Striker,False,True) or Hide',[Add_Striker,self.hide_var])

        # TODO: glass shelves
        # self.add_glass_shelves()
        # self.add_shelves()

        left_door = common_parts.add_door(self)
        left_door.set_name("Left Door")
        self.set_door_drivers(left_door)
        left_door.loc_x('IF(HBLC,LBCD-ST/4-INCH(0.375),IF(FO,-LO*2,-LO))', [LO, FO, HBLC, HBRC, ST, LBCD, Width])
        left_door.rot_z('radians(90)-Open*Rotation', [Open, Rotation])
        left_door.dim_y(
            'IF(OR(HBLC,HBRC),IF(OR(DD,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),(Width-IF(HBLC,LBCD,RBCD)+ST)/2,(Width-IF(HBLC,LBCD,RBCD)+ST)+ST/6),IF(OR(DD,Width>DDAS), IF(FO,(Width+(ST*2)-DDFOD)/2,(Width+LO+RO)/2-DDHOD) ,IF(FO,Width+(ST*2)-SDFOD,Width+LO+RO))) *-1',
            [DDHOD, DDFOD, SDFOD, DD, DDAS, Width, LO, RO, Vertical_Gap, FO, ST, HBLC, HBRC, LBCD, RBCD])
        hide = left_door.get_prompt('Hide')
        hide.set_formula(
            'IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS,left_swing),False,True),IF(OR(double_door,Width>DDAS,left_swing),False,True)) or Hide', 
            [self.hide_var, double_door, DDAS, left_swing, Width, HBLC, HBRC, LBCD, RBCD, ST])
        door_type = left_door.get_prompt('Door Type')
        door_type.set_formula('Door_Type', [Door_Type])
        door_swing = left_door.get_prompt('Door Swing')
        door_swing.set_value(0)
        no_pulls = left_door.get_prompt('No Pulls')
        no_pulls.set_formula('No_Pulls', [No_Pulls])
        cat_num = left_door.get_prompt('CatNum')
        cat_num.set_formula('IF(OR(double_door,Width>DDAS),51,52)', [double_door, Width, DDAS])

        left_pull = common_parts.add_door_pull(self)
        self.set_pull_drivers(left_pull)
        left_pull.loc_x('IF(HBLC,LBCD-ST/4-INCH(0.375),-LO)',[LO,HBLC,Width,LBCD,ST,HBRC,RBCD,double_door,DDAS])
        left_pull.rot_z('IF(HBLC,radians(90)-Open*Rotation,radians(90)-Open*Rotation)', [Open, Rotation, HBLC])
        left_pull.dim_y(
            'IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),((Width-IF(HBLC,LBCD,RBCD))/2),(Width-(IF(HBLC,LBCD,RBCD)))),IF(OR(double_door,Width>DDAS),(Width+LO+RO-Vertical_Gap)/2,(Width+LO+RO)))*-1',
            [double_door, DDAS, Width, LO, RO, Vertical_Gap, ST, HBLC, HBRC, LBCD, RBCD])
        hide = left_pull.get_prompt('Hide')
        hide.set_formula(
            'IF(No_Pulls,True,IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS,left_swing),False,True),IF(OR(double_door,Width>DDAS,left_swing),False,True))) or Hide', 
            [self.hide_var, No_Pulls, double_door, DDAS, left_swing, Width, HBLC, HBRC, LBCD, RBCD, ST])

        right_door = common_parts.add_door(self)
        right_door.set_name("Right Door")
        self.set_door_drivers(right_door)
        right_door.loc_x('IF(HBRC,Width-RBCD+ST/4+INCH(0.375),IF(FO, Width+(RO*2), Width+RO))',[Width,RO,FO,HBLC,HBRC,RBCD,ST])
        right_door.rot_z('radians(90)+Open*Rotation', [Open, Rotation])
        right_door.dim_y('IF(OR(HBLC,HBRC),IF(OR(DD,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),(Width-IF(HBLC,LBCD,RBCD)+ST)/2,(Width-IF(HBLC,LBCD,RBCD)+ST)+ST/6),IF(OR(DD,Width>DDAS), IF(FO,(Width+(ST*2)-DDFOD)/2,(Width+LO+RO)/2-DDHOD) ,IF(FO,Width+(ST*2)-SDFOD,Width+LO+RO)))',[DDHOD,DDFOD,SDFOD,DD,DDAS,Width,LO,RO,Vertical_Gap,FO,ST,HBLC,HBRC,LBCD,RBCD])
        hide = right_door.get_prompt('Hide')
        hide.set_formula(
            'IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),False,IF(left_swing,True,False)),IF(OR(double_door,Width>DDAS),False,IF(left_swing,True,False))) or Hide', 
            [self.hide_var, double_door,DDAS,Width,HBLC,HBRC,LBCD,RBCD,ST,left_swing])
        door_type = right_door.get_prompt('Door Type')
        door_type.set_formula('Door_Type',[Door_Type])
        door_swing = right_door.get_prompt('Door Swing')
        door_swing.set_value(1)
        no_pulls = right_door.get_prompt('No Pulls')
        no_pulls.set_formula('No_Pulls', [No_Pulls])
        cat_num = right_door.get_prompt('CatNum')
        cat_num.set_formula('IF(OR(double_door,Width>DDAS),51,52)', [double_door, Width, DDAS])

        right_pull = common_parts.add_door_pull(self)
        self.set_pull_drivers(right_pull)
        right_pull.loc_x('IF(HBRC,Width-RBCD+ST/4+INCH(0.375),Width+RO)',[RO,HBRC,Width,RBCD,ST,HBRC,double_door,DDAS])
        right_pull.rot_z('radians(90)+Open*Rotation', [Open, Rotation])
        right_pull.dim_y(
            'IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),((Width-IF(HBLC,LBCD,RBCD))/2),(Width-IF(HBLC,LBCD,RBCD))),IF(OR(double_door,Width>DDAS),(Width+LO+RO-Vertical_Gap)/2,(Width+LO+RO)))',
            [double_door, DDAS, Width, LO, RO, Vertical_Gap, ST, HBLC, HBRC, LBCD, RBCD])
        hide = right_pull.get_prompt('Hide')
        hide.set_formula('IF(No_Pulls,True,IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS,left_swing==False),False,True),IF(OR(double_door,Width>DDAS,left_swing==False),False,True))) or Hide', 
                          [self.hide_var, No_Pulls, double_door, DDAS, left_swing, Width, HBLC, HBRC, LBCD, RBCD, ST])
        
        #BOTTOM KD SHELF
        bottom_shelf = common_parts.add_shelf(self)
        IBEKD = bottom_shelf.get_prompt('Is Bottom Exposed KD').get_var('IBEKD')
        bottom_shelf.loc_x('Width',[Width])
        bottom_shelf.loc_y(
            'Depth-IF(Use_Bottom_KD_Setback,Shelf_Backing_Setback,0)',
            [Depth, Shelf_Backing_Setback, Use_Bottom_KD_Setback])
        bottom_shelf.loc_z('IF(Fill_Opening, 0, IF(Door_Type==2,Height-Insert_Height,0))', 
                    [Door_Type,Insert_Height,Height,ST,Fill_Opening])
        bottom_shelf.rot_z(value=math.radians(180))
        bottom_shelf.dim_x('Width',[Width])
        bottom_shelf.dim_y(
            'Depth-IF(Use_Bottom_KD_Setback,Shelf_Backing_Setback,0)',
            [Depth, Shelf_Backing_Setback, Use_Bottom_KD_Setback])
        # bottom_shelf.dim_z('IF(AND(TAS,IBEKD==False), INCH(1),ST) *-1', [ST, TAS, IBEKD])
        bottom_shelf.dim_z('-ST', [ST, TAS, IBEKD])
        hide = bottom_shelf.get_prompt('Hide')
        hide.set_formula(
            "IF(Placed_In_Invalid_Opening,IF(Door_Type!=2,True,IF(Bottom_KD, False, True)),IF(OR(AND(Pard_Has_Bottom_KD,Door_Type!=2),AND(Pard_Has_Bottom_KD,Fill_Opening)), True, IF(Bottom_KD, False, True))) or Hide", 
            [self.hide_var, Bottom_KD,Pard_Has_Bottom_KD,Door_Type,Fill_Opening,Placed_In_Invalid_Opening])
        is_locked_shelf = bottom_shelf.get_prompt('Is Locked Shelf')
        is_locked_shelf.set_value(True)
        bottom_shelf.get_prompt("Is Forced Locked Shelf").set_value(value=True)

        #TOP KD SHELF
        top_shelf = common_parts.add_shelf(self)
        IBEKD = top_shelf.get_prompt('Is Bottom Exposed KD').get_var('IBEKD')
        top_shelf.loc_x('Width',[Width])
        top_shelf.loc_y('Depth',[Depth])
        top_shelf.loc_z('IF(Fill_Opening, Height + ST,IF(Door_Type==2,Height + ST,Insert_Height + ST))',
                    [Door_Type,Insert_Height,Height,ST, Fill_Opening])
        top_shelf.rot_z(value=math.radians(180))
        top_shelf.dim_x('Width',[Width])
        top_shelf.dim_y('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        # top_shelf.dim_z('IF(AND(TAS,IBEKD==False), INCH(1),ST) *-1', [ST, TAS, IBEKD])
        top_shelf.dim_z('-ST', [ST, TAS, IBEKD])
        hide = top_shelf.get_prompt('Hide')
        hide.set_formula("IF(Placed_In_Invalid_Opening,IF(Door_Type==2,True,IF(Top_KD, False, True)),IF(OR(AND(Pard_Has_Top_KD,Door_Type==2),AND(Pard_Has_Top_KD,Fill_Opening)), True, IF(Top_KD, False, True))) or Hide", [Top_KD, Pard_Has_Top_KD,Door_Type,Fill_Opening,Placed_In_Invalid_Opening,self.hide_var])
        is_locked_shelf = top_shelf.get_prompt('Is Locked Shelf')
        is_locked_shelf.set_value(True)
        top_shelf.get_prompt("Is Forced Locked Shelf").set_value(value=True)
        
        opening = common_parts.add_opening(self)
        opening.loc_z('IF(Fill_Opening,0,IF(Door_Type==2,0,Insert_Height+ST))', [Door_Type, Insert_Height, ST, Fill_Opening])
        opening.dim_x('Width', [Width])
        opening.dim_y('Depth', [Depth])
        opening.dim_z('IF(Fill_Opening,Insert_Height,Height-Insert_Height-ST)', [Fill_Opening, Height, Insert_Height, ST])

        # LOCK
        door_lock = common_parts.add_lock(self)
        door_lock.loc_x('IF(OR(double_door,Width>DDAS),Width/2+ddl_offset,IF(left_swing,Width+IF(Lock_to_Panel,dt,-dt),IF(Lock_to_Panel,-dt,dt)))',
                        [Lock_to_Panel,left_swing,Width,double_door,dt,DDAS,ddl_offset])
        door_lock.loc_y('IF(OR(double_door,Width>DDAS),-Front_Thickness-Door_Gap,IF(Lock_to_Panel,Front_Thickness,-Front_Thickness-Door_Gap))',
                        [Lock_to_Panel,Door_Gap,Front_Thickness,dt,DDAS,double_door,Width])
        door_lock.rot_y('IF(OR(double_door,Width>DDAS),radians(90),IF(AND(left_swing,Lock_to_Panel==False),radians(180),0))',
                        [left_swing,double_door,Width,Lock_to_Panel,DDAS])
        door_lock.rot_z('IF(OR(double_door,Width>DDAS),0,IF(Lock_to_Panel==False,0,IF(left_swing,radians(90),radians(-90))))',
                        [Lock_to_Panel,left_swing,double_door,DDAS,Width])
        base_lock_z_location_formula = "IF(Fill_Opening,Height,Insert_Height)-INCH(1.5)"
        tall_lock_z_location_formula = "IF(Fill_Opening,Height/2,Insert_Height/2)-INCH(1.5)"
        upper_lock_z_location_formula = "IF(Fill_Opening,0,Height-Insert_Height)+INCH(1.5)"
        door_lock.loc_z('IF(Door_Type==0,' + base_lock_z_location_formula + ',IF(Door_Type==1,' + tall_lock_z_location_formula + ',' + upper_lock_z_location_formula + '))',
                        [Door_Type,Fill_Opening,Insert_Height,Height])
        hide = door_lock.get_prompt('Hide')
        hide.set_formula('IF(Lock_Door==True,IF(Open>0,IF(Lock_to_Panel,False,True),False),True) or Hide',  [self.hide_var, Lock_Door, Open, Lock_to_Panel])
        door_lock.material('Chrome')        
        
        self.update()


class PROMPTS_Door_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.door_prompts"
    bl_label = "Door Prompt" 
    bl_description = "This shows all of the available door options"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name")


    tabs: EnumProperty(name="Tabs",
                        items=[('DOOR','Door Options','Options for the door'),
                               ('SHELVES','Shelf Options','Options for the shelves')],
                        default = 'DOOR')

    door_type: EnumProperty(
        name="Door Type",
        items=[
            ('0', 'Base', 'Base'),
            ('1', 'Tall', 'Tall'),
            ('2', 'Upper', 'Upper')],
        default='2')

    glass_thickness: EnumProperty(
        name="Glass Thickness",
        items=[
            ('0', '1/4"', '1/4"'),
            ('1', '3/8"', '3/8"'),
            ('2', '1/2"', '1/2"')],
        default='0')

    glass_thickness_prompt = None
    shelf_thickness_prompt = None        
    
    assembly = None
    part = None

    shelf_quantity: EnumProperty(name="Shelf Quantity",
                                   items=[('1',"1",'1'),
                                          ('2',"2",'2'),
                                          ('3',"3",'3'),
                                          ('4',"4",'4'),
                                          ('5',"5",'5'),
                                          ('6',"6",'6'),
                                          ('7',"7",'7'),
                                          ('8',"8",'8'),
                                          ('9',"9",'9'),
                                          ('10',"10",'10'),
                                          ('11',"11",'11'),
                                          ('12',"12",'12'),
                                          ('13',"13",'13'),
                                          ('14',"14",'14'),
                                          ('15',"15",'15')],
                                   default = '3')

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
                                    
    Shelf_11_Height: EnumProperty(name="Shelf 11 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_12_Height: EnumProperty(name="Shelf 12 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_13_Height: EnumProperty(name="Shelf 13 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_14_Height: EnumProperty(name="Shelf 14 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_15_Height: EnumProperty(name="Shelf 15 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    plant_on_top_opening_height: EnumProperty(name="Height",
                                                 items=common_lists.PLANT_ON_TOP_OPENING_HEIGHTS)    
    
    door_opening_height: EnumProperty(name="Height",
                                                 items=common_lists.OPENING_HEIGHTS)  

    use_shelves: BoolProperty(name="Use Shelves", default=False)

    shelf_quantity_prompt = None
    door_type_prompt = None
    cur_shelf_height = None   

    @classmethod
    def poll(cls, context):
        return True

    def delete_shelves(self):
        for assembly in self.assembly.shelves:
            sn_utils.delete_object_and_children(assembly.obj_bp)
        sn_utils.delete_obj_list(self.assembly.shelf_z_loc_empties)    
        self.assembly.shelves.clear()
        self.assembly.shelf_z_loc_empties.clear()
    
    def add_shelves(self):
        glass_shelves = self.assembly.get_prompt("Glass Shelves")

        if glass_shelves.get_value():
            self.assembly.add_shelves(glass=True, shelf_amt=int(self.shelf_quantity))
        else:
            self.assembly.add_shelves(shelf_amt=int(self.shelf_quantity))

        self.assembly.update()
        bpy.ops.object.select_all(action='DESELECT')
    
    def update_shelves(self, context):
        add_shelves = self.assembly.get_prompt("Add Shelves")
        add_shelves.set_value(self.use_shelves)
        glass_shelves = self.assembly.get_prompt("Glass Shelves")
        shelf_amt_changed = len(self.assembly.shelves) != int(self.shelf_quantity)
        shelf_type_changed = False

        if self.assembly.shelves:
            shelf_bp = self.assembly.shelves[0].obj_bp
            shelf_type_changed = shelf_bp.get("IS_GLASS_SHELF") != glass_shelves.get_value()

        if add_shelves.get_value() and not self.assembly.shelves:
            self.add_shelves()
        if add_shelves.get_value() and shelf_amt_changed or shelf_type_changed:
            self.delete_shelves()
            self.add_shelves()
        if not add_shelves.get_value() and self.assembly.shelves:
            self.delete_shelves()

        context.view_layer.objects.active = self.assembly.obj_bp

    def check(self, context):
        start_time = time.perf_counter()
        props = bpy.context.scene.sn_closets
        self.update_shelves(context)

        if self.door_type_prompt:
            self.door_type_prompt.set_value(int(self.door_type))
            door_type_name = self.door_type_prompt.combobox_items[self.door_type_prompt.get_value()].name            

        if self.glass_thickness_prompt:
            self.glass_thickness_prompt.set_value(int(self.glass_thickness))

        if self.shelf_quantity_prompt:
            self.shelf_quantity_prompt.quantity_value = int(self.shelf_quantity)

        insert_height = self.assembly.get_prompt("Insert Height")
        carcass_height = self.assembly.obj_z.location.z
        fill_opening = self.assembly.get_prompt("Fill Opening")
        evenly_space_shelves = self.assembly.get_prompt("Evenly Space Shelves")
        prompts = [insert_height,fill_opening,evenly_space_shelves]
        
        for i in range(1,int(self.shelf_quantity)+1):
            shelf = self.assembly.get_prompt("Shelf " + str(i) + " Height")
            if shelf:
                # if not shelf.equal:
                exec("self.cur_shelf_height = float(self.Shelf_" + str(i) + "_Height)/1000")
                #If Shelf was Just Moved
                if(sn_unit.meter_to_inch(shelf.get_value()) != sn_unit.meter_to_inch(self.cur_shelf_height)):
                    
                    #Get the height of the previous shelves
                    total_shelf_height = 0
                    for ii in range (1,i+1):
                        exec("self.cur_shelf_height = float(self.Shelf_" + str(ii) + "_Height)/1000")
                        total_shelf_height = total_shelf_height + self.cur_shelf_height
                        #print(sn_unit.meter_to_inch(total_shelf_height))

                    #Adjust All Shelves above shelf that was just moved to evenly space themselves in the remaining space
                    for iii in range(i+1,int(self.shelf_quantity)+1):
                        next_shelf = self.assembly.get_prompt("Shelf " + str(iii) + " Height")
                        if all(prompts):
                            if(not evenly_space_shelves.get_value()):
                                if(fill_opening.get_value()):
                                    hole_count = math.ceil(((carcass_height-total_shelf_height)*1000)/32)
                                else:
                                    hole_count = math.ceil(((insert_height.get_value()-total_shelf_height)*1000)/32)
                                holes_per_shelf = round(hole_count/(int(self.shelf_quantity)+1-i))
                                if(holes_per_shelf >=3):
                                    next_shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0])/1000)
                                    exec("self.Shelf_" + str(iii) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0]")
                                else:
                                    next_shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[0][0])/1000)
                                    exec("self.Shelf_" + str(iii) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]")

                exec("shelf.distance_value = sn_unit.inch(float(self.Shelf_" + str(i) + "_Height) / 25.4)")  
                
                if all(prompts):
                    if(evenly_space_shelves.get_value()):
                        if(fill_opening.get_value()):
                            hole_count = math.ceil((carcass_height*1000)/32)
                        else:
                            hole_count = math.ceil((insert_height.get_value()*1000)/32)
                        holes_per_shelf = round(hole_count/(int(self.shelf_quantity)+1))
                        remainder = hole_count - (holes_per_shelf * (int(self.shelf_quantity)))

                        if(i <= remainder):
                                holes_per_shelf = holes_per_shelf + 1
                        if(holes_per_shelf >=3):
                            shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0])/1000)
                            exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0]")
                        else:
                            shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[0][0])/1000)
                            exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]")

        if props.closet_defaults.use_32mm_system:
            insert_height = self.assembly.get_prompt("Insert Height")
            offset_for_plant_on_top = self.assembly.get_prompt("Offset For Plant On Top")
            if insert_height:
                if door_type_name == 'Upper' and offset_for_plant_on_top.get_value():
                    insert_height.distance_value = sn_unit.inch(float(self.plant_on_top_opening_height) / 25.4)
                else:
                    if fill_opening:
                        if fill_opening.get_value():
                            insert_height.distance_value = self.assembly.obj_z.location.z
                        else:
                            insert_height.distance_value = sn_unit.inch(float(self.door_opening_height) / 25.4)
                    else:
                        insert_height.distance_value = sn_unit.inch(float(self.door_opening_height) / 25.4)
        
        lucite_doors = self.assembly.get_prompt('Lucite Doors')
        draw_type = 'TEXTURED'

        fill_opening = self.assembly.get_prompt("Fill Opening").get_value()
        top_pard_KD = self.assembly.get_prompt("Pard Has Top KD")
        top_KD = self.assembly.get_prompt("Top KD")
        bottom_pard_KD = self.assembly.get_prompt("Pard Has Bottom KD")
        bottom_KD = self.assembly.get_prompt("Bottom KD")

        kd_prompts = [
            top_pard_KD,
            bottom_pard_KD,
            top_KD,
            bottom_KD
        ]
        closet_obj = None
        closet_assembly = None

        closet_obj = sn_utils.get_closet_bp(self.assembly.obj_bp)
        if "IS_BP_CLOSET" in closet_obj:
            closet_assembly = sn_types.Assembly(closet_obj)

        if all(kd_prompts):
            if(closet_assembly):
                if(closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.sn_closets.opening_name)):
                    does_opening_have_top_KD = closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.sn_closets.opening_name)
                    does_opening_have_bottom_KD = closet_assembly.get_prompt("Remove Bottom Hanging Shelf " + self.assembly.obj_bp.sn_closets.opening_name)
                    if(fill_opening):
                        if(top_KD.get_value()):
                            does_opening_have_top_KD.set_value(True)
                            top_pard_KD.set_value(True)
                        else:
                            does_opening_have_top_KD.set_value(False)
                            top_pard_KD.set_value(False)

                        if(bottom_KD.get_value()):
                            does_opening_have_bottom_KD.set_value(True)
                            bottom_pard_KD.set_value(True)
                        else:
                            does_opening_have_bottom_KD.set_value(False)
                            bottom_pard_KD.set_value(False)
                    else:
                        if door_type_name=='Upper':
                            if(top_KD.get_value()):
                                does_opening_have_top_KD.set_value(True)
                                top_pard_KD.set_value(True)
                            else:
                                does_opening_have_top_KD.set_value(False)
                                top_pard_KD.set_value(False)
                        else:
                            if(bottom_KD.get_value()):
                                does_opening_have_bottom_KD.set_value(True)
                                bottom_pard_KD.set_value(True)
                            else:
                                does_opening_have_bottom_KD.set_value(False)
                                bottom_pard_KD.set_value(False)
            else:
                placed_in_invalid_opening = self.assembly.get_prompt("Placed In Invalid Opening")
                placed_in_invalid_opening.set_value(True)
                if(fill_opening):
                    top_KD.set_value(False)
                    bottom_KD.set_value(False)
                elif door_type_name == 'Upper':
                    top_KD.set_value(False)
                else:
                    bottom_KD.set_value(False)
        
        self.assign_mirror_material(self.assembly.obj_bp)
        
        for child in self.assembly.obj_bp.children:
            if 'IS_DOOR' in child:
                if not child.visible_get:
                    door_assembly = sn_types.Assembly(child)
                    door_style = door_assembly.get_prompt("Door Style")
                    is_slab_door = self.assembly.get_prompt("Is Slab Door")
                    has_center_rail = self.assembly.get_prompt("Has Center Rail")
                    prompts = [door_style,is_slab_door,has_center_rail]
                    if all(prompts):
                        if(door_style.get_value() == "Slab Door"):
                            is_slab_door.set_value(True)
                            has_center_rail.set_value(False)
                        else:
                            is_slab_door.set_value(False)

        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        bpy.ops.snap.update_scene_from_pointers()
        return True
    
    def assign_mirror_material(self,obj):
        use_mirror = self.assembly.get_prompt("Use Mirror")
        if use_mirror.get_value():
            if obj.snap.type_mesh == 'BUYOUT':
                for mat_slot in obj.snap.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Mirror'  
        else:
            if obj.snap.type_mesh == 'BUYOUT':
                for mat_slot in obj.snap.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Glass'  
                    
        
        for child in obj.children:
            self.assign_mirror_material(child)

    def execute(self, context):
        self.tabs = 'DOOR'      
        return {'FINISHED'}

    def set_properties_from_prompts(self):
        insert_height = self.assembly.get_prompt("Insert Height")
        door_type = self.assembly.get_prompt("Door Type")
        offset_for_plant_on_top = self.assembly.get_prompt("Offset For Plant On Top")
        self.glass_thickness_prompt = self.assembly.get_prompt("Glass Shelf Thickness")
        add_shelves = self.assembly.get_prompt("Add Shelves")

        if add_shelves:
            self.use_shelves = add_shelves.get_value()

        if door_type:
            self.door_type_prompt = door_type
            self.door_type = str(self.door_type_prompt.combobox_index)
            door_type_name = self.door_type_prompt.combobox_items[self.door_type_prompt.get_value()].name

        if self.glass_thickness_prompt:
            self.glass_thickness = str(self.glass_thickness_prompt.combobox_index)        

        self.shelf_quantity_prompt = self.assembly.get_prompt("Shelf Quantity")
        if self.shelf_quantity_prompt:
            self.shelf_quantity = str(self.shelf_quantity_prompt.quantity_value)

        for i in range(1, 16):
            shelf = self.assembly.get_prompt("Shelf " + str(i) + " Height")
            if shelf:
                value = round(shelf.get_value() * 1000, 3)
                for index, height in enumerate(common_lists.SHELF_IN_DOOR_HEIGHTS):
                    if not value >= float(height[0]):
                        exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[index - 1][0]")
                        break

        if insert_height:
            if door_type_name == 'Upper' and offset_for_plant_on_top.get_value():
                value = round(insert_height.distance_value * 1000, 3)
                for index, height in enumerate(common_lists.PLANT_ON_TOP_OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        self.plant_on_top_opening_height = common_lists.PLANT_ON_TOP_OPENING_HEIGHTS[index - 1][0]
                        break
            else:
                fill_opening = self.assembly.get_prompt("Fill Opening")
                if fill_opening:
                    if not fill_opening.get_value():
                        value = round(insert_height.distance_value * 1000, 3)
                        for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                            if not value >= float(height[0]):
                                self.door_opening_height = common_lists.OPENING_HEIGHTS[index - 1][0]
                                break
                else:
                    value = round(insert_height.distance_value * 1000, 3)
                    for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                        if not value >= float(height[0]):
                            self.door_opening_height = common_lists.OPENING_HEIGHTS[index - 1][0]
                            break

    def invoke(self,context,event):
        obj = bpy.data.objects[context.object.name]
        self.assembly = Doors(self.get_insert().obj_bp)
        obj_assembly_bp = sn_utils.get_assembly_bp(obj)
        self.part = sn_types.Assembly(obj_assembly_bp)
        self.set_properties_from_prompts()
        
        door_type_name = self.door_type_prompt.combobox_items[self.door_type_prompt.get_value()].name        
        fill_opening = self.assembly.get_prompt("Fill Opening").get_value()

        top_pard_KD = self.assembly.get_prompt("Pard Has Top KD")
        top_KD = self.assembly.get_prompt("Top KD")
        bottom_pard_KD = self.assembly.get_prompt("Pard Has Bottom KD")
        bottom_KD = self.assembly.get_prompt("Bottom KD")

        closet_obj = None
        closet_assembly = None

        closet_obj = sn_utils.get_closet_bp(self.assembly.obj_bp)
        if "IS_BP_CLOSET" in closet_obj:
            closet_assembly = sn_types.Assembly(closet_obj)

        placed_in_invalid_opening = self.assembly.get_prompt("Placed In Invalid Opening")            

        if(closet_assembly):
            Blind_Corner_Left = closet_assembly.get_prompt("Blind Corner Left")
            Blind_Corner_Right = closet_assembly.get_prompt("Blind Corner Right")
            Blind_Left_Depth = closet_assembly.get_prompt("Blind Left Depth")
            Blind_Right_Depth = closet_assembly.get_prompt("Blind Right Depth")
            Has_Blind_Left_Corner = self.assembly.get_prompt("Has Blind Left Corner")                
            Has_Blind_Right_Corner = self.assembly.get_prompt("Has Blind Right Corner")
            Left_Blind_Corner_Depth = self.assembly.get_prompt("Left Blind Corner Depth")                
            Right_Blind_Corner_Depth = self.assembly.get_prompt("Right Blind Corner Depth")


            kd_prompts = [
                top_pard_KD,
                bottom_pard_KD,
                top_KD,
                bottom_KD
            ]       


            bcp_prompts = [
                Blind_Corner_Left,
                Blind_Corner_Right,
                Blind_Left_Depth,
                Blind_Right_Depth,
                Has_Blind_Left_Corner,
                Has_Blind_Right_Corner,
                Left_Blind_Corner_Depth,
                Right_Blind_Corner_Depth
            ]

            if all(kd_prompts):
                if(closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.sn_closets.opening_name)):
                    does_opening_have_top_KD = closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.sn_closets.opening_name).get_value()
                    does_opening_have_bottom_KD = closet_assembly.get_prompt("Remove Bottom Hanging Shelf " + self.assembly.obj_bp.sn_closets.opening_name).get_value()
                    if(fill_opening):
                        if(does_opening_have_top_KD):
                            top_pard_KD.set_value(True)
                            top_KD.set_value(True)
                        else:
                            top_pard_KD.set_value(False)
                            top_KD.set_value(False)

                        if(does_opening_have_bottom_KD):
                            bottom_pard_KD.set_value(True)
                            bottom_KD.set_value(True)
                        else:
                            bottom_pard_KD.set_value(False)
                            bottom_KD.set_value(False)
                    else:
                        if door_type_name == 'Upper':
                            if(does_opening_have_top_KD):
                                top_pard_KD.set_value(True)
                                top_KD.set_value(True)
                            else:
                                top_pard_KD.set_value(False)
                                top_KD.set_value(False)
                        else:
                            if(does_opening_have_bottom_KD):
                                bottom_pard_KD.set_value(True)
                                bottom_KD.set_value(True)
                            else:
                                bottom_pard_KD.set_value(False)
                                bottom_KD.set_value(False)


            if(closet_assembly.get_prompt("Opening 1 Height")):
                opening_quantity = 0
                for i in range(1,10):
                    if(sn_types.Assembly(self.assembly.obj_bp.parent).get_prompt("Opening " + str(i) + " Height") == None):
                                    opening_quantity = i - 1
                                    break

                if all(bcp_prompts):
                    if(opening_quantity == 1):
                        if Blind_Corner_Left:
                            Has_Blind_Right_Corner.set_value(False)

                        elif Blind_Corner_Right:
                            Has_Blind_Right_Corner.set_value(True)
                            Has_Blind_Left_Corner.set_value(False)

                        else:
                            Has_Blind_Right_Corner.set_value(False)
                            Has_Blind_Left_Corner.set_value(False)

                    elif(self.assembly.obj_bp.sn_closets.opening_name == '1'):
                        if Blind_Corner_Left:
                            Has_Blind_Left_Corner.set_value(True)
                        else:
                            Has_Blind_Left_Corner.set_value(False)

                    elif(self.assembly.obj_bp.sn_closets.opening_name == str(opening_quantity)):

                        if Blind_Corner_Right:
                            Has_Blind_Right_Corner.set_value(True)
                        else:
                            Has_Blind_Right_Corner.set_value(False)

                    else:
                        Has_Blind_Left_Corner.set_value(False)
                        Has_Blind_Right_Corner.set_value(False)
                    Left_Blind_Corner_Depth.set_value(Blind_Left_Depth.get_value())
                    Right_Blind_Corner_Depth.set_value(Blind_Right_Depth.get_value())

        else:
            placed_in_invalid_opening.set_value(True)
            Has_Blind_Left_Corner = self.assembly.get_prompt("Has Blind Left Corner")                
            Has_Blind_Right_Corner = self.assembly.get_prompt("Has Blind Right Corner")
            Left_Blind_Corner_Depth = self.assembly.get_prompt("Left Blind Corner Depth")                
            Right_Blind_Corner_Depth = self.assembly.get_prompt("Right Blind Corner Depth")
            if(fill_opening):
                top_KD.set_value(False)
                bottom_KD.set_value(False)
            elif door_type_name == 'Upper':
                top_KD.set_value(False)
            else:
                bottom_KD.set_value(False)
            Has_Blind_Left_Corner.set_value(False)
            Has_Blind_Right_Corner.set_value(False)


        for child in self.assembly.obj_bp.children:
            if 'IS_DOOR' in child:
                if not child.visible_get():
                    door_assembly = sn_types.Assembly(child)
                    door_style = door_assembly.get_prompt("Door Style")
                    is_slab_door = self.assembly.get_prompt("Is Slab Door")
                    has_center_rail = self.assembly.get_prompt("Has Center Rail")
                    prompts = [door_style,is_slab_door,has_center_rail]
                    if all(prompts):
                        if(door_style.get_value() == "Slab Door"):
                            is_slab_door.set_value(True)
                            has_center_rail.set_value(False)
                        else:
                            is_slab_door.set_value(False)
                
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=375)
        
    def is_glass_door(self):
        if "Glass" in self.part.obj_bp.snap.comment:
            return True
        else:
            return False
        
    def draw(self, context):
        layout = self.layout

        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                props = bpy.context.scene.sn_closets
                
                door_type = self.assembly.get_prompt("Door Type")
                open_prompt = self.assembly.get_prompt("Open")
                pull_type = self.assembly.get_prompt('Pull Location')
                use_left_swing = self.assembly.get_prompt('Use Left Swing')
                force_double_door = self.assembly.get_prompt('Force Double Doors')
                lucite_doors = self.assembly.get_prompt('Lucite Doors')
                force_double_door = self.assembly.get_prompt('Force Double Doors')
                lucite_doors = self.assembly.get_prompt('Lucite Doors')    
                fill_opening = self.assembly.get_prompt('Fill Opening')       
                lock_door = self.assembly.get_prompt('Lock Door')   
                lock_to_panel = self.assembly.get_prompt('Lock to Panel')   
                insert_height = self.assembly.get_prompt("Insert Height")
                no_pulls = self.assembly.get_prompt("No Pulls")
                shelf_qty = self.assembly.get_prompt("Shelf Qty")
                offset_for_plant_on_top = self.assembly.get_prompt("Offset For Plant On Top") 
                add_striker = self.assembly.get_prompt("Add Striker")
                use_mirror = self.assembly.get_prompt("Use Mirror")
                glass_shelves = self.assembly.get_prompt("Glass Shelves")
                glass_shelf_thickness = self.assembly.get_prompt("Glass Shelf Thickness")
                full_overlay = self.assembly.get_prompt("Full Overlay")
                top_KD = self.assembly.get_prompt("Top KD")
                bottom_KD = self.assembly.get_prompt("Bottom KD")
                placed_in_invalid_opening = self.assembly.get_prompt("Placed In Invalid Opening")       
                is_slab_door = self.assembly.get_prompt("Is Slab Door")
                has_center_rail = self.assembly.get_prompt("Has Center Rail")        
                center_rail_distance_from_center = self.assembly.get_prompt("Center Rail Distance From Center")
                shelf_quantity = self.assembly.get_prompt("Shelf Quantity")   
                evenly_space_shelves = self.assembly.get_prompt("Evenly Space Shelves") 
                add_shelves = self.assembly.get_prompt("Add Shelves")
                door_type_name = door_type.combobox_items[door_type.get_value()].name
                      
                box = layout.box()
                row = box.row()
                if add_shelves:
                    row.prop(self,'tabs',expand=True)

                if self.tabs == 'DOOR':
                    box.label(text="Opening Options:")
                    box.prop(add_striker, "checkbox_value", text=add_striker.name)
                    row = box.row()
                    row.label(text="Fill Opening")
                    row.prop(fill_opening,'checkbox_value',text="") 
                    if fill_opening.get_value() != True:
                        row = box.row()
                        if props.closet_defaults.use_32mm_system:
                            row.label(text="Opening Height:")
                            row = box.row()                            
                            if door_type_name == 'Upper' and offset_for_plant_on_top.get_value():
                                row.prop(self,'plant_on_top_opening_height',text="") 
                            else:
                                row.prop(self,'door_opening_height',text="") 
                        else:
                            insert_height.draw_prompt(row)
                            row.prop(insert_height, "distance_value", text=insert_height.name)
                    
                    row = box.row()
                    if shelf_qty:
                        row.prop(shelf_qty, "quantity_value", text=shelf_qty.name)               
                    
                    box = layout.box()
                    box.label(text="Door Options:")
                    if door_type:
                        row = box.row()
                        row.prop(self, "door_type", expand=True)
                        row = box.row()

                        if door_type_name == 'Base':
                            pull_location = self.assembly.get_prompt('Base Pull Location')
                            row.label(text=pull_location.name)
                            row.prop(pull_location, "distance_value", text="")
                        if door_type_name == 'Tall':
                            pull_location = self.assembly.get_prompt('Tall Pull Location')
                            row.label(text=pull_location.name)
                            row.prop(pull_location, "distance_value", text="")
                        if door_type_name == 'Upper':
                            pull_location = self.assembly.get_prompt('Upper Pull Location')
                            row.label(text=pull_location.name)
                            row.prop(pull_location, "distance_value", text="")              

                    row = box.row()
                    row.label(text="Open Door")
                    row.prop(open_prompt, 'factor_value', slider=True, text="")

                    if has_center_rail and is_slab_door and center_rail_distance_from_center:
                        if not is_slab_door.get_value():
                            row = box.row()
                            row.label(text="Center Rail")
                            row.prop(has_center_rail, 'checkbox_value', text="")
                            if has_center_rail.get_value():
                                row = box.row()
                                row.label(text="Distance From Center")
                                row.prop(center_rail_distance_from_center, 'distance_value', text="")

                    if top_KD and bottom_KD:
                        if(placed_in_invalid_opening and placed_in_invalid_opening.get_value()==False):
                            row = box.row()              
                            row.label(text="Top KD")
                            row.prop(top_KD,'checkbox_value',text="")
                            row = box.row()               
                            row.label(text="Bottom KD")
                            row.prop(bottom_KD,'checkbox_value',text="")
                        else:
                            if(fill_opening.get_value()==False):
                                if door_type_name == 'Upper':
                                    row = box.row()              
                                    row.label(text="Top KD")
                                    row.prop(top_KD,'checkbox_value',text="")
                                    row = box.row()               
                                    row.label(text="Bottom KD")
                                    row.prop(bottom_KD,'checkbox_value',text="")
                                else:
                                    row = box.row()              
                                    row.label(text="Top KD")
                                    row.prop(top_KD,'checkbox_value',text="")

                        row = box.row()
                        row.label(text="Force Double Door")
                        row.prop(force_double_door,'checkbox_value',text="")
                        row = box.row()
                        row.label(text="Left Swing")
                        row.prop(use_left_swing,'checkbox_value',text="")
                        row = box.row()
                        row.label(text="No Pulls")
                        row.prop(no_pulls,'checkbox_value',text="")        
                        row = box.row()
                        row.label(text="Lock Door")
                        row.prop(lock_door,'checkbox_value',text="")   
                        if lock_door.get_value() and force_double_door.get_value() == False and self.assembly.obj_x.location.x < sn_unit.inch(24):             
                            row = box.row()
                            row.label(text="Lock to Panel")
                            row.prop(lock_to_panel,'checkbox_value',text="")
                        
                        if full_overlay:
                            row = box.row()
                            row.label(text="Full Overlay")
                            row.prop(full_overlay,'checkbox_value',text="")

                        if self.is_glass_door():
                            row = box.row()
                            use_mirror.draw_prompt(row)

                elif self.tabs == 'SHELVES':
                    row=box.row()
                    row.label(text="Add Shelves")
                    row.prop(self, 'use_shelves', text="")
                    if(add_shelves):
                        if(add_shelves.get_value()):
                            if shelf_quantity:
                                col = box.column(align=True)
                                row = col.row()
                                row.label(text="Qty:")
                                row.prop(self, "shelf_quantity", expand=True)
                                col.separator()

                                if glass_shelves:
                                    row = box.row()
                                    row.label(text="Glass Shelves: ")
                                    row.prop(glass_shelves, "checkbox_value", text="")
                                    if glass_shelves.get_value() and self.glass_thickness_prompt:
                                        row = box.row()
                                        row.label(text="Glass Shelf Thickness: ")
                                        row.prop(self, "glass_thickness", expand=True)

                                row = box.row()
                                row.label(text="Evenly Space Shelves: ")
                                row.prop(evenly_space_shelves, 'checkbox_value', text="")
                                for i in range(1, shelf_quantity.get_value() + 1):
                                    shelf = self.assembly.get_prompt("Shelf " + str(i) + " Height")
                                    setback = self.assembly.get_prompt("Shelf " + str(i) + " Setback")
                                    if shelf:
                                        row = box.row()
                                        if(evenly_space_shelves.get_value()):
                                            row.label(text="Shelf " + str(i) + " Height:")
                                            row.label(text=str(math.ceil((shelf.get_value()*1000)/32)) +"H-" + str(round(sn_unit.meter_to_active_unit(shelf.distance_value),3)) + '"')
                                        else:
                                            row.label(text="Shelf " + str(i) + " Height:")
                                            row.prop(self,'Shelf_' + str(i) + '_Height',text="")
                                    
                                    if setback:
                                        row = box.row()
                                        row.label(text="Shelf " + str(i) + " Setback")
                                        row.prop(setback,'distance_value',text="")


class OPS_Doors_Drop(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.insert_doors_drop"
    bl_label = "Custom drag and drop for doors insert"
    adjacent_cant_be_deeper = True

    def execute(self, context):
        return super().execute(context)    

    def confirm_placement(self, context):
        super().confirm_placement(context)
        self.set_backing_top_gap(self.insert.obj_bp, self.selected_opening)
        context.view_layer.objects.active = self.insert.obj_bp
        closet_obj = None
        closet_assembly = None
        opening_width = None

        closet_obj = sn_utils.get_closet_bp(self.insert.obj_bp)
        if "IS_BP_CLOSET" in closet_obj:
            closet_assembly = sn_types.Assembly(closet_obj)

        if closet_assembly:
            width = closet_assembly.get_prompt("Opening " + self.insert.obj_bp.sn_closets.opening_name + " Width")
            if(width):
                opening_width = width.distance_value

            if(closet_assembly.get_prompt("Remove Top Shelf " + self.insert.obj_bp.sn_closets.opening_name)):
                self.insert.get_prompt("Pard Has Top KD").set_value(closet_assembly.get_prompt("Remove Top Shelf " + self.insert.obj_bp.sn_closets.opening_name).get_value())
                self.insert.get_prompt("Pard Has Bottom KD").set_value(closet_assembly.get_prompt("Remove Bottom Hanging Shelf " + self.insert.obj_bp.sn_closets.opening_name).get_value())
                if(self.insert.get_prompt("Pard Has Top KD").get_value() is False and self.insert.get_prompt("Door Type").get_value() == 2):
                    self.insert.get_prompt("Pard Has Top KD").set_value(True)
                    closet_assembly.get_prompt("Remove Top Shelf " + self.insert.obj_bp.sn_closets.opening_name).set_value(True)
            if(closet_assembly.get_prompt("Opening 1 Height")):
                opening_quantity = 0
                left_depth = 0
                right_depth = 0
                if(closet_assembly.get_prompt("Blind Corner Left Depth") and closet_assembly.get_prompt("Blind Corner Right Depth")):
                    left_depth = closet_assembly.get_prompt("Blind Corner Left Depth").get_value()
                    right_depth = closet_assembly.get_prompt("Blind Corner Right Depth").get_value()
                    for i in range(1, 10):
                        if(closet_assembly.get_prompt("Opening " + str(i) + " Height") is None):
                            opening_quantity = (i - 1)
                            break
                    if(opening_quantity == 1):
                        if(closet_assembly.get_prompt("Blind Corner Left").get_value()):
                            self.insert.get_prompt("Has Blind Left Corner").set_value(True)
                            self.insert.get_prompt("Use Left Swing").set_value(True)
                            opening_width = opening_width - left_depth + sn_unit.inch(0.75)
                        if(closet_assembly.get_prompt("Blind Corner Right").get_value()):
                            self.insert.get_prompt("Has Blind Right Corner").set_value(True)
                            opening_width = opening_width - right_depth + sn_unit.inch(0.75)
                    elif(self.insert.obj_bp.sn_closets.opening_name == '1'):
                        if(closet_assembly.get_prompt("Blind Corner Left").get_value()):
                            self.insert.get_prompt("Has Blind Left Corner").set_value(True)
                            self.insert.get_prompt("Use Left Swing").set_value(True)
                            opening_width = opening_width - left_depth + sn_unit.inch(0.75)
                    elif(self.insert.obj_bp.sn_closets.opening_name == str(opening_quantity)):
                        if(closet_assembly.get_prompt("Blind Corner Right").get_value()):
                            self.insert.get_prompt("Has Blind Right Corner").set_value(True)
                            opening_width = opening_width - right_depth + sn_unit.inch(0.75)
                    else:
                        self.insert.get_prompt("Has Blind Left Corner").set_value(False)
                        self.insert.get_prompt("Has Blind Right Corner").set_value(False)

                    self.insert.get_prompt("Left Blind Corner Depth").set_value(left_depth)
                    self.insert.get_prompt("Right Blind Corner Depth").set_value(right_depth)

            if(opening_width and opening_width >= sn_unit.inch(21)): 
                force_double_door = self.insert.get_prompt("Force Double Doors")
                if(force_double_door):
                    force_double_door.set_value(True)
        else:
            placed_in_invalid_opening = self.insert.get_prompt("Placed In Invalid Opening")
            placed_in_invalid_opening.set_value(True)
            self.insert.get_prompt("Has Blind Left Corner").set_value(False)
            self.insert.get_prompt("Has Blind Right Corner").set_value(False)
            self.insert.get_prompt("Left Blind Corner Depth").set_value(0)
            self.insert.get_prompt("Right Blind Corner Depth").set_value(0)

        self.selected_opening.obj_bp.snap.interior_open = False

        # TOP LEVEL PRODUCT RECAL
        sn_utils.run_calculators(sn_utils.get_closet_bp(self.insert.obj_bp))
        sn_utils.run_calculators(sn_utils.get_closet_bp(self.insert.obj_bp))

    def set_backing_top_gap(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.sn_closets.opening_name
        carcass_bp = sn_utils.get_closet_bp(insert_bp)
        doors_assembly = sn_types.Assembly(insert_bp)
        Doors_Backing_Gap = doors_assembly.get_prompt('Doors Backing Gap').get_var()

        for child in carcass_bp.children:
            if child.sn_closets.is_back_bp:
                if child.sn_closets.opening_name == opening_name:
                    back_assembly = sn_types.Assembly(child)
                    top_insert_backing = back_assembly.get_prompt('Top Insert Backing')
                    if top_insert_backing:
                        top_insert_backing.set_formula('Doors_Backing_Gap', [Doors_Backing_Gap])


bpy.utils.register_class(PROMPTS_Door_Prompts)
bpy.utils.register_class(OPS_Doors_Drop)
