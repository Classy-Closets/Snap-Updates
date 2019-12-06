"""
Microvellum 
Frameless Library
Stores all the products for the Frameless Library
"""

from mv import unit #@UnresolvedImport
from . import frameless_cabinets as cabinets #@UnresolvedImport
from . import carcass_simple as carcass #@UnresolvedImport
from . import frameless_exteriors as exteriors #@UnresolvedImport
from . import cabinet_interiors as interiors #@UnresolvedImport
from . import frameless_splitters as splitters #@UnresolvedImport
from . import frameless_appliances as appliances #@UnresolvedImport
from . import cabinet_properties #@UnresolvedImport

LIBRARY_NAME = "Cabinets - Frameless"
BASE_CATEGORY_NAME = "Base Cabinets"
TALL_CATEGORY_NAME = "Tall Cabinets"
UPPER_CATEGORY_NAME = "Upper Cabinets"
OUTSIDE_CORNER_CATEGORY_NAME = "Outside Corner Cabinets"
INSIDE_CORNER_CATEGORY_NAME = "Inside Corner Cabinets"
TRANSITION_CATEGORY_NAME = "Transition Cabinets"
STARTER_CATEGORY_NAME = "Starter Cabinets"
DRAWER_CATEGORY_NAME = "Drawer Cabinets"
BLIND_CORNER_CATEGORY_NAME = "Blind Corner Cabinets"

def cabinet_shelves():
    return interiors.INSERT_Simple_Shelves()

#---------PRODUCT: BASE CABINETS

