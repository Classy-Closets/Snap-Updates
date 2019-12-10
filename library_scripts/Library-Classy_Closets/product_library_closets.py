from mv import unit
from . import common_parts
from . import mv_closet_defaults as props_closet
from . import data_closet_carcass
from . import data_closet_carcass_hutch
from . import data_closet_carcass_island
from . import data_single_parts
from . import data_rods_and_shelves
from . import data_countertop
from . import data_drawers
from . import data_closet_doors
from . import data_ironing_boards
from . import data_deco_fillers
from . import data_hampers
from . import data_closet_carcass_corner
from . import data_applied_panel
from . import data_base_assembly
from . import data_tie_drawer
from . import data_closet_peninsula
from . import data_closet_carcass_upper
from . import data_closet_bench
from . import data_shoe_cubbies
from . import data_closet_hooks_and_pins
from . import data_hanging_rod
from . import data_closet_top
from . import data_fixed_shelf_and_rod
from . import data_closet_splitters
from . import data_classy_closets_hanging_rods
from . import data_closet_top_molding

LIBRARY_NAME = "Closets"

#CLOSET_PRODUCTS_FLOOR = "Closet Products - Floor Panels"
CLOSET_PRODUCTS_ADD_PARDS = "Closet Products - Add Pards"
CLOSET_PRODUCTS_BASIC = "Closet Products - Basic"
CLOSET_PRODUCTS_SHELVES = "Closet Products - Shelves"
CLOSET_PRODUCTS_HUTCH = "Closet Products - Hutch"
CLOSET_PRODUCTS_ISLANDS = "Closet Products - Islands"
CLOSET_PRODUCTS_STACKED = "Closet Products - Uppers"


CLOSET_PARTS_ACCESSORIES = "Parts - Closet Accessories"

SECTION_INSERTS_DIVIDERS = "Section Inserts - Dividers"


#--------CLOSET PRODUCTS FLOOR

#class PRODUCT_1_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 1
        #super().__init__()
        
#class PRODUCT_2_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 2
        #super().__init__()
        
#class PRODUCT_3_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 3
        #super().__init__()                
        
#class PRODUCT_4_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 4
        #super().__init__()
        
#class PRODUCT_5_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 5
        #super().__init__()             
        
#class PRODUCT_6_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 6
        #super().__init__()                     
        
#class PRODUCT_7_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 7
        #super().__init__()              
        
#class PRODUCT_8_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 8
        #super().__init__()                     
        
#class PRODUCT_9_Floor_Opening(data_closet_carcass.Closet_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.opening_qty = 9
        #super().__init__()                  
        
#class PRODUCT_Peninsula_Opening(data_closet_peninsula.Peninsula_Carcass):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.width = unit.inch(24.75)
        #self.depth = unit.inch(23)
        #self.height = unit.inch(83.9375)
        #super().__init__()
        
#class PRODUCT_Closet_Bench(data_closet_bench.Closet_Bench):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.assembly_type = "PRODUCT"
        #self.width = unit.inch(23)
        #self.height = unit.inch(9.625)
        #self.depth = unit.inch(18)
        
#class PRODUCT_L_Shelves(data_closet_carcass_corner.Corner_L_Shelves):
    
    #def __init__(self):
        #props = props_closet.get_scene_props()
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.width = unit.inch(24)
        #self.height = unit.millimeter(float(props.closet_defaults.panel_height))
        #self.depth = unit.inch(24)
        
#class PRODUCT_Diagonal_Shelves(data_closet_carcass_corner.Corner_Angle_Shelves):
    
    #def __init__(self):
        #props = props_closet.get_scene_props()
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.width = unit.inch(24)
        #self.height = unit.millimeter(float(props.closet_defaults.panel_height))
        #self.depth = unit.inch(24)            
          
#class PRODUCT_Radius_Shelves(data_closet_carcass_corner.Corner_Pie_Shelves):
    
    #def __init__(self):
        #props = props_closet.get_scene_props()
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_FLOOR
        #self.width = props.closet_defaults.panel_depth
        #self.height = unit.millimeter(float(props.closet_defaults.panel_height))
        #self.depth = props.closet_defaults.panel_depth        
        
