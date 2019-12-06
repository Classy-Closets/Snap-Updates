"""
Microvellum 
Face Frame Library
Stores all the products for the Face Frame Library
"""

import bpy
from mv import unit
from . import face_frame_cabinets as cabinets
from . import carcass_advanced as carcass
from . import face_frame_exteriors as exteriors
from . import cabinet_interiors as interiors
from . import face_frame_splitters as splitters
from . import face_frame_appliances as appliances
from . import cabinet_properties

LIBRARY_NAME = "Cabinets - Face Frame"
BASE_CATEGORY_NAME = "Base Cabinets"
TALL_CATEGORY_NAME = "Tall Cabinets"
UPPER_CATEGORY_NAME = "Upper Cabinets"
OUTSIDE_CORNER_CATEGORY_NAME = "Outside Corner Cabinets"
INSIDE_CORNER_CATEGORY_NAME = "Inside Corner Cabinets"
TRANSITION_CATEGORY_NAME = "Transition Cabinets"
STARTER_CATEGORY_NAME = "Starter Cabinets"
DRAWER_CATEGORY_NAME = "Drawer Cabinets"
BLIND_CORNER_CATEGORY_NAME = "Blind Corner Cabinets"

#---------PRODUCT: BASE CABINETS

class PRODUCT_Microwave_2_Door_Base_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = unit.inch(15)
        self.splitter.exterior_1 = appliances.INSERT_Microwave_FF()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 500

class PRODUCT_Microwave_1_Drawer_Base_FF(cabinets.Face_Frame_Standard): # DRAWER STACK
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = unit.inch(15)
        self.splitter.exterior_1 = appliances.INSERT_Microwave_FF()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 400

class PRODUCT_2_Door_Sink_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.carcass.remove_top = True
        self.exterior = exteriors.INSERT_Base_Double_Door_FF()
        self.interior = None
        self.product_price = 500
        
class PRODUCT_2_Door_with_False_Front_Sink_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = "Base Cabinets"
        self.width = props.width_2_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.carcass.remove_top = True
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_1.add_drawer = False
        self.splitter.exterior_1.add_pull = False
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 550

class PRODUCT_2_Door_2_False_Front_Sink_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = "Base Cabinets"
        self.width = props.width_2_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.carcass.remove_top = True
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_Horizontal_Drawers_FF()
        self.splitter.exterior_1.add_drawer = False
        self.splitter.exterior_1.add_pull = False
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()  
        self.product_price = 550 
        
class PRODUCT_1_Door_Sink_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.carcass.remove_top = True
        self.exterior = exteriors.INSERT_Base_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 380

class PRODUCT_1_Door_Base_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 350

class PRODUCT_2_Door_Base_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 500

class PRODUCT_1_Door_1_Drawer_Base_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.interior_2 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door_FF()
        self.product_price = 450

class PRODUCT_2_Door_2_Drawer_Base_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_Horizontal_Drawers_FF()
        self.splitter.interior_2 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 620

class PRODUCT_2_Door_1_Drawer_Base_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.interior_2 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 580
        
#---------PRODUCT: TALL CABINETS

class PRODUCT_4_Door_Oven_Tall_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_3_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door_FF()
        self.splitter.exterior_2 = appliances.INSERT_Single_Oven_FF()
        self.splitter.exterior_3 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 780

class PRODUCT_4_Door_Micro_and_Oven_Tall_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_4_Vertical_Openings_FF()
        self.splitter.opening_3_height = unit.inch(30)
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door_FF()
        self.splitter.exterior_2 = appliances.INSERT_Microwave_FF()
        self.splitter.exterior_3 = appliances.INSERT_Single_Oven_FF()
        self.splitter.exterior_4 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 800

class PRODUCT_Refrigerator_Tall_FF(cabinets.Face_Frame_Refrigerator):
     
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.carcass.prompts = {"Remove Bottom":True,"Toe Kick Height":0}
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door_FF()
        self.splitter.exterior_2 = None
        self.splitter.opening_1_height = unit.inch(10)
        self.product_price = 680
        
class PRODUCT_1_Door_Tall_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 590
        
class PRODUCT_2_Door_Tall_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 610
        
class PRODUCT_1_Double_Door_Tall_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Single_Door_FF()
        self.splitter.interior_2 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door_FF()
        self.product_price = 600

class PRODUCT_2_Double_Door_Tall_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door_FF()
        self.splitter.interior_2 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 760
        
class PRODUCT_2_Door_2_Drawer_Tall_FF(cabinets.Face_Frame_Standard): # NEED DRAWER STACK
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_3_Vertical_Openings_FF()
        self.splitter.opening_2_height = unit.inch(10)
        self.splitter.opening_3_height = unit.inch(10)
        self.splitter.exterior_1 = exteriors.INSERT_Tall_Double_Door_FF()
        self.splitter.interior_1 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_3 = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 780

