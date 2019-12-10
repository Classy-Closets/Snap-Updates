import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

class Hanging_Rods_with_Shelves(fd_types.Assembly):
    
    property_id = ""
    type_assembly = "INSERT"   
    placement_type = "INTERIOR"
    mirror_y = False
    
    def draw(self):
        self.create_assembly()
        
        #ADD PROMPTS
        self.add_tab(name='Hanging Options',tab_type='VISIBLE')
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        
        #GET VARS
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Height = self.get_var('dim_z','Height')    
        Shelf_Quantity = self.get_var('Shelf Quantity')     
        
        #ADD PARTS
        shelf = common_parts.add_shelf(self)
        shelf.x_loc(value = unit.inch(0))
        shelf.y_loc('Depth',[Depth])
        shelf.z_loc('Height/2',[Height])
        shelf.x_dim('Width',[Width])
        shelf.y_dim('-Depth',[Depth])
        shelf.z_dim(value = unit.inch(.75))
        shelf.prompt('Hide','IF(Shelf_Quantity>0,False,True)',[Shelf_Quantity])        
        
        self.update()