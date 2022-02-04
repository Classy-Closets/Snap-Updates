from os import path
import math

import bpy

from snap.libraries.closets import closet_props
from snap.libraries.closets import closet_paths
from snap.libraries.closets import closet_utils
from ..data import data_pull_hardware
from ..data import data_drawer_wood
from snap import sn_unit
from snap import sn_types


LIBRARY_DATA_DIR = path.join(
    path.dirname(bpy.app.binary_path),
    "data",
    "libraries",
    "Library-Classy_Closets")
ASSEMBLY_DIR = closet_paths.get_closet_assemblies_path()
OBJECT_DIR = closet_paths.get_closet_objects_path()

HANGING_RODS_DIR = path.join(ASSEMBLY_DIR, "Hanging Rods")
#OVAL_ROD = path.join(HANGING_RODS_DIR, "Oval Rod.blend")

# UPDATED
PART_WITH_FRONT_EDGEBANDING = path.join(closet_paths.get_closet_assemblies_path(), "Part with Front Edgebanding.blend")
PART_WITH_ALL_EDGES = path.join(ASSEMBLY_DIR, "Part with All Edges.blend")
MITERED_PART_WITH_ALL_EDGES = path.join(ASSEMBLY_DIR, "Mitered Part with All Edges.blend")
PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR, "Part with Edgebanding.blend")
PART_WITH_NO_EDGEBANDING = path.join(ASSEMBLY_DIR, "Part with No Edgebanding.blend")
CLOSET_PANEL = path.join(closet_paths.get_closet_assemblies_path(), "Closet Panel.blend")
ISLAND_PANEL = path.join(closet_paths.get_closet_assemblies_path(), "Island Panel.blend")
FACE = path.join(closet_paths.get_closet_assemblies_path(), "Face.blend")
FULL_BACK = path.join(closet_paths.get_closet_assemblies_path(), "Full Back.blend")
ROUND_HANGING_ROD = path.join(closet_paths.get_closet_assemblies_path(), "Hang Rod Round.blend")
OVAL_HANGING_ROD = path.join(closet_paths.get_closet_assemblies_path(), "Hang Rod Oval.blend")
HANGERS = path.join(closet_paths.get_closet_assemblies_path(), "Hangers.blend")
CAM_LOCK = path.join(closet_paths.get_closet_assemblies_path(), "Cam Lock.blend")
CORNER_NOTCH_PART = path.join(ASSEMBLY_DIR, "Corner Notch Part.blend")
CHAMFERED_PART = path.join(ASSEMBLY_DIR, "Chamfered Part.blend")
WIRE_BASKET = path.join(ASSEMBLY_DIR, "Wire Basket.blend")
LINE_BORE = path.join(ASSEMBLY_DIR, "Line Bore Holes.blend")
STRAIGHT_COUNTER_TOP = path.join(ASSEMBLY_DIR, "Countertop.blend")
BACKSPLASH_PART = path.join(ASSEMBLY_DIR, "Backsplash.blend")
CORNER_CC_COUNTER_TOP = path.join(ASSEMBLY_DIR, "Corner Countertop.blend")
DECO_100_LIP = path.join(ASSEMBLY_DIR, "Deco Lip 100.blend")
DECO_200_LIP = path.join(ASSEMBLY_DIR, "Deco Lip 200.blend")
DECO_300_LIP = path.join(ASSEMBLY_DIR, "Deco Lip 300.blend")
STEEL_FENCE = path.join(ASSEMBLY_DIR, "Steel Fence.blend")
SLIDING_PANTS_RACK = path.join(ASSEMBLY_DIR, "Sliding Pants Rack.blend")
PULL_OUT_CANVAS_HAMPER = path.join(ASSEMBLY_DIR, "Pull Out Canvas Hamper.blend")
DOUBLE_PULL_OUT_CANVAS_HAMPER = path.join(ASSEMBLY_DIR, "Double Pull Out Canvas Hamper.blend")
PLASTIC_LEG = path.join(ASSEMBLY_DIR, "Plastic Leg.blend")
METAL_LEG = path.join(ASSEMBLY_DIR, "Metal Leg.blend")

# UPDATED

RADIUS_PART = path.join(ASSEMBLY_DIR, "Radius Corner Part with Edgebanding.blend")
BENDING_PART = path.join(ASSEMBLY_DIR, "Bending Part.blend")
ISLAND_COUNTER_TOP = path.join(LIBRARY_DATA_DIR, "Closet Assemblies", "Island Countertop.blend")
FLUTED_PART = path.join(ASSEMBLY_DIR, "Fluted Part.blend")
IB_DRAWER = path.join(ASSEMBLY_DIR, "IB-DR.blend")
IBF_IRONING_BOARD = path.join(ASSEMBLY_DIR, "IBF Ironing Board.blend")
TOSP_SINGLE_HAMPER = path.join(ASSEMBLY_DIR, "TOSP Single.blend")
TOSP_DOUBLE_HAMPER = path.join(ASSEMBLY_DIR, "TOSP Double.blend")
SPACER = path.join(ASSEMBLY_DIR, "Spacer.blend")
ADJ_MACHINING = path.join(ASSEMBLY_DIR, "Adjustable Shelf Holes.blend")
BUYOUT_DRAWER_BOX = path.join(ASSEMBLY_DIR, "Buyout Drawer Box.blend")

# OBJECTS
HANGING_ROD_CUPS_DIR = path.join(OBJECT_DIR, "Rod Cups")
OVAL_ROD_CUP = path.join(HANGING_ROD_CUPS_DIR, "Oval Rod Cup.blend")
VALET_ROD = path.join(OBJECT_DIR, "Valet Rod.blend")
VALET_ROD_2 = path.join(OBJECT_DIR, "Valet Rod 2.blend")
TIE_AND_BELT_RACK = path.join(OBJECT_DIR, "Tie and Belt Rack.blend")
ROSETTE = path.join(OBJECT_DIR, "Rosette.blend")
ROD_SUPPORT = path.join(OBJECT_DIR, "Rod Support.blend")
SHELF_SUPPORT = path.join(OBJECT_DIR, "Shelf Support 10x12.blend")


# Updated
def add_panel(assembly, island_panel=False):
    if island_panel:
        panel = sn_types.Part(assembly.add_assembly_from_file(ISLAND_PANEL))
    else:
        panel = sn_types.Part(assembly.add_assembly_from_file(CLOSET_PANEL))
    assembly.add_assembly(panel)
    panel.obj_bp['IS_BP_ASSEMBLY'] = True
    panel.obj_bp['IS_BP_PANEL'] = True
    props = panel.obj_bp.sn_closets
    props.is_panel_bp = True  # TODO: remove
    panel.set_name("Partition")
    panel.add_prompt("Is Left End Panel", 'CHECKBOX', False)
    panel.add_prompt("Is Right End Panel", 'CHECKBOX', False)
    panel.add_prompt("Is Left Blind Corner Panel", 'CHECKBOX', False)
    panel.add_prompt("Is Right Blind Corner Panel", 'CHECKBOX', False)
    panel.add_prompt("Left Depth", 'DISTANCE', 0)
    panel.add_prompt("Right Depth", 'DISTANCE', 0)
    panel.add_prompt("Stop Drilling Bottom Left", 'DISTANCE', 0)
    panel.add_prompt("Stop Drilling Top Left", 'DISTANCE', 0)
    panel.add_prompt("Stop Drilling Bottom Right", 'DISTANCE', 0)
    panel.add_prompt("Stop Drilling Top Right", 'DISTANCE', 0)
    panel.add_prompt("Place Hanging Hardware On Right", 'CHECKBOX', False)
    panel.add_prompt("Exposed Bottom", 'CHECKBOX', False)
    panel.add_prompt("CatNum", 'QUANTITY', 0)
    panel.cutpart("Panel")
    panel.edgebanding("Edge", l2=True)
    panel.edgebanding("Edge_2", w2=True, w1=True)
    panel.set_material_pointers("Closet_Part_Edges", "FrontBackEdge")
    panel.set_material_pointers("Closet_Part_Edges_Secondary", "TopBottomEdge")

    for child in panel.obj_bp.children:
        if child.snap.type_mesh == 'CUTPART':
            child.snap.use_multiple_edgeband_pointers = True
            child.snap.delete_protected = True

    return panel


