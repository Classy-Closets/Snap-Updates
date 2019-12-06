"""
Microvellum 
Cabinets
Stores the logic for the different types of cabinets available in the Face Frame and 
Frameless library. Only controls how the different inserts are combined to assemble a cabinet.
No construction or machining information is stored here.
TODO: Create Face Frame Transition, Create Face Frame Outside Corner
"""

import bpy
from os import path
from mv import unit, fd_types, utils
from . import cabinet_countertops
from . import cabinet_face_frame
from . import cabinet_properties

CUTPARTS_DIR = path.join(path.dirname(__file__),"Cabinet Assemblies","Cut Parts")
BLIND_PANEL = path.join(CUTPARTS_DIR,"Part with Edgebanding.blend")
MICROWAVE = path.join(path.dirname(__file__),"Appliances","Conventional Microwave.blend")
VENT = path.join(path.dirname(__file__),"Appliances","Wall Mounted Range Hood 01.blend")
REFRIGERATOR = path.join(path.dirname(__file__),"Appliances","Professional Refrigerator Generic.blend")
FACE_FRAME = path.join(path.dirname(__file__),"Cabinet Assemblies","Face Frames","Face Frame.blend")
PIE_CUT_FACE_FRAME = path.join(path.dirname(__file__),"Cabinet Assemblies","Face Frames","Pie Cut Face Frame.blend")
MID_RAIL = path.join(CUTPARTS_DIR,"Part with Edgebanding.blend")

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
    


