from mv import unit
from . import mv_closet_defaults as props_closet

USE_DADO_FOR_LOCK_SHELF = False
USE_DOWELS_FOR_LOCK_SHELF = False
USE_SCREWS_FOR_LOCK_SHELF = False
USE_CAMS_FOR_LOCK_SHELF = True

USE_DADO_FOR_DIVISION = False
USE_DOWELS_FOR_DIVISION = True
USE_SCREWS_FOR_DIVISION = False
USE_CAMS_FOR_DIVISION = False

CORNERNOTCH_TOOL= "101"
CHAMFER_TOOL= "101"

ROUTER_LEAD = unit.inch(.25)
DADO_WIDTH_GAP = unit.inch(.01)
DADO_DEPTH_GAP = unit.inch(.125)
DADO_PANEL_PENETRATION = unit.inch(.25)

ADJ_SHELF_BORE_DEPTH = unit.inch(.5)
ADJ_SHELF_BORE_DIA = 5

DOWEL_DIM_TO_FIRST_AND_LAST_HOLE = unit.inch(1)
DOWEL_DRILL_FACE_DIA = 5
DOWEL_DRILL_FACE_DEPTH = unit.inch(.5)
DOWEL_DRILL_EDGE_DIA = 5
DOWEL_DRILL_EDGE_DEPTH = unit.inch(.5)
DOWEL_DISTANCE_BETWEEN_HOLES = unit.inch(5)

SCREW_DIM_TO_FIRST_AND_LAST_HOLE = unit.inch(1)
SCREW_DRILL_FACE_DIA = 5
SCREW_DRILL_FACE_DEPTH = unit.inch(.5)
SCREW_DRILL_EDGE_DIA = 5
SCREW_DRILL_EDGE_DEPTH = unit.inch(.5)
SCREW_DISTANCE_BETWEEN_HOLES = unit.inch(5)

CAM_EDGE_BORE_DIA = 5
CAM_EDGE_BORE_DEPTH = unit.inch(.5)
CAM_FACE_BORE_DIA = 5
CAM_FACE_BORE_DIA_2 = 20
CAM_FACE_BORE_DEPTH = unit.inch(.5)
CAM_FACE_BORE_DEPTH_2 = unit.inch(.5)
CAM_BACKSET = unit.inch(.354)
CAM_SETBACK_FROM_FRONT_AND_REAR = unit.inch(1)

def add_shelf_machining(shelf,product=None,index=1,cam_face='5'):
    default_props = props_closet.get_scene_props().closet_defaults
    machining = default_props.machining_defaults
    
    if machining.add_machining:
        if machining.use_associative_drilling:
            if machining.use_cams:
                add_cams(shelf)
            if machining.use_dowels:
                add_dowel_drilling(shelf)
        else:
            add_32mm_shelf_machining(shelf)

def add_associative_cams_for_shelves(part,cam_face='5'):
    default_props = props_closet.get_scene_props().closet_defaults
    machining_props = default_props.machining_defaults
    
    Width = part.get_var('dim_y','Width')
    
    tokens = []
    tokens.append(part.add_machine_token('Left Cam Drilling' ,'CAMLOCK','3'))
    tokens.append(part.add_machine_token('Right Cam Drilling' ,'CAMLOCK','4'))
    
    for token in tokens:
        token[1].hole_locations[0] = machining_props.dim_to_first_hole
        token[1].add_driver(token[0],'hole_locations','fabs(Width)-' + str(machining_props.dim_to_last_hole),[Width],index=1)
        token[1].edge_bore_depth = machining_props.cam_bore_edge_depth
        token[1].edge_bore_dia = machining_props.cam_bore_edge_dia
        token[1].face_bore_depth = machining_props.cam_bore_face_depth
        token[1].face_bore_dia = machining_props.cam_bore_face_dia
        token[1].face_bore_depth_2 = machining_props.cam_depth
        token[1].face_bore_dia_2 = machining_props.cam_dia
        token[1].backset = machining_props.cam_backset
        token[1].cam_face = cam_face

def add_division_machining(division):
    if USE_DADO_FOR_DIVISION:
        add_dado(division)
    if USE_DOWELS_FOR_DIVISION:
        add_dowel_drilling(division)
    if USE_SCREWS_FOR_DIVISION:
        add_screw_drilling(division)
    if USE_CAMS_FOR_DIVISION:
        add_cams(division)