def add_shelf(assembly):
    defaults = bpy.context.scene.sn_closets.closet_defaults
    shelf = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(shelf)
    shelf.obj_bp['IS_SHELF'] = True
    props = shelf.obj_bp.sn_closets
    props.is_shelf_bp = True
    shelf.set_name("Shelf")
    shelf.add_prompt("CatNum", 'QUANTITY', 0)
    shelf.add_prompt("Shelf Pin Qty", 'QUANTITY', 0)
    shelf.add_prompt("Cam Qty", 'QUANTITY', 0)
    shelf.add_prompt("Is Locked Shelf", 'CHECKBOX', False)
    shelf.add_prompt("Is Forced Locked Shelf", 'CHECKBOX', False)
    shelf.add_prompt("Is Bottom Exposed KD", 'CHECKBOX', False)
    shelf.add_prompt("Adj Shelf Clip Gap", 'DISTANCE', defaults.adj_shelf_clip_gap)
    shelf.add_prompt("Adj Shelf Setback", 'DISTANCE', defaults.adj_shelf_setback)
    shelf.add_prompt("Locked Shelf Setback", 'DISTANCE', defaults.locked_shelf_setback)
    shelf.add_prompt("Drill On Top", 'CHECKBOX', False)
    shelf.add_prompt("Remove Left Holes", 'CHECKBOX', False)
    shelf.add_prompt("Remove Right Holes", 'CHECKBOX', False)
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge', l2=True)
    return shelf


def add_glass_shelf(assembly):
    defaults = bpy.context.scene.sn_closets.closet_defaults
    shelf = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(shelf)
    shelf.obj_bp['IS_SHELF'] = True
    shelf.obj_bp['IS_GLASS_SHELF'] = True
    props = shelf.obj_bp.sn_closets
    props.is_shelf_bp = True  # TODO: remove
    props.is_glass_shelf_bp = True  # TODO: remove
    shelf.obj_bp.snap.name_object = "Glass Shelf"
    shelf.set_name("Glass Shelf")
    shelf.add_prompt("Shelf Pin Qty", 'QUANTITY', 4)
    shelf.add_prompt("Is Locked Shelf", 'CHECKBOX', False)
    shelf.add_prompt("Is Forced Locked Shelf", 'CHECKBOX', False)
    shelf.add_prompt("Adj Shelf Clip Gap", 'DISTANCE', defaults.adj_shelf_clip_gap)
    shelf.add_prompt("Adj Shelf Setback", 'DISTANCE', defaults.adj_shelf_setback)
    shelf.add_prompt("Locked Shelf Setback", 'DISTANCE', defaults.locked_shelf_setback)
    for child in shelf.obj_bp.children:
        if child.type == 'MESH':
            child.snap.type_mesh = 'BUYOUT'
    shelf.material("Glass")
    return shelf


def add_l_shelf(assembly):
    shelf = sn_types.Part(assembly.add_assembly_from_file(CORNER_NOTCH_PART))
    assembly.add_assembly(shelf)
    props = shelf.obj_bp.sn_closets
    props.is_l_shelf_bp = True  # TODO: Remove
    shelf.obj_bp['IS_BP_L_SHELF'] = True
    shelf.add_prompt("Is Locked Shelf",'CHECKBOX',False)
    shelf.add_prompt("Is Forced Locked Shelf", 'CHECKBOX', False)
    shelf.obj_bp.snap.comment_2 = "1525"
    shelf.set_name("L Shelf")
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge', l1=True)
    return shelf


def add_angle_shelf(assembly):
    shelf = sn_types.Part(assembly.add_assembly_from_file(CHAMFERED_PART))
    assembly.add_assembly(shelf)
    shelf.obj_bp.snap.comment_2 = "1520"
    props = shelf.obj_bp.sn_closets
    props.is_angle_shelf_bp = True  # TODO: Remove
    shelf.obj_bp['IS_BP_ANGLE_SHELF'] = True
    shelf.add_prompt("Is Locked Shelf",'CHECKBOX',False)
    shelf.add_prompt("Is Forced Locked Shelf", 'CHECKBOX', False)
    shelf.set_name("Corner Shelf")
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge', l1=True)
    return shelf


def add_filler(assembly):
    filler = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_ALL_EDGES))
    assembly.add_assembly(filler)
    filler.obj_bp.snap.comment_2 = "1036"
    props = filler.obj_bp.sn_closets
    props.is_filler_bp = True
    filler.obj_bp['IS_FILLER'] = True
    filler.set_name("Panel")
    filler.add_prompt("Exposed Left", 'CHECKBOX', False)
    filler.add_prompt("Exposed Right", 'CHECKBOX', False)
    filler.add_prompt("Exposed Back", 'CHECKBOX', False)
    filler.cutpart("Shelf")
    filler.edgebanding('Edge', l1=True, l2=True, w1=True, w2=True)
    filler.set_material_pointers("Closet_Part_Edges", "Edgebanding")
    filler.set_material_pointers("Core", "LeftEdge")
    filler.set_material_pointers("Core", "RightEdge")
    filler.set_material_pointers("Core", "BackEdge")
    for child in filler.obj_bp.children:
        if child.snap.type_mesh == 'CUTPART':
            child.snap.use_multiple_edgeband_pointers = True
    return filler


def add_door_striker(assembly):
    striker = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(striker)
    props = striker.obj_bp.sn_closets
    striker.obj_bp['IS_DOOR_STRIKER'] = True
    props.is_door_striker_bp = True  # TODO: Remove
    striker.obj_bp.snap.comment_2 = "1041"
    striker.set_name("Door Striker")
    striker.cutpart("Shelf")
    striker.edgebanding("Edge", l1 = True)    
    return striker


def add_corbel(assembly):
    corbel = sn_types.Part(assembly.add_assembly_from_file(CHAMFERED_PART))
    assembly.add_assembly(corbel)
    # Does this need a comment?
    # corbel.obj_bp.snap.comment_2 = ""
    props = corbel.obj_bp.sn_closets
    props.is_angle_shelf_bp = True  # TODO: Remove
    corbel.obj_bp['IS_BP_CORBEL'] = True
    corbel.set_name("Support Corbel")
    corbel.cutpart("Shelf")
    corbel.edgebanding('Edge', l1=True)
    return corbel


def add_cover_cleat(assembly, cleat):
    cover_cleat = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(cover_cleat)
    cover_cleat.obj_bp.parent = cleat.obj_bp
    cover_cleat.obj_bp.snap.comment_2 = "1028"
    props = cover_cleat.obj_bp.sn_closets
    props.is_cleat_bp = True
    props.is_cover_cleat_bp = True
    cover_cleat.obj_bp['IS_CLEAT'] = True
    cover_cleat.obj_bp['IS_COVER_CLEAT'] = True
    cover_cleat.set_name("Cover Cleat")
    cover_cleat.cutpart("Cover_Cleat")
    cover_cleat.edgebanding("Edge_2", l1=True)

    cleat.add_prompt("Use Cleat Cover", 'CHECKBOX', True)
    cleat.add_prompt("Cover Cleat Difference", 'DISTANCE', sn_unit.inch(0.04))

    Use_Cleat_Cover = cleat.get_prompt('Use Cleat Cover').get_var('Use_Cleat_Cover')
    Width = cleat.obj_x.snap.get_var('location.x', 'Width')
    Depth = cleat.obj_y.snap.get_var('location.y', 'Depth')
    Hide = cleat.get_prompt('Hide').get_var('Hide')
    Cover_Cleat_Difference = cleat.get_prompt("Cover Cleat Difference").get_var('Cover_Cleat_Difference')

    cover_cleat.dim_x('Width', [Width])
    cover_cleat.dim_y('IF(Depth < 0, Depth - Cover_Cleat_Difference, Depth + Cover_Cleat_Difference)', [Depth, Cover_Cleat_Difference])
    cover_cleat.loc_y('IF(Depth > 0, Cover_Cleat_Difference, -Cover_Cleat_Difference)', [Depth, Cover_Cleat_Difference])
    cover_cleat.dim_z(value=sn_unit.inch(-0.375))
    cover_cleat.loc_z(value=sn_unit.inch(-0.75))
    hide = cover_cleat.get_prompt('Hide')
    hide.set_formula('IF(Use_Cleat_Cover,Hide,True) or Hide', [Hide, Use_Cleat_Cover])