#--------CLOSET PRODUCTS HANGING
        
class PRODUCT_1_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 1
        self.is_hanging = True
        super().__init__()
        
        
class PRODUCT_2_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 2
        self.is_hanging = True 
        super().__init__()
               
        
class PRODUCT_3_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 3
        self.is_hanging = True 
        super().__init__()
               
        
class PRODUCT_4_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 4
        self.is_hanging = True   
        super().__init__()
                  
        
class PRODUCT_5_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 5
        self.is_hanging = True  
        super().__init__()
                     
        
class PRODUCT_6_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 6
        self.is_hanging = True    
        super().__init__()
                 
        
class PRODUCT_7_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 7
        self.is_hanging = True  
        super().__init__()
                     
        
class PRODUCT_8_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 8
        self.is_hanging = True 
        super().__init__()
                   
        
class PRODUCT_9_Hanging_Opening(data_closet_carcass.Closet_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        self.opening_qty = 9
        self.is_hanging = True   
        super().__init__()
                     

        
#class PRODUCT_Fixed_Shelf_and_Rod(data_fixed_shelf_and_rod.Fixed_Shelf_and_Rod):
    
    #def __init__(self):
        #props = props_closet.get_scene_props()
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PRODUCTS_ADD_PARDS
        #self.depth = props.closet_defaults.panel_depth
        #super().__init__()


#--------CLOSET PRODUCTS BASIC

class PRODUCT_Toe_Kick(data_base_assembly.Base_Assembly):
    
    def __init__(self):
        props = props_closet.get_scene_props()
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(18)
        self.height = props.closet_defaults.toe_kick_height
        self.depth = unit.inch(12)

class PRODUCT_Counter_Top(data_countertop.Countertop_Insert):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_countertop"
        self.assembly_type = "PRODUCT"
        self.width = unit.inch(18)
        self.depth = unit.inch(23)  

class PRODUCT_Doors(data_closet_doors.Doors):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(25)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "fd_general.drop_insert"
        self.prompts = {"Door Type":2}
        #DOOR TYPE ONLY USED TO DETERMINE DOOR HEIGHT FOR PLANT ON TOP
        self.door_type = "Upper"

class PRODUCT_Drawers(data_drawers.Drawer_Stack):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(18)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "closets.insert_drawer_drop"        

class PRODUCT_Hamper(data_hampers.Hamper):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(20)
        self.height = unit.inch(34)
        self.depth = unit.inch(16)
        self.drop_id = "fd_general.drop_insert"
        
class PRODUCT_Hang_Double(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(18)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "fd_general.drop_insert"
        self.prompts = {"Add Top Rod":True,
                        "Add Middle Rod":False,
                        "Add Bottom Rod":True,
                        "Add Top Shelf":False,
                        "Add Bottom Shelf":True,
                        "Top Rod Location":unit.millimeter(172.95),
                        "Bottom Rod Location":unit.millimeter(1164.95),
                        "Bottom Shelves Location":unit.millimeter(1164.95),
                        "Add Shelves In Top Section":False,
                        "Add Shelves In Middle Section":False,
                        "Add Shelves In Bottom Section":False,
                        "Top Shelf Quantity":1,
                        "Middle Shelf Quantity":1,
                        "Bottom Shelf Quantity":1} 
        
class PRODUCT_Hang_Double_Tall(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(18)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "fd_general.drop_insert"
        self.prompts = {"Add Top Rod":False,
                        "Add Middle Rod":True,
                        "Add Bottom Rod":True,
                        "Add Top Shelf":True,
                        "Add Bottom Shelf":True,
                        "Top Rod Location":unit.millimeter(300.95),
                        "Bottom Rod Location":unit.millimeter(1388.95),
                        "Bottom Shelves Location":unit.millimeter(1388.95),
                        "Add Shelves In Top Section":False,
                        "Add Shelves In Middle Section":False,
                        "Add Shelves In Bottom Section":False,
                        "Top Shelf Quantity":1,
                        "Middle Shelf Quantity":1,
                        "Bottom Shelf Quantity":1} 

class PRODUCT_Hang_Medium(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(18)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "fd_general.drop_insert"
        self.prompts = {"Add Top Rod":False,
                        "Add Middle Rod":True,
                        "Add Bottom Rod":False,
                        "Add Top Shelf":True,
                        "Add Bottom Shelf":False,
                        "Top Rod Location":unit.millimeter(748.95),
                        "Bottom Rod Location":unit.millimeter(1164.95),
                        "Bottom Shelves Location":unit.millimeter(1164.95),
                        "Add Shelves In Top Section":True,
                        "Add Shelves In Middle Section":False,
                        "Add Shelves In Bottom Section":False,
                        "Top Shelf Quantity":2,
                        "Middle Shelf Quantity":1,
                        "Bottom Shelf Quantity":1}        

class PRODUCT_Hang_Long(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(18)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "fd_general.drop_insert"
        self.prompts = {"Add Top Rod":False,
                        "Add Middle Rod":True,
                        "Add Bottom Rod":False,
                        "Add Top Shelf":True,
                        "Add Bottom Shelf":False,
                        "Top Rod Location":unit.millimeter(300.95),
                        "Bottom Rod Location":unit.millimeter(1164.95),
                        "Bottom Shelves Location":unit.millimeter(1164.95),
                        "Add Shelves In Top Section":False,
                        "Add Shelves In Middle Section":False,
                        "Add Shelves In Bottom Section":False,
                        "Top Shelf Quantity":1,
                        "Middle Shelf Quantity":1,
                        "Bottom Shelf Quantity":1}        
        
class PRODUCT_Corner_Shelves(data_closet_carcass_corner.L_Shelves):
    
    def __init__(self):
        props = props_closet.get_scene_props()
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(24)
        self.height = unit.millimeter(float(props.closet_defaults.panel_height))
        self.depth = unit.inch(24)
        self.prompts = {"Is Hanging":False}

class PRODUCT_Triangle_Shelves(data_closet_carcass_corner.Corner_Triangle_Shelves):
    
    def __init__(self):
        props = props_closet.get_scene_props()
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = props.closet_defaults.panel_depth
        self.height = unit.millimeter(float(props.closet_defaults.panel_height))
        self.depth = props.closet_defaults.panel_depth                                                                        
 
class PRODUCT_Slanted_Shoe_Shelf(data_single_parts.Slanted_Shoe_Shelves):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.assembly_type = "PRODUCT"
        self.width = unit.inch(18)
        self.depth = unit.inch(23) 

class PRODUCT_Top_Shelf(data_closet_top.Top):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)

class PRODUCT_Flat_Crown(data_closet_top_molding.Flat_Crown):
     
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(34)
        self.height = unit.inch(4)
        self.depth = unit.inch(.75)  
        
class PRODUCT_Light_Rail(data_closet_top_molding.Flat_Valance_Full):
     
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(34)
        self.height = unit.inch(4)
        self.depth = unit.inch(.75)      
        
class PRODUCT_Valance(data_closet_top_molding.Flat_Valance_Single):
     
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = unit.inch(34)
        self.height = unit.inch(4)
        self.depth = unit.inch(.75)             
        
                

#--------CLOSET PRODUCTS SHELVES

class PRODUCT_Shelves_Only(data_rods_and_shelves.Shelves_Only):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(18)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "fd_general.drop_insert"

class PRODUCT_Shelves_Glass(data_rods_and_shelves.Glass_Shelves):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(18)
        self.height = unit.inch(50)
        self.depth = unit.inch(14)
        self.drop_id = "fd_general.drop_insert"
        
# class PRODUCT_Shelf(data_single_parts.Shelf):
#     
#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PARTS_CUTPARTS
#         self.assembly_type = "PRODUCT"
#         self.width = unit.inch(18)
#         self.depth = unit.inch(23)  
class PRODUCT_Shelf_1(data_closet_splitters.Vertical_Splitters):  
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 2
        self.drop_id = "fd_general.drop_insert"
        
class PRODUCT_Shelf_2(data_closet_splitters.Vertical_Splitters):  
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 2
        self.drop_id = "fd_general.drop_insert"

class PRODUCT_Shelf_3(data_closet_splitters.Vertical_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 3
        self.drop_id = "fd_general.drop_insert"

class PRODUCT_Shelf_4(data_closet_splitters.Vertical_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 4
        self.drop_id = "fd_general.drop_insert"
        
class PRODUCT_Shelf_5(data_closet_splitters.Vertical_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 5
        self.drop_id = "fd_general.drop_insert"        
        
class PRODUCT_Shelf_6(data_closet_splitters.Vertical_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 6
        self.drop_id = "fd_general.drop_insert"     
        
class PRODUCT_Shelf_7(data_closet_splitters.Vertical_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 7
        self.drop_id = "fd_general.drop_insert"     
        
class PRODUCT_Shelf_8(data_closet_splitters.Vertical_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 8
        self.drop_id = "fd_general.drop_insert"     
        
class PRODUCT_Shelf_9(data_closet_splitters.Vertical_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.vertical_openings = 9
        self.drop_id = "fd_general.drop_insert"     
        
#class PRODUCT_Shelf_10(data_closet_splitters.Vertical_Splitters):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = unit.inch(34)
#         self.height = unit.inch(34)
#         self.depth = unit.inch(12)
#         self.vertical_openings = 10
#         self.drop_id = "fd_general.drop_insert"  

#--------CLOSET PRODUCTS HUTCH
        
class PRODUCT_1_Hutch_Opening(data_closet_carcass_hutch.Hutch):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_HUTCH
        self.opening_qty = 1
        super().__init__()
        
class PRODUCT_2_Hutch_Opening(data_closet_carcass_hutch.Hutch):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_HUTCH
        self.opening_qty = 2
        super().__init__()
        
class PRODUCT_3_Hutch_Opening(data_closet_carcass_hutch.Hutch):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_HUTCH
        self.opening_qty = 3
        super().__init__()
        
class PRODUCT_4_Hutch_Opening(data_closet_carcass_hutch.Hutch):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_HUTCH
        self.opening_qty = 4
        super().__init__()
        
class PRODUCT_5_Hutch_Opening(data_closet_carcass_hutch.Hutch):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_HUTCH
        self.opening_qty = 5
        super().__init__()
        
class PRODUCT_6_Hutch_Opening(data_closet_carcass_hutch.Hutch):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_HUTCH
        self.opening_qty = 6
        super().__init__()
        
#--------CLOSET PRODUCTS UPPERS

class PRODUCT_1_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
     
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 1
        self.height_above_floor = defaults.hanging_height
        super().__init__()
         
class PRODUCT_2_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 2
        self.height_above_floor = defaults.hanging_height
        super().__init__()   
         
class PRODUCT_3_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 3
        self.height_above_floor = defaults.hanging_height
        super().__init__() 
         
class PRODUCT_4_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 4
        self.height_above_floor = defaults.hanging_height
        super().__init__() 
         
class PRODUCT_5_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 5
        self.height_above_floor = defaults.hanging_height
        super().__init__()     
         
class PRODUCT_6_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 6
        self.height_above_floor = defaults.hanging_height
        super().__init__()  
         
class PRODUCT_7_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 7
        self.height_above_floor = defaults.hanging_height
        super().__init__() 
         
class PRODUCT_8_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 8
        self.height_above_floor = defaults.hanging_height
        super().__init__() 
         
class PRODUCT_9_Upper_Opening(data_closet_carcass_upper.Stacked_Carcass):
 
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_STACKED
        self.opening_qty = 9
        self.height_above_floor = defaults.hanging_height
        super().__init__()
        
#---------PARTS - CLOSET ACCESSORIES

class PRODUCT_Belt_Rack(data_closet_hooks_and_pins.Belt_Accessories):
     
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES         
        self.width = unit.inch(12)
        self.depth = unit.inch(1)
        self.height = unit.inch(3)
        
class PRODUCT_Tie_Rack(data_closet_hooks_and_pins.Tie_Accessories):
      
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES         
        self.width = unit.inch(12)
        self.depth = unit.inch(1)
        self.height = unit.inch(3)
 
class PRODUCT_Tie_and_Belt_Rack(data_closet_hooks_and_pins.Tie_and_Belt_Accessories):
      
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES         
        self.width = unit.inch(12)
        self.depth = unit.inch(1)
        self.height = unit.inch(3)        
 
class PRODUCT_Robe_Hooks(data_closet_hooks_and_pins.Robe_Hook_Accessories):
      
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES         
        self.width = unit.inch(4)
        self.depth = unit.inch(1)
        self.height = unit.inch(3) 
         
class PRODUCT_Double_Robe_Hooks(data_closet_hooks_and_pins.Double_Robe_Hook_Accessories):
      
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES         
        self.width = unit.inch(4)
        self.depth = unit.inch(1)
        self.height = unit.inch(3)        
                
class PRODUCT_DORB_Hooks(data_closet_hooks_and_pins.DORB_Hook_Accessories):
      
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES         
        self.width = unit.inch(4)
        self.depth = unit.inch(1)
        self.height = unit.inch(3)                       

class PRODUCT_Coat_and_Hat_Hooks(data_closet_hooks_and_pins.Coat_and_Hat_Hook_Accessories):
      
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES         
        self.width = unit.inch(4)
        self.depth = unit.inch(1)
        self.height = unit.inch(3)
        
class PRODUCT_Hanging_Rod(data_single_parts.Hanging_Rod):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.width = unit.inch(18)
        self.depth = unit.inch(23)
        
        
class PRODUCT_Pants_Rack(data_single_parts.Pants_Rack):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.width = unit.inch(18)
        self.depth = unit.inch(23)


class PRODUCT_Valet_Rod(data_single_parts.Accessory):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.object_path = common_parts.VALET_ROD
        self.accessory_name = "Valet Rod"
        
        
class PRODUCT_Valet_Rod_2(data_single_parts.Accessory):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.object_path = common_parts.VALET_ROD_2
        self.accessory_name = "Valet Rod 2"        


class PRODUCT_Hamper_Single_Pullout_Canvas(data_single_parts.Single_Pull_Out_Hamper):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.width = unit.inch(18)
        self.depth = unit.inch(23)
        
        
class PRODUCT_Hamper_Double_Pullout_Canvas(data_single_parts.Double_Pull_Out_Hamper):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.width = unit.inch(24)
        self.depth = unit.inch(23)

class PRODUCT_Wire_Basket(data_single_parts.Wire_Basket):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.width = unit.inch(18)
        self.depth = unit.inch(23)   
        
class PRODUCT_Metal_Tie_and_Belt_Rack(data_single_parts.Accessory):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.object_path = common_parts.TIE_AND_BELT_RACK
        self.accessory_name = "Metal Tie and Belt Rack"        

#---------PARTS - CLOSET CUTPARTS



#class PRODUCT_Applied_Panel(data_applied_panel.Applied_Panel):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PARTS_CUTPARTS
        #self.assembly_type = "PRODUCT"
        #self.width = unit.inch(18)
        #self.depth = unit.inch(.75)
        #self.height = unit.inch(34)

#class PRODUCT_Pull_Out_Tray(data_single_parts.Tray):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PARTS_CUTPARTS
        #self.assembly_type = "PRODUCT"
        #self.width = unit.inch(18)
        #self.depth = unit.inch(23)

#class PRODUCT_Deco_Filler(data_deco_fillers.Deco_Filler):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = CLOSET_PARTS_CUTPARTS
        #self.width = unit.inch(3)
        #self.height = unit.inch(34)
        #self.depth = unit.inch(1)
        #self.drop_id = "fd_general.drop_insert"

 
#--------ISLAND CLOSETS

class PRODUCT_1_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 1
        self.is_double_sided = False
        super().__init__()

class PRODUCT_2_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 2
        self.is_double_sided = False
        super().__init__()
        
class PRODUCT_3_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 3
        self.is_double_sided = False
        super().__init__()
        
class PRODUCT_4_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 4
        self.is_double_sided = False
        super().__init__()                

class PRODUCT_1_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 1
        self.is_double_sided = True
        super().__init__()

class PRODUCT_2_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 2
        self.is_double_sided = True
        super().__init__()
        
class PRODUCT_3_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 3
        self.is_double_sided = True
        super().__init__()
        
class PRODUCT_4_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 4
        self.is_double_sided = True
        super().__init__()

#--------SECTION INSERTS - SHELVES AND RODS

#class PRODUCT_Classy_Closets_Rods(data_classy_closets_hanging_rods.Hanging_Rods_with_Shelves):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_SHELVES_AND_RODS
        #self.width = unit.inch(18)
        #self.height = unit.inch(50)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"



#class PRODUCT_Long_Hang_2(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_SHELVES_AND_RODS
        #self.width = unit.inch(18)
        #self.height = unit.inch(50)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"
        #self.prompts = {"Add Top Rod":False,
                        #"Add Middle Rod":True,
                        #"Add Bottom Rod":False,
                        #"Add Top Shelf":True,
                        #"Add Bottom Shelf":False,
                        #"Top Shelf Location":unit.millimeter(492.95),
                        #"Bottom Shelf Location":unit.millimeter(76.95),
                        #"Add Shelves In Top Section":True,
                        #"Add Shelves In Middle Section":False,
                        #"Add Shelves In Bottom Section":False,
                        #"Top Shelf Quantity":1,
                        #"Middle Shelf Quantity":1,
                        #"Bottom Shelf Quantity":1}

#class PRODUCT_Long_Hang_3(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_SHELVES_AND_RODS
        #self.width = unit.inch(18)
        #self.height = unit.inch(50)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"
        #self.prompts = {"Add Top Rod":False,
                        #"Add Middle Rod":True,
                        #"Add Bottom Rod":False,
                        #"Add Top Shelf":True,
                        #"Add Bottom Shelf":False,
                        #"Top Shelf Location":unit.millimeter(748.95),
                        #"Bottom Shelf Location":unit.millimeter(76.95),
                        #"Add Shelves In Top Section":True,
                        #"Add Shelves In Middle Section":False,
                        #"Add Shelves In Bottom Section":False,
                        #"Top Shelf Quantity":2,
                        #"Middle Shelf Quantity":1,
                        #"Bottom Shelf Quantity":1}


        
#class PRODUCT_Medium_Hang_2(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_SHELVES_AND_RODS
        #self.width = unit.inch(18)
        #self.height = unit.inch(50)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"
        #self.prompts = {"Add Top Rod":False,
                        #"Add Middle Rod":True,
                        #"Add Bottom Rod":False,
                        #"Add Top Shelf":True,
                        #"Add Bottom Shelf":False,
                        #"Top Shelf Location":unit.millimeter(940.95),
                        #"Bottom Shelf Location":unit.millimeter(76.95),
                        #"Add Shelves In Top Section":True,
                        #"Add Shelves In Middle Section":False,
                        #"Add Shelves In Bottom Section":False,
                        #"Top Shelf Quantity":2,
                        #"Middle Shelf Quantity":1,
                        #"Bottom Shelf Quantity":1}

        

#class PRODUCT_Double_Hang_2(data_rods_and_shelves.Hanging_Rods_with_Shelves):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_SHELVES_AND_RODS
        #self.width = unit.inch(18)
        #self.height = unit.inch(50)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"
        #self.prompts = {"Add Top Rod":True,
                        #"Add Middle Rod":True,
                        #"Add Bottom Rod":False,
                        #"Add Top Shelf":True,
                        #"Add Bottom Shelf":False,
                        #"Top Shelf Location":unit.millimeter(940.95),
                        #"Bottom Shelf Location":unit.millimeter(76.95),
                        #"Add Shelves In Top Section":False,
                        #"Add Shelves In Middle Section":False,
                        #"Add Shelves In Bottom Section":False,
                        #"Top Shelf Quantity":1,
                        #"Middle Shelf Quantity":1,
                        #"Bottom Shelf Quantity":1}

#class PRODUCT_Bridge_Shelves(data_rods_and_shelves.Bridge_Shelves):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_SHELVES_AND_RODS
        #self.width = unit.inch(18)
        #self.height = unit.inch(50)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"

#--------SECTION INSERTS - DOORS AND DRAWERS

#class PRODUCT_Tie_Drawer(data_tie_drawer.Tie_Drawer):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_DOORS_AND_DRAWERS
        #self.width = unit.inch(6)
        #self.height = unit.inch(70)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"

#class PRODUCT_Doors_Base(data_closet_doors.Doors):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_DOORS_AND_DRAWERS
        #self.width = unit.inch(25)
        #self.height = unit.inch(50)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"
        #self.prompts = {"Door Type":0}
        #DOOR TYPE ONLY USED TO DETERMINE DOOR HEIGHT FOR PLANT ON TOP
        #self.door_type = "Base" 

#class PRODUCT_Doors_Tall(data_closet_doors.Doors):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_DOORS_AND_DRAWERS
        #self.width = unit.inch(25)
        #self.height = unit.inch(70)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"
        #self.prompts = {"Door Type":1,
                        #"Fill Opening":True}
        #DOOR TYPE ONLY USED TO DETERMINE DOOR HEIGHT FOR PLANT ON TOP
        #self.door_type = "Tall"

#class PRODUCT_Ironing_Board(data_ironing_boards.Ironing_Board):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_DOORS_AND_DRAWERS
        #self.width = unit.inch(25)
        #self.height = unit.inch(10)
        #self.depth = unit.inch(14)
        #self.drop_id = "fd_general.drop_insert"

#--------Section Inserts - Dividers

       
class PRODUCT_Division_1(data_closet_splitters.Horizontal_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = unit.inch(50)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.horizontal_openings = 2
        self.drop_id = "fd_general.drop_insert"

class PRODUCT_Division_2(data_closet_splitters.Horizontal_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = unit.inch(50)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.horizontal_openings = 3
        self.drop_id = "fd_general.drop_insert"

class PRODUCT_Division_3(data_closet_splitters.Horizontal_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = unit.inch(50)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.horizontal_openings = 4
        self.drop_id = "fd_general.drop_insert"

class PRODUCT_Division_4(data_closet_splitters.Horizontal_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = unit.inch(50)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.horizontal_openings = 5
        self.drop_id = "fd_general.drop_insert"
        
class PRODUCT_Division_5(data_closet_splitters.Horizontal_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = unit.inch(50)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.horizontal_openings = 6
        self.drop_id = "fd_general.drop_insert"
        
class PRODUCT_Division_6(data_closet_splitters.Horizontal_Splitters):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = unit.inch(50)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.horizontal_openings = 7
        self.drop_id = "fd_general.drop_insert"          

#class PRODUCT_Shoe_Cubbies(data_shoe_cubbies.Shoe_Cubbies):
    
    #def __init__(self):
        #self.library_name = LIBRARY_NAME
        #self.category_name = SECTION_INSERTS_DIVIDERS
        #self.width = unit.inch(34)
        #self.height = unit.inch(34)
        #self.depth = unit.inch(12)
        #self.drop_id = "fd_general.drop_insert"

class PRODUCT_Shoe_Cubbies_Divisions(data_shoe_cubbies.Shoe_Cubbies):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = unit.inch(34)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.drop_id = "fd_general.drop_insert"
        self.prompts = {"Divider Thickness":unit.inch(.75)}

