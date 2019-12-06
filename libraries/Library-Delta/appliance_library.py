"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit
from . import appliance_classes


BATHROOM_FAUCETS_PATH = os.path.join(os.path.dirname(__file__),"Bathroom Faucets")

#---------PRODUCT: PARAMETRIC APPLIANCES
        
class PRODUCT_Addison_592(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Addison 592"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Addison 592.blend")
        
class PRODUCT_Ara_567LF_PP(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Ara 567LF-PP"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Ara 567LF-PP.blend")
        
class PRODUCT_Ara_T2768(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Ara T2768"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Ara T2768.blend")
        
class PRODUCT_Cassidy_2597LF(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Cassidy 2597LF"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Cassidy 2597LF.blend")
        
class PRODUCT_Compel_561(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Compel 561"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Compel 561.blend")
        
class PRODUCT_Compel_561T(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Compel 561T"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Compel 561T.blend")
        
