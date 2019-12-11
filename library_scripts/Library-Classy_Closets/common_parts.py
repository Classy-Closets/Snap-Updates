import bpy
from os import path
from . import mv_closet_defaults as props_closet
from . import data_pull_hardware
from . import data_drawer_wood
from mv import unit

LIBRARY_DATA_DIR = path.join(path.dirname(bpy.app.binary_path),"data","libraries","Library-Classy_Closets")
ASSEMBLY_DIR = path.join(LIBRARY_DATA_DIR,"Closet Assemblies")
HANGING_RODS_DIR = path.join(ASSEMBLY_DIR,"Hanging Rods")

OVAL_ROD = path.join(HANGING_RODS_DIR,"Oval Rod.blend")
PART_WITH_FRONT_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with Front Edgebanding.blend")
PART_WITH_ALL_EDGES = path.join(ASSEMBLY_DIR,"Part with All Edges.blend")
PART_WITH_NO_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with No Edgebanding.blend")
PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with Edgebanding.blend")
FULL_BACK = path.join(ASSEMBLY_DIR,"Full Back.blend")
FACE = path.join(ASSEMBLY_DIR,"Face.blend")
CORNER_NOTCH_PART = path.join(ASSEMBLY_DIR,"Corner Notch Part.blend")
CHAMFERED_PART = path.join(ASSEMBLY_DIR,"Chamfered Part.blend")
RADIUS_PART = path.join(ASSEMBLY_DIR,"Radius Corner Part with Edgebanding.blend")
CLOSET_PANEL = path.join(ASSEMBLY_DIR,"Closet Panel.blend")
BENDING_PART = path.join(ASSEMBLY_DIR,"Bending Part.blend")
STRAIGHT_COUNTER_TOP = path.join(LIBRARY_DATA_DIR,"Closet Assemblies","Countertop.blend")    
ISLAND_COUNTER_TOP = path.join(LIBRARY_DATA_DIR,"Closet Assemblies","Island Countertop.blend")
FLUTED_PART = path.join(ASSEMBLY_DIR,"Fluted Part.blend")
IB_DRAWER = path.join(ASSEMBLY_DIR,"IB-DR.blend")
IBF_IRONING_BOARD = path.join(ASSEMBLY_DIR,"IBF Ironing Board.blend")
TOSP_SINGLE_HAMPER = path.join(ASSEMBLY_DIR,"TOSP Single.blend")
TOSP_DOUBLE_HAMPER = path.join(ASSEMBLY_DIR,"TOSP Double.blend")
CAM_LOCK = path.join(ASSEMBLY_DIR,"Cam Lock.blend")
WIRE_BASKET = path.join(ASSEMBLY_DIR,"Wire Basket.blend")
SPACER = path.join(ASSEMBLY_DIR,"Spacer.blend")
PULL_OUT_CANVAS_HAMPER = path.join(ASSEMBLY_DIR,"Pull Out Canvas Hamper.blend")
DOUBLE_PULL_OUT_CANVAS_HAMPER = path.join(ASSEMBLY_DIR,"Double Pull Out Canvas Hamper.blend")
ROUND_HANGING_ROD = path.join(ASSEMBLY_DIR,"Hang Rod Round.blend")
OVAL_HANGING_ROD = path.join(ASSEMBLY_DIR,"Hang Rod Oval.blend")
HANGERS = path.join(ASSEMBLY_DIR,"Hangers.blend")
SLIDING_PANTS_RACK = path.join(ASSEMBLY_DIR,"Sliding Pants Rack.blend")
ADJ_MACHINING = path.join(ASSEMBLY_DIR,"Adjustable Shelf Holes.blend")
DECO_100_LIP = path.join(ASSEMBLY_DIR,"Deco Lip 100.blend")
DECO_200_LIP = path.join(ASSEMBLY_DIR,"Deco Lip 200.blend")
DECO_300_LIP = path.join(ASSEMBLY_DIR,"Deco Lip 300.blend")
STEEL_FENCE = path.join(ASSEMBLY_DIR,"Steel Fence.blend")
LINE_BORE = path.join(ASSEMBLY_DIR,"Line Bore Holes.blend")
BUYOUT_DRAWER_BOX = path.join(ASSEMBLY_DIR,"Buyout Drawer Box.blend")

STRAIGHT_CC_COUNTER_TOP = path.join(LIBRARY_DATA_DIR,"Closet Assemblies","CC Countertops","Straight Countertop.blend")  
CORNER_CC_COUNTER_TOP = path.join(LIBRARY_DATA_DIR,"Closet Assemblies","CC Countertops","Corner Countertop.blend")  

