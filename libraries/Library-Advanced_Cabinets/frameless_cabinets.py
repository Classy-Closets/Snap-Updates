"""
Microvellum 
Cabinets
Stores the logic for the different types of cabinets available in the Face Frame and 
Frameless library. Only controls how the different inserts are combined to assemble a cabinet.
No construction or machining information is stored here.
TODO: Create Face Frame Transition, Create Face Frame Outside Corner
"""

import bpy
from mv import unit, fd_types, utils
from . import cabinet_countertops
from . import cabinet_properties
from os import path

CUTPARTS_DIR = path.join(path.dirname(__file__),"Cabinet Assemblies","Cut Parts")
BLIND_PANEL = path.join(CUTPARTS_DIR,"Part with Edgebanding.blend")
MICROWAVE = path.join(path.dirname(__file__),"Appliances","Conventional Microwave.blend")
VENT = path.join(path.dirname(__file__),"Appliances","Wall Mounted Range Hood 01.blend")
REFRIGERATOR = path.join(path.dirname(__file__),"Appliances","Professional Refrigerator Generic.blend")

def add_price_prompt(assembly):
    
    assembly.add_tab(name='Main Options',tab_type='HIDDEN')
    assembly.add_prompt(name="Product Price Total",prompt_type='PRICE',value=assembly.product_price,tab_index=0,export=True)
    assembly.add_prompt(name="Product Cost Total",prompt_type='PRICE',value=assembly.product_price,tab_index=0,export=True)
    assembly.add_prompt(name="Product Cost Material",prompt_type='PRICE',value=0,tab_index=0,export=True)
    
def add_product_width_dimension(product):
    Product_Width = product.get_var('dim_x','Product_Width')
    
    vdim_x = fd_types.Dimension()
    vdim_x.parent(product.obj_bp)
    if product.mirror_z:
        vdim_x.start_z(value = unit.inch(5))
    else:
        vdim_x.start_z(value = -unit.inch(5))
    if product.carcass.carcass_type == 'Upper':
        vdim_x.start_y(value = unit.inch(8))
    else:
        vdim_x.start_y(value = unit.inch(3))
    vdim_x.end_x('Product_Width',[Product_Width])
    
def add_product_depth_dimension(product):
    Product_Depth = product.get_var('dim_y','Product_Depth')
    
    vdim_x = fd_types.Dimension()
    vdim_x.parent(product.obj_bp)
    if product.mirror_z:
        vdim_x.start_z(value = unit.inch(5))
    else:
        vdim_x.start_z(value = -unit.inch(5))
    if product.carcass.carcass_type == 'Upper':
        vdim_x.start_x(value = - unit.inch(8))
    else:
        vdim_x.start_x(value = - unit.inch(3))
    vdim_x.end_y('Product_Depth',[Product_Depth])
    
