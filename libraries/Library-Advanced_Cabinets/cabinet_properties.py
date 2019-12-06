import bpy
import os
from mv import fd_types, unit, utils

ROOT_DIR = os.path.dirname(__file__)
MOLDING_FOLDER_NAME = "Molding Profiles"
CROWN_MOLDING_FOLDER_NAME = "Crown"
BASE_MOLDING_FOLDER_NAME = "Base"
LIGHT_MOLDING_FOLDER_NAME = "Light"
DOOR_FOLDER_NAME = "Door Panels"
PULL_FOLDER_NAME = "Cabinet Pulls"
MATERIAL_LIBRARY_NAME = "Cabinet Materials"
CORE_CATEGORY_NAME = "Wood Core"
COLUMN_FOLDER_NAME = "Columns"

preview_collections = {}

#---------BASE MOLDING
preview_collections["base_moldings_categories"] = utils.create_image_preview_collection()

def enum_base_molding_categories(self,context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__),MOLDING_FOLDER_NAME,BASE_MOLDING_FOLDER_NAME)
    pcoll = preview_collections["base_moldings_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

preview_collections["base_moldings"] = utils.create_image_preview_collection()

def enum_base_molding(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),MOLDING_FOLDER_NAME,BASE_MOLDING_FOLDER_NAME,self.base_molding_category)
    pcoll = preview_collections["base_moldings"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_base_molding_category(self,context):
    if preview_collections["base_moldings"]:
        bpy.utils.previews.remove(preview_collections["base_moldings"])
        preview_collections["base_moldings"] = utils.create_image_preview_collection()     
        
    enum_base_molding(self,context)

#---------CROWN MOLDING
preview_collections["crown_moldings_categories"] = utils.create_image_preview_collection()   

def enum_crown_molding_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),MOLDING_FOLDER_NAME,CROWN_MOLDING_FOLDER_NAME)
    pcoll = preview_collections["crown_moldings_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

preview_collections["crown_moldings"] = utils.create_image_preview_collection()   

def enum_crown_molding(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),MOLDING_FOLDER_NAME,CROWN_MOLDING_FOLDER_NAME,self.crown_molding_category)
    pcoll = preview_collections["crown_moldings"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_crown_molding_category(self,context):
    if preview_collections["crown_moldings"]:
        bpy.utils.previews.remove(preview_collections["crown_moldings"])
        preview_collections["crown_moldings"] = utils.create_image_preview_collection()     
        
    enum_crown_molding(self,context)

#---------LIGHT RAIL MOLDING
preview_collections["light_rail_moldings_categories"] = utils.create_image_preview_collection()   

def enum_light_rail_molding_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),MOLDING_FOLDER_NAME,LIGHT_MOLDING_FOLDER_NAME)
    pcoll = preview_collections["light_rail_moldings_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

preview_collections["light_rail_moldings"] = utils.create_image_preview_collection()   

def enum_light_rail_molding(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),MOLDING_FOLDER_NAME,LIGHT_MOLDING_FOLDER_NAME,self.light_rail_molding_category)
    pcoll = preview_collections["light_rail_moldings"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_light_rail_molding_category(self,context):
    if preview_collections["light_rail_moldings"]:
        bpy.utils.previews.remove(preview_collections["light_rail_moldings"])
        preview_collections["light_rail_moldings"] = utils.create_image_preview_collection()     
        
    enum_light_rail_molding(self,context)

#---------DOORS
preview_collections["door_style_categories"] = utils.create_image_preview_collection()  

def enum_door_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),DOOR_FOLDER_NAME)
    pcoll = preview_collections["door_style_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

preview_collections["door_styles"] = utils.create_image_preview_collection()  
 
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

#---------COLUMNS
preview_collections["column_categories"] = utils.create_image_preview_collection() 

def enum_column_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),COLUMN_FOLDER_NAME)
    pcoll = preview_collections["column_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

preview_collections["column_styles"] = utils.create_image_preview_collection()   

def enum_column_styles(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),COLUMN_FOLDER_NAME,self.column_category)
    pcoll = preview_collections["column_styles"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_column_category(self,context):
    if preview_collections["column_styles"]:
        bpy.utils.previews.remove(preview_collections["column_styles"])
        preview_collections["column_styles"] = utils.create_image_preview_collection()     
        
    enum_column_styles(self,context)

#---------PULLS
preview_collections["pull_categories"] = utils.create_image_preview_collection() 

def enum_pull_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),PULL_FOLDER_NAME)
    pcoll = preview_collections["pull_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

preview_collections["pulls"] = utils.create_image_preview_collection() 

def enum_pulls(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(os.path.dirname(__file__),PULL_FOLDER_NAME,self.pull_category)
    pcoll = preview_collections["pulls"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_pull_category(self,context):
    if preview_collections["edge_materials"]:
        bpy.utils.previews.remove(preview_collections["edge_materials"])
        preview_collections["edge_materials"] = utils.create_image_preview_collection()     
        
    enum_pulls(self,context)

#---------MATERIALS
preview_collections["wood_core_materials"] = utils.create_image_preview_collection()   

def enum_core_materials(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME,CORE_CATEGORY_NAME)
    pcoll = preview_collections["wood_core_materials"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

preview_collections["material_categories"] = utils.create_image_preview_collection()  

def enum_material_categories(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME)
    pcoll = preview_collections["material_categories"]
    return utils.get_folder_enum_previews(icon_dir,pcoll)

preview_collections["door_materials"] = utils.create_image_preview_collection()  

def enum_door_materials(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME,self.door_material_category)
    pcoll = preview_collections["door_materials"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_door_material_category(self,context):
    if preview_collections["door_materials"]:
        bpy.utils.previews.remove(preview_collections["door_materials"])
        preview_collections["door_materials"] = utils.create_image_preview_collection()     
        
    enum_door_materials(self,context)

preview_collections["exterior_materials"] = utils.create_image_preview_collection()  

def enum_exterior_materials(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME,self.exterior_material_category)
    pcoll = preview_collections["exterior_materials"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_exterior_material_category(self,context):
    if preview_collections["exterior_materials"]:
        bpy.utils.previews.remove(preview_collections["exterior_materials"])
        preview_collections["exterior_materials"] = utils.create_image_preview_collection()     
        
    enum_exterior_materials(self,context)

preview_collections["interior_materials"] = utils.create_image_preview_collection()  

def enum_interior_materials(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME,self.interior_material_category)
    pcoll = preview_collections["interior_materials"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_interior_material_category(self,context):
    if preview_collections["interior_materials"]:
        bpy.utils.previews.remove(preview_collections["interior_materials"])
        preview_collections["interior_materials"] = utils.create_image_preview_collection()     
        
    enum_interior_materials(self,context)

preview_collections["edge_materials"] = utils.create_image_preview_collection()  

def enum_edge_materials(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),MATERIAL_LIBRARY_NAME,self.edge_material_category)
    pcoll = preview_collections["edge_materials"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_edge_material_category(self,context):
    if preview_collections["edge_materials"]:
        bpy.utils.previews.remove(preview_collections["edge_materials"])
        preview_collections["edge_materials"] = utils.create_image_preview_collection()     
        
    enum_edge_materials(self,context)

class PROPERTIES_Cabinet_Sizes(bpy.types.PropertyGroup):
    base_cabinet_depth = bpy.props.FloatProperty(name="Base Cabinet Depth",
                                                 description="Default depth for base cabinets",
                                                 default=unit.inch(23.0),
                                                 unit='LENGTH')
    
    base_cabinet_height = bpy.props.FloatProperty(name="Base Cabinet Height",
                                                  description="Default height for base cabinets",
                                                  default=unit.inch(34.0),
                                                  unit='LENGTH')
    
    base_inside_corner_size= bpy.props.FloatProperty(name="Base Inside Corner Size",
                                                     description="Default width and depth for the inside base corner cabinets",
                                                     default=unit.inch(36.0),
                                                     unit='LENGTH')
    
    tall_cabinet_depth = bpy.props.FloatProperty(name="Tall Cabinet Depth",
                                                 description="Default depth for tall cabinets",
                                                 default=unit.inch(25.0),
                                                 unit='LENGTH')
    
    tall_cabinet_height = bpy.props.FloatProperty(name="Tall Cabinet Height",
                                                  description="Default height for tall cabinets",
                                                  default=unit.inch(84.0),
                                                  unit='LENGTH')
    
    upper_cabinet_depth = bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                  description="Default depth for upper cabinets",
                                                  default=unit.inch(12.0),
                                                  unit='LENGTH')
    
    upper_cabinet_height = bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                   description="Default height for upper cabinets",
                                                   default=unit.inch(34.0),
                                                   unit='LENGTH')
    
    upper_inside_corner_size= bpy.props.FloatProperty(name="Upper Inside Corner Size",
                                                      description="Default width and depth for the inside upper corner cabinets",
                                                      default=unit.inch(24.0),
                                                      unit='LENGTH')
    
    sink_cabinet_depth = bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                 description="Default depth for sink cabinets",
                                                 default=unit.inch(23.0),
                                                 unit='LENGTH')
    
    sink_cabinet_height = bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                  description="Default height for sink cabinets",
                                                  default=unit.inch(34.0),
                                                  unit='LENGTH')

    suspended_cabinet_depth = bpy.props.FloatProperty(name="Upper Cabinet Depth",
                                                      description="Default depth for suspended cabinets",
                                                      default=unit.inch(23.0),
                                                      unit='LENGTH')
    
    suspended_cabinet_height = bpy.props.FloatProperty(name="Upper Cabinet Height",
                                                       description="Default height for suspended cabinets",
                                                       default=unit.inch(6.0),
                                                       unit='LENGTH')

    column_width = bpy.props.FloatProperty(name="Column Width",
                                           description="Default width for cabinet columns",
                                           default=unit.inch(2),
                                           unit='LENGTH')

    width_1_door = bpy.props.FloatProperty(name="Width 1 Door",
                                           description="Default width for one door wide cabinets",
                                           default=unit.inch(18.0),
                                           unit='LENGTH')
    
    width_2_door = bpy.props.FloatProperty(name="Width 2 Door",
                                           description="Default width for two door wide and open cabinets",
                                           default=unit.inch(36.0),
                                           unit='LENGTH')
    
    width_drawer = bpy.props.FloatProperty(name="Width Drawer",
                                           description="Default width for drawer cabinets",
                                           default=unit.inch(18.0),
                                           unit='LENGTH')
    
    base_width_blind = bpy.props.FloatProperty(name="Base Width Blind",
                                               description="Default width for base blind corner cabinets",
                                               default=unit.inch(48.0),
                                               unit='LENGTH')
    
    tall_width_blind = bpy.props.FloatProperty(name="Tall Width Blind",
                                               description="Default width for tall blind corner cabinets",
                                               default=unit.inch(48.0),
                                               unit='LENGTH')
    
    blind_panel_reveal = bpy.props.FloatProperty(name="Blind Panel Reveal",
                                                 description="Default reveal for blind panels",
                                                 default=unit.inch(3.0),
                                                 unit='LENGTH')
    
    inset_blind_panel = bpy.props.BoolProperty(name="Inset Blind Panel",
                                               description="Check this to inset the blind panel into the cabinet carcass",
                                               default=True)
    
    upper_width_blind = bpy.props.FloatProperty(name="Upper Width Blind",
                                                description="Default width for upper blind corner cabinets",
                                                default=unit.inch(36.0),
                                                unit='LENGTH')

    height_above_floor = bpy.props.FloatProperty(name="Height Above Floor",
                                                 description="Default height above floor for upper cabinets",
                                                 default=unit.inch(84.0),
                                                 unit='LENGTH')
    
    equal_drawer_stack_heights = bpy.props.BoolProperty(name="Equal Drawer Stack Heights", 
                                                        description="Check this make all drawer stack heights equal. Otherwise the Top Drawer Height will be set.", 
                                                        default=True)
    
    top_drawer_front_height = bpy.props.FloatProperty(name="Top Drawer Front Height",
                                                      description="Default top drawer front height.",
                                                      default=unit.inch(6.0),
                                                      unit='LENGTH')

bpy.utils.register_class(PROPERTIES_Cabinet_Sizes)

class PROPERTIES_Carcass_Defaults(bpy.types.PropertyGroup):
    
    use_full_tops = bpy.props.BoolProperty(name="Use Full Tops", 
                                           description="Check this to use full tops and not stretchers on base cabinets", 
                                           default=False)
    
    use_notched_sides = bpy.props.BoolProperty(name="Use Notched Sides", 
                                               description="Check this to use notched sides for base and tall cabinets", 
                                               default=True)
    
    use_thick_back = bpy.props.BoolProperty(name="Use Thick Back", 
                                            description="Check this to use thick backs", 
                                            default=False)
    
    use_nailers = bpy.props.BoolProperty(name="Use Nailers", 
                                         description="Check this to use nailers", 
                                         default=True)
    
    use_leg_levelers = bpy.props.BoolProperty(name="Use Leg Levelers", 
                                              description="Turn this on to use leg levelers for the base assembly. Otherwise cabinet sides will extend the full height of the cabinet", 
                                              default=False)
    
    remove_back = bpy.props.BoolProperty(name="Remove Back", 
                                         description="This removes the cabinet back. ", 
                                         default=False)
    
    extend_sides_to_floor = bpy.props.BoolProperty(name="Extend Sides To Floor", 
                                                   description="Extend sides to the floor for base and tall cabinets. ", 
                                                   default=True)
    
    door_valance_top = bpy.props.BoolProperty(name="Door Valance Top", 
                                              description="Extend top of door to top of valance. ", 
                                              default=True)
    
    door_valance_bottom = bpy.props.BoolProperty(name="Door Valance Bottom", 
                                                 description="Extend bottom of door to bottom of valance. ", 
                                                 default=True)
    
    valance_each_unit = bpy.props.BoolProperty(name="Valacne Each Unit", 
                                               description="Add a separte valance part for each cabinet. ", 
                                               default=True)
    
    toe_kick_height = bpy.props.FloatProperty(name="Toe Kick Height",
                                              description="Default toe kick height for cabinets",
                                              default=unit.inch(4.0),
                                              unit='LENGTH')
    
    toe_kick_setback = bpy.props.FloatProperty(name="Toe Kick Setback",
                                               description="Default toe kick height setback for cabinets",
                                               default=unit.inch(3.25),
                                               unit='LENGTH')
    
    center_nailer_switch = bpy.props.FloatProperty(name="Center Nailer Switch",
                                                   description="Smallest height of a cabinet to include a center nailer",
                                                   default=unit.inch(60),
                                                   unit='LENGTH')
    
    nailer_width = bpy.props.FloatProperty(name="Nailer Width",
                                           description="Default width for nailers",
                                           default=unit.inch(4),
                                           unit='LENGTH')
    
    stretcher_width = bpy.props.FloatProperty(name="Stretcher Width",
                                              description="Default width for stretchers",
                                              default=unit.inch(4),
                                              unit='LENGTH')
    
    valance_height_top = bpy.props.FloatProperty(name="Valance Height Top",
                                                 description="Default Top Valance Height",
                                                 default=unit.inch(0),
                                                 unit='LENGTH')
    
    valance_height_bottom = bpy.props.FloatProperty(name="Valance Height Bottom",
                                                    description="Default Bottom Valance Height",
                                                    default=unit.inch(0),
                                                    unit='LENGTH')
    
    sub_front_height = bpy.props.FloatProperty(name="Sub Front Height",
                                               description="Default Sink Sub Front Height",
                                               default=unit.inch(7),
                                               unit='LENGTH')

bpy.utils.register_class(PROPERTIES_Carcass_Defaults)

class PROPERTIES_Exterior_Defaults(bpy.types.PropertyGroup):
    inset_door = bpy.props.BoolProperty(name="Inset Door", 
                              description="Check this to use inset doors", 
                              default=False)
    
    inset_reveal = bpy.props.FloatProperty(name="Inset Reveal",
                                 description="This sets the reveal for inset doors.",
                                 default=unit.inch(.125),
                                 unit='LENGTH',
                                 precision=4)
    
    left_reveal = bpy.props.FloatProperty(name="Left Reveal",
                                description="This sets the left reveal for overlay doors.",
                                default=unit.inch(.0625),
                                unit='LENGTH',
                                precision=4)
    
    right_reveal = bpy.props.FloatProperty(name="Right Reveal",
                                 description="This sets the right reveal for overlay doors.",
                                 default=unit.inch(.0625),
                                 unit='LENGTH',
                                 precision=4)
    
    base_top_reveal = bpy.props.FloatProperty(name="Base Top Reveal",
                                    description="This sets the top reveal for base overlay doors.",
                                    default=unit.inch(.25),
                                    unit='LENGTH',
                                    precision=4)
    
    tall_top_reveal = bpy.props.FloatProperty(name="Tall Top Reveal",
                                    description="This sets the top reveal for tall overlay doors.",
                                    default=unit.inch(0),
                                    unit='LENGTH',
                                    precision=4)
    
    upper_top_reveal = bpy.props.FloatProperty(name="Upper Top Reveal",
                                     description="This sets the top reveal for upper overlay doors.",
                                     default=unit.inch(0),
                                     unit='LENGTH',
                                     precision=4)
    
    base_bottom_reveal = bpy.props.FloatProperty(name="Base Bottom Reveal",
                                       description="This sets the bottom reveal for base overlay doors.",
                                       default=unit.inch(0),
                                       unit='LENGTH',
                                       precision=4)
    
    tall_bottom_reveal = bpy.props.FloatProperty(name="Tall Bottom Reveal",
                                       description="This sets the bottom reveal for tall overlay doors.",
                                       default=unit.inch(0),
                                       unit='LENGTH',
                                       precision=4)
    
    upper_bottom_reveal = bpy.props.FloatProperty(name="Upper Bottom Reveal",
                                        description="This sets the bottom reveal for upper overlay doors.",
                                        default=unit.inch(.25),
                                        unit='LENGTH',
                                        precision=4)
    
    vertical_gap = bpy.props.FloatProperty(name="Vertical Gap",
                                 description="This sets the distance between double doors.",
                                 default=unit.inch(.125),
                                 unit='LENGTH',
                                 precision=4)
    
    door_to_cabinet_gap = bpy.props.FloatProperty(name="Door to Cabinet Gap",
                                        description="This sets the distance between the back of the door and the front cabinet edge.",
                                        default=unit.inch(.125),
                                        unit='LENGTH',
                                        precision=4)
    
    use_buyout_drawer_boxes = bpy.props.BoolProperty(name="Use Buyout Drawer Boxes",
                                        description="Turn this on to use buyout drawer boxes. (Also reduces draw time)",
                                        default=True)    
    
    horizontal_grain_on_drawer_fronts = bpy.props.BoolProperty(name="Horizontal Grain on Drawer Fronts",
                                        description="This rotates the drawer fronts to display horizontal grain on drawer fronts.",
                                        default=False)        
    
    #PULL OPTIONS
    base_pull_location = bpy.props.FloatProperty(name="Base Pull Location",
                                       description="Z Distance from the top of the door edge to the top of the pull",
                                       default=unit.inch(2),
                                       unit='LENGTH') 
    
    tall_pull_location = bpy.props.FloatProperty(name="Tall Pull Location",
                                       description="Z Distance from the bottom of the door edge to the center of the pull",
                                       default=unit.inch(40),
                                       unit='LENGTH')
    
    upper_pull_location = bpy.props.FloatProperty(name="Upper Pull Location",
                                        description="Z Distance from the bottom of the door edge to the bottom of the pull",
                                        default=unit.inch(2),
                                        unit='LENGTH') 
    
    center_pulls_on_drawers = bpy.props.BoolProperty(name="Center Pulls on Drawers",
                                           description="Center pulls on the drawer heights. Otherwise the pull z location is controlled with Drawer Pull From Top",
                                           default=False) 
    
    no_pulls = bpy.props.BoolProperty(name="No Pulls",
                            description="Check this option to turn off pull hardware",
                            default=False) 
    
    pull_from_edge = bpy.props.FloatProperty(name="Pull From Edge",
                                   description="X Distance from the door edge to the pull",
                                   default=unit.inch(1.5),
                                   unit='LENGTH') 
    
    drawer_pull_from_top = bpy.props.FloatProperty(name="Drawer Pull From Top",
                                         description="When Center Pulls on Drawers is off this is the amount from the top of the drawer front to the enter pull",
                                         default=unit.inch(1.5),unit='LENGTH') 
    
    pull_rotation = bpy.props.FloatProperty(name="Pull Rotation",
                                  description="Rotation of pulls on doors",
                                  default=0,
                                  subtype='ANGLE') 

    pull_name = bpy.props.StringProperty(name="Pull Name",default="Test Pull")

bpy.utils.register_class(PROPERTIES_Exterior_Defaults)

class PROPERTIES_Interior_Defaults(bpy.types.PropertyGroup):
    base_adj_shelf_qty = bpy.props.IntProperty(name="Base Adjustable Shelf Quantity",
                                               description="Default number of adjustable shelves for base cabinets",
                                               default=1)
    
    tall_adj_shelf_qty = bpy.props.IntProperty(name="Tall Adjustable Shelf Quantity",
                                               description="Default number of adjustable shelves for tall cabinets",
                                               default=4)
    
    upper_adj_shelf_qty = bpy.props.IntProperty(name="Upper Adjustable Shelf Quantity",
                                                description="Default number of adjustable shelves for upper cabinets",
                                                default=2)
    
    adj_shelf_setback = bpy.props.FloatProperty(name="Adjustable Shelf Setback",
                                                description="This sets the default adjustable shelf setback",
                                                default=unit.inch(.25),
                                                unit='LENGTH')
    
    fixed_shelf_setback = bpy.props.FloatProperty(name="Fixed Shelf Setback",
                                                  description="This sets the default fixed shelf setback",
                                                  default=unit.inch(.25),
                                                  unit='LENGTH')

bpy.utils.register_class(PROPERTIES_Interior_Defaults)

class PROPERTIES_Scene_Properties(bpy.types.PropertyGroup):
    
    main_tabs = bpy.props.EnumProperty(name="Main Tabs",
                                       items=[('DEFAULTS',"Defaults",'Setup the default sizes and options for the products'),
                                              ('MATERIALS',"Materials",'Setup the materials for the project'),
                                              ('OPTIONS',"Options",'Show the available Cabinet & Closet Options')],
                                       default = 'DEFAULTS')
    
    defaults_tabs = bpy.props.EnumProperty(name="Main Tabs",
                                           items=[('SIZES',"Sizes",'Show the default sizes and placement location for cabinets'),
                                                  ('CARCASS',"Carcass",'Show the default carcass settings'),
                                                  ('EXTERIOR',"Exterior",'Show the default door and drawer settings'),
                                                  ('INTERIOR',"Interior",'Show the default interior components settings')],
                                           default = 'SIZES')
    
    #POINTERS
    size_defaults = bpy.props.PointerProperty(name="Sizes",type=PROPERTIES_Cabinet_Sizes)
    carcass_defaults = bpy.props.PointerProperty(name="Carcass Options",type=PROPERTIES_Carcass_Defaults)
    exterior_defaults = bpy.props.PointerProperty(name="Exterior Options",type=PROPERTIES_Exterior_Defaults)
    interior_defaults = bpy.props.PointerProperty(name="Interior Defaults",type=PROPERTIES_Interior_Defaults)
    
    #ENUMERATORS
    expand_base_molding = bpy.props.BoolProperty(name="Expand Base Molding")
    base_molding_category = bpy.props.EnumProperty(name="Base Molding Category",items=enum_base_molding_categories,update=update_base_molding_category)
    base_molding = bpy.props.EnumProperty(name="Base Molding",items=enum_base_molding)
    
    expand_crown_molding = bpy.props.BoolProperty(name="Expand Crown Molding")
    crown_molding_category = bpy.props.EnumProperty(name="Crown Molding Category",items=enum_crown_molding_categories,update=update_crown_molding_category)
    crown_molding = bpy.props.EnumProperty(name="Crown Molding",items=enum_crown_molding)
    
    expand_light_rail_molding = bpy.props.BoolProperty(name="Expand Light Rail Molding")
    light_rail_molding_category = bpy.props.EnumProperty(name="Light Rail Molding Category",items=enum_light_rail_molding_categories,update=update_light_rail_molding_category)
    light_rail_molding = bpy.props.EnumProperty(name="Light Rail Molding",items=enum_light_rail_molding)    
    
    expand_door = bpy.props.BoolProperty(name="Expand Door")
    door_category = bpy.props.EnumProperty(name="Door Category",items=enum_door_categories,update=update_door_category)
    door_style = bpy.props.EnumProperty(name="Door Style",items=enum_door_styles)
    
    expand_core_material = bpy.props.BoolProperty(name="Expand Core Material")
    core_material = bpy.props.EnumProperty(name="Core Material",items=enum_core_materials)    
    
    expand_door_material = bpy.props.BoolProperty(name="Expand Door Material")
    door_material_category = bpy.props.EnumProperty(name="Door Material Category",items=enum_material_categories,update=update_door_material_category)
    door_material = bpy.props.EnumProperty(name="Door Material",items=enum_door_materials)    
    
    expand_exterior_material = bpy.props.BoolProperty(name="Expand Exterior Material")
    exterior_material_category = bpy.props.EnumProperty(name="Exterior Material Category",items=enum_material_categories,update=update_exterior_material_category)
    exterior_material = bpy.props.EnumProperty(name="Exterior Material",items=enum_exterior_materials)        
    
    expand_interior_material = bpy.props.BoolProperty(name="Expand Interior Material")
    interior_material_category = bpy.props.EnumProperty(name="Interior Material Category",items=enum_material_categories,update=update_interior_material_category)
    interior_material = bpy.props.EnumProperty(name="Interior Material",items=enum_interior_materials)     
    
    expand_edge_material = bpy.props.BoolProperty(name="Expand Edge Material")
    edge_material_category = bpy.props.EnumProperty(name="Interior Edge Category",items=enum_material_categories,update=update_edge_material_category)
    edge_material = bpy.props.EnumProperty(name="Edge Material",items=enum_edge_materials)
    
    expand_pull = bpy.props.BoolProperty(name="Expand Pull")
    pull_category = bpy.props.EnumProperty(name="Pull Category",items=enum_pull_categories,update=update_pull_category)
    pull_name = bpy.props.EnumProperty(name="Pull Name",items=enum_pulls)
    
    expand_column = bpy.props.BoolProperty(name="Expand Column")
    column_category = bpy.props.EnumProperty(name="Column Category",items=enum_column_categories,update=update_column_category)
    column_style = bpy.props.EnumProperty(name="Column Style",items=enum_column_styles)
    
class PROPERTIES_Object_Properties(bpy.types.PropertyGroup):
    
    is_cabinet = bpy.props.BoolProperty(name="Is Cabinet",
                                        description="Determines if a product is a cabinet. Used to determine if a product should get crown molding.",
                                        default=False)
    
    is_crown_molding = bpy.props.BoolProperty(name="Is Crown Molding",
                                              description="Used to Delete Molding When Using Auto Add Molding Operator",
                                              default=False)
    
    is_base_molding = bpy.props.BoolProperty(name="Is Base Molding",
                                             description="Used to Delete Molding When Using Auto Add Molding Operator",
                                             default=False)

    is_light_rail_molding = bpy.props.BoolProperty(name="Is Light Rail Molding",
                                                   description="Used to Delete Molding When Using Auto Add Molding Operator",
                                                   default=False)

    is_column = bpy.props.FloatProperty(name="Is Column",
                                        description="Used to determine if an assembly is a column so it can be replaced",
                                        default=False)       

#Namespace for Operators
LIBRARY_NAME_SPACE = "lm_cabinets"

#Functions used to get properties 
def get_scene_props():
    return bpy.context.scene.lm_cabinets 

def get_object_props(obj):
    return obj.lm_cabinets

bpy.utils.register_class(PROPERTIES_Scene_Properties)
bpy.utils.register_class(PROPERTIES_Object_Properties)
bpy.types.Scene.lm_cabinets = bpy.props.PointerProperty(type = PROPERTIES_Scene_Properties)
bpy.types.Object.lm_cabinets = bpy.props.PointerProperty(type = PROPERTIES_Object_Properties)