def add_cleat(assembly):
    cleat = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(cleat)
    cleat.obj_bp.snap.comment_2 = "1008"
    props = cleat.obj_bp.sn_closets
    props.is_cleat_bp = True
    cleat.obj_bp['IS_CLEAT'] = True
    cleat.set_name("Cleat")
    cleat.cutpart("Cleat")
    cleat.edgebanding("Edge_2", l1=True)
    add_cover_cleat(assembly, cleat)
    cleat.dim_y(value=sn_unit.inch(3.64))
    return cleat


def add_wall_cleat(assembly):
    cleat = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_ALL_EDGES))
    cleat.obj_bp.snap.comment_2 = "1008"
    cleat.obj_bp['IS_CLEAT'] = True
    cleat.obj_bp['IS_WALL_CLEAT'] = True
    cleat.obj_bp.sn_closets.is_cleat_bp = True
    cleat.add_prompt("Exposed Top", 'CHECKBOX', False)
    cleat.add_prompt("Exposed Left", 'CHECKBOX', False)
    cleat.add_prompt("Exposed Right", 'CHECKBOX', False)
    cleat.add_prompt("Exposed Bottom", 'CHECKBOX', False)
    cleat.set_name("Cleat")
    cleat.cutpart("Cleat")
    cleat.edgebanding("Edge_1", w1=True)
    cleat.edgebanding("Edge_2", l1=True)
    cleat.edgebanding("Edge_3", w2=True)
    cleat.edgebanding("Edge_4", l2=True)
    cleat.dim_y(value=sn_unit.inch(3.64))
    cleat.set_material_pointers("Core", "Edgebanding")
    cleat.set_material_pointers("Core", "LeftEdge")
    cleat.set_material_pointers("Core", "RightEdge")
    cleat.set_material_pointers("Core", "BackEdge")
    for child in cleat.obj_bp.children:
        if child.snap.type_mesh == 'CUTPART':
            child.snap.use_multiple_edgeband_pointers = True
    return cleat


def add_door(assembly):
    door = sn_types.Part(assembly.add_assembly_from_file(FACE))
    assembly.add_assembly(door)
    door.set_name("Door")
    door.cutpart("Slab_Door")
    door.edgebanding('Door_Edges', l1=True, w1=True, l2=True, w2=True)
    door.add_prompt("CatNum", 'QUANTITY', 1006)
    door.add_prompt("Door Type", 'COMBOBOX', 0, ['Base','Tall','Upper'])
    door.add_prompt("Door Swing", 'COMBOBOX', 0, ['Left','Right','Top','Bottom'])
    door.add_prompt("No Pulls", 'CHECKBOX', False)
    door.obj_bp['IS_DOOR'] = True
    obj_props = door.obj_bp.sn_closets
    obj_props.is_door_bp = True  # TODO: remove
    obj_props.door_type = 'FLAT'
    return door


def add_door_pull(assembly):
    pull_hardware = data_pull_hardware.Standard_Pull()
    pull_hardware.draw()
    pull_hardware.obj_bp.snap.comment_2 = "1015"
    pull_hardware.obj_bp.parent = assembly.obj_bp
    pull_hardware.set_name("Pull")
    return pull_hardware

# TODO: Remove
def add_drawer_pull(assembly):
    pull_hardware = data_pull_hardware.Standard_Pull()
    pull_hardware.draw()
    pull_hardware.obj_bp.snap.comment_2 = "1015"
    pull_hardware.obj_bp.parent = assembly.obj_bp
    pull_hardware.set_name("Pull")
    return pull_hardware


def add_lock(assembly):
    lock = sn_types.Part(assembly.add_assembly_from_file(CAM_LOCK))
    assembly.add_assembly(lock)
    lock.set_name("Lock")
    lock.set_material_pointers('Chrome', "Lock Metal")
    lock.obj_bp["IS_BP_LOCK"] = True
    return lock


def add_toe_kick(assembly):
    kick = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_NO_EDGEBANDING))
    assembly.add_assembly(kick)
    kick.obj_bp.snap.comment_2 = "1034"
    kick.obj_bp['IS_BP_TOE_KICK'] = True
    props = kick.obj_bp.sn_closets
    props.is_toe_kick_bp = True
    kick.set_name("Toe Kick")
    kick.cutpart("Toe_Kick")
    return kick


def add_drawer_front(assembly):
    front = sn_types.Part(assembly.add_assembly_from_file(FACE))
    assembly.add_assembly(front)
    front.obj_bp.snap.comment_2 = "1007"
    front.set_name("Drawer Face")
    front.cutpart("Slab_Drawer_Front")
    front.add_prompt("No Pulls", 'CHECKBOX', False)
    front.add_prompt("Use Double Pulls", 'CHECKBOX', False)
    front.add_prompt("Center Pulls on Drawers", 'CHECKBOX', False)
    front.add_prompt("Drawer Pull From Top", 'DISTANCE', 0)
    front.edgebanding('Door_Edges',l1=True, w1=True, l2=True, w2=True)
    front.obj_bp.snap.is_cabinet_drawer_front = True  # TODO: Remove
    front.obj_bp.snap.comment = "Melamine Drawer Face"
    obj_props = front.obj_bp.sn_closets
    obj_props.door_type = 'FLAT'
    obj_props.is_drawer_front_bp = True  # TODO: Remove
    front.obj_bp["IS_BP_DRAWER_FRONT"] = True
    return front


def add_drawer_side(assembly):
    side = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(side)
    side.obj_bp.snap.comment_2 = "1031"
    side.set_name("Drawer Side")
    side.cutpart("Drawer_Part")
    side.add_prompt("Use Dovetail Construction", 'CHECKBOX', False)
    side.edgebanding('Drawer_Box_Edge',l1 = True)
    props = side.obj_bp.sn_closets
    props.is_drawer_side_bp = True
    side.obj_bp["IS_BP_DRAWER_SIDE"] = True
    return side


def add_drawer_back(assembly):
    drawer_back = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(drawer_back)
    drawer_back.obj_bp.snap.comment_2 = "1032"
    drawer_back.set_name("Drawer Back")
    drawer_back.cutpart("Drawer_Back")
    drawer_back.add_prompt("Use Dovetail Construction", 'CHECKBOX', False)
    drawer_back.edgebanding('Drawer_Box_Edge',l1 = True)
    props = drawer_back.obj_bp.sn_closets
    props.is_drawer_back_bp = True
    drawer_back.obj_bp["IS_BP_DRAWER_BACK"] = True
    return drawer_back

       
def add_drawer_sub_front(assembly):
    front_back = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(front_back)
    front_back.obj_bp.snap.comment_2 = "1029"
    front_back.set_name("Drawer Sub Front")
    front_back.cutpart("Drawer_Part")
    front_back.add_prompt("Use Dovetail Construction", 'CHECKBOX', False)
    front_back.edgebanding('Drawer_Box_Edge',l1 = True)
    props = front_back.obj_bp.sn_closets
    props.is_drawer_sub_front_bp = True
    front_back.obj_bp["IS_BP_DRAWER_SUB_FRONT"] = True
    return front_back


