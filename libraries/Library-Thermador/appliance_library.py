"""
Microvellum 
Appliances 
Stores all of the Logic, Product, and Insert Class definitions for appliances
"""

import os
from mv import fd_types, unit
from . import appliance_classes

COOKTOP_PATH = os.path.join(os.path.dirname(__file__),"Cook Tops")
DISH_WASHER_PATH = os.path.join(os.path.dirname(__file__),"Dish Washers")
FRIDGES_PATH = os.path.join(os.path.dirname(__file__),"Fridges")
FREEZERS_PATH = os.path.join(os.path.dirname(__file__),"Freezers")
MICROWAVE_PATH = os.path.join(os.path.dirname(__file__),"Microwaves")
RANGE_HOOD_PATH = os.path.join(os.path.dirname(__file__),"Range Hoods")
RANGE_PATH = os.path.join(os.path.dirname(__file__),"Ranges")
WALL_OVEN_PATH = os.path.join(os.path.dirname(__file__),"Wall Ovens")
HEIGHT_ABOVE_FLOOR = unit.inch(75)
#---------PRODUCT: COOK TOPS
        
class PRODUCT_Thermador_CEM304FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CEM304FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CEM304FS.blend")
        
class PRODUCT_Thermador_CEM365FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CEM365FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CEM365FS.blend")

class PRODUCT_Thermador_CES304FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CES304FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CES304FS.blend")

class PRODUCT_Thermador_CES365FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CES365FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CES365FS.blend")

class PRODUCT_Thermador_CES366FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CES366FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CES366FS.blend")

class PRODUCT_Thermador_CET304FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CET304FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CET304FS.blend")

class PRODUCT_Thermador_CET366FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CET366FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CET366FS.blend")

class PRODUCT_Thermador_CIS365GB(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIS365GB"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIS365GB.blend")

class PRODUCT_Thermador_CIT36XKB(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT36XKB"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT36XKB.blend")

class PRODUCT_Thermador_CIT304GB(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT304GB"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT304GB.blend")


class PRODUCT_Thermador_CIT304GM(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT304GM"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT304GM.blend")

class PRODUCT_Thermador_CIT304KB(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT304KB"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT304KB.blend")

class PRODUCT_Thermador_CIT304KBB(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT304KBB"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT304KBB.blend")

class PRODUCT_Thermador_CIT304KM(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT304KM"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT304KM.blend")


class PRODUCT_Thermador_CIT365GB(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT365GB"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT365GB.blend")

class PRODUCT_Thermador_CIT365KBB(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT365KBB"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT365KBB.blend")

class PRODUCT_Thermador_CIT365KM(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador CIT365KM"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador CIT365KM.blend")

class PRODUCT_Thermador_PCG304G(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador PCG304G"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador PCG304G.blend")

class PRODUCT_Thermador_PCG364GD(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador PCG364GD"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador PCG364GD.blend")

class PRODUCT_Thermador_PCG366G(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador PCG366G"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador PCG366G.blend")

class PRODUCT_Thermador_PCG486GD(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador PCG486GD"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador PCG486GD.blend")

class PRODUCT_Thermador_SGS304FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador SGS304FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador SGS304FS.blend")

class PRODUCT_Thermador_SGS305FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador SGS305FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador SGS305FS.blend")

class PRODUCT_Thermador_SGS365FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador SGS365FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador SGS365FS.blend")

class PRODUCT_Thermador_SGSL365KS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador SGSL365KS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador SGSL365KS.blend")

class PRODUCT_Thermador_SGSX305FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador SGSX305FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador SGSX305FS.blend")

class PRODUCT_Thermador_SGSX365FS(appliance_classes.Countertop_Appliance):
    
    def __init__(self):
        self.category_name = "Cook Tops"
        self.assembly_name = "Thermador SGSX365FS"
        self.appliance_path = os.path.join(COOKTOP_PATH,"Thermador SGSX365FS.blend")

#---------PRODUCT:RANGES    

class PRODUCT_Thermador_PRD304GHU(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRD304GHU"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRD304GHU.blend")
        
class PRODUCT_Thermador_PRD364GDHU(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRD364GDHU"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRD364GDHU.blend")
        
class PRODUCT_Thermador_PRD364JDGU(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRD364JDGU"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRD364JDGU.blend")
        
class PRODUCT_Thermador_PRD366GHU(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRD366GHU"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRD366GHU.blend")
        
class PRODUCT_Thermador_PRD366JGU(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRD366JGU"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRD366JGU.blend")
        
class PRODUCT_Thermador_PRD486GDHU(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRD486GDHU"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRD486GDHU.blend")
        
class PRODUCT_Thermador_PRD486JDGU(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRD486JDGU"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRD486JDGU.blend")
        
class PRODUCT_Thermador_PRG304GH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRG304GH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRG304GH.blend")
        
class PRODUCT_Thermador_PRG364GDH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRG364GDH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRG364GDH.blend")
        
class PRODUCT_Thermador_PRG364JDG(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRG364JDG"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRG364JDG.blend")
        
class PRODUCT_Thermador_PRG366GH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRG366GH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRG366GH.blend")
        
