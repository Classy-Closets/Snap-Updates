"""
Microvellum 
Carcass
Stores the construction logic for the different types of carcasses that are available
in the frameless and face frame library
"""

import bpy
from mv import unit, utils, fd_types
from os import path
from . import cabinet_properties

#ASSEMBLIES
ROOT_DIR = path.dirname(__file__)
CUTPARTS_DIR = path.join(ROOT_DIR,"Cabinet Assemblies","Cut Parts")
NOTCHED_SIDE = path.join(CUTPARTS_DIR,"Notched Side.blend")
PART_WITH_FRONT_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with Front Edgebanding.blend")
PART_WITH_NO_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with No Edgebanding.blend")
PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with Front and Bottom Edgebanding.blend")
PART_WITH_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with Edgebanding.blend")
CHAMFERED_PART = path.join(CUTPARTS_DIR,"Chamfered Part.blend")
CORNER_NOTCH_PART = path.join(CUTPARTS_DIR,"Corner Notch Part.blend")
TRANSITION_PART = path.join(CUTPARTS_DIR,"Transition Part with Front Edgebanding.blend")
BENDING_PART = path.join(CUTPARTS_DIR,"Cut Parts","Bending Part.blend")
RADIUS_CORNER_PART_WITH_EDGEBANDING = path.join(CUTPARTS_DIR,"Radius Corner Part with Edgebanding.blend")
LEG_LEVELERS = path.join(ROOT_DIR,"Cabinet Assemblies","Hardware","Leg Levelers.blend")

#MATERIAL SLOT NAMES
EXTERIOR = "Exterior"
INTERIOR = "Interior"
EDGES = "Edges"
LEFT_EXTERIOR = "Left_Exterior"
RIGHT_EXTERIOR = "Right_Exterior"

#POINTER_NAMES
EXPOSED_EXTERIOR_SURFACE = "Exposed_Exterior_Surface"
EXPOSED_INTERIOR_SURFACE = "Exposed_Interior_Surface"
SEMI_EXPOSED_SURFACE = "Semi_Exposed_Surface"
EXPOSED_EXTERIOR_EDGE = "Exposed_Exterior_Edge"
EXPOSED_INTERIOR_EDGE = "Exposed_Interior_Edge"
SEMI_EXPOSED_EDGE = "Semi_Exposed_Edge"
CONCEALED_SURFACE = "Concealed_Surface"
CONCEALED_EDGE = "Concealed_Edge"

#ASSEMBLIES
ROOT_DIR = path.dirname(__file__)
CARCASS_DIR = path.join(ROOT_DIR,"Cabinet Assemblies","Basic Carcasses")
SIMPLE_CARCASS = path.join(CARCASS_DIR,"Simple Carcass.blend")
SINK_CARCASS = path.join(CARCASS_DIR,"Sink Carcass.blend")
PIE_CUT_CORNER_CARCASS = path.join(CARCASS_DIR,"Corner Carcass.blend")
DIAGONAL_CORNER_CARCASS = path.join(CARCASS_DIR,"Diagonal Corner Carcass.blend")
PIE_CUT_BASE_ASSEMBLY = path.join(CARCASS_DIR,"Base Corner Assembly.blend")
DIAGONAL_BASE_ASSEMBLY = path.join(CARCASS_DIR,"Diagonal Base Assembly.blend")
BASE_ASSEMBLY = path.join(CARCASS_DIR,"Base Assembly.blend")
CUTPARTS_DIR = path.join(ROOT_DIR,"Cabinet Assemblies","Cut Parts")
PART_WITH_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with Edgebanding.blend")