def add_drawer_bottom(assembly):
    bottom = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_NO_EDGEBANDING))
    assembly.add_assembly(bottom)
    bottom.obj_bp.snap.comment_2 = "1030"
    bottom.set_name("Drawer Bottom")
    bottom.cutpart("Drawer_Bottom")
    bottom.add_prompt("Use Dovetail Construction", 'CHECKBOX', False)
    props = bottom.obj_bp.sn_closets
    props.is_drawer_bottom_bp = True
    bottom.obj_bp["IS_BP_DRAWER_BOTTOM"] = True
    return bottom


def add_drawer(assembly):
    scene_props = bpy.context.scene.sn_closets
    if scene_props.closet_defaults.use_buyout_drawers:
        drawer = assembly.add_assembly_from_file(BUYOUT_DRAWER_BOX)
        drawer = sn_types.Part(drawer)
        drawer.material("Drawer_Box_Surface")
        drawer.obj_bp.snap.comment_2 = "1014"
    else:
        drawer = data_drawer_wood.Wood_Drawer_Box()
        drawer.draw()
        drawer.obj_bp.parent = assembly.obj_bp
        drawer.obj_bp.snap.comment_2 = "1014"
    add_drawer_file_rails(drawer)
    return drawer


def add_dovetail_drawer(assembly):
    drawer = data_drawer_wood.Wood_Drawer_Box()
    drawer.draw()
    drawer.obj_bp.parent = assembly.obj_bp
    drawer.obj_bp.snap.comment_2 = "1014"
    return drawer


def add_hamper_front(assembly):
    front = sn_types.Part(assembly.add_assembly_from_file(FACE))
    assembly.add_assembly(front)
    front.obj_bp.snap.comment_2 = "1044"     
    front.set_name("Hamper Door")
    front.cutpart("Slab_Drawer_Front")
    front.edgebanding('Door_Edges',l1=True, w1=True, l2=True, w2=True)
    front.obj_bp['IS_DOOR'] = True
    props = front.obj_bp.sn_closets
    props.is_hamper_front_bp = True
    front.obj_bp['IS_BP_HAMPER_FRONT'] = True
    return front


def add_wire_hamper(assembly):
    hamper = sn_types.Part(assembly.add_assembly_from_file(WIRE_BASKET))
    assembly.add_assembly(hamper)
    hamper.obj_bp.snap.comment_2 = "1016"
    hamper.set_name("Hamper Basket")
    hamper.material('Wire_Basket')
    props = hamper.obj_bp.sn_closets
    props.is_hamper_bp = True
    hamper.obj_bp['IS_BP_HAMPER'] = True
    return hamper


def add_single_canvas_hamper(assembly):
    hamper = sn_types.Part(assembly.add_assembly_from_file(TOSP_SINGLE_HAMPER))
    assembly.add_assembly(hamper)
    hamper.obj_bp.snap.comment_2 = "1016"
    hamper.set_name("Single Canvas Hamper")
    props = hamper.obj_bp.sn_closets
    props.is_hamper_bp = True
    hamper.obj_bp['IS_BP_HAMPER'] = True
    return hamper


def add_double_canvas_hamper(assembly):
    hamper = sn_types.Part(assembly.add_assembly_from_file(TOSP_DOUBLE_HAMPER))
    assembly.add_assembly(hamper)
    hamper.obj_bp.snap.comment_2 = "1016"
    hamper.set_name("Double Canvas Hamper")
    props = hamper.obj_bp.sn_closets
    props.is_hamper_bp = True
    hamper.obj_bp['IS_BP_HAMPER'] = True
    return hamper


def add_line_bore_holes(assembly):
    holes = sn_types.Part(assembly.add_assembly_from_file(LINE_BORE))
    assembly.add_assembly(holes)    
    return holes


def add_toe_kick_end_cap(assembly):
    kick = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_NO_EDGEBANDING))
    assembly.add_assembly(kick)
    kick.obj_bp.snap.comment_2 = "1033"
    kick.obj_bp['IS_BP_TOE_KICK_END_CAP'] = True
    props = kick.obj_bp.sn_closets
    props.is_toe_kick_end_cap_bp = True # TODO: remove
    kick.set_name("Toe Kick End Cap")
    kick.cutpart("Toe_Kick")
    return kick


def add_toe_kick_stringer(assembly):
    kick = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_NO_EDGEBANDING))
    assembly.add_assembly(kick)
    kick.obj_bp.snap.comment_2 = "1035"
    kick.obj_bp['IS_BP_TOE_KICK_STRINGER'] = True
    props = kick.obj_bp.sn_closets
    props.is_toe_kick_stringer_bp = True  # TODO: remove
    kick.set_name("Toe Kick Stringer")
    kick.cutpart("Toe_Kick")
    return kick


def add_granite_countertop(assembly):
    ctop = sn_types.Part(assembly.add_assembly_from_file(STRAIGHT_COUNTER_TOP))
    assembly.add_assembly(ctop)
    ctop.obj_bp.snap.comment_2 = "1605"
    ctop.obj_bp['IS_BP_COUNTERTOP'] = True
    props = ctop.obj_bp.sn_closets
    props.is_countertop_bp = True
    ctop.set_name("Countertop Deck")
    ctop.material("Countertop_Granite_Surface")
    return ctop


def add_cc_countertop(assembly):
    ctop = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_ALL_EDGES))
    assembly.add_assembly(ctop)
    ctop.obj_bp.snap.comment_2 = "1605"
    ctop.obj_bp['IS_BP_COUNTERTOP'] = True
    props = ctop.obj_bp.sn_closets
    props.is_countertop_bp = True
    ctop.set_name("Countertop")
    ctop.material("Countertop_Surface")
    ctop.add_prompt("Exposed Left", 'CHECKBOX', False)
    ctop.add_prompt("Exposed Right", 'CHECKBOX', False)
    ctop.add_prompt("Exposed Back", 'CHECKBOX', False)
    ctop.add_prompt("Edge Type", 'CHECKBOX', False)
    ctop.cutpart("Shelf")
    ctop.edgebanding('Edge', l1=True, l2=True, w1=True, w2=True)
    ctop.set_material_pointers("Closet_Part_Edges", "Edgebanding")
    ctop.set_material_pointers("Core", "LeftEdge")
    ctop.set_material_pointers("Core", "RightEdge")
    ctop.set_material_pointers("Core", "BackEdge")
    for child in ctop.obj_bp.children:
        if child.snap.type_mesh == 'CUTPART':
            child.snap.use_multiple_edgeband_pointers = True
    return ctop


def add_cc_corner_countertop(assembly):
    ctop = sn_types.Part(assembly.add_assembly_from_file(CORNER_CC_COUNTER_TOP))
    assembly.add_assembly(ctop)
    ctop.obj_bp.snap.comment_2 = "1605"
    ctop.obj_bp['IS_BP_COUNTERTOP'] = True
    props = ctop.obj_bp.sn_closets
    props.is_countertop_bp = True
    ctop.set_name("Countertop Deck")
    ctop.material("Countertop_Surface")
    return ctop


def add_back_splash(assembly):
    b_splash = sn_types.Part(assembly.add_assembly_from_file(BACKSPLASH_PART))
    assembly.add_assembly(b_splash)
    b_splash.obj_bp.snap.comment_2 = "1605"
    b_splash.obj_bp['IS_BP_COUNTERTOP'] = True
    props = b_splash.obj_bp.sn_closets
    props.is_countertop_bp = True
    b_splash.set_name("Countertop Back Splash")
    b_splash.material("Countertop_Surface")
    return b_splash