class PRODUCT_2_Door_3_Drawer_Tall_FF(cabinets.Face_Frame_Standard): # NEED DRAWER STACK
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_4_Vertical_Openings_FF()
        self.splitter.opening_2_height = unit.inch(6)
        self.splitter.opening_3_height = unit.inch(6)
        self.splitter.opening_4_height = unit.inch(6)
        self.splitter.exterior_1 = exteriors.INSERT_Tall_Double_Door_FF()
        self.splitter.interior_1 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_3 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_4 = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 790
        
#---------PRODUCT: UPPER CABINETS

class PRODUCT_1_Door_Upper_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 250
        
class PRODUCT_2_Door_Upper_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 300

class PRODUCT_1_Double_Door_Upper_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Single_Door_FF()
        self.splitter.exterior_2 = exteriors.INSERT_Upper_Single_Door_FF()
        self.product_price = 350

class PRODUCT_2_Double_Door_Upper_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door_FF()
        self.splitter.exterior_2 = exteriors.INSERT_Upper_Double_Door_FF()
        self.product_price = 400

class PRODUCT_Microwave_2_Door_Upper_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door_FF()
        self.splitter.exterior_2 = appliances.INSERT_Microwave_FF()
        self.product_price = 300

class PRODUCT_2_Door_Upper_with_Microwave_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = unit.inch(30)
        self.height = props.upper_cabinet_height - unit.inch(20)
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Double_Door_FF()
        self.interior = None
        self.add_microwave = True
        self.product_price = 500
        
class PRODUCT_2_Door_Upper_with_Vent_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.upper_cabinet_height - unit.inch(20)
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Double_Door_FF()
        self.interior = None
        self.add_vent_hood = True
        self.product_price = 450
        
class PRODUCT_2_Door_2_Drawer_Upper_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = UPPER_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.splitter = splitters.INSERT_3_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door_FF()
        self.splitter.interior_1 = interiors.INSERT_Shelves()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_3 = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 580

#---------PRODUCT: OUTSIDE CORNER CABINETS

# TODO: CREATE OUTSIDE CORNER FF CABINETS

# #---------PRODUCT: TRANSITION CABINETS

# TODO: CREATE TRANSITION FF CABINETS

#---------PRODUCT: STARTER CABINETS

class PRODUCT_Base_Starter_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = STARTER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = None
        self.interior = None
        self.add_empty_opening = True
        self.product_price = 300

class PRODUCT_Tall_Starter_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = STARTER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = None
        self.interior = None
        self.add_empty_opening = True
        self.product_price = 500

class PRODUCT_Upper_Starter_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = STARTER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = None
        self.interior = None
        self.height_above_floor = props.height_above_floor
        self.add_empty_opening = True
        self.product_price = 200

class PRODUCT_Sink_Starter_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = STARTER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.carcass.remove_top = True
        self.exterior = None
        self.interior = None
        self.add_empty_opening = True
        self.product_price = 275

class PRODUCT_Suspended_Starter_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = STARTER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.suspended_cabinet_height
        self.depth = props.suspended_cabinet_depth
        self.carcass = carcass.INSERT_Suspended_Carcass()
        self.mirror_z = True
        self.exterior = None
        self.interior = None
        self.height_above_floor = props.base_cabinet_height
        self.add_empty_opening = True
        self.product_price = 150
        
#---------PRODUCT: DRAWER CABINETS
        
class PRODUCT_1_Drawer_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 200

class PRODUCT_2_Drawer_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 250

class PRODUCT_3_Drawer_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_3_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_3 = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 300
            
class PRODUCT_4_Drawer_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_4_Vertical_Openings_FF()
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_3 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_4 = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 350
        
class PRODUCT_1_Drawer_Suspended_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.suspended_cabinet_height
        self.depth = props.suspended_cabinet_depth
        self.mirror_z = True
        self.carcass = carcass.INSERT_Suspended_Carcass()
        self.height_above_floor = props.base_cabinet_height
        self.exterior = exteriors.INSERT_1_Drawer_FF()
        self.product_price = 200
        
