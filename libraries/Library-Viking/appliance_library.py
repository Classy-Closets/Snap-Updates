"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit
from . import appliance_classes

RANGES_PATH = os.path.join(os.path.dirname(__file__),"Ranges")
BUILT_IN_OVENS_PATH = os.path.join(os.path.dirname(__file__),"Built-in Ovens")
REFRIGERATORS_PATH = os.path.join(os.path.dirname(__file__),"Refrigerators")


#---------PRODUCT: RANGES
        
class PRODUCT_Viking_Gas_Range_30_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "VGCC5304BSS"
        self.appliance_path = os.path.join(RANGES_PATH,"Viking Gas Range 30 inch.blend")
        
class PRODUCT_Viking_Gas_Range_36_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "VGCC5366BSS"
        self.appliance_path = os.path.join(RANGES_PATH,"Viking Gas Range 36 inch.blend")
        
class PRODUCT_Viking_Gas_Range_48_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "VGCC5486GSS"
        self.appliance_path = os.path.join(RANGES_PATH,"Viking Gas Range 48 inch.blend")
        
class PRODUCT_Viking_Gas_Range_60_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "VGCC5606GQSS"
        self.appliance_path = os.path.join(RANGES_PATH,"Viking Gas Range 60 inch.blend")
        
#-------PRODUCT: BUILT-IN OVENS

class PRODUCT_Viking_RVDOE_3_Series_Double_Oven(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Built-In Ovens"
        self.assembly_name = "RVDOE330SS"
        self.appliance_path = os.path.join(BUILT_IN_OVENS_PATH,"Viking RVDOE 3 Series Double Oven.blend")
        
class PRODUCT_Viking_VEDO_5_Series_Double_Oven(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Built-In Ovens"
        self.assembly_name = "VEDO1302SS"
        self.appliance_path = os.path.join(BUILT_IN_OVENS_PATH,"Viking VEDO 5 Series Double Oven.blend")
        
class PRODUCT_Viking_RVSOE_3_Series_Single_Oven(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Built-In Ovens"
        self.assembly_name = "RVSOE330SS"
        self.appliance_path = os.path.join(BUILT_IN_OVENS_PATH,"Viking RVSOE 3 Series Single Oven.blend")
        
class PRODUCT_Viking_VESO_5_Series_Single_Oven(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Built-In Ovens"
        self.assembly_name = "VESO1302SS"
        self.appliance_path = os.path.join(BUILT_IN_OVENS_PATH,"Viking VESO 5 Series Single Oven.blend")
        
#---------PRODUCT: REFRIGERATORS

class PRODUCT_Viking_Professional_Refrigerator_30_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "VCRB5303RSS"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"Viking Professional Refrigerator 30 inch.blend")
        
class PRODUCT_Viking_Professional_Refrigerator_36_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "VCRB5363RSS"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"Viking Professional Refrigerator 36 inch.blend")
        
class PRODUCT_Viking_Refrigerator_Freezer_Combo_36_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "VCBB5363ERSS"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"Viking Refrigerator-Freezer Combo 36 inch.blend")
        
class PRODUCT_Viking_Side_by_Side_Refrigerator_42_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "VCSB5423SS"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"Viking Side-by-Side Refrigerator 42 inch.blend")
        
class PRODUCT_Viking_Side_by_Side_Refrigerator_48_inch(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "VCSB5483SS"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"Viking Side-by-Side Refrigerator 48 inch.blend")
        