class Face_Frame_Standard(fd_types.Assembly):
    
    library_name = "Cabinets - Face Frame"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".face_frame_cabinet_prompts"
    type_assembly = "PRODUCT"

    carcass = None
    splitter = None
    interior = None
    exterior = None
    
    add_empty_opening = False
    
    add_countertop = True
    add_microwave = False
    add_vent_hood = False
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0    
    
    def set_drivers_for_assembly(self,assembly):
        Carcass_X = self.carcass.get_var("loc_x","Carcass_X")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Back_Inset = self.carcass.get_var("Back Inset")
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        
        assembly.x_loc('Carcass_X+Left_Side_Thickness',[Left_Side_Thickness,Carcass_X])
        assembly.y_loc('Depth',[Depth])
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            assembly.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            self.mirror_z = True
            assembly.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = 0)
        assembly.z_rot(value = 0)
        assembly.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        assembly.y_dim('fabs(Depth)-Back_Inset',[Depth,Back_Inset])
        assembly.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
    def draw(self):
        create_cabinet(self)
        self.obj_bp.mv.product_shape = 'RECTANGLE'
        
        self.add_tab(name='Face Frame Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        self.add_prompt(name="Top Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Bottom Rail Width",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=1)
        self.add_prompt(name="Left Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Right Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        
        self.carcass.draw()
        self.carcass.obj_bp.parent = self.obj_bp
        
        frame = cabinet_face_frame.Face_Frame()
        frame.draw()
        frame.obj_bp.parent = self.obj_bp
        frame.set_name("Face Frame")
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Top_Rail_Width = self.get_var("Top Rail Width")
        Bottom_Rail_Width = self.get_var("Bottom Rail Width")
        Left_Stile_Width = self.get_var("Left Stile Width")
        Right_Stile_Width = self.get_var("Right Stile Width")
        Frame_Thickness = frame.get_var("dim_y","Frame_Thickness")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Top_Thickness = self.carcass.get_var("Top Thickness")
        Toe_Kick_Height = self.carcass.get_var("Toe Kick Height")
        Bottom_Thickness = self.carcass.get_var("Bottom Thickness")
        Left_Fin_End = self.carcass.get_var("Left Fin End")
        Right_Fin_End = self.carcass.get_var("Right Fin End")
         
        add_product_width_dimension(self)
         
        self.carcass.x_loc('IF(Left_Fin_End,0,Left_Stile_Width-Left_Side_Thickness)',[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('Product_Width-IF(Left_Fin_End,0,Left_Stile_Width-Left_Side_Thickness)-IF(Right_Fin_End,0,Right_Stile_Width-Right_Side_Thickness)',[Product_Width,Left_Fin_End,Right_Fin_End,Left_Stile_Width,Left_Side_Thickness,Right_Stile_Width,Right_Side_Thickness])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        self.obj_bp.mv.product_sub_type = self.carcass.carcass_type
        
        if self.add_countertop and self.carcass.carcass_type in {"Base","Sink","Suspended"}:
            add_countertop(self)  
         
        frame.x_loc(value = 0)
        frame.y_loc('Product_Depth',[Product_Depth])
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            frame.z_loc('Toe_Kick_Height-Bottom_Rail_Width+Bottom_Thickness',[Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            frame.z_loc('Product_Height-Bottom_Rail_Width+Bottom_Thickness',[Product_Height,Bottom_Rail_Width,Bottom_Thickness])
        frame.x_rot(value = 0)
        frame.y_rot(value = 0)
        frame.z_rot(value = 0)
        frame.x_dim('Product_Width',[Product_Width])
        frame.y_dim(value = unit.inch(-.75))
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            frame.z_dim('Product_Height-Toe_Kick_Height+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            frame.z_dim('fabs(Product_Height)+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Bottom_Rail_Width,Bottom_Thickness])
        frame.prompt("Top Rail Width",'Top_Rail_Width',[Top_Rail_Width])
        frame.prompt("Bottom Rail Width",'Bottom_Rail_Width',[Bottom_Rail_Width])
        frame.prompt("Left Stile Width",'Left_Stile_Width',[Left_Stile_Width])
        frame.prompt("Right Stile Width",'Right_Stile_Width',[Right_Stile_Width])
 
        if self.interior:
            self.interior.draw()
            self.interior.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.interior)
 
        if self.exterior:
            self.exterior.draw()
            self.exterior.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.exterior)
            self.exterior.prompt("Frame Thickness","fabs(Frame_Thickness)",[Frame_Thickness])
            self.exterior.prompt("Frame Left Gap","IF(Left_Fin_End,Left_Stile_Width-Left_Side_Thickness,0)",[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
            self.exterior.prompt("Frame Right Gap","IF(Right_Fin_End,Right_Stile_Width-Right_Side_Thickness,0)",[Right_Fin_End,Right_Stile_Width,Right_Side_Thickness])
            self.exterior.prompt("Frame Top Gap","Top_Rail_Width-Top_Thickness",[Top_Rail_Width,Top_Thickness])
            self.exterior.prompt("Frame Bottom Gap",value = 0)
 
        if self.splitter:
            self.splitter.draw()
            self.splitter.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.splitter)
            self.splitter.prompt("Frame Thickness","fabs(Frame_Thickness)",[Frame_Thickness])
            self.splitter.prompt("Frame Left Gap","IF(Left_Fin_End,Left_Stile_Width-Left_Side_Thickness,0)",[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
            self.splitter.prompt("Frame Right Gap","IF(Right_Fin_End,Right_Stile_Width-Right_Side_Thickness,0)",[Right_Fin_End,Right_Stile_Width,Right_Side_Thickness])
            self.splitter.prompt("Frame Top Gap","Top_Rail_Width-Top_Thickness",[Top_Rail_Width,Top_Thickness])
            self.splitter.prompt("Frame Bottom Gap",value = 0)
 
        if self.add_vent_hood:
            self.add_prompt(name="Vent Height",prompt_type='DISTANCE',value= unit.inch(14),tab_index=0,export=False)
            Vent_Height = self.get_var('Vent Height')
            vent = self.add_assembly(VENT)
            vent.set_name("Vent")
            vent.x_loc(value = 0)
            vent.y_loc(value = 0)
            vent.z_loc('Product_Height-Vent_Height',[Product_Height,Vent_Height])
            vent.x_dim('Product_Width',[Product_Width])
            vent.y_dim('Product_Depth',[Product_Depth])
            vent.z_dim('Vent_Height',[Vent_Height])
            
        if self.add_microwave:
            vent = self.add_assembly(MICROWAVE)
            vent.set_name("Microwave")
            vent.x_loc(value = 0)
            vent.y_loc(value = 0)
            vent.z_loc('Product_Height',[Product_Height])
            vent.x_dim('Product_Width',[Product_Width])
            vent.y_dim('Product_Depth',[Product_Depth])
            
        if self.add_empty_opening:
            opening = self.add_opening()
            opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
            opening.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
            opening.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
            opening.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
            opening.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
            opening.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
            
            Frame_Thickness = frame.get_var("dim_y","Frame_Thickness")
            opening.prompt("Frame Thickness","fabs(Frame_Thickness)",[Frame_Thickness])
            opening.prompt("Frame Left Gap","IF(Left_Fin_End,Left_Stile_Width-Left_Side_Thickness,0)",[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
            opening.prompt("Frame Right Gap","IF(Right_Fin_End,Right_Stile_Width-Right_Side_Thickness,0)",[Right_Fin_End,Right_Stile_Width,Right_Side_Thickness])
            opening.prompt("Frame Top Gap","Top_Rail_Width-Top_Thickness",[Top_Rail_Width,Top_Thickness])
            opening.prompt("Frame Bottom Gap",value = 0)
            self.set_drivers_for_assembly(opening)
            
        self.update()

class Face_Frame_Refrigerator(fd_types.Assembly):
    
    library_name = "Cabinets - Face Frame"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".face_frame_cabinet_prompts"
    type_assembly = "PRODUCT"

    carcass = None
    splitter = None
    interior = None
    exterior = None

    """ Type:float - This is the base price for the product. """   
    product_price = 0

    def set_drivers_for_assembly(self,assembly):
        Carcass_X = self.carcass.get_var("loc_x","Carcass_X")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Back_Inset = self.carcass.get_var("Back Inset")
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        
        assembly.x_loc('Carcass_X+Left_Side_Thickness',[Left_Side_Thickness,Carcass_X])
        assembly.y_loc('Depth',[Depth])
        assembly.z_loc('Bottom_Inset',[Bottom_Inset])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = 0)
        assembly.z_rot(value = 0)
        assembly.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        assembly.y_dim('fabs(Depth)-Back_Inset',[Depth,Back_Inset])
        assembly.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
    def draw(self):
        create_cabinet(self)
        self.obj_bp.mv.product_shape = 'RECTANGLE'
        
        self.add_tab(name='Face Frame Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        self.add_prompt(name="Top Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Bottom Rail Width",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=1)
        self.add_prompt(name="Left Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Right Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        
        self.carcass.draw()
        self.carcass.obj_bp.parent = self.obj_bp
        
        frame = self.add_assembly(FACE_FRAME)
        frame.set_name("Face Frame")
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Top_Rail_Width = self.get_var("Top Rail Width")
        Bottom_Rail_Width = self.get_var("Bottom Rail Width")
        Left_Stile_Width = self.get_var("Left Stile Width")
        Right_Stile_Width = self.get_var("Right Stile Width")
        Frame_Thickness = frame.get_var("dim_y","Frame_Thickness")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Top_Thickness = self.carcass.get_var("Top Thickness")
        Toe_Kick_Height = self.carcass.get_var("Toe Kick Height")
        Bottom_Thickness = self.carcass.get_var("Bottom Thickness")
        Left_Fin_End = self.carcass.get_var("Left Fin End")
        Right_Fin_End = self.carcass.get_var("Right Fin End")
        
        self.carcass.x_loc('IF(Left_Fin_End,0,Left_Stile_Width-Left_Side_Thickness)',[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('Product_Width-IF(Left_Fin_End,0,Left_Stile_Width-Left_Side_Thickness)-IF(Right_Fin_End,0,Right_Stile_Width-Right_Side_Thickness)',[Product_Width,Left_Fin_End,Right_Fin_End,Left_Stile_Width,Left_Side_Thickness,Right_Stile_Width,Right_Side_Thickness])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        self.obj_bp.mv.product_sub_type = self.carcass.carcass_type
        
        add_product_width_dimension(self)
        
        frame.x_loc(value = 0)
        frame.y_loc('Product_Depth',[Product_Depth])
        frame.z_loc(value = 0)
        frame.x_rot(value = 0)
        frame.y_rot(value = 0)
        frame.z_rot(value = 0)
        frame.x_dim('Product_Width',[Product_Width])
        frame.y_dim(value = unit.inch(-.75))
        frame.z_dim('Product_Height',[Product_Height])
        frame.prompt("Top Rail Width",'Top_Rail_Width',[Top_Rail_Width])
        frame.prompt("Bottom Rail Width",'Bottom_Rail_Width',[Bottom_Rail_Width])
        frame.prompt("Left Stile Width",'Left_Stile_Width',[Left_Stile_Width])
        frame.prompt("Right Stile Width",'Right_Stile_Width',[Right_Stile_Width])
        frame.prompt("Remove Bottom Rail",value=True)
        frame.material("Exposed_Exterior_Surface")
        
        if self.interior:
            self.interior.draw()
            self.interior.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.interior)
            
        if self.exterior:
            self.exterior.draw()
            self.exterior.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.exterior)
            self.exterior.prompt("Frame Thickness","fabs(Frame_Thickness)",[Frame_Thickness])
            self.exterior.prompt("Frame Left Gap","IF(Left_Fin_End,Left_Stile_Width-Left_Side_Thickness,0)",[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
            self.exterior.prompt("Frame Right Gap","IF(Right_Fin_End,Right_Stile_Width-Right_Side_Thickness,0)",[Right_Fin_End,Right_Stile_Width,Right_Side_Thickness])
            self.exterior.prompt("Frame Top Gap","Top_Rail_Width-Top_Thickness",[Top_Rail_Width,Top_Thickness])
            self.exterior.prompt("Frame Bottom Gap",value = 0)

        if self.splitter:
            self.splitter.draw()
            self.splitter.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.splitter)
            self.splitter.prompt("Frame Thickness","fabs(Frame_Thickness)",[Frame_Thickness])
            self.splitter.prompt("Frame Left Gap","IF(Left_Fin_End,Left_Stile_Width-Left_Side_Thickness,0)",[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
            self.splitter.prompt("Frame Right Gap","IF(Right_Fin_End,Right_Stile_Width-Right_Side_Thickness,0)",[Right_Fin_End,Right_Stile_Width,Right_Side_Thickness])
            self.splitter.prompt("Frame Top Gap","Top_Rail_Width-Top_Thickness",[Top_Rail_Width,Top_Thickness])
            self.splitter.prompt("Frame Bottom Gap",value = 0)
            
            Opening_2_Height = self.splitter.get_var("Opening 2 Height")
            
            ref = self.add_assembly(REFRIGERATOR)
            ref.set_name("Refrigerator")
            ref.x_loc('Left_Stile_Width',[Left_Stile_Width])
            ref.y_loc(value = unit.inch(-6))
            ref.z_loc(value = 0)
            ref.x_dim('Product_Width-(Left_Stile_Width+Right_Stile_Width)',[Product_Width,Left_Stile_Width,Right_Stile_Width])
            ref.y_dim('Product_Depth',[Product_Depth])
            ref.z_dim('Opening_2_Height',[Opening_2_Height])

        self.update()

class Face_Frame_Blind_Corner(fd_types.Assembly):
    
    library_name = "Cabinets - Face Frame"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".face_frame_cabinet_prompts"
    type_assembly = "PRODUCT"

    carcass = None
    splitter = None
    interior = None
    exterior = None
    add_countertop = True
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0    
    
    def set_drivers_for_assembly(self,assembly):
        Carcass_X = self.carcass.get_var("loc_x","Carcass_X")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness",'Left_Side_Thickness')
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness",'Right_Side_Thickness')
        Top_Inset = self.carcass.get_var("Top Inset",'Top_Inset')
        Bottom_Inset = self.carcass.get_var("Bottom Inset",'Bottom_Inset')
        Back_Inset = self.carcass.get_var("Back Inset",'Back_Inset')
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        
        assembly.x_loc('Carcass_X+Left_Side_Thickness',[Left_Side_Thickness,Carcass_X])
        assembly.y_loc('Depth',[Depth])
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            assembly.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            self.mirror_z = True
            assembly.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = 0)
        assembly.z_rot(value = 0)
        assembly.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        assembly.y_dim('fabs(Depth)-Back_Inset',[Depth,Back_Inset])
        assembly.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
    def draw(self):
        props = cabinet_properties.get_scene_props()
        create_cabinet(self)
        self.obj_bp.mv.product_shape = 'RECTANGLE'

        self.carcass.draw()
        self.carcass.obj_bp.parent = self.obj_bp

        self.add_tab(name='Face Frame Options',tab_type='VISIBLE')
        self.add_tab(name='Blind Panel Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        self.add_prompt(name="Top Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Bottom Rail Width",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=1)
        self.add_prompt(name="Left Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Right Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        if self.carcass.carcass_type == 'Base':
            self.add_prompt(name="Blind Width",prompt_type='DISTANCE',value=props.base_cabinet_depth + unit.inch(1),tab_index=2)
        if self.carcass.carcass_type == 'Tall':
            self.add_prompt(name="Blind Width",prompt_type='DISTANCE',value=props.tall_cabinet_depth + unit.inch(1),tab_index=2)
        if self.carcass.carcass_type == 'Upper':
            self.add_prompt(name="Blind Width",prompt_type='DISTANCE',value=props.upper_cabinet_depth + unit.inch(1),tab_index=2)
        self.add_prompt(name="Blind Panel Width",prompt_type='DISTANCE',value=unit.inch(6),tab_index=2)
        self.add_prompt(name="Blind Panel Reveal",prompt_type='DISTANCE',value=props.blind_panel_reveal,tab_index=2)
        self.add_prompt(name="Inset Blind Panel",prompt_type='CHECKBOX',value=props.inset_blind_panel,tab_index=2)
        self.add_prompt(name="Blind Panel Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=3)

        frame = self.add_assembly(FACE_FRAME)
        frame.set_name("Face Frame")
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Top_Rail_Width = self.get_var("Top Rail Width")
        Bottom_Rail_Width = self.get_var("Bottom Rail Width")
        Left_Stile_Width = self.get_var("Left Stile Width")
        Right_Stile_Width = self.get_var("Right Stile Width")
        Blind_Panel_Width = self.get_var("Blind Panel Width")
        Blind_Panel_Reveal = self.get_var("Blind Panel Reveal")
        Blind_Width = self.get_var("Blind Width")
        
        Frame_Thickness = frame.get_var("dim_y","Frame_Thickness")
        Frame_Z_Loc = frame.get_var("loc_z",'Frame_Z_Loc')
        Frame_Y_Loc = frame.get_var("loc_y",'Frame_Y_Loc')
        Frame_Height = frame.get_var("dim_z","Frame_Height")

        Carcass_Depth = self.carcass.get_var("dim_y",'Carcass_Depth')
        Carcass_Height = self.carcass.get_var("dim_z",'Carcass_Height')
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Toe_Kick_Height = self.carcass.get_var("Toe Kick Height")
        Bottom_Thickness = self.carcass.get_var("Bottom Thickness")
        Bottom_Inset = self.carcass.get_var("Bottom Inset",'Bottom_Inset')
        Back_Inset = self.carcass.get_var("Back Inset",'Back_Inset')
        Left_Fin_End = self.carcass.get_var("Left Fin End")
        Right_Fin_End = self.carcass.get_var("Right Fin End")
        
        self.carcass.x_loc('IF(Left_Fin_End,0,Left_Stile_Width-Left_Side_Thickness)',[Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])
        self.carcass.y_loc(value = 0)
        self.carcass.z_loc(value = 0)
        self.carcass.x_rot(value = 0)
        self.carcass.y_rot(value = 0)
        self.carcass.z_rot(value = 0)
        self.carcass.x_dim('Product_Width-IF(Left_Fin_End,0,Left_Stile_Width-Left_Side_Thickness)-IF(Right_Fin_End,0,Right_Stile_Width-Right_Side_Thickness)',[Product_Width,Left_Fin_End,Right_Fin_End,Left_Stile_Width,Left_Side_Thickness,Right_Stile_Width,Right_Side_Thickness])
        self.carcass.y_dim('Product_Depth',[Product_Depth])
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        self.obj_bp.mv.product_sub_type = self.carcass.carcass_type
        
        add_product_width_dimension(self)
        
        if self.add_countertop and self.carcass.carcass_type in {"Base","Sink","Suspended"}:
            ctop = add_countertop(self)
            ctop.prompt('Side Splash Setback',value=0)
            if self.blind_side == "Left":
                ctop.prompt('Add Left Backsplash',value=True)
            if self.blind_side == "Right":
                ctop.prompt('Add Right Backsplash',value=True)        
        
        frame.x_loc(value = 0)
        frame.y_loc('Product_Depth',[Product_Depth])
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            frame.z_loc('Toe_Kick_Height-Bottom_Rail_Width+Bottom_Thickness',[Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            frame.z_loc('Product_Height-Bottom_Rail_Width+Bottom_Thickness',[Product_Height,Bottom_Rail_Width,Bottom_Thickness])
        frame.x_rot(value = 0)
        frame.y_rot(value = 0)
        frame.z_rot(value = 0)
        frame.x_dim('Product_Width',[Product_Width])
        frame.y_dim(value = unit.inch(-.75))
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            frame.z_dim('Product_Height-Toe_Kick_Height+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            frame.z_dim('fabs(Product_Height)+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Bottom_Rail_Width,Bottom_Thickness])
        frame.prompt("Top Rail Width",'Top_Rail_Width',[Top_Rail_Width])
        frame.prompt("Bottom Rail Width",'Bottom_Rail_Width',[Bottom_Rail_Width])
        frame.prompt("Left Stile Width",'Left_Stile_Width',[Left_Stile_Width])
        frame.prompt("Right Stile Width",'Right_Stile_Width',[Right_Stile_Width])
        frame.material("Exposed_Exterior_Surface")
        
        mid_rail = self.add_assembly(MID_RAIL)  
        mid_rail.set_name("Mid Rail")
        if self.blind_side == "Left":
            mid_rail.x_loc('Blind_Width+Blind_Panel_Reveal',[Blind_Width,Blind_Panel_Reveal])
        if self.blind_side == "Right":
            mid_rail.x_loc('Product_Width-(Blind_Width+Blind_Panel_Reveal-Blind_Panel_Width)',[Product_Width,Blind_Width,Blind_Panel_Width,Blind_Panel_Reveal])
        mid_rail.y_loc('Frame_Y_Loc',[Frame_Y_Loc])
        mid_rail.z_loc('Frame_Z_Loc+Bottom_Rail_Width',[Frame_Z_Loc,Bottom_Rail_Width])
        mid_rail.x_rot(value = 0)
        mid_rail.y_rot(value = -90)
        mid_rail.z_rot(value = 90)
        mid_rail.x_dim('Frame_Height-(Top_Rail_Width+Bottom_Rail_Width)',[Frame_Height,Top_Rail_Width,Bottom_Rail_Width])
        mid_rail.y_dim('Blind_Panel_Width',[Blind_Panel_Width])
        mid_rail.z_dim(value = unit.inch(.75))
        mid_rail.cutpart("Cabinet_Door")
        mid_rail.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        
        if self.interior:
            self.interior.draw()
            self.interior.obj_bp.parent = self.obj_bp
            self.set_drivers_for_assembly(self.interior)
            
        if self.exterior:
            self.exterior.draw()
            self.exterior.obj_bp.parent = self.obj_bp
            if self.blind_side == "Left":
                self.exterior.x_loc('Blind_Width+Blind_Panel_Reveal',[Blind_Width,Blind_Panel_Reveal])
            else:
                self.exterior.x_loc('Left_Stile_Width',[Left_Stile_Width])
            self.exterior.y_loc('Carcass_Depth+Frame_Thickness',[Carcass_Depth,Frame_Thickness])
            if self.carcass.carcass_type in {"Base","Tall","Sink"}:
                self.exterior.z_loc('Frame_Z_Loc+Bottom_Rail_Width',[Frame_Z_Loc,Bottom_Rail_Width])
            if self.carcass.carcass_type in {"Upper","Suspended"}:
                self.exterior.z_loc('Carcass_Height+Bottom_Inset',[Carcass_Height,Bottom_Inset])
            self.exterior.x_rot(value = 0)
            self.exterior.y_rot(value = 0)
            self.exterior.z_rot(value = 0)
            if self.blind_side == "Left":
                self.exterior.x_dim('Product_Width-(Blind_Width+Blind_Panel_Reveal+Right_Stile_Width)',[Product_Width,Blind_Width,Blind_Panel_Reveal,Right_Stile_Width])
            else:
                self.exterior.x_dim('Product_Width-(Blind_Width+Blind_Panel_Reveal+Left_Stile_Width)',[Product_Width,Blind_Width,Blind_Panel_Reveal,Left_Stile_Width])
            self.exterior.y_dim('fabs(Carcass_Depth)-Back_Inset',[Carcass_Depth,Back_Inset])
            self.exterior.z_dim('Frame_Height-Top_Rail_Width-Bottom_Rail_Width',[Frame_Height,Top_Rail_Width,Bottom_Rail_Width])
            
        if self.splitter:
            self.splitter.draw()
            self.splitter.obj_bp.parent = self.obj_bp
            if self.blind_side == "Left":
                self.splitter.x_loc('Blind_Width+Blind_Panel_Reveal',[Blind_Width,Blind_Panel_Reveal])
            else:
                self.splitter.x_loc('Left_Stile_Width',[Left_Stile_Width])
            self.splitter.y_loc('Carcass_Depth+Frame_Thickness',[Carcass_Depth,Frame_Thickness])
            if self.carcass.carcass_type in {"Base","Tall","Sink"}:
                self.splitter.z_loc('Frame_Z_Loc+Bottom_Rail_Width',[Frame_Z_Loc,Bottom_Rail_Width])
            if self.carcass.carcass_type in {"Upper","Suspended"}:
                self.splitter.z_loc('Carcass_Height+Bottom_Inset',[Carcass_Height,Bottom_Inset])
            self.splitter.x_rot(value = 0)
            self.splitter.y_rot(value = 0)
            self.splitter.z_rot(value = 0)
            if self.blind_side == "Left":
                self.splitter.x_dim('Product_Width-(Blind_Width+Blind_Panel_Reveal+Right_Stile_Width)',[Product_Width,Blind_Width,Blind_Panel_Reveal,Right_Stile_Width])
            else:
                self.splitter.x_dim('Product_Width-(Blind_Width+Blind_Panel_Reveal+Left_Stile_Width)',[Product_Width,Blind_Width,Blind_Panel_Reveal,Left_Stile_Width])
            self.splitter.y_dim('fabs(Carcass_Depth)-Back_Inset',[Carcass_Depth,Back_Inset])
            self.splitter.z_dim('Frame_Height-Top_Rail_Width-Bottom_Rail_Width',[Frame_Height,Top_Rail_Width,Bottom_Rail_Width])
            
        self.update()

class Face_Frame_Inside_Corner(fd_types.Assembly):
    
    library_name = "Cabinets - Face Frame"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".face_frame_cabinet_prompts"
    type_assembly = "PRODUCT"
    placement_type = "Corner"

    carcass = None
    interior = None
    exterior = None
    face_frame = None
    
    """ Type:float - This is the base price for the product. """   
    product_price = 0
    
    def set_drivers_for_assembly(self,assembly):
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Back_Inset = self.carcass.get_var("Back Inset")
        
        assembly.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        assembly.y_loc('Depth',[Depth])
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            assembly.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            self.mirror_z = True
            assembly.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = 0)
        assembly.z_rot(value = 0)
        assembly.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        assembly.y_dim('fabs(Depth)-Back_Inset',[Depth,Back_Inset])
        assembly.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
    def add_pie_cut_ff_and_doors(self):
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth') 
        Top_Rail_Width = self.get_var('Top Rail Width','Top_Rail_Width')   
        Bottom_Rail_Width = self.get_var('Bottom Rail Width','Bottom_Rail_Width') 
        Left_Stile_Width = self.get_var('Left Stile Width','Left_Stile_Width') 
        Right_Stile_Width = self.get_var('Right Stile Width','Right_Stile_Width')                
        
        Carcass_Width = self.carcass.get_var("dim_x",'Carcass_Width')
        Carcass_Height = self.carcass.get_var("dim_z",'Carcass_Height')
        Carcass_Depth = self.carcass.get_var("dim_y",'Carcass_Depth')
        Left_Depth = self.carcass.get_var('Cabinet Depth Left','Left_Depth')
        Right_Depth = self.carcass.get_var('Cabinet Depth Right','Right_Depth') 
        Toe_Kick_Height = self.carcass.get_var("Toe Kick Height")        
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Cabinet_Depth_Left = self.carcass.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.carcass.get_var("Cabinet Depth Right")
        Left_Fin_End = self.carcass.get_var("Left Fin End")
        Right_Fin_End = self.carcass.get_var("Right Fin End")        
        Top_Thickness = self.carcass.get_var("Top Thickness")
        Bottom_Thickness = self.carcass.get_var("Bottom Thickness")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness") 
        
        face_frame = self.add_assembly(PIE_CUT_FACE_FRAME)    
        face_frame.set_name("Face Frame")          
        
        face_frame.x_loc('Left_Depth',[Left_Depth])
        face_frame.y_loc('-Right_Depth',[Right_Depth])
        
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            face_frame.z_loc('Toe_Kick_Height-Bottom_Rail_Width+Bottom_Thickness',[Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            face_frame.z_loc('Product_Height-Bottom_Rail_Width+Bottom_Thickness',[Product_Height,Bottom_Rail_Width,Bottom_Thickness])        
        
        face_frame.x_dim('Product_Width-Left_Depth',[Left_Depth,Product_Width])
        face_frame.y_dim('Product_Depth+Right_Depth',[Right_Depth,Product_Depth])
        
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            face_frame.z_dim('Product_Height-Toe_Kick_Height+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            face_frame.z_dim('fabs(Product_Height)+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Bottom_Rail_Width,Bottom_Thickness])        
        
        face_frame.prompt("Top Rail Width",'Top_Rail_Width',[Top_Rail_Width])
        face_frame.prompt("Bottom Rail Width",'Bottom_Rail_Width',[Bottom_Rail_Width])
        face_frame.prompt("Left Stile Width",'Left_Stile_Width',[Left_Stile_Width])
        face_frame.prompt("Right Stile Width",'Right_Stile_Width',[Right_Stile_Width])          
        
        Face_Frame_Thickness = face_frame.get_var("Face Frame Thickness")
        Top_Rail_Width = face_frame.get_var("Top Rail Width")
        Left_Stile_Width = face_frame.get_var("Left Stile Width")
        Right_Stile_Width = face_frame.get_var("Right Stile Width")
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        self.exterior.x_dim('Carcass_Width-Right_Side_Thickness',[Carcass_Width,Right_Side_Thickness])
        self.exterior.y_dim('Carcass_Depth+Left_Side_Thickness',[Carcass_Depth,Left_Side_Thickness])
        self.exterior.z_dim('fabs(Carcass_Height)-Bottom_Inset-Top_Inset',[Carcass_Height,Bottom_Inset,Top_Inset])
        
        if self.carcass.carcass_type == "Base":
            self.exterior.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type == "Upper":
            self.exterior.z_loc('Carcass_Height+Bottom_Inset',[Carcass_Height,Bottom_Inset])
            
        self.exterior.z_rot("",[])
            
        self.exterior.prompt("Left Side Depth","Cabinet_Depth_Left+Face_Frame_Thickness",[Cabinet_Depth_Left,Face_Frame_Thickness])
        self.exterior.prompt("Right Side Depth","Cabinet_Depth_Right+Face_Frame_Thickness",[Cabinet_Depth_Right,Face_Frame_Thickness])
        self.exterior.prompt("Frame Left Gap","IF(Left_Fin_End,Left_Stile_Width-Left_Side_Thickness,0)",[Left_Side_Thickness,Left_Fin_End,Left_Stile_Width])
        self.exterior.prompt("Frame Right Gap","IF(Right_Fin_End,Right_Stile_Width-Right_Side_Thickness,0)",[Right_Side_Thickness,Right_Fin_End,Right_Stile_Width])
        self.exterior.prompt("Frame Top Gap","Top_Rail_Width-Top_Thickness",[Top_Thickness,Top_Rail_Width])
        
    def add_diagonal_ff_and_doors(self):
        Product_Height = self.get_var('dim_z','Product_Height')
        Top_Rail_Width = self.get_var('Top Rail Width','Top_Rail_Width')   
        Bottom_Rail_Width = self.get_var('Bottom Rail Width','Bottom_Rail_Width') 
        Left_Stile_Width = self.get_var('Left Stile Width','Left_Stile_Width') 
        Right_Stile_Width = self.get_var('Right Stile Width','Right_Stile_Width')         
        
        Width = self.carcass.get_var("dim_x",'Width')
        Height = self.carcass.get_var("dim_z",'Height')
        Depth = self.carcass.get_var("dim_y",'Depth')
        Top_Inset = self.carcass.get_var("Top Inset")
        Bottom_Inset = self.carcass.get_var("Bottom Inset")
        Cabinet_Depth_Left = self.carcass.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.carcass.get_var("Cabinet Depth Right")
        Toe_Kick_Height = self.carcass.get_var("Toe Kick Height")
        Top_Thickness = self.carcass.get_var("Top Thickness")
        Bottom_Thickness = self.carcass.get_var("Bottom Thickness")
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        
        #FACE FRAME
        face_frame = self.add_assembly(FACE_FRAME)    
        face_frame.set_name("Face Frame")        
        
        face_frame.x_loc('Cabinet_Depth_Left',[Cabinet_Depth_Left])   
        face_frame.y_loc('Depth+Left_Side_Thickness',[Depth,Left_Side_Thickness]) 

        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            face_frame.z_dim('Product_Height-Toe_Kick_Height+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            face_frame.z_dim('fabs(Product_Height)+(Bottom_Rail_Width-Bottom_Thickness)',[Product_Height,Bottom_Rail_Width,Bottom_Thickness]) 
            
        if self.carcass.carcass_type in {"Base","Tall","Sink"}:
            face_frame.z_loc('Toe_Kick_Height-Bottom_Rail_Width+Bottom_Thickness',[Toe_Kick_Height,Bottom_Rail_Width,Bottom_Thickness])
        if self.carcass.carcass_type in {"Upper","Suspended"}:
            face_frame.z_loc('Product_Height-Bottom_Rail_Width+Bottom_Thickness',[Product_Height,Bottom_Rail_Width,Bottom_Thickness])                
            
        face_frame.z_rot('atan((fabs(Depth)-Left_Side_Thickness-Cabinet_Depth_Right)/(fabs(Width)-Right_Side_Thickness-Cabinet_Depth_Left))',[Depth,Left_Side_Thickness,Cabinet_Depth_Right,Width,Right_Side_Thickness,Cabinet_Depth_Left])
        face_frame.x_dim('sqrt(((fabs(Depth)-Left_Side_Thickness-Cabinet_Depth_Right)**2)+((fabs(Width)-Right_Side_Thickness-Cabinet_Depth_Left)**2))',
                         [Depth,Left_Side_Thickness,Cabinet_Depth_Right,Width,Right_Side_Thickness,Cabinet_Depth_Left])
             
        face_frame.prompt("Face Frame Thickness",value=unit.inch(1.1))
        face_frame.prompt("Top Rail Width",'Top_Rail_Width',[Top_Rail_Width])
        face_frame.prompt("Bottom Rail Width",'Bottom_Rail_Width',[Bottom_Rail_Width])
        face_frame.prompt("Left Stile Width",'Left_Stile_Width',[Left_Stile_Width])
        face_frame.prompt("Right Stile Width",'Right_Stile_Width',[Right_Stile_Width])                
        
        #DOORS
        Face_Frame_Thickness = face_frame.get_var("Face Frame Thickness")
        Top_Rail_Width = face_frame.get_var("Top Rail Width")
        Left_Stile_Width = face_frame.get_var("Left Stile Width")
        Right_Stile_Width = face_frame.get_var("Right Stile Width")       
        Face_Frame_Width = face_frame.get_var("dim_x","Face_Frame_Width") 
        
        self.exterior.draw()
        self.exterior.obj_bp.parent = self.obj_bp
        
        self.exterior.add_prompt(name="Door Insert Rotation",prompt_type='ANGLE',tab_index=1)
        self.exterior.prompt("Door Insert Rotation","atan((fabs(Depth)-Left_Side_Thickness-Cabinet_Depth_Right)/(fabs(Width)-Right_Side_Thickness-Cabinet_Depth_Left))",[Depth,Left_Side_Thickness,Cabinet_Depth_Right,Width,Right_Side_Thickness,Cabinet_Depth_Left])
        Door_Insert_Rotation = self.exterior.get_var("Door Insert Rotation","Door_Insert_Rotation")
        
        self.exterior.x_loc('Cabinet_Depth_Left+Left_Stile_Width*cos(Door_Insert_Rotation)',
                            [Cabinet_Depth_Left,Left_Stile_Width,Door_Insert_Rotation])
        self.exterior.y_loc('Depth+Left_Side_Thickness+Left_Stile_Width*sin(Door_Insert_Rotation)',
                            [Depth,Left_Side_Thickness,Left_Stile_Width,Door_Insert_Rotation])
         
        if self.carcass.carcass_type == "Base":
            self.exterior.z_loc('Bottom_Inset',[Bottom_Inset])
        if self.carcass.carcass_type == "Upper":
            self.exterior.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
 
        self.exterior.z_rot('Door_Insert_Rotation',[Door_Insert_Rotation])
        
        self.exterior.x_dim("Face_Frame_Width-Right_Stile_Width-Left_Stile_Width",[Face_Frame_Width,Right_Stile_Width,Left_Stile_Width])
        self.exterior.y_dim('Depth+Cabinet_Depth_Right+Right_Side_Thickness',[Depth,Cabinet_Depth_Right,Right_Side_Thickness])
        self.exterior.z_dim('fabs(Height)-Bottom_Inset-Top_Inset',[Height,Bottom_Inset,Top_Inset])
        
        self.exterior.prompt("Frame Thickness","Face_Frame_Thickness",[Face_Frame_Thickness])      
        self.exterior.prompt("Frame Top Gap","Top_Rail_Width-Top_Thickness",[Top_Thickness,Top_Rail_Width])
        
        Door_Thickness = self.exterior.get_var("Door Thickness","Door_Thickness")
        self.exterior.prompt("Door Y Offset","-(Face_Frame_Thickness-Door_Thickness)",[Door_Thickness,Face_Frame_Thickness])
        
    def draw(self):
        create_cabinet(self)
        
        self.add_tab(name='Face Frame Options',tab_type='VISIBLE')
        self.add_prompt(name="Top Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Bottom Rail Width",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=1)
        self.add_prompt(name="Left Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Right Stile Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)

        self.carcass.draw()
        self.carcass.obj_bp.parent = self.obj_bp
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Left_Stile_Width = self.get_var('Left Stile Width','Left_Stile_Width') 
        Right_Stile_Width = self.get_var('Right Stile Width','Right_Stile_Width')           
        
        Left_Side_Thickness = self.carcass.get_var("Left Side Thickness")
        Right_Side_Thickness = self.carcass.get_var("Right Side Thickness")
        Left_Fin_End = self.carcass.get_var("Left Fin End")
        Right_Fin_End = self.carcass.get_var("Right Fin End")
        
        self.carcass.z_dim('Product_Height',[Product_Height])
        
        self.obj_bp.mv.product_sub_type = self.carcass.carcass_type
        
        add_product_width_dimension(self)
        add_product_depth_dimension(self)
        
        if self.carcass.carcass_shape == 'Notched':
            self.obj_bp.mv.product_shape = 'INSIDE_NOTCH'
            
            self.carcass.x_dim('Product_Width-IF(Right_Fin_End,0,Right_Stile_Width-Right_Side_Thickness)',[Product_Width,Right_Fin_End,Right_Stile_Width,Right_Side_Thickness])        
            self.carcass.y_dim('Product_Depth+IF(Left_Fin_End,0,Left_Stile_Width-Left_Side_Thickness)',[Product_Depth,Left_Fin_End,Left_Stile_Width,Left_Side_Thickness])        
            
            if self.exterior:
                self.add_pie_cut_ff_and_doors()
        
        if self.carcass.carcass_shape == 'Diagonal':
            self.obj_bp.mv.product_shape = 'INSIDE_DIAGONAL'
            
            self.carcass.x_dim('Product_Width',[Product_Width])
            self.carcass.y_dim('Product_Depth',[Product_Depth])
            
            if self.exterior:
                self.add_diagonal_ff_and_doors()

        self.update()