def add_plant_on_top(assembly):
    shelf = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_ALL_EDGES))
    assembly.add_assembly(shelf)
    shelf.obj_bp['IS_BP_PLANT_ON_TOP'] = True
    props = shelf.obj_bp.sn_closets
    props.is_plant_on_top_bp = True  # TODO: remove
    shelf.add_prompt("Is Countertop", 'CHECKBOX', False)  
    shelf.add_prompt("Exposed Left", 'CHECKBOX', False)
    shelf.add_prompt("Exposed Right", 'CHECKBOX', False)    
    shelf.add_prompt("Exposed Back", 'CHECKBOX', False)  
    shelf.set_name("Top")      
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge', l1=True, l2=True, w1=True, w2=True)
    shelf.set_material_pointers("Closet_Part_Edges", "Edgebanding")
    shelf.set_material_pointers("Core","LeftEdge")
    shelf.set_material_pointers("Core","RightEdge")
    shelf.set_material_pointers("Core","BackEdge")
    for child in shelf.obj_bp.children:
        if child.snap.type_mesh == 'CUTPART':
            child.snap.use_multiple_edgeband_pointers = True    
    return shelf


def add_hpl_top(assembly):
    shelf = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_ALL_EDGES))
    assembly.add_assembly(shelf)
    shelf.obj_bp['IS_BP_HPL_TOP'] = True
    shelf.obj_bp['IS_BP_COUNTERTOP'] = True
    props = shelf.obj_bp.sn_closets
    props.is_hpl_top_bp = True  # TODO: remove
    props.is_countertop_bp = True # TODO: remove
    for child in shelf.obj_bp.children:
        if child.type == 'MESH':
            child.snap.type_mesh = 'BUYOUT'      
    shelf.add_prompt("Exposed Left", 'CHECKBOX', False)
    shelf.add_prompt("Exposed Right", 'CHECKBOX', False)    
    shelf.add_prompt("Exposed Back", 'CHECKBOX', False)  
    shelf.set_name("Top") 
    shelf.edgebanding('Edge', l1=True, l2=True, w1=True, w2=True)
    shelf.material("Countertop_HPL_Surface")
    for child in shelf.obj_bp.children:
        if child.snap.type_mesh == 'CUTPART':
            child.snap.use_multiple_edgeband_pointers = True    
    return shelf


def add_flat_crown(assembly):
    shelf = sn_types.Part(assembly.add_assembly_from_file(MITERED_PART_WITH_ALL_EDGES))
    assembly.add_assembly(shelf)
    shelf.obj_bp['IS_BP_CROWN_MOLDING'] = True
    shelf.obj_bp['IS_BP_FLAT_CROWN'] = True
    props = shelf.obj_bp.sn_closets
    props.is_crown_molding = True  # TODO: remove
    shelf.add_prompt("Exposed Left", 'CHECKBOX', False)
    shelf.add_prompt("Exposed Right", 'CHECKBOX', False)
    shelf.add_prompt("Exposed Back", 'CHECKBOX', False)
    shelf.add_prompt("Exposed Front", 'CHECKBOX', False)
    shelf.set_name("Flat Crown")
    shelf.rot_x(value=math.radians(90))
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge', l1=True, l2=True, w1=True, w2=True)
    shelf.set_material_pointers("Closet_Part_Edges_Secondary", "Edgebanding")
    shelf.set_material_pointers("Core", "LeftEdge")
    shelf.set_material_pointers("Core", "RightEdge")
    shelf.set_material_pointers("Core", "BackEdge")
    for child in shelf.obj_bp.children:
        if child.snap.type_mesh == 'CUTPART':
            child.snap.use_multiple_edgeband_pointers = True
    return shelf


def add_slanted_shoe_shelf(assembly):
    slanted_shelf = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_EDGEBANDING))
    assembly.add_assembly(slanted_shelf)
    slanted_shelf.obj_bp.snap.comment_2 = "1655"
    slanted_shelf.obj_bp['IS_BP_SLANTED_SHELF'] = True
    slanted_shelf.set_name("Slanted Shoe Shelf")
    slanted_shelf.cutpart("Shelf")
    slanted_shelf.edgebanding('Edge', l1=True, w1=True, l2=True, w2=True)
    slanted_shelf.add_prompt("Shelf Pin Qty", 'QUANTITY', 2)
    slanted_shelf.add_prompt("Cam Qty", 'QUANTITY', 2)
    props = slanted_shelf.obj_bp.sn_closets
    props.is_slanted_shelf_bp = True  # TODO: remove
    return slanted_shelf


def add_shelf_lip(assembly):
    shelf_lip = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_EDGEBANDING))
    assembly.add_assembly(shelf_lip)
    shelf_lip.set_name("Shelf Lip")
    shelf_lip.cutpart("Shelf")
    shelf_lip.edgebanding('Edge', l1=True, w1=True, l2=True, w2=True)
    shelf_lip.obj_bp['IS_BP_SHELF_LIP'] = True
    props = shelf_lip.obj_bp.sn_closets
    props.is_shelf_lip_bp = True  # TODO: remove
    return shelf_lip


def add_deco_shelf_lip_1(assembly):
    deco_shelf_lip = sn_types.Part(assembly.add_assembly_from_file(DECO_100_LIP))
    assembly.add_assembly(deco_shelf_lip)
    deco_shelf_lip.obj_bp.snap.comment_2 = "1016"
    deco_shelf_lip.set_name("Deco Shelf Lip #1")
    deco_shelf_lip.material("Closet_Part_Surfaces")
    deco_shelf_lip.obj_bp['IS_BP_DECO_SHELF_LIP'] = True
    props = deco_shelf_lip.obj_bp.sn_closets
    props.is_deco_shelf_lip_bp = True  # TODO: remove
    return deco_shelf_lip


def add_deco_shelf_lip_2(assembly):
    deco_shelf_lip = sn_types.Part(assembly.add_assembly_from_file(DECO_200_LIP))
    assembly.add_assembly(deco_shelf_lip)
    deco_shelf_lip.obj_bp.snap.comment_2 = "1016"
    deco_shelf_lip.set_name("Deco Shelf Lip #2")
    deco_shelf_lip.material("Closet_Part_Surfaces")
    deco_shelf_lip.obj_bp['IS_BP_DECO_SHELF_LIP'] = True
    props = deco_shelf_lip.obj_bp.sn_closets
    props.is_deco_shelf_lip_bp = True  # TODO: remove
    return deco_shelf_lip


def add_deco_shelf_lip_3(assembly):
    deco_shelf_lip = sn_types.Part(assembly.add_assembly_from_file(DECO_300_LIP))
    assembly.add_assembly(deco_shelf_lip)
    deco_shelf_lip.obj_bp.snap.comment_2 = "1016"
    deco_shelf_lip.set_name("Deco Shelf Lip #3")
    deco_shelf_lip.material("Closet_Part_Surfaces")
    deco_shelf_lip.obj_bp['IS_BP_DECO_SHELF_LIP'] = True
    props = deco_shelf_lip.obj_bp.sn_closets
    props.is_deco_shelf_lip_bp = True  # TODO: remove
    return deco_shelf_lip


def add_shelf_fence(assembly):
    steel_fence = sn_types.Part(assembly.add_assembly_from_file(STEEL_FENCE))
    assembly.add_assembly(steel_fence)
    steel_fence.obj_bp.snap.comment_2 = "1016"
    steel_fence.set_name("Steel Fence")
    steel_fence.material("Pull_Finish")
    steel_fence.obj_bp['IS_BP_SHELF_FENCE'] = True
    props = steel_fence.obj_bp.sn_closets
    props.is_shelf_fence_bp = True  # TODO: remove
    return steel_fence