def add_dado(part):
    
    Part_Thickness = part.get_var('dim_z','Part_Thickness')
    
    tokens = []
    tokens.append(part.add_machine_token('Left Dado' ,'DADO','3'))
    tokens.append(part.add_machine_token('Right Dado' ,'DADO','4'))

    for token in tokens:
        token[1].lead_in = ROUTER_LEAD
        token[1].lead_out = ROUTER_LEAD
        token[1].beginning_depth = DADO_PANEL_PENETRATION + DADO_DEPTH_GAP
        token[1].add_driver(token[0],'double_pass','Part_Thickness+' + str(DADO_WIDTH_GAP),[Part_Thickness])
        token[1].panel_penetration = DADO_PANEL_PENETRATION
        
def add_drawer_bottom_dado(part):
    
    Part_Thickness = part.get_var('dim_z','Part_Thickness')
    
    tokens = []
    tokens.append(part.add_machine_token('Left Dado' ,'DADO','3'))
    tokens.append(part.add_machine_token('Right Dado' ,'DADO','4'))
    tokens.append(part.add_machine_token('Front Dado' ,'DADO','1'))
    tokens.append(part.add_machine_token('Back Dado' ,'DADO','2'))
    
    for token in tokens:
        token[1].lead_in = ROUTER_LEAD
        token[1].lead_out = ROUTER_LEAD
        token[1].beginning_depth = DADO_PANEL_PENETRATION + DADO_DEPTH_GAP
        token[1].add_driver(token[0],'double_pass','Part_Thickness+' + str(DADO_WIDTH_GAP),[Part_Thickness])
        token[1].panel_penetration = DADO_PANEL_PENETRATION        
        
def add_cams(part,cam_face='5'):
    Width = part.get_var('dim_y','Width')
    
    tokens = []
    tokens.append(part.add_machine_token('Left Cam Drilling' ,'CAMLOCK','3'))
    tokens.append(part.add_machine_token('Right Cam Drilling' ,'CAMLOCK','4'))
    
    for token in tokens:
        token[1].hole_locations[0] = CAM_SETBACK_FROM_FRONT_AND_REAR
        token[1].add_driver(token[0],'hole_locations','fabs(Width)-' + str(CAM_SETBACK_FROM_FRONT_AND_REAR),[Width],index=1)
        token[1].edge_bore_depth = CAM_EDGE_BORE_DEPTH
        token[1].edge_bore_dia = CAM_EDGE_BORE_DIA
        token[1].face_bore_depth = CAM_FACE_BORE_DEPTH
        token[1].face_bore_dia = CAM_FACE_BORE_DIA
        token[1].face_bore_depth_2 = CAM_FACE_BORE_DEPTH_2
        token[1].face_bore_dia_2 = CAM_FACE_BORE_DIA_2
        token[1].backset = CAM_BACKSET
        token[1].cam_face = cam_face

def add_adj_shelf_machining(part,insert):
    
#     Width = insert.get_var('dim_x','Width')
    Height = insert.get_var('dim_z','Height')
#     Depth = insert.get_var('dim_y','Depth')
    Part_Width = part.get_var('dim_y','Part_Width')
    Part_Z_Loc = part.get_var('loc_z','Part_Z_Loc')
#     Adj_Shelf_Setback = insert.get_var("Adj Shelf Setback")
    Space_From_Front = insert.get_var("Space From Front")
    Space_From_Rear = insert.get_var("Space From Rear")
    Space_From_Top = insert.get_var("Space From Top")
    Space_From_Bottom = insert.get_var("Space From Bottom")
    Shelf_Hole_Spacing = insert.get_var("Shelf Hole Spacing")
    Shelf_Clip_Gap = insert.get_var("Shelf Clip Gap")
#     Adj_Shelf_Qty = insert.get_var("Adj Shelf Qty")
    
    tokens = []
    tokens.append(part.add_machine_token('Left Shelf Drilling' ,'SHELF','3'))
    tokens.append(part.add_machine_token('Right Shelf Drilling' ,'SHELF','4'))
    
    for token in tokens:
        token[1].add_driver(token[0],'space_from_bottom','Part_Z_Loc-Space_From_Bottom',[Part_Z_Loc,Space_From_Bottom])
        token[1].add_driver(token[0],'dim_to_first_row','Space_From_Front',[Space_From_Front])
        token[1].face_bore_depth = ADJ_SHELF_BORE_DEPTH
        token[1].add_driver(token[0],'space_from_top','Height-Part_Z_Loc-Space_From_Top',[Height,Part_Z_Loc,Space_From_Top])
        token[1].add_driver(token[0],'dim_to_second_row','fabs(Part_Width)-Space_From_Rear',[Part_Width,Space_From_Rear])
        token[1].face_bore_dia = ADJ_SHELF_BORE_DIA
        token[1].add_driver(token[0],'shelf_hole_spacing','Shelf_Hole_Spacing',[Shelf_Hole_Spacing])
        token[1].add_driver(token[0],'shelf_clip_gap','Shelf_Clip_Gap',[Shelf_Clip_Gap])
        token[1].reverse_direction = False

