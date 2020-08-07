import bpy
import os
import math
from mv import unit, fd_types, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts

class Pants_Rack(fd_types.Assembly):
    
    insert_type = "Interior"
    placement_type = "INTERIOR"
    type_assembly = "PRODUCT"
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".single_pants_racks"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.lm_closets.is_accessory_bp = True

        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')

        pants_rack = common_parts.add_sliding_pants_rack(self)
        pants_rack.x_loc(value = 0)
        pants_rack.y_loc('Depth',[Depth])
        pants_rack.z_loc(value = 0)
        pants_rack.x_rot(value = 0)
        pants_rack.y_rot(value = 0)
        pants_rack.z_rot(value = 0)
        pants_rack.x_dim('Width',[Width])
        pants_rack.y_dim('-Depth',[Depth])
        pants_rack.z_dim(value = 0)
        
        self.update()

class Single_Pull_Out_Hamper(fd_types.Assembly):
    
    insert_type = "Interior"
    placement_type = "INTERIOR"
    type_assembly = "PRODUCT"
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".single_hamper"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.lm_closets.is_accessory_bp = True

        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')

        pants_rack = common_parts.add_single_pull_out_canvas_hamper(self)
        pants_rack.x_loc(value = 0)
        pants_rack.y_loc('Depth',[Depth])
        pants_rack.z_loc(value = 0)
        pants_rack.x_rot(value = 0)
        pants_rack.y_rot(value = 0)
        pants_rack.z_rot(value = 0)
        pants_rack.x_dim('Width',[Width])
        pants_rack.y_dim('-Depth',[Depth])
        pants_rack.z_dim(value = 0)
        
        self.update()

class Double_Pull_Out_Hamper(fd_types.Assembly):
    
    insert_type = "Interior"
    placement_type = "INTERIOR"
    type_assembly = "PRODUCT"
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".single_hamper"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.lm_closets.is_accessory_bp = True

        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')

        pants_rack = common_parts.add_double_pull_out_canvas_hamper(self)
        pants_rack.x_loc(value = 0)
        pants_rack.y_loc('Depth',[Depth])
        pants_rack.z_loc(value = 0)
        pants_rack.x_rot(value = 0)
        pants_rack.y_rot(value = 0)
        pants_rack.z_rot(value = 0)
        pants_rack.x_dim('Width',[Width])
        pants_rack.y_dim('-Depth',[Depth])
        pants_rack.z_dim(value = 0)
        
        self.update()

class Wire_Basket(fd_types.Assembly):
    
    insert_type = "Interior"
    placement_type = "INTERIOR"
    type_assembly = "INSERT"
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".wire_baskets"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    max_qty = 6
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.lm_closets.is_accessory_bp = True

        self.add_tab(name='Wire Basket Options',tab_type='VISIBLE')
        
        for i in range(1,self.max_qty):
            
            self.add_prompt(name="Basket Height " + str(i),
                            prompt_type='DISTANCE',
                            value=unit.inch(6),
                            tab_index=0)
                             
        self.add_prompt(name="Distance Between Baskets",
                        prompt_type='DISTANCE',
                        value=unit.inch(3),
                        tab_index=0)
        
        self.add_prompt(name="Baskets Qty",
                        prompt_type='QUANTITY',
                        value=1,
                        tab_index=0)            
            
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Distance_Between_Baskets = self.get_var('Distance Between Baskets')
        Baskets_Qty = self.get_var('Baskets Qty')
        
        prev_basket = None
        
        for i in range(1,self.max_qty):
            Basket_Height = self.get_var('Basket Height ' + str(i),'Basket_Height')
            
            wire_basket = common_parts.add_wire_basket(self)
            wire_basket.x_loc(value = 0)
            wire_basket.y_loc(value = 0)
            if prev_basket:
                basket_loc = prev_basket.get_var('loc_z','basket_loc')
                basket_height = prev_basket.get_var('dim_z','basket_height')
                wire_basket.z_loc('basket_loc+basket_height+Distance_Between_Baskets',[basket_loc,basket_height,Distance_Between_Baskets])
            else:
                wire_basket.z_loc(value = 0)
            wire_basket.x_rot(value = 0)
            wire_basket.y_rot(value = 0)
            wire_basket.z_rot(value = 0)
            wire_basket.x_dim('Width',[Width])
            wire_basket.y_dim('Depth',[Depth])
            wire_basket.z_dim('Basket_Height',[Basket_Height])
            wire_basket.prompt('Hide','IF(Baskets_Qty>=' + str(i) + ',False,True)',[Baskets_Qty])
            
            prev_basket = wire_basket
        
        self.update()
        
