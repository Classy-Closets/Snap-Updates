import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

class Hanging_Rods_with_Shelves(fd_types.Assembly):
    
    property_id = props_closet.LIBRARY_NAME_SPACE + ".hanging_rod_with_shelves_prompts"
    type_assembly = "INSERT"   
    placement_type = "INTERIOR"
    mirror_y = False        
            
    def add_rod(self,assembly,location,is_hanger=False):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Height = self.get_var('dim_z','Height')        
        Setback_from_Rear = self.get_var("Setback from Rear")
        Z_Loc = self.get_var("Top Rod Location From Top",'Z_Loc')
        Top_Rod_Location = self.get_var("Top Rod Location")
        Turn_Off_Hangers = self.get_var("Turn Off Hangers")
        Hanging_Rod_Width_Deduction = self.get_var("Hanging Rod Width Deduction")
        Hanging_Rod_Setback = self.get_var("Hanging Rod Setback")
        Add_Rod_Setback = self.get_var("Add Rod Setback")

        assembly.x_loc('Hanging_Rod_Width_Deduction/2',[Hanging_Rod_Width_Deduction])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = 0)
        assembly.z_rot(value = 0)
        assembly.x_dim('Width-Hanging_Rod_Width_Deduction',[Width,Hanging_Rod_Width_Deduction])
        assembly.y_dim(value = unit.inch(.5))
        assembly.z_dim(value = unit.inch(-1))
        
        if location == 'TOP':
            Add_Top_Rod = self.get_var("Add Top Rod")
            assembly.z_loc('Height-Z_Loc',[Height,Z_Loc])
            assembly.y_loc('Hanging_Rod_Setback+Add_Rod_Setback',[Hanging_Rod_Setback,Add_Rod_Setback])
            if is_hanger:
                assembly.prompt("Hide",'IF(Turn_Off_Hangers,True,IF(Add_Top_Rod,False,True))',[Add_Top_Rod,Turn_Off_Hangers])
            else:
                assembly.prompt("Hide",'IF(Add_Top_Rod,False,True)',[Add_Top_Rod])
        if location == 'MID':
            Add_Middle_Rod = self.get_var("Add Middle Rod")
            assembly.z_loc('Height-Top_Rod_Location-Z_Loc+0.032004',[Height,Top_Rod_Location,Z_Loc])
            assembly.y_loc('Hanging_Rod_Setback+Add_Rod_Setback',[Hanging_Rod_Setback,Add_Rod_Setback])
            if is_hanger:
                assembly.prompt("Hide",'IF(Turn_Off_Hangers,True,IF(Add_Middle_Rod,False,True))',[Add_Middle_Rod,Turn_Off_Hangers])
            else:
                assembly.prompt("Hide",'IF(Add_Middle_Rod,False,True)',[Add_Middle_Rod])
        if location == 'BOT':
            Add_Bottom_Rod = self.get_var("Add Bottom Rod")
            Bottom_Rod_Location = self.get_var("Bottom Rod Location")
            assembly.z_loc('Height-Bottom_Rod_Location-Z_Loc+0.032004',[Height,Bottom_Rod_Location,Z_Loc])
            assembly.y_loc('Hanging_Rod_Setback+Add_Rod_Setback',[Hanging_Rod_Setback,Add_Rod_Setback])
            if is_hanger:
                assembly.prompt("Hide",'IF(Turn_Off_Hangers,True,IF(Add_Bottom_Rod,False,True))',[Add_Bottom_Rod,Turn_Off_Hangers])
            else:
                assembly.prompt("Hide",'IF(Add_Bottom_Rod,False,True)',[Add_Bottom_Rod])
            
        return assembly
        
    def add_shelves(self):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Height = self.get_var('dim_z','Height')  
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Add_Shelves_In_Top_Section = self.get_var("Add Shelves In Top Section")
        Add_Shelves_In_Middle_Section = self.get_var("Add Shelves In Middle Section")
        Add_Shelves_In_Bottom_Section = self.get_var("Add Shelves In Bottom Section")
        Top_Shelf_Quantity = self.get_var("Top Shelf Quantity")
        Middle_Shelf_Quantity = self.get_var("Middle Shelf Quantity")
        Bottom_Shelf_Quantity = self.get_var("Bottom Shelf Quantity")
        Top_Rod_Location = self.get_var("Top Rod Location")
        Bottom_Rod_Location = self.get_var("Bottom Rod Location")
        Bottom_Shelves_Location = self.get_var("Bottom Shelves Location")
        Shelf_Clip_Gap = self.get_var("Shelf Clip Gap")
        Shelf_Setback = self.get_var("Shelf Setback")
        Add_Shelf_Setback = self.get_var("Add Shelf Setback")
        
        #TOP SECTION
        top_opening_height = "(Top_Rod_Location-Shelf_Thickness-0.064008)"
        top_opening_z_loc = "(Height-Top_Rod_Location+Shelf_Thickness+0.064008)"
        top_opening_thickness_deduction = "(Shelf_Thickness*Top_Shelf_Quantity)"
        top_opening_qty = "(Top_Shelf_Quantity+1)"
        
        adj_shelf = common_parts.add_shelf(self)
        
        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')
        
        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc(top_opening_z_loc + "+(" + top_opening_height + "-" + top_opening_thickness_deduction + ")/" + top_opening_qty,
                        [Top_Rod_Location,Shelf_Thickness,Height,Top_Shelf_Quantity])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Add_Shelf_Setback',[Add_Shelf_Setback,Depth,Locked_Shelf_Setback,Is_Locked_Shelf,Adj_Shelf_Setback])
        adj_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(AND(Top_Shelf_Quantity>0,Add_Shelves_In_Top_Section),False,True)',
                         [Top_Shelf_Quantity,Add_Shelves_In_Top_Section])
        adj_shelf.prompt('Z Quantity','Top_Shelf_Quantity',[Top_Shelf_Quantity])
        adj_shelf.prompt('Z Offset','((' + top_opening_height + '-' + top_opening_thickness_deduction + ')/' + top_opening_qty + ')+Shelf_Thickness',
                         [Top_Rod_Location,Shelf_Thickness,Top_Shelf_Quantity])        
        
        #MIDDLE SECTION
        mid_opening_height = "(Bottom_Rod_Location-Top_Rod_Location-Shelf_Thickness-0.064008)"
        mid_opening_z_loc = "(Height-Bottom_Rod_Location+Shelf_Thickness+0.064008)"
        mid_opening_thickness_deduction = "(Shelf_Thickness*Middle_Shelf_Quantity)"
        mid_opening_qty = "(Middle_Shelf_Quantity+1)"
        adj_shelf = common_parts.add_shelf(self)
        
        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')
        
        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc(mid_opening_z_loc + "+(" + mid_opening_height + "-" + mid_opening_thickness_deduction + ")/" + mid_opening_qty,
                        [Bottom_Rod_Location,Top_Rod_Location,Shelf_Thickness,Height,Middle_Shelf_Quantity])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Add_Shelf_Setback',[Add_Shelf_Setback,Depth,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
        adj_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(AND(Middle_Shelf_Quantity>0,Add_Shelves_In_Middle_Section),False,True)',
                         [Middle_Shelf_Quantity,Add_Shelves_In_Middle_Section])
        adj_shelf.prompt('Z Quantity','Middle_Shelf_Quantity',[Middle_Shelf_Quantity])
        adj_shelf.prompt('Z Offset','((' + mid_opening_height + '-' + mid_opening_thickness_deduction + ')/' + mid_opening_qty + ')+Shelf_Thickness',
                         [Top_Rod_Location,Bottom_Rod_Location,Shelf_Thickness,Middle_Shelf_Quantity])        
        
        #BOTTOM SECTION
        bottom_opening_height = "(Bottom_Shelves_Location-Bottom_Rod_Location-Shelf_Thickness)"
        bottom_opening_z_loc = "(Height-Bottom_Shelves_Location)"
        bottom_opening_thickness_deduction = "(Shelf_Thickness*Bottom_Shelf_Quantity)"
        bottom_opening_qty = "(Bottom_Shelf_Quantity+1)"
        adj_shelf = common_parts.add_shelf(self)
        
        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')
        
        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Shelf_Clip_Gap)',[Is_Locked_Shelf,Shelf_Clip_Gap])
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc(bottom_opening_z_loc + "+(" + bottom_opening_height + "-" + bottom_opening_thickness_deduction + ")/" + bottom_opening_qty,
                        [Bottom_Shelves_Location,Bottom_Rod_Location,Shelf_Thickness,Height,Bottom_Shelf_Quantity])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Shelf_Setback,0)+Add_Shelf_Setback',[Add_Shelf_Setback,Depth,Is_Locked_Shelf,Shelf_Setback])
        adj_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(AND(Bottom_Shelf_Quantity>0,Add_Shelves_In_Bottom_Section),False,True)',
                         [Bottom_Shelf_Quantity,Add_Shelves_In_Bottom_Section])
        adj_shelf.prompt('Z Quantity','Bottom_Shelf_Quantity',[Bottom_Shelf_Quantity])
        adj_shelf.prompt('Z Offset','((' + bottom_opening_height + '-' + bottom_opening_thickness_deduction + ')/' + bottom_opening_qty + ')+Shelf_Thickness',
                         [Bottom_Shelves_Location,Bottom_Rod_Location,Shelf_Thickness,Bottom_Shelf_Quantity])  

    def add_shelves_above_rod(self):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Height = self.get_var('dim_z','Height')
        Top_Rod_Location = self.get_var("Top Rod Location")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Shelf_Clip_Gap = self.get_var("Shelf Clip Gap")
        Bottom_Rod_Location = self.get_var("Bottom Rod Location")
        Add_Top_Shelf = self.get_var("Add Top Shelf")
        Add_Bottom_Shelf = self.get_var("Add Bottom Shelf")
        Shelf_Setback = self.get_var("Shelf Setback")
        Add_Shelf_Setback = self.get_var("Add Shelf Setback")
        
        shelf = common_parts.add_shelf(self)
        Is_Locked_Shelf = shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = shelf.get_var('Adj Shelf Clip Gap')
        
        shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Adj_Shelf_Clip_Gap,Is_Locked_Shelf])
        shelf.y_loc('Depth',[Depth])
        shelf.z_loc('Height-Top_Rod_Location+0.064008',[Height,Top_Rod_Location])
        shelf.x_dim('Width-IF(Is_Locked_Shelf,0,(Adj_Shelf_Clip_Gap*2))',[Width,Adj_Shelf_Clip_Gap,Is_Locked_Shelf])
        shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Add_Shelf_Setback',[Add_Shelf_Setback,Depth,Is_Locked_Shelf,Adj_Shelf_Setback,Locked_Shelf_Setback])
        shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Hide','IF(Add_Top_Shelf,False,True)',[Add_Top_Shelf])
        
        shelf = common_parts.add_shelf(self)
        Is_Locked_Shelf = shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = shelf.get_var('Adj Shelf Clip Gap')
        
        shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Adj_Shelf_Clip_Gap,Is_Locked_Shelf])
        shelf.y_loc('Depth',[Depth])
        shelf.z_loc('Height-Bottom_Rod_Location+0.064008',[Height,Bottom_Rod_Location])
        shelf.x_dim('Width-IF(Is_Locked_Shelf,0,(Adj_Shelf_Clip_Gap*2))',[Width,Adj_Shelf_Clip_Gap,Is_Locked_Shelf])
        shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Add_Shelf_Setback',[Add_Shelf_Setback,Depth,Is_Locked_Shelf,Adj_Shelf_Setback,Locked_Shelf_Setback])
        shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Hide','IF(Add_Bottom_Shelf,False,True)',[Add_Bottom_Shelf])

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
        
        self.add_prompt(name="Hanging Rod Width Deduction",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        self.add_prompt(name="Shelf Clip Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        self.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        self.add_prompt(name="Setback from Rear",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Top Rod Location From Top",prompt_type='DISTANCE',value=unit.inch(1.26),tab_index=0)
        self.add_prompt(name="Turn Off Hangers",prompt_type='CHECKBOX',value=props.hide_hangers,tab_index=0)
        
        self.add_prompt(name="Shelf Setback",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Add Shelf Setback",prompt_type='DISTANCE',value=unit.inch(0.0),tab_index=0)  
        self.add_prompt(name="Hanging Rod Setback",prompt_type='DISTANCE',value=unit.inch(1.69291),tab_index=0)  
        self.add_prompt(name="Add Rod Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)     
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        self.prompt("Shelf Thickness", 'THICKNESS(sgi,"Shelf")',[sgi])

        self.add_shelves_above_rod()

        opts = props_closet.get_scene_props().closet_options

        if "Oval" in opts.rods_name:
            self.add_rod(common_parts.add_oval_hanging_rod(self), location = "TOP")
            self.add_rod(common_parts.add_oval_hanging_rod(self), location = "MID")
            self.add_rod(common_parts.add_oval_hanging_rod(self), location = "BOT")

        else:
            self.add_rod(common_parts.add_round_hanging_rod(self), location = "TOP")
            self.add_rod(common_parts.add_round_hanging_rod(self), location = "MID")
            self.add_rod(common_parts.add_round_hanging_rod(self), location = "BOT")            
        
        self.add_rod(common_parts.add_hangers(self), location = "TOP",is_hanger=True)
        self.add_rod(common_parts.add_hangers(self), location = "MID",is_hanger=True)
        self.add_rod(common_parts.add_hangers(self), location = "BOT",is_hanger=True)
        
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
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        
        adj_shelf = common_parts.add_shelf(self)
        
        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')
        
        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Adj_Shelf_Clip_Gap,Is_Locked_Shelf])
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc('((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))',[Height,Shelf_Thickness,Shelf_Qty])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',[Depth,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
        adj_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(Shelf_Qty==0,True,False)',[Shelf_Qty])
        adj_shelf.prompt('Z Quantity','Shelf_Qty',[Shelf_Qty])
        adj_shelf.prompt('Z Offset','((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness',[Height,Shelf_Thickness,Shelf_Qty])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        self.add_tab(name='Interior Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
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

    def glass_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        
        adj_shelf = common_parts.add_glass_shelf(self)
        
        adj_shelf.x_loc(value = 0)
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc('((Height-((Shelf_Thickness-.0127)*Shelf_Qty))/(Shelf_Qty+1))',[Height,Shelf_Thickness,Shelf_Qty])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width',[Width])
        adj_shelf.y_dim('-Depth+0.00635',[Depth])
        adj_shelf.z_dim('-Shelf_Thickness+0.0127',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(Shelf_Qty==0,True,False)',[Shelf_Qty])
        adj_shelf.prompt('Z Quantity','Shelf_Qty',[Shelf_Qty])
        adj_shelf.prompt('Z Offset','((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness',[Height,Shelf_Thickness,Shelf_Qty])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        self.add_tab(name='Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        common_prompts.add_thickness_prompts(self)

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
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
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
        
        bridge_shelf.x_loc('IF(Bridge_Left,-Bridge_Amount,Adj_Shelf_Clip_Gap)',[Bridge_Left,Bridge_Amount,Adj_Shelf_Clip_Gap])
        bridge_shelf.y_loc('Depth',[Depth])
        bridge_shelf.z_loc('((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))',[Height,Shelf_Thickness,Shelf_Qty])
        bridge_shelf.x_rot(value = 0)
        bridge_shelf.y_rot(value = 0)
        bridge_shelf.z_rot(value = 0)
        bridge_shelf.x_dim('Width+IF(Bridge_Left,Bridge_Amount,-Adj_Shelf_Clip_Gap)+IF(Bridge_Right,Bridge_Amount,-Adj_Shelf_Clip_Gap)',
                           [Bridge_Left,Bridge_Right,Bridge_Amount,Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        bridge_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',[Depth,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
        bridge_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        bridge_shelf.prompt('Hide','IF(Shelf_Qty==0,True,False)',[Shelf_Qty])
        bridge_shelf.prompt('Z Quantity','Shelf_Qty',[Shelf_Qty])
        bridge_shelf.prompt('Z Offset','((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness',[Height,Shelf_Thickness,Shelf_Qty])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        self.add_tab(name='Interior Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
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
    
    top_shelf_quantity = bpy.props.IntProperty(name="Top Shelf Quantity",min=1,max=10)
    
    middle_shelf_quantity = bpy.props.IntProperty(name="Middle Shelf Quantity",min=1,max=10)
    
    bottom_shelf_quantity = bpy.props.IntProperty(name="Bottom Shelf Quantity",min=1,max=10)
    
    top_rod_location = bpy.props.EnumProperty(name="Top Rod Location",
                                                items=common_lists.OPENING_HEIGHTS)    
    
    bottom_rod_location = bpy.props.EnumProperty(name="Bottom Rod Location",
                                               items=common_lists.OPENING_HEIGHTS)      
    
    bottom_shelves_location = bpy.props.EnumProperty(name="Bottom Shelves Location",
                                               items=common_lists.OPENING_HEIGHTS)       
    
    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        self.set_prompts_from_properties()
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''        
        top_rod_location = self.assembly.get_prompt("Top Rod Location")
        top_shelf_quantity = self.assembly.get_prompt("Top Shelf Quantity")
        bottom_rod_location = self.assembly.get_prompt("Bottom Rod Location") 
        middle_shelf_quantity = self.assembly.get_prompt("Middle Shelf Quantity")
        bottom_shelves_location = self.assembly.get_prompt("Bottom Shelves Location")
        bottom_shelf_quantity = self.assembly.get_prompt("Bottom Shelf Quantity")
        if top_shelf_quantity:
            top_shelf_quantity.set_value(self.top_shelf_quantity)
        if middle_shelf_quantity:
            middle_shelf_quantity.set_value(self.middle_shelf_quantity)             
        if bottom_shelf_quantity:
            bottom_shelf_quantity.set_value(self.bottom_shelf_quantity)        
        if top_rod_location:
            top_rod_location.DistanceValue = unit.inch(float(self.top_rod_location) / 25.4)      
        if bottom_rod_location:
            bottom_rod_location.DistanceValue = unit.inch(float(self.bottom_rod_location) / 25.4)
        if bottom_shelves_location:
            bottom_shelves_location.DistanceValue = unit.inch(float(self.bottom_shelves_location) / 25.4)

    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        top_rod_location = self.assembly.get_prompt("Top Rod Location")
        if top_rod_location:
            value = round(top_rod_location.value() * 1000,2)
            for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                if not value >= float(height[0]):
                    self.top_rod_location = common_lists.OPENING_HEIGHTS[index - 1][0]
                    break
        
        bottom_rod_location = self.assembly.get_prompt("Bottom Rod Location")
        if bottom_rod_location:
            value = round(bottom_rod_location.value() * 1000,2)
            for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                if not value >= float(height[0]):
                    self.bottom_rod_location = common_lists.OPENING_HEIGHTS[index - 1][0]
                    break
        
        bottom_shelves_location = self.assembly.get_prompt("Bottom Shelves Location")
        if bottom_shelves_location:
            value = round(bottom_shelves_location.value() * 1000,2)
            for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                if not value >= float(height[0]):
                    self.bottom_shelves_location = common_lists.OPENING_HEIGHTS[index - 1][0]
                    break
        
        top_shelf_quantity = self.assembly.get_prompt("Top Shelf Quantity")
        middle_shelf_quantity = self.assembly.get_prompt("Middle Shelf Quantity")
        bottom_shelf_quantity = self.assembly.get_prompt("Bottom Shelf Quantity")  
        
        if top_shelf_quantity:
            self.top_shelf_quantity = top_shelf_quantity.value()
        if middle_shelf_quantity:
            self.middle_shelf_quantity = middle_shelf_quantity.value()            
        if bottom_shelf_quantity:
            self.bottom_shelf_quantity = bottom_shelf_quantity.value()        
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
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
                add_shelves_in_top_section = self.assembly.get_prompt("Add Shelves In Top Section")
                add_shelves_in_middle_section = self.assembly.get_prompt("Add Shelves In Middle Section")
                add_shelves_in_bottom_section = self.assembly.get_prompt("Add Shelves In Bottom Section")
                add_top_shelf = self.assembly.get_prompt("Add Top Shelf")
                add_bottom_shelf = self.assembly.get_prompt("Add Bottom Shelf")
                rod_setback = self.assembly.get_prompt("Hanging Rod Setback")
                Add_Rod_Setback = self.assembly.get_prompt("Add Rod Setback")
                shelf_setback = self.assembly.get_prompt("Shelf Setback")
                add_shelf_setback = self.assembly.get_prompt("Add Shelf Setback")
                
                
                if add_top_rod and add_middle_rod and add_bottom_rod:
                    column = layout.column(align=True)
                    
                    #Top
                    box = column.box()
                    box.label("Top Opening:")
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_top_rod.draw_prompt(row,split_text=False,text="Rod at Top")
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_middle_rod.draw_prompt(row,split_text=False,text="Add Rod")
                    row.prop(self,'top_rod_location',text="")
                    row.label(text="",icon='TRIA_DOWN')
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_top_shelf.draw_prompt(row,split_text=False,text="Add Dust Shelf")
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_shelves_in_top_section.draw_prompt(row,split_text=False,text="Add Shelves")
                    if add_shelves_in_top_section.value():
                        row.prop(self,"top_shelf_quantity",text="Quantity")
                    
                    #Mid
                    box = column.box()
                    box.label("Bottom Opening:")
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_bottom_rod.draw_prompt(row,split_text=False,text="Add Rod")
                    row.prop(self,'bottom_rod_location',text="")  
                    row.label(text="",icon='TRIA_UP')     
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_bottom_shelf.draw_prompt(row,split_text=False,text="Add Dust Shelf")  
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_shelves_in_middle_section.draw_prompt(row,text="Add Shelves",split_text=False)
                    if add_shelves_in_middle_section.value():
                        row.prop(self,"middle_shelf_quantity",text="Quantity")
                    
#                     #Bottom
#                     box = column.box()
#                     box.label("Bottom Opening:")
#                     
#                     row = box.row()
#                     row.label(text="",icon='BLANK1')
#                     row.prop(self,'bottom_shelves_location',text="")  
#                     row.label(text="",icon='TRIA_UP')  
#                                       
#                     row = box.row()
#                     row.label(text="",icon='BLANK1')
#                     add_shelves_in_bottom_section.draw_prompt(row,text="Add Shelves",split_text=False)
#                     if add_shelves_in_bottom_section.value():
#                         row.prop(self,"bottom_shelf_quantity",text="Quantity")   
                    
                    box = column.box()
                    box.label("Setbacks:")    
                    
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    Add_Rod_Setback.draw_prompt(row,text="Rod Setback: ",split_text=True)   
                                         
                    row = box.row()
                    row.label(text="",icon='BLANK1')
                    add_shelf_setback.draw_prompt(row,text="Shelf Setback: ",split_text=True)

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
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
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
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
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
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
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


bpy.utils.register_class(PROMPTS_Shelf_Only_Prompts)
bpy.utils.register_class(PROMPTS_Glass_Shelf_Prompts)
bpy.utils.register_class(PROMPTS_Hanging_Rod_With_Shelves_Prompts)
bpy.utils.register_class(PROMPTS_Bridge_Shelf_Prompts)