def add_32mm_shelf_machining(part):
    default_props = props_closet.get_scene_props().closet_defaults
    machining = default_props.machining_defaults    
    
    Width = part.get_var('dim_y','Width')
    Length = part.get_var('dim_x','Length')
    Is_Locked_Shelf = part.get_var('Is Locked Shelf')
    Drill_On_Top = part.get_var('Drill On Top')
    Remove_Left_Holes = part.get_var('Remove Left Holes')
    Remove_Right_Holes = part.get_var('Remove Right Holes')
    
    obj, left_token = part.add_machine_token('Left Drilling' ,'BORE','5')
    left_token.add_driver(obj,'is_disabled','IF(Is_Locked_Shelf,IF(Remove_Left_Holes,True,False),True)',[Is_Locked_Shelf,Remove_Left_Holes])
    left_token.add_driver(obj,'face','IF(Drill_On_Top,5,4)',[Drill_On_Top])
    left_token.dim_in_x = machining.cam_backset
    left_token.dim_in_y = machining.dim_to_first_hole
    left_token.dim_in_z = machining.cam_depth
    left_token.face_bore_dia = machining.cam_dia
    left_token.end_dim_in_x  = machining.cam_backset
    left_token.add_driver(obj,'end_dim_in_y','fabs(Width)-' + str(machining.dim_to_last_hole),[Width])
    left_token.add_driver(obj,'distance_between_holes','fabs(Width)-(' + str(machining.dim_to_first_hole+machining.dim_to_last_hole) + ')',[Width])
    left_token.associative_dia = 0
    left_token.associative_depth = 0
    
    obj, right_token = part.add_machine_token('Right Drilling' ,'BORE','5')
    right_token.add_driver(obj,'is_disabled','IF(Is_Locked_Shelf,IF(Remove_Right_Holes,True,False),True)',[Is_Locked_Shelf,Remove_Right_Holes])
    right_token.add_driver(obj,'face','IF(Drill_On_Top,5,4)',[Drill_On_Top])
    right_token.add_driver(obj,'dim_in_x','Length-' + str(machining.cam_backset),[Length])
    right_token.dim_in_z = machining.cam_depth
    right_token.dim_in_y = machining.dim_to_first_hole
    right_token.face_bore_dia = machining.cam_dia
    right_token.add_driver(obj,'end_dim_in_x','Length-' + str(machining.cam_backset),[Length])
    right_token.add_driver(obj,'end_dim_in_y','fabs(Width)-' + str(machining.dim_to_last_hole),[Width])
    right_token.add_driver(obj,'distance_between_holes','fabs(Width)-(' + str(machining.dim_to_first_hole+machining.dim_to_last_hole) + ')',[Width])
    right_token.associative_dia = 0
    right_token.associative_depth = 0

def add_dowel_drilling(part):
    Width = part.get_var('dim_y','Width')
    
    tokens = []
    tokens.append(part.add_machine_token('Left Dado Drilling' ,'CONST','3'))
    tokens.append(part.add_machine_token('Right Dado Drilling' ,'CONST','4'))
    
    for token in tokens:
        token[1].dim_to_first_const_hole = DOWEL_DIM_TO_FIRST_AND_LAST_HOLE
        token[1].add_driver(token[0],'dim_to_last_const_hole','fabs(Width)-' + str(DOWEL_DIM_TO_FIRST_AND_LAST_HOLE),[Width])
        token[1].edge_bore_depth = DOWEL_DRILL_EDGE_DEPTH
        token[1].edge_bore_dia = DOWEL_DRILL_EDGE_DIA
        token[1].face_bore_depth = DOWEL_DRILL_FACE_DEPTH
        token[1].face_bore_dia = DOWEL_DRILL_FACE_DIA
        token[1].distance_between_holes = DOWEL_DISTANCE_BETWEEN_HOLES
        
def add_screw_drilling(part):
    Width = part.get_var('dim_y','Width')
    
    tokens = []
    tokens.append(part.add_machine_token('Left Screw Drilling' ,'CONST','3'))
    tokens.append(part.add_machine_token('Right Screw Drilling' ,'CONST','4'))
    
    for token in tokens:
        token[1].dim_to_first_const_hole = SCREW_DIM_TO_FIRST_AND_LAST_HOLE
        token[1].add_driver(token[0],'dim_to_last_const_hole','fabs(Width)-' + str(SCREW_DIM_TO_FIRST_AND_LAST_HOLE),[Width])
        token[1].edge_bore_depth = SCREW_DRILL_EDGE_DEPTH
        token[1].edge_bore_dia = SCREW_DRILL_EDGE_DIA
        token[1].face_bore_depth = SCREW_DRILL_FACE_DEPTH
        token[1].face_bore_dia = SCREW_DRILL_FACE_DIA
        token[1].distance_between_holes = SCREW_DISTANCE_BETWEEN_HOLES  
        