OBJECT_DIR = path.join(LIBRARY_DATA_DIR,"Closet Objects")
HANGING_ROD_CUPS_DIR = path.join(OBJECT_DIR,"Rod Cups")

OVAL_ROD_CUP = path.join(HANGING_ROD_CUPS_DIR,"Oval Rod Cup.blend")
VALET_ROD = path.join(OBJECT_DIR,"Valet Rod.blend")
VALET_ROD_2 = path.join(OBJECT_DIR,"Valet Rod 2.blend")
TIE_AND_BELT_RACK = path.join(OBJECT_DIR,"Tie and Belt Rack.blend")
ROSETTE = path.join(OBJECT_DIR,"Rosette.blend")
ROD_SUPPORT = path.join(OBJECT_DIR,"Rod Support.blend")
SHELF_SUPPORT = path.join(OBJECT_DIR,"Shelf Support 10x12.blend")

def add_accessory_panel(assembly):
    accessory_panel = assembly.add_assembly(PART_WITH_EDGEBANDING)
    accessory_panel.set_name("Accessory Panel")
    accessory_panel.cutpart("Panel")
    accessory_panel.edgebanding('Edge',l1 = True)
    return accessory_panel

def add_panel(assembly):
    panel = assembly.add_assembly(CLOSET_PANEL)
    props = props_closet.get_object_props(panel.obj_bp)
    props.is_panel_bp = True
    panel.set_name("Panel")
    panel.add_prompt(name="Is Left End Panel",prompt_type='CHECKBOX',value=False,tab_index=0)
    panel.add_prompt(name="Is Right End Panel",prompt_type='CHECKBOX',value=False,tab_index=0)
    panel.add_prompt(name="Left Depth",prompt_type='DISTANCE',value=0,tab_index=0)
    panel.add_prompt(name="Right Depth",prompt_type='DISTANCE',value=0,tab_index=0)
    panel.add_prompt(name="Stop Drilling Bottom Left",prompt_type='DISTANCE',value=0,tab_index=0)
    panel.add_prompt(name="Stop Drilling Top Left",prompt_type='DISTANCE',value=0,tab_index=0)
    panel.add_prompt(name="Stop Drilling Bottom Right",prompt_type='DISTANCE',value=0,tab_index=0)
    panel.add_prompt(name="Stop Drilling Top Right",prompt_type='DISTANCE',value=0,tab_index=0)
    panel.add_prompt(name="Place Hanging Hardware On Right",prompt_type='CHECKBOX',value=False,tab_index=0)
    panel.add_prompt(name="CatNum",prompt_type='NUMBER',value=0,tab_index=0)
    panel.cutpart("Panel")
    panel.edgebanding("Edge",l2 = True)
    panel.edgebanding("Edge_2",w2 = True,w1 = True)
    panel.set_material_pointers("Closet_Part_Edges","FrontBackEdge")
    panel.set_material_pointers("Closet_Part_Edges_Secondary","TopBottomEdge")
    for child in panel.obj_bp.children:
        if child.cabinetlib.type_mesh == 'CUTPART':
            child.mv.use_multiple_edgeband_pointers = True
    return panel

def add_shelf(assembly):
    defaults = props_closet.get_scene_props().closet_defaults
    shelf = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_shelf_bp = True
    shelf.set_name("Shelf")
    shelf.add_prompt(name="CatNum",prompt_type='NUMBER',value=0,tab_index=0)
    shelf.add_prompt(name="Shelf Pin Qty",prompt_type='QUANTITY',value=0,tab_index=0)
    shelf.add_prompt(name="Cam Qty",prompt_type='QUANTITY',value=0,tab_index=0)
    shelf.add_prompt(name="Is Locked Shelf",prompt_type='CHECKBOX',value=False,tab_index=0)
    shelf.add_prompt(name="Adj Shelf Clip Gap",prompt_type='DISTANCE',value=defaults.adj_shelf_clip_gap,tab_index=0)
    shelf.add_prompt(name="Adj Shelf Setback",prompt_type='DISTANCE',value=defaults.adj_shelf_setback,tab_index=0)
    shelf.add_prompt(name="Locked Shelf Setback",prompt_type='DISTANCE',value=defaults.locked_shelf_setback,tab_index=0)
    shelf.add_prompt(name="Drill On Top",prompt_type='CHECKBOX',value=False,tab_index=0)
    shelf.add_prompt(name="Remove Left Holes",prompt_type='CHECKBOX',value=False,tab_index=0)
    shelf.add_prompt(name="Remove Right Holes",prompt_type='CHECKBOX',value=False,tab_index=0)
    Is_Locked_Shelf = shelf.get_var('Is Locked Shelf')
    shelf.x_rot(value = 0)
    shelf.y_rot(value = 0)
    shelf.z_rot(value = 0)    
    shelf.prompt('Shelf Pin Qty','IF(Is_Locked_Shelf,0,4)',[Is_Locked_Shelf])
    shelf.prompt('Cam Qty','IF(Is_Locked_Shelf,4,0)',[Is_Locked_Shelf])      
    shelf.prompt('CatNum','IF(Is_Locked_Shelf,1002,1001)',[Is_Locked_Shelf])
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l2 = True)
    return shelf
            