def add_common_carcass_prompts(assembly):
    assembly.add_tab(name='Carcass Options',tab_type='VISIBLE')
    assembly.add_tab(name='Formulas',tab_type='HIDDEN')
    
    assembly.add_prompt(name="Left Fin End",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
    assembly.add_prompt(name="Right Fin End",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
    assembly.add_prompt(name="Left Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=0,export=True)
    assembly.add_prompt(name="Right Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=0,export=True)
    
    assembly.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Back Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Thick Back Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Filler Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)    
    assembly.add_prompt(name="Back Inset",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Top Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    assembly.add_prompt(name="Bottom Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)

def add_base_assembly_prompts(assembly):
    props = cabinet_properties.get_scene_props().carcass_defaults
    assembly.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value= props.toe_kick_height,tab_index=0,export=True)
    assembly.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value= props.toe_kick_setback,tab_index=0,export=True)
    assembly.add_prompt(name="Base Inset Front",prompt_type='CHECKBOX',value= True,tab_index=0)
    assembly.add_prompt(name="Base Inset Rear",prompt_type='CHECKBOX',value= False,tab_index=0)
    assembly.add_prompt(name="Base Inset Left",prompt_type='CHECKBOX',value= False,tab_index=0)
    assembly.add_prompt(name="Base Inset Right",prompt_type='CHECKBOX',value= False,tab_index=0)

def add_valance_prompts(assembly,add_bottom_valance):
    props = cabinet_properties.get_scene_props().carcass_defaults
    assembly.add_prompt(name="Valance Height Top",prompt_type='DISTANCE',value=props.valance_height_top,tab_index=0,export=True)
    assembly.add_prompt(name="Door Valance Top",prompt_type='CHECKBOX',value=props.door_valance_top,tab_index=0,export=True)
    if add_bottom_valance:
        assembly.add_prompt(name="Valance Height Bottom",prompt_type='DISTANCE',value=props.valance_height_bottom,tab_index=0,export=True)
        assembly.add_prompt(name="Door Valance Bottom",prompt_type='CHECKBOX',value=props.door_valance_bottom,tab_index=0,export=True)
    assembly.add_prompt(name="Left Side Full Height",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
    assembly.add_prompt(name="Right Side Full Height",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
    assembly.add_prompt(name="Valance Each Unit",prompt_type='CHECKBOX',value=props.valance_each_unit,tab_index=0,export=True)
    assembly.add_prompt(name="Valance Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)        

def add_sink_prompts(assembly):
    props = cabinet_properties.get_scene_props().carcass_defaults
    assembly.add_prompt(name="Sub Front Height",prompt_type='DISTANCE',value= props.sub_front_height,tab_index=0,export=True)
    assembly.add_prompt(name="Sub Front Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)        

def add_prompt_formulas(assembly):
    tt = assembly.get_var("Top Thickness",'tt')
    bt = assembly.get_var("Bottom Thickness",'bt')
    if assembly.carcass_type in {'Base','Sink','Tall'}:
        kick_height = assembly.get_var("Toe Kick Height",'kick_height')
    if assembly.carcass_type in {'Upper','Tall'}:
        vhb = assembly.get_var("Valance Height Bottom",'vhb')
        vht = assembly.get_var("Valance Height Top",'vht')

    # Used to calculate the exterior opening for doors
    if assembly.carcass_type == 'Base':
        assembly.prompt('Top Inset','tt',[tt])
        assembly.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
    if assembly.carcass_type == 'Sink':
        Sub_Front_Height = assembly.get_var("Sub Front Height")
        assembly.prompt('Top Inset','Sub_Front_Height',[Sub_Front_Height])
        assembly.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
    if assembly.carcass_type == 'Tall':
        assembly.prompt('Top Inset','vht+tt',[vht,tt])
        assembly.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
    if assembly.carcass_type == 'Upper':
        assembly.prompt('Top Inset','vht+tt',[vht,tt])
        assembly.prompt('Bottom Inset','vhb+bt',[vhb,bt])
    if assembly.carcass_type == 'Suspended':
        assembly.prompt('Top Inset','tt',[tt])
        assembly.prompt('Bottom Inset','bt',[bt])
        
def add_carcass_with_base_assembly(assembly,use_sink_carcass=False):
    Product_Width = assembly.get_var('dim_x','Product_Width')
    Product_Height = assembly.get_var('dim_z','Product_Height')
    Product_Depth = assembly.get_var('dim_y','Product_Depth')    
    Toe_Kick_Height = assembly.get_var('Toe Kick Height')  
    Toe_Kick_Setback = assembly.get_var('Toe Kick Setback')  
    Base_Inset_Front = assembly.get_var('Base Inset Front')  
    Base_Inset_Rear = assembly.get_var('Base Inset Rear')  
    Base_Inset_Left = assembly.get_var('Base Inset Left')  
    Base_Inset_Right = assembly.get_var('Base Inset Right')  
    
    carcass = assembly.add_assembly(SINK_CARCASS if use_sink_carcass else SIMPLE_CARCASS)
    carcass.x_loc(value = 0)
    carcass.y_loc(value = 0)
    carcass.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
    carcass.x_rot(value = 0)
    carcass.y_rot(value = 0)
    carcass.z_rot(value = 0)
    carcass.x_dim('Product_Width',[Product_Width])
    carcass.y_dim('Product_Depth',[Product_Depth])
    carcass.z_dim('Product_Height-Toe_Kick_Height',[Product_Height,Toe_Kick_Height])
    if use_sink_carcass:
        Sub_Front_Height = assembly.get_var('Sub Front Height') 
        carcass.prompt('Sub Front Height','Sub_Front_Height',[Sub_Front_Height])
    carcass.set_material_pointers(EXPOSED_EXTERIOR_SURFACE,EXTERIOR)    
    carcass.set_material_pointers(EXPOSED_INTERIOR_SURFACE,INTERIOR)  
    carcass.set_material_pointers(CONCEALED_SURFACE,LEFT_EXTERIOR)  
    carcass.set_material_pointers(CONCEALED_SURFACE,RIGHT_EXTERIOR)  
    carcass.set_material_pointers(EXPOSED_EXTERIOR_EDGE,EDGES)  
    
    base_assembly = assembly.add_assembly(BASE_ASSEMBLY)
    base_assembly.x_loc('IF(Base_Inset_Left,Toe_Kick_Setback,0)',[Base_Inset_Left,Toe_Kick_Setback])
    base_assembly.y_loc('IF(Base_Inset_Rear,-Toe_Kick_Setback,0)',[Base_Inset_Rear,Toe_Kick_Setback])
    base_assembly.z_loc(value = 0)
    base_assembly.x_rot(value = 0)
    base_assembly.y_rot(value = 0)
    base_assembly.z_rot(value = 0)
    base_assembly.x_dim('Product_Width-IF(Base_Inset_Left,Toe_Kick_Setback,0)-IF(Base_Inset_Right,Toe_Kick_Setback,0)',[Product_Width,Base_Inset_Left,Base_Inset_Right,Toe_Kick_Setback])
    base_assembly.y_dim('Product_Depth+IF(Base_Inset_Front,Toe_Kick_Setback,0)+IF(Base_Inset_Rear,Toe_Kick_Setback,0)',[Product_Depth,Base_Inset_Front,Base_Inset_Rear,Toe_Kick_Setback])
    base_assembly.z_dim('Toe_Kick_Height',[Toe_Kick_Height])
    base_assembly.material("Exposed_Exterior_Surface")
    base_assembly.set_material_pointers(EXPOSED_EXTERIOR_SURFACE,EXTERIOR)
    base_assembly.set_material_pointers(CONCEALED_SURFACE,LEFT_EXTERIOR)
    base_assembly.set_material_pointers(CONCEALED_SURFACE,RIGHT_EXTERIOR)        
    
def add_fillers(assembly):
    
    Product_Width = assembly.get_var('dim_x','Product_Width')
    Product_Height = assembly.get_var('dim_z','Product_Height')
    Product_Depth = assembly.get_var('dim_y','Product_Depth')    
    Toe_Kick_Height = assembly.get_var('Toe Kick Height')  
    Left_Side_Wall_Filler = assembly.get_var('Left Side Wall Filler')  
    Right_Side_Wall_Filler = assembly.get_var('Right Side Wall Filler') 
    
    left_filler = assembly.add_assembly(PART_WITH_EDGEBANDING)
    left_filler.set_name("Left Filler")
    left_filler.x_loc('-Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
    left_filler.y_loc('Product_Depth',[Product_Depth])
    left_filler.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
    left_filler.x_rot(value = 0)
    left_filler.y_rot(value = -90)
    left_filler.z_rot(value = -90)
    left_filler.x_dim('Product_Height-Toe_Kick_Height',[Product_Height,Toe_Kick_Height])
    left_filler.y_dim('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
    left_filler.z_dim(value = unit.inch(.75))
    left_filler.cutpart("Cabinet_Filler")
    left_filler.prompt('Hide','IF(Left_Side_Wall_Filler==0,True,False)',[Left_Side_Wall_Filler])
    
    right_filler = assembly.add_assembly(PART_WITH_EDGEBANDING)
    right_filler.set_name("Right Filler")
    right_filler.x_loc('Product_Width',[Product_Width])
    right_filler.y_loc('Product_Depth',[Product_Depth])
    right_filler.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
    right_filler.x_rot(value = 0)
    right_filler.y_rot(value = -90)
    right_filler.z_rot(value = -90)
    right_filler.x_dim('Product_Height-Toe_Kick_Height',[Product_Height,Toe_Kick_Height])
    right_filler.y_dim('Right_Side_Wall_Filler',[Right_Side_Wall_Filler])
    right_filler.z_dim(value = unit.inch(.75))
    right_filler.cutpart("Cabinet_Filler")
    right_filler.prompt('Hide','IF(Right_Side_Wall_Filler==0,True,False)',[Right_Side_Wall_Filler])           
        
#---------ASSEMBLY INSTRUCTIONS
    
class Standard_Carcass(fd_types.Assembly):
    
    library_name = "Carcasses"
    placement_type = ""
    type_assembly = "INSERT"
    
    carcass_type = "" # {Base, Tall, Upper, Sink, Suspended}
    open_name = ""
    
    remove_top = False # Used to remove top for face frame sink cabinets
    
    def draw(self):
#         props = cabinet_properties.get_scene_props().carcass_defaults
        self.create_assembly()
        add_common_carcass_prompts(self)
        add_base_assembly_prompts(self)
        if self.carcass_type == 'Sink':
            add_sink_prompts(self)
        add_prompt_formulas(self)
        add_carcass_with_base_assembly(self, use_sink_carcass=True if self.carcass_type == 'Sink' else False)
        add_fillers(self)
        self.update()
        
class Transition_Carcass(fd_types.Assembly):
    
    library_name = "Carcasses"
    placement_type = ""
    type_assembly = "INSERT"
    
    carcass_type = "" # {Base, Tall, Upper, Sink, Suspended}
    open_name = ""
    
    def add_common_carcass_prompts(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        self.add_tab(name='Carcass Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        self.add_tab(name='Machining Options',tab_type='HIDDEN')
        self.add_prompt(name="Left Fin End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Right Fin End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Left Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=0)
        self.add_prompt(name="Right Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=0)
        self.add_prompt(name="Cabinet Depth Left",prompt_type='DISTANCE',value=unit.inch(23.0),tab_index=0)
        self.add_prompt(name="Cabinet Depth Right",prompt_type='DISTANCE',value=unit.inch(12.0),tab_index=0)
        self.add_prompt(name="Use Nailers",prompt_type='CHECKBOX',value= props.use_nailers,tab_index=0)
        self.add_prompt(name="Nailer Width",prompt_type='DISTANCE',value= props.nailer_width,tab_index=0)
        self.add_prompt(name="Center Nailer Switch",prompt_type='DISTANCE',value= props.center_nailer_switch,tab_index=0)
        self.add_prompt(name="Use Thick Back",prompt_type='CHECKBOX',value= props.use_thick_back,tab_index=0)
        self.add_prompt(name="Remove Back",prompt_type='CHECKBOX',value= props.remove_back,tab_index=0)
        self.add_prompt(name="Remove Bottom",prompt_type='CHECKBOX',value= False,tab_index=0)
        
        if self.carcass_type in {'Base','Suspended'} and not props.use_full_tops:
            self.add_prompt(name="Stretcher Width",prompt_type='DISTANCE',value=props.stretcher_width,tab_index=0)
        
        self.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Back Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Thick Back Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Filler Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Nailer Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Edgebanding Thickness",prompt_type='DISTANCE',value=unit.inch(.02),tab_index=1)
        self.add_prompt(name="Back Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Top Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Bottom Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        
    def add_base_assembly_prompts(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        self.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value= props.toe_kick_height,tab_index=0)
        self.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value= props.toe_kick_setback,tab_index=0)
        self.add_prompt(name="Toe Kick Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        
    def add_valance_prompts(self,add_bottom_valance):
        props = cabinet_properties.get_scene_props().carcass_defaults
        self.add_prompt(name="Valance Height Top",prompt_type='DISTANCE',value=props.valance_height_top,tab_index=0)
        self.add_prompt(name="Door Valance Top",prompt_type='CHECKBOX',value=props.door_valance_top,tab_index=0)
        if add_bottom_valance:
            self.add_prompt(name="Valance Height Bottom",prompt_type='DISTANCE',value=props.valance_height_bottom,tab_index=0)
            self.add_prompt(name="Door Valance Bottom",prompt_type='CHECKBOX',value=props.door_valance_bottom,tab_index=0)
        self.add_prompt(name="Left Side Full Height",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Right Side Full Height",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Valance Each Unit",prompt_type='CHECKBOX',value=props.valance_each_unit,tab_index=0)
        self.add_prompt(name="Valance Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    
    def add_prompt_formulas(self):
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        tt = self.get_var("Top Thickness",'tt')
        bt = self.get_var("Bottom Thickness",'bt')
        use_nailers = self.get_var("Use Nailers",'use_nailers')
        nt = self.get_var("Nailer Thickness",'nt')
        bkt = self.get_var("Back Thickness",'bkt')
        tbkt = self.get_var("Thick Back Thickness",'tbkt')
        use_thick_back = self.get_var("Use Thick Back",'use_thick_back')
        remove_back = self.get_var("Remove Back",'remove_back')
        lfe = self.get_var("Left Fin End",'lfe')
        rfe = self.get_var("Right Fin End",'rfe')
        Remove_Bottom = self.get_var('Remove Bottom','Remove_Bottom')
        if self.carcass_type in {'Base','Sink','Tall'}:
            kick_height = self.get_var("Toe Kick Height",'kick_height')
        if self.carcass_type in {'Upper','Tall'}:
            vhb = self.get_var("Valance Height Bottom",'vhb')
            vht = self.get_var("Valance Height Top",'vht')

        Side_Pointer_Name = 'Cabinet_Unfinished_Side' + self.open_name
        FE_Pointer_Name = 'Cabinet_Finished_Side' + self.open_name
        Top_Pointer_Name = 'Cabinet_Top' + self.open_name
        Bottom_Pointer_Name = 'Cabinet_Bottom' + self.open_name
        Back_Pointer_Name = 'Cabinet_Back' + self.open_name
        Thick_Back_Pointer_Name = 'Cabinet_Thick_Back' + self.open_name
        Edgebanding_Pointer_Name = 'Cabinet_Body_Edges' + self.open_name

        self.prompt('Left Side Thickness','IF(lfe,THICKNESS(sgi,"' + FE_Pointer_Name +'"),THICKNESS(sgi,"' + Side_Pointer_Name +'"))',[lfe,sgi])
        self.prompt('Right Side Thickness','IF(rfe,THICKNESS(sgi,"' + FE_Pointer_Name +'"),THICKNESS(sgi,"' + Side_Pointer_Name +'"))',[rfe,sgi])
        if self.carcass_type == "Sink":
            self.prompt('Top Thickness',value = 0)
        else:
            self.prompt('Top Thickness','THICKNESS(sgi,"' + Top_Pointer_Name +'")',[sgi])
        self.prompt('Bottom Thickness','THICKNESS(sgi,"' + Bottom_Pointer_Name +'")',[sgi])
        if self.carcass_type in {'Base','Sink','Tall'}:
            self.prompt('Toe Kick Thickness','THICKNESS(sgi,"Cabinet_Toe_Kick")',[sgi])
        self.prompt('Back Thickness','IF(remove_back,0,IF(use_thick_back,THICKNESS(sgi,"' + Thick_Back_Pointer_Name +'"),THICKNESS(sgi,"' + Back_Pointer_Name +'")))',[sgi,use_thick_back,remove_back])
        self.prompt('Thick Back Thickness','THICKNESS(sgi,"Cabinet_Thick_Back' + self.open_name +'")',[sgi])
        self.prompt('Filler Thickness','THICKNESS(sgi,"Cabinet_Filler")',[sgi])
        self.prompt('Nailer Thickness','THICKNESS(sgi,"Cabinet_Nailer")',[sgi])
        if self.carcass_type in {'Tall','Upper'}:
            self.prompt('Valance Thickness','THICKNESS(sgi,"Cabinet_Valance")',[sgi])
        self.prompt('Edgebanding Thickness','EDGE_THICKNESS(sgi,"' + Edgebanding_Pointer_Name + '")',[sgi])
        
        if self.carcass_type == 'Base':
            self.prompt('Top Inset','tt',[tt])
            self.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
        if self.carcass_type == 'Sink':
            Sub_Front_Height = self.get_var("Sub Front Height")
            self.prompt('Top Inset','Sub_Front_Height',[Sub_Front_Height])
            self.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
        if self.carcass_type == 'Tall':
            self.prompt('Top Inset','vht+tt',[vht,tt])
            self.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
        if self.carcass_type == 'Upper':
            self.prompt('Top Inset','vht+tt',[vht,tt])
            self.prompt('Bottom Inset','IF(Remove_Bottom,0,vhb+bt)',[vhb,bt,Remove_Bottom])
        if self.carcass_type == 'Suspended':
            self.prompt('Top Inset','tt',[tt])
            self.prompt('Bottom Inset','IF(Remove_Bottom,0,bt)',[bt,Remove_Bottom])
        
        self.prompt('Back Inset','IF(use_nailers,nt,0)+IF(remove_back,0,IF(use_thick_back,tbkt,bkt))',[use_nailers,nt,bkt,tbkt,use_thick_back,remove_back])
    
    def add_base_sides(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Left_Fin_End = self.get_var('Left Fin End')
        Right_Fin_End = self.get_var('Right Fin End')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')
        
        left_side = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        left_side.set_name(self.carcass_type + " Left Side")
        left_side.x_loc(value = 0)
        left_side.y_loc(value = 0)
        if props.use_notched_sides:
            left_side.z_loc(value = 0)
            left_side.x_dim('Height',[Height])
            left_side.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            left_side.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            left_side.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            left_side.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
        left_side.x_rot(value = 0)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
        left_side.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.prompt('Hide','IF(Left_Fin_End,True,False)',[Left_Fin_End])
        left_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        left_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_side = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        right_side.set_name(self.carcass_type + " Right Side")
        right_side.x_loc('Width',[Width])
        right_side.y_loc(value = 0)
        if props.use_notched_sides:
            right_side.z_loc(value = 0)
            right_side.x_dim('Height',[Height])
            right_side.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            right_side.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            right_side.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            right_side.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
        right_side.x_rot(value = 0)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)
        right_side.x_dim(value = 0)
        right_side.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.prompt('Hide','IF(Right_Fin_End,True,False)',[Right_Fin_End])
        right_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        right_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        left_fe = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        left_fe.set_name(self.carcass_type + " Left FE")
        left_fe.x_loc(value = 0)
        left_fe.y_loc(value = 0)
        if props.use_notched_sides:
            left_fe.z_loc(value = 0)
            left_fe.x_dim('Height',[Height])
            left_fe.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            left_fe.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            left_fe.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            left_fe.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
        left_fe.x_rot(value = 0)
        left_fe.y_rot(value = -90)
        left_fe.z_rot(value = 0)
        left_fe.x_dim(value = 0)
        left_fe.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_fe.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_fe.prompt('Hide','IF(Left_Fin_End,False,True)',[Left_Fin_End])
        left_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        left_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_fe = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        right_fe.set_name(self.carcass_type + " Right FE")
        right_fe.x_loc('Width',[Width])
        right_fe.y_loc(value = 0)
        if props.use_notched_sides:
            right_fe.z_loc(value = 0)
            right_fe.x_dim('Height',[Height])
            right_fe.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            right_fe.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            right_fe.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            right_fe.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
        right_fe.x_rot(value = 0)
        right_fe.y_rot(value = -90)
        right_fe.z_rot(value = 0)
        right_fe.x_dim(value = 0)
        right_fe.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_fe.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_fe.prompt('Hide','IF(Right_Fin_End,False,True)',[Right_Fin_End])
        right_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        right_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
    def add_tall_sides(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Left_Fin_End = self.get_var('Left Fin End')
        Right_Fin_End = self.get_var('Right Fin End')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Left_Side_Full_Height = self.get_var('Left Side Full Height')
        Right_Side_Full_Height = self.get_var('Right Side Full Height')
        Top_Inset = self.get_var('Top Inset')
        Top_Thickness = self.get_var('Top Thickness')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')
        
        left_side = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        left_side.set_name(self.carcass_type + " Left Side")
        left_side.x_loc(value = 0)
        left_side.y_loc(value = 0)
        if props.use_notched_sides:
            left_side.z_loc(value = 0)
            left_side.x_dim('Height+IF(Left_Side_Full_Height,0,-Top_Inset+Top_Thickness)',[Height,Top_Inset,Top_Thickness,Left_Side_Full_Height])
            left_side.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            left_side.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            left_side.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            left_side.x_dim('Height-Toe_Kick_Height+IF(Left_Side_Full_Height,0,-Top_Inset+Top_Thickness)',[Left_Side_Full_Height,Height,Toe_Kick_Height,Top_Thickness,Top_Inset])
        left_side.x_rot(value = 0)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
        left_side.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.prompt('Hide','IF(Left_Fin_End,True,False)',[Left_Fin_End])
        left_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        left_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_side = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        right_side.set_name(self.carcass_type + " Right Side")
        right_side.x_loc('Width',[Width])
        right_side.y_loc(value = 0)
        if props.use_notched_sides:
            right_side.z_loc(value = 0)
            right_side.x_dim('Height+IF(Right_Side_Full_Height,0,-Top_Inset+Top_Thickness)',[Height,Top_Inset,Top_Thickness,Right_Side_Full_Height])
            right_side.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            right_side.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            right_side.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            right_side.x_dim('Height-Toe_Kick_Height+IF(Right_Side_Full_Height,0,-Top_Inset+Top_Thickness)',[Right_Side_Full_Height,Top_Thickness,Top_Inset,Height,Toe_Kick_Height])
        right_side.x_rot(value = 0)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)
        right_side.x_dim(value = 0)
        right_side.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.prompt('Hide','IF(Right_Fin_End,True,False)',[Right_Fin_End])
        right_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        right_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        left_fe = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        left_fe.set_name(self.carcass_type + " Left FE")
        left_fe.x_loc(value = 0)
        left_fe.y_loc(value = 0)
        if props.use_notched_sides:
            left_fe.z_loc(value = 0)
            left_fe.x_dim('Height',[Height])
            left_fe.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            left_fe.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            left_fe.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            left_fe.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
        left_fe.x_rot(value = 0)
        left_fe.y_rot(value = -90)
        left_fe.z_rot(value = 0)
        left_fe.x_dim(value = 0)
        left_fe.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_fe.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_fe.prompt('Hide','IF(Left_Fin_End,False,True)',[Left_Fin_End])
        left_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        left_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_fe = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
        right_fe.set_name(self.carcass_type + " Right FE")
        right_fe.x_loc('Width',[Width])
        right_fe.y_loc(value = 0)
        if props.use_notched_sides:
            right_fe.z_loc(value = 0)
            right_fe.x_dim('Height',[Height])
            right_fe.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
            right_fe.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            right_fe.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            right_fe.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
        right_fe.x_rot(value = 0)
        right_fe.y_rot(value = -90)
        right_fe.z_rot(value = 0)
        right_fe.x_dim(value = 0)
        right_fe.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_fe.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_fe.prompt('Hide','IF(Right_Fin_End,False,True)',[Right_Fin_End])
        right_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        right_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
    def add_upper_sides(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Left_Fin_End = self.get_var('Left Fin End')
        Right_Fin_End = self.get_var('Right Fin End')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Left_Side_Full_Height = self.get_var('Left Side Full Height')
        Right_Side_Full_Height = self.get_var('Right Side Full Height')
        Valance_Height_Top = self.get_var('Valance Height Top')
        Valance_Height_Bottom = self.get_var('Valance Height Bottom')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')
        
        left_side = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
        left_side.set_name(self.carcass_type + " Left Side")
        left_side.x_loc(value = 0)
        left_side.y_loc(value = 0)
        left_side.z_loc('IF(Left_Side_Full_Height,0,-Valance_Height_Top)',[Left_Side_Full_Height,Valance_Height_Top])
        left_side.x_rot(value = 0)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
        left_side.x_dim('Height+IF(Left_Side_Full_Height,0,Valance_Height_Top+Valance_Height_Bottom)',[Height,Valance_Height_Bottom,Valance_Height_Top,Left_Side_Full_Height])
        left_side.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.prompt('Hide','IF(Left_Fin_End,True,False)',[Left_Fin_End])
        left_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        left_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_side = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
        right_side.set_name(self.carcass_type + " Right Side")
        right_side.x_loc('Width',[Width])
        right_side.y_loc(value = 0)
        right_side.z_loc('IF(Right_Side_Full_Height,0,-Valance_Height_Top)',[Right_Side_Full_Height,Valance_Height_Top])
        right_side.x_rot(value = 0)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)
        right_side.x_dim('Height+IF(Right_Side_Full_Height,0,Valance_Height_Top+Valance_Height_Bottom)',[Height,Right_Side_Full_Height,Valance_Height_Top,Valance_Height_Bottom])
        right_side.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.prompt('Hide','IF(Right_Fin_End,True,False)',[Right_Fin_End])
        right_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        right_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        left_fe = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
        left_fe.set_name(self.carcass_type + " Left FE")
        left_fe.x_loc(value = 0)
        left_fe.y_loc(value = 0)
        left_fe.z_loc(value = 0)
        left_fe.x_rot(value = 0)
        left_fe.y_rot(value = -90)
        left_fe.z_rot(value = 0)
        left_fe.x_dim('Height',[Height])
        left_fe.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_fe.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_fe.prompt('Hide','IF(Left_Fin_End,False,True)',[Left_Fin_End])
        left_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        left_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_fe = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
        right_fe.set_name(self.carcass_type + " Right FE")
        right_fe.x_loc('Width',[Width])
        right_fe.y_loc(value = 0)
        right_fe.z_loc(value = 0)
        right_fe.x_rot(value = 0)
        right_fe.y_rot(value = -90)
        right_fe.z_rot(value = 0)
        right_fe.x_dim('Height',[Height])
        right_fe.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_fe.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_fe.prompt('Hide','IF(Right_Fin_End,False,True)',[Right_Fin_End])
        right_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        right_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
    def add_suspended_sides(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Left_Fin_End = self.get_var('Left Fin End')
        Right_Fin_End = self.get_var('Right Fin End')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')

        left_side = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        left_side.set_name(self.carcass_type + " Left Side")
        left_side.x_loc(value = 0)
        left_side.y_loc(value = 0)
        left_side.z_loc(value = 0)
        left_side.x_rot(value = 0)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
        left_side.x_dim('Height',[Height])
        left_side.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.prompt('Hide','IF(Left_Fin_End,True,False)',[Left_Fin_End])
        left_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        left_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_side = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        right_side.set_name(self.carcass_type + " Right Side")
        right_side.x_loc('Width',[Width])
        right_side.y_loc(value = 0)
        right_side.z_loc(value = 0)
        right_side.x_rot(value = 0)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)
        right_side.x_dim('Height',[Height])
        right_side.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.prompt('Hide','IF(Right_Fin_End,True,False)',[Right_Fin_End])
        right_side.cutpart('Cabinet_Unfinished_Side' + self.open_name)
        right_side.edgebanding('Cabinet_Body_Edges',l1=True)
        
        left_fe = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        left_fe.set_name(self.carcass_type + " Left FE")
        left_fe.x_loc(value = 0)
        left_fe.y_loc(value = 0)
        left_fe.z_loc(value = 0)
        left_fe.x_rot(value = 0)
        left_fe.y_rot(value = -90)
        left_fe.z_rot(value = 0)
        left_fe.x_dim('Height',[Height])
        left_fe.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_fe.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_fe.prompt('Hide','IF(Left_Fin_End,False,True)',[Left_Fin_End])
        left_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        left_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
        right_fe = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        right_fe.set_name(self.carcass_type + " Right FE")
        right_fe.x_loc('Width',[Width])
        right_fe.y_loc(value = 0)
        right_fe.z_loc(value = 0)
        right_fe.x_rot(value = 0)
        right_fe.y_rot(value = -90)
        right_fe.z_rot(value = 0)
        right_fe.x_dim('Height',[Height])
        right_fe.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_fe.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_fe.prompt('Hide','IF(Right_Fin_End,False,True)',[Right_Fin_End])
        right_fe.cutpart('Cabinet_Finished_Side' + self.open_name)
        right_fe.edgebanding('Cabinet_Body_Edges',l1=True)
        
    def add_fillers(self):
        width = self.get_var('dim_x','width')
        height = self.get_var('dim_z','height')
        l_filler = self.get_var("Left Side Wall Filler",'l_filler')
        r_filler = self.get_var("Right Side Wall Filler",'r_filler')
        ft = self.get_var("Filler Thickness",'ft')
        if self.carcass_type in {'Base','Sink','Tall'}:
            kick_height = self.get_var("Toe Kick Height",'kick_height')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')
        
        left_filler = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        left_filler.set_name("Left Filler")
        left_filler.x_loc(value = unit.inch(0))
        left_filler.y_loc('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_filler.z_loc('height',[height])
        left_filler.x_rot(value = 90)
        left_filler.y_rot(value = 90)
        left_filler.z_rot(value = 180)
        left_filler.y_dim('l_filler',[l_filler])
        left_filler.z_dim('ft',[ft])
        left_filler.prompt('Hide','IF(l_filler>0,False,True)',[l_filler])
        left_filler.cutpart('Cabinet_Filler')
        
        right_filler = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        right_filler.set_name("Right Filler")
        right_filler.x_loc('width',[width])
        right_filler.y_loc('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_filler.z_loc('height',[height])
        right_filler.x_rot(value = 90)
        right_filler.y_rot(value = 90)
        right_filler.z_rot(value = 0)
        right_filler.y_dim('r_filler',[r_filler])
        right_filler.z_dim('-ft',[ft])
        right_filler.prompt('Hide','IF(r_filler>0,False,True)',[r_filler])
        right_filler.cutpart('Cabinet_Filler')
        
        if self.carcass_type in {'Base','Sink','Tall'}:
            left_filler.x_dim('height-kick_height',[height,kick_height])
            right_filler.x_dim('height-kick_height',[height,kick_height])
            
        if self.carcass_type in {'Upper','Suspended'}:
            left_filler.x_dim('height',[height])
            right_filler.x_dim('height',[height])
            
    def add_full_top(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Top_Thickness = self.get_var('Top Thickness')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Top_Inset = self.get_var('Top Inset')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')
        
        top = self.add_assembly(TRANSITION_PART)
        top.set_name(self.carcass_type + " Top")
        top.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        top.y_dim('Depth',[Depth])
        top.z_dim('-Top_Thickness',[Top_Thickness])
        top.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        top.y_loc(value = 0)
        top.z_loc('IF(Height>0,Height-Top_Inset+Top_Thickness,-Top_Inset+Top_Thickness)',[Height,Top_Inset,Top_Thickness])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.prompt("Left Depth",'Cabinet_Depth_Left',[Cabinet_Depth_Left])
        top.prompt("Right Depth",'Cabinet_Depth_Right',[Cabinet_Depth_Right])
        top.cutpart("Cabinet_Top"+self.open_name)
        top.edgebanding('Cabinet_Body_Edges', l1 = True)
        
    def add_bottom(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Bottom_Thickness = self.get_var('Bottom Thickness')
        Remove_Bottom = self.get_var('Remove Bottom')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')
        
        bottom = self.add_assembly(TRANSITION_PART)
        bottom.set_name(self.carcass_type + " Bottom")
        bottom.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        bottom.y_dim('Depth',[Depth])
        bottom.z_dim('Bottom_Thickness',[Bottom_Thickness])
        bottom.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        bottom.y_loc(value = 0)
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 0)
        bottom.prompt('Hide','Remove_Bottom',[Remove_Bottom])
        bottom.prompt("Left Depth",'Cabinet_Depth_Left',[Cabinet_Depth_Left])
        bottom.prompt("Right Depth",'Cabinet_Depth_Right',[Cabinet_Depth_Right])
        bottom.cutpart("Cabinet_Bottom"+self.open_name)
        bottom.edgebanding('Cabinet_Body_Edges', l1 = True)
        
        if self.carcass_type in {'Upper','Suspended'}:
            Bottom_Inset = self.get_var('Bottom Inset')
            bottom.z_loc('Height+Bottom_Inset-Bottom_Thickness',[Height,Bottom_Inset,Bottom_Thickness])
            
        if self.carcass_type in {'Base','Tall','Sink'}:
            bottom.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            
    def add_toe_kick(self):
        Width = self.get_var('dim_x','Width')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Remove_Bottom = self.get_var('Remove Bottom')
        Cabinet_Depth_Left = self.get_var('Cabinet Depth Left')
        Cabinet_Depth_Right = self.get_var('Cabinet Depth Right')
        
        kick = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        kick.set_name("Toe Kick")
        kick.x_dim('sqrt(((Cabinet_Depth_Left-Cabinet_Depth_Right)**2)+((Width-(Left_Side_Thickness+Right_Side_Thickness))**2))',[Cabinet_Depth_Left,Cabinet_Depth_Right,Width,Left_Side_Thickness,Right_Side_Thickness])
        kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        kick.z_dim(value = unit.inch(-.75))
        kick.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        kick.y_loc('-Cabinet_Depth_Left+Toe_Kick_Setback',[Cabinet_Depth_Left,Toe_Kick_Setback])
        kick.z_loc(value = 0)
        kick.x_rot(value = 90)
        kick.y_rot(value = 0)
        kick.z_rot('atan((Cabinet_Depth_Left-Cabinet_Depth_Right)/(Width-(Left_Side_Thickness+Right_Side_Thickness)))',[Cabinet_Depth_Left,Cabinet_Depth_Right,Width,Left_Side_Thickness,Right_Side_Thickness])
        kick.prompt('Hide','Remove_Bottom',[Remove_Bottom])
        kick.cutpart("Cabinet_Toe_Kick")
        
    def add_back(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Top_Inset = self.get_var('Top Inset')
        Bottom_Inset = self.get_var('Bottom Inset')
        Back_Thickness = self.get_var('Back Thickness')
        Bottom_Thickness = self.get_var('Bottom Thickness')
        Top_Thickness = self.get_var('Top Thickness')
        Use_Nailers = self.get_var('Use Nailers')
        Nailer_Thickness = self.get_var('Nailer Thickness')
        Remove_Back = self.get_var('Remove Back')
        Remove_Bottom = self.get_var('Remove Bottom')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        
        back = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        back.set_name(self.carcass_type + " Back")
        back.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        back.y_loc('IF(Use_Nailers,-Nailer_Thickness,0)',[Use_Nailers,Nailer_Thickness])
        back.x_rot(value = 0)
        back.y_rot(value = -90)
        back.z_rot(value = -90)
        
        if self.carcass_type in {'Base','Sink'}:
            back.x_dim('fabs(Height)-IF(Remove_Bottom,0,Toe_Kick_Height+Bottom_Thickness)-Top_Thickness',[Height,Toe_Kick_Height,Bottom_Thickness,Remove_Bottom,Top_Thickness])
        
        if self.carcass_type == 'Tall':
            back.x_dim('fabs(Height)-IF(Remove_Bottom,0,Toe_Kick_Height+Bottom_Thickness)-Top_Inset',[Height,Top_Inset,Toe_Kick_Height,Bottom_Thickness,Remove_Bottom])
        
        if self.carcass_type in {'Upper','Suspended'}:
            back.x_dim('fabs(Height)-(Top_Inset+Bottom_Inset)',[Height,Top_Inset,Bottom_Inset])
            
        back.y_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        back.z_dim('-Back_Thickness',[Back_Thickness])
        back.cutpart("Cabinet_Back" + self.open_name)
        back.edgebanding('Cabinet_Body_Edges', l1 = True)
        back.prompt('Hide','IF(Remove_Back,True,False)',[Remove_Back])
        
        if self.carcass_type in {'Base','Tall','Sink'}:
            back.z_loc('IF(Remove_Bottom,0,Toe_Kick_Height+Bottom_Thickness)',[Remove_Bottom,Toe_Kick_Height,Bottom_Thickness])
        
        if self.carcass_type in {'Upper','Suspended'}:
            back.z_loc('Height+Bottom_Inset',[Height,Bottom_Inset])
    
    def add_nailers(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Top_Thickness = self.get_var('Top Thickness')
        Top_Inset = self.get_var('Top Inset')
        Bottom_Inset = self.get_var('Bottom Inset')
        Remove_Bottom = self.get_var('Remove Bottom')
        Use_Nailers = self.get_var('Use Nailers')
        Nailer_Thickness = self.get_var('Nailer Thickness')
        Nailer_Width = self.get_var('Nailer Width')
        Center_Nailer_Switch = self.get_var('Center Nailer Switch')
        
        top_n = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        top_n.set_name("Top Nailer")
        top_n.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        top_n.y_loc('IF(Use_Nailers,-Nailer_Thickness,0)',[Use_Nailers,Nailer_Thickness])
        if self.carcass_type in {'Base','Sink'}:
            top_n.z_loc('Height-Top_Thickness',[Height,Top_Thickness])
        if self.carcass_type in {'Upper','Tall'}:
            top_n.z_loc('IF(Height>0,Height-Top_Inset,-Top_Inset)',[Height,Top_Inset])
        top_n.x_rot(value = 90)
        top_n.y_rot(value = 0)
        top_n.z_rot(value = 0)
        top_n.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        top_n.y_dim('-Nailer_Width',[Nailer_Width])
        top_n.z_dim('-Nailer_Thickness',[Nailer_Thickness])
        top_n.prompt('Hide','IF(Use_Nailers,False,True)',[Use_Nailers])
        top_n.cutpart("Cabinet_Nailer")
    
        center_n = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        center_n.set_name("Center Nailer")
        center_n.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        center_n.y_loc('IF(Use_Nailers,-Nailer_Thickness,0)',[Use_Nailers,Nailer_Thickness])
        center_n.z_loc('IF(Height>0,(Height/2)-(Nailer_Width/2)+(Bottom_Inset/2),(Height/2)-(Nailer_Width/2))',[Height,Nailer_Width,Bottom_Inset])
        center_n.x_rot(value = 90)
        center_n.y_rot(value = 0)
        center_n.z_rot(value = 0)
        center_n.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        center_n.y_dim('Nailer_Width',[Nailer_Width])
        center_n.z_dim('-Nailer_Thickness',[Nailer_Thickness])
        center_n.prompt('Hide','IF(Use_Nailers,IF(Height>Center_Nailer_Switch,False,True),True)',[Height,Center_Nailer_Switch,Use_Nailers])
        center_n.cutpart("Cabinet_Nailer")
    
        bottom_n = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        bottom_n.set_name("Bottom Nailer")
        bottom_n.x_loc('Left_Side_Thickness',[Left_Side_Thickness])
        bottom_n.y_loc('IF(Use_Nailers,-Nailer_Thickness,0)',[Use_Nailers,Nailer_Thickness])
        bottom_n.z_loc('IF(Height>0,IF(Remove_Bottom,0,Bottom_Inset),Height+Bottom_Inset)',[Height,Bottom_Inset,Remove_Bottom])
        bottom_n.x_rot(value = 90)
        bottom_n.y_rot(value = 0)
        bottom_n.z_rot(value = 0)
        bottom_n.x_dim('Width-(Left_Side_Thickness+Right_Side_Thickness)',[Width,Left_Side_Thickness,Right_Side_Thickness])
        bottom_n.y_dim('Nailer_Width',[Nailer_Width])
        bottom_n.z_dim('-Nailer_Thickness',[Nailer_Thickness])
        bottom_n.prompt('Hide','IF(Use_Nailers,False,True)',[Use_Nailers])
        bottom_n.cutpart("Cabinet_Nailer")
    
    def add_valances(self):
        width = self.get_var('dim_x','width')
        Height = self.get_var('dim_z','Height')
        Top_Inset = self.get_var('Top Inset')
        Top_Thickness = self.get_var('Top Thickness')
        Valance_Thickness = self.get_var("Valance Thickness")
        Valance_Each_Unit = self.get_var("Valance Each Unit")
        Valance_Height_Top = self.get_var("Valance Height Top")
        Valance_Height_Bottom = self.get_var("Valance Height Bottom")
        
        ld = self.get_var('Cabinet Depth Left','ld')
        rd = self.get_var('Cabinet Depth Right','rd')
        lst = self.get_var('Left Side Thickness','lst')
        rst = self.get_var('Right Side Thickness','rst')
        
        top_val = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        top_val.set_name("Top Valance")
        top_val.x_loc('lst',[lst])
        top_val.y_loc('-ld',[ld])
        top_val.z_loc('IF(Height>0,Height-Top_Inset+Top_Thickness,-Top_Inset+Top_Thickness)',[Height,Top_Thickness,Top_Inset])
        top_val.x_rot(value = 90)
        top_val.y_rot(value = 0)
        top_val.z_rot('atan((ld-rd)/(width-lst-rst))',[rd,ld,width,lst,rst])
        top_val.x_dim('sqrt(((ld-rd)**2)+((width-lst-rst)**2))',[lst,rst,width,ld,rd])
        top_val.y_dim('Valance_Height_Top',[Valance_Height_Top])
        top_val.z_dim('-Valance_Thickness',[Valance_Thickness])
        top_val.prompt('Hide','IF(AND(Valance_Each_Unit,Valance_Height_Top>0),False,True)',[Valance_Each_Unit,Valance_Height_Top])
        top_val.cutpart("Cabinet_Valance")
        top_val.edgebanding('Cabinet_Body_Edges',l1=True)
        
        if self.carcass_type == 'Upper':
            bottom_val = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
            bottom_val.set_name("Bottom Valance")
            bottom_val.x_loc('lst',[lst])
            bottom_val.y_loc('-ld',[ld])
            bottom_val.z_loc('Height+Valance_Height_Bottom',[Height,Valance_Height_Bottom])
            bottom_val.x_rot(value = 90)
            bottom_val.y_rot(value = 0)
            bottom_val.z_rot('atan((ld-rd)/(width-lst-rst))',[rd,ld,width,lst,rst])
            bottom_val.x_dim('sqrt(((ld-rd)**2)+((width-lst-rst)**2))',[lst,rst,width,ld,rd])
            bottom_val.y_dim('-Valance_Height_Bottom',[Valance_Height_Bottom])
            bottom_val.z_dim('-Valance_Thickness',[Valance_Thickness])
            bottom_val.prompt('Hide','IF(AND(Valance_Each_Unit,Valance_Height_Bottom>0),False,True)',[Valance_Each_Unit,Valance_Height_Bottom])
            bottom_val.cutpart("Cabinet_Valance")
            bottom_val.edgebanding('Cabinet_Body_Edges',l1=True)
            
    def draw(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        self.create_assembly()

        self.add_common_carcass_prompts()
        if self.carcass_type == "Base":
            self.add_base_assembly_prompts()

            self.add_full_top()
            if props.use_notched_sides:
                self.add_toe_kick()
            self.add_base_sides()
#             if g.use_leg_levelers:
#                 self.add_leg_levelers()

        if self.carcass_type == "Tall":
            self.add_base_assembly_prompts()
            self.add_full_top()
            self.add_valance_prompts(add_bottom_valance=False)
            if props.use_notched_sides:
                self.add_toe_kick()
            self.add_tall_sides()
#             if g.use_leg_levelers:
#                 self.add_leg_levelers()
            self.add_valances()
                
        if self.carcass_type == "Upper":
            self.flip_z = True
            self.add_full_top()
            self.add_valance_prompts(add_bottom_valance=True)
            self.add_valances()
            self.add_upper_sides()
            
        if self.carcass_type == "Sink":
            self.add_base_assembly_prompts()
            self.add_sink_prompts()
            self.add_sink_top()
            if props.use_notched_sides:
                self.add_toe_kick()
            self.add_base_sides()
#             if g.use_leg_levelers:
#                 self.add_leg_levelers()
                
        if self.carcass_type == "Suspended":
            self.flip_z = True
            self.add_finger_pull_prompts()
            self.add_suspended_sides()
            self.add_full_top()

        self.add_fillers()
        self.add_bottom()
        self.add_back()
        self.add_nailers()
        self.add_prompt_formulas()
        
        self.update()
        
class Inside_Corner_Carcass(fd_types.Assembly):
    
    library_name = "Carcasses"
    placement_type = ""
    type_assembly = "INSERT"
    
    carcass_type = "" # {Base, Tall, Upper}
    open_name = ""
    
    carcass_shape = "" # {Notched, Diagonal}
    left_right_depth = unit.inch(23)
    
    def add_common_carcass_prompts(self):
        
        self.add_tab(name='Carcass Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        self.add_tab(name='Machining Options',tab_type='HIDDEN')
        self.add_prompt(name="Left Fin End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Right Fin End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Left Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=0)
        self.add_prompt(name="Right Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=0)
        
        self.add_prompt(name="Cabinet Depth Left",prompt_type='DISTANCE',value=self.left_right_depth,tab_index=0)
        self.add_prompt(name="Cabinet Depth Right",prompt_type='DISTANCE',value=self.left_right_depth,tab_index=0)
        
        self.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Back Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Thick Back Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Filler Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Nailer Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Edgebanding Thickness",prompt_type='DISTANCE',value=unit.inch(.02),tab_index=1)
        self.add_prompt(name="Back Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Top Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Bottom Inset",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        
    def add_base_assembly_prompts(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        self.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value= props.toe_kick_height,tab_index=0)
        self.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value= props.toe_kick_setback,tab_index=0)
        self.add_prompt(name="Toe Kick Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    
    def add_valance_prompts(self,add_bottom_valance):
        props = cabinet_properties.get_scene_props().carcass_defaults
        self.add_prompt(name="Valance Height Top",prompt_type='DISTANCE',value=props.valance_height_top,tab_index=0,export=True)
        self.add_prompt(name="Door Valance Top",prompt_type='CHECKBOX',value=props.door_valance_top,tab_index=0,export=True)
        if add_bottom_valance:
            self.add_prompt(name="Valance Height Bottom",prompt_type='DISTANCE',value=props.valance_height_bottom,tab_index=0,export=True)
            self.add_prompt(name="Door Valance Bottom",prompt_type='CHECKBOX',value=props.door_valance_bottom,tab_index=0,export=True)
        self.add_prompt(name="Left Side Full Height",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Right Side Full Height",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Valance Each Unit",prompt_type='CHECKBOX',value=props.valance_each_unit,tab_index=0,export=True)
        self.add_prompt(name="Valance Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    
    def add_prompt_formulas(self):
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        tt = self.get_var("Top Thickness",'tt')
        bt = self.get_var("Bottom Thickness",'bt')
        bkt = self.get_var("Back Thickness",'bkt')
        lfe = self.get_var("Left Fin End",'lfe')
        rfe = self.get_var("Right Fin End",'rfe')
        if self.carcass_type in {'Base','Sink','Tall'}:
            kick_height = self.get_var("Toe Kick Height",'kick_height')
        if self.carcass_type in {'Upper','Tall'}:
            vhb = self.get_var("Valance Height Bottom",'vhb')
            vht = self.get_var("Valance Height Top",'vht')
            
        Side_Pointer_Name = 'Cabinet_Unfinished_Side' + self.open_name
        FE_Pointer_Name = 'Cabinet_Finished_Side' + self.open_name
        Top_Pointer_Name = 'Cabinet_Top' + self.open_name
        Bottom_Pointer_Name = 'Cabinet_Bottom' + self.open_name
        Thick_Back_Pointer_Name = 'Cabinet_Thick_Back' + self.open_name
        Edgebanding_Pointer_Name = 'Cabinet_Body_Edges' + self.open_name            
            
        self.prompt('Left Side Thickness','IF(lfe,THICKNESS(sgi,"' + FE_Pointer_Name +'"),THICKNESS(sgi,"' + Side_Pointer_Name +'"))',[lfe,sgi])
        self.prompt('Right Side Thickness','IF(rfe,THICKNESS(sgi,"' + FE_Pointer_Name +'"),THICKNESS(sgi,"' + Side_Pointer_Name +'"))',[rfe,sgi])
        self.prompt('Top Thickness','THICKNESS(sgi,"' + Top_Pointer_Name +'")',[sgi])
        self.prompt('Bottom Thickness','THICKNESS(sgi,"' + Bottom_Pointer_Name +'")',[sgi])
        if self.carcass_type in {'Base','Sink','Tall'}:
            self.prompt('Toe Kick Thickness','THICKNESS(sgi,"Cabinet_Toe_Kick")',[sgi])
        if self.carcass_type == 'Sink':
            self.prompt('Sub Front Thickness','THICKNESS(sgi,"Sink_Sub_Front")',[sgi])
        self.prompt('Back Thickness','THICKNESS(sgi,"' + Thick_Back_Pointer_Name +'")',[sgi])
        self.prompt('Thick Back Thickness','THICKNESS(sgi,"Cabinet_Thick_Back' + self.open_name +'")',[sgi])
        self.prompt('Filler Thickness','THICKNESS(sgi,"Cabinet_Filler")',[sgi])
        self.prompt('Nailer Thickness','THICKNESS(sgi,"Cabinet_Nailer")',[sgi])
        if self.carcass_type in {'Tall','Upper'}:
            self.prompt('Valance Thickness','THICKNESS(sgi,"Cabinet_Valance")',[sgi])
        self.prompt('Edgebanding Thickness','EDGE_THICKNESS(sgi,"' + Edgebanding_Pointer_Name + '")',[sgi])
        
        if self.carcass_type == 'Base':
            self.prompt('Top Inset','tt',[tt])
            self.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
        if self.carcass_type == 'Sink':
            self.prompt('Top Inset',value = unit.inch(.75))
            self.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
        if self.carcass_type == 'Tall':
            self.prompt('Top Inset','vht+tt',[vht,tt])
            self.prompt('Bottom Inset','kick_height+bt',[kick_height,bt])
        if self.carcass_type == 'Upper':
            self.prompt('Top Inset','vht+tt',[vht,tt])
            self.prompt('Bottom Inset','vhb+bt',[vhb,bt])
        if self.carcass_type == 'Suspended':
            self.prompt('Top Inset','tt',[tt])
            self.prompt('Bottom Inset','bt',[bt])
        
        self.prompt('Back Inset','bkt',[bkt])
    
    def add_sides(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        width = self.get_var('dim_x','width')
        height = self.get_var('dim_z','height')
        depth = self.get_var('dim_y','depth')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Left_Fin_End = self.get_var('Left Fin End')
        Right_Fin_End = self.get_var('Right Fin End')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Cabinet_Depth_Left = self.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.get_var("Cabinet Depth Right")
        sides = []
    
        if self.carcass_type in {"Base","Tall","Sink"}:
            left_side = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
            left_side.set_name(self.carcass_type + " Left Side")
            left_side.y_loc('depth',[depth])
            left_side.x_dim('height',[height])
            left_side.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
            left_side.z_rot(value = 90)
            sides.append(left_side)
        
            right_side = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
            right_side.set_name(self.carcass_type + " Right Side")
            right_side.x_dim('height',[height])
            right_side.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
            sides.append(right_side)
            
            left_fe = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
            left_fe.set_name(self.carcass_type + " Left FE")
            left_fe.y_loc('depth',[depth])
            left_fe.x_dim('height',[height])
            left_fe.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
            left_fe.z_rot(value = 90)
            sides.append(left_fe)
            
            right_fe = self.add_assembly(NOTCHED_SIDE if props.use_notched_sides else PART_WITH_FRONT_EDGEBANDING)
            right_fe.set_name(self.carcass_type + " Right FE")
            right_fe.x_dim('height',[height])
            right_fe.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
            sides.append(right_fe)
        
        if self.carcass_type in {"Upper","Suspended"}:
            left_side = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
            left_side.set_name(self.carcass_type + " Left Side")
            left_side.y_loc('depth',[depth])
            left_side.x_dim('height',[height])
            left_side.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
            left_side.z_rot(value = 90)
            sides.append(left_side)
        
            right_side = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
            right_side.set_name(self.carcass_type + " Right Side")
            right_side.x_dim('height',[height])
            right_side.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
            sides.append(right_side)
            
            left_fe = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
            left_fe.set_name(self.carcass_type + " Left FE")
            left_fe.y_loc('depth',[depth])
            left_fe.x_dim('height',[height])
            left_fe.y_dim('-Cabinet_Depth_Left',[Cabinet_Depth_Left])
            left_fe.z_rot(value = 90)
            sides.append(left_fe)
            
            right_fe = self.add_assembly(PART_WITH_FRONT_AND_BOTTOM_EDGEBANDING)
            right_fe.set_name(self.carcass_type + " Right FE")
            right_fe.x_dim('height',[height])
            right_fe.y_dim('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
            sides.append(right_fe)
    
        for side in sides:
            side.x_loc(value = 0)
            side.y_loc(value = 0)
            side.z_loc(value = 0)
            side.x_rot(value = 0)
            side.y_rot(value = -90)
            side.edgebanding('Cabinet_Body_Edges',l1=True)
            if self.carcass_type in {'Base','Tall'}:
                side.prompt('Notch X Dimension','Toe_Kick_Height',[Toe_Kick_Height])
                side.prompt('Notch Y Dimension','Toe_Kick_Setback',[Toe_Kick_Setback])
            if "Left Side" in side.obj_bp.mv.name_object:
                side.prompt('Hide','IF(Left_Fin_End,True,False)',[Left_Fin_End])
                side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
                side.cutpart("Cabinet_Unfinished_Side"+self.open_name)
            if "Right Side" in side.obj_bp.mv.name_object:
                side.prompt('Hide','IF(Right_Fin_End,True,False)',[Right_Fin_End])
                side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
                side.cutpart("Cabinet_Unfinished_Side"+self.open_name)
                side.x_loc('width',[width])
            if "Left FE" in side.obj_bp.mv.name_object:
                side.prompt('Hide','IF(Left_Fin_End,False,True)',[Left_Fin_End])
                side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
                side.cutpart("Cabinet_Finished_Side"+self.open_name)
            if "Right FE" in side.obj_bp.mv.name_object:
                side.prompt('Hide','IF(Right_Fin_End,False,True)',[Right_Fin_End])
                side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
                side.cutpart("Cabinet_Finished_Side"+self.open_name)
                side.x_loc('width',[width])
                
    def add_fillers(self):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Height = self.get_var('dim_z','Height')
        Left_Side_Wall_Filler = self.get_var("Left Side Wall Filler")
        Right_Side_Wall_Filler = self.get_var("Right Side Wall Filler")
        Filler_Thickness = self.get_var("Filler Thickness")
        Cabinet_Depth_Left = self.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.get_var("Cabinet Depth Right")
        
        if self.carcass_type in {'Base','Sink','Tall'}:
            Toe_Kick_Height = self.get_var("Toe Kick Height")
            
        left_filler = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        left_filler.set_name("Left Filler")
        left_filler.x_loc('Cabinet_Depth_Left',[Cabinet_Depth_Left])
        left_filler.y_loc('Depth',[Depth])
        left_filler.z_loc('Height',[Height])
        left_filler.x_rot(value = 90)
        left_filler.y_rot(value = 90)
        left_filler.z_rot(value = -90)
        left_filler.y_dim('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_filler.z_dim('Filler_Thickness',[Filler_Thickness])
        left_filler.prompt('Hide','IF(Left_Side_Wall_Filler>0,False,True)',[Left_Side_Wall_Filler])
        left_filler.cutpart('Cabinet_Filler')
        
        right_filler = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        right_filler.set_name("Right Filler")
        right_filler.x_loc('Width',[Width])
        right_filler.y_loc('-Cabinet_Depth_Right',[Cabinet_Depth_Right])
        right_filler.z_loc('Height',[Height])
        right_filler.x_rot(value = 90)
        right_filler.y_rot(value = 90)
        right_filler.z_rot(value = 0)
        right_filler.y_dim('Right_Side_Wall_Filler',[Right_Side_Wall_Filler])
        right_filler.z_dim('-Filler_Thickness',[Filler_Thickness])
        right_filler.prompt('Hide','IF(Right_Side_Wall_Filler>0,False,True)',[Right_Side_Wall_Filler])
        right_filler.cutpart('Cabinet_Filler')
        
        if self.carcass_type in {'Base','Sink','Tall'}:
            left_filler.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
            right_filler.x_dim('Height-Toe_Kick_Height',[Height,Toe_Kick_Height])
            
        if self.carcass_type in {'Upper','Suspended'}:
            left_filler.x_dim('Height',[Height])
            right_filler.x_dim('Height',[Height])
            
    def add_full_top(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Top_Thickness = self.get_var('Top Thickness')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Cabinet_Depth_Left = self.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.get_var("Cabinet Depth Right")
        
        if self.carcass_shape == 'Diagonal':
            top = self.add_assembly(CHAMFERED_PART)
        if self.carcass_shape == 'Notched':
            top = self.add_assembly(CORNER_NOTCH_PART)
        
        top.set_name(self.carcass_type + " Top")
        top.x_dim('Width-Right_Side_Thickness',[Width,Right_Side_Thickness])
        top.y_dim('Depth+Left_Side_Thickness',[Depth,Left_Side_Thickness])
        top.z_dim('-Top_Thickness',[Top_Thickness])
        top.x_loc(value = 0)
        top.y_loc(value = 0)
        top.z_loc('IF(Height>0,Height,0)',[Height])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.cutpart("Cabinet_Top"+self.open_name)
        top.prompt('Left Depth','Cabinet_Depth_Left',[Cabinet_Depth_Left])
        top.prompt('Right Depth','Cabinet_Depth_Right',[Cabinet_Depth_Right])
        top.edgebanding('Cabinet_Body_Edges', l1 = True)
        
    def add_bottom(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Bottom_Thickness = self.get_var('Bottom Thickness')
        Cabinet_Depth_Left = self.get_var("Cabinet Depth Left")
        Cabinet_Depth_Right = self.get_var("Cabinet Depth Right")
        
        if self.carcass_shape == 'Diagonal':
            bottom = self.add_assembly(CHAMFERED_PART)
        if self.carcass_shape == 'Notched':
            bottom = self.add_assembly(CORNER_NOTCH_PART)
            
        bottom.set_name(self.carcass_type + " Bottom")
        bottom.x_dim('Width-Right_Side_Thickness',[Width,Right_Side_Thickness])
        bottom.y_dim('Depth+Left_Side_Thickness',[Depth,Left_Side_Thickness])
        bottom.x_loc(value = 0)
        bottom.y_loc(value = 0)
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 0)
        bottom.prompt('Left Depth','Cabinet_Depth_Left',[Cabinet_Depth_Left])
        bottom.prompt('Right Depth','Cabinet_Depth_Right',[Cabinet_Depth_Right])
        bottom.cutpart("Cabinet_Bottom"+self.open_name)
        bottom.edgebanding('Cabinet_Body_Edges', l1 = True)
        
        if self.carcass_type in {'Upper','Suspended'}:
            bottom.z_dim('Bottom_Thickness',[Bottom_Thickness])
            bottom.z_loc('Height',[Height])
            
        if self.carcass_type in {'Base','Tall','Sink'}:
            bottom.z_dim('Bottom_Thickness',[Bottom_Thickness])
            bottom.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            
            left_kick = self.add_assembly(PART_WITH_NO_EDGEBANDING)
            left_kick.set_name("Left Toe Kick")
            left_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
            left_kick.z_dim('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
            left_kick.x_loc('Cabinet_Depth_Left-Toe_Kick_Setback',[Cabinet_Depth_Left,Toe_Kick_Setback])
            left_kick.y_loc('Depth+Left_Side_Thickness',[Depth,Left_Side_Thickness])
            left_kick.z_loc(value = 0)
            left_kick.x_rot(value = 90)
            left_kick.y_rot(value = 0)
            left_kick.z_rot(value = 90)
            left_kick.cutpart("Toe_Kick")
    
            if self.carcass_shape == 'Notched':
                left_kick.x_dim('fabs(Depth)-Cabinet_Depth_Right+Toe_Kick_Setback',[Depth,Cabinet_Depth_Right,Toe_Kick_Setback])
                
                right_kick = self.add_assembly(PART_WITH_NO_EDGEBANDING)
                right_kick.set_name("Left Toe Kick")
                right_kick.x_dim('fabs(Width)-Cabinet_Depth_Left+Toe_Kick_Setback-Right_Side_Thickness',[Width,Cabinet_Depth_Left,Toe_Kick_Setback,Right_Side_Thickness])
                right_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
                right_kick.z_dim('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
                right_kick.x_loc('Cabinet_Depth_Left-Toe_Kick_Setback',[Cabinet_Depth_Left,Toe_Kick_Setback,Toe_Kick_Thickness])
                right_kick.y_loc('-Cabinet_Depth_Right+Toe_Kick_Setback',[Cabinet_Depth_Right,Toe_Kick_Setback])
                right_kick.z_loc(value = 0)
                right_kick.x_rot(value = 90)
                right_kick.y_rot(value = 0)
                right_kick.z_rot(value = 0)
                right_kick.cutpart("Toe_Kick")
            
            else:
                left_kick.x_dim('sqrt(((fabs(Depth)-Left_Side_Thickness-Cabinet_Depth_Right+Toe_Kick_Setback)**2)+((fabs(Width)-Right_Side_Thickness-Cabinet_Depth_Left+Toe_Kick_Setback)**2))',
                                [Depth,Width,Cabinet_Depth_Right,Cabinet_Depth_Left,Left_Side_Thickness,Right_Side_Thickness,Toe_Kick_Setback])
                
                left_kick.z_rot('atan((fabs(Depth)-Left_Side_Thickness-Cabinet_Depth_Right+Toe_Kick_Setback)/(fabs(Width)-Right_Side_Thickness-Cabinet_Depth_Left+Toe_Kick_Setback))',
                                [Depth,Width,Left_Side_Thickness,Right_Side_Thickness,Cabinet_Depth_Left,Cabinet_Depth_Right,Toe_Kick_Setback])
    
    def add_backs(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Top_Inset = self.get_var('Top Inset')
        Bottom_Inset = self.get_var('Bottom Inset')
        Back_Thickness = self.get_var('Back Thickness')

        r_back = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        r_back.set_name(self.carcass_type + " Back")
        r_back.x_loc('Back_Thickness',[Back_Thickness])
        r_back.y_loc(value = 0)
        r_back.z_loc('IF(Height>0,Bottom_Inset,Height+Bottom_Inset)',[Bottom_Inset,Height])
        r_back.x_rot(value = 0)
        r_back.y_rot(value = -90)
        r_back.z_rot(value = -90)
        r_back.x_dim('fabs(Height)-(Top_Inset+Bottom_Inset)',[Height,Top_Inset,Bottom_Inset])
        r_back.y_dim('Width-(Back_Thickness+Right_Side_Thickness)',[Width,Back_Thickness,Right_Side_Thickness])
        r_back.z_dim('-Back_Thickness',[Back_Thickness])
        r_back.cutpart("Cabinet_Thick_Back" + self.open_name)
        
        l_back = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        l_back.set_name(self.carcass_type + " Back")
        l_back.x_loc(value=0)
        l_back.y_loc(value = 0)
        l_back.z_loc('IF(Height>0,Bottom_Inset,Height+Bottom_Inset)',[Bottom_Inset,Height])
        l_back.x_rot(value = 0)
        l_back.y_rot(value = -90)
        l_back.z_rot(value = 180)
        l_back.x_dim('fabs(Height)-(Top_Inset+Bottom_Inset)',[Height,Top_Inset,Bottom_Inset])
        l_back.y_dim('fabs(Depth)-Right_Side_Thickness',[Depth,Right_Side_Thickness])
        l_back.z_dim('Back_Thickness',[Back_Thickness])
        l_back.cutpart("Cabinet_Thick_Back" + self.open_name)
        
    def add_valances(self):
        pass
    
    def draw(self):
        self.create_assembly()
        
        self.add_common_carcass_prompts()
        
        if self.carcass_type in {"Base","Tall"}:
            self.add_base_assembly_prompts()
        
        self.add_prompt_formulas()
        self.add_sides()
        self.add_full_top()
        self.add_bottom()
        self.add_backs()
        self.add_fillers()

        self.update()
        
class Outside_Corner_Carcass(fd_types.Assembly):
    
    library_name = "Carcasses"
    placement_type = ""
    type_assembly = "INSERT"
    
    carcass_type = "" # Base, Tall, Upper, Sink, Suspended
    open_finish = False
    carcass_shape = '' # Diagonal, Radius
    open_name = ""

    def add_prompts(self):
        props = cabinet_properties.get_scene_props().carcass_defaults
        self.add_tab(name='Carcass Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        if self.carcass_type == "Base":
            self.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value= props.toe_kick_height,tab_index=0)
            self.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value= props.toe_kick_setback,tab_index=0)
            
        if self.carcass_type == "Tall":
            self.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value= props.toe_kick_height,tab_index=0)
            self.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value= props.toe_kick_setback,tab_index=0)
            self.add_prompt(name="Valance Each Unit",prompt_type='CHECKBOX',value= props.valance_each_unit,tab_index=0)
            self.add_prompt(name="Valance Height Top",prompt_type='DISTANCE',value= props.valance_height_top,tab_index=0)
            self.add_prompt(name="Door Valance Top",prompt_type='CHECKBOX',value= props.door_valance_top,tab_index=0)
            self.add_prompt(name="Valance Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=2)
            
        if self.carcass_type == "Upper":
            self.add_prompt(name="Valance Each Unit",prompt_type='CHECKBOX',value= props.valance_each_unit,tab_index=0)
            self.add_prompt(name="Valance Height Top",prompt_type='DISTANCE',value= props.valance_height_top,tab_index=0)
            self.add_prompt(name="Valance Height Bottom",prompt_type='DISTANCE',value= props.valance_height_bottom,tab_index=0)
            self.add_prompt(name="Door Valance Top",prompt_type='CHECKBOX',value= props.door_valance_top,tab_index=0)
            self.add_prompt(name="Door Valance Bottom",prompt_type='CHECKBOX',value= props.g.door_valance_bottom,tab_index=0)
            self.add_prompt(name="Valance Thickness",prompt_type='DISTANCE',value= unit.inch(.75),tab_index=1)

        self.add_prompt(name="Toe Kick Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Thick Back Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Fixed Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Top Inset",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Bottom Inset",prompt_type='DISTANCE',value=0,tab_index=1)

        tt = self.get_var('Top Thickness','tt')
        bt = self.get_var('Bottom Thickness','bt')
        depth = self.get_var('dim_y','depth')
        
        self.x_dim('fabs(depth)',[depth])
        
        if self.carcass_type == 'Base':
            kick_height = self.get_var('Toe Kick Height','kick_height')
            
            self.prompt("Top Inset",'tt',[tt])
            self.prompt("Bottom Inset",'bt+kick_height',[bt,kick_height])
            
        if self.carcass_type == 'Tall':
            kick_height = self.get_var('Toe Kick Height','kick_height')
            vht = self.get_var('Valance Height Top','vht')
            
            self.prompt("Top Inset",'tt+vht',[tt,vht])
            self.prompt("Bottom Inset",'bt+kick_height',[bt,kick_height])
            
        if self.carcass_type == 'Upper':
            vht = self.get_var('Valance Height Top','vht')
            vhb = self.get_var('Valance Height Bottom','vhb')
            
            self.prompt("Top Inset",'tt+vht',[tt,vht])
            self.prompt("Bottom Inset",'bt+vhb',[bt,vhb])
    
    def add_left_back(self):
        kick_height = self.get_var('Toe Kick Height','kick_height')
        height = self.get_var('dim_z','height')
        depth = self.get_var('dim_y','depth')
        
        left_back = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        left_back.set_name("Left Back")
        left_back.x_loc(value=unit.inch(0))
        left_back.y_loc(value=unit.inch(0))
        left_back.z_loc('kick_height',[kick_height])
        left_back.y_rot(value=-90)
        left_back.x_dim('height-kick_height',[height,kick_height])
        left_back.y_dim('depth',[depth])
        left_back.z_dim(value=unit.inch(-.75))
        left_back.cutpart('Cabinet_Thick_Back' + self.open_name)
        left_back.edgebanding('Cabinet_Body_Edges',l1=True)
    
    def add_right_back(self):
        height = self.get_var('dim_z','height')
        width = self.get_var('dim_x','width')
        kick_height = self.get_var('Toe Kick Height','kick_height')
        tbt = self.get_var('Thick Back Thickness','tbt')
        
        right_back = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        right_back.set_name("Right Back")
        right_back.x_loc('tbt',[tbt])
        right_back.y_loc(value=unit.inch(0))
        right_back.z_loc('kick_height',[kick_height])
        right_back.y_rot(value=-90)
        right_back.z_rot(value=90)
        right_back.x_dim('height-kick_height',[height,kick_height])
        right_back.y_dim('(width-tbt)*-1',[width,tbt])
        right_back.x_dim(value=unit.inch(.75))
        right_back.cutpart('Cabinet_Thick_Back' + self.open_name)
        right_back.edgebanding('Cabinet_Body_Edges',l1=True)
        
    def add_top(self):
        height = self.get_var('dim_z','height')
        width = self.get_var('dim_x','width')
        depth = self.get_var('dim_y','depth')
        tbt = self.get_var('Thick Back Thickness','tbt')
        tt = self.get_var('Top Thickness','tt')
        vht = self.get_var('Valance Height Top','vht')

        top = self.add_assembly(RADIUS_CORNER_PART_WITH_EDGEBANDING if self.carcass_shape == 'Radius' else CHAMFERED_PART)
        top.set_name("Top")
        top.x_loc('tbt',[tbt])
        top.y_loc('-tbt',[tbt])
        if self.carcass_type == 'Base':
            top.z_loc('height',[height])
        if self.carcass_type == 'Tall':
            top.z_loc('height-vht',[height,vht])
        if self.carcass_type == 'Upper':
            top.z_loc('-vht',[vht])
        top.y_rot(value=-180)
        top.z_rot(value=90)
        top.x_dim('fabs(depth)-tbt',[depth,tbt])
        top.y_dim('(width-tbt)*-1',[width,tbt])
        top.z_dim('tt',[tt])
        top.prompt('Radius','width-tbt',[width,tbt])
        if self.carcass_shape == 'Diagonal':
            top.prompt('Left Depth',value = 0)
            top.prompt('Right Depth',value = 0)
        top.cutpart('Cabinet_Top' + self.open_name)
        top.edgebanding('Cabinet_Body_Edges',l1=True)
        
    def add_bottom(self):
        height = self.get_var('dim_z','height')
        width = self.get_var('dim_x','width')
        depth = self.get_var('dim_y','depth')
        kick_height = self.get_var('Toe Kick Height','kick_height')
        tbt = self.get_var('Thick Back Thickness','tbt')
        vhb = self.get_var('Valance Height Bottom','vhb')
        bt = self.get_var('Bottom Thickness','bt')

        bottom = self.add_assembly(RADIUS_CORNER_PART_WITH_EDGEBANDING if self.carcass_shape == 'Radius' else CHAMFERED_PART)
        bottom.x_loc('tbt',[tbt])
        bottom.y_loc('-tbt',[tbt])
        if self.carcass_type == 'Upper':
            bottom.z_loc('height+vhb',[height,vhb])
        else:
            bottom.z_loc('kick_height',[kick_height])
        bottom.y_rot(value=-180)
        bottom.z_rot(value=90)
        bottom.x_dim('fabs(depth)-tbt',[depth,tbt])
        bottom.y_dim('(width-tbt)*-1',[width,tbt])
        bottom.z_dim('(bt)*-1',[bt])
        bottom.prompt('Radius','width-tbt',[width,tbt])
        if self.carcass_shape == 'Diagonal':
            bottom.prompt('Left Depth',value = 0)
            bottom.prompt('Right Depth',value = 0)
        bottom.cutpart('Cabinet_Bottom' + self.open_name)
        bottom.edgebanding('Cabinet_Body_Edges',l1=True)
        
    def add_toe_kick(self):
        width = self.get_var('dim_x','width')
        depth = self.get_var('dim_y','depth')
        kick_height = self.get_var('Toe Kick Height','kick_height')
        kick_setback = self.get_var('Toe Kick Setback','kick_setback')
        tkt = self.get_var('Toe Kick Thickness','tkt')

        toe_kick = self.add_assembly(BENDING_PART if self.carcass_shape == 'Radius' else PART_WITH_NO_EDGEBANDING)
        toe_kick.x_loc('width-kick_setback',[width,kick_setback])
        toe_kick.y_loc(value=unit.inch(0))
        toe_kick.x_loc(value=unit.inch(0))
        toe_kick.x_rot(value=90)
        if self.carcass_shape == 'Diagonal':
            toe_kick.x_dim('sqrt(((fabs(depth)-kick_setback)**2)+((fabs(width)-kick_setback)**2))*-1',[width,depth,kick_setback])
            toe_kick.z_rot('atan((fabs(depth)+kick_setback)/(fabs(width)+kick_setback))',[width,depth,kick_setback])

        if self.carcass_shape == 'Radius':
            toe_kick.z_rot(value=-90)
            toe_kick.x_dim('radians(90)*(width-kick_setback)',[width,kick_setback])
            toe_kick.prompt('Bending',value=90)

        toe_kick.y_dim('kick_height',[kick_height])
        toe_kick.z_dim('tkt',[tkt])
        toe_kick.cutpart('Cabinet_Toe_Kick')
    
    def add_top_valance(self):
        width = self.get_var('dim_x','width')
        depth = self.get_var('dim_y','depth')
        height = self.get_var('dim_z','height')
        vht = self.get_var('Valance Height Top','vht')
        tbt = self.get_var('Thick Back Thickness','tbt')
        vt = self.get_var('Valance Thickness','vt')

        top_valance = self.add_assembly(BENDING_PART if self.carcass_shape == 'Radius' else PART_WITH_NO_EDGEBANDING)
        top_valance.set_name("Top Valance")
        top_valance.x_loc('width',[width])
        top_valance.y_loc('-tbt',[tbt])
        if self.carcass_type == 'TALL':
            top_valance.z_loc('height-vht',[height,vht])
        if self.carcass_type == 'UPPER':
            top_valance.z_loc('-vht',[vht])
        top_valance.x_rot(value=90)
        if self.carcass_shape == 'Diagonal':
            top_valance.x_dim('sqrt(((fabs(depth)-tbt)**2)+((fabs(width)-tbt)**2))*-1',[width,depth,tbt])
            top_valance.z_rot('atan((fabs(depth)-tbt)/(fabs(width)-tbt))',[width,depth,tbt])
            
        if self.carcass_shape == 'Radius':
            top_valance.z_rot(value=-90)
            top_valance.x_dim('radians(90)*(width-tbt)',[width,tbt])
            top_valance.prompt('Bending',value=90)
            
        top_valance.y_dim('vht',[vht])
        top_valance.z_dim('-vt',[vt])
        top_valance.cutpart('Cabinet_Valance')
        top_valance.prompt('Hide','IF(vht<=0,True,False)',[vht])
        
    def add_bottom_valance(self):
        width = self.get_var('dim_x','width')
        height = self.get_var('dim_z','height')
        depth = self.get_var('dim_y','depth')
        vhb = self.get_var('Valance Height Bottom','vhb')
        tbt = self.get_var('Thick Back Thickness','tbt')
        vt = self.get_var('Valance Thickness','vt')

        bottom_valance = self.add_assembly(BENDING_PART if self.carcass_shape == 'Radius' else PART_WITH_NO_EDGEBANDING)
        bottom_valance.set_name("Bottom Valance")
        bottom_valance.x_loc('width',[width])
        bottom_valance.y_loc('-tbt',[tbt])
        bottom_valance.z_loc('height',[height,vhb])
        bottom_valance.x_rot(value=90)
        if self.carcass_shape == 'Diagonal':
            bottom_valance.x_dim('sqrt(((fabs(depth)-tbt)**2)+((fabs(width)-tbt)**2))*-1',[width,depth,tbt])
            bottom_valance.z_rot('atan((fabs(depth)-tbt)/(fabs(width)-tbt))',[width,depth,tbt])
            
        if self.carcass_shape == 'Radius':
            bottom_valance.z_rot(value=-90)
            bottom_valance.x_dim('radians(90)*(width-tbt)',[width,tbt])
            bottom_valance.prompt('Bending',value=90)
            
        bottom_valance.y_dim('vhb',[vhb])
        bottom_valance.z_dim('-vt',[vt])
        bottom_valance.cutpart('Cabinet_Valance')
        bottom_valance.prompt('Hide','IF(vhb<=0,True,False)',[vhb])
    
    def draw(self):
        self.create_assembly()
        self.open_name = ' Open' if self.open_finish else ''
            
        self.add_prompts()
        self.add_left_back()
        self.add_right_back()
        self.add_bottom()
        self.add_top()

        if self.carcass_type in {"BASE","TALL"}:
            self.add_toe_kick()
            
        if self.carcass_type == 'TALL':
            self.add_top_valance()
        
        if self.carcass_type == 'UPPER':
            self.add_top_valance()
            self.add_bottom_valance()
            
        self.update()
        
#---------Standard Carcasses
        
class INSERT_Base_Carcass(Standard_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Base Carcass"
        self.carcass_type = "Base"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Tall_Carcass(Standard_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Tall Carcass"
        self.carcass_type = "Tall"
        self.width = unit.inch(18)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)
        
class INSERT_Upper_Carcass(Standard_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Upper Carcass"
        self.carcass_type = "Upper"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        
class INSERT_Sink_Carcass(Standard_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Sink Carcass"
        self.carcass_type = "Sink"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Suspended_Carcass(Standard_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Suspended Carcass"
        self.carcass_type = "Suspended"
        self.width = unit.inch(18)
        self.height = unit.inch(6)
        self.depth = unit.inch(23)

#---------Transition Carcasses

class INSERT_Base_Transition_Carcass(Transition_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Base Carcass"
        self.carcass_type = "Base"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Tall_Transition_Carcass(Transition_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Tall Carcass"
        self.carcass_type = "Tall"
        self.width = unit.inch(18)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)
        
class INSERT_Upper_Transition_Carcass(Transition_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Upper Carcass"
        self.carcass_type = "Upper"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        
class INSERT_Sink_Transition_Carcass(Transition_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Sink Carcass"
        self.carcass_type = "Sink"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Suspended_Transition_Carcass(Transition_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Suspended Carcass"
        self.carcass_type = "Suspended"
        self.width = unit.inch(18)
        self.height = unit.inch(6)
        self.depth = unit.inch(23)

#---------Inside Corner Carcasses

class INSERT_Base_Inside_Corner_Notched_Carcass(Inside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Base Inside Corner Notched Carcass"
        self.carcass_type = "Base"
        self.carcass_shape = "Notched"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(36)
        self.left_right_depth = unit.inch(23)
        
class INSERT_Upper_Inside_Corner_Notched_Carcass(Inside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Upper Inside Corner Notched Carcass"
        self.carcass_type = "Upper"
        self.carcass_shape = "Notched"
        self.width = unit.inch(12)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.left_right_depth = unit.inch(12)

class INSERT_Base_Inside_Corner_Diagonal_Carcass(Inside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Base Inside Corner Diagonal Carcass"
        self.carcass_type = "Base"
        self.carcass_shape = "Diagonal"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(36)
        self.left_right_depth = unit.inch(23)
        
class INSERT_Upper_Inside_Corner_Diagonal_Carcass(Inside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Upper Inside Corner Diagonal Carcass"
        self.carcass_type = "Upper"
        self.carcass_shape = "Diagonal"
        self.width = unit.inch(12)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        self.left_right_depth = unit.inch(12)

#---------Outside Corner Carcasses

class INSERT_Base_Outside_Chamfered_Corner_Carcass(Outside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Base Outside Chamfered Corner Carcass"
        self.carcass_type = "Base"
        self.carcass_shape = "Diagonal"
        self.width = unit.inch(23)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Base_Outside_Radius_Corner_Carcass(Outside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Base Outside Radius Corner Carcass"
        self.carcass_type = "Base"
        self.carcass_shape = "Radius"
        self.width = unit.inch(23)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)

class INSERT_Tall_Outside_Chamfered_Corner_Carcass(Outside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Tall Outside Chamfered Corner Carcass"
        self.carcass_type = "Tall"
        self.carcass_shape = "Diagonal"
        self.width = unit.inch(23)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)
        
class INSERT_Tall_Outside_Radius_Corner_Carcass(Outside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Tall Outside Radius Corner Carcass"
        self.carcass_type = "Tall"
        self.carcass_shape = "Radius"
        self.width = unit.inch(23)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)

class INSERT_Upper_Outside_Chamfered_Corner_Carcass(Outside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Upper Outside Chamfered Corner Carcass"
        self.carcass_type = "Upper"
        self.carcass_shape = "Diagonal"
        self.width = unit.inch(12)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
        
class INSERT_Upper_Outside_Radius_Corner_Carcass(Outside_Corner_Carcass):
    
    def __init__(self):
        self.category_name = "Carcasses"
        self.assembly_name = "Upper Outside Radius Corner Carcass"
        self.carcass_type = "Upper"
        self.carcass_shape = "Radius"
        self.width = unit.inch(12)
        self.height = unit.inch(34)
        self.depth = unit.inch(12)
    