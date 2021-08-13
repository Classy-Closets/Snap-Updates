import bpy
import os
from bpy.types import PropertyGroup
from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatProperty,
                       PointerProperty,
                       EnumProperty,
                       CollectionProperty)
from snap.libraries.closets.common import common_lists
from snap.libraries.closets.common import common_parts

from snap import sn_types
from snap import sn_unit
from snap import sn_utils
from snap import sn_db
from . import closet_paths

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

LIBRARY_NAME_SPACE = "sn_closets"


def update_render_materials(self, context):
    try:
        bpy.ops.closet_materials.poll_assign_materials()
    except Exception as e:
        print(e)


def update_back_mat_pointer(self, context):
    back_mesh = context.object
    back_bp = back_mesh.parent

    if back_bp.sn_closets.use_unique_material:
        back_mesh.cabinetlib.material_slots[0].pointer_name = ""
    else:
        back_mesh.cabinetlib.material_slots[0].pointer_name = "Closet_Part_Surfaces"

    update_render_materials(self, context)


# ---------DICTIONARY DYNAMIC ENUM PROPERTIES
"""
Dynamic Enum Properties
Used to dynamically retrieve files from harddrive and display in comboboxes
"""
preview_collections = {}
preview_collections["base_moldings_categories"] = sn_utils.create_image_preview_collection()
preview_collections["base_moldings"] = sn_utils.create_image_preview_collection()
preview_collections["crown_moldings_categories"] = sn_utils.create_image_preview_collection()
preview_collections["crown_moldings"] = sn_utils.create_image_preview_collection()
preview_collections["door_style_categories"] = sn_utils.create_image_preview_collection()
preview_collections["door_styles"] = sn_utils.create_image_preview_collection()
preview_collections["pull_categories"] = sn_utils.create_image_preview_collection()
preview_collections["rods"] = sn_utils.create_image_preview_collection()
preview_collections["pulls"] = sn_utils.create_image_preview_collection()
preview_collections["hinges"] = sn_utils.create_image_preview_collection()
preview_collections["drawers"] = sn_utils.create_image_preview_collection()
preview_collections["melamine_slides"] = sn_utils.create_image_preview_collection()
preview_collections["dovetail_slides"] = sn_utils.create_image_preview_collection()
preview_collections["accessory_categories"] = sn_utils.create_image_preview_collection()
preview_collections["accessories"] = sn_utils.create_image_preview_collection()
preview_collections["material_categories"] = sn_utils.create_image_preview_collection()
preview_collections["materials"] = sn_utils.create_image_preview_collection()


# ---------BASE MOLDING DYNAMIC ENUMS
def enum_base_molding_categories(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__), BASE_MOLDING_FOLDER_NAME)
    pcoll = preview_collections["base_moldings_categories"]
    return sn_utils.get_folder_enum_previews(icon_dir, pcoll)