def add_glass_shelf(assembly):
    shelf = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    shelf.add_prompt(name="Shelf Pin Qty",prompt_type='QUANTITY',value=4,tab_index=0)
    for child in shelf.obj_bp.children:
        if child.type == 'MESH':
            child.cabinetlib.type_mesh = 'BUYOUT'    
    shelf.material("Glass")
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_glass_shelf_bp = True
    return shelf

def add_sliding_shelf(assembly):
    shelf = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_sliding_shelf_bp = True
    shelf.obj_bp.mv.comment_2 = "1013"
    shelf.set_name("Sliding Shelf")
    shelf.x_rot(value = 0)
    shelf.y_rot(value = 0)
    shelf.z_rot(value = 0)
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l2 = True)
    return shelf

def add_l_shelf(assembly):
    shelf = assembly.add_assembly(CORNER_NOTCH_PART)
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_l_shelf_bp = True
    shelf.obj_bp.mv.comment_2 = "1525"
    shelf.set_name("L Shelf")
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l1 = True)  
    return shelf

def add_hanging_rod_cup(assembly):
    cup = assembly.add_object(OVAL_ROD_CUP)
    cup.obj_bp.mv.comment_2 = "1015"
    return cup

def add_rod_support(assembly):
    rod_support = assembly.add_assembly(ROD_SUPPORT)
    rod_support.obj_bp.mv.comment_2 = "1015"
    return rod_support

def add_shelf_support(assembly):
    shelf_support = assembly.add_assembly(SHELF_SUPPORT)
    shelf_support.obj_bp.mv.comment_2 = "1015"
    return shelf_support

def add_hanging_rod(assembly):
    rod = assembly.add_assembly(OVAL_ROD)
    props = props_closet.get_object_props(rod.obj_bp)
    props.is_hanging_rod = True
    rod.obj_bp.mv.comment_2 = "1015"
    rod.solid_stock("Oval Hanging Rod")
    closet_options = bpy.context.scene.lm_closets.closet_options
    rod.obj_bp.mv.name_object = closet_options.rods_name
    return rod

def add_hanging_rail(assembly):
    rail = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    props = props_closet.get_object_props(assembly.obj_bp)
    rail.obj_bp.mv.comment_2 = "1015"
    props.is_hanging_rail_bp = True
    rail.cutpart("Hanging_Rail")
    rail.set_name("Hanging Rail")
    return rail

def add_drawer_side(assembly):
    side = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    side.obj_bp.mv.comment_2 = "1031"
    side.set_name("Drawer Side")
    side.cutpart("Drawer_Part")
    side.edgebanding('Drawer_Box_Edge',l1 = True)
    props = props_closet.get_object_props(side.obj_bp)
    props.is_drawer_side_bp = True
    return side

def add_drawer_back(assembly):
    drawer_back = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    drawer_back.obj_bp.mv.comment_2 = "1032"
    drawer_back.set_name("Drawer Back")
    drawer_back.cutpart("Drawer_Back")
    drawer_back.edgebanding('Drawer_Box_Edge',l1 = True)
    props = props_closet.get_object_props(drawer_back.obj_bp)
    props.is_drawer_back_bp = True
    return drawer_back
                
def add_drawer_sub_front(assembly):
    front_back = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    front_back.obj_bp.mv.comment_2 = "1029"
    front_back.set_name("Drawer Sub Front")
    front_back.cutpart("Drawer_Part")
    front_back.edgebanding('Drawer_Box_Edge',l1 = True)
    props = props_closet.get_object_props(front_back.obj_bp)
    props.is_drawer_sub_front_bp = True
    return front_back

def add_drawer_bottom(assembly):
    bottom = assembly.add_assembly(PART_WITH_NO_EDGEBANDING)
    bottom.obj_bp.mv.comment_2 = "1030"
    bottom.set_name("Drawer Bottom")
    bottom.cutpart("Drawer_Bottom")
    props = props_closet.get_object_props(bottom.obj_bp)
    props.is_drawer_bottom_bp = True
    return bottom

