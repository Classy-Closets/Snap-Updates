import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists


class Hanging_Rods_with_Shelves(fd_types.Assembly):

    property_id = props_closet.LIBRARY_NAME_SPACE + \
        ".hanging_rod_with_shelves_prompts"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    mirror_y = False

    def add_rod(self, assembly, location, is_hanger=False):
        Width = self.get_var('dim_x', 'Width')
        Depth = self.get_var('dim_y', 'Depth')
        Height = self.get_var('dim_z', 'Height')
        Setback_from_Rear = self.get_var("Setback from Rear")
        Z_Loc = self.get_var("Top Rod Location From Top", 'Z_Loc')
        Top_Rod_Location = self.get_var("Top Rod Location")
        Turn_Off_Hangers = self.get_var("Turn Off Hangers")
        Hanging_Rod_Width_Deduction = self.get_var(
            "Hanging Rod Width Deduction")
        Hanging_Rod_Setback = self.get_var("Hanging Rod Setback")
        Add_Rod_Setback = self.get_var("Add Rod Setback")
        Add_Deep_Rod_Setback = self.get_var("Add Deep Rod Setback")

        Default_Deep_Setback = self.get_var("Default Deep Setback")
        Extra_Deep_Pard = self.get_var("Extra Deep Pard")

        assembly.x_loc('Hanging_Rod_Width_Deduction/2',
                       [Hanging_Rod_Width_Deduction])
        assembly.x_rot(value=0)
        assembly.y_rot(value=0)
        assembly.z_rot(value=0)
        assembly.x_dim('Width-Hanging_Rod_Width_Deduction',
                       [Width, Hanging_Rod_Width_Deduction])
        assembly.y_dim(value=unit.inch(.5))
        assembly.z_dim(value=unit.inch(-1))

        if location == 'TOP':
            Add_Top_Rod = self.get_var("Add Top Rod")
            assembly.z_loc('Height-Z_Loc', [Height, Z_Loc])
            assembly.y_loc('IF(Depth>=Extra_Deep_Pard,Hanging_Rod_Setback+Add_Deep_Rod_Setback,Hanging_Rod_Setback+Add_Rod_Setback)',
                           [Hanging_Rod_Setback, Add_Rod_Setback, Extra_Deep_Pard, Depth, Default_Deep_Setback, Add_Deep_Rod_Setback])
            if is_hanger:
                assembly.prompt("Hide", 'IF(Turn_Off_Hangers,True,IF(Add_Top_Rod,False,True))', [
                                Add_Top_Rod, Turn_Off_Hangers])
            else:
                assembly.prompt(
                    "Hide", 'IF(Add_Top_Rod,False,True)', [Add_Top_Rod])
        if location == 'MID':
            Add_Middle_Rod = self.get_var("Add Middle Rod")
            assembly.z_loc('Height-Top_Rod_Location-Z_Loc+0.032004',
                           [Height, Top_Rod_Location, Z_Loc])
            assembly.y_loc('IF(Depth>=Extra_Deep_Pard,Hanging_Rod_Setback+Add_Deep_Rod_Setback,Hanging_Rod_Setback+Add_Rod_Setback)',
                           [Hanging_Rod_Setback, Add_Rod_Setback, Extra_Deep_Pard, Depth, Default_Deep_Setback, Add_Deep_Rod_Setback])
            if is_hanger:
                assembly.prompt("Hide", 'IF(Turn_Off_Hangers,True,IF(Add_Middle_Rod,False,True))', [
                                Add_Middle_Rod, Turn_Off_Hangers])
            else:
                assembly.prompt(
                    "Hide", 'IF(Add_Middle_Rod,False,True)', [Add_Middle_Rod])
        if location == 'BOT':
            Add_Bottom_Rod = self.get_var("Add Bottom Rod")
            Bottom_Rod_Location = self.get_var("Bottom Rod Location")
            assembly.z_loc('Height-Bottom_Rod_Location-Z_Loc+0.032004',
                           [Height, Bottom_Rod_Location, Z_Loc])
            assembly.y_loc('IF(Depth>=Extra_Deep_Pard,Hanging_Rod_Setback+Add_Deep_Rod_Setback,Hanging_Rod_Setback+Add_Rod_Setback)',
                           [Hanging_Rod_Setback, Add_Rod_Setback, Extra_Deep_Pard, Depth, Default_Deep_Setback, Add_Deep_Rod_Setback])
            if is_hanger:
                assembly.prompt("Hide", 'IF(Turn_Off_Hangers,True,IF(Add_Bottom_Rod,False,True))', [
                                Add_Bottom_Rod, Turn_Off_Hangers])
            else:
                assembly.prompt(
                    "Hide", 'IF(Add_Bottom_Rod,False,True)', [Add_Bottom_Rod])

        return assembly

    def add_shelves(self):
        Width = self.get_var('dim_x', 'Width')
        Depth = self.get_var('dim_y', 'Depth')
        Height = self.get_var('dim_z', 'Height')
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Add_Shelves_In_Top_Section = self.get_var("Add Shelves In Top Section")
        Add_Shelves_In_Middle_Section = self.get_var(
            "Add Shelves In Middle Section")
        Add_Shelves_In_Bottom_Section = self.get_var(
            "Add Shelves In Bottom Section")
        Top_Shelf_Quantity = self.get_var("Top Shelf Quantity")
        Middle_Shelf_Quantity = self.get_var("Middle Shelf Quantity")
        Bottom_Shelf_Quantity = self.get_var("Bottom Shelf Quantity")
        Top_Rod_Location = self.get_var("Top Rod Location")
        Bottom_Rod_Location = self.get_var("Bottom Rod Location")
        Bottom_Shelves_Location = self.get_var("Bottom Shelves Location")
        Shelf_Clip_Gap = self.get_var("Shelf Clip Gap")
        Shelf_Setback = self.get_var("Shelf Setback")

        Is_Hang_Single = self.get_var("Is Hang Single")

        ATSS = self.get_var("Add Top Shelf Setback", 'ATSS')
        AMSS = self.get_var("Add Middle Shelf Setback", 'AMSS')
        ABSS = self.get_var("Add Bottom Shelf Setback", 'ABSS')
        IHD = self.get_var("Is Hang Double", 'IHD')
        DDS = self.get_var("Default Deep Setback", 'DDS')
        EDP = self.get_var("Extra Deep Pard", 'EDP')

        # TOP SECTION
        top_opening_height = "(Top_Rod_Location-Shelf_Thickness-0.064008)"
        top_opening_z_loc = "(Height-Top_Rod_Location+Shelf_Thickness+0.064008)"
        top_opening_thickness_deduction = "(Shelf_Thickness*Top_Shelf_Quantity)"
        top_opening_qty = "(Top_Shelf_Quantity+1)"

        adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')

        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [
                        Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.y_loc('Depth', [Depth])
        adj_shelf.z_loc(top_opening_z_loc + "+(" + top_opening_height + "-" + top_opening_thickness_deduction + ")/" + top_opening_qty,
                        [Top_Rod_Location, Shelf_Thickness, Height, Top_Shelf_Quantity])
        adj_shelf.x_rot(value=0)
        adj_shelf.y_rot(value=0)
        adj_shelf.z_rot(value=0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                        [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ATSS',
                        [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, ATSS])
        adj_shelf.z_dim('Shelf_Thickness', [Shelf_Thickness])
        adj_shelf.prompt('Hide', 'IF(AND(Top_Shelf_Quantity>0,Add_Shelves_In_Top_Section),False,True)',
                         [Top_Shelf_Quantity, Add_Shelves_In_Top_Section])
        adj_shelf.prompt('Z Quantity', 'Top_Shelf_Quantity',
                         [Top_Shelf_Quantity])
        adj_shelf.prompt('Z Offset', '((' + top_opening_height + '-' + top_opening_thickness_deduction + ')/' + top_opening_qty + ')+Shelf_Thickness',
                         [Top_Rod_Location, Shelf_Thickness, Top_Shelf_Quantity])

        # MIDDLE SECTION
        mid_opening_height = "(Bottom_Rod_Location-Top_Rod_Location-Shelf_Thickness-0.064008)"
        mid_opening_z_loc = "(Height-Bottom_Rod_Location+Shelf_Thickness+0.064008)"
        mid_opening_thickness_deduction = "(Shelf_Thickness*Middle_Shelf_Quantity)"
        mid_opening_qty = "(Middle_Shelf_Quantity+1)"
        adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')

        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [
                        Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.y_loc('Depth', [Depth])
        adj_shelf.z_loc(mid_opening_z_loc + "+(" + mid_opening_height + "-" + mid_opening_thickness_deduction + ")/" + mid_opening_qty,
                        [Bottom_Rod_Location, Top_Rod_Location, Shelf_Thickness, Height, Middle_Shelf_Quantity])
        adj_shelf.x_rot(value=0)
        adj_shelf.y_rot(value=0)
        adj_shelf.z_rot(value=0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                        [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+AMSS',
                        [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, AMSS])
        adj_shelf.z_dim('Shelf_Thickness', [Shelf_Thickness])
        adj_shelf.prompt('Hide', 'IF(Is_Hang_Single,True,IF(AND(Middle_Shelf_Quantity>0,Add_Shelves_In_Middle_Section),False,True))',
                         [Middle_Shelf_Quantity, Add_Shelves_In_Middle_Section, Is_Hang_Single])
        adj_shelf.prompt('Z Quantity', 'Middle_Shelf_Quantity', [
                         Middle_Shelf_Quantity])
        adj_shelf.prompt('Z Offset', '((' + mid_opening_height + '-' + mid_opening_thickness_deduction + ')/' + mid_opening_qty + ')+Shelf_Thickness',
                         [Top_Rod_Location, Bottom_Rod_Location, Shelf_Thickness, Middle_Shelf_Quantity, Height])

        # Short Hang Mid
        short_mid_opening_height = "(Bottom_Rod_Location-Shelf_Thickness)"
        short_mid_opening_z_loc = "(Height-Bottom_Rod_Location+Shelf_Thickness+0.064008)"
        short_mid_opening_thickness_deduction = "(Shelf_Thickness*Middle_Shelf_Quantity)"
        short_mid_opening_qty = "(Middle_Shelf_Quantity+1)"
        short_adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')

        short_adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [
                              Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        short_adj_shelf.y_loc('Depth', [Depth])
        short_adj_shelf.z_loc(short_mid_opening_z_loc + "+(" + short_mid_opening_height + "-" + short_mid_opening_thickness_deduction + ")/" + short_mid_opening_qty,
                              [Bottom_Rod_Location, Top_Rod_Location, Shelf_Thickness, Height, Middle_Shelf_Quantity])
        short_adj_shelf.x_rot(value=0)
        short_adj_shelf.y_rot(value=0)
        short_adj_shelf.z_rot(value=0)
        short_adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                              [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        short_adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+AMSS', [
                              Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, AMSS])
        short_adj_shelf.z_dim('Shelf_Thickness', [Shelf_Thickness])
        short_adj_shelf.prompt('Hide', 'IF(Is_Hang_Single, IF(AND(Middle_Shelf_Quantity>0,Add_Shelves_In_Middle_Section),False,True),True)',
                               [Middle_Shelf_Quantity, Add_Shelves_In_Middle_Section, Is_Hang_Single])
        short_adj_shelf.prompt('Z Quantity', 'Middle_Shelf_Quantity', [
                               Middle_Shelf_Quantity])
        short_adj_shelf.prompt('Z Offset', '((' + short_mid_opening_height + '-' + short_mid_opening_thickness_deduction + ')/' + short_mid_opening_qty + ')+Shelf_Thickness',
                               [Top_Rod_Location, Bottom_Rod_Location, Shelf_Thickness, Middle_Shelf_Quantity, Height])

        # BOTTOM SECTION
        bottom_opening_height = "(Bottom_Shelves_Location-Bottom_Rod_Location-Shelf_Thickness)"
        bottom_opening_z_loc = "(Height-Bottom_Shelves_Location)"
        bottom_opening_thickness_deduction = "(Shelf_Thickness*Bottom_Shelf_Quantity)"
        bottom_opening_qty = "(Bottom_Shelf_Quantity+1)"
        adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')

        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Shelf_Clip_Gap)',
                        [Is_Locked_Shelf, Shelf_Clip_Gap])
        adj_shelf.y_loc('Depth', [Depth])
        adj_shelf.z_loc(bottom_opening_z_loc + "+(" + bottom_opening_height + "-" + bottom_opening_thickness_deduction + ")/" + bottom_opening_qty,
                        [Bottom_Shelves_Location,Bottom_Rod_Location,Shelf_Thickness,Height,Bottom_Shelf_Quantity])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABSS',[Depth,Locked_Shelf_Setback,Is_Locked_Shelf,Adj_Shelf_Setback,ABSS])
        adj_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(AND(Bottom_Shelf_Quantity>0,Add_Shelves_In_Bottom_Section),False,True)',
                         [Bottom_Shelf_Quantity,Add_Shelves_In_Bottom_Section])
        adj_shelf.prompt('Z Quantity','Bottom_Shelf_Quantity',[Bottom_Shelf_Quantity])
        adj_shelf.prompt('Z Offset','((' + bottom_opening_height + '-' + bottom_opening_thickness_deduction + ')/' + bottom_opening_qty + ')+Shelf_Thickness',
                         [Bottom_Shelves_Location,Bottom_Rod_Location,Shelf_Thickness,Bottom_Shelf_Quantity])

        #Below Shelves Section

        Add_Below_Shelves = self.get_var("Add Below Shelves")
        Below_Shelf_Quantity = self.get_var("Below Shelf Quantity")

        previous_splitter = None          
        
        for i in range(1,9):

            Shelf_Height = self.get_var("Below Shelf " + str(i) + " Height", 'Shelf_Height')

            shelf_empty = self.add_empty()
            if previous_splitter:
                prev_shelf_z_loc = previous_splitter.get_var('loc_z','prev_shelf_z_loc')
                shelf_empty.z_loc('prev_shelf_z_loc-Shelf_Height',[prev_shelf_z_loc,Shelf_Height])
            else:
                shelf_empty.z_loc('Height-Bottom_Rod_Location-Shelf_Height',
                                  [Shelf_Height,Height,Bottom_Rod_Location])   

            sh_z_loc = shelf_empty.get_var('loc_z','sh_z_loc')
                
            splitter = common_parts.add_shelf(self)
            
            Is_Locked_Shelf = splitter.get_var('Is Locked Shelf')
            Adj_Shelf_Setback = splitter.get_var('Adj Shelf Setback')
            Locked_Shelf_Setback = splitter.get_var('Locked Shelf Setback')
            Adj_Shelf_Clip_Gap = splitter.get_var('Adj Shelf Clip Gap')    
            Shelf_Setback = self.get_var("Below Shelf " + str(i) + " Setback", 'Shelf_Setback')
            
            splitter.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_loc('Depth',[Depth])
            splitter.z_loc('sh_z_loc',[sh_z_loc])
            splitter.x_rot(value = 0)
            splitter.y_rot(value = 0)
            splitter.z_rot(value = 0)
            splitter.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Shelf_Setback',[Depth,Locked_Shelf_Setback,Is_Locked_Shelf,Adj_Shelf_Setback,Shelf_Setback])
            splitter.z_dim('Shelf_Thickness',[Shelf_Thickness])
            splitter.prompt('Hide','IF(Add_Below_Shelves,IF(Below_Shelf_Quantity+1>'+str(i)+',False,True),True)',[Add_Below_Shelves,Below_Shelf_Quantity])
            
            previous_splitter = splitter  

    def add_shelves_above_rod(self):
        Width = self.get_var('dim_x', 'Width')
        Depth = self.get_var('dim_y', 'Depth')
        Height = self.get_var('dim_z', 'Height')
        Top_Rod_Location = self.get_var("Top Rod Location")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Shelf_Clip_Gap = self.get_var("Shelf Clip Gap")
        Bottom_Rod_Location = self.get_var("Bottom Rod Location")
        Add_Top_Shelf = self.get_var("Add Top Shelf")
        Add_Bottom_Shelf = self.get_var("Add Bottom Shelf")
        Shelf_Setback = self.get_var("Shelf Setback")

        IHD = self.get_var("Is Hang Double", 'IHD')
        DDS = self.get_var("Default Deep Setback", 'DDS')
        EDP = self.get_var("Extra Deep Pard", 'EDP')
        edp = self.get_prompt("Extra Deep Pard")
        #abss = self.get_prompt("Add Bottom Shelf Setback")
        #abdss = self.get_prompt("Add Bottom Deep Shelf Setback")
        # if(self.obj_y.location.y >= edp.value()):
        #abdss.set_value(self.obj_y.location.y - unit.inch(12))
        ATSS = self.get_var("Add Top Shelf Setback", 'ATSS')
        ABSS = self.get_var("Add Bottom Shelf Setback", 'ABSS')
        ABDSS = self.get_var("Add Bottom Deep Shelf Setback", 'ABDSS')

        shelf = common_parts.add_shelf(self)
        Is_Locked_Shelf = shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = shelf.get_var('Adj Shelf Clip Gap')

        shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',
                    [Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        shelf.y_loc('Depth', [Depth])
        shelf.z_loc('Height-Top_Rod_Location+0.064008',
                    [Height, Top_Rod_Location])
        shelf.x_dim('Width-IF(Is_Locked_Shelf,0,(Adj_Shelf_Clip_Gap*2))',
                    [Width, Adj_Shelf_Clip_Gap, Is_Locked_Shelf])

        shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ATSS',
                    [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, ATSS])
        shelf.z_dim('-Shelf_Thickness', [Shelf_Thickness])
        shelf.prompt('Hide', 'IF(Add_Top_Shelf,False,True)', [Add_Top_Shelf])

        shelf = common_parts.add_shelf(self)
        Is_Locked_Shelf = shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = shelf.get_var('Adj Shelf Clip Gap')

        shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',
                    [Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        shelf.y_loc('Depth', [Depth])
        shelf.z_loc('Height-Bottom_Rod_Location+0.064008',
                    [Height, Bottom_Rod_Location])
        shelf.x_dim('Width-IF(Is_Locked_Shelf,0,(Adj_Shelf_Clip_Gap*2))',
                    [Width, Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        shelf.y_dim('IF(IHD,IF(Depth>=EDP,-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABDSS,-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABSS),-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+ABSS)',
                    [Depth, Locked_Shelf_Setback, Is_Locked_Shelf, Adj_Shelf_Setback, ABSS, IHD, DDS, EDP, ABDSS])
        shelf.z_dim('Shelf_Thickness', [Shelf_Thickness])
        shelf.prompt('Hide', 'IF(Add_Bottom_Shelf,False,True)',
                     [Add_Bottom_Shelf])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True

        props = props_closet.get_scene_props().closet_defaults
        
        self.add_tab(name='Hanging Options',tab_type='VISIBLE')
        self.add_prompt(name="Add Top Rod",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Add Middle Rod",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Add Bottom Rod",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Add Top Shelf",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Add Bottom Shelf",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Top Rod Location",prompt_type='DISTANCE',value=unit.millimeter(428.95),tab_index=0)
        self.add_prompt(name="Bottom Rod Location",prompt_type='DISTANCE',value=unit.millimeter(1164.95),tab_index=0)
        self.add_prompt(name="Bottom Shevles Location",prompt_type='DISTANCE',value=unit.millimeter(1164.95),tab_index=0)
        
        self.add_prompt(name="Add Shelves In Top Section",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Add Shelves In Middle Section",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Add Shelves In Bottom Section",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Top Shelf Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        self.add_prompt(name="Middle Shelf Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        self.add_prompt(name="Bottom Shelf Quantity",prompt_type='QUANTITY',value=1,tab_index=0)

        self.add_prompt(name="Add Below Shelves",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Below Shelf Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        for i in range(1,9):
            self.add_prompt(name="Below Shelf " + str(i) + " Height",prompt_type='DISTANCE',value=unit.millimeter(91.95),tab_index=0)
            self.add_prompt(name="Below Shelf " + str(i) + " Setback",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Below Shelf Stack Height",prompt_type='DISTANCE',value=0,tab_index=0)
        
        self.add_prompt(name="Hanging Rod Width Deduction",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        self.add_prompt(name="Shelf Clip Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        self.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        self.add_prompt(name="Setback from Rear",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Top Rod Location From Top",prompt_type='DISTANCE',value=unit.inch(1.26),tab_index=0)
        self.add_prompt(name="Turn Off Hangers",prompt_type='CHECKBOX',value=props.hide_hangers,tab_index=0)
        
        self.add_prompt(name="Shelf Setback",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Hanging Rod Setback",prompt_type='DISTANCE',value=unit.inch(1.69291),tab_index=0)  
        self.add_prompt(name="Add Rod Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)

        self.add_prompt(name="Is Hang Single",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Is Hang Double",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Add Top Shelf Setback",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Add Middle Shelf Setback",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Add Bottom Shelf Setback",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Add Bottom Deep Shelf Setback",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Default Deep Setback",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)
        self.add_prompt(name="Extra Deep Pard",prompt_type='DISTANCE',value=unit.inch(16),tab_index=0)
        self.add_prompt(name="Add Deep Rod Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        self.prompt("Shelf Thickness", 'THICKNESS(sgi,"Shelf")',[sgi])

        self.add_shelves_above_rod()

        opts = props_closet.get_scene_props().closet_options

        if "Oval" in opts.rods_name:
            self.add_rod(common_parts.add_oval_hanging_rod(
                self), location="TOP")
            self.add_rod(common_parts.add_oval_hanging_rod(
                self), location="MID")
            self.add_rod(common_parts.add_oval_hanging_rod(
                self), location="BOT")

        else:
            self.add_rod(common_parts.add_round_hanging_rod(
                self), location="TOP")
            self.add_rod(common_parts.add_round_hanging_rod(
                self), location="MID")
            self.add_rod(common_parts.add_round_hanging_rod(
                self), location="BOT")

        self.add_rod(common_parts.add_hangers(self),
                     location="TOP", is_hanger=True)
        self.add_rod(common_parts.add_hangers(self),
                     location="MID", is_hanger=True)
        self.add_rod(common_parts.add_hangers(self),
                     location="BOT", is_hanger=True)

        self.add_shelves()

        self.update()


class Shelves_Only(fd_types.Assembly):

    property_id = props_closet.LIBRARY_NAME_SPACE + ".shelves_only"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    mirror_y = False

    def add_adj_prompts(self):
        self.add_prompt(name="Shelf Qty",
                        prompt_type='QUANTITY',
                        value=5,
                        tab_index=0)

    def add_shelves(self):
        Width = self.get_var('dim_x', 'Width')
        Height = self.get_var('dim_z', 'Height')
        Depth = self.get_var('dim_y', 'Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Thickness = self.get_var("Shelf Thickness")

        adj_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')

        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)', [
                        Adj_Shelf_Clip_Gap, Is_Locked_Shelf])
        adj_shelf.y_loc('Depth', [Depth])
        adj_shelf.z_loc('((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))',
                        [Height, Shelf_Thickness, Shelf_Qty])
        adj_shelf.x_rot(value=0)
        adj_shelf.y_rot(value=0)
        adj_shelf.z_rot(value=0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',
                        [Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',
                        [Depth, Is_Locked_Shelf, Locked_Shelf_Setback, Adj_Shelf_Setback])
        adj_shelf.z_dim('Shelf_Thickness', [Shelf_Thickness])
        adj_shelf.prompt('Hide', 'IF(Shelf_Qty==0,True,False)', [Shelf_Qty])
        adj_shelf.prompt('Z Quantity', 'Shelf_Qty', [Shelf_Qty])
        adj_shelf.prompt('Z Offset', '((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness',
                         [Height, Shelf_Thickness, Shelf_Qty])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True

        self.add_tab(name='Interior Options', tab_type='VISIBLE')
        self.add_tab(name='Formulas', tab_type='HIDDEN')

        common_prompts.add_thickness_prompts(self)

        self.add_adj_prompts()
        self.add_shelves()
        self.draw_as_hidden_line()
        self.update()


class Glass_Shelves(fd_types.Assembly):

    property_id = props_closet.LIBRARY_NAME_SPACE + ".glass_shelves"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    mirror_y = False

    def add_adj_prompts(self):
        self.add_prompt(name="Shelf Qty",
                        prompt_type='QUANTITY',
                        value=5,
                        tab_index=0)

    def add_glass_thickness_prompts(self):
        self.add_prompt(
            name="Glass Shelf Thickness",
            prompt_type='COMBOBOX',
            items=['1/4"', '3/8"', '1/2"'],
            value=0,
            tab_index=0,
            columns=3
        )

        ST = self.get_var("Glass Shelf Thickness", "ST")
        self.add_prompt(name="Shelf Thickness", prompt_type='DISTANCE',
                        value=unit.inch(0.75), tab_index=1)
        self.prompt('Shelf Thickness',
                    'IF(ST==0,INCH(0.25),IF(ST==1,INCH(0.375),INCH(0.5)))', [ST])

    def glass_shelves(self):
        Width = self.get_var('dim_x', 'Width')
        Height = self.get_var('dim_z', 'Height')
        Depth = self.get_var('dim_y', 'Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Thickness = self.get_var("Shelf Thickness")

        adj_shelf = common_parts.add_glass_shelf(self)

        adj_shelf.x_loc(value=0)
        adj_shelf.y_loc('Depth', [Depth])
        adj_shelf.z_loc('((Height-((Shelf_Thickness)*Shelf_Qty))/(Shelf_Qty+1))',
                        [Height, Shelf_Thickness, Shelf_Qty])
        adj_shelf.x_rot(value=0)
        adj_shelf.y_rot(value=0)
        adj_shelf.z_rot(value=0)
        adj_shelf.x_dim('Width', [Width])
        adj_shelf.y_dim('-Depth+0.00635', [Depth])
        adj_shelf.z_dim('-Shelf_Thickness', [Shelf_Thickness])
        adj_shelf.prompt('Hide', 'IF(Shelf_Qty==0,True,False)', [Shelf_Qty])
        adj_shelf.prompt('Z Quantity', 'Shelf_Qty', [Shelf_Qty])
        adj_shelf.prompt('Z Offset', '((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness',
                         [Height, Shelf_Thickness, Shelf_Qty])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True

        self.add_tab(name='Options', tab_type='VISIBLE')
        self.add_tab(name='Formulas', tab_type='HIDDEN')

        self.add_glass_thickness_prompts()

        self.add_adj_prompts()
        self.glass_shelves()
        self.draw_as_hidden_line()
        self.update()


class Bridge_Shelves(fd_types.Assembly):

    property_id = props_closet.LIBRARY_NAME_SPACE + ".bridge_shelves"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    mirror_y = False

    def add_adj_prompts(self):
        self.add_prompt(name="Shelf Qty",
                        prompt_type='QUANTITY',
                        value=5,
                        tab_index=0)

        self.add_prompt(name="Bridge Left",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=0)

        self.add_prompt(name="Bridge Right",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=0)

        self.add_prompt(name="Bridge Amount",
                        prompt_type='DISTANCE',
                        value=unit.inch(.1875),
                        tab_index=0)

    def add_shelves(self):
        Width = self.get_var('dim_x', 'Width')
        Height = self.get_var('dim_z', 'Height')
        Depth = self.get_var('dim_y', 'Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Bridge_Left = self.get_var("Bridge Left")
        Bridge_Right = self.get_var("Bridge Right")
        Bridge_Amount = self.get_var("Bridge Amount")

        bridge_shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = bridge_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = bridge_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = bridge_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = bridge_shelf.get_var('Adj Shelf Clip Gap')

        bridge_shelf.x_loc('IF(Bridge_Left,-Bridge_Amount,Adj_Shelf_Clip_Gap)',
                           [Bridge_Left, Bridge_Amount, Adj_Shelf_Clip_Gap])
        bridge_shelf.y_loc('Depth', [Depth])
        bridge_shelf.z_loc('((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))',
                           [Height, Shelf_Thickness, Shelf_Qty])
        bridge_shelf.x_rot(value=0)
        bridge_shelf.y_rot(value=0)
        bridge_shelf.z_rot(value=0)
        bridge_shelf.x_dim('Width+IF(Bridge_Left,Bridge_Amount,-Adj_Shelf_Clip_Gap)+IF(Bridge_Right,Bridge_Amount,-Adj_Shelf_Clip_Gap)',
                           [Bridge_Left, Bridge_Right, Bridge_Amount, Width, Is_Locked_Shelf, Adj_Shelf_Clip_Gap])
        bridge_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',
                           [Depth, Is_Locked_Shelf, Locked_Shelf_Setback, Adj_Shelf_Setback])
        bridge_shelf.z_dim('Shelf_Thickness', [Shelf_Thickness])
        bridge_shelf.prompt('Hide', 'IF(Shelf_Qty==0,True,False)', [Shelf_Qty])
        bridge_shelf.prompt('Z Quantity', 'Shelf_Qty', [Shelf_Qty])
        bridge_shelf.prompt(
            'Z Offset', '((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness', [Height, Shelf_Thickness, Shelf_Qty])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True

        self.add_tab(name='Interior Options', tab_type='VISIBLE')
        self.add_tab(name='Formulas', tab_type='HIDDEN')

        common_prompts.add_thickness_prompts(self)

        self.add_adj_prompts()
        self.add_shelves()
        self.draw_as_hidden_line()
        self.update()


class PROMPTS_Hanging_Rod_With_Shelves_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".hanging_rod_with_shelves_prompts"
    bl_label = "Hanging Rod Prompts"
    bl_description = "This shows all of the available door options"
    bl_options = {'UNDO'}

    object_name = bpy.props.StringProperty(name="Object Name")

    top_shelf_quantity = bpy.props.IntProperty(
        name="Top Shelf Quantity", min=1, max=10)

    middle_shelf_quantity = bpy.props.IntProperty(
        name="Middle Shelf Quantity", min=1, max=10)

    bottom_shelf_quantity = bpy.props.IntProperty(
        name="Bottom Shelf Quantity", min=1, max=10)

    top_rod_location = bpy.props.EnumProperty(name="Top Rod Location",
                                              items=common_lists.ROD_HEIGHTS)

    bottom_rod_location = bpy.props.EnumProperty(name="Bottom Rod Location",
                                                 items=common_lists.ROD_HEIGHTS)

    bottom_shelves_location = bpy.props.EnumProperty(name="Bottom Shelves Location",
                                               items=common_lists.ROD_HEIGHTS)  

    below_shelf_quantity = bpy.props.EnumProperty(name="Below Shelf Quantity",
                                   items=[('1',"1",'1'),
                                          ('2',"2",'2'),
                                          ('3',"3",'3'),
                                          ('4',"4",'4'),
                                          ('5',"5",'5'),
                                          ('6',"6",'6'),
                                          ('7',"7",'7'),
                                          ('8',"8",'8')],
                                   default = '3')

    Below_Shelf_1_Height = bpy.props.EnumProperty(name="Below Shelf 1 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_2_Height = bpy.props.EnumProperty(name="Below Shelf 2 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_3_Height = bpy.props.EnumProperty(name="Below Shelf 3 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_4_Height = bpy.props.EnumProperty(name="Below Shelf 4 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_5_Height = bpy.props.EnumProperty(name="Below Shelf 5 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_6_Height = bpy.props.EnumProperty(name="Below Shelf 6 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_7_Height = bpy.props.EnumProperty(name="Below Shelf 7 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Below_Shelf_8_Height = bpy.props.EnumProperty(name="Below Shelf 8 Height",
                                    items=common_lists.OPENING_HEIGHTS)  

    shelf_quantity_prompt = None    
    
    assembly = None

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        self.set_prompts_from_properties()
        self.assembly.obj_bp.location = self.assembly.obj_bp.location  # Redraw Viewport
        return True

    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''
        top_rod_location = self.assembly.get_prompt("Top Rod Location")
        top_shelf_quantity = self.assembly.get_prompt("Top Shelf Quantity")
        bottom_rod_location = self.assembly.get_prompt("Bottom Rod Location")
        middle_shelf_quantity = self.assembly.get_prompt(
            "Middle Shelf Quantity")
        bottom_shelves_location = self.assembly.get_prompt(
            "Bottom Shelves Location")
        bottom_shelf_quantity = self.assembly.get_prompt(
            "Bottom Shelf Quantity")
        if top_shelf_quantity:
            top_shelf_quantity.set_value(self.top_shelf_quantity)
        if middle_shelf_quantity:
            middle_shelf_quantity.set_value(self.middle_shelf_quantity)
        if bottom_shelf_quantity:
            bottom_shelf_quantity.set_value(self.bottom_shelf_quantity)
        if top_rod_location:
            top_rod_location.DistanceValue = unit.inch(
                float(self.top_rod_location) / 25.4)
        if bottom_rod_location:
            bottom_rod_location.DistanceValue = unit.inch(
                float(self.bottom_rod_location) / 25.4)
        if bottom_shelves_location:
            bottom_shelves_location.DistanceValue = unit.inch(
                float(self.bottom_shelves_location) / 25.4)

        self.shelf_quantity_prompt.QuantityValue = int(self.below_shelf_quantity)
        for i in range(1,9):
            shelf = self.assembly.get_prompt("Below Shelf " + str(i) + " Height")
            if shelf:
                if not shelf.equal:
                    exec("shelf.DistanceValue = unit.inch(float(self.Below_Shelf_" + str(i) + "_Height) / 25.4)")  

    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        top_rod_location = self.assembly.get_prompt("Top Rod Location")
        if top_rod_location:
            value = round(top_rod_location.value() * 1000, 2)
            for index, height in enumerate(common_lists.ROD_HEIGHTS):
                if not value >= float(height[0]):
                    self.top_rod_location = common_lists.ROD_HEIGHTS[index - 1][0]
                    break

        bottom_rod_location = self.assembly.get_prompt("Bottom Rod Location")
        if bottom_rod_location:
            value = round(bottom_rod_location.value() * 1000, 2)
            for index, height in enumerate(common_lists.ROD_HEIGHTS):
                if not value >= float(height[0]):
                    self.bottom_rod_location = common_lists.ROD_HEIGHTS[index - 1][0]
                    break

        bottom_shelves_location = self.assembly.get_prompt(
            "Bottom Shelves Location")
        if bottom_shelves_location:
            value = round(bottom_shelves_location.value() * 1000, 2)
            for index, height in enumerate(common_lists.ROD_HEIGHTS):
                if not value >= float(height[0]):
                    self.bottom_shelves_location = common_lists.ROD_HEIGHTS[index - 1][0]
                    break

        top_shelf_quantity = self.assembly.get_prompt("Top Shelf Quantity")
        middle_shelf_quantity = self.assembly.get_prompt(
            "Middle Shelf Quantity")
        bottom_shelf_quantity = self.assembly.get_prompt(
            "Bottom Shelf Quantity")

        if top_shelf_quantity:
            self.top_shelf_quantity = top_shelf_quantity.value()
        if middle_shelf_quantity:
            self.middle_shelf_quantity = middle_shelf_quantity.value()
        if bottom_shelf_quantity:
            self.bottom_shelf_quantity = bottom_shelf_quantity.value()    

        self.shelf_quantity_prompt = self.assembly.get_prompt("Below Shelf Quantity")
        if self.shelf_quantity_prompt:
            self.below_shelf_quantity = str(self.shelf_quantity_prompt.QuantityValue)

        for i in range(1,9):
            shelf = self.assembly.get_prompt("Below Shelf " + str(i) + " Height")
            if shelf:
                value = round(shelf.value() * 1000,3)
                for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        exec("self.Below_Shelf_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[index - 1][0]")
                        break    
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj, 'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                add_top_rod = self.assembly.get_prompt("Add Top Rod")
                add_middle_rod = self.assembly.get_prompt("Add Middle Rod")
                add_bottom_rod = self.assembly.get_prompt("Add Bottom Rod")
                add_shelves_in_top_section = self.assembly.get_prompt(
                    "Add Shelves In Top Section")
                add_shelves_in_middle_section = self.assembly.get_prompt(
                    "Add Shelves In Middle Section")
                add_shelves_in_bottom_section = self.assembly.get_prompt(
                    "Add Shelves In Bottom Section")
                add_top_shelf = self.assembly.get_prompt("Add Top Shelf")
                add_bottom_shelf = self.assembly.get_prompt("Add Bottom Shelf")
                rod_setback = self.assembly.get_prompt("Hanging Rod Setback")
                Add_Rod_Setback = self.assembly.get_prompt("Add Rod Setback")
                shelf_setback = self.assembly.get_prompt("Shelf Setback")
                is_hang_single = self.assembly.get_prompt("Is Hang Single")

                add_top_shelf_setback = self.assembly.get_prompt(
                    "Add Top Shelf Setback")
                add_middle_shelf_setback = self.assembly.get_prompt(
                    "Add Middle Shelf Setback")
                add_bottom_shelf_setback = self.assembly.get_prompt(
                    "Add Bottom Shelf Setback")
                add_bottom_deep_shelf_setback = self.assembly.get_prompt(
                    "Add Bottom Deep Shelf Setback")
                Add_Deep_Rod_Setback = self.assembly.get_prompt(
                    "Add Deep Rod Setback")
                is_hang_double = self.assembly.get_prompt("Is Hang Double")
                extra_deep_pard = self.assembly.get_prompt("Extra Deep Pard")

                if add_top_rod and add_middle_rod and add_bottom_rod:
                    column = layout.column(align=True)

                    # Top

                    box = column.box()
                    box.label("Top Opening:")

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    add_top_rod.draw_prompt(
                        row, split_text=False, text="Rod at Top")

                    if(is_hang_single.value() != True):

                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        add_middle_rod.draw_prompt(
                            row, split_text=False, text="Add Rod")
                        row.prop(self, 'top_rod_location', text="")
                        row.label(text="", icon='TRIA_DOWN')

                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        add_top_shelf.draw_prompt(
                            row, split_text=False, text="Add Dust Shelf")

                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        add_shelves_in_top_section.draw_prompt(
                            row, split_text=False, text="Add Shelves")
                        if add_shelves_in_top_section.value():
                            row.prop(self, "top_shelf_quantity",
                                     text="Quantity")

                    # Mid
                    box = column.box()
                    box.label("Bottom Opening:")

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    add_bottom_rod.draw_prompt(
                        row, split_text=False, text="Add Rod")
                    row.prop(self, 'bottom_rod_location', text="")
                    row.label(text="", icon='TRIA_UP')

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    add_bottom_shelf.draw_prompt(
                        row, split_text=False, text="Add Dust Shelf")

                    row = box.row()
                    row.label(text="", icon='BLANK1')
                    add_shelves_in_middle_section.draw_prompt(
                        row, text="Add Shelves", split_text=False)
                    if add_shelves_in_middle_section.value():
                        row.prop(self, "middle_shelf_quantity",
                                 text="Quantity")

                    # #Bottom
                    # box = column.box()
                    # box.label("Bottom Opening:")

                    # row = box.row()
                    # row.label(text="",icon='BLANK1')
                    # row.prop(self,'bottom_shelves_location',text="")
                    # row.label(text="",icon='TRIA_UP')

                    # row = box.row()
                    # row.label(text="",icon='BLANK1')
                    # add_shelves_in_bottom_section.draw_prompt(row,text="Add Shelves",split_text=False)
                    # if add_shelves_in_bottom_section.value():
                    #     row.prop(self,"bottom_shelf_quantity",text="Quantity")

                    box = column.box()
                    box.label("Setbacks:")
                    if(self.assembly.obj_y.location.y >= extra_deep_pard.value()):
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        Add_Deep_Rod_Setback.draw_prompt(
                            row, text="Rod Setback: ", split_text=True)
                    else:
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        Add_Rod_Setback.draw_prompt(
                            row, text="Rod Setback: ", split_text=True)

                    if(add_shelves_in_top_section.value()):
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        add_top_shelf_setback.draw_prompt(
                            row, text="Top Shelves Setback: ", split_text=True)
                    elif(add_top_shelf.value()):
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        add_top_shelf_setback.draw_prompt(
                            row, text="Top Dust Shelf Setback: ", split_text=True)

                    if(add_shelves_in_middle_section.value()):
                        row = box.row()
                        row.label(text="", icon='BLANK1')
                        add_middle_shelf_setback.draw_prompt(
                            row, text="Bottom Shelves Setback: ", split_text=True)

                    if(add_bottom_shelf.value() and is_hang_double.value()):
                        if(self.assembly.obj_y.location.y >= extra_deep_pard.value()):
                            row = box.row()
                            row.label(text="", icon='BLANK1')
                            add_bottom_deep_shelf_setback.draw_prompt(
                                row, text="Dust Shelf Setback: ", split_text=True)
                        else:
                            row = box.row()
                            row.label(text="", icon='BLANK1')
                            add_bottom_shelf_setback.draw_prompt(
                                row, text="Dust Shelf Setback: ", split_text=True)


                
                    #Below
                    shelf_quantity = self.assembly.get_prompt("Below Shelf Quantity")    
                    add_shelves = self.assembly.get_prompt("Add Below Shelves")
                    box = column.box()
                    row=box.row()
                    row.label("Add Shelves Below Hang")
                    row.prop(add_shelves, 'CheckBoxValue', text="")
                    if(add_shelves.value()):
                        if shelf_quantity:
                            col = box.column(align=True)
                            row = col.row()
                            row.label("Qty:")
                            row.prop(self,"below_shelf_quantity",expand=True)   
                            col.separator()  
                            for i in range(1,shelf_quantity.value() + 1):
                                shelf = self.assembly.get_prompt("Below Shelf " + str(i) + " Height")
                                setback = self.assembly.get_prompt("Below Shelf " + str(i) + " Setback")
                                if shelf:
                                    row = box.row()
                                    row.label("Shelf " + str(i) + " Height:")
                                    row.prop(self,'Below_Shelf_' + str(i) + '_Height',text="")
                                
                                if setback:
                                    row = box.row()
                                    row.label("Shelf " + str(i) + " Setback")
                                    row.prop(setback,'DistanceValue',text="")

class PROMPTS_Shelf_Only_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".shelves_only"
    bl_label = "Shelf Prompts"
    bl_description = "This shows all of the available shelf options"
    bl_options = {'UNDO'}

    object_name = bpy.props.StringProperty(name="Object Name")

    assembly = None

    shelf = None

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj, 'INSERT')
        obj_bp = utils.get_assembly_bp(obj)
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.shelf = fd_types.Assembly(obj_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:

                shelf_quantity = self.assembly.get_prompt("Shelf Qty")

                row = layout.row()
                shelf_quantity.draw_prompt(row)


class PROMPTS_Glass_Shelf_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".glass_shelves"
    bl_label = "Glass Shelf Prompts"
    bl_description = "This shows all of the available shelf options"
    bl_options = {'UNDO'}

    object_name = bpy.props.StringProperty(name="Object Name")

    assembly = None

    shelf = None

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj, 'INSERT')
        obj_bp = utils.get_assembly_bp(obj)
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.shelf = fd_types.Assembly(obj_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:

                shelf_quantity = self.assembly.get_prompt("Shelf Qty")
                shelf_thickness = self.assembly.get_prompt(
                    "Glass Shelf Thickness")

                box = layout.box()
                col = box.column()
                shelf_quantity.draw_prompt(col)
                shelf_thickness.draw_prompt(col)


class PROMPTS_Bridge_Shelf_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".bridge_shelves"
    bl_label = "Bridge Shelf Prompts"
    bl_description = "This shows all of the available bridge shelf options"
    bl_options = {'UNDO'}

    object_name = bpy.props.StringProperty(name="Object Name")

    assembly = None

    shelf = None

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj, 'INSERT')
        obj_bp = utils.get_assembly_bp(obj)
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.shelf = fd_types.Assembly(obj_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:

                shelf_quantity = self.assembly.get_prompt("Shelf Qty")
                bridge_left = self.assembly.get_prompt("Bridge Left")
                bridge_right = self.assembly.get_prompt("Bridge Right")
                bridge_amount = self.assembly.get_prompt("Bridge Amount")

                row = layout.row()
                shelf_quantity.draw_prompt(row)

                row = layout.row()
                bridge_left.draw_prompt(row)

                row = layout.row()
                bridge_right.draw_prompt(row)

                row = layout.row()
                bridge_amount.draw_prompt(row)


class OPS_Rods_And_Shelves_Drop(bpy.types.Operator):
    bl_idname = "closets.insert_rods_and_shelves_drop"
    bl_label = "Custom drag and drop for Rods and Shelves insert"

    object_name = bpy.props.StringProperty(name="Object Name")
    product_name = bpy.props.StringProperty(name="Product Name")
    category_name = bpy.props.StringProperty(name="Category Name")
    library_name = bpy.props.StringProperty(name="Library Name")

    insert = None
    default_z_loc = 0.0
    default_height = 0.0
    default_depth = 0.0

    openings = []
    objects = []

    header_text = "Place Insert   (Esc, Right Click) = Cancel Command  :  (Left Click) = Place Insert"

    def execute(self, context):
        return {'FINISHED'}

    def __del__(self):
        bpy.context.area.header_text_set()

    def set_wire_and_xray(self, obj, turn_on):
        if turn_on:
            obj.draw_type = 'WIRE'
        else:
            obj.draw_type = 'TEXTURED'
        obj.show_x_ray = turn_on
        for child in obj.children:
            self.set_wire_and_xray(child, turn_on)

    def get_insert(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        if self.object_name in bpy.data.objects:
            bp = bpy.data.objects[self.object_name]
            self.insert = fd_types.Assembly(bp)

        if not self.insert:
            lib = context.window_manager.cabinetlib.lib_inserts[self.library_name]
            blend_path = os.path.join(
                lib.lib_path, self.category_name, self.product_name + ".blend")
            obj_bp = None

            if os.path.exists(blend_path):
                obj_bp = utils.get_group(blend_path)
                self.insert = fd_types.Assembly(obj_bp)
            else:
                self.insert = utils.get_insert_class(
                    context, self.library_name, self.category_name, self.product_name)

            if obj_bp:
                pass
            # TODO: SET UP UPDATE OPERATOR
                # self.insert.update(obj_bp)
            else:
                self.insert.draw()
                self.insert.update()

        self.show_openings()

        utils.init_objects(self.insert.obj_bp)
        self.default_z_loc = self.insert.obj_bp.location.z
        self.default_height = self.insert.obj_z.location.z
        self.default_depth = self.insert.obj_y.location.y

    def invoke(self, context, event):
        self.insert = None
        context.window.cursor_set('WAIT')
        self.get_insert(context)
        self.set_wire_and_xray(self.insert.obj_bp, True)
        if self.insert is None:
            bpy.ops.fd_general.error('INVOKE_DEFAULT', message="Could Not Find Insert Class: " +
                                     "\\" + self.library_name + "\\" + self.category_name + "\\" + self.product_name)
            return {'CANCELLED'}
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update()  # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self, context, event):
        if self.insert:
            utils.delete_object_and_children(self.insert.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def show_openings(self):
        # Clear  to avoid old/duplicate openings
        self.objects.clear()
        insert_type = self.insert.obj_bp.mv.placement_type
        for obj in bpy.context.scene.objects:
            # Check to avoid opening that is part of the dropped insert
            if utils.get_parent_assembly_bp(obj) == self.insert.obj_bp:
                continue

            if obj.layers[0]:  # Make sure wall is not hidden
                opening = None
                if obj.mv.type_group == 'OPENING':
                    if insert_type in {'INTERIOR', 'SPLITTER'}:
                        opening = fd_types.Assembly(
                            obj) if obj.mv.interior_open else None
                    if insert_type == 'EXTERIOR':
                        opening = fd_types.Assembly(
                            obj) if obj.mv.exterior_open else None
                    if opening:
                        cage = opening.get_cage()
                        opening.obj_x.hide = True
                        opening.obj_y.hide = True
                        opening.obj_z.hide = True
                        cage.hide_select = False
                        cage.hide = False
                        self.objects.append(cage)

    def selected_opening(self, selected_obj):
        if selected_obj:
            opening = fd_types.Assembly(selected_obj.parent)
            if opening.obj_bp.parent:
                if self.insert.obj_bp.parent is not opening.obj_bp.parent:
                    self.insert.obj_bp.parent = opening.obj_bp.parent
                    self.insert.obj_bp.location = opening.obj_bp.location
                    self.insert.obj_bp.rotation_euler = opening.obj_bp.rotation_euler
                    self.insert.obj_x.location.x = opening.obj_x.location.x
                    self.insert.obj_y.location.y = opening.obj_y.location.y
                    self.insert.obj_z.location.z = opening.obj_z.location.z
                    utils.run_calculators(self.insert.obj_bp)
                    return opening

    def set_opening_name(self, obj, name):
        obj.mv.opening_name = name
        for child in obj.children:
            self.set_opening_name(child, name)

    def place_insert(self, opening):
        if self.insert.obj_bp.mv.placement_type == 'INTERIOR':
            opening.obj_bp.mv.interior_open = False
        if self.insert.obj_bp.mv.placement_type == 'EXTERIOR':
            opening.obj_bp.mv.exterior_open = False
        if self.insert.obj_bp.mv.placement_type == 'SPLITTER':
            opening.obj_bp.mv.interior_open = False
            opening.obj_bp.mv.exterior_open = False

        utils.copy_assembly_drivers(opening, self.insert)
        self.set_opening_name(self.insert.obj_bp,
                              opening.obj_bp.mv.opening_name)
        self.set_wire_and_xray(self.insert.obj_bp, False)

        for obj in self.objects:
            obj.hide = True
            obj.hide_render = True
            obj.hide_select = True

    def insert_drop(self, context, event):
        if len(self.objects) == 0:
            bpy.ops.fd_general.error(
                'INVOKE_DEFAULT', message="There are no openings in this scene.")
            return self.cancel_drop(context, event)
        else:
            selected_point, selected_obj = utils.get_selection_point(
                context, event, objects=self.objects)
            bpy.ops.object.select_all(action='DESELECT')
            selected_opening = self.selected_opening(selected_obj)
            if selected_opening:
                selected_obj.select = True

                edp = self.insert.get_prompt("Extra Deep Pard")
                abdss = self.insert.get_prompt("Add Bottom Deep Shelf Setback")
                adrs = self.insert.get_prompt("Add Deep Rod Setback")
                ihd = self.insert.get_prompt("Is Hang Double")
                if(self.insert.obj_y.location.y >= edp.value()):
                    if(ihd.value()):
                        abdss.set_value(
                            self.insert.obj_y.location.y - unit.inch(12))
                    adrs.set_value(
                        self.insert.obj_y.location.y - unit.inch(12))

                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.place_insert(selected_opening)

                    context.scene.objects.active = self.insert.obj_bp
                    # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
                    utils.run_calculators(self.insert.obj_bp)
                    utils.run_calculators(self.insert.obj_bp)

                    bpy.context.window.cursor_set('DEFAULT')

                    return {'FINISHED'}

            return {'RUNNING_MODAL'}

    def modal(self, context, event):
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        if event.type in {'ESC', 'RIGHTMOUSE'}:
            self.cancel_drop(context, event)
            return {'FINISHED'}

        return self.insert_drop(context, event)


bpy.utils.register_class(OPS_Rods_And_Shelves_Drop)
bpy.utils.register_class(PROMPTS_Shelf_Only_Prompts)
bpy.utils.register_class(PROMPTS_Glass_Shelf_Prompts)
bpy.utils.register_class(PROMPTS_Hanging_Rod_With_Shelves_Prompts)
bpy.utils.register_class(PROMPTS_Bridge_Shelf_Prompts)
