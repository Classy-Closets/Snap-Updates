"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit
from . import appliance_classes

BATHROOM_SINK_PATH = os.path.join(os.path.dirname(__file__),"Bathroom_Sinks")
BATHROOM_FAUCETS_PATH = os.path.join(os.path.dirname(__file__),"Bathroom Faucets")
BATHROOM_SHOWER_FAUCETS_PATH = os.path.join(os.path.dirname(__file__),"Shower Faucets")
BATHTUBS_PATH = os.path.join(os.path.dirname(__file__),"Bathtubs")
FLOOR_MOUNT_FAUCETS_PATH = os.path.join(os.path.dirname(__file__),"Floor Mount Faucets")
KITCHEN_FAUCETS_PATH = os.path.join(os.path.dirname(__file__),"Kitchen Faucets")
KITCHEN_SINKS_PATH = os.path.join(os.path.dirname(__file__),"Kitchen_sinks")
TOILET_PATH = os.path.join(os.path.dirname(__file__),"Toilets")
SHOWER_WALL_PANELS_PATH = os.path.join(os.path.dirname(__file__),"Shower Wall Panels") 
SHOWER_DOOR_PATH = os.path.join(os.path.dirname(__file__),"Shower Doors") 
#---------PRODUCT: BATHROOM SINKS    

class PRODUCT_Bachata_2609_MU(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Bachata 2609-MU"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Bachata 2609-MU.blend")  

class PRODUCT_Bachata_2609_SU(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Bachata 2609-SU"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Bachata 2609-SU.blend")  

class PRODUCT_Briolette_2373(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Briolette 2373"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Briolette 2373.blend")  

class PRODUCT_Bryant_2699(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Bryant 2699"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Bryant 2699.blend")  

class PRODUCT_Bryant_2714(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Bryant 2714"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Bryant 2714.blend")  

class PRODUCT_Camber_2349(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Camber 2349"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Camber 2349.blend")  

class PRODUCT_Carillon_7799(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Carillon 7799"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Carillon 7799.blend")  

class PRODUCT_Carillon_7806(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Carillon 7806"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Carillon 7806.blend")  