class PRODUCT_1_Door_Base(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 400

class PRODUCT_2_Door_Base(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 500
        
class PRODUCT_2_Door_Sink(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Sink_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door()
        self.interior = None
        self.product_price = 500
        
class PRODUCT_2_Door_with_False_Front_Sink(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Sink_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door_With_False_Front()
        self.interior = None
        self.product_price = 550
        
class PRODUCT_2_Door_2_False_Front_Sink(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Sink_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door_With_2_False_Front()
        self.interior = None
        self.product_price = 600
        
class PRODUCT_1_Door_Sink(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Sink_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 400

class PRODUCT_1_Door_1_Drawer_Base(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 450

class PRODUCT_2_Door_2_Drawer_Base(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_Horizontal_Drawers()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 550

class PRODUCT_2_Door_1_Drawer_Base(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 525
        
class PRODUCT_Microwave_2_Door_Base(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = unit.inch(15)
        self.splitter.exterior_1 = appliances.INSERT_Microwave()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door()
        self.product_price = 450

class PRODUCT_Microwave_1_Drawer_Base(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BASE_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = unit.inch(15)
        self.splitter.exterior_1 = appliances.INSERT_Microwave()
        self.splitter.exterior_2 = exteriors.INSERT_1_Drawer()
        self.product_price = 425
        
#---------PRODUCT: TALL CABINETS

class PRODUCT_4_Door_Oven_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_3_Vertical_Openings()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_2 = appliances.INSERT_Single_Oven()
        self.splitter.exterior_3 = exteriors.INSERT_Base_Double_Door()
        self.product_price = 720

class PRODUCT_4_Door_Micro_and_Oven_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_4_Vertical_Openings()
        self.splitter.opening_3_height = unit.inch(30)
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_2 = appliances.INSERT_Microwave()
        self.splitter.exterior_3 = appliances.INSERT_Single_Oven()
        self.splitter.exterior_4 = exteriors.INSERT_Base_Double_Door()
        self.product_price = 740

class PRODUCT_Refrigerator_Tall(cabinets.Refrigerator):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.carcass.prompts = {'Remove Bottom':True}
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = unit.inch(10)
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door()
        self.product_price = 700
        
class PRODUCT_1_Door_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 620
        
class PRODUCT_2_Door_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 680
        
class PRODUCT_1_Double_Door_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Single_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 710

class PRODUCT_2_Double_Door_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_2 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 780
        
class PRODUCT_2_Door_2_Drawer_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_2_height = unit.inch(20)
        self.splitter.exterior_1 = exteriors.INSERT_Tall_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_1 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_2_Drawer_Stack()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 750

class PRODUCT_2_Door_3_Drawer_Tall(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TALL_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_2_height = unit.inch(20)
        self.splitter.exterior_1 = exteriors.INSERT_Tall_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_1 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_3_Drawer_Stack()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 725
        
#---------PRODUCT: UPPER CABINETS

class PRODUCT_1_Door_Upper(cabinets.Standard):
    
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
        self.exterior = exteriors.INSERT_Upper_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 250
        
class PRODUCT_2_Door_Upper(cabinets.Standard):
    
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
        self.exterior = exteriors.INSERT_Upper_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 300

class PRODUCT_1_Double_Door_Upper(cabinets.Standard):
    
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
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Single_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = exteriors.INSERT_Upper_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 350

class PRODUCT_2_Double_Door_Upper(cabinets.Standard):
    
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
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 400

class PRODUCT_Microwave_2_Door_Upper(cabinets.Standard):
    
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
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_2 = appliances.INSERT_Microwave()
        self.product_price = 300

class PRODUCT_2_Door_Upper_with_Microwave(cabinets.Standard):
    
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
        self.exterior = exteriors.INSERT_Upper_Double_Door()
        self.interior = None
        self.add_microwave = True
        self.product_price = 500
        
class PRODUCT_2_Door_Upper_with_Vent(cabinets.Standard):
    
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
        self.exterior = exteriors.INSERT_Upper_Double_Door()
        self.interior = None
        self.add_vent_hood = True
        self.product_price = 340
        
class PRODUCT_2_Door_2_Drawer_Upper(cabinets.Standard):
    
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
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.exterior_1 = exteriors.INSERT_Upper_Double_Door()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.interior_1 = cabinet_shelves()
        self.splitter.exterior_2 = exteriors.INSERT_2_Drawer_Stack()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 450

#---------PRODUCT: OUTSIDE CORNER CABINETS

class PRODUCT_Outside_Radius_Corner_Base(cabinets.Outside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Outside_Radius_Corner_Carcass()
        self.exterior = None
        self.interior = None
        self.product_price = 200

class PRODUCT_Outside_Radius_Corner_Tall(cabinets.Outside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Outside_Radius_Corner_Carcass()
        self.exterior = None
        self.interior = None
        self.product_price = 350
        
class PRODUCT_Outside_Radius_Corner_Upper(cabinets.Outside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Outside_Radius_Corner_Carcass()
        self.exterior = None
        self.interior = None
        self.product_price = 180
        
class PRODUCT_Outside_Chamfer_Corner_Base(cabinets.Outside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Outside_Chamfered_Corner_Carcass()
        self.exterior = None
        self.interior = None
        self.product_price = 160

class PRODUCT_Outside_Chamfer_Corner_Tall(cabinets.Outside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Outside_Chamfered_Corner_Carcass()
        self.exterior = None
        self.interior = None
        self.product_price = 340
        
class PRODUCT_Outside_Chamfer_Corner_Upper(cabinets.Outside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = OUTSIDE_CORNER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Outside_Chamfered_Corner_Carcass()
        self.exterior = None
        self.interior = None
        self.product_price = 160
        
#---------PRODUCT: TRANSITION CABINETS

class PRODUCT_1_Door_Base_Transition(cabinets.Transition):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Transition_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None
        self.product_price = 350

class PRODUCT_2_Door_Base_Transition(cabinets.Transition):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Transition_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None
        self.product_price = 430

class PRODUCT_1_Door_Tall_Transition(cabinets.Transition):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Transition_Carcass()
        self.exterior = exteriors.INSERT_Tall_Single_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None
        self.product_price = 530

class PRODUCT_2_Door_Tall_Transition(cabinets.Transition):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Transition_Carcass()
        self.exterior = exteriors.INSERT_Tall_Double_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None
        self.product_price = 500

class PRODUCT_1_Door_Upper_Transition(cabinets.Transition):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Transition_Carcass()
        self.exterior = exteriors.INSERT_Upper_Single_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None
        self.product_price = 250

class PRODUCT_2_Door_Upper_Transition(cabinets.Transition):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = TRANSITION_CATEGORY_NAME
        self.width = props.width_2_door
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        self.carcass = carcass.INSERT_Upper_Transition_Carcass()
        self.exterior = exteriors.INSERT_Upper_Double_Door()
        self.exterior.prompts = {'Half Overlay Left':True,'Half Overlay Right':True}
        self.interior = None
        self.product_price = 300
        
#---------PRODUCT: STARTER CABINETS

class PRODUCT_Base_Starter(cabinets.Standard):
    
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

class PRODUCT_Tall_Starter(cabinets.Standard):
    
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

class PRODUCT_Upper_Starter(cabinets.Standard):
    
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

class PRODUCT_Sink_Starter(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = STARTER_CATEGORY_NAME
        self.width = props.width_1_door
        self.height = props.sink_cabinet_height
        self.depth = props.sink_cabinet_depth
        self.carcass = carcass.INSERT_Sink_Carcass()
        self.exterior = None
        self.interior = None
        self.add_empty_opening = True
        self.product_price = 275

class PRODUCT_Suspended_Starter(cabinets.Standard):
    
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
        
class PRODUCT_1_Drawer(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_1_Drawer()
        self.product_price = 200

class PRODUCT_2_Drawer(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_2_Drawer_Stack()
        self.product_price = 250
        if not props.equal_drawer_stack_heights:
            self.exterior.top_drawer_front_height = props.top_drawer_front_height

class PRODUCT_3_Drawer(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_3_Drawer_Stack()
        self.product_price = 300
        if not props.equal_drawer_stack_heights:
            self.exterior.top_drawer_front_height = props.top_drawer_front_height
            
class PRODUCT_4_Drawer(cabinets.Standard):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = DRAWER_CATEGORY_NAME
        self.width = props.width_drawer
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_4_Drawer_Stack()
        self.product_price = 350
        if not props.equal_drawer_stack_heights:
            self.exterior.top_drawer_front_height = props.top_drawer_front_height
            
class PRODUCT_1_Drawer_Suspended(cabinets.Standard):
    
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
        self.exterior = exteriors.INSERT_1_Drawer()
        self.product_price = 200
        
class PRODUCT_2_Drawer_Suspended(cabinets.Standard):
    
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
        self.exterior = exteriors.INSERT_Horizontal_Drawers()
        self.product_price = 250
        
#---------PRODUCT: BLIND CORNER CABINETS

class PRODUCT_1_Door_Blind_Left_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 350

class PRODUCT_1_Door_Blind_Right_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 350

class PRODUCT_1_Door_Blind_Left_Corner_Tall(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 550

class PRODUCT_1_Door_Blind_Right_Corner_Tall(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 550

class PRODUCT_1_Door_Blind_Left_Corner_Upper(cabinets.Blind_Corner):
    
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
        self.exterior = exteriors.INSERT_Upper_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 250

class PRODUCT_1_Door_Blind_Right_Corner_Upper(cabinets.Blind_Corner):
    
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
        self.exterior = exteriors.INSERT_Upper_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 250

class PRODUCT_2_Door_Blind_Left_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door()
        self.interior = cabinet_shelves()
        self.product_price = 400

class PRODUCT_2_Door_Blind_Right_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 400

class PRODUCT_2_Door_Blind_Left_Corner_Tall(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 600

class PRODUCT_2_Door_Blind_Right_Corner_Tall(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.tall_width_blind
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        self.carcass = carcass.INSERT_Tall_Carcass()
        self.exterior = exteriors.INSERT_Tall_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 600

class PRODUCT_2_Door_Blind_Left_Corner_Upper(cabinets.Blind_Corner):
    
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
        self.exterior = exteriors.INSERT_Upper_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 350

class PRODUCT_2_Door_Blind_Right_Corner_Upper(cabinets.Blind_Corner):
    
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
        self.exterior = exteriors.INSERT_Upper_Double_Door()
        self.interior = cabinet_shelves()
        self.product_price = 350

class PRODUCT_1_Door_1_Drawer_Blind_Right_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 450
        
class PRODUCT_1_Door_1_Drawer_Blind_Left_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_1_Drawer()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = exteriors.INSERT_Base_Single_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 450
        
class PRODUCT_2_Door_2_Drawer_Blind_Right_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Right"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_Horizontal_Drawers()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 500
        
class PRODUCT_2_Door_2_Drawer_Blind_Left_Corner_Base(cabinets.Blind_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = BLIND_CORNER_CATEGORY_NAME
        self.blind_side = "Left"
        self.width = props.base_width_blind
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth
        self.carcass = carcass.INSERT_Base_Carcass()
        self.splitter = splitters.INSERT_2_Vertical_Openings()
        self.splitter.opening_1_height = props.top_drawer_front_height - unit.inch(1)
        self.splitter.exterior_1 = exteriors.INSERT_Horizontal_Drawers()
        self.splitter.exterior_1.prompts = {'Half Overlay Bottom':True}
        self.splitter.exterior_2 = exteriors.INSERT_Base_Double_Door()
        self.splitter.exterior_2.prompts = {'Half Overlay Top':True}
        self.product_price = 500
        
#---------PRODUCT: INSIDE CORNER CABINETS

class PRODUCT_Pie_Cut_Corner_Base(cabinets.Inside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.base_inside_corner_size
        self.height = props.base_cabinet_height
        self.depth = props.base_inside_corner_size
        self.carcass = carcass.INSERT_Base_Inside_Corner_Notched_Carcass()
        self.exterior = exteriors.INSERT_Base_Pie_Cut_Door()
        self.interior = None
        self.product_price = 500
        
class PRODUCT_Pie_Cut_Corner_Upper(cabinets.Inside_Corner):
    
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
        self.exterior = exteriors.INSERT_Upper_Pie_Cut_Door()
        self.interior = None
        self.product_price = 350
        
class PRODUCT_1_Door_Diagonal_Corner_Base(cabinets.Inside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.base_inside_corner_size
        self.height = props.base_cabinet_height
        self.depth = props.base_inside_corner_size
        self.carcass = carcass.INSERT_Base_Inside_Corner_Diagonal_Carcass()
        self.exterior = exteriors.INSERT_Base_Single_Door()
        self.interior = None
        self.product_price = 500
        
class PRODUCT_2_Door_Diagonal_Corner_Base(cabinets.Inside_Corner):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.library_name = LIBRARY_NAME
        self.category_name = INSIDE_CORNER_CATEGORY_NAME
        self.width = props.base_inside_corner_size
        self.height = props.base_cabinet_height
        self.depth = props.base_inside_corner_size
        self.carcass = carcass.INSERT_Base_Inside_Corner_Diagonal_Carcass()
        self.exterior = exteriors.INSERT_Base_Double_Door()
        self.interior = None
        self.product_price = 520
        
class PRODUCT_1_Door_Diagonal_Corner_Upper(cabinets.Inside_Corner):
    
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
        self.exterior = exteriors.INSERT_Upper_Single_Door()
        self.interior = None
        self.product_price = 350
        
class PRODUCT_2_Door_Diagonal_Corner_Upper(cabinets.Inside_Corner):
    
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
        self.exterior = exteriors.INSERT_Upper_Double_Door()
        self.interior = None
        self.product_price = 380