def add_countertop(product):
    product.add_prompt(name="Countertop Overhang Front",prompt_type='DISTANCE',value=unit.inch(1),tab_index=0)
    product.add_prompt(name="Countertop Overhang Back",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
    product.add_prompt(name="Countertop Overhang Left",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
    product.add_prompt(name="Countertop Overhang Right",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
    Countertop_Overhang_Front = product.get_var('Countertop Overhang Front')
    Countertop_Overhang_Left = product.get_var('Countertop Overhang Left')
    Countertop_Overhang_Right = product.get_var('Countertop Overhang Right')
    Countertop_Overhang_Back = product.get_var('Countertop Overhang Back')
    Left_Side_Wall_Filler = product.carcass.get_var('Left Side Wall Filler')
    Right_Side_Wall_Filler = product.carcass.get_var('Right Side Wall Filler')
    
    Width = product.get_var("dim_x","Width")
    Height = product.get_var("dim_z","Height")
    Depth = product.get_var("dim_y","Depth")
    
    ctop = cabinet_countertops.PRODUCT_Straight_Countertop()
    ctop.draw()
    ctop.obj_bp.mv.type_group = 'INSERT'
    ctop.obj_bp.parent = product.obj_bp
    ctop.x_loc('-Countertop_Overhang_Left-Left_Side_Wall_Filler',[Countertop_Overhang_Left,Left_Side_Wall_Filler])
    ctop.y_loc('Countertop_Overhang_Back',[Countertop_Overhang_Back])
    if product.carcass.carcass_type == "Suspended":
        ctop.z_loc(value = 0)
    else:
        ctop.z_loc('Height',[Height])
    ctop.x_rot(value = 0)
    ctop.y_rot(value = 0)
    ctop.z_rot(value = 0)
    ctop.x_dim('Width+Countertop_Overhang_Left+Countertop_Overhang_Right+Left_Side_Wall_Filler+Right_Side_Wall_Filler',
               [Width,Countertop_Overhang_Left,Countertop_Overhang_Right,Left_Side_Wall_Filler,Right_Side_Wall_Filler])
    ctop.y_dim('Depth-Countertop_Overhang_Front-Countertop_Overhang_Back',[Depth,Countertop_Overhang_Front,Countertop_Overhang_Back])
    ctop.z_dim(value = unit.inch(4))
    return ctop
    
def create_cabinet(product):
    product.create_assembly()
    product.obj_bp.mv.product_type = "Cabinet"
    add_price_prompt(product)
    add_product_width_dimension(product)
    
def add_carcass(product):
    Product_Width = product.get_var('dim_x','Product_Width')
    Product_Height = product.get_var('dim_z','Product_Height')
    Product_Depth = product.get_var('dim_y','Product_Depth')    
    
    product.carcass.draw()
    product.carcass.obj_bp.parent = product.obj_bp
    product.carcass.x_loc(value = 0)
    product.carcass.y_loc(value = 0)
    product.carcass.z_loc(value = 0)
    product.carcass.x_rot(value = 0)
    product.carcass.y_rot(value = 0)
    product.carcass.z_rot(value = 0)
    product.carcass.x_dim('Product_Width',[Product_Width])
    product.carcass.y_dim('Product_Depth',[Product_Depth])
    product.carcass.z_dim('Product_Height',[Product_Height])
    product.obj_bp.mv.product_sub_type = product.carcass.carcass_type

def add_insert(product,insert):
    if insert:
        if not insert.obj_bp:
            insert.draw()
            insert.obj_bp.parent = product.obj_bp
    
    Width = product.carcass.get_var("dim_x",'Width')
    Height = product.carcass.get_var("dim_z",'Height')
    Depth = product.carcass.get_var("dim_y",'Depth')
    Left_Side_Thickness = product.carcass.get_var("Left Side Thickness")
    Right_Side_Thickness = product.carcass.get_var("Right Side Thickness")
    Top_Thickness = product.carcass.get_var("Top Thickness")
    Bottom_Thickness = product.carcass.get_var("Bottom Thickness")
    Top_Inset = product.carcass.get_var("Top Inset")
    Bottom_Inset = product.carcass.get_var("Bottom Inset")
    Back_Inset = product.carcass.get_var("Back Inset")
    
    insert.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
    insert.y_loc('Depth',[Depth])
    if product.carcass.carcass_type in {"Base","Tall","Sink"}:
        insert.z_loc('Bottom_Inset',[Bottom_Inset])
    if product.carcass.carcass_type in {"Upper","Suspended"}:
        product.mirror_z = True
        insert.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
    insert.x_rot(value = 0)
    insert.y_rot(value = 0)
    insert.z_rot(value = 0)
    insert.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
    insert.y_dim('fabs(Depth)-Back_Inset',[Depth,Back_Inset])
    insert.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
    
    # ALLOW DOOR TO EXTEND TO TOP FOR VALANCE
    extend_top_amount = insert.get_prompt("Extend Top Amount")
    valance_height_top = product.carcass.get_prompt("Valance Height Top")

    if extend_top_amount and valance_height_top:
        Valance_Height_Top = product.carcass.get_var("Valance Height Top")
        Door_Valance_Top = product.carcass.get_var("Door Valance Top")
        Top_Reveal = insert.get_var("Top Reveal")
        
        insert.prompt('Extend Top Amount','IF(AND(Door_Valance_Top,Valance_Height_Top>0),Valance_Height_Top+Top_Thickness-Top_Reveal,0)',[Valance_Height_Top,Door_Valance_Top,Top_Thickness,Top_Reveal])
        
    # ALLOW DOOR TO EXTEND TO BOTTOM FOR VALANCE
    extend_bottom_amount = insert.get_prompt("Extend Bottom Amount")
    valance_height_bottom = product.carcass.get_prompt("Valance Height Bottom")
    
    if extend_bottom_amount and valance_height_bottom:
        Valance_Height_Bottom = product.carcass.get_var("Valance Height Bottom")
        Door_Valance_Bottom = product.carcass.get_var("Door Valance Bottom")
        Bottom_Reveal = insert.get_var("Bottom Reveal")
        
        insert.prompt('Extend Bottom Amount','IF(AND(Door_Valance_Bottom,Valance_Height_Bottom>0),Valance_Height_Bottom+Bottom_Thickness-Bottom_Reveal,0)',[Valance_Height_Bottom,Door_Valance_Bottom,Bottom_Thickness,Bottom_Reveal])
    
    # ALLOR DOOR TO EXTEND WHEN SUB FRONT IS FOUND
    sub_front_height = product.carcass.get_prompt("Sub Front Height")
    
    if extend_bottom_amount and sub_front_height:
        Sub_Front_Height = product.carcass.get_var("Sub Front Height")
        Top_Reveal = insert.get_var("Top Reveal")
        
        insert.prompt('Extend Top Amount','Sub_Front_Height-Top_Reveal',[Sub_Front_Height,Top_Reveal])

def add_opening(product):
    opening = product.add_opening()
    opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
    opening.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    opening.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    opening.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    opening.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    opening.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    opening.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    add_insert(product,opening)

def add_undercabinet_appliance(product,insert):
    Product_Width = product.get_var('dim_x','Product_Width')
    Product_Height = product.get_var('dim_z','Product_Height')
    Product_Depth = product.get_var('dim_y','Product_Depth')
        
    insert.x_loc(value = 0)
    insert.y_loc(value = 0)
    insert.z_loc('Product_Height',[Product_Height])
    insert.x_dim('Product_Width',[Product_Width])
    insert.y_dim('Product_Depth',[Product_Depth])

class Standard(fd_types.Assembly):
    """ Standard Frameless Cabinet
    """

    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".frameless_cabinet_prompts"
    plan_id = "framelss_standard.draw_plan"
    update_id = cabinet_properties.LIBRARY_NAME_SPACE + ".update"
    type_assembly = "PRODUCT"

    """ Type:fd_types.Assembly - The main carcass used
        The carcass must implement These Prompts:
        Left Side Thickness
        Right Side Thickness
        Top Thickness
        Bottom Thickness
        Top Inset
        Bottom Inset
        Back Inset 
        Left Side Wall Filler
        Right Side Wall Filler
    """
    carcass = None
    
    """ Type:fd_types.Assembly - Splitter insert to add to the cabinet """
    splitter = None
    
    """ Type:fd_types.Assembly - Interior insert to add to the cabinet """
    interior = None
    
    """ Type:fd_types.Assembly - Exterior insert to add to the cabinet """
    exterior = None
    
    """ Type:bool - This adds an empty opening to the carcass for starter products """
    add_empty_opening = False
    
    """ Type:bool - This adds a microwave below the cabinet. 
                        This is typically only used for upper cabinets """
    add_microwave = False
    
    """ Type:bool - This adds a vent below the cabinet. 
                        This is typically only used for upper cabinets """
    add_vent_hood = False
    
    """ Type:bool - This adds a countertop to the product. """    
    add_countertop = True
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0
    
    def draw(self):
        create_cabinet(self)
        self.obj_bp.mv.product_shape = 'RECTANGLE'
        
        add_carcass(self)

        if self.add_countertop and self.carcass.carcass_type in {"Base","Sink","Suspended"}:
            add_countertop(self)

        if self.splitter:
            add_insert(self,self.splitter)
            
        if self.interior:
            add_insert(self,self.interior)
            
        if self.exterior:
            add_insert(self,self.exterior)
            
        if self.add_empty_opening:
            add_opening(self)
            
        if self.add_vent_hood:
            vent = self.add_assembly(VENT)
            vent.set_name("Vent")
            add_undercabinet_appliance(self,vent)
            
        if self.add_microwave:
            microwave = self.add_assembly(MICROWAVE)
            microwave.set_name("Microwave")
            add_undercabinet_appliance(self,microwave)
        
class Refrigerator(fd_types.Assembly):
    """ Standard Frameless Cabinet
    """

    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".frameless_cabinet_prompts"
    type_assembly = "PRODUCT"
    update_id = cabinet_properties.LIBRARY_NAME_SPACE + ".update"
    
    """ Type:fd_types.Assembly - The main carcass used """
    carcass = None
    
    """ Type:fd_types.Assembly - Splitter insert to add to the cabinet """
    splitter = None
    
    """ Type:fd_types.Assembly - Interior insert to add to the cabinet """
    interior = None
    
    """ Type:fd_types.Assembly - Exterior insert to add to the cabinet """
    exterior = None
    
    """ Type:bool - This adds an empty opening to the carcass for starter products """
    add_empty_opening = False
    
    """ Type:bool - This adds a microwave below the cabinet. 
                        This is typically only used for upper cabinets """
    add_microwave = False
    
    """ Type:bool - This adds a vent below the cabinet. 
                        This is typically only used for upper cabinets """
    add_vent_hood = False
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0
    
    def draw(self):
        create_cabinet(self)
        self.obj_bp.mv.product_shape = 'RECTANGLE'
        
        add_carcass(self)

        if self.splitter:
            add_insert(self,self.splitter)
            
            Product_Width = self.get_var('dim_x','Product_Width')
            Product_Depth = self.get_var('dim_y','Product_Depth')
            Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
            Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")            
            Opening_2_Height = self.splitter.get_var("Opening 2 Height")
             
            ref = self.add_assembly(REFRIGERATOR)
            ref.set_name("Refrigerator")
            ref.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
            ref.y_loc(value = unit.inch(-6))
            ref.z_loc(value = 0)
            ref.x_dim('Product_Width-(Left_Side_Thickness+Right_Side_Thickness)',[Product_Width,Left_Side_Thickness,Right_Side_Thickness])
            ref.y_dim('Product_Depth',[Product_Depth])
            ref.z_dim('Opening_2_Height+INCH(4)',[Opening_2_Height])            
            
        self.update()
        
class Transition(fd_types.Assembly):
    
    library_name = "Cabinets - Frameless"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".frameless_cabinet_prompts"
    type_assembly = "PRODUCT"
    update_id = cabinet_properties.LIBRARY_NAME_SPACE + ".update"

    carcass = None
    interior = None
    exterior = None
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0    
    
    def add_doors(self):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Cabinet_Depth_Left = self.carcass.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.carcass.get_var("Cabinet Depth Right")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        self.exterior.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        self.exterior.y_loc('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        if self.carcass.carcass_type in {"Base","Tall"}:
            self.exterior.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type == "Upper":
            self.exterior.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
        self.exterior.x_rot(value = 0)
        self.exterior.y_rot(value = 0)
        self.exterior.z_rot('atan((Cabinet_Depth_Left-Cabinet_Depth_Right)/(Width-Left_Side_Thickness-Right_Side_Thickness))',
                            [Left_Side_Thickness,Cabinet_Depth_Right,Width,Right_Side_Thickness,Cabinet_Depth_Left])
        self.exterior.x_dim('sqrt(((Cabinet_Depth_Left-Cabinet_Depth_Right)**2)+((Width-Left_Side_Thickness-Right_Side_Thickness)**2))',
                            [Left_Side_Thickness,Cabinet_Depth_Right,Width,Right_Side_Thickness,Cabinet_Depth_Left])
        self.exterior.y_dim('Depth+Cabinet_Depth_Right+Right_Side_Thickness',[Depth,Cabinet_Depth_Right,Right_Side_Thickness])
        self.exterior.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
    def draw(self):
        create_cabinet(self)
        self.obj_bp.mv.product_shape = 'TRANSITION'
        
        add_carcass(self)
        
        if self.exterior:
            self.add_doors()
            
        self.update()
        
class Inside_Corner(fd_types.Assembly):
    
    library_name = "Cabinets - Frameless"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".frameless_cabinet_prompts"
    type_assembly = "PRODUCT"
    placement_type = "Corner"
    update_id = cabinet_properties.LIBRARY_NAME_SPACE + ".update"

    carcass = None
    interior = None
    exterior = None
    
    add_countertop = True
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0

    def add_pie_cut_doors(self):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Cabinet_Depth_Left = self.carcass.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.carcass.get_var("Cabinet Depth Right")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        self.exterior.x_loc('Cabinet_Depth_Left',[Cabinet_Depth_Left])
        self.exterior.y_loc('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        if self.carcass.carcass_type == "Base":
            self.exterior.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type == "Upper":
            self.exterior.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
        self.exterior.x_rot(value = 0)
        self.exterior.y_rot(value = 0)
        self.exterior.z_rot(value = 0)
        self.exterior.x_dim('Width-Cabinet_Depth_Left-Left_Side_Thickness',[Width,Cabinet_Depth_Left,Left_Side_Thickness])
        self.exterior.y_dim('Depth+Cabinet_Depth_Right+Right_Side_Thickness',[Depth,Cabinet_Depth_Right,Right_Side_Thickness])
        self.exterior.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
    def add_diagonal_doors(self):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Cabinet_Depth_Left = self.carcass.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.carcass.get_var("Cabinet Depth Right")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        self.exterior.x_loc('Cabinet_Depth_Left',[Cabinet_Depth_Left])
        self.exterior.y_loc('Depth+Left_Side_Thickness',[Depth,Left_Side_Thickness])
        if self.carcass.carcass_type == "Base":
            self.exterior.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type == "Upper":
            self.exterior.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
        self.exterior.x_rot(value = 0)
        self.exterior.y_rot(value = 0)
        self.exterior.z_rot('atan((fabs(Depth)-Left_Side_Thickness-Cabinet_Depth_Right)/(fabs(Width)-Right_Side_Thickness-Cabinet_Depth_Left))',[Depth,Left_Side_Thickness,Cabinet_Depth_Right,Width,Right_Side_Thickness,Cabinet_Depth_Left])
        self.exterior.x_dim('sqrt(((fabs(Depth)-Left_Side_Thickness-Cabinet_Depth_Right)**2)+((fabs(Width)-Right_Side_Thickness-Cabinet_Depth_Left)**2))',[Depth,Left_Side_Thickness,Cabinet_Depth_Right,Width,Right_Side_Thickness,Cabinet_Depth_Left])
        self.exterior.y_dim('Depth+Cabinet_Depth_Right+Right_Side_Thickness',[Depth,Cabinet_Depth_Right,Right_Side_Thickness])
        self.exterior.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
    def draw(self):
        create_cabinet(self)
        add_carcass(self)
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        
        add_product_depth_dimension(self)
        
        if self.add_countertop and self.carcass.carcass_type in {"Base","Sink","Suspended"}:
            self.add_prompt(name="Countertop Overhang",prompt_type='DISTANCE',value=unit.inch(1),tab_index=0)
            Countertop_Overhang = self.get_var('Countertop Overhang')
            Left_Side_Wall_Filler = self.carcass.get_var('Left Side Wall Filler')
            Right_Side_Wall_Filler = self.carcass.get_var('Right Side Wall Filler')
            Cabinet_Depth_Left = self.carcass.get_var('Cabinet Depth Left')
            Cabinet_Depth_Right = self.carcass.get_var('Cabinet Depth Right')
            
            if self.carcass.carcass_shape == "Notched":
                ctop = cabinet_countertops.PRODUCT_Notched_Corner_Countertop()
            else:
                ctop = cabinet_countertops.PRODUCT_Diagonal_Corner_Countertop()
            ctop.draw()
            ctop.obj_bp.mv.type_group = 'INSERT'
            ctop.obj_bp.parent = self.obj_bp
            ctop.x_loc(value = 0)
            ctop.y_loc(value = 0)
            ctop.z_loc('Product_Height',[Product_Height])
            ctop.x_rot(value = 0)
            ctop.y_rot(value = 0)
            ctop.z_rot(value = 0)
            ctop.x_dim('Product_Width+Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
            ctop.y_dim('Product_Depth-Left_Side_Wall_Filler',[Product_Depth,Left_Side_Wall_Filler])
            ctop.z_dim(value = unit.inch(4))
            ctop.prompt("Left Side Depth",'Cabinet_Depth_Left+Countertop_Overhang',[Cabinet_Depth_Left,Countertop_Overhang])
            ctop.prompt("Right Side Depth",'Cabinet_Depth_Right+Countertop_Overhang',[Cabinet_Depth_Right,Countertop_Overhang])
            
        if self.carcass.carcass_shape == 'Notched':
            self.obj_bp.mv.product_shape = 'INSIDE_NOTCH'
            if self.exterior:
                self.add_pie_cut_doors()
        
        if self.carcass.carcass_shape == 'Diagonal':
            self.obj_bp.mv.product_shape = 'INSIDE_DIAGONAL'
            if self.exterior:
                self.add_diagonal_doors()

        self.update()
        
class Outside_Corner(fd_types.Assembly):
    
    library_name = "Cabinets - Frameless"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".frameless_cabinet_prompts"
    type_assembly = "PRODUCT"
    placement_type = "Corner"
    update_id = cabinet_properties.LIBRARY_NAME_SPACE + ".update"

    carcass = None
    interior = None
    exterior = None
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0
    
    def draw(self):
        create_cabinet(self)

        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        
        self.carcass.draw()
        self.carcass.obj_bp.parent = self.obj_bp
        self.carcass.x_loc(value = 0)
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('fabs(Product_Depth)',[Product_Depth])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        self.obj_bp.mv.product_sub_type = self.carcass.carcass_type
        
        self.x_dim('fabs(Product_Depth)',[Product_Depth])
        
        if self.carcass.carcass_shape == 'Notched':
            self.obj_bp.mv.product_shape = 'OUTSIDE_NOTCH'
            if self.exterior:
                pass #TODO
        
        if self.carcass.carcass_shape == 'Diagonal':
            self.obj_bp.mv.product_shape = 'OUTSIDE_DIAGONAL'
            if self.exterior:
                pass #TODO
        
        self.update()
        
class Blind_Corner(fd_types.Assembly):
    
    library_name = "Cabinets - Frameless"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".frameless_cabinet_prompts"
    type_assembly = "PRODUCT"
    update_id = cabinet_properties.LIBRARY_NAME_SPACE + ".update"
    
    blind_side = "Left" # {Left, Right}
    
    carcass = None
    splitter = None
    interior = None
    exterior = None
    add_countertop = True
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0    
    
    def draw(self):
        props = cabinet_properties.get_scene_props().size_defaults
        create_cabinet(self)
        self.obj_bp.mv.product_shape = 'RECTANGLE'
        add_carcass(self)

        self.add_tab(name='Blind Corner Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        if self.carcass.carcass_type == 'Base':
            self.add_prompt(name="Blind Panel Width",prompt_type='DISTANCE',value=props.base_cabinet_depth,tab_index=1)
        if self.carcass.carcass_type == 'Tall':
            self.add_prompt(name="Blind Panel Width",prompt_type='DISTANCE',value=props.tall_cabinet_depth,tab_index=1)
        if self.carcass.carcass_type == 'Upper':
            self.mirror_z = True
            self.add_prompt(name="Blind Panel Width",prompt_type='DISTANCE',value=props.upper_cabinet_depth,tab_index=1)
        self.add_prompt(name="Blind Panel Reveal",prompt_type='DISTANCE',value=props.blind_panel_reveal,tab_index=1)
        self.add_prompt(name="Inset Blind Panel",prompt_type='CHECKBOX',value=props.inset_blind_panel,tab_index=1)
        self.add_prompt(name="Blind Panel Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=2)
        
        Blind_Panel_Width = self.get_var('Blind Panel Width')
        Blind_Panel_Reveal = self.get_var('Blind Panel Reveal')
        Inset_Blind_Panel = self.get_var('Inset Blind Panel')
        Blind_Panel_Thickness = self.get_var('Blind Panel Thickness')
        Carcass_Width = self.carcass.get_var("dim_x",'Carcass_Width')
        Carcass_Depth = self.carcass.get_var("dim_y",'Carcass_Depth')
        Carcass_Height = self.carcass.get_var("dim_z",'Carcass_Height')
        Toe_Kick_Height = self.carcass.get_var("Toe Kick Height")
        Top_Thickness = self.carcass.get_var("Top Thickness")
        Bottom_Thickness = self.carcass.get_var("Bottom Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Top_Inset = self.carcass.get_var("Top Inset",'Top_Inset')
        Bottom_Inset = self.carcass.get_var("Bottom Inset",'Bottom_Inset')
        Back_Inset = self.carcass.get_var("Back Inset",'Back_Inset')
        
        if self.add_countertop and self.carcass.carcass_type in {"Base","Sink","Suspended"}:
            ctop = add_countertop(self)
            ctop.prompt('Side Splash Setback',value=0)
            if self.blind_side == "Left":
                ctop.prompt('Add Left Backsplash',value=True)
            if self.blind_side == "Right":
                ctop.prompt('Add Right Backsplash',value=True)
        
        blind_panel = self.add_assembly(BLIND_PANEL)
        blind_panel.obj_bp.mv.name_object = "Blind Panel"
        if self.blind_side == "Left":
            blind_panel.x_loc('IF(Inset_Blind_Panel,Left_Side_Thickness,0)',[Inset_Blind_Panel,Left_Side_Thickness])
            blind_panel.y_dim('(Blind_Panel_Width+Blind_Panel_Reveal-IF(Inset_Blind_Panel,Left_Side_Thickness,0))*-1',[Blind_Panel_Width,Blind_Panel_Reveal,Inset_Blind_Panel,Left_Side_Thickness])
        if self.blind_side == "Right":
            blind_panel.x_loc('Carcass_Width-IF(Inset_Blind_Panel,Right_Side_Thickness,0)',[Carcass_Width,Inset_Blind_Panel,Right_Side_Thickness])
            blind_panel.y_dim('Blind_Panel_Width+Blind_Panel_Reveal-IF(Inset_Blind_Panel,Right_Side_Thickness,0)',[Blind_Panel_Width,Blind_Panel_Reveal,Right_Side_Thickness,Inset_Blind_Panel])
        blind_panel.y_loc('Carcass_Depth+IF(Inset_Blind_Panel,Blind_Panel_Thickness,0)',[Carcass_Depth,Inset_Blind_Panel,Blind_Panel_Thickness])
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            blind_panel.z_loc('Toe_Kick_Height+IF(Inset_Blind_Panel,Bottom_Thickness,0)',[Toe_Kick_Height,Inset_Blind_Panel,Bottom_Thickness])
            blind_panel.x_dim('Carcass_Height-Toe_Kick_Height-IF(Inset_Blind_Panel,Top_Thickness+Bottom_Thickness,0)',[Carcass_Height,Toe_Kick_Height,Inset_Blind_Panel,Top_Thickness,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            blind_panel.z_loc('Carcass_Height+Bottom_Inset-IF(Inset_Blind_Panel,0,Bottom_Thickness)',[Carcass_Height,Bottom_Inset,Inset_Blind_Panel,Bottom_Thickness])
            blind_panel.x_dim('fabs(Carcass_Height)-Top_Inset-Bottom_Inset+IF(Inset_Blind_Panel,0,Top_Thickness+Bottom_Thickness)',[Carcass_Height,Top_Inset,Bottom_Inset,Inset_Blind_Panel,Top_Thickness,Bottom_Thickness])
        blind_panel.x_rot(value = 0)
        blind_panel.y_rot(value = -90)
        blind_panel.z_rot(value = 90)
        blind_panel.z_dim('Blind_Panel_Thickness',[Blind_Panel_Thickness])
        blind_panel.cutpart("Cabinet_Blind_Panel")
        
        if self.splitter:
            self.splitter.draw()
            self.splitter.obj_bp.parent = self.obj_bp
            if self.blind_side == "Left":
                self.splitter.x_loc('Blind_Panel_Width+Blind_Panel_Reveal',[Blind_Panel_Width,Blind_Panel_Reveal])
            if self.blind_side == "Right":
                self.splitter.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
            self.splitter.y_loc('Carcass_Depth',[Carcass_Depth])
            if self.carcass.carcass_type in {"Base","Tall","Sink"}:
                self.splitter.z_loc('Bottom_Inset',[Bottom_Inset])
            if self.carcass.carcass_type in {"Upper","Suspended"}:
                self.splitter.z_loc('Carcass_Height+Bottom_Inset',[Carcass_Height,Bottom_Inset])
            self.splitter.x_rot(value = 0)
            self.splitter.y_rot(value = 0)
            self.splitter.z_rot(value = 0)
            if self.blind_side == "Left":
                self.splitter.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Right_Side_Thickness)',[Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Right_Side_Thickness])
            else:
                self.splitter.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Left_Side_Thickness)',[Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Left_Side_Thickness])
            self.splitter.y_dim('fabs(Carcass_Depth)-Back_Inset-IF(Inset_Blind_Panel,Blind_Panel_Thickness,0)',[Carcass_Depth,Back_Inset,Inset_Blind_Panel,Blind_Panel_Thickness])
            self.splitter.z_dim('fabs(Carcass_Height)-Bottom_Inset-Top_Inset',[Carcass_Height,Bottom_Inset,Top_Inset])
            
        if self.interior:
            self.interior.draw()
            self.interior.obj_bp.parent = self.obj_bp
            self.interior.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
            self.interior.y_loc('Carcass_Depth+IF(Inset_Blind_Panel,Blind_Panel_Thickness,0)',[Carcass_Depth,Inset_Blind_Panel,Blind_Panel_Thickness])
            if self.carcass.carcass_type in {"Base","Tall","Sink"}:
                self.interior.z_loc('Bottom_Inset',[Bottom_Inset])
            if self.carcass.carcass_type in {"Upper","Suspended"}:
                self.interior.z_loc('Carcass_Height+Bottom_Inset',[Carcass_Height,Bottom_Inset])
            self.interior.x_rot(value = 0)
            self.interior.y_rot(value = 0)
            self.interior.z_rot(value = 0)
            self.interior.x_dim('Carcass_Width-(Left_Side_Thickness+Right_Side_Thickness)',[Carcass_Width,Left_Side_Thickness,Right_Side_Thickness])
            self.interior.y_dim('fabs(Carcass_Depth)-Back_Inset-IF(Inset_Blind_Panel,Blind_Panel_Thickness,0)',[Carcass_Depth,Back_Inset,Inset_Blind_Panel,Blind_Panel_Thickness])
            self.interior.z_dim('fabs(Carcass_Height)-Bottom_Inset-Top_Inset',[Carcass_Height,Bottom_Inset,Top_Inset])
            
        if self.exterior:
            self.exterior.draw()
            self.exterior.obj_bp.parent = self.obj_bp
            if self.blind_side == "Left":
                self.exterior.x_loc('Blind_Panel_Width+Blind_Panel_Reveal',[Blind_Panel_Width,Blind_Panel_Reveal])
            if self.blind_side == "Right":
                self.exterior.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
            self.exterior.y_loc('Carcass_Depth',[Carcass_Depth])
            if self.carcass.carcass_type in {"Base","Tall","Sink"}:
                self.exterior.z_loc('Bottom_Inset',[Bottom_Inset])
            if self.carcass.carcass_type in {"Upper","Suspended"}:
                self.exterior.z_loc('Carcass_Height+Bottom_Inset',[Carcass_Height,Bottom_Inset])
            self.exterior.x_rot(value = 0)
            self.exterior.y_rot(value = 0)
            self.exterior.z_rot(value = 0)
            if self.blind_side == "Left":
                self.exterior.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Right_Side_Thickness)',[Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Right_Side_Thickness])
            else:
                self.exterior.x_dim('Carcass_Width-(Blind_Panel_Width+Blind_Panel_Reveal+Left_Side_Thickness)',[Carcass_Width,Blind_Panel_Width,Blind_Panel_Reveal,Left_Side_Thickness])
            self.exterior.y_dim('fabs(Carcass_Depth)-Back_Inset-IF(Inset_Blind_Panel,Blind_Panel_Thickness,0)',[Carcass_Depth,Back_Inset,Inset_Blind_Panel,Blind_Panel_Thickness])
            self.exterior.z_dim('fabs(Carcass_Height)-Bottom_Inset-Top_Inset',[Carcass_Height,Bottom_Inset,Top_Inset])
            
        self.update()
