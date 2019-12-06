"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit
from . import appliance_classes

REFRIGERATORS_PATH = os.path.join(os.path.dirname(__file__),"Refrigerators")

#---------PRODUCT: REFRIGERATORS
        
class PRODUCT_SubeZero_ID_30F(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "ID-30F"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"SubeZero_ID-30F.blend")
        
class PRODUCT_SubZero_648PROG(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "648PROG"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"SubZero_648PROG.blend")
 
class PRODUCT_SubZero_BI_36RG_O(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "BI-36RG-O"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"SubZero_BI-36RG_O.blend")
 
class PRODUCT_SubZero_BI_36UID_O(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "BI-36UID-O"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"SubZero_BI-36UID_O.blend")
 
class PRODUCT_SubZero_BI_42UFD_O(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "SBI-42UFD-O"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"SubZero_BI-42UFD_O.blend")
 
class PRODUCT_SubZero_IC_36R(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "IC-36R"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"SubZero_IC-36R.blend")
         
class PRODUCT_SUB_ZERO_UW_24FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "UW-24FS"
        self.appliance_path = os.path.join(REFRIGERATORS_PATH,"SUB-ZERO_UW-24FS.blend")
         
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
        