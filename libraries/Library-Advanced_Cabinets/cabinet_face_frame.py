'''
Created on Sep 26, 2016

@author: Andrew
'''

from mv import fd_types, unit
from os import path

HARDWOOD = path.join(path.dirname(__file__),"Cabinet Assemblies","Face Frames","Hardwood.blend")

class Face_Frame(fd_types.Assembly):
    
    type_assembly = "NONE"
    
    def draw(self):    
        self.create_assembly()
        
        self.add_tab(name='Blind Corner Options',tab_type='VISIBLE')
        self.add_prompt(name="Top Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
        self.add_prompt(name="Bottom Rail Width",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)
        self.add_prompt(name="Left Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
        self.add_prompt(name="Right Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
        
        dim_x = self.get_var('dim_x')
        dim_y = self.get_var('dim_y')
        dim_z = self.get_var('dim_z')
        Top_Rail_Width = self.get_var("Top Rail Width")
        Bottom_Rail_Width = self.get_var("Bottom Rail Width")
        Left_Stile_Width = self.get_var("Left Stile Width")
        Right_Stile_Width = self.get_var("Right Stile Width")
        
        top = self.add_assembly(HARDWOOD)
        top.set_name("Top Rail")
        top.x_loc('Left_Stile_Width',[Left_Stile_Width])
        top.y_loc(value = 0)
        top.z_loc('dim_z',[dim_z])
        top.x_rot(value = -90)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.x_dim('dim_x-Left_Stile_Width-Right_Stile_Width',[dim_x,Left_Stile_Width,Right_Stile_Width])
        top.y_dim('Top_Rail_Width',[Top_Rail_Width])
        top.z_dim('dim_y',[dim_y])
        top.material('Exposed_Exterior_Surface')
        top.solid_stock("Hardwood")

        bottom = self.add_assembly(HARDWOOD)
        bottom.set_name("Bottom Rail")
        bottom.x_loc('Left_Stile_Width',[Left_Stile_Width])
        bottom.y_loc(value = 0)
        bottom.z_loc('Bottom_Rail_Width',[Bottom_Rail_Width])
        bottom.x_rot(value = -90)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 0)
        bottom.x_dim('dim_x-Left_Stile_Width-Right_Stile_Width',[dim_x,Left_Stile_Width,Right_Stile_Width])
        bottom.y_dim('Bottom_Rail_Width',[Bottom_Rail_Width])
        bottom.z_dim('dim_y',[dim_y])
        bottom.material('Exposed_Exterior_Surface')
        bottom.solid_stock("Hardwood")
        
        left = self.add_assembly(HARDWOOD)
        left.set_name("Left Stile")
        left.x_loc(value = 0)
        left.y_loc(value = 0)
        left.z_loc(value = 0)
        left.x_rot(value = -90)
        left.y_rot(value = -90)
        left.z_rot(value = 0)
        left.x_dim('dim_z',[dim_z])
        left.y_dim('Left_Stile_Width',[Left_Stile_Width])
        left.z_dim('dim_y',[dim_y])
        left.material('Exposed_Exterior_Surface')       
        left.solid_stock("Hardwood") 
        
        right = self.add_assembly(HARDWOOD)
        right.set_name("Right Stile")
        right.x_loc('dim_x-Right_Stile_Width',[dim_x,Right_Stile_Width])
        right.y_loc(value = 0)
        right.z_loc(value = 0)
        right.x_rot(value = -90)
        right.y_rot(value = -90)
        right.z_rot(value = 0)
        right.x_dim('dim_z',[dim_z])
        right.y_dim('Right_Stile_Width',[Right_Stile_Width])
        right.z_dim('dim_y',[dim_y])
        right.material('Exposed_Exterior_Surface')
        right.solid_stock("Hardwood") 
        
        self.update()