class PRODUCT_2_Drawer_Suspended_FF(cabinets.Face_Frame_Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer * 2
        self.height = props.suspended_cabinet_height
        self.depth = props.suspended_cabinet_depth
        self.mirror_z = True
        self.carcass = carcass.INSERT_Suspended_Carcass()
        self.height_above_floor = props.base_cabinet_height
        self.exterior = exteriors.INSERT_Horizontal_Drawers_FF()
        self.product_price = 250
        
#---------PRODUCT: BLIND CORNER CABINETS

class PRODUCT_1_Door_Blind_Left_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 350

class PRODUCT_1_Door_Blind_Right_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 350

class PRODUCT_1_Door_Blind_Left_Corner_Tall_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 550

class PRODUCT_1_Door_Blind_Right_Corner_Tall_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 550

class PRODUCT_1_Door_Blind_Left_Corner_Upper_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.height_above_floor = props.height_above_floor
        self.mirror_z = True
        self.width = props.upper_width_blind
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 250

class PRODUCT_1_Door_Blind_Right_Corner_Upper_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.height_above_floor = props.height_above_floor
        self.mirror_z = True
        self.width = props.upper_width_blind
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Single_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 250

class PRODUCT_2_Door_Blind_Left_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 400

class PRODUCT_2_Door_Blind_Right_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 400

class PRODUCT_2_Door_Blind_Left_Corner_Tall_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 600

class PRODUCT_2_Door_Blind_Right_Corner_Tall_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 600

class PRODUCT_2_Door_Blind_Left_Corner_Upper_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.height_above_floor = props.height_above_floor
        self.mirror_z = True
        self.width = props.upper_width_blind
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 350

class PRODUCT_2_Door_Blind_Right_Corner_Upper_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.height_above_floor = props.height_above_floor
        self.mirror_z = True
        self.width = props.upper_width_blind
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.carcass = carcass.INSERT_Upper_Carcass()
        self.exterior = exteriors.INSERT_Upper_Double_Door_FF()
        self.interior = interiors.INSERT_Shelves()
        self.product_price = 350

class PRODUCT_1_Door_1_Drawer_Blind_Right_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door_FF()
        self.product_price = 450
        
class PRODUCT_1_Door_1_Drawer_Blind_Left_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer_FF()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door_FF()
        self.product_price = 450
        
class PRODUCT_2_Door_2_Drawer_Blind_Right_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_Horizontal_Drawers_FF()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 500
        
class PRODUCT_2_Door_2_Drawer_Blind_Left_Corner_Base_FF(cabinets.Face_Frame_Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings_FF()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_Horizontal_Drawers_FF()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door_FF()
        self.product_price = 500
        
#---------PRODUCT: INSIDE CORNER CABINETS

class PRODUCT_Pie_Cut_Corner_Base(cabinets.Face_Frame_Inside_Corner):
     
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.base_inside_corner_size
        self.height = props.base_cabinet_height
        self.depth = props.base_inside_corner_size
        self.carcass = carcass.INSERT_Base_Inside_Corner_Notched_Carcass()
        self.exterior = exteriors.INSERT_Base_Pie_Cut_Door_FF()
        self.interior = None
        self.face_frame = "Pie Cut Face Frame.blend"
        self.product_price = 500
         
class PRODUCT_Pie_Cut_Corner_Upper(cabinets.Face_Frame_Inside_Corner):
     
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.upper_inside_corner_size
        self.height = props.upper_cabinet_height
        self.depth = props.upper_inside_corner_size
        self.height_above_floor = props.height_above_floor
        self.mirror_z = True
        self.carcass = carcass.INSERT_Upper_Inside_Corner_Notched_Carcass()
        self.exterior = exteriors.INSERT_Upper_Pie_Cut_Door_FF()
        self.interior = None
        self.face_frame = "Pie Cut Face Frame.blend"
        self.product_price = 350
         
class PRODUCT_1_Door_Diagonal_Corner_Base(cabinets.Face_Frame_Inside_Corner):
     
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.base_inside_corner_size
        self.height = props.base_cabinet_height
        self.depth = props.base_inside_corner_size
        self.carcass = carcass.INSERT_Base_Inside_Corner_Diagonal_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door_FF()
        self.interior = None
        self.face_frame = "Face Frame.blend"
        self.product_price = 500
         
class PRODUCT_2_Door_Diagonal_Corner_Base(cabinets.Face_Frame_Inside_Corner):
     
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.base_inside_corner_size
        self.height = props.base_cabinet_height
        self.depth = props.base_inside_corner_size
        self.carcass = carcass.INSERT_Base_Inside_Corner_Diagonal_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door_FF()
        self.interior = None
        self.face_frame = "Face Frame.blend"
        self.product_price = 520
         
class PRODUCT_1_Door_Diagonal_Corner_Upper(cabinets.Face_Frame_Inside_Corner):
     
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.upper_inside_corner_size
        self.height = props.upper_cabinet_height
        self.depth = props.upper_inside_corner_size
        self.height_above_floor = props.height_above_floor
        self.mirror_z = True
        self.carcass = carcass.INSERT_Upper_Inside_Corner_Diagonal_Carcass()
        self.exterior = exteriors.INSERT_Upper_Single_Door_FF()
        self.interior = None
        self.face_frame = "Face Frame.blend"
        self.product_price = 350
         
class PRODUCT_2_Door_Diagonal_Corner_Upper(cabinets.Face_Frame_Inside_Corner):
     
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.upper_inside_corner_size
        self.height = props.upper_cabinet_height
        self.depth = props.upper_inside_corner_size
        self.height_above_floor = props.height_above_floor
        self.mirror_z = True
        self.carcass = carcass.INSERT_Upper_Inside_Corner_Diagonal_Carcass()
        self.exterior = exteriors.INSERT_Upper_Double_Door_FF()
        self.interior = None
        self.face_frame = "Face Frame.blend"
        self.product_price = 380
