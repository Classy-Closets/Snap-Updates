"""
Microvellum 
Columns
Stores the logic and product defs for columns
"""

import bpy
from mv import fd_types, utils, unit
from os import path
from . import cabinet_properties

ROOT_DIR = path.dirname(__file__)
COLUMN_PARTS_DIR = path.join(ROOT_DIR,"Columns")
CUTPARTS_DIR = path.join(ROOT_DIR,"Cabinet Assemblies","Cut Parts")
PART_WITH_FRONT_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with Front Edgebanding.blend")

#---------PRODUCT TEMPLATES

class Column(fd_types.Assembly):
    library_name = "Columns"
    category_name = "Standard Columns"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".column_prompts"
    type_assembly = "PRODUCT"

    product_type = None

    object_name = ""
    height_above_floor = 0
    trim = None

    def draw(self):
        self.create_assembly()

        self.add_tab(name='Basic Column Options',tab_type='VISIBLE')
        self.add_tab(name='Formuls',tab_type='HIDDEN')
        self.add_prompt(name="Extend Left End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Extend Right End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Panel Depth",prompt_type='DISTANCE',value=unit.inch(4),tab_index=0)
        self.add_prompt(name="Part Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)

        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Extend_Left_End = self.get_var("Extend Left End")
        Extend_Right_End = self.get_var("Extend Right End")
        Panel_Depth = self.get_var("Panel Depth")
        Part_Thickness = self.get_var("Part Thickness")

        left_part = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        left_part.set_name("Left Part")
        left_part.x_loc(value = 0)
        left_part.y_loc('IF(Extend_Left_End,0,Depth+Panel_Depth)',[Extend_Left_End,Depth,Panel_Depth])
        left_part.z_loc(value = 0)
        left_part.x_rot(value = 0)
        left_part.y_rot(value = -90)
        left_part.z_rot(value = 0)
        left_part.x_dim('Height',[Height])
        left_part.y_dim('IF(Extend_Left_End,Depth,-Panel_Depth)',[Depth,Extend_Left_End,Panel_Depth])
        left_part.z_dim('-Part_Thickness',[Part_Thickness])
        left_part.cutpart('Base_Side_FE')
        left_part.edgebanding('Cabinet_Body_Edges',l1=True)

        right_part = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        right_part.set_name("Right Part")
        right_part.x_loc('Width',[Width])
        right_part.y_loc('IF(Extend_Right_End,0,Depth+Panel_Depth)',[Extend_Right_End,Depth,Panel_Depth])
        right_part.z_loc(value = 0)
        right_part.x_rot(value = 0)
        right_part.y_rot(value = -90)
        right_part.z_rot(value = 0)
        right_part.x_dim('Height',[Height])
        right_part.y_dim('IF(Extend_Right_End,Depth,-Panel_Depth)',[Depth,Extend_Right_End,Panel_Depth])
        right_part.z_dim('Part_Thickness',[Part_Thickness])
        right_part.cutpart('Base_Side_FE')
        right_part.edgebanding('Cabinet_Body_Edges',l1=True)

        front_part = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        front_part.set_name("Front Part")
        front_part.x_loc('Part_Thickness',[Part_Thickness])
        front_part.y_loc('Depth',[Depth])
        front_part.z_loc(value = 0)
        front_part.x_rot(value = 0)
        front_part.y_rot(value = -90)
        front_part.z_rot(value = -90)
        front_part.x_dim('Height',[Height])
        front_part.y_dim('Width-(Part_Thickness*2)',[Width,Part_Thickness])
        front_part.z_dim('Part_Thickness',[Part_Thickness])
        front_part.cutpart('Base_Side_FE')
        front_part.edgebanding('Cabinet_Body_Edges',l1=True)
            
        self.update()
       
class Angled_Column(fd_types.Assembly):
    library_name = "Columns"
    category_name = "Angled Columns"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".angled_column_prompts"
    type_assembly = "PRODUCT"
    detail_piece = ""
    detail_type = ''
    orientation = ''

    product_type = None

    object_name = ""
    height_above_floor = 0
    trim = None

    def draw(self):  
        props = cabinet_properties.get_scene_props()
        self.create_assembly()

        self.add_tab(name='Basic Column Options',tab_type='VISIBLE')
        self.add_prompt(name="Extend Left End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Extend Right End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Panel Depth",prompt_type='DISTANCE',value=unit.inch(4),tab_index=0)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')        
        
        detail = self.add_assembly(path.join(COLUMN_PARTS_DIR,props.column_category,self.detail_piece+".blend"))
        detail.obj_bp.mv.name_object = self.assembly_name + " Column Style"
        obj_props = cabinet_properties.get_object_props(detail.obj_bp)
        obj_props.is_column = True
        detail.material("Exposed_Exterior_Surface")
        detail.y_rot(value = -90)
        detail.y_loc("Depth+INCH(1.75)",[Depth])
        
        if self.orientation == 'LEFT':
            detail.z_rot(value = 90)
            detail.x_loc(value = unit.inch(1.75)) 
            
            if self.detail_type == 'C':
                column = self.add_assembly(path.join(COLUMN_PARTS_DIR,props.column_category,"Column_C_Left.blend"))

            elif self.detail_type == 'R':
                column = self.add_assembly(path.join(COLUMN_PARTS_DIR,props.column_category,"Column_R_Left.blend"))
                
        elif self.orientation == 'RIGHT':
            detail.z_rot(value = 180)
            detail.x_loc(value = unit.inch(0.25))
            
            if self.detail_type == 'C':
                column = self.add_assembly(path.join(COLUMN_PARTS_DIR,props.column_category,"Column_C_Right.blend"))
                
            elif self.detail_type == 'R':
                column = self.add_assembly(path.join(COLUMN_PARTS_DIR,props.column_category,"Column_R_Right.blend"))
            
        column.material("Exposed_Exterior_Surface")
        column.x_dim('Width',[Width])
        column.y_dim('Depth',[Depth])
        
        if self.product_type == 'UPPER':
            column.z_loc("Height",[Height])
            column.z_dim('-Height',[Height])
            detail.z_loc("Height",[Height])
            detail.x_dim("-Height",[Height])
            
        elif self.product_type == 'TALL':
            column.z_dim('Height',[Height])
            detail.x_dim("Height*0.5",[Height])
            detail2 = self.add_assembly(path.join(COLUMN_PARTS_DIR,props.column_category,self.detail_piece+".blend"))
            props = cabinet_properties.get_object_props(detail2.obj_bp)
            props.is_column = True
            detail2.obj_bp.mv.name_object = self.assembly_name + " Column Style"
            detail2.material("Exposed_Exterior_Surface")
            detail2.y_loc("Depth+INCH(1.75)",[Depth])
            detail2.z_loc("Height*0.5",[Height])
            detail2.y_rot(value = -90)              
            detail2.x_dim("Height*0.5",[Height])
            
            if self.orientation == 'LEFT':
                detail2.z_rot(value = 90)
                detail2.x_loc(value = unit.inch(1.75))          
            elif self.orientation == 'RIGHT':
                detail2.z_rot(value = 180)
                detail2.x_loc(value = unit.inch(0.25))                        
            
        else:
            column.z_dim('Height',[Height])
            detail.x_dim("Height",[Height])  
            
        self.update()

#---------PRODUCT: CABINET COLUMNS

class PRODUCT_Base_Column(Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.category_name = "Standard Columns"
        self.assembly_name = "Base Column"
        self.width = props.column_width
        self.height = props.base_cabinet_height
        self.depth = props.base_cabinet_depth

class PRODUCT_Tall_Column(Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.category_name = "Standard Columns"
        self.assembly_name = "Tall Column"
        self.width = props.column_width
        self.height = props.tall_cabinet_height
        self.depth = props.tall_cabinet_depth
        
class PRODUCT_Upper_Column(Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().size_defaults
        self.category_name = "Standard Columns"
        self.assembly_name = "Upper Column"
        self.width = props.column_width
        self.height = props.upper_cabinet_height
        self.depth = props.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.height_above_floor
        
#---------PRODUCT: ANGLED CABINET COLUMNS        
        
class PRODUCT_Base_Angled_Column_Left(Angled_Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props()
        self.product_type = 'BASE'
        self.category_name = "Angled Columns"
        self.assembly_name = "Base Angled Column Left"
        self.detail_piece = props.column_style
        self.orientation = 'LEFT'
        self.detail_type = 'C'
        self.width = props.size_defaults.column_width
        self.height = props.size_defaults.base_cabinet_height
        self.depth = props.size_defaults.base_cabinet_depth
        
class PRODUCT_Base_Angled_Column_Right(Angled_Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props()
        self.product_type = 'BASE'
        self.category_name = "Angled Columns"
        self.assembly_name = "Base Angled Column Right"
        self.detail_piece = props.column_style
        self.orientation = 'RIGHT'
        self.detail_type = 'C'
        self.width = props.size_defaults.column_width
        self.height = props.size_defaults.base_cabinet_height
        self.depth = props.size_defaults.base_cabinet_depth       

class PRODUCT_Tall_Angled_Column_Left(Angled_Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props()
        self.product_type = 'TALL'
        self.category_name = "Angled Columns"
        self.assembly_name = "Tall Angled Column Left"
        self.detail_piece = props.column_style
        self.orientation = 'LEFT'
        self.detail_type = 'C'
        self.width = props.size_defaults.column_width
        self.height = props.size_defaults.tall_cabinet_height
        self.depth = props.size_defaults.tall_cabinet_depth
        
class PRODUCT_Tall_Angled_Column_Right(Angled_Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props()
        self.product_type = 'TALL'
        self.category_name = "Angled Columns"
        self.assembly_name = "Tall Angled Column Right"
        self.detail_piece = props.column_style
        self.orientation = 'RIGHT'
        self.detail_type = 'C'
        self.width = props.size_defaults.column_width
        self.height = props.size_defaults.tall_cabinet_height
        self.depth = props.size_defaults.tall_cabinet_depth        
        
class PRODUCT_Upper_Angled_Column_Left(Angled_Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props()
        self.product_type = 'UPPER'
        self.category_name = "Angled Columns"
        self.assembly_name = "Upper Angled Column Left"
        self.detail_piece = props.column_style
        self.orientation = 'LEFT'
        self.detail_type = 'C'
        self.width = props.size_defaults.column_width
        self.height = props.size_defaults.upper_cabinet_height
        self.depth = props.size_defaults.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.size_defaults.height_above_floor
        
class PRODUCT_Upper_Angled_Column_Right(Angled_Column):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props()
        self.product_type = 'UPPER'
        self.category_name = "Angled Columns"
        self.assembly_name = "Upper Angled Column Right"
        self.detail_piece = props.column_style
        self.orientation = 'RIGHT'
        self.detail_type = 'C'
        self.width = props.size_defaults.column_width
        self.height = props.size_defaults.upper_cabinet_height
        self.depth = props.size_defaults.upper_cabinet_depth
        self.mirror_z = True
        self.height_above_floor = props.size_defaults.height_above_floor  
        