def add_tie_drawer_top_or_bottom(assembly):
    top = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    top.cutpart("Drawer_Part")
    top.edgebanding('Drawer_Box_Edge',l1 = True)

def add_tie_drawer_division(assembly):
    division = assembly.add_assembly(PART_WITH_NO_EDGEBANDING)
    division.set_name("Tie Drawer Division")
    division.cutpart("Drawer_Part")
        
def add_angle_shelf(assembly):
    shelf = assembly.add_assembly(CHAMFERED_PART)
    shelf.obj_bp.mv.comment_2 = "1520"
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_angle_shelf_bp = True
    shelf.set_name("Angle Shelf")
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l1 = True)  
    return shelf

def add_radius_shelf(assembly):
    shelf = assembly.add_assembly(RADIUS_PART)
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_radius_shelf_bp = True
    shelf.set_name("Radius Shelf")
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l1 = True)
    return shelf

def add_plant_on_top(assembly):
    shelf = assembly.add_assembly(PART_WITH_ALL_EDGES)
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_plant_on_top_bp = True    
    shelf.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=False,tab_index=0)
    shelf.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=False,tab_index=0)    
    shelf.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=False,tab_index=0)  
    shelf.set_name("Top")
    shelf.x_rot(value = 0)
    shelf.y_rot(value = 0)
    shelf.z_rot(value = 0)        
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l1 = True,l2 = True,w1 = True,w2 = True)
    shelf.set_material_pointers("Closet_Part_Edges","Edgebanding")
    shelf.set_material_pointers("Core","LeftEdge")
    shelf.set_material_pointers("Core","RightEdge")
    shelf.set_material_pointers("Core","BackEdge")
    for child in shelf.obj_bp.children:
        if child.cabinetlib.type_mesh == 'CUTPART':
            child.mv.use_multiple_edgeband_pointers = True    
    return shelf

def add_flat_crown(assembly):
    shelf = assembly.add_assembly(PART_WITH_ALL_EDGES)
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_crown_molding = True    
    shelf.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=False,tab_index=0)
    shelf.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=False,tab_index=0)    
    shelf.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=False,tab_index=0)  
    shelf.set_name("Flat Crown")
    shelf.x_rot(value = 90)
    shelf.y_rot(value = 0)
    shelf.z_rot(value = 0)        
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l1 = True,l2 = True,w1 = True,w2 = True)
    shelf.set_material_pointers("Closet_Part_Edges_Secondary","Edgebanding")
    shelf.set_material_pointers("Core","LeftEdge")
    shelf.set_material_pointers("Core","RightEdge")
    shelf.set_material_pointers("Core","BackEdge")
    for child in shelf.obj_bp.children:
        if child.cabinetlib.type_mesh == 'CUTPART':
            child.mv.use_multiple_edgeband_pointers = True    
    return shelf

def add_hpl_top(assembly):
    shelf = assembly.add_assembly(PART_WITH_ALL_EDGES)
    props = props_closet.get_object_props(shelf.obj_bp)
    props.is_hpl_top_bp = True    
    for child in shelf.obj_bp.children:
        if child.type == 'MESH':
            child.cabinetlib.type_mesh = 'BUYOUT'      
    shelf.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=False,tab_index=0)
    shelf.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=False,tab_index=0)    
    shelf.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=False,tab_index=0)  
    shelf.set_name("Top")
    shelf.x_rot(value = 0)
    shelf.y_rot(value = 0)
    shelf.z_rot(value = 0)    
    shelf.edgebanding('Edge',l1 = True,l2 = True,w1 = True,w2 = True)
    shelf.material("Countertop_Surface")
    for child in shelf.obj_bp.children:
        if child.cabinetlib.type_mesh == 'CUTPART':
            child.mv.use_multiple_edgeband_pointers = True    
    return shelf

def add_door_pull(assembly):
    pull_hardware = data_pull_hardware.Standard_Pull()
    pull_hardware.draw()
    pull_hardware.obj_bp.mv.comment_2 = "1015"
    pull_hardware.obj_bp.parent = assembly.obj_bp
    pull_hardware.set_name("Pull")
    return pull_hardware

def add_drawer_pull(assembly):
    pull_hardware = data_pull_hardware.Standard_Pull()
    pull_hardware.draw()
    pull_hardware.obj_bp.mv.comment_2 = "1015"
    pull_hardware.obj_bp.parent = assembly.obj_bp
    pull_hardware.set_name("Pull")
    return pull_hardware