def add_accessory_panel(assembly):
    accessory_panel = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_EDGEBANDING))
    assembly.add_assembly(accessory_panel)
    # these are setup for xml export. They are not linked up
    accessory_panel.add_prompt('Exposed Left', 'CHECKBOX', True)
    accessory_panel.add_prompt('Exposed Top', 'CHECKBOX', True)
    accessory_panel.add_prompt('Exposed Right', 'CHECKBOX', True)
    accessory_panel.add_prompt('Exposed Bottom', 'CHECKBOX', True)
    accessory_panel.obj_bp['IS_WALL_CLEAT'] = True
    accessory_panel.obj_bp['IS_CLEAT'] = True
    accessory_panel.set_name("Accessory Panel")
    accessory_panel.cutpart("Panel")
    accessory_panel.edgebanding('Edge', l1=True)
    return accessory_panel


def add_division(assembly):
    division = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_EDGEBANDING))
    assembly.add_assembly(division)
    division.set_name("Panel")
    division.cutpart("Panel")
    division.edgebanding("Edge", l2=True)
    division.obj_bp['IS_BP_DIVISION'] = True
    props = division.obj_bp.sn_closets # TODO: remove
    props.is_division_bp = True
    return division


def add_wire_basket(assembly):
    basket = sn_types.Part(assembly.add_assembly_from_file(WIRE_BASKET))
    assembly.add_assembly(basket)
    basket.obj_bp['IS_BP_BASKET'] = True
    basket.obj_bp.snap.comment_2 = "1016"
    basket.set_name("Wire Basket")
    basket.material('Wire_Basket')
    props = basket.obj_bp.sn_closets
    props.is_basket_bp = True  # TODO: Remove
    return basket


def add_sliding_pants_rack(assembly):
    pants_rack = sn_types.Part(assembly.add_assembly_from_file(SLIDING_PANTS_RACK))
    assembly.add_assembly(pants_rack)
    pants_rack.set_name("Sliding Panels Rack")
    return pants_rack


def add_single_pull_out_canvas_hamper(assembly):
    hamper = sn_types.Part(assembly.add_assembly_from_file(PULL_OUT_CANVAS_HAMPER))
    hamper = assembly.add_assembly(hamper)
    hamper.obj_bp['IS_BP_HAMPER'] = True
    hamper.obj_bp.snap.comment_2 = "1016"
    hamper.set_name("Single Pull Out Canvas Hamper")
    props = hamper.obj_bp.sn_closets
    props.is_hamper_bp = True
    return hamper


def add_double_pull_out_canvas_hamper(assembly):
    hamper = sn_types.Part(assembly.add_assembly_from_file(DOUBLE_PULL_OUT_CANVAS_HAMPER))
    hamper = assembly.add_assembly(hamper)
    hamper.obj_bp['IS_BP_HAMPER'] = True
    hamper.obj_bp.snap.comment_2 = "1016"
    hamper.set_name("Double Pull Out Canvas Hamper")
    props = hamper.obj_bp.sn_closets
    props.is_hamper_bp = True
    return hamper


def add_toe_kick_skin(assembly):
    kick = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_NO_EDGEBANDING))
    kick.obj_bp["IS_BP_TOE_KICK_SKIN"] = True
    assembly.add_assembly(kick)
    kick.obj_bp.snap.comment_2 = "1035"
    props = kick.obj_bp.sn_closets
    props.is_toe_kick_skin_bp = True
    kick.set_name("Toe Kick Skin")
    kick.cutpart("Back")
    return kick


def add_back(assembly):
    backing = sn_types.Part(assembly.add_assembly_from_file(FULL_BACK))
    assembly.add_assembly(backing)
    backing.obj_bp.snap.comment_2 = "1037"
    backing.obj_bp['IS_BP_ASSEMBLY'] = True
    backing.obj_bp["IS_BACK"] = True
    props = backing.obj_bp.sn_closets
    props.is_back_bp = True
    backing.set_name("Backing")
    backing.cutpart("Back")
    return backing

def add_corner_back(assembly):
    backing = sn_types.Part(assembly.add_assembly_from_file(FULL_BACK))
    assembly.add_assembly(backing)
    backing.obj_bp.snap.comment_2 = "1037"
    backing.add_prompt("Is Left Back",'CHECKBOX',False)
    backing.obj_bp['IS_BP_ASSEMBLY'] = True
    backing.obj_bp["IS_BACK"] = True
    backing.obj_bp["IS_CORNER_BACK"] = True
    props = backing.obj_bp.sn_closets
    props.is_back_bp = True
    backing.set_name("Backing")
    backing.cutpart("Back")
    return backing

# Updated


def add_hanging_rod_cup(assembly):
    cup = assembly.add_object(OVAL_ROD_CUP)
    cup.obj_bp.snap.comment_2 = "1015"
    return cup

def add_rod_support(assembly):
    rod_support = assembly.add_assembly_from_file(ROD_SUPPORT)
    rod_support = sn_types.Part(rod_support)
    rod_support.obj_bp.snap.comment_2 = "1015"
    return rod_support

def add_shelf_support(assembly):
    shelf_support = assembly.add_assembly_from_file(SHELF_SUPPORT)
    shelf_support = sn_types.Part(shelf_support)
    shelf_support.obj_bp.snap.comment_2 = "1015"
    return shelf_support

def add_hanging_rod(assembly):
    rod = assembly.add_assembly_from_file(OVAL_ROD)
    rod = sn_types.Part(rod)
    props = rod.obj_bp.sn_closets
    props.is_hanging_rod = True
    rod.obj_bp.snap.comment_2 = "1015"
    rod.solid_stock("Oval Hanging Rod")
    closet_options = bpy.context.scene.lm_closets.closet_options
    rod.obj_bp.snap.name_object = closet_options.rods_name
    return rod

def add_hanging_rail(assembly):
    rail = assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING)
    rail = sn_types.Part(rail)
    props = assembly.obj_bp.sn_closets
    rail.obj_bp.snap.comment_2 = "1015"
    props.is_hanging_rail_bp = True
    rail.cutpart("Hanging_Rail")
    rail.set_name("Hanging Rail")
    return rail

def add_tie_drawer_top_or_bottom(assembly):
    top = assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING)
    top = sn_types.Part(top)
    top.cutpart("Drawer_Part")
    top.edgebanding('Drawer_Box_Edge',l1 = True)

def add_tie_drawer_division(assembly):
    division = assembly.add_assembly_from_file(PART_WITH_NO_EDGEBANDING)
    division = sn_types.Part(division)
    division.set_name("Tie Drawer Division")
    division.cutpart("Drawer_Part")

def add_radius_shelf(assembly):
    shelf = assembly.add_assembly_from_file(RADIUS_PART)
    shelf = sn_types.Part(shelf)
    props = shelf.obj_bp.sn_closets
    props.is_radius_shelf_bp = True
    shelf.set_name("Radius Shelf")
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l1 = True)
    return shelf