class Hanging_Rod(fd_types.Assembly):
    
    type_assembly = 'PRODUCT'
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".single_hanging_rod_prompts"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    hanging_rod_qty = 1
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.lm_closets.is_accessory_bp = True
        props = props_closet.get_scene_props().closet_defaults
        
        self.add_tab(name='Hanging Options',tab_type='VISIBLE')
        self.add_prompt(name="Setback from Rear",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Hanging Rod Location From Top",prompt_type='DISTANCE',value=unit.inch(2.145),tab_index=0)
        self.add_prompt(name="Hanging Rod Setback",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
        self.add_prompt(name="Add Hanging Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)   
        self.add_prompt(name="Hanging Rod Deduction",prompt_type='DISTANCE',value=unit.inch(.375),tab_index=0)
        self.add_prompt(name="Turn Off Hangers",prompt_type='CHECKBOX',value=props.hide_hangers,tab_index=0)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Setback_from_Rear = self.get_var("Setback from Rear")
        Hanging_Rod_Setback = self.get_var("Hanging Rod Setback")
        Turn_Off_Hangers = self.get_var("Turn Off Hangers")
        Hanging_Rod_Deduction = self.get_var("Hanging Rod Deduction")
        
        rod = common_parts.add_oval_hanging_rod(self)
        rod.x_loc('Hanging_Rod_Deduction/2',[Hanging_Rod_Deduction])
        rod.y_loc('IF(Setback_from_Rear,Depth-Hanging_Rod_Setback,Hanging_Rod_Setback)',[Setback_from_Rear,Depth,Hanging_Rod_Setback])
        rod.z_loc(value = 0)
        rod.x_rot(value = 0)
        rod.y_rot(value = 0)
        rod.z_rot(value = 0)
        rod.x_dim('Width-Hanging_Rod_Deduction',[Width,Hanging_Rod_Deduction])
        rod.y_dim('-Depth',[Depth])
        rod.z_dim(value = 0)
        
        hangers = common_parts.add_hangers(self)
        hangers.x_loc(value = 0)
        hangers.y_loc('IF(Setback_from_Rear,Depth-Hanging_Rod_Setback,Hanging_Rod_Setback)',[Setback_from_Rear,Depth,Hanging_Rod_Setback])
        hangers.z_loc(value = 0)
        hangers.x_rot(value = 0)
        hangers.y_rot(value = 0)
        hangers.z_rot(value = 0)
        hangers.x_dim('Width',[Width])
        hangers.y_dim('-Depth',[Depth])
        hangers.z_dim(value = 0)
        hangers.prompt("Hide",'Turn_Off_Hangers',[Turn_Off_Hangers]) 
        hangers.prompt("Quantity",value=3)              
        
        self.update()

class Shelf(fd_types.Assembly):
    
    type_assembly = 'INSERT'
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".shelf"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    hanging_rod_qty = 1
    
    def draw(self):
        self.create_assembly()

        self.add_tab(name='Shelf Options',tab_type='VISIBLE')
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        self.add_prompt(name="Shelf Type",prompt_type='COMBOBOX',items=['Adjustable','Fixed','Sliding'],value=0,tab_index=0)
        self.add_prompt(name="Drawer Slide Gap",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Shelf Spacing",prompt_type='DISTANCE',value=unit.inch(6),tab_index=0)
        
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Shelf_Type = self.get_var('Shelf Type')
        Drawer_Slide_Gap = self.get_var('Drawer Slide Gap')
        Shelf_Quantity = self.get_var('Shelf Quantity')
        Shelf_Spacing = self.get_var('Shelf Spacing')

        shelf = common_parts.add_shelf(self)

        Is_Locked_Shelf = shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = shelf.get_var('Adj Shelf Clip Gap')
        
        shelf.x_loc('IF(Shelf_Type==2,Drawer_Slide_Gap,IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap))',[Shelf_Type,Drawer_Slide_Gap,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        shelf.y_loc('Depth',[Depth])
        shelf.z_loc(value = 0)
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 0)
        shelf.x_dim('Width-IF(Shelf_Type==2,Drawer_Slide_Gap*2,IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2))',[Width,Shelf_Type,Drawer_Slide_Gap,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',[Depth,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
        shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Is Locked Shelf','IF(Shelf_Type==1,True,False)',[Shelf_Type])
        shelf.prompt('Z Quantity','Shelf_Quantity',[Shelf_Quantity])
        shelf.prompt('Z Offset','Shelf_Spacing',[Shelf_Spacing])
        shelf.prompt('Hide','IF(Shelf_Type==2,True,False)',[Shelf_Type])
        
        sliding_shelf = common_parts.add_sliding_shelf(self)
        sliding_shelf.x_loc('IF(Shelf_Type==2,Drawer_Slide_Gap,IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap))',[Shelf_Type,Drawer_Slide_Gap,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        sliding_shelf.y_loc('Depth',[Depth])
        sliding_shelf.z_loc(value = 0)
        sliding_shelf.x_rot(value = 0)
        sliding_shelf.y_rot(value = 0)
        sliding_shelf.z_rot(value = 0)
        sliding_shelf.x_dim('Width-IF(Shelf_Type==2,Drawer_Slide_Gap*2,IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2))',[Width,Shelf_Type,Drawer_Slide_Gap,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        sliding_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',[Depth,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
        sliding_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        sliding_shelf.prompt('Is Locked Shelf','IF(Shelf_Type==1,True,False)',[Shelf_Type])
        sliding_shelf.prompt('Z Quantity','Shelf_Quantity',[Shelf_Quantity])
        sliding_shelf.prompt('Z Offset','Shelf_Spacing',[Shelf_Spacing])        
        sliding_shelf.prompt('Hide','IF(Shelf_Type==2,False,True)',[Shelf_Type])
        
        self.update()

class Tray(fd_types.Assembly):
    
    type_assembly = 'INSERT'
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".tray"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    hanging_rod_qty = 1
    
    def draw(self):
        self.create_assembly()

        self.add_tab(name='Tray Options',tab_type='VISIBLE')
        self.add_prompt(name="Tray Height",prompt_type='DISTANCE',value=unit.inch(3),tab_index=0)
        self.add_prompt(name="Drawer Slide Gap",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Tray_Height = self.get_var('Tray Height')
        Drawer_Slide_Gap = self.get_var('Drawer Slide Gap')

        tray = common_parts.add_drawer(self)
        tray.x_loc('Drawer_Slide_Gap',[Drawer_Slide_Gap])
        tray.y_loc(value = 0)
        tray.z_loc(value = 0)
        tray.x_rot(value = 0)
        tray.y_rot(value = 0)
        tray.z_rot(value = 0)
        tray.x_dim('Width-Drawer_Slide_Gap*2',[Width,Drawer_Slide_Gap])
        tray.y_dim('Depth',[Depth])
        tray.z_dim('Tray_Height',[Tray_Height])
        
        self.update()

class Accessory(fd_types.Assembly):

    type_assembly = "PRODUCT"

    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_panel_accessory_x"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessory"
    
    accessory_name = ""
    object_path = ""
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.lm_closets.is_accessory_bp = True
        
        accessory = self.add_object(self.object_path)
        accessory.set_name(self.accessory_name)
        accessory.x_loc(value = unit.inch(12))
        accessory.y_loc(value = 0)
        accessory.z_loc(value = 0)
        accessory.x_rot(value = 0)
        accessory.y_rot(value = 0)
        accessory.z_rot(value = 0)
        accessory.material("Chrome")

class Slanted_Shoe_Shelves(fd_types.Assembly):
    
    property_id = props_closet.LIBRARY_NAME_SPACE + ".shoe_shelf_prompt"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    # placement_type = "INTERIOR"
    type_assembly = "INSERT"
    mirror_y = False
    
    def add_shoe_shelf_prompts(self):
        defaults = props_closet.get_scene_props().closet_defaults
        
        self.add_tab(name='Slanted Shoe Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')

        self.add_prompt(name="Shelf Lip Type",
                        prompt_type='COMBOBOX',
                        items=["Wood Toe","Deco 1","Deco 2","Deco 3",'Steel Fence'],
                        value=0,
                        tab_index=1)
        
        self.add_prompt(name="Adj Shelf Qty",
                        prompt_type='QUANTITY',
                        value=1,
                        tab_index=0)

        self.add_prompt(name="Shelf Clip Gap",
                        prompt_type='DISTANCE',
                        value=defaults.adj_shelf_clip_gap,
                        tab_index=0)

        self.add_prompt(name="Shelf Angle",
                        prompt_type='ANGLE',
                        value=math.radians(17.25),
                        tab_index=0)
        
        self.add_prompt(name="Space From Bottom",
                        prompt_type='DISTANCE',
                        value=unit.inch(3.5),
                        tab_index=0)
        
        self.add_prompt(name="Space From Top",
                        prompt_type='DISTANCE',
                        value=unit.inch(8),
                        tab_index=0)
        
        self.add_prompt(name="Shelf Lip Width",
                        prompt_type='DISTANCE',
                        value=defaults.shelf_lip_width,
                        tab_index=0)
        
        self.add_prompt(name="Distance Between Shelves",
                        prompt_type='DISTANCE',
                        value=unit.inch(8),
                        tab_index=0)
        
        self.add_prompt(name="Adj Shelf Setback",
                        prompt_type='DISTANCE',
                        value=unit.inch(1),
                        tab_index=0)
        
        self.add_prompt(name="Adjustable Shelf Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
        
        Shelf_Lip_Type = self.get_var("Shelf Lip Type")
        
        self.prompt('Adj Shelf Setback','IF(Shelf_Lip_Type==4,0,INCH(.75))',[Shelf_Lip_Type])
        
    def draw_shoe_shelves(self):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Adj_Shelf_Qty = self.get_var("Adj Shelf Qty")
        Adj_Shelf_Setback = self.get_var("Adj Shelf Setback")
        Adjustable_Shelf_Thickness = self.get_var("Adjustable Shelf Thickness")
        Shelf_Clip_Gap = self.get_var("Shelf Clip Gap")
        Shelf_Angle = self.get_var("Shelf Angle")
        Shelf_Lip_Type = self.get_var("Shelf Lip Type")
        Space_From_Bottom = self.get_var("Space From Bottom")
        Distance_Between_Shelves = self.get_var("Distance Between Shelves")
        Shelf_Lip_Width = self.get_var("Shelf Lip Width")
        
        for i in range(1,11):
            adj_shelf = common_parts.add_slanted_shoe_shelf(self)
            adj_shelf.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            adj_shelf.y_loc('Depth',[Depth])
            if i == 1:
                adj_shelf.z_loc('Space_From_Bottom',[Space_From_Bottom])
            else:
                adj_shelf.z_loc('Space_From_Bottom+(Distance_Between_Shelves*' + str(i - 1) + ')',[Space_From_Bottom,Adjustable_Shelf_Thickness,Distance_Between_Shelves])
            adj_shelf.x_rot('Shelf_Angle',[Shelf_Angle])
            adj_shelf.y_rot(value = 0)
            adj_shelf.z_rot(value = 0)
            adj_shelf.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            adj_shelf.y_dim('-Depth+Adj_Shelf_Setback',[Depth,Adj_Shelf_Setback])
            adj_shelf.z_dim('Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            adj_shelf.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,False)',[Adj_Shelf_Qty])
            
            Z_Loc = adj_shelf.get_var('loc_z','Z_Loc')
            Shelf_Depth = adj_shelf.get_var('dim_y','Shelf_Depth')

            shelf_lip = common_parts.add_shelf_lip(self)
            shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            shelf_lip.y_rot(value = 0)
            shelf_lip.z_rot(value = 0)
            shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==0,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])
            
            deco_1_shelf_lip = common_parts.add_deco_shelf_lip_1(self)
            deco_1_shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            deco_1_shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            deco_1_shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            deco_1_shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            deco_1_shelf_lip.y_rot(value = 0)
            deco_1_shelf_lip.z_rot(value = 0)
            deco_1_shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            deco_1_shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            deco_1_shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            deco_1_shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==1,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])

            deco_2_shelf_lip = common_parts.add_deco_shelf_lip_2(self)
            deco_2_shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            deco_2_shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            deco_2_shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            deco_2_shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            deco_2_shelf_lip.y_rot(value = 0)
            deco_2_shelf_lip.z_rot(value = 0)
            deco_2_shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            deco_2_shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            deco_2_shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            deco_2_shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==2,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])
            
            deco_3_shelf_lip = common_parts.add_deco_shelf_lip_3(self)
            deco_3_shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            deco_3_shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            deco_3_shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            deco_3_shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            deco_3_shelf_lip.y_rot(value = 0)
            deco_3_shelf_lip.z_rot(value = 0)
            deco_3_shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            deco_3_shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            deco_3_shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            deco_3_shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==3,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])      
            
            steel_fence = common_parts.add_shelf_fence(self)
            steel_fence.x_loc('Shelf_Clip_Gap+INCH(1)',[Shelf_Clip_Gap])
            steel_fence.y_loc('fabs(Depth)-(fabs(Shelf_Depth+INCH(1))*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            steel_fence.z_loc('Z_Loc-(fabs(Shelf_Depth+INCH(1))*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            steel_fence.x_rot('Shelf_Angle+radians(90)',[Shelf_Angle])
            steel_fence.y_rot(value = 0)
            steel_fence.z_rot(value = 0)
            steel_fence.x_dim('Width-(Shelf_Clip_Gap*2)-INCH(2)',[Width,Shelf_Clip_Gap])
            steel_fence.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            steel_fence.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            steel_fence.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==4,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])
            
    def draw(self):
        self.create_assembly()
        
        self.add_shoe_shelf_prompts()
        self.draw_shoe_shelves()
        
        self.update()
        
#----------PROMPTS PAGES
class PROMPTS_Single_Hanging_Rod_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".single_hanging_rod_prompts"
    bl_label = "Single Hanging Rod Prompts" 
    bl_description = "This shows all of the available door options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                
                hangers = self.assembly.get_prompt("Turn Off Hangers")
                setback_from_rear = self.assembly.get_prompt("Setback from Rear")
                setback_amount = self.assembly.get_prompt("Hanging Rod Setback")
                
                box = layout.box()
                row = box.row()
                row.label("Set Offset from Back")
                row.prop(setback_from_rear,setback_from_rear.prompt_type,text="")   
                row = box.row()
                row.label("Setback Amount")
                row.prop(setback_amount,setback_amount.prompt_type,text="")                                  
                row = box.row()
                row.label(hangers.name)
                row.prop(hangers,hangers.prompt_type,text="")
                row = box.row()
                row.prop(self.assembly.obj_bp,'location',index=2,text="Height")

class PROMPTS_Pants_Rack_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".single_pants_racks"
    bl_label = "Pants Rack Prompts" 
    bl_description = "This shows all of the available pants rack options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
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
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                row = layout.row()
                row.label("Pants Rack Location")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")

class PROMPTS_Accessory_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".accessory"
    bl_label = "Accessory Prompts" 
    bl_description = "This shows all of the available accessory options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
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
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                row = layout.row()
                row.label("Accessory Location")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")

class PROMPTS_Single_Hamper_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".single_hamper"
    bl_label = "Single Hamper Prompts" 
    bl_description = "This shows all of the available hamper options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
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
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                row = layout.row()
                row.label("Hamper Location")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")

class PROMPTS_Shelf_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".shelf"
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
                row = layout.row()
                row.label("Shelf Location")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")
                shelf_type = self.assembly.get_prompt("Shelf Type")
                shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
                shelf_spacing = self.assembly.get_prompt("Shelf Spacing")
                
                row = layout.row()
                shelf_type.draw_prompt(row)

                row = layout.row()
                shelf_quantity.draw_prompt(row)
                
                row = layout.row()
                shelf_spacing.draw_prompt(row)     
                
class PROMPTS_Tray_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".tray"
    bl_label = "Tray Prompts" 
    bl_description = "This shows all of the available tray options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    tray = None
    
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
        self.tray = fd_types.Assembly(obj_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                row = layout.row()
                row.label("Tray Location")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")
                tray_height = self.assembly.get_prompt("Tray Height")
                row = layout.row()
                tray_height.draw_prompt(row)

class PROMPTS_Wire_Baskets_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".wire_baskets"
    bl_label = "Wire Baskets Prompts" 
    bl_description = "This shows all of the available wire_basket options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
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
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                basket_qty = self.assembly.get_prompt("Baskets Qty")
                box = layout.box()
                basket_qty.draw_prompt(box)
                
                for i in reversed(range(1,6)):
                    if basket_qty.value() >= i:
                        basket_height = self.assembly.get_prompt("Basket Height " + str(i))
                        basket_height.draw_prompt(box)
                    
                dist_between_baskets = self.assembly.get_prompt("Distance Between Baskets")
                dist_between_baskets.draw_prompt(box)
                
                row = box.row()
                row.label("Basket Location")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")

class PROMPTS_Shoe_Shelf_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".shoe_shelf_prompt"
    bl_label = "Shoe Shelf Prompts" 
    bl_description = "This shows all of the available shoe shelf options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    shelf_qty = bpy.props.IntProperty(name="Shelf Quantity",min=1,max=10)

    adj_shelf_qty_prompt = None

    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        utils.run_calculators(self.assembly.obj_bp)
        
        if self.adj_shelf_qty_prompt:
            self.adj_shelf_qty_prompt.set_value(self.shelf_qty)
            
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        
        return True
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        
        self.adj_shelf_qty_prompt = self.assembly.get_prompt("Adj Shelf Qty")

        if self.adj_shelf_qty_prompt:
            self.shelf_qty = self.adj_shelf_qty_prompt.value()

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                
                if self.adj_shelf_qty_prompt:
                    shelf_lip_type = self.assembly.get_prompt("Shelf Lip Type")
                    dist_between_shelves = self.assembly.get_prompt("Distance Between Shelves")

                    box = layout.box()
                    row = box.row()
                    row.label("Adjustable Shelf Options:")
                    
                    row = box.row()
                    shelf_lip_type.draw_prompt(row)

                    row = box.row()
                    row.label("Shelf Quantity")
                    row.prop(self,'shelf_qty',text="")
                    
                    row = box.row()
                    row.label("Shoe Shelf Location")
                    row.prop(self.assembly.obj_bp,'location',index=2)

                    row = box.row()
                    dist_between_shelves.draw_prompt(row)                        

#----------DROP OPERATORS
class OPERATOR_Drop_Single_Part(bpy.types.Operator):
    """ This will be called when you drop a hanging rod into the scene
    """
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    bl_label = "Place Single Part"
    bl_description = "This will allow the user to place a hanging rod into the scene"

    object_name = bpy.props.StringProperty(name="Object Name")

    product_name = bpy.props.StringProperty(name="Product Name")
    category_name = bpy.props.StringProperty(name="Category Name")
    library_name = bpy.props.StringProperty(name="Library Name")
    filepath = bpy.props.StringProperty(name="Filepath") #MAYBE DONT NEED THIS?

    insert = None
    default_z_loc = 0.0
    default_height = 0.0
    default_depth = 0.0
    
    openings = []
    objects = []
    
    header_text = "Place In Closet Section   (Esc, Right Click) = Cancel Command  :  (Left Click) = Place Hanging Rod"
    
    def execute(self, context):
        return {'FINISHED'}

    def __del__(self):
        bpy.context.area.header_text_set()

    def invoke(self,context,event):
        bp = bpy.data.objects[self.object_name]
        self.insert = fd_types.Assembly(bp)
        context.window.cursor_set('WAIT')
        self.set_wire_and_xray(self.insert.obj_bp, True)
        self.show_openings()
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def set_wire_and_xray(self,obj,turn_on):
        if turn_on:
            obj.draw_type = 'WIRE'
        else:
            obj.draw_type = 'TEXTURED'
        obj.show_x_ray = turn_on
        for child in obj.children:
            self.set_wire_and_xray(child,turn_on)

    def cancel_drop(self,context,event):
        if self.insert:
            utils.delete_object_and_children(self.insert.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def show_openings(self):
        insert_type = self.insert.obj_bp.mv.placement_type
        for obj in  bpy.context.scene.objects:
            if obj.layers[0]: #Make sure wall is not hidden
                props = props_closet.get_object_props(obj)
                if props.opening_type == 'SECTION':
                    opening = fd_types.Assembly(obj)
                    cage = opening.get_cage()
                    opening.obj_x.hide = True
                    opening.obj_y.hide = True
                    opening.obj_z.hide = True
                    cage.hide_select = False
                    cage.hide = False
                    self.objects.append(cage)

    def get_32mm_position(self,selected_point):
        number_of_holes =  math.floor((selected_point / unit.millimeter(32)))
        return number_of_holes * unit.millimeter(32)

    def selected_opening(self,selected_obj,selected_point):
        '''
        Gets the Selected Opening and positions the assembly
        '''
        if selected_obj:
            opening = fd_types.Assembly(selected_obj.parent)
            if opening.obj_bp.parent and opening.obj_bp.parent is not self.insert.obj_bp.parent:
                loc_pos = opening.obj_bp.matrix_world.inverted() * selected_point
                self.insert.obj_bp.parent = opening.obj_bp.parent
                self.insert.obj_bp.location = opening.obj_bp.location
                self.insert.obj_bp.location.z = self.get_32mm_position(loc_pos[2]) + opening.obj_bp.location.z
                self.insert.obj_bp.rotation_euler = opening.obj_bp.rotation_euler
                self.insert.obj_x.location.x = opening.obj_x.location.x
                self.insert.obj_y.location.y = opening.obj_y.location.y
                self.insert.obj_z.location.z = 0
                utils.run_calculators(self.insert.obj_bp)
                return opening
            
    def set_opening_name(self,obj,name):
        obj.mv.opening_name = name
        for child in obj.children:
            self.set_opening_name(child, name)
        
    def place_insert(self,opening):
        z_loc = self.insert.obj_bp.location.z
        height = self.insert.obj_z.location.z
        utils.copy_assembly_drivers(opening,self.insert)
        self.insert.obj_bp.driver_remove('location',2)
        self.insert.obj_z.driver_remove('location',2)
        self.insert.obj_bp.location.z = z_loc
        self.insert.obj_z.location.z = height
        
        #DONT ASSIGN PROPERTIES ID's SO USERS CAN ACCESS PROPERTIES FOR INSERTS USED IN CLOSET LIBRARY
        #cabinet_utils.set_property_id(self.insert.obj_bp,opening.obj_bp.mv.property_id)
        self.set_opening_name(self.insert.obj_bp, opening.obj_bp.mv.opening_name)
        
        self.set_wire_and_xray(self.insert.obj_bp, False)
        
        for obj in self.objects:
            obj.hide = True
            obj.hide_render = True
            obj.hide_select = True

    def insert_drop(self,context,event):
        if len(self.objects) == 0:
            bpy.ops.fd_general.error('INVOKE_DEFAULT',message="There are no openings in this scene.")  #@UndefinedVariable
            return self.cancel_drop(context,event)
        else:
            selected_point, selected_obj = utils.get_selection_point(context,event,objects=self.objects)
            bpy.ops.object.select_all(action='DESELECT')
            selected_opening = self.selected_opening(selected_obj,selected_point)
            if selected_opening:
                selected_obj.select = True
                
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
        
        if event.type in {'ESC','RIGHTMOUSE'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.insert_drop(context,event)

class OPERATOR_Place_Panel_Accessory_Y(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_panel_accessory_y"
    bl_label = "Place Panel Accessory Y"
    bl_description = "This allows you to place an accessory object into the scene."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    product = None
    
    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.product = fd_types.Assembly(bp)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def get_rotation(self,obj,prev_rotation):
        rotation = obj.rotation_euler.z + prev_rotation
        if obj.parent:
            return self.get_rotation(obj.parent, rotation)
        else:
            return rotation

    def cancel_drop(self,context,event):
        if self.product:
            utils.delete_object_and_children(self.product.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def accessory_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        selected_assembly = None
        
        self.product.obj_bp.location = selected_point
        self.product.obj_bp.parent = None
        
        if selected_obj:
            wall_bp = utils.get_wall_bp(selected_obj)
            selected_assembly_bp = utils.get_assembly_bp(selected_obj)
            selected_assembly = fd_types.Assembly(selected_assembly_bp)
            
            assembly_props = props_closet.get_object_props(selected_assembly.obj_bp)
            
            if wall_bp:
                self.product.obj_bp.rotation_euler.z = wall_bp.rotation_euler.z
                self.product.obj_bp.rotation_euler.y = 0
                self.product.obj_bp.rotation_euler.x = 0
                
            if selected_assembly and selected_assembly.obj_bp and assembly_props.is_panel_bp:
                
                ass_world_loc = (selected_assembly.obj_bp.matrix_world[0][3],
                                 selected_assembly.obj_bp.matrix_world[1][3],
                                 selected_assembly.obj_bp.matrix_world[2][3])
                
                ass_z_world_loc = (selected_assembly.obj_z.matrix_world[0][3],
                                   selected_assembly.obj_z.matrix_world[1][3],
                                   selected_assembly.obj_z.matrix_world[2][3])                
                
                dist_to_bp = math.fabs(utils.calc_distance(selected_point,ass_world_loc))
                dist_to_z = math.fabs(utils.calc_distance(selected_point,ass_z_world_loc))

                loc_pos = selected_assembly.obj_bp.matrix_world.inverted() * selected_point

                self.product.obj_bp.parent = selected_assembly.obj_bp
                
                self.product.obj_bp.location.x = loc_pos[0]
                
                self.product.obj_bp.location.z = 0
                
                self.product.obj_x.location.x = math.fabs(selected_assembly.obj_y.location.y) #SET DEPTH
                
                if selected_assembly.obj_z.location.z < 0: #LEFT PANEL
                    if dist_to_bp > dist_to_z:#PLACE ON RIGHT SIDE
                        self.product.obj_bp.location.y = selected_assembly.obj_y.location.y
                        self.product.obj_bp.rotation_euler.x = math.radians(90)
                        self.product.obj_bp.rotation_euler.y = math.radians(0)
                        self.product.obj_bp.rotation_euler.z = math.radians(90)   
                        self.product.obj_bp.location.z = selected_assembly.obj_z.location.z                     
                    else:#PLACE ON LEFT SIDE
                        self.product.obj_bp.location.y = 0
                        self.product.obj_bp.rotation_euler.x = math.radians(90)
                        self.product.obj_bp.rotation_euler.y = math.radians(180)
                        self.product.obj_bp.rotation_euler.z = math.radians(90)   
                        self.product.obj_bp.location.z = 0
                else: # CENTER AND RIGHT PANEL
                    if dist_to_bp > dist_to_z:#PLACE ON LEFT SIDE
                        self.product.obj_bp.location.y = 0
                        self.product.obj_bp.rotation_euler.x = math.radians(90)
                        self.product.obj_bp.rotation_euler.y = math.radians(180)
                        self.product.obj_bp.rotation_euler.z = math.radians(90) 
                        self.product.obj_bp.location.z = selected_assembly.obj_z.location.z                       
                    else:#PLACE ON RIGHT SIDE
                        self.product.obj_bp.location.y = selected_assembly.obj_y.location.y
                        self.product.obj_bp.rotation_euler.x = math.radians(90)
                        self.product.obj_bp.rotation_euler.y = math.radians(0)
                        self.product.obj_bp.rotation_euler.z = math.radians(90)
                        self.product.obj_bp.location.z = 0

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            utils.set_wireframe(self.product.obj_bp,False)
            context.scene.objects.active = self.product.obj_bp
            self.product.obj_bp.select = True
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}    
        
        return self.accessory_drop(context,event)
    
class OPERATOR_Place_Panel_Accessory_X(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_panel_accessory_x"
    bl_label = "Place Panel Accessory X"
    bl_description = "This allows you to place an accessory on a panel."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    product = None
    
    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.product = fd_types.Assembly(bp)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def get_rotation(self,obj,prev_rotation):
        rotation = obj.rotation_euler.z + prev_rotation
        if obj.parent:
            return self.get_rotation(obj.parent, rotation)
        else:
            return rotation

    def cancel_drop(self,context,event):
        if self.product:
            utils.delete_object_and_children(self.product.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def accessory_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        selected_assembly = None
        
        self.product.obj_bp.location = selected_point
        self.product.obj_bp.parent = None
        
        if selected_obj:
            wall_bp = utils.get_wall_bp(selected_obj)
            selected_assembly_bp = utils.get_assembly_bp(selected_obj)
            selected_assembly = fd_types.Assembly(selected_assembly_bp)
            
            if selected_assembly.obj_bp:
                assembly_props = props_closet.get_object_props(selected_assembly.obj_bp)
                
                if wall_bp:
                    self.product.obj_bp.rotation_euler.z = wall_bp.rotation_euler.z
                    self.product.obj_bp.rotation_euler.y = 0
                    self.product.obj_bp.rotation_euler.x = 0
                    
                if selected_assembly and selected_assembly.obj_bp and assembly_props.is_panel_bp:
                    
                    ass_world_loc = (selected_assembly.obj_bp.matrix_world[0][3],
                                     selected_assembly.obj_bp.matrix_world[1][3],
                                     selected_assembly.obj_bp.matrix_world[2][3])
                    
                    ass_z_world_loc = (selected_assembly.obj_z.matrix_world[0][3],
                                       selected_assembly.obj_z.matrix_world[1][3],
                                       selected_assembly.obj_z.matrix_world[2][3])                
                    
                    dist_to_bp = math.fabs(utils.calc_distance(selected_point,ass_world_loc))
                    dist_to_z = math.fabs(utils.calc_distance(selected_point,ass_z_world_loc))
    
                    loc_pos = selected_assembly.obj_bp.matrix_world.inverted() * selected_point
    
                    self.product.obj_bp.parent = selected_assembly.obj_bp
                    
                    self.product.obj_bp.location.x = loc_pos[0]
                    
                    self.product.obj_bp.location.z = 0
                    
                    self.product.obj_x.location.x = math.fabs(selected_assembly.obj_y.location.y) #SET DEPTH
                    
                    if selected_assembly.obj_z.location.z < 0: #LEFT PANEL
                        if dist_to_bp > dist_to_z: #PLACE ON RIGHT SIDE
                            self.product.obj_bp.location.y = selected_assembly.obj_y.location.y + unit.inch(12)
                            self.product.obj_bp.rotation_euler.x = math.radians(-90)
                            self.product.obj_bp.rotation_euler.y = math.radians(180)
                            self.product.obj_bp.rotation_euler.z = math.radians(90)   
                            self.product.obj_bp.location.z = selected_assembly.obj_z.location.z                     
                        else: #PLACE ON LEFT SIDE
                            self.product.obj_bp.location.y = selected_assembly.obj_y.location.y + unit.inch(12)
                            self.product.obj_bp.rotation_euler.x = math.radians(90)
                            self.product.obj_bp.rotation_euler.y = math.radians(180)
                            self.product.obj_bp.rotation_euler.z = math.radians(90)   
                            self.product.obj_bp.location.z = 0
                    else: # CENTER AND RIGHT PANEL
                        if dist_to_bp > dist_to_z: #PLACE ON LEFT SIDE
                            self.product.obj_bp.location.y = selected_assembly.obj_y.location.y + unit.inch(12)
                            self.product.obj_bp.rotation_euler.x = math.radians(90)
                            self.product.obj_bp.rotation_euler.y = math.radians(180)
                            self.product.obj_bp.rotation_euler.z = math.radians(90) 
                            self.product.obj_bp.location.z = selected_assembly.obj_z.location.z                       
                        else :#PLACE ON RIGHT SIDE
                            self.product.obj_bp.location.y = selected_assembly.obj_y.location.y + unit.inch(12)
                            self.product.obj_bp.rotation_euler.x = math.radians(-90)
                            self.product.obj_bp.rotation_euler.y = math.radians(180)
                            self.product.obj_bp.rotation_euler.z = math.radians(90)
                            self.product.obj_bp.location.z = 0

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            utils.set_wireframe(self.product.obj_bp,False)
            context.scene.objects.active = self.product.obj_bp
            self.product.obj_bp.select = True
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}    
        
        return self.accessory_drop(context,event)    

bpy.utils.register_class(PROMPTS_Pants_Rack_Prompts)
bpy.utils.register_class(PROMPTS_Single_Hanging_Rod_Prompts)
bpy.utils.register_class(PROMPTS_Single_Hamper_Prompts)
bpy.utils.register_class(PROMPTS_Shelf_Prompts)
bpy.utils.register_class(PROMPTS_Tray_Prompts)
bpy.utils.register_class(PROMPTS_Wire_Baskets_Prompts)
bpy.utils.register_class(PROMPTS_Accessory_Prompts)
bpy.utils.register_class(PROMPTS_Shoe_Shelf_Prompts)
bpy.utils.register_class(OPERATOR_Drop_Single_Part)
bpy.utils.register_class(OPERATOR_Place_Panel_Accessory_Y)
bpy.utils.register_class(OPERATOR_Place_Panel_Accessory_X)