def add_drawer(assembly):
    scene_props = props_closet.get_scene_props()
    if scene_props.closet_defaults.use_buyout_drawers:
        drawer = assembly.add_assembly(BUYOUT_DRAWER_BOX)
        drawer.material("Drawer_Box_Surface")
        drawer.obj_bp.mv.comment_2 = "1014"
    else:
        drawer = data_drawer_wood.Wood_Drawer_Box()
        drawer.draw()
        drawer.obj_bp.parent = assembly.obj_bp
        drawer.obj_bp.mv.comment_2 = "1014"
    return drawer

def add_line_bore_holes(assembly):
    holes = assembly.add_assembly(LINE_BORE)    
    return holes

def add_slanted_shoe_shelf(assembly):
    slanted_shelf = assembly.add_assembly(PART_WITH_EDGEBANDING)
    slanted_shelf.obj_bp.mv.comment_2 = "1655"
    slanted_shelf.set_name("Slanted Shoe Shelf")
    slanted_shelf.cutpart("Shelf")
    slanted_shelf.edgebanding('Edge',l1 = True, w1 = True, l2 = True, w2 = True)
    slanted_shelf.add_prompt(name="Shelf Pin Qty",prompt_type='QUANTITY',value=2,tab_index=0)
    slanted_shelf.add_prompt(name="Cam Qty",prompt_type='QUANTITY',value=2,tab_index=0)
    props = props_closet.get_object_props(slanted_shelf.obj_bp)
    props.is_slanted_shelf_bp = True
    return slanted_shelf
    
def add_shelf_lip(assembly):
    shelf_lip = assembly.add_assembly(PART_WITH_EDGEBANDING)
    shelf_lip.set_name("Shelf Lip")
    shelf_lip.cutpart("Shelf")
    shelf_lip.edgebanding('Edge',l1 = True, w1 = True, l2 = True, w2 = True)    
    props = props_closet.get_object_props(shelf_lip.obj_bp)
    props.is_shelf_lip_bp = True
    return shelf_lip

def add_wine_rack_support(assembly):
    support = assembly.add_assembly(PART_WITH_EDGEBANDING)
    support.set_name("Support")
    support.cutpart("Shelf")
    support.edgebanding('Edge',l1 = True)
    return support
    
def add_deco_shelf_lip_1(assembly):
    deco_shelf_lip = assembly.add_assembly(DECO_100_LIP)
    deco_shelf_lip.obj_bp.mv.comment_2 = "1016"
    deco_shelf_lip.set_name("Deco Shelf Lip #1")
    deco_shelf_lip.material("Closet_Part_Surfaces")
    props = props_closet.get_object_props(deco_shelf_lip.obj_bp)
    props.is_deco_shelf_lip_bp = True
    return deco_shelf_lip
    
def add_deco_shelf_lip_2(assembly):
    deco_shelf_lip = assembly.add_assembly(DECO_200_LIP)
    deco_shelf_lip.obj_bp.mv.comment_2 = "1016"
    deco_shelf_lip.set_name("Deco Shelf Lip #2")
    deco_shelf_lip.material("Closet_Part_Surfaces")
    props = props_closet.get_object_props(deco_shelf_lip.obj_bp)
    props.is_deco_shelf_lip_bp = True
    return deco_shelf_lip

def add_deco_shelf_lip_3(assembly):
    deco_shelf_lip = assembly.add_assembly(DECO_300_LIP)
    deco_shelf_lip.obj_bp.mv.comment_2 = "1016"
    deco_shelf_lip.set_name("Deco Shelf Lip #3")
    deco_shelf_lip.material("Closet_Part_Surfaces")
    props = props_closet.get_object_props(deco_shelf_lip.obj_bp)
    props.is_deco_shelf_lip_bp = True
    return deco_shelf_lip
    
def add_shelf_fence(assembly):
    steel_fence = assembly.add_assembly(STEEL_FENCE)
    steel_fence.obj_bp.mv.comment_2 = "1016"
    steel_fence.set_name("Steel Fence")
    steel_fence.material("Pull_Finish")
    props = props_closet.get_object_props(steel_fence.obj_bp)
    props.is_shelf_fence_bp = True
    return steel_fence
            
def add_visual_shelf_holes(assembly):
    shelf_holes = assembly.add_assembly(ADJ_MACHINING)
    shelf_holes.set_name("Adjustable Shelf Holes")
    return shelf_holes
    
def add_divider(assembly):
    divider = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    divider.obj_bp.mv.comment_2 = "1027"
    divider.set_name("Divider")
    divider.cutpart("Shoe_Cubby")
    divider.edgebanding("Edge",l1 = True)
    props = props_closet.get_object_props(divider.obj_bp)
    props.is_divider_bp = True
    return divider
        