class PRODUCT_Brookline_2202(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Sinks"
        self.assembly_name = "Brookline 2202"
        self.appliance_path = os.path.join(BATHROOM_SINK_PATH,"Brookline 2202.blend")  

#---------PRODUCT: BATHROOM FAUCETS            
        
class PRODUCT_Alteo_45100_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Aleto 45100-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Alteo 45100-4.blend")        

class PRODUCT_Alteo_45102_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Alteo 45102-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Alteo 45102-4.blend") 

class PRODUCT_Alteo_45800_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Alteo 45800-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Alteo 45800-4.blend") 

class PRODUCT_Archer_11076_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Archer 11076-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Archer 11076-4.blend") 

class PRODUCT_Artifacts_72758(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Artifacts 72758"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Artifacts 72758.blend")

class PRODUCT_Artifacts_72760(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Artifacts 72760"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Artifacts 72760.blend")

class PRODUCT_Artifacts_72762_9m(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Artifacts 72762-9m"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Artifacts 72762-9m.blend")

class PRODUCT_Bancroft_10577_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Bancroft 10577-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Bancroft 10577-4.blend")

class PRODUCT_Composed_73050_7(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Composed 73050-7"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Composed 73050-7.blend")

class PRODUCT_Composed_73054_7(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Composed 73054-7"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Composed 73054-7.blend")

class PRODUCT_Composed_73060_3(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Composed 73060-3"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Composed 73060-3.blend")
        
class PRODUCT_Composed_73060_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Composed 73060-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Composed 73060-4.blend")

class PRODUCT_Composed_73159_7(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Composed 73159-7"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Composed 73159-7.blend")

class PRODUCT_Composed_73167_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Composed 73167-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Composed 73167-4.blend")

class PRODUCT_Composed_73168_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Composed 73168-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Composed 73168-4.blend")

class PRODUCT_Coralais_15182_4NDR(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Coralais 15182-4NDR"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Coralais 15182-4NDR.blend")

class PRODUCT_Coralais_15198_4RA(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Coralais 15198-4RA"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Coralais 15198-4RA.blend")

class PRODUCT_Coralais_15199_4NDR(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Coralais 15199-4NDR"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Coralais 15199-4NDR.blend")

class PRODUCT_Devonshire_193_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Devonshire 193-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Devonshire 193-4.blend")

class PRODUCT_Devonshire_393_N4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Devonshire 393-N4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Devonshire 393-N4.blend")

class PRODUCT_Devonshire_394_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Devonshire 394-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Devonshire 394-4.blend")

class PRODUCT_Elliston_R72780_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Elliston R72780-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Elliston R72780-4D.blend")

class PRODUCT_Elliston_R72781_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Elliston R72781-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Elliston R72781-4D.blend")

class PRODUCT_Elliston_R72782_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Elliston R72782-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Elliston R72782 4D.blend")

class PRODUCT_Fairfax_12182(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Fairfax 12182"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Fairfax 12182.blend")

class PRODUCT_Fairfax_12266_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Fairfax 12266-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Fairfax 12266-4.blend")

class PRODUCT_Fairfax12265_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Fairfax12265-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Fairfax12265-4.blend")

class PRODUCT_Falling_Water_T197(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Falling Water T197"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Falling Water T197.blend")

class PRODUCT_Finial_310_4M(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Finial 310-4M"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Finial 310-4M.blend")

class PRODUCT_Forte_10215_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Forte 10215-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Forte 10215-4.blend")

class PRODUCT_Forte_10270_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Forte 10270-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Forte 10270-4.blend")

class PRODUCT_Forte_10270_4A(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Forte 10270-4A"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Forte 10270-4A.blend")

class PRODUCT_Georgeson_R99910_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Georgeson R99910-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Georgeson R99910-4D.blend")

class PRODUCT_Georgeson_R99911_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Georgeson R99911-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Georgeson R99911-4D.blend")

class PRODUCT_Georgeson_R99912_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Georgeson R99912-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Georgeson R99912-4D.blend")

class PRODUCT_Honesty_99760_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Honesty 99760-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Honesty 99760-4.blend")

class PRODUCT_Kelston_13491_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Kelston 13491-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Kelston 13491-4.blend")

class PRODUCT_Loure_14660_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Loure 14660-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Loure 14660-4.blend")

class PRODUCT_Loure_14661_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Loure 14661-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Loure 14661-4.blend")

class PRODUCT_Loure_14662_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Loure 14662-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Loure 14662-4.blend")

class PRODUCT_Margaux_16231_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Margaux 16231-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Margaux 16231-4.blend")

class PRODUCT_Margaux_16232_3(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Margaux 16232-3"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Margaux 16232-3.blend")

class PRODUCT_Margaux_16232_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Margaux 16232-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Margaux 16232-4.blend")

class PRODUCT_Memoirs_454_X4V(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Memoirs 454-X4V"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Memoirs 454-X4V.blend")
        
class PRODUCT_Pinstripe_13132_4A(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Pinstripe 13132-4A"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Pinstripe 13132-4A.blend")       
        
class PRODUCT_Purist_14402_4A(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Purist 14402-4A"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Purist 14402-4A.blend")        

class PRODUCT_Purist_T14414_3(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Purist T14414-3"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Purist T14414-3.blend")
        
class PRODUCT_Purist_T14414_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Purist T14414-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Purist T14414-4.blend")        
        
class PRODUCT_Purist_T14415_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Purist T14415-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Purist T14415-4.blend")        
        
class PRODUCT_Refinia_5313_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Refinia 5313-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Refinia 5313-4.blend")  
        
class PRODUCT_Refinia_5316_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Refinia 5316-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Refinia 5316-4.blend")          
        
class PRODUCT_Refinia_5317_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Refinia 5317-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Refinia 5317-4.blend")          
                
class PRODUCT_Revival_T16106_4A(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Revival T16106-4A"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Revival T16106-4A.blend")          
                                      
class PRODUCT_Stance_14760_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Stance 14760-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Stance 14760-4.blend")          
                                      
class PRODUCT_Stance_14761_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Stance 14761-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Stance 14761-4.blend")          
                                      
class PRODUCT_Stillness_T944_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Stillness T944-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Stillness T944-4.blend")          
                                      
class PRODUCT_Symbol_19774_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Symbol 19774-4"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Symbol 19774-4.blend")          
                                      