def enum_base_molding(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(
        os.path.dirname(__file__), BASE_MOLDING_FOLDER_NAME, self.base_molding_category)
    pcoll = preview_collections["base_moldings"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def update_base_molding_category(self, context):
    if preview_collections["base_moldings"]:
        bpy.utils.previews.remove(preview_collections["base_moldings"])
        preview_collections["base_moldings"] = sn_utils.create_image_preview_collection(
        )

    enum_base_molding(self, context)


# ---------CROWN MOLDING DYNAMIC ENUMS
def enum_crown_molding_categories(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__),
                            CROWN_MOLDING_FOLDER_NAME)
    pcoll = preview_collections["crown_moldings_categories"]
    return sn_utils.get_folder_enum_previews(icon_dir, pcoll)


def enum_crown_molding(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(
        os.path.dirname(__file__), CROWN_MOLDING_FOLDER_NAME, self.crown_molding_category)
    pcoll = preview_collections["crown_moldings"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def update_crown_molding_category(self, context):
    if preview_collections["crown_moldings"]:
        bpy.utils.previews.remove(preview_collections["crown_moldings"])
        preview_collections["crown_moldings"] = sn_utils.create_image_preview_collection()

    enum_crown_molding(self, context)


# ---------DOORS DYNAMIC ENUMS
def enum_door_categories(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(closet_paths.get_asset_folder_path(), DOOR_FOLDER_NAME)
    pcoll = preview_collections["door_style_categories"]
    return sn_utils.get_folder_enum_previews(icon_dir, pcoll)


def enum_door_styles(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(closet_paths.get_asset_folder_path(), DOOR_FOLDER_NAME, self.door_category)
    pcoll = preview_collections["door_styles"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def update_door_category(self, context):
    if preview_collections["door_styles"]:
        bpy.utils.previews.remove(preview_collections["door_styles"])
        preview_collections["door_styles"] = sn_utils.create_image_preview_collection()
    enum_door_styles(self, context)


# ---------RODS DYNAMIC ENUMS

def part_is_not_hidden(part):
    ''' Returns bool
        Determines if part assembly is hidden
    '''
    hide = part.get_prompt("Hide")
    if hide:
        if hide.get_value():
            return False
        else:
            return True
    else:
        return True


def scene_parts(context):
    ''' Generator that Returns a List of all of the assemblies in the Scene
    '''
    for obj in bpy.context.scene.objects:
        if obj.get('IS_BP_ASSEMBLY'):
            part = sn_types.Part(obj)
            if part_is_not_hidden(part):
                yield part


def enum_rods(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__), ROD_FOLDER_NAME)
    pcoll = preview_collections["rods"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def update_rods(self, context):
    for spec_group in context.scene.snap.spec_groups:
        rod_finish = spec_group.materials["Rod_Finish"]
        rod_finish.category_name = "Finished Metals"

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
        props = assembly.obj_bp.sn_closets
        if props.is_hanging_rod:
            if 'Round' in self.rods_name:
                parent_assembly = sn_types.Assembly(assembly.obj_bp.parent)
                new_rod = common_parts.add_round_hanging_rod(parent_assembly)
            else:
                parent_assembly = sn_types.Assembly(assembly.obj_bp.parent)
                new_rod = common_parts.add_oval_hanging_rod(parent_assembly)

            id_prompt = assembly.obj_bp.get("ID_PROMPT")
            new_rod.obj_bp.location = assembly.obj_bp.location
            new_rod.obj_bp.rotation_euler = assembly.obj_bp.rotation_euler
            sn_utils.copy_drivers(assembly.obj_bp, new_rod.obj_bp)
            sn_utils.copy_prompt_drivers(assembly.obj_bp, new_rod.obj_bp)
            sn_utils.copy_drivers(assembly.obj_x, new_rod.obj_x)
            sn_utils.copy_drivers(assembly.obj_y, new_rod.obj_y)
            sn_utils.copy_drivers(assembly.obj_z, new_rod.obj_z)
            sn_utils.delete_obj_list(sn_utils.get_child_objects(assembly.obj_bp))
            closet_options = bpy.context.scene.sn_closets.closet_options
            new_rod.obj_bp.snap.name_object = closet_options.rods_name

            new_rod.obj_bp.hide_set(True)
            for child in new_rod.obj_bp.children:
                if child.type == 'EMPTY':
                    child.hide_set(True)

                if child.type == 'MESH':
                    child["ID_PROMPT"] = id_prompt
                    child.display_type = 'TEXTURED'
                    sn_utils.assign_materials_from_pointers(child)
                    for mat in child.snap.material_slots:
                        mat.pointer_name = "Rod_Finish"

    bpy.ops.snap.update_scene_from_pointers()


# ---------PULLS DYNAMIC ENUMS
def enum_pull_categories(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(os.path.dirname(__file__), PULL_FOLDER_NAME)
    pcoll = preview_collections["pull_categories"]
    return sn_utils.get_folder_enum_previews(icon_dir, pcoll)


def enum_pulls(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(
        os.path.dirname(__file__), PULL_FOLDER_NAME, self.pull_category)
    pcoll = preview_collections["pulls"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def update_pull_category(self, context):
    if preview_collections["pulls"]:
        bpy.utils.previews.remove(preview_collections["pulls"])
        preview_collections["pulls"] = sn_utils.create_image_preview_collection()     

    enum_pulls(self, context)


# ---------HINGES DYNAMIC ENUMS
def enum_hinges(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(os.path.dirname(__file__), HINGE_FOLDER_NAME)
    pcoll = preview_collections["hinges"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def update_hinge(self, context):
    for obj in context.scene.objects:
        props = obj.sn_closets
        if props.is_hinge:
            obj.snap.name_object = self.hinge_name
            sn_utils.set_object_name(obj)


# ---------DRAWER DYNAMIC ENUMS
def enum_drawer(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(os.path.dirname(__file__), DRAWER_FOLDER_NAME)
    pcoll = preview_collections["drawers"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def update_drawer(self, context):
    pass


# ---------SLIDES DYNAMIC ENUMS
def enum_dt_slides(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(os.path.dirname(__file__), SLIDE_DT_FOLDER_NAME)
    pcoll = preview_collections["dovetail_slides"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def enum_mel_slides(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(os.path.dirname(__file__), SLIDE_FOLDER_NAME)
    pcoll = preview_collections["melamine_slides"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)

# def enum_slides(self, context):
    # if context is None:
    #     return []

    # if len(enum_items_slide) > 1:
    #     return enum_items_slide

    # else:
    #     with open(sn_db.SLIDE_TYPES_CSV_PATH) as slides_file:
    #         reader = csv.reader(slides_file, delimiter=',')
    #         next(reader)

    #         for row in reader:
    #             enum_items_slide.append((row[0], row[1], row[2]))

    #     return enum_items_slide

# ---------POLE CUP DYNAMIC ENUMS
def enum_rod_cups(self, context):
    if context is None:
        return []

    if len(enum_items_rod_cups) > 1:
        return enum_items_rod_cups
    
    else:
        conn = sn_db.connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT\
                *\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE '{}'\
            ;".format("%" + "pole cup" + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            enum_items_rod_cups.append((row[0], row[2], row[2]))
        
        conn.close()

        return enum_items_rod_cups                        
    
# ---------ACCESSORIES DYNAMIC ENUMS
def enum_accessories_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),ACCESSORY_FOLDER_NAME)
    pcoll = preview_collections["accessory_categories"]
    return sn_utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_accessories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),ACCESSORY_FOLDER_NAME,self.accessory_category)
    pcoll = preview_collections["accessories"]
    return sn_utils.get_image_enum_previews(icon_dir,pcoll)

def update_accessories_category(self,context):
    if preview_collections["accessories"]:
        bpy.utils.previews.remove(preview_collections["accessories"])
        preview_collections["accessories"] = sn_utils.create_image_preview_collection()     
        
    enum_accessories(self,context)        
    
# ---------MATERIALS DYNAMIC ENUMS
def enum_material_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(sn_utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME)
    pcoll = preview_collections["material_categories"]
    return sn_utils.get_folder_enum_previews(icon_dir,pcoll)

def enum_materials(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(sn_utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME,self.material_category)
    pcoll = preview_collections["materials"]
    return sn_utils.get_image_enum_previews(icon_dir,pcoll)

def update_material_category(self,context):
    if preview_collections["materials"]:
        bpy.utils.previews.remove(preview_collections["materials"])
        preview_collections["materials"] = sn_utils.create_image_preview_collection()     
        
    enum_materials(self,context)

def get_mel_colors(self, context):
    return bpy.context.scene.closet_materials.materials.mel_color_list

def get_tex_mel_colors(self, context):
    return bpy.context.scene.closet_materials.materials.textured_mel_color_list

def get_veneer_colors(self, context):
    return bpy.context.scene.closet_materials.materials.veneer_backing_color_list
    
# ---------PROPERTY GROUPS
    
class Closet_Defaults(PropertyGroup):

    defaults_tabs: EnumProperty(name="Defaults Tabs",
                       items=[('SIZE',"Size",'Show the default size options'),
                              ('CONSTRUCTION',"Construction",'Show the default construction'),
                              ('TOOLS',"Tools",'Show the Tools')],
                       default = 'SIZE')

    export_subassemblies: BoolProperty(name="Export Subassemblies",description="Export Subassemblies",default=True)   
    
    add_backing: BoolProperty(name="Add Backing",description="Add Backing",default=False)      
    
    dog_ear_active: BoolProperty(name="Dog Ear Active",description="Active Dog Ear Partition",default=False)

    add_hanging_rail: BoolProperty(name="Add Hanging Rail",description="Add Hanging Rail",default=False)   
    
    add_top_cleat: BoolProperty(name="Add Top Cleat",description="Add Top Cleat",default=True)  
    
    add_bottom_cleat: BoolProperty(name="Add Bottom Cleat",description="Add Bottom Cleat",default=True)  
    
    add_mid_cleat: BoolProperty(name="Add Mid Rail",description="Add Mid Cleat",default=False)
    
    height_to_add_mid_cleat: FloatProperty(name="Height to Add Mid Cleat",default=sn_unit.inch(59),unit='LENGTH', precision=4)
    
    hanging_rail_distance_from_top: FloatProperty(name="Hanging Rail Distance From Top",default=sn_unit.millimeter(8),unit='LENGTH', precision=4)
    
    panel_depth: FloatProperty(name="Default Partition Depth",default=sn_unit.inch(12),unit='LENGTH', precision=4)
    
    hanging_height: FloatProperty(name="Hanging Height", default=sn_unit.inch(83.25), unit='LENGTH', precision=4)
    
    panel_height: EnumProperty(name="Default Partition Height",items=common_lists.PANEL_HEIGHTS,default='2035')
    
    stacked_panel_height: EnumProperty(name="Stacked Panel Height",items=common_lists.PANEL_HEIGHTS,default='787')
    
    island_panel_height: EnumProperty(name="Default Island Panel Height",items=common_lists.PANEL_HEIGHTS,default='915')    
    
    hanging_panel_height: EnumProperty(name="Default Hanging Panel Height",items=common_lists.PANEL_HEIGHTS,default='1203')
    
    angle_top_front_panel_height: FloatProperty(name="Angle Top Front Panel Height",default=0,unit='LENGTH', precision=4)
    
    angle_top_front_panel_depth: FloatProperty(name="Angle Top Front Panel Depth",default=0,unit='LENGTH', precision=4)

    rear_notch_height_1: FloatProperty(name="Rear Notch Height 1",default=0,unit='LENGTH', precision=4)  
    
    rear_notch_height_2: FloatProperty(name="Rear Notch Height 2",default=0,unit='LENGTH', precision=4)  
    
    rear_notch_depth_1: FloatProperty(name="Rear Notch Depth 1",default=0,unit='LENGTH', precision=4)  
    
    rear_notch_depth_2: FloatProperty(name="Rear Notch Depth 2",default=0,unit='LENGTH', precision=4)      
    
    shelf_lip_width: FloatProperty(name="Shelf Lip Width",default=sn_unit.inch(1.5),unit='LENGTH', precision=4)
    
    toe_kick_height: FloatProperty(name="Toe Kick Height", default=sn_unit.inch(4.39), unit='LENGTH', precision=4)
    
    toe_kick_setback: FloatProperty(name="Toe Kick Setback",default=sn_unit.inch(1.5),unit='LENGTH', precision=4)
    
    adj_shelf_clip_gap: FloatProperty(name="Adjustable Shelf Clip Gap",default=0,unit='LENGTH', precision=4)
    
    adj_shelf_setback: FloatProperty(name="Adjustable Shelf Setback",default=sn_unit.inch(.25),unit='LENGTH', precision=4)
    
    locked_shelf_setback: FloatProperty(name="Locked Shelf Setback",default=sn_unit.inch(0),unit='LENGTH', precision=4)
    
    double_door_auto_switch: FloatProperty(name="Double Door Auto Switch",description="The opening width that door inserts should automatically switch to double doors",default=sn_unit.inch(24),unit='LENGTH', precision=4)
    
    inset_front: BoolProperty(name="Double Door Auto Switch",description="Set Inset Front to be used by default",default=False)    
    
    no_pulls: BoolProperty(name="No Pulls",description="Dont add pulls by default",default=False)  
    
    use_buyout_drawers: BoolProperty(name="Use Buyout Drawers",description="This will use buyout drawers. This will draw the drawer inserts faster",default=False)  
    
    hide_hangers: BoolProperty(name="Hide Hangers",
                                    description="Check this box to hide the models for the hangers",
                                    default=False)
    
    use_plant_on_top: BoolProperty(name="Use Plant On Top",
                                    description="Check this box to place the top above the panels. Otherwise it will place them between the sides.",
                                    default=False)
    
    use_32mm_system: BoolProperty(name="Use 32mm System",
                                    description="Check this box to use the 32mm system. This will limit the size of panels, openings, drawer fronts to ensure they are always work with the 32mm System.",
                                    default=True)
    
    show_panel_drilling: BoolProperty(name="Show Panel Drilling",
                                    description="Check this box to see the drilling operation on the panels",
                                    default=False)
    
    panel_drilling_from_front: FloatProperty(
        name="Panel Drilling from Front",
        description="This sets the dim to the front set of system holes for the visual representation ONLY. See Machining Setup Interface for machining defaults",
        default=sn_unit.millimeter(37),
        unit='LENGTH'
        )  
    
    panel_drilling_from_rear: FloatProperty(
        name="Panel Drilling from Rear",
        description="This sets the dim to the rear set of system holes for the visual representation ONLY. See Machining Setup Interface for machining defaults",
        default=sn_unit.millimeter(37),
        unit='LENGTH'
        ) 
    
    remove_bottom_hanging_shelf: BoolProperty(name="Remove Bottom Hanging Shelf",
                                               description="This will remove the bottom hanging shelf if the section is set to hanging",
                                               default=False)
    
    remove_top_shelf: BoolProperty(name="Remove Top Shelf",
                                    description="This will remove the top shelf if the section is set to hanging",
                                    default=False)
    
    drawer_bottom_dado_depth: FloatProperty(name="Drawer Bottom Dado Depth",
                                             description="This sets the dado depth for drawer bottoms. Set to 0 for no dado",
                                             default=sn_unit.inch(.25),unit='LENGTH')     
    
    drawer_bottom_z_location: FloatProperty(name="Drawer Bottom Z Location",
                                             description="This sets the distance from the bottom of the drawer box to the bottom of the drawer bottom",
                                             default=sn_unit.inch(.5),unit='LENGTH')         
    
    drawer_box_rear_gap: FloatProperty(name="Drawer Box Rear Gap",
                                             description="This sets the drawer box rear gap",
                                             default=sn_unit.inch(2),unit='LENGTH')           
    
    drawer_box_bottom_gap: FloatProperty(name="Drawer Box Bottom Gap",
                                             description="This sets the drawer box distance from the bottom of the drawer front to the bottom of the drawer box",
                                             default=sn_unit.inch(1.2),unit='LENGTH')        
    
    drawer_box_top_gap: FloatProperty(name="Drawer Box Top Gap",
                                             description="This sets the drawer box distance from the top of the drawer front to the top of the drawer box",
                                             default=sn_unit.inch(1),unit='LENGTH')     
    
    drawer_box_slide_gap: FloatProperty(name="Drawer Box Slide Gap",
                                             description="This sets the drawer box slide gap",
                                             default=sn_unit.inch(0.5),unit='LENGTH')  
    
    def draw_door_defaults(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label(text="Double Door Auto Switch:")
        row.prop(self,'double_door_auto_switch',text="")
        props = row.operator('sn_prompt.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Double Door Auto Switch'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.double_door_auto_switch
        
        row = box.row()
        row.label(text="Inset Fronts:")
        row.prop(self,'inset_front',text="")
        props = row.operator('sn_prompt.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'Inset Front'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.inset_front
        
    def draw_pull_defaults(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label(text="No Pulls:")
        row.prop(self,'no_pulls',text="")
        props = row.operator('sn_prompt.update_all_prompts_in_scene',text="",icon='FILE_REFRESH')
        props.prompt_name = 'No Pulls'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.no_pulls
        
    def draw_size_defaults(self,layout):
        box = layout.box()

        row = box.row()
        row.label(text="Default Closet Sizes:", icon='ARROW_LEFTRIGHT')

        row = box.row()
        row.label(text="Default Hang Height:")
        row.prop(self, 'hanging_height', text="")
        row.operator("sn_closets.update_closet_hanging_height",
                     text="", icon='FILE_REFRESH')

        row = box.row()
        row.label(text="Default Partition Height:")
        row.prop(self, 'hanging_panel_height', text="")
        row.operator("sn_closets.update_closet_section_height",
                     text="", icon='FILE_REFRESH').update_hanging = True

        row = box.row()
        row.label(text="Default Partition Depth:")
        row.prop(self, 'panel_depth', text="")
        row.label(text="", icon='BLANK1')

        row = box.row()
        row.label(text="Toe Kick Height:")
        row.prop(self, 'toe_kick_height', text="")
        props = row.operator(
            'sn_prompt.update_all_prompts_in_scene', text="", icon='FILE_REFRESH')
        props.prompt_name = 'Toe Kick Height'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.toe_kick_height

        row = box.row()
        row.label(text="Toe Kick Setback:")
        row.prop(self, 'toe_kick_setback', text="")
        props = row.operator(
            'sn_prompt.update_all_prompts_in_scene', text="", icon='FILE_REFRESH')
        props.prompt_name = 'Toe Kick Setback'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.toe_kick_setback
        
    def draw_construction_defaults(self, layout):
        main_col = layout.column(align=True)

        box = main_col.box()
        box.label(text="General Construction Options:", icon='MODIFIER')
        row = box.row()
        row.label(text="Show Partition Drilling:")
        row.prop(self, 'show_panel_drilling', text="")
        row.label(text="", icon='BLANK1')

        row = box.row()
        row.label(text="Hide Hangers:")
        row.prop(self, 'hide_hangers', text="")
        props = row.operator(
            'sn_prompt.update_all_prompts_in_scene', text="", icon='FILE_REFRESH')
        props.prompt_name = 'Turn Off Hangers'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.hide_hangers

        box = main_col.box()
        box.label(text="Section Options:", icon='MODIFIER')
        row = box.row()
        row.label(text="Add Backing:")
        row.prop(self, 'add_backing', text="")
        props = row.operator(
            'sn_prompt.update_all_prompts_in_scene', text="", icon='FILE_REFRESH')
        props.prompt_name = 'Add Backing'
        props.prompt_type = 'CHECKBOX'
        props.bool_value = self.add_backing

        row = box.row()
        row.label(text="Adjustable Shelf Clip Gap:")
        row.prop(self, 'adj_shelf_clip_gap', text="")
        props = row.operator(
            'sn_prompt.update_all_prompts_in_scene', text="", icon='FILE_REFRESH')
        props.prompt_name = 'Adj Shelf Clip Gap'
        props.prompt_type = 'DISTANCE'
        props.float_value = self.adj_shelf_clip_gap

        box = main_col.box()
        box.label(text="Dog Eared Partitions:", icon='MODIFIER')
        row = box.row(align=True)
        row.label(text="Angle Top Front:")
        row.prop(self, 'angle_top_front_panel_height', text="Height")
        row.prop(self, 'angle_top_front_panel_depth', text="Depth")
        
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
            tool_box.label(text="Closet Tools:",icon='SCULPTMODE_HLT')
            tool_box.operator('sn_closets.combine_parts',icon='UV_ISLANDSEL')               


class Closet_Options(PropertyGroup):
    
    hardware_tabs: EnumProperty(name="Hardware Tabs",
                                 items=[('RODS',"Rods",'Show the rod options'),
                                        ('PULLS',"Pulls",'Show the pull options'),
                                        ('HINGES',"Hinges",'Show the hinge options'),
                                        ('DRAWERS',"Drawer Slides",'Show the drawer options')],
                                 default = 'RODS')
    
    base_molding_category: EnumProperty(name="Base Molding Category",items=enum_base_molding_categories,update=update_base_molding_category)
    base_molding: EnumProperty(name="Base Molding",items=enum_base_molding)
    
    crown_molding_category: EnumProperty(name="Crown Molding Category",items=enum_crown_molding_categories,update=update_crown_molding_category)
    crown_molding: EnumProperty(name="Crown Molding",items=enum_crown_molding)
    
    door_category: EnumProperty(name="Door Category",items=enum_door_categories,update=update_door_category)
    door_style: EnumProperty(name="Door Style",items=enum_door_styles)
    
    material_category: EnumProperty(name="Material Category",items=enum_material_categories,update=update_material_category)
    material: EnumProperty(name="Material",items=enum_materials)     

    rods_name: EnumProperty(name="Rod Name",items=enum_rods,update=update_rods)
    
    pull_category: EnumProperty(name="Pull Category",items=enum_pull_categories,update=update_pull_category)
    pull_name: EnumProperty(name="Pull Name",items=enum_pulls)
    
    hinge_name: EnumProperty(name="Hinge Name",items=enum_hinges,update=update_hinge)    
    
    drawer_name: EnumProperty(name="Drawer Name",items=enum_drawer,update=update_drawer)  
    
    box_type: EnumProperty(name="Drawer Box Type",
                                 items=[('MEL',"Melamine Drawer Box",'Show the slide options'),
                                        ('DOVE',"Dovetail Drawer Box",'Show the slide options')],
                                 default = 'MEL')    
    
    dt_slide_name: EnumProperty(name="Dove Tail Slide Name",items=enum_dt_slides)    
    mel_slide_name: EnumProperty(name="Melamine Slide Name",items=enum_mel_slides)

    pole_cup_name: EnumProperty(name="Pole Cup Name",items=enum_rod_cups)
    
    accessory_category: EnumProperty(name="Accessory Category",items=enum_accessories_categories,update=update_accessories_category)
    accessory_name: EnumProperty(name="Accessory Name",items=enum_accessories)    
    
    def draw_molding_options(self,layout):
        molding_box = layout.box()
        row = molding_box.row(align=True)
        row.label(text="Moldings Options:")
        row.operator('sn_closets.auto_add_molding',text="Add Crown",icon='PLUS').molding_type = 'Crown'
        row.operator('sn_closets.auto_add_molding',text="Add Base",icon='PLUS').molding_type = 'Base'

        col = molding_box.column(align=True)
        row = col.row()
        row.label(text="Crown Molding:")
        row.operator(LIBRARY_NAME_SPACE + '.delete_molding',text="",icon='X').molding_type = 'Crown'
        col.prop(self,'crown_molding_category',text="",icon='FILE_FOLDER')
        col.template_icon_view(self,"crown_molding",show_labels=True)        
        
        col = molding_box.column(align=True)
        row = col.row()
        row.label(text="Base Molding:")
        row.operator(LIBRARY_NAME_SPACE + '.delete_molding',text="",icon='X').molding_type = 'Base'
        col.prop(self,'base_molding_category',text="",icon='FILE_FOLDER')
        col.template_icon_view(self,"base_molding",show_labels=True)   
    
    def draw_door_options(self,layout):
        door_style_box = layout.box()
        row = door_style_box.row(align=True)
        row.label(text="Door/Drawer Options:")
        row.operator('sn_closets.update_door_selection',text="Replace Selection",icon='FILE_REFRESH')
        row.operator('sn_closets.place_applied_panel',text="Place Door",icon='RESTRICT_SELECT_OFF')
        col = door_style_box.column(align=True)
        col.prop(self,'door_category',text="",icon='FILE_FOLDER')

        box = col.box()
        box.label(text=self.door_style)
        box.template_icon_view(self,"door_style",show_labels=True)
            
        props = bpy.context.scene.sn_closets
        props.closet_defaults.draw_door_defaults(door_style_box)
    
    def draw_hardware_options(self,layout):
        hardware_box = layout.box()
        row = hardware_box.row()
        row.prop(self,'hardware_tabs',expand=True)
        
        if self.hardware_tabs == 'RODS':
            col = hardware_box.column(align=True)
            row = col.row(align=True)
            row.label(text="Rods:")
            col.template_icon_view(self,"rods_name",show_labels=True)   
        
        if self.hardware_tabs == 'PULLS':
            col = hardware_box.column(align=True)
            row = col.row(align=True)
            row.label(text="Pull Options:")
            row.operator(LIBRARY_NAME_SPACE + '.update_pull_selection',text="Change Pull",icon='RESTRICT_SELECT_OFF').update_all = False
            row.operator(LIBRARY_NAME_SPACE + '.update_pull_selection',text="Replace All",icon='FILE_REFRESH').update_all = True
            col.separator()
            col.prop(self,'pull_category',text="",icon='FILE_FOLDER')
            col.label(text=self.pull_name)
            col.template_icon_view(self,"pull_name",show_labels=True)
            
            props = bpy.context.scene.sn_closets
            props.closet_defaults.draw_pull_defaults(hardware_box)
                
        if self.hardware_tabs == 'HINGES':
            col = hardware_box.column(align=True)
            row = col.row(align=True)
            row.label(text="Hinges:")
            col.template_icon_view(self,"hinge_name",show_labels=True)
        
        if self.hardware_tabs == 'DRAWERS':
            col = hardware_box.column(align=True)
            row = col.row()
            row.prop(self,'box_type',expand=True)
            
            if self.box_type == 'MEL':
                row = col.row(align=True)
                row.label(text="Melamine Slides:")
                mat_props = bpy.context.scene.closet_materials
                slide_type = mat_props.get_drawer_slide_type()
                col.menu('SNAP_MATERIAL_MT_Drawer_Slides', text=slide_type.name, icon='SOLO_ON')

            else:
                row = col.row(align=True)
                row.label(text="Dovetail Slides:")
                mat_props = bpy.context.scene.closet_materials
                slide_type = mat_props.get_drawer_slide_type()
                col.menu('SNAP_MATERIAL_MT_Drawer_Slides', text=slide_type.name, icon='SOLO_ON')


class Project_Property(PropertyGroup):
    value: StringProperty(name="Value")
    global_variable_name: StringProperty(name="Global Variable Name")
    project_wizard_variable_name: StringProperty(name="Project Wizard Variable Name")
    specification_group_name: StringProperty(name="Specification Group Name")
    
bpy.utils.register_class(Project_Property)


class PROPERTIES_Scene_Variables(PropertyGroup):
    is_drill_scene: BoolProperty(name="Is Drilling Scene",default=False)
    
    main_tabs: EnumProperty(name="Main Tabs",
                       items=[('DEFAULTS',"Defaults",'Show the closet defaults.'),
                              ('MOLDING',"Molding",'Show the molding options.'),
                              ('DOORS',"Wood Doors+Drawers",'Show the wood panel style options.'),
                              ('HARDWARE',"Hardware",'Show the hardware options.')],
                       default = 'DEFAULTS')
    
    closet_defaults: PointerProperty(name="Closet Info",type=Closet_Defaults)
    closet_options: PointerProperty(name="Closet Options",type=Closet_Options)
    project_properties: CollectionProperty(name="Project Properties",
                                            type=Project_Property,
                                            description="Collection of all of the User Defined Project Properties")    
    
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
        
        if self.main_tabs == 'DEFAULTS':
            defaults.draw(box)
            
        if self.main_tabs == 'MOLDING':
            options.draw_molding_options(box)
            
        if self.main_tabs == 'DOORS':
            options.draw_door_options(box)
            
        if self.main_tabs == 'HARDWARE':
            options.draw_hardware_options(box)

    @classmethod
    def register(cls):
        bpy.types.Scene.sn_closets = PointerProperty(
            name="SNaP Closet Library Scene Properties",
            description="SNaP Closet Library Scene Properties",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.sn_closets


class PROPERTIES_Object_Properties(PropertyGroup):
    
    is_temp_obj: BoolProperty(name="Is Temp Object",
                              description="Is temp object that should be removed before calculating price",
                              default=False)
    
    is_temp_hardware: BoolProperty(name="Is Temp Hardware",
                                   description="Is temp hardware that is added from an operator",
                                   default=False)    
    
    is_closet: BoolProperty(name="Is Closet",
                            description="Used to determine if the product is a closet",
                            default=False)
    
    is_fixed_shelf_and_rod_product_bp: BoolProperty(name="Is Fixed Shelf and Rod Product",
                                                    description="Used to determine if the product is a fixed shelf and rod",
                                                    default=False)    

    is_hutch: BoolProperty(name="Is Hutch",
                           description="Used to determine if the product is a hutch",
                           default=False)
    
    is_island: BoolProperty(name="Is Island",
                            description="Used to determine if the product is a island",
                            default=False)        
    
    is_hamper_insert_bp: BoolProperty(name="Is Hamper Insert BP",
                                      description="Used to determine if the insert is a Hamper Insert",
                                      default=False)
    
    is_closet_top_bp: BoolProperty(name="Is Closet Top BP",
                                   description="Used to determine if the object is a closet top base point",
                                   default=False)
    
    is_empty_molding: BoolProperty(name="Is Empty Molding",
                                    description="Used to determine if the object is an empty assembly used for molding export")

    is_crown_molding: BoolProperty(name="Is Crown Molding",
                                   description="Used to determine if the object is closet crown molding",
                                   default=False)
    
    is_base_molding: BoolProperty(name="Is Base Molding",
                                  description="Used to determine if the object is closet base molding",
                                  default=False)
    
    is_door_bp: BoolProperty(name="Is Door Base Point",
                             description="Used to determine if the assembly is a door",
                             default=False)

    is_door_insert_bp: BoolProperty(
        name="Is Door Insert Base Point",
        description="Used to determine if the assembly is a door insert",
        default=False
    )

    is_drawer_front_bp: BoolProperty(name="Is Drawer Front Base Point",
                                      description="Used to determine if the assembly is a drawer front",
                                      default=False)
    
    is_hamper_front_bp: BoolProperty(name="Is Hamper Front Base Point",
                                      description="Used to determine if the assembly is a hamper front",
                                      default=False)
    
    is_counter_top_insert_bp: BoolProperty(name="Is Countertop Insert Base Point",
                                      description="Used to determine if the assembly is a countertop insert",
                                      default=False)
    
    is_ironing_board_door_front_bp: BoolProperty(name="Is Ironing Board Door Front Base Point",
                                      description="Used to determine if the assembly is a ironing board front",
                                      default=False) 
    
    is_panel_bp: BoolProperty(name="Is Panel Base Point",
                               description="Used to determine if the assembly is a vertical panel",
                               default=False)

    is_blind_corner_panel_bp: BoolProperty(name="Is Blind Corner Panel Point",
                               description="Used to determine if the part is a vertical blind corner panel",
                               default=False)

    is_mitered_pard_bp: BoolProperty(name="Is Mitered Partition Point",
                               description="Used to determine if the part is a mitered partition base point",
                               default=False)                                       

    is_slanted_shelf_bp: BoolProperty(name="Is Slanted Shelf Base Point",
                               description="Used to determine if the assembly is a slanted shelf base point",
                               default=False)    
    
    is_sliding_shelf_bp: BoolProperty(name="Is Sliding Shelf Base Point",
                               description="Used to determine if the assembly is a sliding shelf base point",
                               default=False)
    
    is_rollout_tray_bp: BoolProperty(name="Is Rollout Tray Base Point",
                               description="Used to determine if the assembly is a rollout tray base point",
                               default=False)    
    
    is_shelf_bp: BoolProperty(name="Is Shelf Base Point",
                               description="Used to determine if the assembly is a fixed or adj shelf",
                               default=False)

    is_glass_shelf_bp: BoolProperty(name="Is Glass Shelf Base Point",
                               description="Used to determine if the assembly is a glass shelf",
                               default=False)
    
    is_l_shelf_bp: BoolProperty(name="Is L Shelf Base Point",
                               description="Used to determine if the assembly is a l shelf base point",
                               default=False)    
    
    is_angle_shelf_bp: BoolProperty(name="Is Angle Shelf Base Point",
                               description="Used to determine if the assembly is a angle shelf base point",
                               default=False)        
    
    is_radius_shelf_bp: BoolProperty(name="Is Radius Shelf Base Point",
                               description="Used to determine if the assembly is a radius shelf base point",
                               default=False) 
    
    is_plant_on_top_bp: BoolProperty(name="Is Plant on Top Base Point",
                                      description="Used to determine if the assembly is a plant on top",
                                      default=False)
    
    is_hpl_top_bp: BoolProperty(name="Is HPL Top Base Point",
                                      description="Used to determine if the assembly is a hpl top",
                                      default=False)    
    
    is_cleat_bp: BoolProperty(name="Is Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)

    is_cover_cleat_bp: BoolProperty(name="Is Cover Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)

    is_wall_cleat_bp: BoolProperty(name="Is Wall Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)
    
    is_door_striker_bp: BoolProperty(name="Is Door Striker Base Point",
                               description="Used to determine if the assembly is a door striker",
                               default=False)    
    
    is_shelf_and_rod_bp = BoolProperty(name="Is Shelf and Rod Base Point",
                               description="Used to determine if the assembly is a shelf and rod assembly",
                               default=False)

    is_shelf_and_rod_cleat_bp: BoolProperty(name="Is Shelf and Rod Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)    
    
    is_shelf_and_rod_fe_cleat_bp: BoolProperty(name="Is Shelf and Rod Cleat Base Point",
                               description="Used to determine if the assembly is a cleat",
                               default=False)        
    
    is_toe_kick_insert_bp: BoolProperty(name="Is Toe Kick Insert Base Point",
                                  description="Used to determine if the assembly is a toe kick insert",
                                  default=False)

    is_toe_kick_bp: BoolProperty(name="Is Toe Kick Base Point",
                                  description="Used to determine if the assembly is a toe kick",
                                  default=False)

    is_toe_kick_end_cap_bp: BoolProperty(name="Is Toe Kick End Cap Base Point",
                                  description="Used to determine if the assembly is a toe kick end cap",
                                  default=False)

    is_toe_kick_stringer_bp: BoolProperty(name="Is Toe Kick Stringer Base Point",
                                  description="Used to determine if the assembly is a toe kick stringer",
                                  default=False)
    
    is_toe_kick_skin_bp: BoolProperty(name="Is Toe Kick Skin Base Point",
                                  description="Used to determine if the assembly is a toe kick skin",
                                  default=False)    

    is_shelf_lip_bp: BoolProperty(name="Is Shelf Lip Base Point",
                                   description="Used to determine if the assembly is a shelf lip",
                                   default=False)    
    
    is_deco_shelf_lip_bp: BoolProperty(name="Is Deco Shelf Lip Base Point",
                                   description="Used to determine if the assembly is a deco shelf lip",
                                   default=False)
    
    is_spacer_bp: BoolProperty(name="Is Spacer Base Point",
                                description="Used to determine if the assembly is a drawer spacer",
                                default=False)

    is_shelf_fence_bp: BoolProperty(name="Is Shelf Fence Base Point",
                                   description="Used to determine if the assembly is a shelf fence",
                                   default=False)
    
    is_divider_bp: BoolProperty(name="Is Divider Base Point",
                                   description="Used to determine if the assembly is a divider",
                                   default=False)
    
    is_division_bp: BoolProperty(name="Is Division Base Point",
                                  description="Used to determine if the assembly is a division",
                                  default=False)
    
    is_back_bp: BoolProperty(name="Is Back Base Point",
                              description="Used to determine if the assembly is a back",
                              default=False)

    is_top_back_bp: BoolProperty(name="Is Top Back Base Point",
                              description="Used to determine if the assembly is a top section back",
                              default=False)

    is_bottom_back_bp: BoolProperty(name="Is Bottom Back Base Point",
                              description="Used to determine if the assembly is a bottom section back",
                              default=False)
    
    is_hutch_back_bp: BoolProperty(
        name="Is Hutch Back Base Point",
        description="Used to determine if the assembly is a hutch back",
        default=False)

    is_corner_back_bp: BoolProperty(name="Is Corner Back Base Point",
                              description="Used to determine if the assembly is a back apart of a corner shelf assembly",
                              default=False)        

    is_closet_bottom_bp: BoolProperty(
        name="Is Closet Bottom BP",
        description="Used to determine if the object is a closet bottom base point",
        default=False)        

    is_drawer_stack_bp: BoolProperty(name="Is Drawer Stack Base Point",
                                    description="Used to determine if the assembly is a drawer stack base point",
                                    default=False)       
    
    is_drawer_box_bp: BoolProperty(name="Is Drawer Box Base Point",
                                    description="Used to determine if the assembly is a drawer box",
                                    default=False)       
    
    is_drawer_side_bp: BoolProperty(name="Is Drawer Side Base Point",
                              description="Used to determine if the assembly is a drawer side",
                              default=False)
    
    is_drawer_back_bp: BoolProperty(name="Is Drawer Back Base Point",
                              description="Used to determine if the assembly is a drawer back",
                              default=False)     
    
    is_drawer_sub_front_bp: BoolProperty(name="Is Drawer Sub Front Base Point",
                              description="Used to determine if the assembly is a drawer sub front",
                              default=False)      
    
    is_drawer_bottom_bp: BoolProperty(name="Is Drawer Bottom Base Point",
                              description="Used to determine if the assembly is a drawer bottom",
                              default=False)     
    
    is_filler_bp: BoolProperty(name="Is Filler Base Point",
                                description="Used to determine if the assembly is a filler",
                                default=False)        
    
    is_fluted_filler_bp: BoolProperty(name="Is Fluted Filler Base Point",
                                description="Used to determine if the assembly is a fluted filler",
                                default=False)     
    
    is_basket_bp: BoolProperty(name="Is Basket Base Point",
                               description="Used to determine if the assembly is basket",
                               default=False)
    
    is_hamper_bp: BoolProperty(name="Is Hamper Base Point",
                               description="Used to determine if the assembly is hamper",
                               default=False)    
    
    is_countertop_bp: BoolProperty(name="Is Countertop Base Point",
                              description="Used to determine if the object is a countertop",
                              default=False)
    
    is_handle: BoolProperty(name="Is Handle",
                              description="Used to determine if the object is a cabinet door or drawer handle",
                              default=False)
    
    is_cam: BoolProperty(name="Is Cam",
                          description="Used to determine if the object is a cam",
                          default=False)
    
    is_hinge: BoolProperty(name="Is Hinge",
                            description="Used to determine if the object is a hinge",
                            default=False)    
    
    is_hanging_rod: BoolProperty(name="Is Hanging Rod",
                                  description="Used to determine if the object is a hanging rod",
                                  default=False)
    
    is_splitter_bp: BoolProperty(name="Is Splitter Base Point",
                                  description="Used to determine if the assembly is a splitter",
                                  default=False)    
    
    is_cutpart_bp: BoolProperty(name="Is Cut Part Base Point",
                              description="Used to determine if the assembly is cutpart",
                              default=False)

    is_accessory_bp: BoolProperty(name="Is Accessory Base Point",
                              description="Used to determine if the assembly is an accessory",
                              default=False)   

    is_file_rail_bp: BoolProperty(name="Is File Rail Base Point",
                              description="Used to determine if the assembly is an file rail",
                              default=False)

    is_flat_crown_bp: BoolProperty(name="Is Flat Crown BP",
                              description="Used to determine if the assembly is an Flat Crown",
                              default=False)   

    opening_type: StringProperty(name="Opening Type",
                                  description="Type of Opening")
    
    door_type: StringProperty(name="Door Type",
                               description="Used to determine the door type. Used for pricing and reports")

    use_unique_material: BoolProperty(
        name="Use Unique Material",
        description="Specify a unique material for this part",
        default=False,
        update=update_back_mat_pointer
    )

    unique_mat_types: EnumProperty(
        name="Unique Material Type",
        items=[
            ('MELAMINE','Melamine','Melamine'),
            ('TEXTURED_MELAMINE','Textured Melamine','Textured Melamine'),
            ('VENEER','Veneer','Veneer')
        ],
        update=update_render_materials        
    )

    unique_mat_mel: EnumProperty(
        name="Unique Melamine Material Type",
        items=get_mel_colors,
        update=update_render_materials
    )

    unique_mat_tex_mel: EnumProperty(
        name="Unique Textured Melamine Material Color",
        items=get_tex_mel_colors,
        update=update_render_materials
    )

    unique_mat_veneer: EnumProperty(
        name="Unique Veneer Material Color",
        items=get_veneer_colors,
        update=update_render_materials
    )

    opening_name: StringProperty(name="Opening Name",description="Name of the opening")   


    @classmethod
    def register(cls):
        bpy.types.Object.sn_closets = PointerProperty(
            name="SNaP Closet Library Object Properties",
            description="SNaP Closet Library Object Properties",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Object.sn_closets


classes = (
    Closet_Defaults,
    Closet_Options,
    PROPERTIES_Scene_Variables,
    PROPERTIES_Object_Properties,
)

register, unregister = bpy.utils.register_classes_factory(classes)