def add_division(assembly):
    division = assembly.add_assembly(PART_WITH_EDGEBANDING)
    division.set_name("Panel")
    division.cutpart("Panel")
    division.edgebanding("Edge",l2 = True)
    props = props_closet.get_object_props(division.obj_bp)
    props.is_division_bp = True    
    return division

def add_applied_top(assembly):
    top = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    top.obj_bp.mv.comment_2 = "1024"
    props = props_closet.get_object_props(top.obj_bp)
    props.is_shelf_bp = True
    top.set_name("Top")
    top.cutpart("Shelf")
    top.edgebanding("Edge",l2 = True)    
    return top

def add_filler(assembly):
    filler = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    filler.obj_bp.mv.comment_2 = "1036"
    props = props_closet.get_object_props(filler.obj_bp)
    props.is_filler_bp = True
    filler.set_name("Filler")
    filler.cutpart("Panel")
    return filler

def add_toe_kick(assembly):
    kick = assembly.add_assembly(PART_WITH_NO_EDGEBANDING)
    props = props_closet.get_object_props(kick.obj_bp)
    props.is_toe_kick_bp = True
    kick.set_name("Toe Kick")
    kick.cutpart("Toe_Kick")
    return kick

def add_toe_kick_radius(assembly):
    kick = assembly.add_assembly(BENDING_PART)
    props = props_closet.get_object_props(kick.obj_bp)
    props.is_toe_kick_bp = True
    kick.set_name("Toe Kick")
    kick.cutpart("Toe_Kick")
    return kick

def add_door_striker(assembly):
    cleat = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    cleat.obj_bp.mv.comment_2 = "1041"
    props = props_closet.get_object_props(cleat.obj_bp)
    props.is_door_striker_bp = True
    cleat.set_name("Cleat")
    cleat.cutpart("Shelf")
    cleat.edgebanding("Edge",l1 = True)    
    return cleat

def add_cleat(assembly):
    cleat = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    cleat.obj_bp.mv.comment_2 = "1008"
    props = props_closet.get_object_props(cleat.obj_bp)
    props.is_cleat_bp = True
    cleat.set_name("Cleat")
    cleat.cutpart("Shelf")
    cleat.edgebanding("Edge_2",l1 = True)    
    return cleat

def add_shelf_and_rod_cleat(assembly):
    cleat = assembly.add_assembly(PART_WITH_FRONT_EDGEBANDING)
    props = props_closet.get_object_props(cleat.obj_bp)
    props.is_shelf_and_rod_cleat_bp = True
    cleat.set_name("Cleat")
    cleat.cutpart("Shelf")
    cleat.edgebanding("Edge",l1 = True,w2 = True)    
    return cleat

def add_shelf_rod_cleat_fe(assembly):
    cleat = assembly.add_assembly(CHAMFERED_PART)
    props = props_closet.get_object_props(cleat.obj_bp)
    props.is_shelf_and_rod_fe_cleat_bp = True
    cleat.set_name("Cleat FE")
    cleat.cutpart("Shelf")
    cleat.edgebanding("Edge",l2 = True,w2 = True)    
    return cleat

def add_back(assembly):
    backing = assembly.add_assembly(FULL_BACK)
    backing.obj_bp.mv.comment_2 = "1037"
    props = props_closet.get_object_props(backing.obj_bp)
    props.is_back_bp = True
    backing.set_name("Back")
    backing.cutpart("Back")
    return backing

def add_frame(assembly):
    frame = assembly.add_assembly(PART_WITH_EDGEBANDING)
    frame.set_name("Frame")
    frame.cutpart("Panel")
    frame.edgebanding("Edge",l2 = True)
    return frame

def add_island_countertop(assembly):
    island_ctop = assembly.add_assembly(ISLAND_COUNTER_TOP) 
    props = props_closet.get_object_props(island_ctop.obj_bp)
    props.is_countertop_bp = True
    island_ctop.set_name("Countertop Deck")
    island_ctop.material("Countertop_Surface")
    return island_ctop

def add_countertop(assembly):
    ctop = assembly.add_assembly(STRAIGHT_COUNTER_TOP)
    ctop.obj_bp.mv.comment_2 = "1605" 
    props = props_closet.get_object_props(ctop.obj_bp)
    props.is_countertop_bp = True
    ctop.set_name("Countertop Deck")
    ctop.material("Countertop_Surface")
    return ctop

def add_cc_countertop(assembly):
    ctop = assembly.add_assembly(STRAIGHT_CC_COUNTER_TOP)
    ctop.obj_bp.mv.comment_2 = "1605" 
    props = props_closet.get_object_props(ctop.obj_bp)
    props.is_countertop_bp = True
    ctop.set_name("Countertop Deck")
    ctop.material("Countertop_Surface")
    return ctop