class PRODUCT_Thermador_PRG366JG(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRG366JG"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRG366JG.blend")
        
class PRODUCT_Thermador_PRG486GDH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRG486GDH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRG486GDH.blend")
        
class PRODUCT_Thermador_PRG486JDG(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRG486JDG"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRG486JDG.blend")
        
class PRODUCT_Thermador_PRL304GH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRL304GH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRL304GH.blend")
        
class PRODUCT_Thermador_PRL364GDH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRL364GDH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRL364GDH.blend")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
class PRODUCT_Thermador_PRL364JDG(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRL364JDG"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRL364JDG.blend")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
class PRODUCT_Thermador_PRL366GH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRL366GH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRL366GH.blend")
                                                                                      
class PRODUCT_Thermador_PRL366JG(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRL366JG"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRL366JG.blend")
                                                                                      
class PRODUCT_Thermador_PRL486GDH(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRL486GDH"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRL486GDH.blend")
                                                                                            
class PRODUCT_Thermador_PRL486JDG(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Ranges"
        self.assembly_name = "Thermador PRL486JDG"
        self.appliance_path = os.path.join(RANGE_PATH,"Thermador PRL486JDG.blend")
                                                           
#---------PRODUCT: WALL OVENS            
        
class PRODUCT_Thermador_ME301JP(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador ME301JP"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador ME301JP.blend")
                                                           
class PRODUCT_Thermador_ME301JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador ME301JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador ME301JS.blend")
                                                           
class PRODUCT_Thermador_ME302JP(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador ME302JP"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador ME302JP.blend")
                                                           
class PRODUCT_Thermador_ME302JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador ME302JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador ME302JS.blend")
                                                           
class PRODUCT_Thermador_MED271JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MED271JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MED271JS.blend")
                                                           
class PRODUCT_Thermador_MED272JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MED272JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MED272JS.blend")
                                                           
class PRODUCT_Thermador_MED301JP(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MED301JP"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MED301JP.blend")
                                                           
class PRODUCT_Thermador_MED301JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MED301JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MED301JS.blend")
                                                           
class PRODUCT_Thermador_MED302JP(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MED302JP"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MED302JP.blend")
                                                           
class PRODUCT_Thermador_MED302JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MED302JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MED302JS.blend")
                                                           
class PRODUCT_Thermador_MEDMC301JP(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MEDMC301JP"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MEDMC301JP.blend")
                                                           
class PRODUCT_Thermador_MEDMC301JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MEDMC301JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MEDMC301JS.blend")
                                    
class PRODUCT_Thermador_MEDMCW31JP(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MEDMCW31JP"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MEDMCW31JP.blend")
                                    
class PRODUCT_Thermador_MEDMCW31JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MEDMCW31JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MEDMCW31JS.blend")
                                    
class PRODUCT_Thermador_MEDMCW71JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MEDMCW71JS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MEDMCW71JS.blend")
                                    
class PRODUCT_Thermador_MES301HP(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MES301HP"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MES301HP.blend")
                                    
class PRODUCT_Thermador_MES301HS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador MES301HS"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador MES301HS.blend")
                                    
class PRODUCT_Thermador_POD301J(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador POD301J"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador POD301J.blend")
                                    
class PRODUCT_Thermador_PODC302J(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador PODC302J"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador PODC302J.blend")
                                    
class PRODUCT_Thermador_PODM301J(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador PODM301J"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador PODM301J.blend")
                                    
