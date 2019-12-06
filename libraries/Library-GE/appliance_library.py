"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit
from . import appliance_classes

RANGES_PATH = os.path.join(os.path.dirname(__file__),"Ranges")
BUILT_IN_OVENS_PATH = os.path.join(os.path.dirname(__file__),"Built-In Ovens")
REFIGERATORS_PATH = os.path.join(os.path.dirname(__file__),"Refrigerators")
DISHWASHERS_PATH = os.path.join(os.path.dirname(__file__),"Dishwashers")


#---------PRODUCT: RANGES
        
class PRODUCT_GE_C2S985SETSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "GE_C2S985SETSS_DC"
        self.appliance_path = os.path.join(RANGES_PATH,"GE_C2S985SETSS_DC.blend")
        
class PRODUCT_GE_CS980STSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "GE_CS980STSS_DC"
        self.appliance_path = os.path.join(RANGES_PATH,"GE_CS980STSS_DC.blend")
        
class PRODUCT_GE_JGB282SETSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "GE_JGB282SETSS_DC"
        self.appliance_path = os.path.join(RANGES_PATH,"GE_JGB282SETSS_DC.blend")
        
#---------PRODUCTS: BUILT_IN OVENS

class PRODUCT_GE_CT918STSS_DC(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Built-In Ovens"
        self.assembly_name = "GE_CT918STSS_DC"
        self.appliance_path = os.path.join(BUILT_IN_OVENS_PATH,"GE_CT918STSS_DC.blend")
        
class PRODUCT_GE_CT959STSS_DC(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Built-In Ovens"
        self.assembly_name = "GE_CT959STSS_DC"
        self.appliance_path = os.path.join(BUILT_IN_OVENS_PATH,"GE_CT959STSS_DC.blend")
        
class PRODUCT_GE_JGRP20BEJBB_DC(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Built-In Ovens"
        self.assembly_name = "GE_JGRP20BEJBB_DC"
        self.appliance_path = os.path.join(BUILT_IN_OVENS_PATH,"GE_JGRP20BEJBB_DC.blend")
        
#--------PRODUCT: REFRIGERATORS  

class PRODUCT_GE_CFCP1NIYSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "GE_CFCP1NIYSS_DC"
        self.appliance_path = os.path.join(REFIGERATORS_PATH,"GE_CFCP1NIYSS_DC.blend")
              
class PRODUCT_GE_CSCP5UGXSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "GE_CSCP5UGXSS_DC"
        self.appliance_path = os.path.join(REFIGERATORS_PATH,"GE_CSCP5UGXSS_DC.blend")
              
class PRODUCT_GE_PGCS1NFZSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "GE_PGCS1NFZSS_DC"
        self.appliance_path = os.path.join(REFIGERATORS_PATH,"GE_PGCS1NFZSS_DC.blend")
              
class PRODUCT_GE_PSDS5YGXSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "GE_PSDS5YGXSS_DC"
        self.appliance_path = os.path.join(REFIGERATORS_PATH,"GE_PSDS5YGXSS_DC.blend")
              
class PRODUCT_GE_ZIC30GNZII_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Refrigerators"
        self.assembly_name = "GE_ZIC30GNZII_DC"
        self.appliance_path = os.path.join(REFIGERATORS_PATH,"GE_ZIC30GNZII_DC.blend")
        
#---------PRODUCT: DISHWASHERS

class PRODUCT_GE_CDWT280VSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Dishwashers"
        self.assembly_name = "GE_CDWT280VSS_DC"
        self.appliance_path = os.path.join(DISHWASHERS_PATH,"GE_CDWT280VSS_DC.blend")
                
class PRODUCT_GE_GDWT368VSS_DC(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Dishwashers"
        self.assembly_name = "GE_GDWT368VSS_DC"
        self.appliance_path = os.path.join(DISHWASHERS_PATH,"GE_GDWT368VSS_DC.blend")
                
              
                                                                              
                                                                
        

        