def add_drawer_file_rails(assembly):
    assembly.add_prompt("Use File Rail", 'CHECKBOX', False)
    assembly.add_prompt("File Rail Type", 'COMBOBOX', 1, ['Letter', 'Legal'])
    assembly.add_prompt("File Rail Direction", 'COMBOBOX', 0, ['Front to Back', 'Lateral'])
    assembly.add_prompt("File Rail Thickness", 'DISTANCE', sn_unit.inch(0.5))
    assembly.add_prompt("File Rail Height", 'DISTANCE', sn_unit.inch(9))
    assembly.add_prompt("File Rail Letter Distance", 'DISTANCE', sn_unit.inch(12))
    assembly.add_prompt("File Rail Legal Distance", 'DISTANCE', sn_unit.inch(15))
    assembly.add_prompt("File Rail Difference", 'DISTANCE', sn_unit.inch(0.05))

    Use_File_Rail = assembly.get_prompt('Use File Rail').get_var('Use_File_Rail')
    Width = assembly.obj_x.snap.get_var('location.x','Width')
    Depth = assembly.obj_y.snap.get_var('location.y','Depth')
    Hide = assembly.get_prompt('Hide').get_var('Hide')
    File_Rail_Type = assembly.get_prompt("File Rail Type").get_var('File_Rail_Type')
    File_Rail_Direction = assembly.get_prompt("File Rail Direction").get_var('File_Rail_Direction')
    File_Rail_Thickness = assembly.get_prompt("File Rail Thickness").get_var('File_Rail_Thickness')
    File_Rail_Height = assembly.get_prompt("File Rail Height").get_var('File_Rail_Height')
    File_Rail_Difference = assembly.get_prompt("File Rail Difference").get_var('File_Rail_Difference')

    left_rail = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(left_rail)
    props = left_rail.obj_bp.sn_closets
    props.is_file_rail_bp = True  # TODO: remove
    left_rail.obj_bp["IS_BP_FILE_RAIL"] = True
    left_rail.set_name("File Rail")
    left_rail.cutpart("Left File Rail")
    left_rail.edgebanding("Edge_2",l1 = True)
    left_rail.dim_x('File_Rail_Thickness',[File_Rail_Thickness])
    left_rail.dim_y('Depth-(File_Rail_Thickness*2)-File_Rail_Difference', [Depth, File_Rail_Thickness,File_Rail_Difference])
    left_rail.dim_z('File_Rail_Height',[File_Rail_Height])
    left_rail.loc_x('File_Rail_Thickness',[File_Rail_Thickness])
    left_rail.loc_y('File_Rail_Thickness + File_Rail_Difference/2',[File_Rail_Thickness,File_Rail_Difference])
    left_rail.get_prompt('Hide').set_formula('IF(Use_File_Rail,IF(File_Rail_Direction==0,Hide,True),True)',[Hide, Use_File_Rail,File_Rail_Type,File_Rail_Direction])
    
    right_rail = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(right_rail)
    props = right_rail.obj_bp.sn_closets
    props.is_file_rail_bp = True  # TODO: remove
    right_rail.obj_bp["IS_BP_FILE_RAIL"] = True
    right_rail.set_name("File Rail")
    right_rail.cutpart("Right File Rail")
    right_rail.edgebanding("Edge_2",l1 = True)
    right_rail.dim_x('File_Rail_Thickness',[File_Rail_Thickness])
    right_rail.dim_y('Depth-(File_Rail_Thickness*2)-File_Rail_Difference', [Depth, File_Rail_Thickness,File_Rail_Difference])
    right_rail.dim_z('File_Rail_Height',[File_Rail_Height])
    right_rail.loc_x('IF(File_Rail_Type==0, File_Rail_Thickness*2+'+str(sn_unit.inch(12))+',File_Rail_Thickness*2+'+str(sn_unit.inch(15))+')',[File_Rail_Thickness, File_Rail_Type])
    right_rail.loc_y('File_Rail_Thickness + File_Rail_Difference/2',[File_Rail_Thickness,File_Rail_Difference])
    right_rail.get_prompt('Hide').set_formula('IF(Use_File_Rail,IF(File_Rail_Direction==0,Hide,True),True)',[Hide, Use_File_Rail,File_Rail_Type,File_Rail_Direction])

    front_rail = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(front_rail)
    props = front_rail.obj_bp.sn_closets
    props.is_file_rail_bp = True  # TODO: remove
    front_rail.obj_bp["IS_BP_FILE_RAIL"] = True
    front_rail.set_name("File Rail")
    front_rail.cutpart("Front File Rail")
    front_rail.edgebanding("Edge_2",l1 = True)
    front_rail.dim_x('Width-(File_Rail_Thickness*2)-File_Rail_Difference',[Width,File_Rail_Thickness,File_Rail_Difference])
    front_rail.dim_y('File_Rail_Thickness', [File_Rail_Thickness])
    front_rail.dim_z('File_Rail_Height',[File_Rail_Height])
    front_rail.loc_x('File_Rail_Thickness + File_Rail_Difference/2',[File_Rail_Thickness,File_Rail_Difference])
    front_rail.loc_y('File_Rail_Thickness',[File_Rail_Thickness])
    front_rail.get_prompt('Hide').set_formula('IF(Use_File_Rail,IF(File_Rail_Direction==1,Hide,True),True)',[Hide, Use_File_Rail,File_Rail_Type,File_Rail_Direction])
    
    back_rail = sn_types.Part(assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING))
    assembly.add_assembly(back_rail)
    props = back_rail.obj_bp.sn_closets
    props.is_file_rail_bp = True  # TODO: remove
    back_rail.obj_bp["IS_BP_FILE_RAIL"] = True
    back_rail.set_name("File Rail")
    back_rail.cutpart("Back File Rail")
    back_rail.edgebanding("Edge_2",l1 = True)
    back_rail.dim_x('Width-(File_Rail_Thickness*2)-File_Rail_Difference',[Width,File_Rail_Thickness,File_Rail_Difference])
    back_rail.dim_y('File_Rail_Thickness', [File_Rail_Thickness])
    back_rail.dim_z('File_Rail_Height',[File_Rail_Height])
    back_rail.loc_x('File_Rail_Thickness + File_Rail_Difference/2',[File_Rail_Thickness,File_Rail_Difference])
    back_rail.loc_y('IF(File_Rail_Type==0, File_Rail_Thickness*2+'+str(sn_unit.inch(12))+',File_Rail_Thickness*2+'+str(sn_unit.inch(15))+')',[File_Rail_Thickness, File_Rail_Type])
    back_rail.get_prompt('Hide').set_formula('IF(Use_File_Rail,IF(File_Rail_Direction==1,Hide,True),True)',[Hide, Use_File_Rail,File_Rail_Type,File_Rail_Direction])

def add_wine_rack_support(assembly):
    support = assembly.add_assembly_from_file(PART_WITH_EDGEBANDING)
    support = sn_types.Part(support)
    support.set_name("Support")
    support.cutpart("Shelf")
    support.edgebanding('Edge',l1 = True)
    return support
            
def add_visual_shelf_holes(assembly):
    shelf_holes = assembly.add_assembly_from_file(ADJ_MACHINING)
    shelf_holes = sn_types.Part(shelf_holes)
    shelf_holes.set_name("Adjustable Shelf Holes")
    return shelf_holes

def add_sliding_shelf(assembly):
    shelf = assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING)
    shelf = sn_types.Part(shelf)
    props = shelf.obj_bp.sn_closets
    props.is_sliding_shelf_bp = True
    shelf.obj_bp.snap.comment_2 = "1013"
    shelf.set_name("Sliding Shelf")
    shelf.rot_x(value = 0)
    shelf.rot_y(value = 0)
    shelf.rot_z(value = 0)
    shelf.cutpart("Shelf")
    shelf.edgebanding('Edge',l2 = True)
    return shelf

def add_divider(assembly):
    divider = assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING)
    divider = sn_types.Part(divider)
    divider.obj_bp.snap.comment_2 = "1027"
    divider.set_name("Divider")
    divider.cutpart("Shoe_Cubby")
    divider.edgebanding("Edge",l1 = True)
    props = divider.obj_bp.sn_closets
    props.is_divider_bp = True
    return divider

def add_applied_top(assembly):
    top = assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING)
    top = sn_types.Part(top)
    top.obj_bp.snap.comment_2 = "1024"
    props = top.obj_bp.sn_closets
    props.is_shelf_bp = True
    top.set_name("Top")
    top.cutpart("Shelf")
    top.edgebanding("Edge",l2 = True)    
    return top

def add_toe_kick_radius(assembly):
    kick = assembly.add_assembly_from_file(BENDING_PART)
    kick = sn_types.Part(kick)
    props = kick.obj_bp.sn_closets
    props.is_toe_kick_bp = True
    kick.set_name("Toe Kick")
    kick.cutpart("Toe_Kick")
    return kick

