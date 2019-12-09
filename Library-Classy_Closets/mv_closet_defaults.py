import bpy
import os
import math
from mv import fd_types, utils, unit
from bpy.app.handlers import persistent
from bpy.types import PropertyGroup, UIList, Panel, Operator
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)
from . import common_lists
import snap_db
from snap_db import property_groups
import csv

#---------COMMON FOLDER NAMES
""" 
Folder Names where data is located in
"""
CROWN_MOLDING_FOLDER_NAME = "Crown Molding Profiles"
BASE_MOLDING_FOLDER_NAME = "Base Molding Profiles"
DOOR_FOLDER_NAME = "Door Panels"
ROD_FOLDER_NAME = "Hanging Rods"
PULL_FOLDER_NAME = "Door Pulls"
HINGE_FOLDER_NAME = "Hinges"
SLIDE_FOLDER_NAME = "Slides"
SLIDE_DT_FOLDER_NAME = "Dovetail Slides"
DRAWER_FOLDER_NAME = "Drawers"
ACCESSORY_FOLDER_NAME = "Accessories"
MATERIAL_LIBRARY_NAME = "Cabinet Materials"
CORE_CATEGORY_NAME = "Wood Core"

enum_items_slide = []
enum_items_rod_cups = []

def update_render_materials(self, context):
    try:
        bpy.ops.db_materials.poll_assign_materials()
    except:
        pass

def update_back_mat_pointer(self, context):
    back_mesh = context.object
    back_bp = back_mesh.parent

    if back_bp.lm_closets.use_unique_material:
        back_mesh.cabinetlib.material_slots[0].pointer_name = ""
    else:
        back_mesh.cabinetlib.material_slots[0].pointer_name = "Closet_Part_Surfaces"

#---------LIBRARY NAMESPACE
LIBRARY_NAME_SPACE = "lm_closets"