def add_rear_notches(part,product):
    loc_z = part.get_var("loc_z")
    First_Rear_Notch_Height = product.get_var('First Rear Notch Height')
    First_Rear_Notch_Depth = product.get_var('First Rear Notch Depth')
    Second_Rear_Notch_Height = product.get_var('Second Rear Notch Height')
    Second_Rear_Notch_Depth = product.get_var('Second Rear Notch Depth')
    Panel_Thickness = product.get_var('Panel Thickness')
    
    first_notch = part.add_machine_token('First Rear Notch' ,'CORNERNOTCH','5','3')
    first_notch[1].add_driver(first_notch[0],'is_disabled','IF(OR(First_Rear_Notch_Height==0,loc_z>INCH(1)),True,False)',[First_Rear_Notch_Height,loc_z])
    first_notch[1].add_driver(first_notch[0],'dim_in_x','First_Rear_Notch_Height',[First_Rear_Notch_Height])
    first_notch[1].add_driver(first_notch[0],'dim_in_y','First_Rear_Notch_Depth',[First_Rear_Notch_Depth])
    first_notch[1].add_driver(first_notch[0],'dim_in_z','Panel_Thickness',[Panel_Thickness])
    first_notch[1].lead_in = ROUTER_LEAD
    first_notch[1].tool_number = CORNERNOTCH_TOOL
        
    second_notch = part.add_machine_token('Second Rear Notch' ,'CORNERNOTCH','5','3')
    second_notch[1].add_driver(second_notch[0],'is_disabled','IF(OR(Second_Rear_Notch_Height==0,loc_z>INCH(1)),True,False)',[Second_Rear_Notch_Height,loc_z])
    second_notch[1].add_driver(second_notch[0],'dim_in_x','Second_Rear_Notch_Height',[Second_Rear_Notch_Height])
    second_notch[1].add_driver(second_notch[0],'dim_in_y','First_Rear_Notch_Depth+Second_Rear_Notch_Depth',[First_Rear_Notch_Depth,Second_Rear_Notch_Depth])
    second_notch[1].add_driver(second_notch[0],'dim_in_z','Panel_Thickness',[Panel_Thickness])
    second_notch[1].lead_in = ROUTER_LEAD
    second_notch[1].tool_number = CORNERNOTCH_TOOL
    
def add_top_chamfers(part,product):
    Front_Angle_Height = product.get_var('Front Angle Height')
    Front_Angle_Depth = product.get_var('Front Angle Depth')
    Rear_Angle_Height = product.get_var('Rear Angle Height')
    Rear_Angle_Depth = product.get_var('Rear Angle Depth')
    Panel_Thickness = product.get_var('Panel Thickness')
    
    front_chamfer = part.add_machine_token('Front Chamfer' ,'CHAMFER','5','7')
    front_chamfer[1].add_driver(front_chamfer[0],'is_disabled','IF(Front_Angle_Height==0,True,False)',[Front_Angle_Height])
    front_chamfer[1].add_driver(front_chamfer[0],'dim_in_x','Front_Angle_Height',[Front_Angle_Height])
    front_chamfer[1].add_driver(front_chamfer[0],'dim_in_y','Front_Angle_Depth',[Front_Angle_Depth])
    front_chamfer[1].add_driver(front_chamfer[0],'dim_in_z','Panel_Thickness',[Panel_Thickness])
    front_chamfer[1].lead_in = ROUTER_LEAD
    front_chamfer[1].tool_number = CHAMFER_TOOL
        
    rear_chamfer = part.add_machine_token('Rear Chamfer' ,'CHAMFER','5','5')
    rear_chamfer[1].add_driver(rear_chamfer[0],'is_disabled','IF(Rear_Angle_Height==0,True,False)',[Rear_Angle_Height])
    rear_chamfer[1].add_driver(rear_chamfer[0],'dim_in_x','Rear_Angle_Height',[Rear_Angle_Height])
    rear_chamfer[1].add_driver(rear_chamfer[0],'dim_in_y','Rear_Angle_Depth',[Rear_Angle_Depth])
    rear_chamfer[1].add_driver(rear_chamfer[0],'dim_in_z','Panel_Thickness',[Panel_Thickness])
    rear_chamfer[1].lead_in = ROUTER_LEAD
    rear_chamfer[1].tool_number = CHAMFER_TOOL