class PRODUCT_Thermador_PODMW301J(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Wall Ovens"
        self.assembly_name = "Thermador PODMW301J"
        self.appliance_path = os.path.join(WALL_OVEN_PATH,"Thermador PODMW301J.blend")
                                    

#---------PRODUCT: MICROWAVES 

class PRODUCT_Thermador_MBES(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Microwaves"
        self.assembly_name = "Thermador MBES"
        self.appliance_path = os.path.join(MICROWAVE_PATH,"Thermador MBES.blend")
                                    
class PRODUCT_Thermador_MCES(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Microwaves"
        self.assembly_name = "Thermador MCES"
        self.appliance_path = os.path.join(MICROWAVE_PATH,"Thermador MCES.blend")
                                    
class PRODUCT_Thermador_MD24JS(appliance_classes.Built_In_Appliance):
    
    def __init__(self):
        self.category_name = "Microwaves"
        self.assembly_name = "Thermador MD24JS"
        self.appliance_path = os.path.join(MICROWAVE_PATH,"Thermador MD24JS.blend")
                                    

#---------PRODUCT: RANGE HOODS

class PRODUCT_Thermador_HDDW36FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HDDW36FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HDDW36FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                                    
class PRODUCT_Thermador_HMCB36FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMCB36FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMCB36FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                                    
class PRODUCT_Thermador_HMCB42FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMCB42FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMCB42FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                                    
class PRODUCT_Thermador_HMCN36FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMCN36FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMCN36FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                                    
class PRODUCT_Thermador_HMCN42FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMCN42FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMCN42FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HMIB40HS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMIB40HS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMIB40HS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HMWB30FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMWB30FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMWB30FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HMWB36FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMWB36FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMWB36FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HMWN30FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMWN30FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMWN30FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HMWN36FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMWN36FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMWN36FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HMWN48FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HMWN48FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HMWN48FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
                             
class PRODUCT_Thermador_HPIB48HS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HPIB48HS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HPIB48HS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HPIN42HS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HPIN42HS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HPIN42HS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
                             
class PRODUCT_Thermador_HPWB30FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HPWB30FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HPWB30FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HPWB36FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HPWB36FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HPWB36FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HPWB48FS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HPWB48FS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HPWB48FS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HSB30BS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HSB30BS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HSB30BS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_HSB36BS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador HSB36BS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador HSB36BS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_PH30HS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador PH30HS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador PH30HS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR
                             
class PRODUCT_Thermador_PH36GS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador PH36GS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador PH36GS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

class PRODUCT_Thermador_PH36HS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador PH36HS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador PH36HS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

class PRODUCT_Thermador_PH42GS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador PH42GS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador PH42GS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

class PRODUCT_Thermador_PH48GS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador PH48GS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador PH48GS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

class PRODUCT_Thermador_PH48HS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Range Hoods"
        self.assembly_name = "Thermador PH48HS"
        self.appliance_path = os.path.join(RANGE_HOOD_PATH,"Thermador PH48HS.blend")
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

#---------PRODUCT: FRIDGES

class PRODUCT_Thermador_T18IW800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T18IW800SP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T18IW800SP.blend")

class PRODUCT_Thermador_T30BB810SS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T30BB810SS"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T30BB810SS.blend")

class PRODUCT_Thermador_T30IB800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T30IB800SP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T30IB800SP.blend")

class PRODUCT_Thermador_T30IF800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T30IF800SP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T30IF800SP.blend")

class PRODUCT_Thermador_T30IR800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T30IR800SP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T30IR800SP.blend")

class PRODUCT_Thermador_T36BB810SS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T36BB810SS"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T36BB810SS.blend")

class PRODUCT_Thermador_T36BB820SS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T36BB820SS"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T36BB820SS.blend")

class PRODUCT_Thermador_T36BT810NS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T36BT810NS"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T36BT810NS.blend")

class PRODUCT_Thermador_T36BT820NS(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T36BT820NS"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T36BT820NS.blend")

class PRODUCT_Thermador_T36IB800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T36IB800SP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T36IB800SP.blend")

class PRODUCT_Thermador_T36IT71NNP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T36IT71NNP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T36IT71NNP.blend")

class PRODUCT_Thermador_T36IT800NP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador T36IT800NP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T36IT800NP.blend")

class PRODUCT_Thermador_T24IR800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Fridges"
        self.assembly_name = "Thermador_T24IR800SP"
        self.appliance_path = os.path.join(FRIDGES_PATH,"Thermador T24IR800SP.blend")

#---------PRODUCT: FREEZERS

class PRODUCT_Thermador_T18ID800LP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Freezers"
        self.assembly_name = "Thermador T18ID800LP"
        self.appliance_path = os.path.join(FREEZERS_PATH,"Thermador T18ID800LP.blend")

class PRODUCT_Thermador_T18ID800RP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Freezers"
        self.assembly_name = "Thermador T18ID800RP"
        self.appliance_path = os.path.join(FREEZERS_PATH,"Thermador T18ID800RP.blend")

class PRODUCT_Thermador_T18IF800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Freezers"
        self.assembly_name = "Thermador T18IF800SP"
        self.appliance_path = os.path.join(FREEZERS_PATH,"Thermador T18IF800SP.blend")

class PRODUCT_Thermador_T24ID800LP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Freezers"
        self.assembly_name = "Thermador T24ID800LP"
        self.appliance_path = os.path.join(FREEZERS_PATH,"Thermador T24ID800LP.blend")

class PRODUCT_Thermador_T24ID800RP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Freezers"
        self.assembly_name = "Thermador T24ID800RP"
        self.appliance_path = os.path.join(FREEZERS_PATH,"Thermador T24ID800RP.blend")

class PRODUCT_Thermador_T24IF800SP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Freezers"
        self.assembly_name = "Thermador T24IF800SP"
        self.appliance_path = os.path.join(FREEZERS_PATH,"Thermador T24IF800SP.blend")

#---------PRODUCT: DISHWASHERS

class PRODUCT_Thermador_DWHD640JFM(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Dishwashers"
        self.assembly_name = "Thermador DWHD640JFM"
        self.appliance_path = os.path.join(DISH_WASHER_PATH,"Thermador DWHD640JFM.blend")

class PRODUCT_Thermador_DWHD651JFM(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Dishwashers"
        self.assembly_name = "Thermador DWHD651JFM"
        self.appliance_path = os.path.join(DISH_WASHER_PATH,"Thermador DWHD651JFM.blend")

class PRODUCT_Thermador_DWHD651JFP(appliance_classes.Static_Wall_Appliance):
    
    def __init__(self):
        self.category_name = "Dishwashers"
        self.assembly_name = "Thermador DWHD651JFP"
        self.appliance_path = os.path.join(DISH_WASHER_PATH,"Thermador DWHD651JFP.blend")











