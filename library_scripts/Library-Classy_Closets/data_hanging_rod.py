'''
TODO: This is the start of a script that will break out the hanging rod and the hanging rod cups
      Still need to include interface to select the style of cup and the style of rod.
'''

import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts

class Hanging_Rod(fd_types.Assembly):
    
    type_assembly = 'INSERT'
    mirror_y = False
    property_id = props_closet.LIBRARY_NAME_SPACE + ".single_hanging_rod_prompts"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_single_part"
    
    hanging_rod_qty = 1
    
    def draw(self):
        self.create_assembly()
        props = props_closet.get_scene_props().closet_defaults
        
        self.add_tab(name='Hanging Options',tab_type='VISIBLE')
        self.add_prompt(name="Setback from Rear",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Hanging Rod Location From Top",prompt_type='DISTANCE',value=unit.inch(2.145),tab_index=0)
        self.add_prompt(name="Hanging Rod Setback",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
        self.add_prompt(name="Hanging Rod Deduction",prompt_type='DISTANCE',value=unit.inch(.375),tab_index=0)
        self.add_prompt(name="Add Hanging Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)   
        self.add_prompt(name="Turn Off Hangers",prompt_type='CHECKBOX',value=props.hide_hangers,tab_index=0)
        self.add_prompt(name="Shelf Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Setback_from_Rear = self.get_var("Setback from Rear")
        Hanging_Rod_Setback = self.get_var("Hanging Rod Setback")
        Turn_Off_Hangers = self.get_var("Turn Off Hangers")
        Hanging_Rod_Deduction = self.get_var("Hanging Rod Deduction")
        Add_Rod_Setback = self.get_prompt("Add Hanging Setback")
        
        rod = common_parts.add_hanging_rod(self)
        rod.x_loc('Hanging_Rod_Deduction/2',[Hanging_Rod_Deduction])
        rod.y_loc('IF(Setback_from_Rear,Depth-Hanging_Rod_Setback,Hanging_Rod_Setback)',[Setback_from_Rear,Depth,Hanging_Rod_Setback])
        rod.z_loc(value = 0)
        rod.x_rot(value = 0)
        rod.y_rot(value = 0)
        rod.z_rot(value = 0)
        rod.x_dim('Width-Hanging_Rod_Deduction',[Width,Hanging_Rod_Deduction])

        left_cup = common_parts.add_hanging_rod_cup(self)
        left_cup.x_loc(value = unit.inch(-.01))
        left_cup.y_loc('IF(Setback_from_Rear,Depth-Hanging_Rod_Setback,Hanging_Rod_Setback)',[Setback_from_Rear,Depth,Hanging_Rod_Setback])
        left_cup.z_loc(value = 0)
        left_cup.x_rot(value = 90)
        left_cup.y_rot(value = 0)
        left_cup.z_rot(value = 90)
        
        right_cup = common_parts.add_hanging_rod_cup(self)
        right_cup.x_loc('Width+INCH(.01)',[Width])
        right_cup.y_loc('IF(Setback_from_Rear,Depth-Hanging_Rod_Setback,Hanging_Rod_Setback)',[Setback_from_Rear,Depth,Hanging_Rod_Setback])
        right_cup.z_loc(value = 0)
        right_cup.x_rot(value = 90)
        right_cup.y_rot(value = 0)
        right_cup.z_rot(value = -90)
        
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
        
        