class PRODUCT_Toobi_8990_7(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Toobi 8990-7"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Toobi 8990 7.blend")          
                                      
class PRODUCT_Toobi_8959_7(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Toobi 8959-7"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Toobi 8959-7.blend")          
                                      
class PRODUCT_Willamette_R99900_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Willamette R99900-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Willamette R99900-4D.blend")          
                                      
class PRODUCT_Willamette_R99901_4D(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Bathroom Faucets"
        self.assembly_name = "Willamette R99901-4D"
        self.appliance_path = os.path.join(BATHROOM_FAUCETS_PATH,"Willamette R99901-4D.blend")
        
        
        
#------------ PRODUCTS: SHOWER FAUCETS
class PRODUCT_Contemporary_13690(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Faucets"
        self.assembly_name = "Contemporary 13690"
        self.appliance_path = os.path.join(BATHROOM_SHOWER_FAUCETS_PATH,"Contemporary 13690.blend")
                
class PRODUCT_Contemporary_13696(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Faucets"
        self.assembly_name = "Contemporary 13696"
        self.appliance_path = os.path.join(BATHROOM_SHOWER_FAUCETS_PATH,"Contemporary 13696.blend")
        
class PRODUCT_Purist_9059(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Faucets"
        self.assembly_name = "Purist 9059"
        self.appliance_path = os.path.join(BATHROOM_SHOWER_FAUCETS_PATH,"Purist 9059.blend")
                
class PRODUCT_Devonshire_T395_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Faucets"
        self.assembly_name = "Devonshire T395-4"
        self.appliance_path = os.path.join(BATHROOM_SHOWER_FAUCETS_PATH,"Devonshire T395-4.blend")

class PRODUCT_Devonshire_Shower_Only(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Faucets"
        self.assembly_name = "Devonshire Shower Only"
        self.appliance_path = os.path.join(BATHROOM_SHOWER_FAUCETS_PATH,"Devonshire Shower Only.blend")
                        
#------------ PRODUCT: BATHTUBS

class PRODUCT_Dynametric_520_0(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Bathtubs"
        self.assembly_name = "Dynametric 520-0"
        self.appliance_path = os.path.join(BATHTUBS_PATH,"Dynametric 520-0.blend")        
        
class PRODUCT_Iron_Works_710_W(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Bathtubs"
        self.assembly_name = "Iron Works 710-W"
        self.appliance_path = os.path.join(BATHTUBS_PATH,"Iron Works 710-W.blend")        
        
class PRODUCT_Reve_894(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Bathtubs"
        self.assembly_name = "Reve 894"
        self.appliance_path = os.path.join(BATHTUBS_PATH,"Reve 894.blend")        
                        
class PRODUCT_Stargaze_6367(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Bathtubs"
        self.assembly_name = "Stargaze 6367"
        self.appliance_path = os.path.join(BATHTUBS_PATH,"Stargaze 6367.blend")        
                                
class PRODUCT_Sunstruck_6368(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Bathtubs"
        self.assembly_name = "Sunstruck 6368"
        self.appliance_path = os.path.join(BATHTUBS_PATH,"Sunstruck 6368.blend")          
        
class PRODUCT_Villager_715_0(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Bathtubs"
        self.assembly_name = "Villager 715-0"
        self.appliance_path = os.path.join(BATHTUBS_PATH,"Villager 715-0.blend")          
                
class PRODUCT_Vintage_700_0(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Bathtubs"
        self.assembly_name = "Vintage 700-0"
        self.appliance_path = os.path.join(BATHTUBS_PATH,"Vintage 700-0.blend") 
        
        
#------- PRODUCT: FLOOR MOUNT FAUCETS

class PRODUCT_Kelston_T97332_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Floor Mount Faucets"
        self.assembly_name = "Kelston T97332-4"
        self.appliance_path = os.path.join(FLOOR_MOUNT_FAUCETS_PATH,"Kelston T97332-4.blend")                                           
                                                               
class PRODUCT_Loure_T97330_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Floor Mount Faucets"
        self.assembly_name = "Loure T97330-4"
        self.appliance_path = os.path.join(FLOOR_MOUNT_FAUCETS_PATH,"Loure T97330-4.blend")                                           
                                                              
class PRODUCT_Margaux_T97331_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Floor Mount Faucets"
        self.assembly_name = "Margaux T97331-4"
        self.appliance_path = os.path.join(FLOOR_MOUNT_FAUCETS_PATH,"Margaux T97331-4.blend")                                           
                                                              
class PRODUCT_Purist_T97328_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Floor Mount Faucets"
        self.assembly_name = "Purist T97328-4"
        self.appliance_path = os.path.join(FLOOR_MOUNT_FAUCETS_PATH,"Purist T97328-4.blend")                                           
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
#---------PRODUCT: KITCHEN FAUCETS             

class PRODUCT_Antique_149_3(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Antique 149-3"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Antique 149-3.blend") 
        
class PRODUCT_Antique_158_3(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Antique 158-3"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Antique 158-3.blend")         
        
class PRODUCT_Antique_158_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Antique 158-4"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Antique 158-4.blend")          
        
class PRODUCT_Antique_169(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Antique 169"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Antique 169.blend")          
                
class PRODUCT_Artifacts_99259(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99259"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99259.blend")         
        
class PRODUCT_Artifacts_99260(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99260"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99260.blend")         
        
class PRODUCT_Artifacts_99261(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99261"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99261.blend")         
                
class PRODUCT_Artifacts_99262(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99262"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99262.blend")         
                        
class PRODUCT_Artifacts_99263(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99263"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99263.blend")         
                                
class PRODUCT_Artifacts_99264(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99264"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99264.blend")         
                                        
class PRODUCT_Artifacts_99265(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99265"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99265.blend")         
                                        
class PRODUCT_Artifacts_99266(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99266"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99266.blend")         
                                                       
class PRODUCT_Artifacts_99267(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99267"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99267.blend")         
                                                               
class PRODUCT_Artifacts_99268(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99268"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99268.blend")         
                                                                       
class PRODUCT_Artifacts_99270(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99270"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99270.blend")         
                                                                               
class PRODUCT_Artifacts_99271(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Artifacts 99271"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Artifacts 99271.blend")         
                                                                                  
class PRODUCT_Barossa_R78035_SD(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Barossa R78035-SD"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Barossa R78035-SD.blend")         
                                                                                          
class PRODUCT_Beckon_99332(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Beckon 99332"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Beckon 99332.blend")         
                                                                                               
class PRODUCT_Bellera_560(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Bellera 560"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Bellera 560.blend")         
                                                                                                
class PRODUCT_Carmichael_R72512_SD(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Carmichael R72512-SD"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Carmichael R72512-SD.blend")         
                                                                                                
class PRODUCT_Clairette_692(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Clairette 692"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Clairette 692.blend")         
                                                                                                            
class PRODUCT_Coralais_15160(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Coralais 15160"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Coralais 15160.blend")         
                                                                                              
class PRODUCT_Cruette_780(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Cruette 780"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Cruette 780.blend")         
        
class PRODUCT_Elate_13963(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Elate 13963"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Elate 13963.blend")          
        
class PRODUCT_Evoke_6331(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Evoke 6331"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Evoke 6331.blend")        
        
class PRODUCT_Evoke_6332(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Evoke 6332"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Evoke 6332.blend")        
        
class PRODUCT_Fairfax_12172(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Fairfax 12172"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Fairfax 12172.blend")        
                
class PRODUCT_Fairfax_12176(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Fairfax 12176"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Fairfax 12176.blend")        
                        
class PRODUCT_Fairfax_12177(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Fairfax 12177"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Fairfax 12177.blend")        
        
class PRODUCT_Fairfax_12185(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Fairfax 12185"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Fairfax 12185.blend")        
                
class PRODUCT_Fairfax_12231(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Fairfax 12231"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Fairfax 12231.blend")        
                        
class PRODUCT_Forte_10412(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Forte 10412"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Forte 10412.blend")        
                                
class PRODUCT_Forte_10416(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Forte 10416"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Forte 10416.blend")        
                                        
class PRODUCT_Forte_10433(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Forte 10433"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Forte 10433.blend")        
                                                
class PRODUCT_Forte_10445(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Forte 10445"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Forte 10445.blend")          
        
class PRODUCT_HiRise_7322_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "HiRise 7322-4"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"HiRise 7322-4.blend")          
        
class PRODUCT_HiRise_7337(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "HiRise 7337"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"HiRise 7337.blend")                      
        
class PRODUCT_HiRise_7338_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "HiRise 7338-4"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"HiRise 7338-4.blend")                      
                
class PRODUCT_Karbon_6227_C12(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Karbon 6227-C12"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Karbon 6227-C12.blend")                      
                
class PRODUCT_Karbon_6268_C11(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Karbon 6268-C11"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Karbon 6268-C11.blend")                      
                                
class PRODUCT_Malleco_R562_SD(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Malleco R562-SD"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Malleco R562-SD.blend")                      
                                        
class PRODUCT_Mazz_R72510_SD(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Mazz R72510-SD"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Mazz R72510-SD.blend")                      
                                                
class PRODUCT_Mazz_R72511_SD(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Mazz R72511-SD"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Mazz R72511-SD.blend")                      
                                                        
class PRODUCT_Mistos_R72508(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Mistos R72508"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Mistos R72508.blend")                      
                                                                
class PRODUCT_Mistos_R72509(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Mistos R72509"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Mistos R72509.blend")                      
                                                                        
class PRODUCT_ProMaster_6330(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "ProMaster 6330"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"ProMaster 6330.blend")                      
                                                                                
class PRODUCT_Purist_7505(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7505"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7505.blend")                      
                                                                                       
class PRODUCT_Purist_7506(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7506"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7506.blend")                      
                                                                                     
class PRODUCT_Purist_7507(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7507"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7507.blend")                      
                                                                                     
class PRODUCT_Purist_7508(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7508"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7508.blend")                      
                                                                                          
class PRODUCT_Purist_7509(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7509"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7509.blend")                      
                                                                                        
class PRODUCT_Purist_7511(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7511"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7511.blend")                      
                                                                                         
class PRODUCT_Purist_7547_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7547-4"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7547-4.blend")                      
                                                               
class PRODUCT_Purist_7548_4(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Purist 7548-4"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Purist 7548-4.blend")                      
                                                                       
class PRODUCT_Revival_16109_4A(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Revival 16109-4A"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Revival 16109-4A.blend")                      
                                                                               
class PRODUCT_Revival_16111_4A(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Revival Revival 16111-4A"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Revival 16111-4A.blend")                      
                                                                                       
class PRODUCT_Sensate_72218_B7(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Sensate 72218-B7"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Sensate 72218-B7.blend")                      
                                                                                           
class PRODUCT_Simplice_596(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Simplice 596"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Simplice 596.blend")                      
                                                                                                
class PRODUCT_Simplice_597(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Simplice 597"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Simplice 597.blend")                      
                                                                                              
class PRODUCT_Vinnata_691(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Vinnata 691"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Vinnata 691.blend")                      
                                                                                              
class PRODUCT_Wellspring_6666(appliance_classes.Object_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Faucets"
        self.assembly_name = "Wellspring 6666"
        self.appliance_path = os.path.join(KITCHEN_FAUCETS_PATH,"Wellspring 6666.blend")                      
                                                                                      
#--------PRODUCT: KITCHEN SINKS

class PRODUCT_Cape_Dory_5863(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Cape Dory 5863"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Cape Dory 5863.blend")         
 
class PRODUCT_Hartland_5818(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Hartland 5818"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Hartland 5818.blend")         
  
class PRODUCT_Octave_3842(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Octave 3842"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Octave 3842.blend")         
   
 
class PRODUCT_Prolific_5540(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Prolific 5540"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Prolific 5540.blend")         
   
class PRODUCT_Riverby_5871(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Riverby 5871"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Riverby 5871.blend")  
 
class PRODUCT_Riverby_8669(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Riverby 8669"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Riverby 8669.blend")  
  
class PRODUCT_Riverby_8679(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Riverby 8679"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Riverby 8679.blend")  
   
class PRODUCT_Riverby_8689(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Riverby 8689"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Riverby 8689.blend")  
   
class PRODUCT_Stages_3760(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Stages 3760"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Stages 3760.blend")  
     
class PRODUCT_Stages_3761(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Stages 3761"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Stages 3761.blend")   
 
class PRODUCT_Strive_5281(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Kitchen Sinks"
        self.assembly_name = "Strive 5281"
        self.appliance_path = os.path.join(KITCHEN_SINKS_PATH,"Strive 5281.blend")  
        
#-------- PRODUCT: TOILETS

class PRODUCT_Cimarron_6418_0(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Toilets"
        self.assembly_name = "Cimarron 6418-0"
        self.appliance_path = os.path.join(TOILET_PATH,"Cimarron 6418-0.blend")        
         
class PRODUCT_Cimarron_6418_7(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Toilets"
        self.assembly_name = "Cimarron 6418-7"
        self.appliance_path = os.path.join(TOILET_PATH,"Cimarron 6418-7.blend")        
         
class PRODUCT_San_Souci_4000_0(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Toilets"
        self.assembly_name = "San Souci 4000-0"
        self.appliance_path = os.path.join(TOILET_PATH,"San Souci 4000-0.blend")        
         
class PRODUCT_San_Souci_4000_7(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Toilets"
        self.assembly_name = "San Souci 4000-7"
        self.appliance_path = os.path.join(TOILET_PATH,"San Souci 4000-7.blend")        
         
class PRODUCT_Veil_6299_0(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Toilets"
        self.assembly_name = "Veil 6299-0"
        self.appliance_path = os.path.join(TOILET_PATH,"Veil 6299-0.blend")        
         
class PRODUCT_Veil_6299_7(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Toilets"
        self.assembly_name = "Veil 6299-7"
        self.appliance_path = os.path.join(TOILET_PATH,"Veil 6299-7.blend")
        
#-------- PRODUCT: SHOWER WALL PANELS

class PRODUCT_Choreograph_Cord_97601_T02(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Wall Panels"
        self.assembly_name = "Choreograph Cord 97601-T02"
        self.appliance_path = os.path.join(SHOWER_WALL_PANELS_PATH,"Choreograph Cord 97601-T02.blend")                
                                 
class PRODUCT_Choreograph_Brick_97601_T02(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Wall Panels"
        self.assembly_name = "Choreograph Brick 97601-T02"
        self.appliance_path = os.path.join(SHOWER_WALL_PANELS_PATH,"Choreograph Brick 97601-T02.blend")
        
#--------- PRODUCT: SHOWER DOORS          
 
class PRODUCT_Revel_70x40(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Shower Doors"
        self.assembly_name = "Revel 70x40"
        self.appliance_path = os.path.join(SHOWER_DOOR_PATH,"Revel 70x40.blend")
         
 
 
 
 
 
 
 
 
 
 
        
           