def add_shelf_and_rod_cleat(assembly):
    cleat = assembly.add_assembly_from_file(PART_WITH_FRONT_EDGEBANDING)
    cleat = sn_types.Part(cleat)
    props = cleat.obj_bp.sn_closets
    props.is_shelf_and_rod_cleat_bp = True
    cleat.set_name("Cleat")
    cleat.cutpart("Shelf")
    cleat.edgebanding("Edge",l1 = True,w2 = True)    
    return cleat

def add_shelf_rod_cleat_fe(assembly):
    cleat = assembly.add_assembly_from_file(CHAMFERED_PART)
    cleat = sn_types.Part(cleat)
    props = cleat.obj_bp.sn_closets
    props.is_shelf_and_rod_fe_cleat_bp = True
    cleat.set_name("Cleat FE")
    cleat.cutpart("Shelf")
    cleat.edgebanding("Edge",l2 = True,w2 = True)    
    return cleat

def add_frame(assembly):
    frame = assembly.add_assembly_from_file(PART_WITH_EDGEBANDING)
    frame = sn_types.Part(frame)
    frame.set_name("Frame")
    frame.cutpart("Panel")
    frame.edgebanding("Edge",l2 = True)
    return frame

def add_island_countertop(assembly):
    island_ctop = assembly.add_assembly_from_file(ISLAND_COUNTER_TOP)
    island_ctop = sn_types.Part(island_ctop) 
    props = island_ctop.obj_bp.sn_closets
    props.is_countertop_bp = True
    island_ctop.set_name("Countertop Deck")
    island_ctop.material("Countertop_Surface")
    return island_ctop

def add_ironing_board_door_front(assembly):
    door = assembly.add_assembly_from_file(FACE)
    door = sn_types.Part(door)
    door.set_name("Door")
    door.cutpart("Slab_Door")
    door.edgebanding('Edge',l1 = True, w1 = True, l2 = True, w2 = True)
    door.add_prompt("Door Type", 'COMBOBOX', 0, ['Base','Tall','Upper'])
    door.add_prompt("Door Swing", 'COMBOBOX', 0, ['Left','Right','Top','Bottom'])
    door.add_prompt("No Pulls", 'CHECKBOX', False)
    door.obj_bp['IS_DOOR'] = True
    obj_props = door.obj_bp.sn_closets
    obj_props.is_ironing_board_door_front_bp = True
    obj_props.door_type = 'FLAT'
    return door

def add_round_hanging_rod(assembly):
    opts = bpy.context.scene.sn_closets.closet_options
    rod = sn_types.Part(assembly.add_assembly_from_file(ROUND_HANGING_ROD))
    assembly.add_assembly(rod)
    rod.obj_bp["IS_BP_ASSEMBLY"] = True
    rod.obj_bp.snap.comment_2 = "1015"
    rod.set_name("Round Hang Rod")
    rod.solid_stock("Round Hanging Rod")
    rod.material("Rod_Finish")
    rod.loc_z(value=sn_unit.inch(1)) # SET MATERIAL THICKNESS
    props = rod.obj_bp.sn_closets
    props.is_hanging_rod = True
    return rod

def add_oval_hanging_rod(assembly):
    opts = bpy.context.scene.sn_closets.closet_options    
    rod = sn_types.Part(assembly.add_assembly_from_file(OVAL_HANGING_ROD))
    assembly.add_assembly(rod)
    rod.obj_bp["IS_BP_ASSEMBLY"] = True
    rod.obj_bp.snap.comment_2 = "1015"
    rod.set_name("Oval Hang Rod")
    rod.solid_stock("Oval Hanging Rod")
    rod.material("Rod_Finish")
    rod.dim_y(value=sn_unit.inch(.5))
    rod.dim_z(value=sn_unit.inch(-1)) # SET MATERIAL THICKNESS
    props = rod.obj_bp.sn_closets
    props.is_hanging_rod = True
    return rod

def add_hangers(assembly):
    hangers = sn_types.Part(assembly.add_assembly_from_file(HANGERS))
    assembly.add_assembly(hangers)
    hangers.set_name("Hangers")
    hangers.set_material_pointers("Chrome", "Hanger Metal")
    hangers.set_material_pointers("Hanger_Wood", "Hanger Wood")
    return hangers

def add_spacer(assembly):
    spacer = assembly.add_assembly_from_file(SPACER)
    spacer = sn_types.Part(spacer)
    spacer.set_name("Spacer")
    props = spacer.obj_bp.sn_closets
    props.is_spacer_bp = True   
    return spacer

def add_fluted_molding(assembly):
    flute = assembly.add_assembly_from_file(FLUTED_PART)
    flute = sn_types.Part(flute)
    props = flute.obj_bp.sn_closets
    props.is_fluted_filler_bp = True
    flute.set_name("Fluted Part")
    flute.material("Closet_Part_Surfaces")
    return flute

def add_ironing_board_drawer(assembly):
    IBDR_1 = assembly.add_assembly_from_file(IB_DRAWER)
    IBDR_1 = sn_types.Part(IBDR_1)
    IBDR_1.set_name("IB-DR")
    return IBDR_1

def add_ironing_board_door(assembly):
    IBF_1 = assembly.add_assembly_from_file(IBF_IRONING_BOARD)
    IBF_1 = sn_types.Part(IBF_1)
    IBF_1.set_name("IBF")
    return IBF_1

def add_rosette(assembly):
    rosette = assembly.add_object(ROSETTE)
    return rosette

def add_section_opening(assembly):
    opening = assembly.add_opening()
    props = opening.obj_bp.sn_closets
    props.opening_type = "SECTION"
    opening.set_name("Opening")
    opening.add_prompt("Left Side Thickness", 'DISTANCE', sn_unit.inch(.75))
    opening.add_prompt("Right Side Thickness", 'DISTANCE', sn_unit.inch(.75))
    opening.add_prompt("Top Thickness", 'DISTANCE', sn_unit.inch(.75))
    opening.add_prompt("Bottom Thickness", 'DISTANCE', sn_unit.inch(.75))
    return opening

def add_opening(assembly):
    opening = assembly.add_opening()
    opening.set_name("Opening")
    opening.add_prompt("Left Side Thickness", 'DISTANCE', sn_unit.inch(.75))
    opening.add_prompt("Right Side Thickness", 'DISTANCE', sn_unit.inch(.75))
    opening.add_prompt("Top Thickness", 'DISTANCE', sn_unit.inch(.75))
    opening.add_prompt("Bottom Thickness", 'DISTANCE', sn_unit.inch(.75))
    return opening


def add_garage_rail(assembly):
    rail = sn_types.Part(assembly.add_assembly_from_file(GARAGE_RAIL))
    assembly.add_assembly(rail)
    rail.obj_bp.snap.comment_2 = ""
    rail.set_name("Garage Rail")
    return rail


def add_plastic_leg(assembly):
    plastic_leg = sn_types.Part(assembly.add_assembly_from_file(PLASTIC_LEG))
    assembly.add_assembly(plastic_leg)
    plastic_leg.obj_bp['IS_BP_GARAGE_LEG'] = True
    plastic_leg.obj_bp['IS_BP_PLASTIC_LEG'] = True
    plastic_leg.obj_bp.snap.comment_2 = ""
    plastic_leg.set_name("Plastic Leg")
    return plastic_leg


def add_metal_leg(assembly):
    metal_leg = sn_types.Part(assembly.add_assembly_from_file(METAL_LEG))
    assembly.add_assembly(metal_leg)
    metal_leg.obj_bp['IS_BP_GARAGE_LEG'] = True
    metal_leg.obj_bp['IS_BP_METAL_LEG'] = True
    metal_leg.obj_bp.snap.comment_2 = ""
    metal_leg.set_name("Metal Leg")
    return metal_leg
