"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import bpy
import os
from mv import fd_types, unit

APPLIANCE_PATH = os.path.join(os.path.dirname(__file__),"Appliances")

class Parametric_Built_In_Appliance_FF(fd_types.Assembly):
    
    library_name = "Cabinet Appliances"
    placement_type = "EXTERIOR"
    type_assembly = "INSERT"
    
    # Name of the appliance in the assembly library
    appliance_name = ""
    
    # Size of the built in appliance so it can center in the opening
    appliance_width = 0
    appliance_height = 0
    
    def draw(self):
        self.create_assembly()
        #INHERITED
        self.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=0,tab_index=1)
        
        Width = self.get_var("dim_x","Width")
        Height = self.get_var("dim_z","Height")
        Frame_Left_Gap = self.get_var("Frame Left Gap")
        Frame_Right_Gap = self.get_var("Frame Right Gap")
        
        appliance = self.add_assembly(os.path.join(APPLIANCE_PATH,self.appliance_name+".blend"))
        appliance.x_dim('Width-(Frame_Left_Gap+Frame_Right_Gap)',[Width,Frame_Left_Gap,Frame_Right_Gap])
        appliance.z_dim('Height',[Height])
        appliance.x_loc('Frame_Left_Gap',[Frame_Left_Gap])
        appliance.y_loc(value = unit.inch(-1))
        appliance.z_loc(value = 0)
        
        self.update()
        
#---------INSERT: PARAMETRIC APPLIANCES        

class INSERT_Microwave_FF(Parametric_Built_In_Appliance_FF):
    
    def __init__(self):
        self.category_name = "Appliances - Parametric"
        self.assembly_name = "Microwave FF"
        self.width = unit.inch(30)
        self.height = unit.inch(14)
        self.depth = unit.inch(12.5)
        self.appliance_name = "Microwave"      
        
class INSERT_Single_Oven_FF(Parametric_Built_In_Appliance_FF):
    
    def __init__(self):
        self.category_name = "Appliances - Parametric"
        self.assembly_name = "Single Oven FF"
        self.width = unit.inch(30)
        self.height = unit.inch(14)
        self.depth = unit.inch(12.5)
        self.appliance_name = "Single Oven"