def get_scene_props():
    """ 
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("bpy.context.scene." + LIBRARY_NAME_SPACE)
    return props

def get_object_props(obj):
    """ 
    This is a function to get access to all of the object properties that are registered in this library
    Arg1: obj - object to retrieve data from
    """
    props = eval("obj." + LIBRARY_NAME_SPACE)
    return props

#---------DICTIONARY DYNAMIC ENUM PROPERTIES
""" 
Dynamic Enum Properties
Used to dynamically retrieve files from harddrive and display in comboboxes
"""
preview_collections = {}   
preview_collections["base_moldings_categories"] = utils.create_image_preview_collection()
preview_collections["base_moldings"] = utils.create_image_preview_collection()
preview_collections["crown_moldings_categories"] = utils.create_image_preview_collection()   
preview_collections["crown_moldings"] = utils.create_image_preview_collection()   
preview_collections["door_style_categories"] = utils.create_image_preview_collection()  
preview_collections["door_styles"] = utils.create_image_preview_collection() 
preview_collections["pull_categories"] = utils.create_image_preview_collection() 
preview_collections["rods"] = utils.create_image_preview_collection()  
preview_collections["pulls"] = utils.create_image_preview_collection() 
preview_collections["hinges"] = utils.create_image_preview_collection()
preview_collections["drawers"] = utils.create_image_preview_collection()
preview_collections["melamine_slides"] = utils.create_image_preview_collection()
preview_collections["dovetail_slides"] = utils.create_image_preview_collection()
preview_collections["accessory_categories"] = utils.create_image_preview_collection() 
preview_collections["accessories"] = utils.create_image_preview_collection() 
preview_collections["material_categories"] = utils.create_image_preview_collection()  
preview_collections["materials"] = utils.create_image_preview_collection()  

#---------BASE MOLDING DYNAMIC ENUMS
def enum_base_molding_categories(self,context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__),BASE_MOLDING_FOLDER_NAME)
    pcoll = preview_collections["base_moldings_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_base_molding(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),BASE_MOLDING_FOLDER_NAME,self.base_molding_category)
    pcoll = preview_collections["base_moldings"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_base_molding_category(self,context):
    if preview_collections["base_moldings"]:
        bpy.utils.previews.remove(preview_collections["base_moldings"])
        preview_collections["base_moldings"] = utils.create_image_preview_collection()     
        
    enum_base_molding(self,context)

#---------CROWN MOLDING DYNAMIC ENUMS
def enum_crown_molding_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),CROWN_MOLDING_FOLDER_NAME)
    pcoll = preview_collections["crown_moldings_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_crown_molding(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),CROWN_MOLDING_FOLDER_NAME,self.crown_molding_category)
    pcoll = preview_collections["crown_moldings"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_crown_molding_category(self,context):
    if preview_collections["crown_moldings"]:
        bpy.utils.previews.remove(preview_collections["crown_moldings"])
        preview_collections["crown_moldings"] = utils.create_image_preview_collection()     
        
    enum_crown_molding(self,context)
    
#---------DOORS DYNAMIC ENUMS
def enum_door_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),DOOR_FOLDER_NAME)
    pcoll = preview_collections["door_style_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_door_styles(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),DOOR_FOLDER_NAME,self.door_category)
    pcoll = preview_collections["door_styles"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_door_category(self,context):
    if preview_collections["door_styles"]:
        bpy.utils.previews.remove(preview_collections["door_styles"])
        preview_collections["door_styles"] = utils.create_image_preview_collection()     
        
    enum_door_styles(self,context)    


#---------RODS DYNAMIC ENUMS

def part_is_not_hidden(part):
    ''' Returns bool
        Determines if part assembly is hidden
    '''    
    hide = part.get_prompt("Hide")
    if hide:
        if hide.value():
            return False
        else:
            return True
    else:
        return True
    
def scene_parts(context):
    ''' Generator that Returns a List of all of the assemblies in the Scene
    '''    
    for obj in bpy.context.scene.objects:
        if obj.mv.type == 'BPASSEMBLY':
            part = fd_types.Part(obj)
            if part_is_not_hidden(part):
                yield part   
                
def enum_rods(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),ROD_FOLDER_NAME)
    pcoll = preview_collections["rods"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_rods(self,context):
    for spec_group in context.scene.mv.spec_groups:    
        rod_finish = spec_group.materials["Rod_Finish"]
        rod_finish.library_name = "Cabinet Materials"
        rod_finish.category_name = "Metals"
        
        if 'Aluminum' in self.rods_name:
            rod_finish.item_name = "Matte Aluminum"
        if 'Matte Brass' in self.rods_name:
            rod_finish.item_name = "Matte Brass"  
        if 'Matte Nickel' in self.rods_name:
            rod_finish.item_name = "Matte Nickel"                          
        if 'Bronze' in self.rods_name:
            rod_finish.item_name = "Oil Rubbed Bronze"  
        if 'Polished Brass' in self.rods_name:
            rod_finish.item_name = "Polished Brass"  
        if 'Chrome' in self.rods_name:
            rod_finish.item_name = "Polished Chrome"              
    
    for assembly in scene_parts(context):
        props = get_object_props(assembly.obj_bp)
        if props.is_hanging_rod:
            if 'Round' in self.rods_name:
                group_bp = utils.get_group(os.path.join(os.path.dirname(__file__),
                                                     "Closet Assemblies",
                                                     "Hang Rod Round.blend"))    
            else:
                group_bp = utils.get_group(os.path.join(os.path.dirname(__file__),
                                                     "Closet Assemblies",
                                                     "Hang Rod Oval.blend"))   
            new_rod = fd_types.Assembly(group_bp)
            
            new_rod.obj_bp.parent = assembly.obj_bp.parent
            new_rod.obj_bp.location = assembly.obj_bp.location
            new_rod.obj_bp.rotation_euler = assembly.obj_bp.rotation_euler
            utils.copy_drivers(assembly.obj_bp,new_rod.obj_bp)
            utils.copy_prompt_drivers(assembly.obj_bp,new_rod.obj_bp)
            utils.copy_drivers(assembly.obj_x,new_rod.obj_x)
            utils.copy_drivers(assembly.obj_y,new_rod.obj_y)
            utils.copy_drivers(assembly.obj_z,new_rod.obj_z)
            utils.delete_obj_list(utils.get_child_objects(assembly.obj_bp))
            
            closet_options = bpy.context.scene.lm_closets.closet_options
            new_rod.obj_bp.mv.name_object = closet_options.rods_name
            new_props = get_object_props(new_rod.obj_bp)
            new_props.is_hanging_rod = True
            
            for child in new_rod.obj_bp.children:
                if child.type == 'EMPTY':
                    child.hide = True

                if child.type == 'MESH':
                    child.draw_type = 'TEXTURED'
                    utils.assign_materials_from_pointers(child)
                    for mat in child.cabinetlib.material_slots:
                        mat.pointer_name = "Rod_Finish"
                        
    bpy.ops.cabinetlib.update_scene_from_pointers()
    
#---------PULLS DYNAMIC ENUMS
def enum_pull_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),PULL_FOLDER_NAME)
    pcoll = preview_collections["pull_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_pulls(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),PULL_FOLDER_NAME,self.pull_category)
    pcoll = preview_collections["pulls"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_pulls(self,context):
    for spec_group in context.scene.mv.spec_groups:    
        pull_finish = spec_group.materials["Pull_Finish"]
        pull_finish.library_name = "Cabinet Materials"
        pull_finish.category_name = "Metals"
         
        if 'Staineless' in self.pull_category:
            pull_finish.item_name = "Stainless Steel"
        if 'Nickel' in self.pull_category:
            pull_finish.item_name = "Satin Nickel"  
        if 'Matte Nickel' in self.pull_category:
            pull_finish.item_name = "Matte Nickel"                          
        if 'Bronze' in self.pull_category:
            pull_finish.item_name = "Oil Rubbed Bronze" 
        if 'Chrome' in self.pull_category:
            pull_finish.item_name = "Polished Chrome"
        if 'Matte Chrome' in self.pull_category:
            pull_finish.item_name = "Matte Chrome"  
        if 'Black' in self.pull_category:
            pull_finish.item_name = "Black Anodized Metal"  
        if 'Matte Black' in self.pull_category:
            pull_finish.item_name = "Cast Iron" 
            
    bpy.ops.cabinetlib.update_scene_from_pointers()            

def update_pull_category(self,context):
    if preview_collections["pulls"]:
        bpy.utils.previews.remove(preview_collections["pulls"])
        preview_collections["pulls"] = utils.create_image_preview_collection()     
        
    enum_pulls(self,context)    
    
#---------HINGES DYNAMIC ENUMS
def enum_hinges(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),HINGE_FOLDER_NAME)
    pcoll = preview_collections["hinges"]
    return utils.get_image_enum_previews(icon_dir,pcoll)
    
def update_hinge(self,context):
    for obj in context.scene.objects:
        props = get_object_props(obj)
        if props.is_hinge:
            obj.mv.name_object = self.hinge_name
            utils.set_object_name(obj)
    
#---------DRAWER DYNAMIC ENUMS
def enum_drawer(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),DRAWER_FOLDER_NAME)
    pcoll = preview_collections["drawers"]
    return utils.get_image_enum_previews(icon_dir,pcoll)
    
def update_drawer(self,context):
    pass
    
#---------SLIDES DYNAMIC ENUMS
def enum_dt_slides(self,context):
    if context is None:
        return []    
    
    icon_dir = os.path.join(os.path.dirname(__file__),SLIDE_DT_FOLDER_NAME)
    pcoll = preview_collections["dovetail_slides"]
    return utils.get_image_enum_previews(icon_dir,pcoll)
       
def enum_mel_slides(self,context):
    if context is None:
        return []    
    
    icon_dir = os.path.join(os.path.dirname(__file__),SLIDE_FOLDER_NAME)
    pcoll = preview_collections["melamine_slides"]
    return utils.get_image_enum_previews(icon_dir,pcoll)        

# def enum_slides(self,context):
#     if context is None:
#         return []

#     if len(enum_items_slide) > 1:
#         return enum_items_slide
    
#     else:
#         with open(snap_db.SLIDE_TYPES_CSV_PATH) as slides_file:
#             reader = csv.reader(slides_file, delimiter=',')
#             next(reader)

#             for row in reader:
#                 enum_items_slide.append((row[0], row[1], row[2]))

#         return enum_items_slide

#---------POLE CUP DYNAMIC ENUMS
def enum_rod_cups(self,context):
    if context is None:
        return []

    if len(enum_items_rod_cups) > 1:
        return enum_items_rod_cups
    
    else:
        conn = snap_db.connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT\
                *\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE '{}'\
            ;".format("%" + "pole cup" + "%")
        )

        rows = cursor.fetchall()

        for row in rows:
            enum_items_rod_cups.append((row[0], row[2], row[2]))
        
        conn.close()

        return enum_items_rod_cups                        
    
#---------ACCESSORIES DYNAMIC ENUMS
def enum_accessories_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),ACCESSORY_FOLDER_NAME)
    pcoll = preview_collections["accessory_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_accessories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),ACCESSORY_FOLDER_NAME,self.accessory_category)
    pcoll = preview_collections["accessories"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_accessories_category(self,context):
    if preview_collections["accessories"]:
        bpy.utils.previews.remove(preview_collections["accessories"])
        preview_collections["accessories"] = utils.create_image_preview_collection()     
        
    enum_accessories(self,context)        
    
#---------MATERIALS DYNAMIC ENUMS
def enum_material_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME)
    pcoll = preview_collections["material_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_materials(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME,self.material_category)
    pcoll = preview_collections["materials"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_material_category(self,context):
    if preview_collections["materials"]:
        bpy.utils.previews.remove(preview_collections["materials"])
        preview_collections["materials"] = utils.create_image_preview_collection()     
        
    enum_materials(self,context)

def available_material_colors(self,context):
    scene_props = bpy.context.scene.db_materials    
    mat_type = scene_props.materials.get_mat_type()

    if mat_type.name == "Melamine":
        items = scene_props.materials.mel_color_list

    if mat_type.name == "Textured Melamine":
        items = scene_props.materials.textured_mel_color_list

    if context is None:
        return []
    
    return items
    
#---------PROPERTY GROUPS
    
class Closet_Defaults(PropertyGroup):

    defaults_tabs = EnumProperty(name="Defaults Tabs",
                       items=[('SIZE',"Size",'Show the default size options'),
                              ('CONSTRUCTION',"Construction",'Show the default construction'),
                              ('TOOLS',"Tools",'Show the Tools')],
                       default = 'SIZE')

    export_subassemblies = BoolProperty(name="Export Subassemblies",description="Export Subassemblies",default=True)   
    
    add_backing = BoolProperty(name="Add Backing",description="Add Backing",default=False)      
    
    dog_ear_each = BoolProperty(name="Dog Ear Each",description="Dog Ear Each Partition",default=False)
    
    add_hanging_rail = BoolProperty(name="Add Hanging Rail",description="Add Hanging Rail",default=False)   
    
    add_top_cleat = BoolProperty(name="Add Top Cleat",description="Add Top Cleat",default=True)  
    
    add_bottom_cleat = BoolProperty(name="Add Bottom Cleat",description="Add Bottom Cleat",default=True)  
    
    add_mid_cleat = BoolProperty(name="Add Mid Rail",description="Add Mid Cleat",default=False)
    
    height_to_add_mid_cleat = FloatProperty(name="Height to Add Mid Cleat",default=unit.inch(59),unit='LENGTH')
    
    hanging_rail_distance_from_top = FloatProperty(name="Hanging Rail Distance From Top",default=unit.millimeter(8),unit='LENGTH')
    
    panel_depth = FloatProperty(name="Default Panel Depth",default=unit.inch(12),unit='LENGTH')
    
    hanging_height = FloatProperty(name="Hanging Height",default=unit.millimeter(2131),unit='LENGTH')
    
    panel_height = EnumProperty(name="Default Panel Height",items=common_lists.PANEL_HEIGHTS,default='2035')
    
    stacked_panel_height = EnumProperty(name="Stacked Panel Height",items=common_lists.PANEL_HEIGHTS,default='787')
    
    island_panel_height = EnumProperty(name="Default Island Panel Height",items=common_lists.PANEL_HEIGHTS,default='915')    
    
    hanging_panel_height = EnumProperty(name="Default Hanging Panel Height",items=common_lists.PANEL_HEIGHTS,default='1203')
    
    angle_top_front_panel_height = FloatProperty(name="Angle Top Front Panel Height",default=0,unit='LENGTH')
    
    angle_top_front_panel_depth = FloatProperty(name="Angle Top Front Panel Depth",default=0,unit='LENGTH')
    
    angle_top_rear_panel_height = FloatProperty(name="Angle Top Rear Panel Height",default=0,unit='LENGTH')
    
    angle_top_rear_panel_depth = FloatProperty(name="Angle Top Rear Panel Depth",default=0,unit='LENGTH')    
    
    rear_notch_height_1 = FloatProperty(name="Rear Notch Height 1",default=0,unit='LENGTH')  
    
    rear_notch_height_2 = FloatProperty(name="Rear Notch Height 2",default=0,unit='LENGTH')  
    
    rear_notch_depth_1 = FloatProperty(name="Rear Notch Depth 1",default=0,unit='LENGTH')  
    
    rear_notch_depth_2 = FloatProperty(name="Rear Notch Depth 2",default=0,unit='LENGTH')      
    
    shelf_lip_width = FloatProperty(name="Shelf Lip Width",default=unit.inch(1.5),unit='LENGTH')
    
    toe_kick_height = FloatProperty(name="Toe Kick Height",default=unit.inch(2.5),unit='LENGTH')
    
    toe_kick_setback = FloatProperty(name="Toe Kick Setback",default=unit.inch(1.125),unit='LENGTH')
    
    adj_shelf_clip_gap = FloatProperty(name="Adjustable Shelf Clip Gap",default=0,unit='LENGTH')
    
    adj_shelf_setback = FloatProperty(name="Adjustable Shelf Setback",default=unit.inch(.25),unit='LENGTH')
    
    locked_shelf_setback = FloatProperty(name="Locked Shelf Setback",default=unit.inch(0),unit='LENGTH')
    
    double_door_auto_switch = FloatProperty(name="Double Door Auto Switch",description="The opening width that door inserts should automatically switch to double doors",default=unit.inch(24),unit='LENGTH')
    
    inset_front = BoolProperty(name="Double Door Auto Switch",description="Set Inset Front to be used by default",default=False)    
    
    no_pulls = BoolProperty(name="No Pulls",description="Dont add pulls by default",default=False)  
    
    use_buyout_drawers = BoolProperty(name="Use Buyout Drawers",description="This will use buyout drawers. This will draw the drawer inserts faster",default=False)  
    
    hide_hangers = BoolProperty(name="Hide Hangers",
                                    description="Check this box to hide the models for the hangers",
                                    default=False)
    
    use_plant_on_top = BoolProperty(name="Use Plant On Top",
                                    description="Check this box to place the top above the panels. Otherwise it will place them between the sides.",
                                    default=False)
    
    use_32mm_system = BoolProperty(name="Use 32mm System",
                                    description="Check this box to use the 32mm system. This will limit the size of panels, openings, drawer fronts to ensure they are always work with the 32mm System.",
                                    default=True)
    
    show_panel_drilling = BoolProperty(name="Show Panel Drilling",
                                    description="Check this box to see the drilling operation on the panels",
                                    default=False)
    
    panel_drilling_from_front = FloatProperty(name="Panel Drilling from Front",
                                              description="This sets the dim to the front set of system holes for the visual representation ONLY. See Machining Setup Interface for machining defaults",
                                              default=unit.inch(1.69291),unit='LENGTH')  
    
    panel_drilling_from_rear = FloatProperty(name="Panel Drilling from Rear",
                                             description="This sets the dim to the rear set of system holes for the visual representation ONLY. See Machining Setup Interface for machining defaults",
                                             default=unit.inch(1.69291),unit='LENGTH') 
    
    remove_bottom_hanging_shelf = BoolProperty(name="Remove Bottom Hanging Shelf",
                                               description="This will remove the bottom hanging shelf if the section is set to hanging",
                                               default=False)
    
    remove_top_shelf = BoolProperty(name="Remove Top Shelf",
                                    description="This will remove the top shelf if the section is set to hanging",
                                    default=False)
    
    drawer_bottom_dado_depth = FloatProperty(name="Drawer Bottom Dado Depth",
                                             description="This sets the dado depth for drawer bottoms. Set to 0 for no dado",
                                             default=unit.inch(.25),unit='LENGTH')     
    
    drawer_bottom_z_location = FloatProperty(name="Drawer Bottom Z Location",
                                             description="This sets the distance from the bottom of the drawer box to the bottom of the drawer bottom",
                                             default=unit.inch(.5),unit='LENGTH')         
    
    drawer_box_rear_gap = FloatProperty(name="Drawer Box Rear Gap",
                                             description="This sets the drawer box rear gap",
                                             default=unit.inch(2),unit='LENGTH')           
    
    drawer_box_bottom_gap = FloatProperty(name="Drawer Box Bottom Gap",
                                             description="This sets the drawer box distance from the bottom of the drawer front to the bottom of the drawer box",
                                             default=unit.inch(1.2),unit='LENGTH')        
    
    drawer_box_top_gap = FloatProperty(name="Drawer Box Top Gap",
                                             description="This sets the drawer box distance from the top of the drawer front to the top of the drawer box",
                                             default=unit.inch(1),unit='LENGTH')     
    
    drawer_box_slide_gap = FloatProperty(name="Drawer Box Slide Gap",
                                             description="This sets the drawer box slide gap",
                                             default=unit.inch(1),unit='LENGTH')  
    
    def draw_door_defaults(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Double Door Auto Switch:")
        row.prop(self,'double_door_auto_switch',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Double Door Auto Switch'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.double_door_auto_switch
        
        row = box.row()
        row.label("Inset Fronts:")
        row.prop(self,'inset_front',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Inset Front'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.inset_front
        
    def draw_pull_defaults(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("No Pulls:")
        row.prop(self,'no_pulls',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'No Pulls'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.no_pulls
        
    def draw_size_defaults(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Default Closet Sizes:",icon='ARROW_LEFTRIGHT')        
        
        row = box.row()
        row.label("Default Hang Height:")
        row.prop(self,'hanging_height',text="")    
        row.operator(LIBRARY_NAME_SPACE + ".update_closet_hanging_height",text="",icon='FILE_REFRESH')

#         row = box.row()
#         row.label("Floor Panel Height:")
#         row.prop(self,'panel_height',text="")
#         row.operator(LIBRARY_NAME_SPACE + ".update_closet_section_height",text="",icon='FILE_REFRESH').update_hanging = False

        row = box.row()
        row.label("Default Panel Height:")
        row.prop(self,'hanging_panel_height',text="")
        row.operator(LIBRARY_NAME_SPACE + ".update_closet_section_height",text="",icon='FILE_REFRESH').update_hanging = True
        
        row = box.row()
        row.label("Default Upper Panel Height:")
        row.prop(self,'stacked_panel_height',text="")
        row.operator(LIBRARY_NAME_SPACE + ".update_closet_section_height",text="",icon='FILE_REFRESH').update_hanging = False        
        
        row = box.row()
        row.label("Default Panel Depth:")
        row.prop(self,'panel_depth',text="")
        row.label(text="",icon='BLANK1')
        
        row = box.row()
        row.label("Toe Kick Height:")
        row.prop(self,'toe_kick_height',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Toe Kick Height'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.toe_kick_height        
        
        row = box.row()
        row.label("Toe Kick Setback:")
        row.prop(self,'toe_kick_setback',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Toe Kick Setback'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.toe_kick_setback 
        
    def draw_construction_defaults(self,layout):
        main_col = layout.column(align=True)
        
        box = main_col.box()
        box.label("General Construction Options:",icon='MODIFIER')          
        
    #GENERAL
        
        row = box.row()
        row.label("Show Panel Drilling:")
        row.prop(self,'show_panel_drilling',text="")
        row.label(text="",icon='BLANK1')        
        
        row = box.row()
        row.label("Hide Hangers:")
        row.prop(self,'hide_hangers',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Turn Off Hangers'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.hide_hangers         
              
#         row = box.row()
#         row.label("Use 32mm System:")
#         row.prop(self,'use_32mm_system',text="")  
#         row.label(text="",icon='BLANK1')        
         
#         row = box.row()
#         row.label("Visual Drilling From Front:")
#         row.prop(self,'panel_drilling_from_front',text="")
#         props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Drilling Distance From Front'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.panel_drilling_from_front
         
#         row = box.row()
#         row.label("Visual Drilling From Rear:")
#         row.prop(self,'panel_drilling_from_rear',text="")
#         props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Drilling Distance From Rear'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.panel_drilling_from_rear   
 
#         row = box.row()
#         row.label("Use Plant On Top:")
#         row.prop(self,'use_plant_on_top',text="")
#         row.label(text="",icon='BLANK1')

    #SHELF OPTIONS
        box = main_col.box()
        box.label("Section Options:",icon='MODIFIER')   
        
        row = box.row()
        row.label("Add Backing:")
        row.prop(self,'add_backing',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Add Backing'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.add_backing        
        
#         row = box.row()
#         row.label("Remove Bottom Hanging Shelf:")
#         row.prop(self,'remove_bottom_hanging_shelf',text="")
#         props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         props.prompt_name = 'Remove Bottom Hanging Shelf'
#         props.prompt_type = 'CHECKBOX'
#         props.bool_value = self.remove_bottom_hanging_shelf
#          
#         row = box.row()
#         row.label("Remove Top Shelf:")
#         row.prop(self,'remove_top_shelf',text="")
#         props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         props.prompt_name = 'Remove Top Shelf'
#         props.prompt_type = 'CHECKBOX'
#         props.bool_value = self.remove_top_shelf    
#         
#         #row = box.row()
#         #row.label("Shelf Lip Width:")
#         #row.prop(self,'shelf_lip_width',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Shelf Lip Width'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.shelf_lip_width            
#         
        row = box.row()
        row.label("Adjustable Shelf Clip Gap:")
        row.prop(self,'adj_shelf_clip_gap',text="")
        props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Adj Shelf Clip Gap'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.adj_shelf_clip_gap        
#         
#         #row = box.row()
#         #row.label("Adjustable Shelf Setback:")
#         #row.prop(self,'adj_shelf_setback',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Adj Shelf Setback'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.adj_shelf_setback                
#         
#         #row = box.row()
#         #row.label("Locked Shelf Setback:")
#         #row.prop(self,'locked_shelf_setback',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Locked Shelf Setback'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.locked_shelf_setback        
        
#         #CLEAT AND BACK OPTIONS
#         #box = main_col.box()
#         #box.label("Cleat and Back Options:",icon='MODIFIER')           
#         #row = box.row()
#         #row.label("Add Cleats:")
#         #row.prop(self,'add_top_cleat',text="Top")
#         #row.prop(self,'add_mid_cleat',text="Mid")
#         #row.prop(self,'add_bottom_cleat',text="Bottom")
#         #row.label(text="",icon='BLANK1')
#         
#         #row = box.row()
#         #row.label("Height To Add Mid Cleat:")
#         #row.prop(self,'height_to_add_mid_cleat',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Height To Add Mid Cleat'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.height_to_add_mid_cleat
#         
#         #HANGING OPTIONS
#         #row = box.row()
#         #row.label("Add Hanging Rail:")
#         #row.prop(self,'add_hanging_rail',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Add Hanging Rail'
#         #props.prompt_type = 'CHECKBOX'
#         #props.bool_value = self.add_hanging_rail        
#         
#         #row = box.row()
#         #row.label("Hanging Rail Distance From Top:")
#         #row.prop(self,'hanging_rail_distance_from_top',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Hanging Rail Distance From Top'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.hanging_rail_distance_from_top

        #DRAWER OPTIONS
#         box = main_col.box()
#         box.label("Drawer Options:",icon='MODIFIER')           
#         row = box.row()
#         row.label("Use Dovetail Drawers:")
#         row.prop(self,'use_buyout_drawers',text="")
#         row.label(text="",icon='BLANK1')
# 
#         #row = box.row()
#         #row.label("Drawer Box Bottom Gap:")
#         #row.prop(self,'drawer_box_bottom_gap',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Drawer Box Bottom Gap'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.drawer_box_bottom_gap  
# 
#         #row = box.row()
#         #row.label("Drawer Box Top Gap:")
#         #row.prop(self,'drawer_box_top_gap',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Drawer Box Top Gap'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.drawer_box_top_gap  
#         
#         #row = box.row()
#         #row.label("Drawer Box Rear Gap:")
#         #row.prop(self,'drawer_box_rear_gap',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Drawer Box Rear Gap'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.drawer_box_rear_gap          
#         
#         #row = box.row()
#         #row.label("Drawer Box Slide Gap:")
#         #row.prop(self,'drawer_box_slide_gap',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Drawer Box Slide Gap'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.drawer_box_slide_gap            
#         
#         #row = box.row()
#         #row.label("Drawer Box Dado Depth:")
#         #row.prop(self,'drawer_bottom_dado_depth',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Drawer Box Bottom Dado Depth'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.drawer_bottom_dado_depth            
#         
#         #row = box.row()
#         #row.label("Drawer Bottom Z Location:")
#         #row.prop(self,'drawer_bottom_z_location',text="")
#         #props = row.operator('fd_prompts.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
#         #props.prompt_name = 'Drawer Bottom Z Location'
#         #props.prompt_type = 'DISTANCE'
#         #props.float_value = self.drawer_bottom_z_location  
        
    #PANEL ROUTING
        box = main_col.box()
        box.label("Dog Eared Partitions:",icon='MODIFIER')          
        row = box.row(align=True)
        row.label("Angle Top Front:")
        row.prop(self,'angle_top_front_panel_height',text="Height")  
        row.prop(self,'angle_top_front_panel_depth',text="Depth")  
        row.label(text="",icon='BLANK1')   
        
        row = box.row(align=True)
        row.label("Angle Top Rear:")
        row.prop(self,'angle_top_rear_panel_height',text="Height")  
        row.prop(self,'angle_top_rear_panel_depth',text="Depth")  
        row.label(text="",icon='BLANK1')           
        
        #row = box.row(align=True)
        #row.label("Base Notch 1:")
        #row.prop(self,'rear_notch_height_1',text="Height")  
        #row.prop(self,'rear_notch_depth_1',text="Depth")  
        #row.label(text="",icon='BLANK1')            
        
        #row = box.row(align=True)
        #row.label("Base Notch 2:")
        #row.prop(self,'rear_notch_height_2',text="Height")  
        #row.prop(self,'rear_notch_depth_2',text="Depth")  
        #row.label(text="",icon='BLANK1')                   
        
    def draw(self,layout):
        box = layout.box()
        row = box.row()
        row.prop(self,'defaults_tabs',expand=True)
        
        if self.defaults_tabs == 'SIZE':
            self.draw_size_defaults(box)
            
        if self.defaults_tabs == 'CONSTRUCTION':
            self.draw_construction_defaults(box)
            
        if self.defaults_tabs == 'TOOLS':
            tool_box = box.box()
            tool_box.label("Closet Tools:",icon='SCULPTMODE_HLT')
            tool_box.operator(LIBRARY_NAME_SPACE + '.combine_parts',icon='UV_ISLANDSEL')               
        
class Closet_Options(PropertyGroup):
    
    hardware_tabs = EnumProperty(name="Hardware Tabs",
                                 items=[('RODS',"Rods",'Show the rod options'),
                                        ('PULLS',"Pulls",'Show the pull options'),
                                        ('HINGES',"Hinges",'Show the hinge options'),
                                        ('DRAWERS',"Drawer Slides",'Show the drawer options')],
                                 default = 'RODS')
    
    base_molding_category = bpy.props.EnumProperty(name="Base Molding Category",items=enum_base_molding_categories,update=update_base_molding_category)
    base_molding = bpy.props.EnumProperty(name="Base Molding",items=enum_base_molding)
    
    crown_molding_category = bpy.props.EnumProperty(name="Crown Molding Category",items=enum_crown_molding_categories,update=update_crown_molding_category)
    crown_molding = bpy.props.EnumProperty(name="Crown Molding",items=enum_crown_molding)
    
    door_category = bpy.props.EnumProperty(name="Door Category",items=enum_door_categories,update=update_door_category)
    door_style = bpy.props.EnumProperty(name="Door Style",items=enum_door_styles)
    
    material_category = bpy.props.EnumProperty(name="Material Category",items=enum_material_categories,update=update_material_category)
    material = bpy.props.EnumProperty(name="Material",items=enum_materials)     

    rods_name = bpy.props.EnumProperty(name="Rod Name",items=enum_rods,update=update_rods)
    
    pull_category = bpy.props.EnumProperty(name="Pull Category",items=enum_pull_categories,update=update_pull_category)
    pull_name = bpy.props.EnumProperty(name="Pull Name",items=enum_pulls,update=update_pulls)
    
    hinge_name = bpy.props.EnumProperty(name="Hinge Name",items=enum_hinges,update=update_hinge)    
    
    drawer_name = bpy.props.EnumProperty(name="Drawer Name",items=enum_drawer,update=update_drawer)  
    
    box_type = EnumProperty(name="Drawer Box Type",
                                 items=[('MEL',"Melamine Drawer Box",'Show the slide options'),
                                        ('DOVE',"Dovetail Drawer Box",'Show the slide options')],
                                 default = 'MEL')    
    
    dt_slide_name = bpy.props.EnumProperty(name="Dove Tail Slide Name",items=enum_dt_slides)    
    mel_slide_name = bpy.props.EnumProperty(name="Melamine Slide Name",items=enum_mel_slides)

    pole_cup_name = bpy.props.EnumProperty(name="Pole Cup Name",items=enum_rod_cups)
    
    accessory_category = bpy.props.EnumProperty(name="Accessory Category",items=enum_accessories_categories,update=update_accessories_category)
    accessory_name = bpy.props.EnumProperty(name="Accessory Name",items=enum_accessories)    
    
    def draw_molding_options(self,layout):
        molding_box = layout.box()
        row = molding_box.row(align=True)
        row.label("Moldings Options:")
        row.operator(LIBRARY_NAME_SPACE + '.auto_add_molding',text="Add Crown",icon='ZOOMIN').molding_type = 'Crown'
        row.operator(LIBRARY_NAME_SPACE + '.auto_add_molding',text="Add Base",icon='ZOOMIN').molding_type = 'Base'

        col = molding_box.column(align=True)
        row = col.row()
        row.label("Crown Molding:")
        row.operator(LIBRARY_NAME_SPACE + '.delete_molding',text="",icon='X').molding_type = 'Crown'
        col.prop(self,'crown_molding_category',text="",icon='FILE_FOLDER')
        col.template_icon_view(self,"crown_molding",show_labels=True)        
        
        col = molding_box.column(align=True)
        row = col.row()
        row.label("Base Molding:")
        row.operator(LIBRARY_NAME_SPACE + '.delete_molding',text="",icon='X').molding_type = 'Base'
        col.prop(self,'base_molding_category',text="",icon='FILE_FOLDER')
        col.template_icon_view(self,"base_molding",show_labels=True)   
    
    def draw_door_options(self,layout):
        door_style_box = layout.box()
        
        row = door_style_box.row(align=True)
        row.label("Door/Drawer Options:")
        row.operator(LIBRARY_NAME_SPACE + '.update_door_selection',text="Replace Selection",icon='FILE_REFRESH')
        row.operator(LIBRARY_NAME_SPACE + '.place_applied_panel',text="Place Door",icon='MAN_TRANS')   
        col = door_style_box.column(align=True)
        col.prop(self,'door_category',text="",icon='FILE_FOLDER')
        col.template_icon_view(self,"door_style",show_labels=True)    
        
        props = get_scene_props()
        props.closet_defaults.draw_door_defaults(door_style_box)
    
    #def draw_material_options(self,layout):
        #materials = []
        #materials.append("Closet_Part_Surfaces")
        #materials.append("Closet_Part_Edges")
        #materials.append("Door_Surface")
        #materials.append("Door_Edge")
        #materials.append("Countertop_Surface")
        #materials.append("Drawer_Box_Surface")
        #materials.append("Drawer_Box_Edge")
        #materials.append("Pull_Finish")
        #materials.append("Rod_Finish")
        #materials.append("Wire_Basket")
        #materials.append("Glass")
        #materials.append("Molding")
        #materials.append("Lucite")
        
        library = bpy.context.scene.mv
        sg = library.spec_groups[library.spec_group_index]           
        
        #material_box = layout.box()
        #row = material_box.row()
        #row.label("Material Selection:")
        #row.operator('cabinetlib.update_scene_from_pointers',text="Update Materials",icon='FILE_REFRESH')
        
        #col = material_box.column(align=True)
        #col.prop(self,'material_category',text="",icon='FILE_FOLDER')
        #col.template_icon_view(self,"material",show_labels=True)        
        
        #col = material_box.column(align=True)
        
        #for mat in materials:
            #Pointer = sg.materials[mat]

            #row = col.row()
            #row.operator(LIBRARY_NAME_SPACE + '.set_pointer',text=mat.replace("_"," "),icon='MATERIAL').pointer_name = mat
            #row.label(Pointer.category_name + " - " + Pointer.item_name,icon='SCREEN_BACK')
    
    def draw_hardware_options(self,layout):
        hardware_box = layout.box()
        row = hardware_box.row()
        row.prop(self,'hardware_tabs',expand=True)
        
        if self.hardware_tabs == 'RODS':
            col = hardware_box.column(align=True)
            row = col.row(align=True)
            row.label("Rods:")
            col.template_icon_view(self,"rods_name",show_labels=True)

            col.label("Rod Cup Type:")
            col.prop(self, "pole_cup_name", text="")
                    
        
        if self.hardware_tabs == 'PULLS':
            col = hardware_box.column(align=True)
            row = col.row(align=True)
            row.label("Pull Options:")
            row.operator(LIBRARY_NAME_SPACE + '.update_pull_selection',text="Change Pull",icon='MAN_TRANS').update_all = False
            row.operator(LIBRARY_NAME_SPACE + '.update_pull_selection',text="Replace All",icon='FILE_REFRESH').update_all = True
            col.separator()
            col.prop(self,'pull_category',text="",icon='FILE_FOLDER')
            col.template_icon_view(self,"pull_name",show_labels=True)
            
            props = get_scene_props()
            props.closet_defaults.draw_pull_defaults(hardware_box)
                
        if self.hardware_tabs == 'HINGES':
            col = hardware_box.column(align=True)
            row = col.row(align=True)
            row.label("Hinges:")
            col.template_icon_view(self,"hinge_name",show_labels=True)
        
        if self.hardware_tabs == 'DRAWERS':
            col = hardware_box.column(align=True)
            row = col.row()
            row.prop(self,'box_type',expand=True)
            
            if self.box_type == 'MEL':
                row = col.row(align=True)
                row.label("Melamine Slides:")
                mat_props = bpy.context.scene.db_materials
                slide_type = mat_props.get_drawer_slide_type()
                col.menu('MENU_Drawer_Slides', text=slide_type.name, icon='SOLO_ON')


            else:
                row = col.row(align=True)
                row.label("Dovetail Slides:")
                mat_props = bpy.context.scene.db_materials
                slide_type = mat_props.get_drawer_slide_type()
                col.menu('MENU_Drawer_Slides', text=slide_type.name, icon='SOLO_ON')
                
bpy.utils.register_class(Closet_Defaults)
bpy.utils.register_class(Closet_Options)

class PROPERTIES_Scene_Variables(PropertyGroup):
    
    main_tabs = EnumProperty(name="Main Tabs",
                       items=[('DEFAULTS',"Defaults",'Show the closet defaults.'),
                              #('MATERIALS',"Materials",'Show the closet materials.'),
                              ('MOLDING',"Molding",'Show the molding options.'),
                              ('DOORS',"Wood Doors+Drawers",'Show the wood panel style options.'),
                              ('HARDWARE',"Hardware",'Show the hardware options.')],
                       default = 'DEFAULTS')
    
    closet_defaults = PointerProperty(name="Closet Info",type=Closet_Defaults)
    closet_options = PointerProperty(name="Closet Options",type=Closet_Options)
    
    def draw(self,layout):
        defaults = self.closet_defaults
        options = self.closet_options
        
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "main_tabs", 'DEFAULTS',icon='MODIFIER',  text="Closet Defaults")
        row.prop_enum(self, "main_tabs", 'HARDWARE',icon='NOCURVE', text="Hardware")
        row = col.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "main_tabs", 'DOORS',icon='MESH_PLANE', text="Wood Doors + Drawer Faces")
        row.prop_enum(self, "main_tabs", 'MOLDING',icon='IPO_CONSTANT', text="Molding")
                
#         row = box.row(align=True)
#         split = row.split(percentage=.2,align=True)
#         split.prop_enum(self, "main_tabs", 'DEFAULTS',  text="Main")
#         split = split.split(percentage=.2,align=True)
#         split.prop_enum(self, "main_tabs", 'MOLDING', text="Molding")
#         split = split.split(percentage=.4,align=True)
#         split.prop_enum(self, "main_tabs", 'DOORS', text="Wood Doors+Drawers")
#         split.prop_enum(self, "main_tabs", 'HARDWARE', text="Hardware")
#         row.prop(self,'main_tabs',expand=True)
        
        if self.main_tabs == 'DEFAULTS':
            defaults.draw(box)
            
        if self.main_tabs == 'MATERIALS':
            options.draw_material_options(box)
            
        if self.main_tabs == 'MOLDING':
            options.draw_molding_options(box)
            
        if self.main_tabs == 'DOORS':
            options.draw_door_options(box)
            
        if self.main_tabs == 'HARDWARE':
            options.draw_hardware_options(box)
    
class PROPERTIES_Object_Properties(PropertyGroup):
    
    is_temp_obj = BoolProperty(name="Is Temp Object",
                               description="Is temp object that should be removed before calculating price",
                               default=False)
    
    is_temp_hardware = BoolProperty(name="Is Temp Hardware",
                               description="Is temp hardware that is added from an operator",
                               default=False)    
    
    is_closet = BoolProperty(name="Is Closet",
                             description="Used to determine if the product is a closet",
                             default=False)
    
    is_fixed_shelf_and_rod_product_bp = BoolProperty(name="Is Fixed Shelf and Rod Product",
                             description="Used to determine if the product is a fixed shelf and rod",
                             default=False)    

    is_hutch = BoolProperty(name="Is Hutch",
                             description="Used to determine if the product is a hutch",
                             default=False)    
    
    is_island = BoolProperty(name="Is Island",
                             description="Used to determine if the product is a island",
                             default=False)        
    
    is_hamper_insert_bp = BoolProperty(name="Is Hamper Insert BP",
                                       description="Used to determine if the insert is a Hamper Insert",
                                       default=False)
    
    is_closet_top_bp = BoolProperty(name="Is Closet Top BP",
                                    description="Used to determine if the object is a closet top base point",
                                    default=False)
    
    is_crown_molding = BoolProperty(name="Is Crown Molding",
                                    description="Used to determine if the object is closet crown molding",
                                    default=False)
    
    is_base_molding = BoolProperty(name="Is Base Molding",
                                   description="Used to determine if the object is closet base molding",
                                   default=False)
    
    is_door_bp = BoolProperty(name="Is Door Base Point",
                              description="Used to determine if the assembly is a door",
                              default=False)

    is_door_insert_bp = BoolProperty(
        name="Is Door Insert Base Point",
        description="Used to determine if the assembly is a door insert",
        default=False
    )

    is_drawer_front_bp = BoolProperty(name="Is Drawer Front Base Point",
                                      description="Used to determine if the assembly is a drawer front",
                                      default=False)
    
    is_hamper_front_bp = BoolProperty(name="Is Hamper Front Base Point",
                                      description="Used to determine if the assembly is a hamper front",
                                      default=False)
    
    is_counter_top_insert_bp = BoolProperty(name="Is Countertop Insert Base Point",
                                      description="Used to determine if the assembly is a countertop insert",
                                      default=False)
    
    is_ironing_board_door_front_bp = BoolProperty(name="Is Ironing Board Door Front Base Point",
                                      description="Used to determine if the assembly is a ironing board front",
                                      default=False) 
    
    is_panel_bp = BoolProperty(name="Is Panel Point",
                               description="Used to determine if the assembly is a vertical panel",
                               default=False)    

    is_slanted_shelf_bp = BoolProperty(name="Is Slanted Shelf Base Point",
                               description="Used to determine if the assembly is a slanted shelf base point",
                               default=False)    
    
    is_sliding_shelf_bp = BoolProperty(name="Is Sliding Shelf Base Point",
                               description="Used to determine if the assembly is a sliding shelf base point",
                               default=False)
    
    is_rollout_tray_bp = BoolProperty(name="Is Rollout Tray Base Point",
                               description="Used to determine if the assembly is a rollout tray base point",
                               default=False)    
    
    is_shelf_bp = BoolProperty(name="Is Shelf Base Point",
                               description="Used to determine if the assembly is a fixed or adj shelf",
                               default=False)
    
    is_l_shelf_bp = BoolProperty(name="Is L Shelf Base Point",
                               description="Used to determine if the assembly is a l shelf base point",
                               default=False)    
    
    is_angle_shelf_bp = BoolProperty(name="Is Angle Shelf Base Point",
                               description="Used to determine if the assembly is a angle shelf base point",
                               default=False)        
    
    is_radius_shelf_bp = BoolProperty(name="Is Radius Shelf Base Point",
                               description="Used to determine if the assembly is a radius shelf base point",
                               default=False) 
    
    is_plant_on_top_bp = BoolProperty(name="Is Plant on Top Base Point",
                                      description="Used to determine if the assembly is a plant on top",
                                      default=False)
    
    is_hpl_top_bp = BoolProperty(name="Is HPL Top Base Point",
                                      description="Used to determine if the assembly is a hpl top",
                                      default=False)    
    
    is_cleat_bp = BoolProperty(name="Is Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)
    
    is_door_striker_bp = BoolProperty(name="Is Door Striker Base Point",
                               description="Used to determine if the assembly is a door striker",
                               default=False)    
    
    is_shelf_and_rod_cleat_bp = BoolProperty(name="Is Shelf and Rod Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)    
    
    is_shelf_and_rod_fe_cleat_bp = BoolProperty(name="Is Shelf and Rod Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)        
    
    is_toe_kick_bp = BoolProperty(name="Is Toe Kick Base Point",
                                  description="Used to determine if the assembly is a toe kick",
                                  default=False)
    
    is_shelf_lip_bp = BoolProperty(name="Is Shelf Lip Base Point",
                                   description="Used to determine if the assembly is a shelf lip",
                                   default=False)    
    
    is_deco_shelf_lip_bp = BoolProperty(name="Is Deco Shelf Lip Base Point",
                                   description="Used to determine if the assembly is a deco shelf lip",
                                   default=False)
    
    is_spacer_bp = BoolProperty(name="Is Spacer Base Point",
                                description="Used to determine if the assembly is a drawer spacer",
                                default=False)

    is_shelf_fence_bp = BoolProperty(name="Is Shelf Fence Base Point",
                                   description="Used to determine if the assembly is a shelf fence",
                                   default=False)
    
    is_divider_bp = BoolProperty(name="Is Divider Base Point",
                                   description="Used to determine if the assembly is a divider",
                                   default=False)
    
    is_division_bp = BoolProperty(name="Is Division Base Point",
                                  description="Used to determine if the assembly is a division",
                                  default=False)
    
    is_back_bp = BoolProperty(name="Is Back Base Point",
                              description="Used to determine if the assembly is a back",
                              default=False)
    
    is_drawer_stack_bp = BoolProperty(name="Is Drawer Stack Base Point",
                                    description="Used to determine if the assembly is a drawer stack base point",
                                    default=False)       
    
    is_drawer_box_bp = BoolProperty(name="Is Drawer Box Base Point",
                                    description="Used to determine if the assembly is a drawer box",
                                    default=False)       
    
    is_drawer_side_bp = BoolProperty(name="Is Drawer Side Base Point",
                              description="Used to determine if the assembly is a drawer side",
                              default=False)
    
    is_drawer_back_bp = BoolProperty(name="Is Drawer Back Base Point",
                              description="Used to determine if the assembly is a drawer back",
                              default=False)     
    
    is_drawer_sub_front_bp = BoolProperty(name="Is Drawer Sub Front Base Point",
                              description="Used to determine if the assembly is a drawer sub front",
                              default=False)      
    
    is_drawer_bottom_bp = BoolProperty(name="Is Drawer Bottom Base Point",
                              description="Used to determine if the assembly is a drawer bottom",
                              default=False)     
    
    is_filler_bp = BoolProperty(name="Is Filler Base Point",
                                description="Used to determine if the assembly is a filler",
                                default=False)        
    
    is_fluted_filler_bp = BoolProperty(name="Is Fluted Filler Base Point",
                                description="Used to determine if the assembly is a fluted filler",
                                default=False)     
    
    is_basket_bp = BoolProperty(name="Is Basket Base Point",
                               description="Used to determine if the assembly is basket",
                               default=False)
    
    is_hamper_bp = BoolProperty(name="Is Hamper Base Point",
                               description="Used to determine if the assembly is hamper",
                               default=False)    
    
    is_countertop_bp = BoolProperty(name="Is Countertop Base Point",
                              description="Used to determine if the object is a countertop",
                              default=False)
    
    is_handle = BoolProperty(name="Is Handle",
                              description="Used to determine if the object is a cabinet door or drawer handle",
                              default=False)
    
    is_cam = BoolProperty(name="Is Cam",
                          description="Used to determine if the object is a cam",
                          default=False)
    
    is_hinge = BoolProperty(name="Is Hinge",
                            description="Used to determine if the object is a hinge",
                            default=False)    
    
    is_hanging_rod = BoolProperty(name="Is Hanging Rod",
                                  description="Used to determine if the object is a hanging rod",
                                  default=False)
    
    is_splitter_bp = BoolProperty(name="Is Splitter Base Point",
                                  description="Used to determine if the assembly is a splitter",
                                  default=False)    
    
    is_cutpart_bp = BoolProperty(name="Is Cut Part Base Point",
                              description="Used to determine if the assembly is cutpart",
                              default=False)    

    opening_type = StringProperty(name="Opening Type",
                                  description="Type of Opening")
    
    door_type = StringProperty(name="Door Type",
                               description="Used to determine the door type. Used for pricing and reports")

    use_unique_material = BoolProperty(
        name="Use Unique Material",
        description="Specify a unique material for this part",
        default=False,
        update=update_back_mat_pointer
    )

    unique_mat_colors = EnumProperty(
        name="Unique Material Color",
        items=available_material_colors,
        update=update_render_materials
    )    

class OPERATOR_Update_Closet_Hanging_Height(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".update_closet_hanging_height"
    bl_label = "Update Closet Height"
    bl_description = "Update Closet Height"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        scene_props = get_scene_props()
        
        for obj in context.scene.objects:
            obj_props = get_object_props(obj)
            if obj_props.is_closet:
                closet = fd_types.Assembly(obj)
                closet.obj_z.location.z = scene_props.closet_defaults.hanging_height      
        
        #CANNOT IMPORT CLOSET UTILS
#         for closet in common_closet_utils.closet_products(context):
#             closet.obj_z.location.z = scene_props.closet_defaults.hanging_height
            
        return {'FINISHED'}

class OPERATOR_Update_Closet_Section_Height(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".update_closet_section_height"
    bl_label = "Update Closet Section Height"
    bl_description = "Update the Closet Section Height"
    bl_options = {'UNDO'}
    
    update_hanging = bpy.props.BoolProperty(name="Update Hanging")

    def execute(self, context):
        scene_props = get_scene_props()
        
        for obj in context.scene.objects:
            obj_props = get_object_props(obj)
            if obj_props.is_closet:     
                closet = fd_types.Assembly(obj)
        
                for i in range(1,10):
                    opening_height = closet.get_prompt("Opening " + str(i) + " Height")
                    floor_mounted = closet.get_prompt("Opening " + str(i) + " Floor Mounted")
                    
                    if opening_height and floor_mounted:
                        if self.update_hanging:
                            if not floor_mounted.value():
                                opening_height.set_value(unit.millimeter(float(scene_props.closet_defaults.hanging_panel_height)))
                        else:
                            if floor_mounted.value():
                                opening_height.set_value(unit.millimeter(float(scene_props.closet_defaults.panel_height)))
                                
                #FORCE REFRESH
                closet.obj_bp.location = closet.obj_bp.location        
        
        #CANNOT IMPORT CLOSET UTILS
#         for closet in common_closet_utils.closet_products(context):
#             for i in range(1,10):
#                 opening_height = closet.get_prompt("Opening " + str(i) + " Height")
#                 floor_mounted = closet.get_prompt("Opening " + str(i) + " Floor Mounted")
#                 
#                 if opening_height and floor_mounted:
#                     if self.update_hanging:
#                         if not floor_mounted.value():
#                             opening_height.set_value(unit.millimeter(float(scene_props.closet_defaults.hanging_panel_height)))
#                     else:
#                         if floor_mounted.value():
#                             opening_height.set_value(unit.millimeter(float(scene_props.closet_defaults.panel_height)))
#                             
#             #FORCE REFRESH
#             closet.obj_bp.location = closet.obj_bp.location
        return {'FINISHED'}

class OPERATOR_Auto_Add_Molding(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".auto_add_molding"
    bl_label = "Add Molding" 
    bl_options = {'UNDO'}

    molding_type = bpy.props.StringProperty(name="Molding Type")

    crown_profile = None
    base_profile = None
    
    tall_cabinet_switch = unit.inch(60)
    
    def get_profile(self):
        props = get_scene_props().closet_options
        if self.molding_type == 'Base':
            self.profile = utils.get_object(os.path.join(os.path.dirname(__file__),
                                                      BASE_MOLDING_FOLDER_NAME,
                                                      props.base_molding_category,
                                                      props.base_molding+".blend"))
        else:
            self.is_crown = True
            self.profile = utils.get_object(os.path.join(os.path.dirname(__file__),
                                                      CROWN_MOLDING_FOLDER_NAME,
                                                      props.crown_molding_category,
                                                      props.crown_molding+".blend"))

    def get_products(self):
        products = []
        for obj in bpy.context.visible_objects:
            if obj.mv.product_type == "Closet":
                product = fd_types.Assembly(obj)
                products.append(product)
        return products
        
    def create_extrusion(self,points,is_crown=True,product=None):
        if self.profile is None:
            self.get_profile()
        
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False)
        obj_curve = bpy.context.active_object
        obj_curve.modifiers.new("Edge Split",type='EDGE_SPLIT')
        obj_props = get_object_props(obj_curve)
        if is_crown:
            obj_props.is_crown_molding = True
        else:
            obj_props.is_base_molding = True
        obj_curve.data.splines.clear()
        spline = obj_curve.data.splines.new('BEZIER')
        spline.bezier_points.add(count=len(points) - 1)        
        obj_curve.data.show_handles = False
        obj_curve.data.bevel_object = self.profile
        obj_curve.cabinetlib.spec_group_index = product.obj_bp.cabinetlib.spec_group_index
        
        bpy.ops.fd_object.add_material_slot(object_name=obj_curve.name)
        bpy.ops.cabinetlib.sync_material_slots(object_name=obj_curve.name)
        obj_curve.cabinetlib.material_slots[0].pointer_name = "Molding"
        
        obj_curve.location = (0,0,0)
        
        for i, point in enumerate(points):
            obj_curve.data.splines[0].bezier_points[i].co = point
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.ops.object.editmode_toggle()
        obj_curve.data.dimensions = '2D'
        
        active_specgroup = bpy.context.scene.mv.spec_groups[bpy.context.scene.mv.spec_group_index]

        pointer = active_specgroup.materials["Molding"]        
        
        props = get_scene_props().closet_options
        surface_material = utils.get_material((MATERIAL_LIBRARY_NAME,
                                               pointer.category_name),
                                               pointer.item_name)
        for index, slot in enumerate(obj_curve.cabinetlib.material_slots):
            obj_curve.material_slots[index].material = surface_material        
        return obj_curve
        
    def clean_up_room(self):
        """ Removes all of the Dimensions and other objects
            That were added to the scene from this command
            We dont want multiple objects added on top of each other
            So we must clean up the scene before running this command 
        """
        is_crown = True if self.molding_type == 'Crown' else False
        objs = []
        for obj in bpy.data.objects:
            obj_props = get_object_props(obj)
            if is_crown:
                if obj_props.is_crown_molding == True:
                    objs.append(obj)
            else:
                if obj_props.is_base_molding == True:
                    objs.append(obj)
        utils.delete_obj_list(objs)

    def set_curve_location(self,product,curve,is_crown):
        curve.parent = product.obj_bp
        if is_crown:
            if product.obj_z.location.z < 0:
                curve.location.z = 0
            else:
                curve.location.z = product.obj_z.location.z

    def add_molding(self,product,is_crown=True):
        thickness = product.get_prompt("Panel Thickness")
        left_end_condition = product.get_prompt("Left End Condition")
        right_end_condition = product.get_prompt("Right End Condition")
        if left_end_condition and right_end_condition:
            start_x = 0
            for i in range(1,10):
                points = []
                width = product.get_prompt("Opening " + str(i) + " Width")
    
                if width:
                    next_width = product.get_prompt("Opening " + str(i + 1) + " Width")
                    height = product.get_prompt("Opening " + str(i) + " Height")
                    depth = product.get_prompt("Opening " + str(i) + " Depth")
                    floor = product.get_prompt("Opening " + str(i) + " Floor Mounted")
                    
                    if floor:
                        if is_crown and height.value() < unit.inch(50) and floor and floor.value():
                            continue #DONT ADD MOLDING TO UNITS SMALLER THAN 50"                    
                        
                        if not is_crown and floor and not floor.value():
                            start_x += width.value()
                            if left_end_condition and left_end_condition.value() != 'OFF':
                                start_x += thickness.value()
                            continue
                        
                        if i == 1: #FIRST
                            left_side_wall_filler = product.get_prompt("Left Side Wall Filler")
                            
                            next_height = product.get_prompt("Opening " + str(i + 1) + " Height")
                            next_depth = product.get_prompt("Opening " + str(i + 1) + " Depth")
        
                            if left_side_wall_filler and left_side_wall_filler.value() > 0:
                                
                                points.append((0,-depth.value(),0))
                            
                            else:
                            
                                if left_end_condition.value() == 'EP':
                                    points.append((0,0,0))
                                    points.append((0,-depth.value(),0))
                                else:
                                    points.append((0,-depth.value(),0))
                                    
                            if next_height:
                                
                                if (height.value() > next_height.value()) or (depth.value() > next_depth.value()):
                                    left_side_thickness = product.get_prompt("Left Side Thickness")
                                    start_x = width.value() + left_side_thickness.value() + thickness.value() + left_side_wall_filler.value()
                                    points.append((start_x,-depth.value(),0))
                                    points.append((start_x,0,0))
                                else:
                                    left_side_thickness = product.get_prompt("Left Side Thickness")
                                    start_x = width.value() + left_side_thickness.value() + left_side_wall_filler.value()
                                    points.append((start_x,-depth.value(),0))
                                    
                            else: #USED ONLY WHEN A SINGLE OPENING IS BEING CREATED
                                
                                right_side_wall_filler = product.get_prompt("Right Side Wall Filler")
                                
        
                                if right_side_wall_filler and right_side_wall_filler.value() > 0:
                                    start_x += width.value() + thickness.value() + right_side_wall_filler.value()
                                    points.append((start_x,-depth.value(),0))
                                else:
                                
                                    if right_end_condition.value() == 'EP':
                                        start_x += width.value() + (thickness.value()*2)
                                        points.append((start_x,-depth.value(),0))
                                        points.append((start_x,0,0))
                                    else:
                                        start_x += width.value() + (thickness.value()*2)
                                        points.append((start_x,-depth.value(),0))
        
                        elif next_width: #MIDDLE
                            prev_height = product.get_prompt("Opening " + str(i - 1) + " Height")
                            prev_depth = product.get_prompt("Opening " + str(i - 1) + " Depth")
                            next_height = product.get_prompt("Opening " + str(i + 1) + " Height")
                            next_depth = product.get_prompt("Opening " + str(i + 1) + " Depth")
                            
                            if (height.value() > prev_height.value()) or (depth.value() > prev_depth.value()):
                                points.append((start_x,0,0))
                                points.append((start_x,-depth.value(),0))
                                start_x += thickness.value()
                            else:
                                points.append((start_x,-depth.value(),0))
                                start_x += thickness.value()
                            
                            if (height.value() > next_height.value()) or (depth.value() > next_depth.value()):
                                start_x += width.value() + thickness.value()
                                points.append((start_x,-depth.value(),0))
                                points.append((start_x,0,0))
                            else:
                                start_x += width.value()
                                points.append((start_x,-depth.value(),0))
                        
                        else: #LAST
                            right_side_wall_filler = product.get_prompt("Right Side Wall Filler")
                            right_end_condition = product.get_prompt("Right End Condition")
                            prev_height = product.get_prompt("Opening " + str(i - 1) + " Height")
                            prev_depth = product.get_prompt("Opening " + str(i - 1) + " Depth")
                            
                            if (height.value() > prev_height.value()) or (depth.value() > prev_depth.value()):
                                points.append((start_x,0,0))
                                points.append((start_x,-depth.value(),0))
                                start_x += thickness.value()
                            else:
                                points.append((start_x,-depth.value(),0))
                                start_x += thickness.value()
                            
                            if right_side_wall_filler and right_side_wall_filler.value() > 0:
                                start_x += width.value() + thickness.value() + right_side_wall_filler.value()
                                points.append((start_x,-depth.value(),0))
                            else:
                            
                                if right_end_condition.value() == 'EP':
                                    start_x += width.value()
                                    points.append((start_x,-depth.value(),0))
                                    points.append((start_x,0,0))
                                else:
                                    start_x += width.value() + thickness.value()
                                    points.append((start_x,-depth.value(),0))
        
                        curve = self.create_extrusion(points,is_crown,product)
                        curve.parent = product.obj_bp
                        curve.mv.property_id = product.obj_bp.mv.property_id
                        if is_crown:
                            if floor.value():
                                curve.location.z = height.value()
                            else:
                                curve.location.z = product.obj_z.location.z

    def add_hutch_molding(self,product,is_crown=True):
        points = []
        current_x = 0
        
        thickness = product.get_prompt("Panel Thickness")
        
        for i in range(1,10):
            width = product.get_prompt("Opening " + str(i) + " Width")
            double_panel = product.get_prompt("Double Center Panel " + str(i))
            
            if width:
                depth = product.get_prompt("Opening " + str(i) + " Depth")
                next_depth = product.get_prompt("Opening " + str(i + 1) + " Depth")
                
                points.append((current_x,-depth.value(),0)) #FIRST POINT ON OPENING
                
                if i == 1: 
                    current_x += thickness.value()      
                    points.append((current_x,-depth.value(),0)) #LEFT SIDE THICKNESS  
                
                current_x += width.value() 
                points.append((current_x,-depth.value(),0)) #WIDTH OF OPENING
                    
                if next_depth:
                    if next_depth.value() > depth.value():
                        
                        if double_panel and double_panel.value():
                            current_x += thickness.value() 
                            points.append((current_x,-depth.value(),0)) #DOUBLE PANEL THICKNESS                        
                        
                        points.append((current_x,-next_depth.value(),0)) #NEXT DEPTH
                        current_x += thickness.value()
                        
                    elif next_depth.value() < depth.value():
                        current_x += thickness.value()
                        points.append((current_x,-depth.value(),0)) #NEXT DEPTH
                        points.append((current_x,-next_depth.value(),0)) #NEXT DEPTH     
                        
                        if double_panel and double_panel.value():
                            current_x += thickness.value()
                            points.append((current_x,-next_depth.value(),0)) #DOUBLE PANEL THICKNESS                                                

                    else:
                        current_x += thickness.value()
                        
                        if double_panel and double_panel.value():
                            current_x += thickness.value() 
                            points.append((current_x,-depth.value(),0)) #DOUBLE PANEL THICKNESS          
                                                    
                else:
                    current_x += thickness.value()
                    points.append((current_x,-depth.value(),0)) #RIGHT SIDE THICKNESS
                
        curve = self.create_extrusion(points,is_crown,product)
        curve.parent = product.obj_bp
        curve.mv.property_id = product.obj_bp.mv.property_id
        curve.location.z = product.obj_z.location.z 

    def add_island_molding(self,product):
        width = product.obj_x.location.x
        depth = product.obj_y.location.y
        
        points = []
        points.append((width/2,0,0))
        points.append((0,0,0))
        points.append((0,depth,0))
        points.append((width,depth,0))
        points.append((width,0,0))
        points.append((width/2,0,0))
        
        curve = self.create_extrusion(points,False,product)
        curve.parent = product.obj_bp
        curve.mv.property_id = product.obj_bp.mv.property_id
        curve.location.z = 0       
        
    def execute(self, context):
        self.clean_up_room()
        self.profile = None
        products = self.get_products()
        for product in products:
            obj_props = get_object_props(product.obj_bp)
            if obj_props.is_hutch and self.molding_type == 'Crown':
                self.add_hutch_molding(product)
            elif obj_props.is_island and self.molding_type == 'Base':
                self.add_island_molding(product)
            else:
                self.add_molding(product,True if self.molding_type == 'Crown' else False)
        return {'FINISHED'}
        
        
class OPERATOR_Delete_Molding(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".delete_molding"
    bl_label = "Delete Molding" 
    bl_options = {'UNDO'}

    molding_type = bpy.props.StringProperty(name="Molding Type")

    def execute(self, context):
        is_crown = True if self.molding_type == 'Crown' else False
        objs = []
        for obj in context.scene.objects:
            obj_props = get_object_props(obj)
            if is_crown:
                if obj_props.is_crown_molding == True:
                    objs.append(obj)
            else:
                if obj_props.is_base_molding == True:
                    objs.append(obj)
        utils.delete_obj_list(objs)
        return {'FINISHED'}


class OPERATOR_Update_Door_Selection(bpy.types.Operator):
    """ This will clear all the spec groups to save on file size.
    """
    bl_idname = LIBRARY_NAME_SPACE + ".update_door_selection"
    bl_label = "Update Door Selection"
    bl_description = "This will change the selected door with the active door"
    bl_options = {'UNDO'}
    
    cabinet_type = bpy.props.StringProperty(name = "Cabinet Type")
    
    def update_door_children_properties(self,obj,property_id,door_style):
        obj.mv.property_id = property_id
        if obj.type == 'EMPTY':
            obj.hide = True
        if obj.type in ('MESH','CURVE'):
            self.set_door_material_pointers(obj)
            obj.draw_type = 'TEXTURED'
            obj.mv.comment = door_style
#             for slot in obj.cabinetlib.material_slots:
#                 slot.pointer_name = "Door_Surface"
            utils.assign_materials_from_pointers(obj)
        if obj.mv.type == 'CAGE':
            obj.hide = True
        for child in obj.children:
            self.update_door_children_properties(child, property_id,door_style)
    
    def set_door_material_pointers(self,obj):
        for index, slot in enumerate(obj.cabinetlib.material_slots):
            if slot.name == 'Moderno':
                slot.pointer_name = "Moderno_Door"    
            if slot.name == 'Glass Panel':
                slot.pointer_name = "Glass"   
            if slot.name == 'Door Panel':
                slot.pointer_name = "Wood_Door_Surface"    
    
    def get_door_assembly(self,obj):
        if obj.mv.is_cabinet_door or obj.mv.is_cabinet_drawer_front:
            return obj
        else:
            if obj.parent:
                return self.get_door_assembly(obj.parent)
    
    def execute(self, context):
        door_bps = []
        props = get_scene_props().closet_options
        for obj in context.selected_objects:
            door_bp = self.get_door_assembly(obj)
            if door_bp and door_bp not in door_bps:
                door_bps.append(door_bp)

        for obj_bp in door_bps:
            door_assembly = fd_types.Assembly(obj_bp)
            
            group_bp = utils.get_group(os.path.join(os.path.dirname(__file__),
                                                 DOOR_FOLDER_NAME,
                                                 props.door_category,
                                                 props.door_style+".blend"))
            new_door = fd_types.Assembly(group_bp)
            if props.door_category == '5 Piece Doors':
                new_door.obj_bp.mv.comment_2 == '1111'
            if props.door_category == 'Deco Panels':
                new_door.obj_bp.mv.comment_2 == '2222'                                
            new_door.obj_bp.mv.name_object = door_assembly.obj_bp.mv.name_object
            new_door.obj_bp.parent = door_assembly.obj_bp.parent
            new_door.obj_bp.location = door_assembly.obj_bp.location
            new_door.obj_bp.rotation_euler = door_assembly.obj_bp.rotation_euler
            
            property_id = door_assembly.obj_bp.mv.property_id
            
            utils.copy_drivers(door_assembly.obj_bp,new_door.obj_bp)
            utils.copy_prompt_drivers(door_assembly.obj_bp,new_door.obj_bp)
            utils.copy_drivers(door_assembly.obj_x,new_door.obj_x)
            utils.copy_drivers(door_assembly.obj_y,new_door.obj_y)
            utils.copy_drivers(door_assembly.obj_z,new_door.obj_z)

            utils.delete_obj_list(utils.get_child_objects(door_assembly.obj_bp,[]))
            
            new_door.obj_bp.mv.property_id = property_id
            new_door.obj_bp.mv.is_cabinet_door = True
            obj_props = get_object_props(new_door.obj_bp)
            obj_props.is_door_bp = True
            self.update_door_children_properties(new_door.obj_bp, property_id, props.door_style)

        return {'FINISHED'}

class OPERATOR_Update_Drawer_Selection(bpy.types.Operator):
    """ This will clear all the spec groups to save on file size.
    """
    bl_idname = LIBRARY_NAME_SPACE + ".update_drawer_selection"
    bl_label = "Update Drawer Selection"
    bl_description = "This will change the drawer type"
    bl_options = {'UNDO'}
    
    cabinet_type = bpy.props.StringProperty(name = "Cabinet Type")
    
    def update_door_children_properties(self,obj,property_id,door_style):
        obj.mv.property_id = property_id
        if obj.type == 'EMPTY':
            obj.hide = True
        if obj.type == 'MESH':
            self.set_door_material_pointers(obj)
            obj.draw_type = 'TEXTURED'
            obj.mv.comment = door_style
#             for slot in obj.cabinetlib.material_slots:
#                 slot.pointer_name = "Door_Surface"
            utils.assign_materials_from_pointers(obj)
        if obj.mv.type == 'CAGE':
            obj.hide = True
        for child in obj.children:
            self.update_door_children_properties(child, property_id,door_style)
    
    def set_door_material_pointers(self,obj):
        for index, slot in enumerate(obj.cabinetlib.material_slots):
            if len(obj.material_slots) - 1 >= index:
                if obj.material_slots[index].material:
                    continue #SKIP IF MATERIAL ALREADY APPLIED
            if slot.pointer_name == "":
                slot.pointer_name = "Door_Surface"
    
    def get_door_assembly(self,obj):
        if obj.mv.is_cabinet_door or obj.mv.is_cabinet_drawer_front:
            return obj
        else:
            if obj.parent:
                return self.get_door_assembly(obj.parent)
    
    def execute(self, context):
        scene_props = get_scene_props()
        drawer_name = scene_props.closet_options.drawer_name
        
        drawer_sides = []
        drawer_boxes = []
        drawer_stacks = []
        
        for obj in context.scene.objects:
            props = get_object_props(obj)
            
            if props.is_drawer_side_bp:
                drawer_sides.append(obj)
            
            if props.is_drawer_box_bp:
                drawer_boxes.append(obj)
            
            if props.is_drawer_stack_bp:
                drawer_stacks.append(obj)
            
        for drawer_stack_bp in drawer_stacks:
            drawer_stack = fd_types.Assembly(drawer_stack_bp)
            #change drawer slide gap
            drawer_box_slide_gap = drawer_stack.get_prompt("Drawer Box Slide Gap")
            drawer_box_bottom_gap = drawer_stack.get_prompt("Drawer Box Bottom Gap")
            drawer_box_top_gap = drawer_stack.get_prompt("Drawer Box Top Gap")
        
        for drawer_box_bp in drawer_boxes:
            drawer_box = fd_types.Assembly(drawer_box_bp)
            #change box prompts
            
            hide_drawer_sub_front = drawer_box.get_prompt("Hide Drawer Sub Front")
            drawer_bottom_z_location = drawer_box.get_prompt("Drawer Bottom Z Location")
            applied_bottom = drawer_box.get_prompt("Applied Bottom")
            applied_bottom_width_deduction = drawer_box.get_prompt("Applied Bottom Width Deduction")
            applied_bottom_depth_deduction = drawer_box.get_prompt("Applied Bottom Depth Deduction")
            drawer_bottom_thickness = drawer_box.get_prompt("Drawer Bottom Thickness")
            drawer_side_thickness = drawer_box.get_prompt("Drawer Side Thickness")
            front_back_thickness = drawer_box.get_prompt("Front Back Thickness")
            
        for drawer_side_bp in drawer_sides: #SET THIS LAST TO MAKE SURE SIZE IS CORRECT
            drawer_side = fd_types.Assembly(drawer_side_bp)
            for child in drawer_side.obj_bp:
                if child.type == 'MESH':
                    pass
                    #IF drawer_name in Wood Drawer or dovetail: set to cutpart
                    #Else
                    #Set to Hardware and change name to corrrect naming            
            
        return {'FINISHED'}

class OPERATOR_Update_Pull_Selection(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".update_pull_selection"
    bl_label = "Change Pulls"
    bl_description = "This will update all of the door pulls that are currently selected"
    bl_options = {'UNDO'}
    
    update_all = bpy.props.BoolProperty(name = "Update All",default=False)
    
    def execute(self, context):
        props = get_scene_props().closet_options
        pulls = []
        
        if self.update_all:
            for obj in context.scene.objects:
                if obj.mv.is_cabinet_pull == True:
                    pulls.append(obj)    
        
        else:
            for obj in context.selected_objects:
                if obj.mv.is_cabinet_pull == True:
                    pulls.append(obj)
                
        for pull in pulls:
            pull_assembly = fd_types.Assembly(pull.parent)
            pull_assembly.set_name(props.pull_name)
            pull_length = pull_assembly.get_prompt("Pull Length")
            new_pull = utils.get_object(os.path.join(os.path.dirname(__file__),
                                                  PULL_FOLDER_NAME,
                                                  props.pull_category,
                                                  props.pull_name+".blend"))
            new_pull.mv.is_cabinet_pull = True
            new_pull.mv.name_object = pull.mv.name_object
            new_pull.mv.comment = props.pull_name
            new_pull.parent = pull.parent
            new_pull.location = pull.location
            new_pull.rotation_euler = pull.rotation_euler
            for slot in new_pull.cabinetlib.material_slots:
                slot.pointer_name = "Pull_Finish"            
            
            utils.assign_materials_from_pointers(new_pull)
            pull_length.set_value(new_pull.dimensions.x)
            utils.copy_drivers(pull,new_pull)
            
        utils.delete_obj_list(pulls)
        
        return {'FINISHED'}

class OPERATOR_Combine_Parts(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".combine_parts"
    bl_label = "Combine Parts" 
    bl_options = {'UNDO'}
    bl_description = "This will Combine the length of all of the selected parts. (This is mainly used when the Use Plant on Top option is turned on and you want to join specific tops for cutlist purposes)"

    assemblies = []

    def invoke(self,context,event):
        self.assemblies = []
        for obj in context.selected_objects:
            assembly = utils.get_assembly_bp(obj)
            if assembly not in self.assemblies:
                self.assemblies.append(assembly)
        
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(380))

    def draw(self, context):
        layout = self.layout
        layout.label("Are you sure you want to combine these parts:")
        for part in self.assemblies:
            layout.label("Part Name: " + part.mv.name_object)

    def execute(self, context):
        self.assemblies.sort(key=lambda obj: obj.location.x, reverse=False)
        first_assembly = fd_types.Assembly(self.assemblies.pop(0))
        first_assembly.obj_x.driver_remove('location',0)
        obj_list = []
        for assembly in self.assemblies:
            ass = fd_types.Assembly(assembly)
            first_assembly.obj_x.location.x += ass.obj_x.location.x
            obj_list = utils.get_child_objects(ass.obj_bp,obj_list)
            
        utils.delete_obj_list(obj_list)
        return {'FINISHED'}

class OPERATOR_Set_Pointer(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".set_pointer"
    bl_label = "Set Pointer"
    bl_description = "This will set the selected item in the file browser to this pointer."
    
    pointer_name = bpy.props.StringProperty(name="Pointer Name")

    def execute(self, context):
        closet_options = get_scene_props().closet_options
        active_specgroup = context.scene.mv.spec_groups[context.scene.mv.spec_group_index]

        pointer = active_specgroup.materials[self.pointer_name]
        pointer.library_name = MATERIAL_LIBRARY_NAME
        pointer.category_name = closet_options.material_category
        pointer.item_name = closet_options.material
        return {'FINISHED'}

class OPERATOR_Update_Material(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".update_material"
    bl_label = "Update Materials for Closet"
    bl_description = "This will update the materials for the selected cabinet"
    bl_options = {'UNDO'}
    
    selection_only = bpy.props.BoolProperty(name = "Selection Only",default=False,description="Update the materials for the selected products only.")
    
    core_material = None
    door_material = None
    surface_material = None
    edge_material = None
    
    def assign_materials(self,obj):
        if obj.type in {'MESH','CURVE'}:
            for index, slot in enumerate(obj.cabinetlib.material_slots):
                if slot.pointer_name in ("Concealed_Surface","Concealed_Edge"):
                    obj.material_slots[index].material = self.core_material
                    
                if slot.pointer_name == "Door_Surface" or slot.pointer_name == 'Door_Edges':
                    obj.material_slots[index].material = self.door_material
                    
                if slot.pointer_name == "Closet_Part_Surfaces":
                    obj.material_slots[index].material = self.surface_material

                if slot.pointer_name in ("Closet_Part_Edges"):
                    obj.material_slots[index].material = self.edge_material
                    
                if slot.pointer_name == "Molding":
                    obj.material_slots[index].material = self.molding
                                       
                    
        for child in obj.children:
            self.assign_materials(child)

    def get_products(self,context):
        product_bps = []
        
        if self.selection_only:
            for obj in context.selected_objects:
                product_bp = utils.get_bp(obj,'PRODUCT')
                if product_bp and product_bp not in product_bps:
                    product_bps.append(product_bp)
        else:
            for obj in context.visible_objects:
                product_bp = utils.get_bp(obj,'PRODUCT')
                if product_bp and product_bp not in product_bps:
                    product_bps.append(product_bp)
        
        return product_bps

    def get_materials(self,context):
        props = get_scene_props().closet_options
        self.core_material = utils.get_material((MATERIAL_LIBRARY_NAME,CORE_CATEGORY_NAME),props.core_material)
        self.door_material = utils.get_material((MATERIAL_LIBRARY_NAME,props.door_material_category),props.door_material)
        self.surface_material = utils.get_material((MATERIAL_LIBRARY_NAME,props.surface_material_category),props.surface_material)
        self.edge_material = utils.get_material((MATERIAL_LIBRARY_NAME,props.edge_material_category),props.edge_material)

    def execute(self, context):
        self.get_materials(context)
        
        product_bps = self.get_products(context)
        
        for product in product_bps:
            self.assign_materials(product)
        return {'FINISHED'}

        
class OPERATOR_Place_Applied_Panel(bpy.types.Operator):
    bl_idname = LIBRARY_NAME_SPACE + ".place_applied_panel"
    bl_label = "Place Applied Panel"
    bl_description = "This will allow you to place the active panel on cabinets and closets for an applied panel"
    bl_options = {'UNDO'}
    
    #READONLY
    filepath = bpy.props.StringProperty(name="Material Name")
    type_insert = bpy.props.StringProperty(name="Type Insert")
    
    item_name = None
    dir_name = ""
    
    assembly = None
    
    cages = []
    
    def get_panel(self,context):
        props = get_scene_props().closet_options
        bp = utils.get_group(os.path.join(os.path.dirname(__file__),
                                       DOOR_FOLDER_NAME,
                                       props.door_category,
                                       props.door_style+".blend"))
        self.assembly = fd_types.Assembly(bp)
        self.set_door_material_pointers()
        
    def set_door_material_pointers(self):
        for child in self.assembly.obj_bp.children:
            if child.type == 'MESH':
                for index, slot in enumerate(child.cabinetlib.material_slots):
                    if len(child.material_slots) - 1 >= index:
                        if child.material_slots[index].material:
                            continue #SKIP IF MATERIAL ALREADY APPLIED
                    if slot.pointer_name == "":
                        slot.pointer_name = "Door_Surface"
        
    def set_xray(self,turn_on=True):
        cages = []
        for child in self.assembly.obj_bp.children:
            child.show_x_ray = turn_on
            if turn_on:
                child.draw_type = 'WIRE'
            else:
                if child.mv.type == 'CAGE':
                    cages.append(child)
                child.draw_type = 'TEXTURED'
                utils.assign_materials_from_pointers(child)
        utils.delete_obj_list(cages)
        
    def invoke(self, context, event):
        self.get_panel(context)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
    def cancel_drop(self,context,event):
        if self.assembly:
            utils.delete_object_and_children(self.assembly.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        utils.delete_obj_list(self.cages)
        return {'FINISHED'}
        
    def add_to_left(self,part,product):
        self.assembly.obj_bp.parent = product.obj_bp
        
        if product.obj_z.location.z > 0:
            self.assembly.obj_bp.location = (0,0,0)
        else:
            self.assembly.obj_bp.location = (0,0,0)
        
        self.assembly.obj_bp.rotation_euler = (0,math.radians(-90),0)
        self.assembly.obj_x.location.x = math.fabs(product.obj_z.location.z)
        self.assembly.obj_y.location.y = product.obj_y.location.y
        
    def add_to_right(self,part,product):
        self.assembly.obj_bp.parent = product.obj_bp
        
        if product.obj_z.location.z > 0:
            self.assembly.obj_bp.location = (product.obj_x.location.x,0,0)
        else:
            self.assembly.obj_bp.location = (product.obj_x.location.x,0,0)
            
        self.assembly.obj_bp.rotation_euler = (0,math.radians(-90),math.radians(180))
        self.assembly.obj_x.location.x = math.fabs(product.obj_z.location.z)
        self.assembly.obj_y.location.y = math.fabs(product.obj_y.location.y)
        
    def add_to_back(self,part,product):
        self.assembly.obj_bp.parent = product.obj_bp
        
        toe_kick_height = 0
        if product.get_prompt('Toe Kick Height'):
            toe_kick_height = product.get_prompt('Toe Kick Height')
        
        if product.obj_z.location.z > 0:
            self.assembly.obj_bp.location = (0,0,toe_kick_height)
        else:
            self.assembly.obj_bp.location = (0,0,product.obj_z.location.z)
            
        self.assembly.obj_bp.rotation_euler = (0,math.radians(-90),math.radians(-90))
        self.assembly.obj_x.location.x = math.fabs(product.obj_z.location.z) - toe_kick_height
        self.assembly.obj_y.location.y = product.obj_x.location.x
    
    def door_panel_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event,objects=self.cages)
        bpy.ops.object.select_all(action='DESELECT')
        sel_product_bp = utils.get_bp(selected_obj,'PRODUCT')
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)
        
        if sel_product_bp and sel_assembly_bp:
            product = fd_types.Assembly(sel_product_bp)
            assembly = fd_types.Assembly(sel_assembly_bp)
            if product and assembly and 'Door' not in assembly.obj_bp.mv.name_object:
                self.assembly.obj_bp.parent = None
                sel_product_world_loc = (product.obj_bp.matrix_world[0][3],
                                         product.obj_bp.matrix_world[1][3],
                                         product.obj_bp.matrix_world[2][3])
                
                sel_product_x_world_loc = (product.obj_x.matrix_world[0][3],
                                           product.obj_x.matrix_world[1][3],
                                           product.obj_x.matrix_world[2][3])
                
                dist_to_bp = utils.calc_distance(selected_point,sel_product_world_loc)
                dist_to_x = utils.calc_distance(selected_point,sel_product_x_world_loc)
                if dist_to_bp < dist_to_x:
                    self.add_to_left(assembly,product)
                else:
                    self.add_to_right(assembly,product)
        else:
            self.assembly.obj_bp.parent = None
            self.assembly.obj_bp.location = selected_point

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.set_xray(False)
            utils.delete_obj_list(self.cages)
            bpy.context.window.cursor_set('DEFAULT')
            if event.shift:
                self.get_panel(context)
            else:
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.assembly.obj_bp
                self.assembly.obj_bp.select = True
                return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}    
        
        return self.door_panel_drop(context,event)

bpy.utils.register_class(PROPERTIES_Scene_Variables)
bpy.utils.register_class(PROPERTIES_Object_Properties)
bpy.utils.register_class(OPERATOR_Update_Closet_Hanging_Height)
bpy.utils.register_class(OPERATOR_Update_Closet_Section_Height)
bpy.utils.register_class(OPERATOR_Auto_Add_Molding)
bpy.utils.register_class(OPERATOR_Delete_Molding)
bpy.utils.register_class(OPERATOR_Update_Door_Selection)
bpy.utils.register_class(OPERATOR_Update_Pull_Selection)
bpy.utils.register_class(OPERATOR_Combine_Parts)
bpy.utils.register_class(OPERATOR_Set_Pointer)
bpy.utils.register_class(OPERATOR_Update_Material)
bpy.utils.register_class(OPERATOR_Place_Applied_Panel)
exec("bpy.types.Object." + LIBRARY_NAME_SPACE + "= PointerProperty(type = PROPERTIES_Object_Properties)")
exec("bpy.types.Scene." + LIBRARY_NAME_SPACE + "= PointerProperty(type = PROPERTIES_Scene_Variables)")