import bpy
from bpy.types import Operator
from bpy.props import EnumProperty

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from ..common import common_parts
from ..common import common_prompts
from ..common import common_lists


class Hanging_Rods_with_Shelves(sn_types.Assembly):

    type_assembly = "INSERT"
    id_prompt = "sn_closets.hanging_rod_with_shelves_prompts"
    drop_id = "sn_closets.insert_rods_and_shelves_drop"
    placement_type = "INTERIOR"
    show_in_library = True
    category_name = "Closet Products - Basic"
    mirror_y = False

    def add_rod(self, assembly, location, is_hanger=False):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        # Setback_from_Rear = self.get_var("Setback from Rear")
        Z_Loc = self.get_prompt("Top Rod Location From Top").get_var('Z_Loc')
        Top_Rod_Location = self.get_prompt("Top Rod Location").get_var('Top_Rod_Location')
        Turn_Off_Hangers = self.get_prompt("Turn Off Hangers").get_var('Turn_Off_Hangers')
        Hanging_Rod_Width_Deduction = self.get_prompt(
            "Hanging Rod Width Deduction").get_var('Hanging_Rod_Width_Deduction')
        Hanging_Rod_Setback = self.get_prompt("Hanging Rod Setback").get_var('Hanging_Rod_Setback')
        Add_Rod_Setback = self.get_prompt("Add Rod Setback").get_var('Add_Rod_Setback')
        Add_Deep_Rod_Setback = self.get_prompt("Add Deep Rod Setback").get_var('Add_Deep_Rod_Setback')
        Default_Deep_Setback = self.get_prompt("Default Deep Setback").get_var('Default_Deep_Setback')
        Extra_Deep_Pard = self.get_prompt("Extra Deep Pard").get_var('Extra_Deep_Pard')

        assembly.loc_x('Hanging_Rod_Width_Deduction/2', [Hanging_Rod_Width_Deduction])
        assembly.dim_x('Width-Hanging_Rod_Width_Deduction', [Width, Hanging_Rod_Width_Deduction])
        assembly.dim_y(value=sn_unit.inch(.5))
        assembly.dim_z(value=sn_unit.inch(-1))

        if location == 'TOP':
            Add_Top_Rod = self.get_prompt("Add Top Rod").get_var('Add_Top_Rod')
            assembly.loc_z('Height-Z_Loc', [Height, Z_Loc])
            assembly.loc_y('IF(Depth>=Extra_Deep_Pard,Hanging_Rod_Setback+Add_Deep_Rod_Setback,Hanging_Rod_Setback+Add_Rod_Setback)',
                           [Hanging_Rod_Setback, Add_Rod_Setback, Extra_Deep_Pard, Depth, Default_Deep_Setback, Add_Deep_Rod_Setback])
            if is_hanger:
                hide = assembly.get_prompt("Hide")
                hide.set_formula(
                    'IF(Turn_Off_Hangers,True,IF(Add_Top_Rod,False,True)) or Hide',
                    [Add_Top_Rod, Turn_Off_Hangers,self.hide_var])
            else:
                hide = assembly.get_prompt("Hide")
                hide.set_formula('IF(Add_Top_Rod,False,True) or Hide', [Add_Top_Rod,self.hide_var])
        if location == 'MID':
            Add_Middle_Rod = self.get_prompt("Add Middle Rod").get_var('Add_Middle_Rod')
            assembly.loc_z('Height-Top_Rod_Location-Z_Loc+0.032004',
                           [Height, Top_Rod_Location, Z_Loc])
            assembly.loc_y('IF(Depth>=Extra_Deep_Pard,Hanging_Rod_Setback+Add_Deep_Rod_Setback,Hanging_Rod_Setback+Add_Rod_Setback)',
                           [Hanging_Rod_Setback, Add_Rod_Setback, Extra_Deep_Pard, Depth, Default_Deep_Setback, Add_Deep_Rod_Setback])
            if is_hanger:
                hide = assembly.get_prompt("Hide")
                hide.set_formula(
                    'IF(Turn_Off_Hangers,True,IF(Add_Middle_Rod,False,True)) or Hide',
                    [Add_Middle_Rod, Turn_Off_Hangers,self.hide_var])
            else:
                hide = assembly.get_prompt("Hide")
                hide.set_formula('IF(Add_Middle_Rod,False,True) or Hide', [Add_Middle_Rod,self.hide_var])
        if location == 'BOT':
            Add_Bottom_Rod = self.get_prompt("Add Bottom Rod").get_var('Add_Bottom_Rod')
            Bottom_Rod_Location = self.get_prompt("Bottom Rod Location").get_var('Bottom_Rod_Location')
            assembly.loc_z('Height-Bottom_Rod_Location-Z_Loc+0.032004', [Height, Bottom_Rod_Location, Z_Loc])
            assembly.loc_y(
                'IF(Depth>=Extra_Deep_Pard,Hanging_Rod_Setback+Add_Deep_Rod_Setback,Hanging_Rod_Setback+Add_Rod_Setback)',
                [Hanging_Rod_Setback, Add_Rod_Setback, Extra_Deep_Pard, Depth, Default_Deep_Setback, Add_Deep_Rod_Setback])
            if is_hanger:
                hide = assembly.get_prompt("Hide")
                hide.set_formula(
                    'IF(Turn_Off_Hangers,True,IF(Add_Bottom_Rod,False,True)) or Hide',
                    [Add_Bottom_Rod, Turn_Off_Hangers,self.hide_var])
            else:
                hide = assembly.get_prompt("Hide")
                hide.set_formula('IF(Add_Bottom_Rod,False,True) or Hide', [Add_Bottom_Rod,self.hide_var])

        return assembly

    def add_shelves(self):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Height = self.obj_z.snap.get_var('location.z', 'Height')

        Shelf_Thickness = self.get_prompt("Shelf Thickness").get_var('Shelf_Thickness')
        Add_Shelves_In_Top_Section = self.get_prompt("Add Shelves In Top Section").get_var('Add_Shelves_In_Top_Section')
        Add_Shelves_In_Middle_Section = self.get_prompt("Add Shelves In Middle Section").get_var('Add_Shelves_In_Middle_Section')
        Add_Shelves_In_Bottom_Section = self.get_prompt("Add Shelves In Bottom Section").get_var('Add_Shelves_In_Bottom_Section')
        Top_Shelf_Quantity = self.get_prompt("Top Shelf Quantity").get_var('Top_Shelf_Quantity')
        Middle_Shelf_Quantity = self.get_prompt("Middle Shelf Quantity").get_var('Middle_Shelf_Quantity')
        Bottom_Shelf_Quantity = self.get_prompt("Bottom Shelf Quantity").get_var('Bottom_Shelf_Quantity')
        Top_Rod_Location = self.get_prompt("Top Rod Location").get_var('Top_Rod_Location')
        Bottom_Rod_Location = self.get_prompt("Bottom Rod Location").get_var('Bottom_Rod_Location')
        Bottom_Shelves_Location = self.get_prompt("Bottom Shelves Location").get_var('Bottom_Shelves_Location')
        Shelf_Clip_Gap = self.get_prompt("Shelf Clip Gap").get_var('Shelf_Clip_Gap')
        Shelf_Setback = self.get_prompt("Shelf Setback").get_var('Shelf_Setback')
        Is_Hang_Single = self.get_prompt("Is Hang Single").get_var('Is_Hang_Single')
        SBS = self.get_prompt("Shelf Backing Setback").get_var('SBS')
        ATSS = self.get_prompt("Add Top Shelf Setback").get_var('ATSS')
        AMSS = self.get_prompt("Add Middle Shelf Setback").get_var('AMSS')
        ABSS = self.get_prompt("Add Bottom Shelf Setback").get_var('ABSS')
        # IHD = self.get_prompt("Is Hang Double").get_var('IHD')
        # DDS = self.get_prompt("Default Deep Setback").get_var('DDS')
        # EDP = self.get_prompt("Extra Deep Pard").get_var('EDP')

        # TOP SECTION
        top_opening_height = "(Top_Rod_Location-Shelf_Thickness-0.064008)"
        top_opening_z_loc = "(Height-Top_Rod_Location+Shelf_Thickness+0.064008)"
        top_opening_thickness_deduction = "(Shelf_Thickness*Top_Shelf_Quantity)"
        top_opening_qty = "(Top_Shelf_Quantity+1)"

        adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
        Adj_Shelf_Setback = adj_shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
        Locked_Shelf_Setback = adj_shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')

        adj_shelf.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [
                        Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.loc_y('Depth-SBS', [Depth, SBS])
        adj_shelf.loc_z(top_opening_z_loc + "+(" + top_opening_height + "-" + top_opening_thickness_deduction + ")/" + top_opening_qty,
                        [Top_Rod_Location, Shelf_Thickness, Height, Top_Shelf_Quantity])
        adj_shelf.dim_x('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                        [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.dim_y('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ATSS+SBS',
                        [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, ATSS, SBS])
        adj_shelf.dim_z('Shelf_Thickness', [Shelf_Thickness])

        hide = adj_shelf.get_prompt('Hide')
        hide.set_formula('IF(AND(Top_Shelf_Quantity>0,Add_Shelves_In_Top_Section),False,True) or Hide', 
                         [self.hide_var, Top_Shelf_Quantity, Add_Shelves_In_Top_Section])
        z_qty = adj_shelf.get_prompt('Z Quantity')
        z_qty.set_formula('Top_Shelf_Quantity', [Top_Shelf_Quantity])
        z_offset = adj_shelf.get_prompt('Z Offset')
        z_offset.set_formula('((' + top_opening_height + '-' + top_opening_thickness_deduction + ')/' + top_opening_qty + ')+Shelf_Thickness',
                         [Top_Rod_Location, Shelf_Thickness, Top_Shelf_Quantity])

        # MIDDLE SECTION
        mid_opening_height = "(Bottom_Rod_Location-Top_Rod_Location-Shelf_Thickness-0.064008)"
        mid_opening_z_loc = "(Height-Bottom_Rod_Location+Shelf_Thickness+0.064008)"
        mid_opening_thickness_deduction = "(Shelf_Thickness*Middle_Shelf_Quantity)"
        mid_opening_qty = "(Middle_Shelf_Quantity+1)"
        adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
        Adj_Shelf_Setback = adj_shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
        Locked_Shelf_Setback = adj_shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')

        adj_shelf.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [
                        Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.loc_y('Depth-SBS', [Depth, SBS])
        adj_shelf.loc_z(mid_opening_z_loc + "+(" + mid_opening_height + "-" + mid_opening_thickness_deduction + ")/" + mid_opening_qty,
                        [Bottom_Rod_Location, Top_Rod_Location, Shelf_Thickness, Height, Middle_Shelf_Quantity])
        adj_shelf.dim_x('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                        [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.dim_y('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+AMSS+SBS',
                        [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, AMSS, SBS])
        adj_shelf.dim_z('Shelf_Thickness', [Shelf_Thickness])

        hide = adj_shelf.get_prompt('Hide')
        hide.set_formula('IF(Is_Hang_Single,True,IF(AND(Middle_Shelf_Quantity>0,Add_Shelves_In_Middle_Section),False,True)) or Hide', 
                         [self.hide_var, Middle_Shelf_Quantity, Add_Shelves_In_Middle_Section, Is_Hang_Single])
        z_qty = adj_shelf.get_prompt('Z Quantity')
        z_qty.set_formula('Middle_Shelf_Quantity', [Middle_Shelf_Quantity])
        z_offset = adj_shelf.get_prompt('Z Offset')
        z_offset.set_formula('((' + mid_opening_height + '-' + mid_opening_thickness_deduction + ')/' + mid_opening_qty + ')+Shelf_Thickness',
                            [Top_Rod_Location, Bottom_Rod_Location, Shelf_Thickness, Middle_Shelf_Quantity, Height])

        # Short Hang Mid
        short_mid_opening_height = "(Bottom_Rod_Location-Shelf_Thickness)"
        short_mid_opening_z_loc = "(Height-Bottom_Rod_Location+Shelf_Thickness+0.064008)"
        short_mid_opening_thickness_deduction = "(Shelf_Thickness*Middle_Shelf_Quantity)"
        short_mid_opening_qty = "(Middle_Shelf_Quantity+1)"
        short_adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = short_adj_shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
        Adj_Shelf_Setback = short_adj_shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
        Locked_Shelf_Setback = short_adj_shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
        Adj_Shelf_Clip_Gap = short_adj_shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')

        short_adj_shelf.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [
                              Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        short_adj_shelf.loc_y('Depth-SBS', [Depth, SBS])
        short_adj_shelf.loc_z(short_mid_opening_z_loc + "+(" + short_mid_opening_height + "-" + short_mid_opening_thickness_deduction + ")/" + short_mid_opening_qty,
                              [Bottom_Rod_Location, Top_Rod_Location, Shelf_Thickness, Height, Middle_Shelf_Quantity])
        short_adj_shelf.dim_x('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                              [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        short_adj_shelf.dim_y('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+AMSS+SBS', [
                              Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, AMSS, SBS])
        short_adj_shelf.dim_z('Shelf_Thickness', [Shelf_Thickness])

        hide = short_adj_shelf.get_prompt('Hide')
        hide.set_formula('IF(Is_Hang_Single, IF(AND(Middle_Shelf_Quantity>0,Add_Shelves_In_Middle_Section),False,True),True) or Hide', 
                        [self.hide_var, Middle_Shelf_Quantity, Add_Shelves_In_Middle_Section, Is_Hang_Single])
        z_qty = short_adj_shelf.get_prompt('Z Quantity')
        z_qty.set_formula('Middle_Shelf_Quantity', [Middle_Shelf_Quantity])
        z_offset = short_adj_shelf.get_prompt('Z Offset')
        z_offset.set_formula('((' + short_mid_opening_height + '-' + short_mid_opening_thickness_deduction + ')/' + short_mid_opening_qty + ')+Shelf_Thickness',
                            [Top_Rod_Location, Bottom_Rod_Location, Shelf_Thickness, Middle_Shelf_Quantity, Height])

        # BOTTOM SECTION
        bottom_opening_height = "(Bottom_Shelves_Location-Bottom_Rod_Location-Shelf_Thickness)"
        bottom_opening_z_loc = "(Height-Bottom_Shelves_Location)"
        bottom_opening_thickness_deduction = "(Shelf_Thickness*Bottom_Shelf_Quantity)"
        bottom_opening_qty = "(Bottom_Shelf_Quantity+1)"
        adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
        Adj_Shelf_Setback = adj_shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
        Locked_Shelf_Setback = adj_shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')

        adj_shelf.loc_x('IF(Is_Locked_Shelf,0,Shelf_Clip_Gap)', [Is_Locked_Shelf, Shelf_Clip_Gap])
        adj_shelf.loc_y('Depth-SBS', [Depth, SBS])
        adj_shelf.loc_z(bottom_opening_z_loc + "+(" + bottom_opening_height + "-" + bottom_opening_thickness_deduction + ")/" + bottom_opening_qty,
                        [Bottom_Shelves_Location,Bottom_Rod_Location,Shelf_Thickness,Height,Bottom_Shelf_Quantity])
        adj_shelf.dim_x('Width-IF(Is_Locked_Shelf,0,Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Shelf_Clip_Gap])
        adj_shelf.dim_y('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABSS+SBS',
                        [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, ABSS, SBS])
        adj_shelf.dim_z('Shelf_Thickness',[Shelf_Thickness])

        hide = adj_shelf.get_prompt('Hide')
        hide.set_formula('IF(AND(Bottom_Shelf_Quantity>0,Add_Shelves_In_Bottom_Section),False,True) or Hide', 
                         [self.hide_var, Bottom_Shelf_Quantity, Add_Shelves_In_Bottom_Section])
        z_qty = adj_shelf.get_prompt('Z Quantity')
        z_qty.set_formula('Bottom_Shelf_Quantity',[Bottom_Shelf_Quantity])
        z_offset = adj_shelf.get_prompt('Z Offset')
        z_offset.set_formula('((' + bottom_opening_height + '-' + bottom_opening_thickness_deduction + ')/' + bottom_opening_qty + ')+Shelf_Thickness',
                            [Bottom_Shelves_Location,Bottom_Rod_Location,Shelf_Thickness,Bottom_Shelf_Quantity])

        #Below Shelves Section
        Add_Below_Shelves = self.get_prompt("Add Below Shelves").get_var('Add_Below_Shelves')
        Below_Shelf_Quantity = self.get_prompt("Below Shelf Quantity").get_var('Below_Shelf_Quantity')
        previous_splitter = None

        for i in range(1,9):

            Shelf_Height = self.get_prompt("Below Shelf " + str(i) + " Height").get_var('Shelf_Height')
            shelf_empty = self.add_empty("Shelf Empty")
            if previous_splitter:
                # we want to location at the bottom of the object
                prev_shelf_z_loc = previous_splitter.obj_bp.snap.get_var('location.z', 'prev_shelf_z_loc')
                shelf_empty.snap.loc_z('prev_shelf_z_loc-Shelf_Height', [prev_shelf_z_loc, Shelf_Height])
            else:
                shelf_empty.snap.loc_z('Height-Bottom_Rod_Location-Shelf_Height',
                                  [Shelf_Height, Height, Bottom_Rod_Location])

            sh_z_loc = shelf_empty.snap.get_var('location.z', 'sh_z_loc')

            splitter = common_parts.add_shelf(self)

            Is_Locked_Shelf = splitter.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
            Adj_Shelf_Setback = splitter.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
            Locked_Shelf_Setback = splitter.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
            Adj_Shelf_Clip_Gap = splitter.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')
            Shelf_Setback = self.get_prompt("Below Shelf " + str(i) + " Setback").get_var('Shelf_Setback')

            splitter.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
            splitter.loc_y('Depth-SBS', [Depth, SBS])
            splitter.loc_z('sh_z_loc',[sh_z_loc])
            splitter.dim_x('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.dim_y('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Shelf_Setback+SBS',
                           [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, Shelf_Setback, SBS])
            splitter.dim_z('Shelf_Thickness',[Shelf_Thickness])
            hide = splitter.get_prompt('Hide')
            hide.set_formula('IF(Add_Below_Shelves,IF(Below_Shelf_Quantity+1>'+str(i)+',False,True),True)',[Add_Below_Shelves,Below_Shelf_Quantity])

            previous_splitter = splitter

    def add_shelves_above_rod(self):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Top_Rod_Location = self.get_prompt("Top Rod Location").get_var('Top_Rod_Location')
        Shelf_Thickness = self.get_prompt("Shelf Thickness").get_var('Shelf_Thickness')
        Bottom_Rod_Location = self.get_prompt("Bottom Rod Location").get_var('Bottom_Rod_Location')
        Add_Top_Shelf = self.get_prompt("Add Top Shelf").get_var('Add_Top_Shelf')
        Add_Bottom_Shelf = self.get_prompt("Add Bottom Shelf").get_var('Add_Bottom_Shelf')
        SBS = self.get_prompt("Shelf Backing Setback").get_var('SBS')

        IHD = self.get_prompt("Is Hang Double").get_var('IHD')
        DDS = self.get_prompt("Default Deep Setback").get_var('DDS')
        EDP = self.get_prompt("Extra Deep Pard").get_var('EDP')
        ATSS = self.get_prompt("Add Top Shelf Setback").get_var('ATSS')
        ABSS = self.get_prompt("Add Bottom Shelf Setback").get_var('ABSS')
        ABDSS = self.get_prompt("Add Bottom Deep Shelf Setback").get_var('ABDSS')

        shelf = common_parts.add_shelf(self)
        Is_Locked_Shelf = shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
        Adj_Shelf_Setback = shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
        Locked_Shelf_Setback = shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
        Adj_Shelf_Clip_Gap = shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')

        shelf.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',
                    [Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        shelf.loc_y('Depth-SBS', [Depth, SBS])
        shelf.loc_z('Height-Top_Rod_Location+0.064008',
                    [Height, Top_Rod_Location])
        shelf.dim_x('Width-IF(Is_Locked_Shelf,0,(Adj_Shelf_Clip_Gap*2))',
                    [Width, Adj_Shelf_Clip_Gap, Is_Locked_Shelf])

        shelf.dim_y('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ATSS+SBS',
                    [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, ATSS, SBS])
        shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        hide = shelf.get_prompt('Hide')
        hide.set_formula('IF(Add_Top_Shelf,False,True) or Hide', [Add_Top_Shelf,self.hide_var])

        shelf = common_parts.add_shelf(self)
        Is_Locked_Shelf = shelf.get_prompt('Is Locked Shelf').get_var('Is_Locked_Shelf')
        Adj_Shelf_Setback = shelf.get_prompt('Adj Shelf Setback').get_var('Adj_Shelf_Setback')
        Locked_Shelf_Setback = shelf.get_prompt('Locked Shelf Setback').get_var('Locked_Shelf_Setback')
        Adj_Shelf_Clip_Gap = shelf.get_prompt('Adj Shelf Clip Gap').get_var('Adj_Shelf_Clip_Gap')

        shelf.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',
                    [Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        shelf.loc_y('Depth-SBS', [Depth, SBS])
        shelf.loc_z('Height-Bottom_Rod_Location+0.064008',
                    [Height, Bottom_Rod_Location])
        shelf.dim_x('Width-IF(Is_Locked_Shelf,0,(Adj_Shelf_Clip_Gap*2))',
                    [Width, Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        shelf.dim_y('IF(IHD,IF(Depth>=EDP,-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABDSS,-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABSS),-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABSS)+SBS',
                    [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, ABSS, IHD, DDS, EDP, ABDSS, SBS])
        shelf.dim_z('Shelf_Thickness', [Shelf_Thickness])
        hide = shelf.get_prompt('Hide')
        hide.set_formula('IF(Add_Bottom_Shelf,False,True) or Hide', [Add_Bottom_Shelf,self.hide_var])

    def update(self):
        self.set_prompts()
        self.obj_bp["ID_DROP"] = self.drop_id
        self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.obj_bp["IS_BP_ROD_AND_SHELF"] = True
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.obj_bp.snap.placement_type = self.placement_type
        super().update()

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        props = bpy.context.scene.sn_closets.closet_defaults

        self.add_prompt("Add Top Rod", 'CHECKBOX', False)
        self.add_prompt("Add Middle Rod", 'CHECKBOX', True)
        self.add_prompt("Add Bottom Rod", 'CHECKBOX', False)

        self.add_prompt("Add Top Shelf", 'CHECKBOX', True)
        self.add_prompt("Add Bottom Shelf", 'CHECKBOX', False)

        self.add_prompt("Top Rod Location", 'DISTANCE', sn_unit.millimeter(428.95))
        self.add_prompt("Bottom Rod Location", 'DISTANCE', sn_unit.millimeter(1164.95))
        self.add_prompt("Bottom Shelves Location", 'DISTANCE', sn_unit.millimeter(1164.95))

        self.add_prompt("Add Shelves In Top Section", 'CHECKBOX', False)
        self.add_prompt("Add Shelves In Middle Section", 'CHECKBOX', False)
        self.add_prompt("Add Shelves In Bottom Section", 'CHECKBOX', False)

        self.add_prompt("Top Shelf Quantity", 'QUANTITY', 1)
        self.add_prompt("Middle Shelf Quantity", 'QUANTITY', 1)
        self.add_prompt("Bottom Shelf Quantity", 'QUANTITY', 1)

        self.add_prompt("Add Below Shelves", 'CHECKBOX', False)
        self.add_prompt("Below Shelf Quantity", 'QUANTITY', 1)

        for i in range(1, 9):
            self.add_prompt("Below Shelf " + str(i) + " Height", 'DISTANCE', sn_unit.millimeter(91.95))
            self.add_prompt("Below Shelf " + str(i) + " Setback", 'DISTANCE', 0)

        self.add_prompt("Below Shelf Stack Height", 'DISTANCE', 0)

        self.add_prompt("Hanging Rod Width Deduction", 'DISTANCE', sn_unit.inch(0))

        self.add_prompt("Shelf Clip Gap", 'DISTANCE', sn_unit.inch(0))

        self.add_prompt("Shelf Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Setback from Rear", 'CHECKBOX', False)
        self.add_prompt("Top Rod Location From Top", 'DISTANCE', sn_unit.inch(1.26))
        self.add_prompt("Turn Off Hangers", 'CHECKBOX', props.hide_hangers)

        self.add_prompt("Shelf Setback", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Hanging Rod Setback", 'DISTANCE', sn_unit.inch(1.69291))
        self.add_prompt("Add Rod Setback", 'DISTANCE', sn_unit.inch(0))

        self.add_prompt("Is Hang Single", 'CHECKBOX', False)
        self.add_prompt("Is Hang Double", 'CHECKBOX', False)

        self.add_prompt("Add Top Shelf Setback", 'DISTANCE', 0)
        self.add_prompt("Add Middle Shelf Setback", 'DISTANCE', 0)
        self.add_prompt("Add Bottom Shelf Setback", 'DISTANCE', 0)
        self.add_prompt("Add Bottom Deep Shelf Setback", 'DISTANCE', 0)
        self.add_prompt("Default Deep Setback", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Extra Deep Pard", 'DISTANCE', sn_unit.inch(16))
        self.add_prompt("Add Deep Rod Setback", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Shelf Backing Setback", 'DISTANCE', 0)

        self.add_shelves_above_rod()

        opts = bpy.context.scene.sn_closets.closet_options

        if "Oval" in opts.rods_name:
            self.add_rod(common_parts.add_oval_hanging_rod(self), location="TOP")
            self.add_rod(common_parts.add_oval_hanging_rod(self), location="MID")
            self.add_rod(common_parts.add_oval_hanging_rod(self), location="BOT")

        else:
            self.add_rod(common_parts.add_round_hanging_rod(self), location="TOP")
            self.add_rod(common_parts.add_round_hanging_rod(self), location="MID")
            self.add_rod(common_parts.add_round_hanging_rod(self), location="BOT")

        self.add_rod(common_parts.add_hangers(self), location="TOP", is_hanger=True)
        self.add_rod(common_parts.add_hangers(self), location="MID", is_hanger=True)
        self.add_rod(common_parts.add_hangers(self), location="BOT", is_hanger=True)

        self.add_shelves()
        self.update()


class Shelves_Only(sn_types.Assembly):

    type_assembly = "INSERT"
    id_prompt = "sn_closets.shelves_only"
    placement_type = "INTERIOR"
    show_in_library = True
    category_name = "Closet Products - Basic"
    mirror_y = False

    def add_adj_prompts(self):
        self.add_prompt("Shelf Qty", 'QUANTITY', 5)

    def add_shelves(self):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Shelf_Qty = self.get_prompt("Shelf Qty").get_var()
        Shelf_Thickness = self.get_prompt("Shelf Thickness").get_var()

        adj_shelf = common_parts.add_shelf(self)
        Is_Locked_Shelf = adj_shelf.get_prompt('Is Locked Shelf').get_var()
        Adj_Shelf_Setback = adj_shelf.get_prompt('Adj Shelf Setback').get_var()
        Locked_Shelf_Setback = adj_shelf.get_prompt('Locked Shelf Setback').get_var()
        Adj_Shelf_Clip_Gap = adj_shelf.get_prompt('Adj Shelf Clip Gap').get_var()

        adj_shelf.loc_x('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        adj_shelf.loc_y('Depth', [Depth])
        adj_shelf.loc_z('((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))',
                        [Height, Shelf_Thickness, Shelf_Qty])
        adj_shelf.dim_x('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                        [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.dim_y('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',
                        [Depth, Is_Locked_Shelf, Locked_Shelf_Setback, Adj_Shelf_Setback])
        adj_shelf.dim_z('Shelf_Thickness', [Shelf_Thickness])
        adj_shelf.get_prompt('Hide').set_formula('IF(Shelf_Qty==0,True,False) or Hide', [Shelf_Qty,self.hide_var])
        adj_shelf.get_prompt('Z Quantity').set_formula('Shelf_Qty', [Shelf_Qty])
        adj_shelf.get_prompt('Z Offset').set_formula(
            '((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness',
            [Height, Shelf_Thickness, Shelf_Qty])

    def update(self):
        self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.obj_bp.snap.placement_type = self.placement_type
        super().update()

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        common_prompts.add_thickness_prompts(self)
        self.add_adj_prompts()
        self.add_shelves()
        self.draw_as_hidden_line()
        self.update()


class Glass_Shelves(sn_types.Assembly):

    type_assembly = "INSERT"
    id_prompt = "sn_closets.glass_shelves"
    placement_type = "INTERIOR"
    show_in_library = True
    category_name = "Closet Products - Basic"
    mirror_y = False
    shelf_thickness_ppt_obj = None

    def add_adj_prompts(self):
        self.add_prompt("Shelf Qty", 'QUANTITY', 5)

    def add_glass_thickness_prompts(self):
        glass_thickness = self.add_prompt("Glass Shelf Thickness", 'COMBOBOX', 0, ['1/4"', '3/8"', '1/2"'])
        glass_thickness.combobox_columns = 3
        ST = self.get_prompt("Glass Shelf Thickness").get_var("ST")

        self.shelf_thickness_ppt_obj = self.add_empty("OBJ_PROMPTS_Shelf_Thickness")
        self.shelf_thickness_ppt_obj.empty_display_size = 0.01
        shelf_thickness_ppt = self.shelf_thickness_ppt_obj.snap.add_prompt('DISTANCE', "Shelf Thickness")
        shelf_thickness_ppt.set_value(sn_unit.inch(0.75))
        self.shelf_thickness_ppt_obj.snap.get_prompt('Shelf Thickness').set_formula(
            'IF(ST==0,INCH(0.25),IF(ST==1,INCH(0.375),INCH(0.5)))', [ST])

    def glass_shelves(self):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Shelf_Qty = self.get_prompt("Shelf Qty").get_var()
        Shelf_Thickness = self.shelf_thickness_ppt_obj.snap.get_prompt("Shelf Thickness").get_var()

        adj_shelf = common_parts.add_glass_shelf(self)
        adj_shelf.loc_y('Depth', [Depth])
        adj_shelf.loc_z('((Height-((Shelf_Thickness)*Shelf_Qty))/(Shelf_Qty+1))',
                        [Height, Shelf_Thickness, Shelf_Qty])
        adj_shelf.dim_x('Width', [Width])
        adj_shelf.dim_y('-Depth+0.00635', [Depth])
        adj_shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        adj_shelf.get_prompt('Hide').set_formula('IF(Shelf_Qty==0,True,False) or Hide', [Shelf_Qty,self.hide_var])
        adj_shelf.get_prompt('Z Quantity').set_formula('Shelf_Qty', [Shelf_Qty])
        adj_shelf.get_prompt('Z Offset').set_formula(
            '((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness',
            [Height, Shelf_Thickness, Shelf_Qty])

    def update(self):
        self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.obj_bp.snap.placement_type = self.placement_type
        super().update()

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.add_glass_thickness_prompts()
        self.add_adj_prompts()
        self.glass_shelves()
        self.draw_as_hidden_line()
        self.update()


class PROMPTS_Hanging_Rod_With_Shelves_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.hanging_rod_with_shelves_prompts"
    bl_label = "Hanging Rod Prompts"
    bl_description = "This shows all of the available hanging rod options"
    bl_options = {'UNDO'}

    object_name: bpy.props.StringProperty(name="Object Name")

    top_shelf_quantity: bpy.props.IntProperty(
        name="Top Shelf Quantity", min=1, max=10)

    middle_shelf_quantity: bpy.props.IntProperty(
        name="Middle Shelf Quantity", min=1, max=10)

    bottom_shelf_quantity: bpy.props.IntProperty(
        name="Bottom Shelf Quantity", min=1, max=10)

    top_rod_location: bpy.props.EnumProperty(name="Top Rod Location",
                                              items=common_lists.ROD_HEIGHTS)

    bottom_rod_location: bpy.props.EnumProperty(name="Bottom Rod Location",
                                                 items=common_lists.ROD_HEIGHTS)

    bottom_shelves_location: bpy.props.EnumProperty(name="Bottom Shelves Location",
                                               items=common_lists.ROD_HEIGHTS)  

    below_shelf_quantity: bpy.props.EnumProperty(name="Below Shelf Quantity",
                                   items=[('1',"1",'1'),
                                          ('2',"2",'2'),
                                          ('3',"3",'3'),
                                          ('4',"4",'4'),
                                          ('5',"5",'5'),
                                          ('6',"6",'6'),
                                          ('7',"7",'7'),
                                          ('8',"8",'8')],
                                   default = '3')

    Below_Shelf_1_Height: bpy.props.EnumProperty(name="Below Shelf 1 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_2_Height: bpy.props.EnumProperty(name="Below Shelf 2 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_3_Height: bpy.props.EnumProperty(name="Below Shelf 3 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_4_Height: bpy.props.EnumProperty(name="Below Shelf 4 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_5_Height: bpy.props.EnumProperty(name="Below Shelf 5 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_6_Height: bpy.props.EnumProperty(name="Below Shelf 6 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_7_Height: bpy.props.EnumProperty(name="Below Shelf 7 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_8_Height: bpy.props.EnumProperty(name="Below Shelf 8 Height",
                                    items=common_lists.OPENING_HEIGHTS)  

    shelf_quantity_prompt = None    
    
    assembly = None

    def check(self, context):
        self.set_prompts_from_properties()
        self.insert.obj_bp.location = self.insert.obj_bp.location  # Redraw Viewport
        return True

    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''
        top_rod_location = self.insert.get_prompt("Top Rod Location")
        top_shelf_quantity = self.insert.get_prompt("Top Shelf Quantity")
        bottom_rod_location = self.insert.get_prompt("Bottom Rod Location")
        middle_shelf_quantity = self.insert.get_prompt(
            "Middle Shelf Quantity")
        bottom_shelves_location = self.insert.get_prompt(
            "Bottom Shelves Location")
        bottom_shelf_quantity = self.insert.get_prompt(
            "Bottom Shelf Quantity")
        if top_shelf_quantity:
            top_shelf_quantity.set_value(self.top_shelf_quantity)
        if middle_shelf_quantity:
            middle_shelf_quantity.set_value(self.middle_shelf_quantity)
        if bottom_shelf_quantity:
            bottom_shelf_quantity.set_value(self.bottom_shelf_quantity)
        if top_rod_location:
            top_rod_location.set_value(sn_unit.inch(
                float(self.top_rod_location) / 25.4))
        if bottom_rod_location:
            bottom_rod_location.set_value(sn_unit.inch(
                float(self.bottom_rod_location) / 25.4))
        if bottom_shelves_location:
            bottom_shelves_location.set_value(sn_unit.inch(
                float(self.bottom_shelves_location) / 25.4))

        self.shelf_quantity_prompt.set_value(int(self.below_shelf_quantity))

        for i in range(1,9):
            shelf = self.insert.get_prompt("Below Shelf " + str(i) + " Height")
            if shelf:
                exec("shelf.set_value(sn_unit.inch(float(self.Below_Shelf_" + str(i) + "_Height) / 25.4))")  

    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        top_rod_location = self.insert.get_prompt("Top Rod Location")
        if top_rod_location:
            value = round(top_rod_location.get_value() * 1000, 2)
            for index, height in enumerate(common_lists.ROD_HEIGHTS):
                if not value >= float(height[0]):
                    self.top_rod_location = common_lists.ROD_HEIGHTS[index - 1][0]
                    break

        bottom_rod_location = self.insert.get_prompt("Bottom Rod Location")
        if bottom_rod_location:
            value = round(bottom_rod_location.get_value() * 1000, 2)
            for index, height in enumerate(common_lists.ROD_HEIGHTS):
                if not value >= float(height[0]):
                    self.bottom_rod_location = common_lists.ROD_HEIGHTS[index - 1][0]
                    break

        bottom_shelves_location = self.insert.get_prompt(
            "Bottom Shelves Location")
        if bottom_shelves_location:
            value = round(bottom_shelves_location.get_value() * 1000, 2)
            for index, height in enumerate(common_lists.ROD_HEIGHTS):
                if not value >= float(height[0]):
                    self.bottom_shelves_location = common_lists.ROD_HEIGHTS[index - 1][0]
                    break

        top_shelf_quantity = self.insert.get_prompt("Top Shelf Quantity")
        middle_shelf_quantity = self.insert.get_prompt(
            "Middle Shelf Quantity")
        bottom_shelf_quantity = self.insert.get_prompt(
            "Bottom Shelf Quantity")

        if top_shelf_quantity:
            self.top_shelf_quantity = top_shelf_quantity.get_value()
        if middle_shelf_quantity:
            self.middle_shelf_quantity = middle_shelf_quantity.get_value()
        if bottom_shelf_quantity:
            self.bottom_shelf_quantity = bottom_shelf_quantity.get_value()    

        self.shelf_quantity_prompt = self.insert.get_prompt("Below Shelf Quantity")
        if self.shelf_quantity_prompt:
            self.below_shelf_quantity = str(self.shelf_quantity_prompt.get_value())

        for i in range(1,9):
            shelf = self.insert.get_prompt("Below Shelf " + str(i) + " Height")
            if shelf:
                value = round(shelf.get_value() * 1000,3)
                for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        exec("self.Below_Shelf_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[index - 1][0]")
                        break    
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        self.insert = self.get_insert()
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        if self.insert.obj_bp:
            if self.insert.obj_bp.name in context.scene.objects:
                add_top_rod = self.insert.get_prompt("Add Top Rod")
                add_middle_rod = self.insert.get_prompt("Add Middle Rod")
                add_bottom_rod = self.insert.get_prompt("Add Bottom Rod")
                add_shelves_in_top_section = self.insert.get_prompt(
                    "Add Shelves In Top Section")
                add_shelves_in_middle_section = self.insert.get_prompt(
                    "Add Shelves In Middle Section")
                add_shelves_in_bottom_section = self.insert.get_prompt(
                    "Add Shelves In Bottom Section")
                add_top_shelf = self.insert.get_prompt("Add Top Shelf")
                add_bottom_shelf = self.insert.get_prompt("Add Bottom Shelf")
                rod_setback = self.insert.get_prompt("Hanging Rod Setback")
                Add_Rod_Setback = self.insert.get_prompt("Add Rod Setback")
                shelf_setback = self.insert.get_prompt("Shelf Setback")
                is_hang_single = self.insert.get_prompt("Is Hang Single")

                add_top_shelf_setback = self.insert.get_prompt(
                    "Add Top Shelf Setback")
                add_middle_shelf_setback = self.insert.get_prompt(
                    "Add Middle Shelf Setback")
                add_bottom_shelf_setback = self.insert.get_prompt(
                    "Add Bottom Shelf Setback")
                add_bottom_deep_shelf_setback = self.insert.get_prompt(
                    "Add Bottom Deep Shelf Setback")
                Add_Deep_Rod_Setback = self.insert.get_prompt(
                    "Add Deep Rod Setback")
                is_hang_double = self.insert.get_prompt("Is Hang Double")
                extra_deep_pard = self.insert.get_prompt("Extra Deep Pard")

                if add_top_rod and add_middle_rod and add_bottom_rod:
                    column = layout.column(align=True)

                    # Top
                    box = column.box()
                    box.label(text="Top Opening:")

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    row.prop(add_top_rod, "checkbox_value", text="Rod at Top")

                    if is_hang_single and not is_hang_single.get_value():

                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        row.prop(add_middle_rod, "checkbox_value", text="Add Rod")
                        row.prop(self, 'top_rod_location', text="")
                        row.label(text="", icon='TRIA_DOWN')

                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        row.prop(add_top_shelf, "checkbox_value", text="Add Dust Shelf")

                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        row.prop(add_shelves_in_top_section, "checkbox_value", text="Add Shelves")
                        if add_shelves_in_top_section.get_value():
                            row.prop(self, "top_shelf_quantity", text="Quantity")

                    # Mid
                    box = column.box()
                    box.label(text="Bottom Opening:")

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    row.prop(add_bottom_rod, "checkbox_value", text="Add Rod")
                    row.prop(self, 'bottom_rod_location', text="")
                    row.label(text="", icon='TRIA_UP')

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    row.prop(add_bottom_shelf, "checkbox_value", text="Add Dust Shelf")

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    row.prop(add_shelves_in_middle_section, "checkbox_value", text="Add Shelves")
                    if add_shelves_in_middle_section.get_value():
                        row.prop(self, "middle_shelf_quantity",
                                 text="Quantity")

                    box = column.box()
                    box.label(text="Setbacks:")

                    if(extra_deep_pard and self.insert.obj_y.location.y >= extra_deep_pard.get_value()):
                            row = box.row()
                            row.label(text="", icon='BLANK1')
                            row.prop(Add_Deep_Rod_Setback, "distance_value", text="Rod Setback: ")
                    else:
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        row.prop(Add_Rod_Setback, "distance_value", text="Rod Setback: ")

                    if(add_shelves_in_top_section.get_value()):
                        if add_top_shelf_setback:
                            row = box.row()
                            row.label(text="", icon='BLANK1')
                            row.prop(add_top_shelf_setback, "distance_value", text="Top Shelves Setback: ")
                    elif(add_top_shelf.get_value()):
                        if add_top_shelf_setback:
                            row = box.row()
                            row.label(text="", icon='BLANK1')
                            row.prop(add_top_shelf_setback, "distance_value", text="Top Dust Shelf Setback: ")

                    if add_shelves_in_middle_section.get_value():
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        row.prop(add_middle_shelf_setback, "distance_value", text="Bottom Shelves Setback: ")

                    if add_bottom_shelf.get_value() and is_hang_double.get_value():
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        row.prop(add_bottom_shelf_setback, "distance_value", text="Dust Shelf Setback: ")
                
                    #Below
                    shelf_quantity = self.insert.get_prompt("Below Shelf Quantity")    
                    add_shelves = self.insert.get_prompt("Add Below Shelves")

                    if shelf_quantity and add_shelves:
                        box = column.box()
                        row = box.row()
                        row.label(text="Add Shelves Below Hang")
                        row.prop(add_shelves, 'checkbox_value', text="")
                        if(add_shelves.get_value()):
                            if shelf_quantity:
                                col = box.column(align=True)
                                row = col.row()
                                row.label(text="Qty:")
                                row.prop(self,"below_shelf_quantity",expand=True)   
                                col.separator()  
                                for i in range(1,shelf_quantity.get_value() + 1):
                                    shelf = self.insert.get_prompt("Below Shelf " + str(i) + " Height")
                                    setback = self.insert.get_prompt("Below Shelf " + str(i) + " Setback")
                                    if shelf:
                                        row = box.row()
                                        row.label(text="Shelf " + str(i) + " Height:")
                                        row.prop(self,'Below_Shelf_' + str(i) + '_Height',text="")
                                    
                                    if setback:
                                        row = box.row()
                                        row.label(text="Shelf " + str(i) + " Setback")
                                        row.prop(setback,'distance_value',text="")


class PROMPTS_Shelf_Only_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.shelves_only"
    bl_label = "Shelf Prompts"
    bl_description = "This shows all of the available shelf options"
    bl_options = {'UNDO'}

    assembly = None

    def check(self, context):
        return True

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
                shelf_quantity = self.assembly.get_prompt("Shelf Qty")
                row = layout.row()
                shelf_quantity.draw(row, allow_edit=False)


class PROMPTS_Glass_Shelf_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.glass_shelves"
    bl_label = "Glass Shelf Prompts"
    bl_description = "This shows all of the available shelf options"
    bl_options = {'UNDO'}

    assembly = None

    glass_thickness: EnumProperty(
        name="Glass Thickness",
        items=[
            ('0', '1/4"', '1/4"'),
            ('1', '3/8"', '3/8"'),
            ('2', '1/2"', '1/2"')],
        default='0')

    glass_thickness_prompt = None
    shelf_thickness_prompt = None

    def set_glass_thickness_prompt(self, context):
        if self.glass_thickness_prompt:
            self.glass_thickness_prompt.set_value(int(self.glass_thickness))

    def check(self, context):
        self.set_glass_thickness_prompt(context)   
        return True

    def execute(self, context):
        return {'FINISHED'}

    def set_properties_from_prompts(self, context):
        self.glass_thickness_prompt = self.assembly.get_prompt("Glass Shelf Thickness")
        if self.glass_thickness_prompt:
            self.glass_thickness = str(self.glass_thickness_prompt.combobox_index)


    def invoke(self, context, event):
        self.assembly = self.get_insert()
        self.set_properties_from_prompts(context)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                shelf_quantity = self.assembly.get_prompt("Shelf Qty")
                shelf_thickness = self.assembly.get_prompt("Glass Shelf Thickness")
                box = layout.box()
                col = box.column()
                shelf_quantity.draw(col, allow_edit=False)
                row = col.row()
                row.label(text="Glass Shelf Thickness")
                row.prop(self, "glass_thickness", expand=True)


class OPS_Rods_And_Shelves_Drop(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.insert_rods_and_shelves_drop"
    bl_label = "Custom drag and drop for Rods and Shelves insert"

    def execute(self, context):
        return super().execute(context)

    def position_asset(self, context):
        super().position_asset(context)
        edp = self.insert.get_prompt("Extra Deep Pard")
        abdss = self.insert.get_prompt("Add Bottom Deep Shelf Setback")
        adrs = self.insert.get_prompt("Add Deep Rod Setback")
        ihd = self.insert.get_prompt("Is Hang Double")

        if self.insert.obj_y.location.y >= edp.get_value():
            if ihd.get_value():
                abdss.set_value(self.insert.obj_y.location.y - sn_unit.inch(12))
            adrs.set_value(self.insert.obj_y.location.y - sn_unit.inch(12))        

bpy.utils.register_class(OPS_Rods_And_Shelves_Drop)
bpy.utils.register_class(PROMPTS_Shelf_Only_Prompts)
bpy.utils.register_class(PROMPTS_Glass_Shelf_Prompts)
bpy.utils.register_class(PROMPTS_Hanging_Rod_With_Shelves_Prompts)
