"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit
from . import appliance_classes

ASSEMBLY_PATH = os.path.join(os.path.dirname(__file__),"Parametric Appliances")
WALL_APPLIANCE_PATH = os.path.join(os.path.dirname(__file__),"Wall Appliances")
COOKTOP_APPLIANCE_PATH = os.path.join(os.path.dirname(__file__),"Cooktops")
SINK_APPLIANCE_PATH = os.path.join(os.path.dirname(__file__),"Sinks")
FAUCET_APPLIANCE_PATH = os.path.join(os.path.dirname(__file__),"Faucets")
LAUNDRY_APPLIANCE_PATH = os.path.join(os.path.dirname(__file__),"Laundry")

#---------PRODUCT: PARAMETRIC APPLIANCES
        
class PRODUCT_Refrigerator(appliance_classes.Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Refrigerator"
        self.width = unit.inch(36)
        self.height = unit.inch(84)
        self.depth = unit.inch(27)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH,"Professional Refrigerator Generic.blend")
        
class PRODUCT_Range(appliance_classes.Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range"
        self.width = unit.inch(30)
        self.height = unit.inch(42)
        self.depth = unit.inch(28)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH,"Professional Gas Range Generic.blend")
        
class PRODUCT_Dishwasher(appliance_classes.Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Dishwasher"
        self.width = unit.inch(24)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH,"Professional Dishwasher Generic.blend")
        self.add_countertop = True
        
class PRODUCT_Range_Hood(appliance_classes.Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range Hood"
        self.width = unit.inch(30)
        self.height = unit.inch(14)
        self.depth = unit.inch(12.5)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH,"Wall Mounted Range Hood 01.blend")
        self.height_above_floor = unit.inch(60)
    
#---------PRODUCT: COOK TOPS    
    
class PRODUCT_Wolf_CG152_Transitional_Gas_Cooktop(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(COOKTOP_APPLIANCE_PATH,"Wolf CG152 Transitional Gas Cooktop.blend")

#---------PRODUCT: SINKS    

class PRODUCT_Bathroom_Sink(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(SINK_APPLIANCE_PATH,"Bathroom Sink.blend")      
        
class PRODUCT_Double_Basin_Sink(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(SINK_APPLIANCE_PATH,"Double Basin Sink.blend")            
        
class PRODUCT_Single_Basin_Sink(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(SINK_APPLIANCE_PATH,"Single Basin Sink.blend")           
        
#---------PRODUCT: FAUCETS            
        
class PRODUCT_Bathroom_Faucet(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(FAUCET_APPLIANCE_PATH,"Bathroom Faucet.blend")        
        
class PRODUCT_Faucet(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(FAUCET_APPLIANCE_PATH,"Faucet.blend")        
        
class PRODUCT_High_Arc_Faucet(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "High-Arc Faucet"
        self.appliance_path = os.path.join(FAUCET_APPLIANCE_PATH,"High-Arc Faucet.blend")  
        

#---------PRODUCT: LAUNDRY            
        
class PRODUCT_Washer(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH,"Washer.blend")  
              
class PRODUCT_Dryer(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH,"Dryer.blend") 
        
class PRODUCT_Metal_Stool(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH,"Metal Stool.blend")           
              
class PRODUCT_Wall_Mirror(appliance_classes.Parametric_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.width = unit.inch(24)
        self.height = unit.inch(.75)
        self.depth = unit.inch(-12)
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH,"Wall Mirror.blend")   
        self.height_above_floor = unit.inch(36)        
        
class PRODUCT_Vanity_Light_5(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH,"Vanity Light 5.blend")   
        self.height_above_floor = unit.inch(78)          
        
class PRODUCT_Vanity_Light_4(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH,"Vanity Light 4.blend")   
        self.height_above_floor = unit.inch(78)         
        
class PRODUCT_Vanity_Light_3(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH,"Vanity Light 3.blend")   
        self.height_above_floor = unit.inch(78)  