def add_cc_corner_countertop(assembly):
    ctop = assembly.add_assembly(CORNER_CC_COUNTER_TOP)
    ctop.obj_bp.mv.comment_2 = "1605" 
    props = props_closet.get_object_props(ctop.obj_bp)
    props.is_countertop_bp = True
    ctop.set_name("Countertop Deck")
    ctop.material("Countertop_Surface")
    return ctop

def add_door(assembly):
    door = assembly.add_assembly(FACE)
    door.set_name("Door")
    door.cutpart("Slab_Door")
    door.edgebanding('Edge',l1 = True, w1 = True, l2 = True, w2 = True)
    door.add_prompt(name="CatNum",prompt_type='NUMBER',value=0,tab_index=0)
    door.add_prompt(name="Door Type",prompt_type='COMBOBOX',value=0,tab_index=0,items=['Base','Tall','Upper'],columns=4)
    door.add_prompt(name="Door Swing",prompt_type='COMBOBOX',value=0,tab_index=0,items=['Left','Right','Top','Bottom'],columns=4)
    door.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=False,tab_index=0)
    door.obj_bp.mv.is_cabinet_door = True
    obj_props = props_closet.get_object_props(door.obj_bp)
    obj_props.is_door_bp = True
    obj_props.door_type = 'FLAT'
    return door

def add_ironing_board_door_front(assembly):
    door = assembly.add_assembly(FACE)
    door.set_name("Door")
    door.cutpart("Slab_Door")
    door.edgebanding('Edge',l1 = True, w1 = True, l2 = True, w2 = True)
    door.add_prompt(name="Door Type",prompt_type='COMBOBOX',value=0,tab_index=0,items=['Base','Tall','Upper'],columns=4)
    door.add_prompt(name="Door Swing",prompt_type='COMBOBOX',value=0,tab_index=0,items=['Left','Right','Top','Bottom'],columns=4)
    door.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=False,tab_index=0)
    door.obj_bp.mv.is_cabinet_door = True
    obj_props = props_closet.get_object_props(door.obj_bp)
    obj_props.is_ironing_board_door_front_bp = True
    obj_props.door_type = 'FLAT'
    return door

def add_drawer_front(assembly):
    front = assembly.add_assembly(FACE)
    front.obj_bp.mv.comment_2 = "1007"
    front.set_name("Drawer Front")
    front.cutpart("Slab_Drawer_Front")
    front.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=False,tab_index=0)
    front.add_prompt(name="Use Double Pulls",prompt_type='CHECKBOX',value=False,tab_index=0)
    front.add_prompt(name="Center Pulls on Drawers",prompt_type='CHECKBOX',value=False,tab_index=0)
    front.add_prompt(name="Drawer Pull From Top",prompt_type='DISTANCE',value=0,tab_index=0)
    front.edgebanding('Edge',l1 = True, w1 = True, l2 = True, w2 = True)
    front.obj_bp.mv.is_cabinet_drawer_front = True
    front.obj_bp.mv.comment = "Melamine Drawer Face"
    obj_props = props_closet.get_object_props(front.obj_bp)
    obj_props.door_type = 'FLAT'
    obj_props.is_drawer_front_bp = True
    return front

def add_hamper_front(assembly):
    front = assembly.add_assembly(FACE)
    front.obj_bp.mv.comment_2 = "1044"     
    front.set_name("Hamper Door")
    front.cutpart("Slab_Drawer_Front")
    front.edgebanding('Edge',l1 = True, w1 = True, l2 = True, w2 = True)
    front.obj_bp.mv.is_cabinet_door = True
    props = props_closet.get_object_props(front.obj_bp)
    props.is_hamper_front_bp = True   
    return front        

def add_wire_basket(assembly):
    basket = assembly.add_assembly(WIRE_BASKET)
    basket.obj_bp.mv.comment_2 = "1016"
    basket.set_name("Wire Basket")
    basket.material('Wire_Basket')
    props = props_closet.get_object_props(basket.obj_bp)
    props.is_basket_bp = True
    return basket

def add_wire_hamper(assembly):
    hamper = assembly.add_assembly(WIRE_BASKET)
    hamper.obj_bp.mv.comment_2 = "1016"
    hamper.set_name("Hamper Basket")
    hamper.material('Wire_Basket')
    props = props_closet.get_object_props(hamper.obj_bp)
    props.is_hamper_bp = True
    return hamper

def add_single_canvas_hamper(assembly):
    hamper = assembly.add_assembly(TOSP_SINGLE_HAMPER)
    hamper.obj_bp.mv.comment_2 = "1016"
    hamper.set_name("Single Canvas Hamper")
    props = props_closet.get_object_props(hamper.obj_bp)
    props.is_hamper_bp = True    
    return hamper

def add_double_canvas_hamper(assembly):
    hamper = assembly.add_assembly(TOSP_DOUBLE_HAMPER)
    hamper.obj_bp.mv.comment_2 = "1016"
    hamper.set_name("Double Canvas Hamper")
    props = props_closet.get_object_props(hamper.obj_bp)
    props.is_hamper_bp = True
    return hamper

def add_single_pull_out_canvas_hamper(assembly):
    hamper = assembly.add_assembly(PULL_OUT_CANVAS_HAMPER)
    hamper.obj_bp.mv.comment_2 = "1016"
    hamper.set_name("Single Pull Out Canvas Hamper")
    props = props_closet.get_object_props(hamper.obj_bp)
    props.is_hamper_bp = True    
    return hamper

def add_double_pull_out_canvas_hamper(assembly):
    hamper = assembly.add_assembly(DOUBLE_PULL_OUT_CANVAS_HAMPER)
    hamper.obj_bp.mv.comment_2 = "1016"
    hamper.set_name("Double Pull Out Canvas Hamper")
    props = props_closet.get_object_props(hamper.obj_bp)
    props.is_hamper_bp = True
    return hamper

def add_round_hanging_rod(assembly):
    opts = props_closet.get_scene_props().closet_options
    rod = assembly.add_assembly(ROUND_HANGING_ROD)
    rod.obj_bp.mv.comment_2 = "1015"
    rod.set_name(opts.rods_name)
    rod.solid_stock("Oval Hanging Rod")
    rod.material("Rod_Finish")
    rod.z_loc(value=unit.inch(1)) # SET MATERIAL THICKNESS
    props = props_closet.get_object_props(rod.obj_bp)
    props.is_hanging_rod = True
    return rod

def add_oval_hanging_rod(assembly):
    opts = props_closet.get_scene_props().closet_options    
    rod = assembly.add_assembly(OVAL_HANGING_ROD)
    rod.obj_bp.mv.comment_2 = "1015"
    rod.set_name(opts.rods_name)
    rod.solid_stock("Oval Hanging Rod")
    rod.material("Rod_Finish")
    rod.y_dim(value = unit.inch(.5))
    rod.z_dim(value = unit.inch(-1)) # SET MATERIAL THICKNESS
    props = props_closet.get_object_props(rod.obj_bp)
    props.is_hanging_rod = True
    return rod

def add_hangers(assembly):
    hangers = assembly.add_assembly(HANGERS)
    hangers.set_name("Hangers")
    return hangers

def add_spacer(assembly):
    spacer = assembly.add_assembly(SPACER)
    spacer.set_name("Spacer")
    props = props_closet.get_object_props(spacer.obj_bp)
    props.is_spacer_bp = True   
    return spacer
        
def add_lock(assembly):
    lock = assembly.add_assembly(CAM_LOCK)
    lock.set_name("Lock")
    lock.material('Chrome')   
    return lock

def add_fluted_molding(assembly):
    flute = assembly.add_assembly(FLUTED_PART)
    props = props_closet.get_object_props(flute.obj_bp)
    props.is_fluted_filler_bp = True
    flute.set_name("Fluted Part")
    flute.material("Closet_Part_Surfaces")
    return flute

def add_ironing_board_drawer(assembly):
    IBDR_1 = assembly.add_assembly(IB_DRAWER)
    IBDR_1.set_name("IB-DR")
    return IBDR_1

def add_ironing_board_door(assembly):
    IBF_1 = assembly.add_assembly(IBF_IRONING_BOARD)
    IBF_1.set_name("IBF")
    return IBF_1

def add_sliding_pants_rack(assembly):
    pants_rack = assembly.add_assembly(SLIDING_PANTS_RACK)
    pants_rack.set_name("Sliding Panels Rack")
    return pants_rack

def add_rosette(assembly):
    rosette = assembly.add_object(ROSETTE)
    return rosette

def add_section_opening(assembly):
    opening = assembly.add_opening()
    props = props_closet.get_object_props(opening.obj_bp)
    props.opening_type = "SECTION"
    opening.set_name("Opening")
    opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
    opening.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    opening.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    opening.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    opening.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    return opening

def add_opening(assembly):
    opening = assembly.add_opening()
    opening.set_name("Opening")
    opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
    opening.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    opening.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    opening.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    opening.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    return opening


