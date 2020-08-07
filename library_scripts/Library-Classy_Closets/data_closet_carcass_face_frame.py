import bpy
import math
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_lists

ASSEMBLY_DIR = path.join(common_parts.LIBRARY_DATA_DIR,"Closet Assemblies")
CLOSET_PANEL = path.join(ASSEMBLY_DIR,"Closet Panel.blend")
PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with Edgebanding.blend")
PART_WITH_FRONT_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with Front Edgebanding.blend")
PART_WITH_NO_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with No Edgebanding.blend")
LINE_BORE = path.join(ASSEMBLY_DIR,"Line Bore Holes.blend")

def update_closet_height(self,context):
    ''' EVENT changes height for all closet openings
    '''
    self.Opening_1_Height = self.height
    self.Opening_2_Height = self.height
    self.Opening_3_Height = self.height
    self.Opening_4_Height = self.height
    self.Opening_5_Height = self.height
    self.Opening_6_Height = self.height
    self.Opening_7_Height = self.height
    self.Opening_8_Height = self.height
    obj_product_bp = utils.get_bp(context.active_object,'PRODUCT')
    product = fd_types.Assembly(obj_product_bp)
    product.obj_z.location.z = unit.millimeter(float(self.height))
    
def add_opening_prompts(product):
    props = props_closet.get_scene_props().closet_defaults
    
    product.add_tab(name='Opening Widths',tab_type='CALCULATOR',calc_type="XDIM") #0
    product.add_tab(name='Carcass Options',tab_type='VISIBLE') #1
    
    if product.is_hanging:
        floor_mounted = False
        panel_height = props.hanging_panel_height
    else:
        floor_mounted = True
        panel_height = props.panel_height
    
    for i in range(1,product.opening_qty+1):
        product.add_prompt(name="Opening " + str(i) + " Width",
                        prompt_type='DISTANCE',
                        value=0,
                        tab_index=0,
                        equal=True)
        
        product.add_prompt(name="Opening " + str(i) + " Depth",
                        prompt_type='DISTANCE',
                        value=product.depth,
                        tab_index=1)
        
        product.add_prompt(name="Opening " + str(i) + " Height",
                        prompt_type='DISTANCE',
                        value=unit.millimeter(float(panel_height)),
                        tab_index=1)

        product.add_prompt(name="Opening " + str(i) + " Floor Mounted",
                           prompt_type='CHECKBOX',
                           value=floor_mounted,
                           tab_index=1)
        
def add_common_closet_prompts(product):
    props = props_closet.get_scene_props()
    
    product.add_prompt(name="Left End Condition",prompt_type='COMBOBOX',items=['EP','WP','CP','OFF'],value=1,tab_index=1,columns=4)
    product.add_prompt(name="Right End Condition",prompt_type='COMBOBOX',items=['EP','WP','CP','OFF'],value=1,tab_index=1,columns=4)
    product.add_prompt(name="Left Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=1)
    product.add_prompt(name="Right Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=1)
    product.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value=props.closet_defaults.toe_kick_height,tab_index=1)
    product.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value=props.closet_defaults.toe_kick_setback,tab_index=1)
    product.add_prompt(name="Add Backing",prompt_type='CHECKBOX',value=False,tab_index=1)
    product.add_prompt(name="Front Angle Height",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="Front Angle Depth",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="Rear Angle Height",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="Rear Angle Depth",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="First Rear Notch Height",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="First Rear Notch Depth",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="Second Rear Notch Height",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="Second Rear Notch Depth",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
    product.add_prompt(name="Face Frame Width",prompt_type='DISTANCE',value=unit.inch(2.125),tab_index=1)
    
    for i in range(1,product.opening_qty+1):
        product.add_prompt(name="CTF Opening " + str(i),
                           prompt_type='CHECKBOX',
                           value=False,
                           tab_index=1)
    
    product.add_prompt(name="Cut to Fit Amount",prompt_type='DISTANCE',value=unit.inch(4),tab_index=1)    
    
    Left_End_Condition = product.get_var('Left End Condition')
    Right_End_Condition = product.get_var('Right End Condition')
    Left_Side_Thickness = product.get_var('Left Side Thickness')
    Right_Side_Thickness = product.get_var('Right Side Thickness')    
    Panel_Thickness = product.get_var('Panel Thickness')
    Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
    Right_Side_Wall_Filler = product.get_var('Right Side Wall Filler')
    sgi = product.get_var('cabinetlib.spec_group_index','sgi')
    
    product.prompt("Left Side Thickness", 'IF(Left_End_Condition!=3,THICKNESS(sgi,"Panel"),0)',[Left_End_Condition,sgi])
    product.prompt("Right Side Thickness", 'IF(Right_End_Condition!=3,THICKNESS(sgi,"Panel"),0)',[Right_End_Condition,sgi])
    product.prompt("Panel Thickness", 'THICKNESS(sgi,"Panel")',[sgi])
    
    product.calculator_deduction("Left_Side_Thickness+Right_Side_Thickness+Panel_Thickness*(" + str(product.opening_qty) +"-1)+Left_Side_Wall_Filler+Right_Side_Wall_Filler",
                                 [Left_Side_Thickness,Right_Side_Thickness,Panel_Thickness,Left_Side_Wall_Filler,Right_Side_Wall_Filler])    
    
def add_material_thickness_prompts(product):
    product.add_prompt(name="Panel Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    product.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    product.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    product.add_prompt(name="Back Thickness",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=1)
    product.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)

def add_machining_prompts(product):
    product.add_tab(name='Machining Options',tab_type='VISIBLE') #2
    
    for i in range(1,product.opening_qty+1):
        product.add_prompt(name="Add " + str(i) + " Cleat",
                        prompt_type='CHECKBOX',
                        value=0,
                        tab_index=2)
                    
        product.add_prompt(name="Cleat " + str(i) + " Location",
                        prompt_type='DISTANCE',
                        value=unit.inch(4),
                        tab_index=2)
                    
        product.add_prompt(name="Opening " + str(i) + " Stop LB",
                        prompt_type='DISTANCE',
                        value=0,
                        tab_index=2)
        
        product.add_prompt(name="Opening " + str(i) + " Start LB",
                        prompt_type='DISTANCE',
                        value=0,
                        tab_index=2)
        
        product.add_prompt(name="Opening " + str(i) + " Add Mid Drilling",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=2)
        
        product.add_prompt(name="Opening " + str(i) + " Drill Thru Left",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=2)
    
        product.add_prompt(name="Opening " + str(i) + " Drill Thru Right",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=2)
    
        product.add_prompt(name="Opening " + str(i) + " Remove Left Drill",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=2)
    
        product.add_prompt(name="Opening " + str(i) + " Remove Right Drill",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=2)

def set_panel_prompts(product, panel):
    Front_Angle_Height = product.get_var('Front Angle Height')
    Front_Angle_Depth = product.get_var('Front Angle Depth')
    Rear_Angle_Height = product.get_var('Rear Angle Height')
    Rear_Angle_Depth = product.get_var('Rear Angle Depth')
    First_Rear_Notch_Height = product.get_var('First Rear Notch Height')
    First_Rear_Notch_Depth = product.get_var('First Rear Notch Depth')
    Second_Rear_Notch_Height = product.get_var('Second Rear Notch Height')
    Second_Rear_Notch_Depth = product.get_var('Second Rear Notch Depth')
    
    panel.prompt("Front Chamfer Height",'Front_Angle_Height',[Front_Angle_Height])
    panel.prompt("Front Chamfer Depth",'Front_Angle_Depth',[Front_Angle_Depth])
    panel.prompt("Rear Chamfer Height",'Rear_Angle_Height',[Rear_Angle_Height])
    panel.prompt("Rear Chamfer Depth",'Rear_Angle_Depth',[Rear_Angle_Depth])
    panel.prompt("First Rear Notch Height",'First_Rear_Notch_Height',[First_Rear_Notch_Height])
    panel.prompt("First Rear Notch Depth",'First_Rear_Notch_Depth',[First_Rear_Notch_Depth])
    panel.prompt("Second Rear Notch Height",'Second_Rear_Notch_Height',[Second_Rear_Notch_Height])
    panel.prompt("Second Rear Notch Depth",'Second_Rear_Notch_Depth',[Second_Rear_Notch_Depth])
    
def add_sides(product):
    Product_Height = product.get_var('dim_z','Product_Height')
    Product_Width = product.get_var('dim_x','Product_Width')
    Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
    Right_Side_Wall_Filler = product.get_var('Right Side Wall Filler')
    Left_Side_Thickness = product.get_var('Left Side Thickness')
    Right_Side_Thickness = product.get_var('Right Side Thickness')
    Panel_Thickness = product.get_var('Panel Thickness')
    Depth_1 = product.get_var('Opening 1 Depth','Depth_1')
    Height_1 = product.get_var('Opening 1 Height','Height_1')
    Floor_1 = product.get_var('Opening 1 Floor Mounted','Floor_1')
    Last_Depth = product.get_var('Opening ' + str(product.opening_qty) + ' Depth',"Last_Depth")
    Last_Height = product.get_var('Opening ' + str(product.opening_qty) + ' Height',"Last_Height")
    Last_Floor = product.get_var('Opening ' + str(product.opening_qty) + ' Floor Mounted',"Last_Floor")
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Left_End_Condition = product.get_var('Left End Condition')
    Right_End_Condition = product.get_var('Right End Condition')
    Face_Frame_Width = product.get_var('Face Frame Width')
    Toe_Kick_Height = product.get_var('Toe Kick Height')

    left_filler = common_parts.add_filler(product)
    left_filler.x_dim('Height_1',[Height_1])
    left_filler.y_dim('-Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
    left_filler.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
    left_filler.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
    left_filler.y_loc('-Depth_1-IF(Add_Backing,Back_Thickness,0)',[Depth_1,Add_Backing,Back_Thickness])
    left_filler.z_loc('IF(Floor_1,0,Product_Height-Height_1)',[Floor_1,Product_Height,Height_1])
    left_filler.x_rot(value = 0)
    left_filler.y_rot(value = -90)
    left_filler.z_rot(value = -90)
    left_filler.prompt('Hide','IF(Left_Side_Wall_Filler==0,True,False)',[Left_Side_Wall_Filler])
    
    left_side = common_parts.add_panel(product)
    left_side.x_dim('Height_1',[Height_1])
    left_side.y_dim('-Depth_1',[Depth_1])
    left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
    left_side.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
    left_side.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
    left_side.z_loc('IF(Floor_1,0,Product_Height-Height_1)',[Floor_1,Product_Height,Height_1])
    left_side.x_rot(value = 0)
    left_side.y_rot(value = -90)
    left_side.z_rot(value = 0)
    left_side.prompt('Hide','IF(Left_End_Condition==3,True,False)',[Left_End_Condition])
    set_panel_prompts(product,left_side)

    right_filler = common_parts.add_filler(product)
    right_filler.x_dim('Last_Height',[Last_Height])
    right_filler.y_dim('Right_Side_Wall_Filler',[Right_Side_Wall_Filler])
    right_filler.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
    right_filler.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
    right_filler.y_loc('-Last_Depth-IF(Add_Backing,Back_Thickness,0)',[Last_Depth,Add_Backing,Back_Thickness])
    right_filler.z_loc('IF(Last_Floor,0,Product_Height-Last_Height)',[Last_Floor,Product_Height,Last_Height])
    right_filler.x_rot(value = 0)
    right_filler.y_rot(value = -90)
    right_filler.z_rot(value = -90)
    right_filler.prompt('Hide','IF(Right_Side_Wall_Filler==0,True,False)',[Right_Side_Wall_Filler])
    
    right_side = common_parts.add_panel(product)
    right_side.x_dim('Last_Height',[Last_Height])
    right_side.y_dim('-Last_Depth',[Last_Depth])
    right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
    right_side.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
    right_side.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
    right_side.z_loc('IF(Last_Floor,0,Product_Height-Last_Height)',[Last_Floor,Product_Height,Last_Height])
    right_side.x_rot(value = 0)
    right_side.y_rot(value = -90)
    right_side.z_rot(value = 0)
    right_side.prompt('Hide','IF(Right_End_Condition==3,True,False)',[Right_End_Condition])
    set_panel_prompts(product,right_side)

    left_frame = common_parts.add_frame(product)
    left_frame.x_dim('Height_1-Toe_Kick_Height-Panel_Thickness-Face_Frame_Width',[Height_1,Toe_Kick_Height,Panel_Thickness,Last_Height,Face_Frame_Width])
    left_frame.y_dim('-Face_Frame_Width',[Face_Frame_Width])
    left_frame.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
    left_frame.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
    left_frame.y_loc('-Depth_1-IF(Add_Backing,-Back_Thickness,0)',[Depth_1,Add_Backing,Back_Thickness])
    left_frame.z_loc('IF(Floor_1,Toe_Kick_Height+Panel_Thickness,Product_Height-Height_1)',[Floor_1,Toe_Kick_Height,Panel_Thickness,Product_Height,Height_1])
    left_frame.x_rot(value = 90)
    left_frame.y_rot(value = -90)
    left_frame.z_rot(value = 0)
    left_frame.prompt('Hide','IF(Left_End_Condition==3,True,False)',[Left_End_Condition])

    right_frame = common_parts.add_frame(product)
    right_frame.x_dim('Last_Height-Toe_Kick_Height-Panel_Thickness-Face_Frame_Width',[Toe_Kick_Height,Panel_Thickness,Last_Height,Face_Frame_Width])
    right_frame.y_dim('Face_Frame_Width',[Face_Frame_Width])
    right_frame.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
    right_frame.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
    right_frame.y_loc('-Depth_1-IF(Add_Backing,-Back_Thickness,0)',[Depth_1,Add_Backing,Back_Thickness])
    right_frame.z_loc('IF(Last_Floor,Toe_Kick_Height+Panel_Thickness,Product_Height-Last_Height)',[Last_Floor,Toe_Kick_Height,Panel_Thickness,Product_Height,Last_Height])
    right_frame.x_rot(value = 90)
    right_frame.y_rot(value = -90)
    right_frame.z_rot(value = 0)
    right_frame.prompt('Hide','IF(Right_End_Condition==3,True,False)',[Right_End_Condition])

def add_panel(product,index,previous_panel):
    PH = product.get_var('dim_z','PH')
    Width = product.get_var('Opening ' + str(index-1) + ' Width',"Width")
    Depth = product.get_var('Opening ' + str(index-1) + ' Depth',"Depth")
    H = product.get_var('Opening ' + str(index-1) + ' Height',"H")
    Floor = product.get_var('Opening ' + str(index-1) + ' Floor Mounted',"Floor")
    Next_Floor = product.get_var('Opening ' + str(index) + ' Floor Mounted',"Next_Floor")
    Next_Depth = product.get_var('Opening ' + str(index) + ' Depth',"Next_Depth")
    NH = product.get_var('Opening ' + str(index) + ' Height',"NH")
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Panel_Thickness = product.get_var('Panel Thickness')
    Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
    FFW = product.get_var('Face Frame Width','FFW')
    Toe_Kick_Height = product.get_var('Toe Kick Height')
    
    panel = common_parts.add_panel(product)
    if previous_panel:
        Prev_Panel_X = previous_panel.get_var("loc_x",'Prev_Panel_X')
        Left_Side_Thickness = product.get_var('Left_Side_Thickness')
        panel.x_loc('Prev_Panel_X+Panel_Thickness+Width',[Prev_Panel_X,Panel_Thickness,Width])
    else:
        Left_Side_Thickness = product.get_var('Left Side Thickness')
        panel.x_loc('Left_Side_Thickness+Width+Left_Side_Wall_Filler+Panel_Thickness',
                    [Left_Side_Thickness,Width,Left_Side_Wall_Filler,Panel_Thickness])
    panel.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
    panel.z_loc('min(IF(Floor,0,IF(Next_Floor,0,PH-H)),IF(Next_Floor,0,IF(Floor,0,PH-NH)))',
                [Floor,Next_Floor,H,PH,NH])
    panel.x_rot(value = 0)
    panel.y_rot(value = -90)
    panel.z_rot(value = 0)
    panel.x_dim('max(IF(Floor,H,IF(Next_Floor,PH,H)),IF(Next_Floor,NH,IF(Floor,PH,NH)))',
                [Floor,Next_Floor,PH,H,NH]) 
    panel.y_dim('-max(Depth,Next_Depth)',[Depth,Next_Depth])
    panel.z_dim('Panel_Thickness',[Panel_Thickness])
    set_panel_prompts(product,panel)
    default_props = props_closet.get_scene_props().closet_defaults
    if default_props.use_32mm_system:
        add_panel_drilling(panel,product,index + 1)
        
    frame = common_parts.add_frame(product)
    if previous_panel:
        Prev_Panel_X = previous_panel.get_var("loc_x",'Prev_Panel_X')
        Left_Side_Thickness = product.get_var('Left_Side_Thickness')
        frame.x_loc('Prev_Panel_X+Width+(FFW/2)+(Panel_Thickness/2)',[Prev_Panel_X,Panel_Thickness,Width,FFW])
    else:
        Left_Side_Thickness = product.get_var('Left Side Thickness')
        frame.x_loc('Left_Side_Thickness+Width+Left_Side_Wall_Filler+(FFW/2)+(Panel_Thickness/2)',
                    [Left_Side_Thickness,Width,Left_Side_Wall_Filler,Panel_Thickness,FFW])
    frame.y_loc('IF(Add_Backing,-max(Depth,Next_Depth)-Back_Thickness,-max(Depth,Next_Depth))',[Depth,Add_Backing,Back_Thickness,Next_Depth])
    frame.z_loc('min(IF(Floor,Toe_Kick_Height+Panel_Thickness,IF(Next_Floor,Toe_Kick_Height+Panel_Thickness,PH-H)),IF(Next_Floor,Toe_Kick_Height+Panel_Thickness,IF(Floor,Toe_Kick_Height+Panel_Thickness,PH-NH)))',
                [Floor,Panel_Thickness,Toe_Kick_Height,Next_Floor,H,PH,NH])
    frame.x_rot(value = 90)
    frame.y_rot(value = -90)
    frame.z_rot(value = 0)
    frame.x_dim('max(IF(Floor,H-Toe_Kick_Height-Panel_Thickness-FFW,IF(Next_Floor,PH,H-Toe_Kick_Height-Panel_Thickness-FFW)),IF(Next_Floor,NH-Toe_Kick_Height-Panel_Thickness-FFW,IF(Floor,PH-Toe_Kick_Height-Panel_Thickness-FFW,NH-Toe_Kick_Height-Panel_Thickness-FFW)))',
                [Floor,Next_Floor,PH,H,NH,Toe_Kick_Height,Panel_Thickness,FFW]) 
    frame.y_dim('FFW',[FFW])
    frame.z_dim('Panel_Thickness',[Panel_Thickness])
    set_panel_prompts(product,frame)

    return panel

def add_plant_on_top(product,i,panel):
    Product_Height = product.get_var('dim_z','Product_Height')
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Depth = product.get_var('Opening ' + str(i) + ' Depth','Depth')
    Height = product.get_var('Opening ' + str(i) + ' Height','Height')
    P_Depth = product.get_var('Opening ' + str(i-1) + ' Depth','P_Depth') 
    P_Height = product.get_var('Opening ' + str(i-1) + ' Height','P_Height')    
    N_Depth = product.get_var('Opening ' + str(i+1) + ' Depth','N_Depth') 
    N_Height = product.get_var('Opening ' + str(i+1) + ' Height','N_Height')       
    Floor = product.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Shelf_Thickness = product.get_var('Shelf Thickness')
    PT = product.get_var('Panel Thickness','PT')
    Rear_Angle_Depth = product.get_var('Rear Angle Depth')
    Front_Angle_Depth = product.get_var('Front Angle Depth')
    Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
    Right_Side_Wall_Filler = product.get_var('Right Side Wall Filler')
    
    top = common_parts.add_applied_top(product)
    if i == 1:
        # FIRST
        right_offset = "IF(AND(N_Depth==Depth,N_Height==Height),PT/2,IF(OR(N_Depth<Depth,N_Height<Height),PT,0))"
        top.x_loc(value = 0)
        top.x_dim('Width+Left_Side_Wall_Filler+PT+' + right_offset,[Width,Left_Side_Wall_Filler,Depth,N_Depth,N_Height,Height,PT])
    elif i == product.opening_qty:
        # LAST
        X_Loc = panel.get_var('loc_x','X_Loc')
        left_offset = "IF(AND(P_Depth==Depth,P_Height==Height),PT/2,IF(OR(P_Depth<Depth,P_Height<Height),PT,0))"
        top.x_loc("X_Loc-" + left_offset,[X_Loc,P_Depth,Depth,P_Height,Height,PT])
        top.x_dim('Width+Right_Side_Wall_Filler+PT+' + left_offset,[Width,Right_Side_Wall_Filler,Depth,P_Depth,P_Height,Height,PT])
    else:
        # MIDDLE
        X_Loc = panel.get_var('loc_x','X_Loc')
        left_offset = "IF(AND(P_Depth==Depth,P_Height==Height),PT/2,IF(OR(P_Depth<Depth,P_Height<Height),PT,0))"
        right_offset = "IF(AND(N_Depth==Depth,N_Height==Height),PT/2,IF(OR(N_Depth<Depth,N_Height<Height),PT,0))"
        top.x_loc("X_Loc-" + left_offset,[X_Loc,P_Depth,Depth,P_Height,Height,PT])
        top.x_dim('Width+' + right_offset + "+" + left_offset,[Width,Left_Side_Wall_Filler,Depth,N_Depth,N_Height,P_Height,P_Depth,Height,PT])
    
    top.y_loc('IF(Add_Backing,-Back_Thickness,0)-Rear_Angle_Depth',[Add_Backing,Back_Thickness,Rear_Angle_Depth])
    top.z_loc('IF(Floor,Height,Product_Height)',[Floor,Height,Product_Height])
    top.z_dim('Shelf_Thickness',[Shelf_Thickness])
    top.y_dim("-Depth+Rear_Angle_Depth+Front_Angle_Depth",[Depth,Rear_Angle_Depth,Front_Angle_Depth])
    top.x_rot(value = 0)
    top.y_rot(value = 0)
    top.z_rot(value = 0)

def add_shelf(product,i,panel,is_top=False):
    Product_Height = product.get_var('dim_z','Product_Height')
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Depth = product.get_var('Opening ' + str(i) + ' Depth','Depth')
    Prev_Depth = product.get_var('Opening ' + str(i - 1) + ' Depth','Prev_Depth')
    Next_Depth = product.get_var('Opening ' + str(i + 1) + ' Depth','Next_Depth')
    Height = product.get_var('Opening ' + str(i) + ' Height','Height')
    Floor = product.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Shelf_Thickness = product.get_var('Shelf Thickness')
    Toe_Kick_Height = product.get_var('Toe Kick Height')
    Rear_Angle_Depth = product.get_var('Rear Angle Depth')
    Front_Angle_Depth = product.get_var('Front Angle Depth')
    RN_1_H = product.get_var('First Rear Notch Height','RN_1_H')
    RN_1_D = product.get_var('First Rear Notch Depth','RN_1_D')
    RN_2_H = product.get_var('Second Rear Notch Height','RN_2_H')
    RN_2_D = product.get_var('Second Rear Notch Depth','RN_2_D')
    Face_Frame_Width = product.get_var('Face Frame Width')
    Left_Side_Thickness = product.get_var('Left Side Thickness')
    Panel_Thickness = product.get_var('Panel Thickness')
    
    top_frame = common_parts.add_frame(product)
    top_frame.z_dim('Shelf_Thickness',[Shelf_Thickness])
    top_frame.y_loc('-Depth-IF(Add_Backing,-Back_Thickness,0)',[Depth,Add_Backing,Back_Thickness])
    top_frame.x_rot(value = 90)
    top_frame.y_rot(value = 0)
    top_frame.z_rot(value = 0)
    
    shelf = common_parts.add_shelf(product)
    if panel:
        X_Loc = panel.get_var('loc_x','X_Loc')
        shelf.x_loc('X_Loc',[X_Loc])
        top_frame.x_loc('X_Loc-(Panel_Thickness/2)',[X_Loc,Panel_Thickness])
        if i == product.opening_qty:
            top_frame.x_dim('Width+Panel_Thickness+(Panel_Thickness/2)',[Width,Panel_Thickness])
        else:
            top_frame.x_dim('Width+Panel_Thickness',[Width,Panel_Thickness])
    else:
        Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
        shelf.x_loc('Left_Side_Wall_Filler+Left_Side_Thickness',[Left_Side_Wall_Filler,Left_Side_Thickness])
        top_frame.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler,Left_Side_Thickness])
        top_frame.x_dim('Width+Left_Side_Thickness+(Panel_Thickness/2)',[Width,Left_Side_Thickness,Panel_Thickness])
    
    if is_top:
        top_frame.z_loc('IF(Floor,Height,Product_Height)',[Floor,Height,Product_Height])
        top_frame.y_dim('-Face_Frame_Width',[Face_Frame_Width])
        shelf.y_loc('IF(Add_Backing,-Back_Thickness,0)-Rear_Angle_Depth',[Add_Backing,Back_Thickness,Rear_Angle_Depth])
        shelf.z_loc('IF(Floor,Height,Product_Height)',[Floor,Height,Product_Height])
        shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        shelf.y_dim("-Depth+Rear_Angle_Depth+Front_Angle_Depth",[Depth,Rear_Angle_Depth,Front_Angle_Depth])
    else:
        backing_inset = 'IF(Add_Backing,-Back_Thickness,0)'
        rear_notch_1_inset = "IF(Floor,IF(Toe_Kick_Height<RN_1_H,RN_1_D,0),0)"
        rear_notch_2_inset = "IF(Floor,IF(Toe_Kick_Height<RN_2_H,RN_2_D,0),0)"
        shelf.y_loc(backing_inset + "-" + rear_notch_1_inset + "-" + rear_notch_2_inset,[Floor,Add_Backing,Back_Thickness,Toe_Kick_Height,RN_1_H,RN_2_H,RN_1_D,RN_2_D])
        top_frame.y_dim('Face_Frame_Width',[Face_Frame_Width])
        top_frame.z_loc('IF(Floor,Toe_Kick_Height,Product_Height-Height)',[Floor,Toe_Kick_Height,Product_Height,Height])
        shelf.z_loc('IF(Floor,Toe_Kick_Height,Product_Height-Height)',[Floor,Toe_Kick_Height,Product_Height,Height])
        shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        shelf.y_dim("-Depth+" + rear_notch_1_inset + "+" + rear_notch_2_inset,[Floor,Depth,Toe_Kick_Height,RN_1_H,RN_2_H,RN_1_D,RN_2_D])
    shelf.x_rot(value = 0)
    shelf.y_rot(value = 0)
    shelf.z_rot(value = 0)
    shelf.x_dim('Width',[Width])

def add_toe_kick(product,i,panel):
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Depth = product.get_var('Opening ' + str(i) + ' Depth','Depth')
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Toe_Kick_Height = product.get_var('Toe Kick Height')
    Toe_Kick_Setback = product.get_var('Toe Kick Setback')
    Left_End_Condition = product.get_var('Left End Condition')
    Right_End_Condition = product.get_var('Right End Condition')
    Shelf_Thickness = product.get_var('Shelf Thickness')
    Floor_Mounted = product.get_var('Opening ' + str(i) + ' Floor Mounted','Floor_Mounted')
    
    if panel:
        X_Loc = panel.get_var('loc_x','X_Loc')
    else:
        X_Loc = product.get_var('Left Side Thickness','X_Loc')
    
    kick = product.add_assembly(PART_WITH_NO_EDGEBANDING)
    props = props_closet.get_object_props(kick.obj_bp)
    props.is_toe_kick_bp = True
    kick.set_name("Toe Kick " + str(i))
    kick.y_dim('-Toe_Kick_Height',[Toe_Kick_Height,Shelf_Thickness])
    kick.z_dim(value = unit.inch(.75))
    kick.y_loc('-Depth+Toe_Kick_Setback-IF(Add_Backing,Back_Thickness,0)',[Depth,Toe_Kick_Setback,Add_Backing,Back_Thickness])
    kick.z_loc(value = 0)
    kick.x_rot(value = -90)
    kick.y_rot(value = 0)
    kick.z_rot(value = 0)
    kick.cutpart("Toe_Kick")
    kick.prompt("Hide",'IF(Floor_Mounted,False,True)',[Floor_Mounted])
    
    if i == 1: #FIRST OPENING
        Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
        kick.x_dim("Width+IF(Left_End_Condition!=3,0,Toe_Kick_Setback)",[Width,Left_End_Condition,Toe_Kick_Setback])
        kick.x_loc("X_Loc-IF(Left_End_Condition!=3,0,Toe_Kick_Setback)+Left_Side_Wall_Filler",[X_Loc,Left_End_Condition,Toe_Kick_Setback,Left_Side_Wall_Filler])
    elif i == product.opening_qty: #LAST OPENING
        kick.x_dim("Width+IF(Right_End_Condition!=3,0,Toe_Kick_Setback)",[Width,Right_End_Condition,Toe_Kick_Setback])
        kick.x_loc('X_Loc',[X_Loc])
    else: #MIDDLE OPENING
        kick.x_dim("Width",[Width])
        kick.x_loc('X_Loc',[X_Loc])

def add_cleat(product,i,panel):
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Add_Cleat = product.get_var('Add ' + str(i) + ' Cleat','Add_Cleat')
    Cleat_Location = product.get_var('Cleat ' + str(i) + ' Location','Cleat_Location')
    Shelf_Thickness = product.get_var('Shelf Thickness')
    Cut_to_Fit_Amount = product.get_var("Cut to Fit Amount")
    Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
    
    if panel:
        X_Loc = panel.get_var('loc_x','X_Loc')
    else:
        X_Loc = product.get_var('Left Side Thickness','X_Loc')
    
    cleat = common_parts.add_cleat(product)
    cleat.y_loc(value = 0)
    cleat.z_loc('Cleat_Location',[Cleat_Location])
    cleat.x_rot(value = -90)
    cleat.y_rot(value = 0)
    cleat.z_rot(value = 0)
    cleat.y_dim(value=unit.inch(-3.64))
    cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])
    cleat.prompt('Hide','IF(Add_Cleat,False,True)',[Add_Cleat])
    if i == 1:
        cleat.x_loc('X_Loc+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
        cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
    elif i == product.opening_qty: #LAST OPENING
        cleat.x_loc('X_Loc',[X_Loc])
        cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
    else:
        cleat.x_loc('X_Loc',[X_Loc])
        cleat.x_dim('Width',[Width])

def add_closet_opening(product,i,panel):
    props = props_closet.get_scene_props().closet_defaults
    
    Product_Height = product.get_var('dim_z','Product_Height')
    Height = product.get_var('Opening ' + str(i) + ' Height','Height')
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Depth = product.get_var('Opening ' + str(i) + ' Depth','Depth')
    Floor = product.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Toe_Kick_Height = product.get_var('Toe Kick Height')
    Shelf_Thickness = product.get_var('Shelf Thickness')
    
    opening = common_parts.add_opening(product)
    
    if panel:
        X_Loc = panel.get_var('loc_x','X_Loc')
        opening.x_loc('X_Loc',[X_Loc])
    else:
        Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
        X_Loc = product.get_var('Left Side Thickness','X_Loc')
        opening.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])
    opening.y_loc('-Depth-IF(Add_Backing,Back_Thickness,0)',[Depth,Add_Backing,Back_Thickness])
    opening.z_loc('IF(Floor,Toe_Kick_Height+Shelf_Thickness,Product_Height-Height+Shelf_Thickness)',
                  [Floor,Toe_Kick_Height,Shelf_Thickness,Product_Height,Height])
    opening.x_rot(value = 0)
    opening.y_rot(value = 0)
    opening.z_rot(value = 0)
    opening.x_dim('Width',[Width])
    opening.y_dim("fabs(Depth)",[Depth])
    if props.use_plant_on_top:
        opening.z_dim('Height-Shelf_Thickness-IF(Floor,Toe_Kick_Height,0)',[Height,Shelf_Thickness,Floor,Toe_Kick_Height,Product_Height])
    else:
        opening.z_dim('Height-(Shelf_Thickness*2)-IF(Floor,Toe_Kick_Height,0)',[Height,Shelf_Thickness,Floor,Toe_Kick_Height,Product_Height])
    
def add_inside_dimension(product,i,panel):
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
    
    if panel:
        X_Loc = panel.get_var('loc_x','X_Loc')
    else:
        X_Loc = product.get_var('Left Side Thickness','X_Loc')
        
    dim = fd_types.Dimension()
    dim.parent(product.obj_bp)
    dim.start_z(value = unit.inch(-4))
    dim.start_y(value = unit.inch(4))
    if panel:
        dim.start_x('X_Loc',[X_Loc])
    else:
        dim.start_x('X_Loc+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
    dim.end_x('Width',[Width])
    dim.set_color('IF(Width>INCH(42),3,0)',[Width])

def add_backing(product,i,panel):
    scene_props = props_closet.get_scene_props().closet_defaults
    
    Product_Height = product.get_var('dim_z','Product_Height')
    Height = product.get_var('Opening ' + str(i) + ' Height','Height')
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Floor = product.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Toe_Kick_Height = product.get_var('Toe Kick Height')
    Shelf_Thickness = product.get_var('Shelf Thickness')
    Panel_Thickness = product.get_var('Panel Thickness')
    
    backing = common_parts.add_back(product)

    if panel:
        X_Loc = panel.get_var('loc_x','X_Loc')
        backing.x_loc('X_Loc-(Panel_Thickness/2)',[X_Loc,Panel_Thickness])
    else:
        Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
        X_Loc = product.get_var('Left Side Thickness','X_Loc')
        backing.x_loc('Left_Side_Wall_Filler+X_Loc-(Panel_Thickness/2)',[Left_Side_Wall_Filler,X_Loc,Panel_Thickness])
    backing.y_loc(value = 0)
    backing.z_loc('IF(Floor,Toe_Kick_Height+(Shelf_Thickness/2),Product_Height-Height+(Shelf_Thickness/2))',[Floor,Toe_Kick_Height,Shelf_Thickness,Product_Height,Height])
    backing.x_rot(value = -90)
    backing.y_rot(value = -90)
    backing.z_rot(value = 0)
    if scene_props.use_plant_on_top:
        backing.x_dim('Height-IF(Floor,Toe_Kick_Height,0)',[Height,Floor,Toe_Kick_Height,Shelf_Thickness])
    else:
        backing.x_dim('Height-IF(Floor,Toe_Kick_Height+Shelf_Thickness,Shelf_Thickness)',[Height,Floor,Toe_Kick_Height,Shelf_Thickness])
    backing.y_dim("Width+Panel_Thickness",[Width,Panel_Thickness])
    backing.z_dim('-Back_Thickness',[Back_Thickness])
    backing.prompt('Hide','IF(Add_Backing,False,True)',[Add_Backing])
    
def add_system_holes(product,i,panel):
    Product_Height = product.get_var('dim_z',"Product_Height")
    Width = product.get_var('Opening ' + str(i) + ' Width','Width')
    Height = product.get_var('Opening ' + str(i) + ' Height','Height')
    Depth = product.get_var('Opening ' + str(i) + ' Depth','Depth')
    Floor = product.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
    Add_Backing = product.get_var('Add Backing')
    Back_Thickness = product.get_var('Back Thickness')
    Left_End_Condition = product.get_var('Left End Condition')
    Right_End_Condition = product.get_var('Right End Condition')
    
    Stop_LB = product.get_var("Opening " + str(i) + " Stop LB",'Stop_LB')
    Start_LB = product.get_var("Opening " + str(i) + " Start LB",'Start_LB')
    Drill_Thru_Left = product.get_var("Opening " + str(i) + " Drill Thru Left",'Drill_Thru_Left')
    Drill_Thru_Right = product.get_var("Opening " + str(i) + " Drill Thru Right",'Drill_Thru_Right')
    Add_Mid = product.get_var("Opening " + str(i) + " Add Mid Drilling",'Add_Mid')
    Remove_Left = product.get_var("Opening " + str(i) + " Remove Left Drill",'Remove_Left')
    Remove_Right = product.get_var("Opening " + str(i) + " Remove Right Drill",'Remove_Right')
    Panel_Thickness = product.get_var('Panel Thickness')
    
    if panel:
        X_Loc = panel.get_var('loc_x','X_Loc')
    else:
        X_Loc = product.get_var('Left Side Thickness','X_Loc')
        
    ass_list = []
        
    lfb_holes = product.add_assembly(LINE_BORE)
    lfb_holes.set_name("Left Front Bottom Holes " + str(i))
    ass_list.append(lfb_holes)
    lrb_holes = product.add_assembly(LINE_BORE)
    lrb_holes.set_name("Left Rear Bottom Holes " + str(i))
    ass_list.append(lrb_holes)
    rfb_holes = product.add_assembly(LINE_BORE)
    rfb_holes.set_name("Right Front Bottom Holes " + str(i))
    ass_list.append(rfb_holes)
    rrb_holes = product.add_assembly(LINE_BORE)
    rrb_holes.set_name("Right Rear Bottom Holes " + str(i))
    ass_list.append(rrb_holes)
    lfb_holes = product.add_assembly(LINE_BORE)
    lfb_holes.set_name("Left Front Top Holes " + str(i))
    ass_list.append(lfb_holes)
    lrb_holes = product.add_assembly(LINE_BORE)
    lrb_holes.set_name("Left Rear Top Holes " + str(i))
    ass_list.append(lrb_holes)
    rfb_holes = product.add_assembly(LINE_BORE)
    rfb_holes.set_name("Right Front Top Holes " + str(i))
    ass_list.append(rfb_holes)
    rrb_holes = product.add_assembly(LINE_BORE)
    rrb_holes.set_name("Right Rear Top Holes " + str(i))
    ass_list.append(rrb_holes)
    rfb_holes = product.add_assembly(LINE_BORE)
    rfb_holes.set_name("Left Mid Top Holes " + str(i))
    ass_list.append(rfb_holes)
    rrb_holes = product.add_assembly(LINE_BORE)
    rrb_holes.set_name("Right Mid Top Holes " + str(i))
    ass_list.append(rrb_holes)
    rfb_holes = product.add_assembly(LINE_BORE)
    rfb_holes.set_name("Left Mid Bottom Holes " + str(i))
    ass_list.append(rfb_holes)
    rrb_holes = product.add_assembly(LINE_BORE)
    rrb_holes.set_name("Right Mid Bottom Holes " + str(i))
    ass_list.append(rrb_holes)
    
    for ass in ass_list:

        ass.x_rot(value = 0)
        ass.y_rot(value = -90)
        ass.z_rot(value = 0)
        ass.y_dim(value = 0)
        ass.prompt('Shelf Hole Spacing',value = unit.inch(1.2598))
        
        if "Left" in ass.obj_bp.mv.name_object:
            if i == 1:
                Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
                ass.x_loc('X_Loc+INCH(.01)+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
            else:
                ass.x_loc('X_Loc+INCH(.01)',[X_Loc])
            ass.z_dim('IF(Drill_Thru_Left,Panel_Thickness+INCH(.02),INCH(.2))',[Drill_Thru_Left,Panel_Thickness])

            if "Top" in ass.obj_bp.mv.name_object:
                if i == 1:                  #FIRST OPENING
                    ass.prompt('Hide','IF(Left_End_Condition!=3,IF(OR(Remove_Left,Start_LB==0),True,False),True)',[Left_End_Condition,Remove_Left,Start_LB])
                elif i == product.opening_qty: #LAST OPENING
                    ass.prompt('Hide','IF(Right_End_Condition!=3,IF(OR(Remove_Left,Start_LB==0),True,False),True)',[Right_End_Condition,Remove_Left,Start_LB])
                else:                       #MIDDLE OPENING
                    ass.prompt('Hide','IF(OR(Remove_Left,Start_LB==0),True,False)',[Remove_Left,Start_LB])
            else:
                if i == 1:                  #FIRST OPENING
                    ass.prompt('Hide','IF(Left_End_Condition!=3,IF(Remove_Left,True,False),True)',[Left_End_Condition,Remove_Left])
                elif i == product.opening_qty: #LAST OPENING
                    ass.prompt('Hide','IF(Right_End_Condition!=3,IF(Remove_Left,True,False),True)',[Right_End_Condition,Remove_Left])
                else:                       #MIDDLE OPENING
                    ass.prompt('Hide','IF(Remove_Left,True,False)',[Remove_Left])
        
        if "Right" in ass.obj_bp.mv.name_object:
            if i == 1:
                Left_Side_Wall_Filler = product.get_var('Left Side Wall Filler')
                ass.x_loc('X_Loc+Width-INCH(.01)+Left_Side_Wall_Filler',[X_Loc,Width,Left_Side_Wall_Filler])
            else:
                ass.x_loc('X_Loc+Width-INCH(.01)',[X_Loc,Width])
            ass.z_dim('IF(Drill_Thru_Right,-Panel_Thickness-INCH(.02),-INCH(.2))',[Drill_Thru_Right,Panel_Thickness])

            if "Top" in ass.obj_bp.mv.name_object:
                if i == 1:                  #FIRST OPENING
                    ass.prompt('Hide','IF(Left_End_Condition!=3,IF(OR(Remove_Right,Start_LB==0),True,False),True)',[Left_End_Condition,Remove_Right,Start_LB])
                elif i == product.opening_qty: #LAST OPENING
                    ass.prompt('Hide','IF(Right_End_Condition!=3,IF(OR(Remove_Right,Start_LB==0),True,False),True)',[Right_End_Condition,Remove_Right,Start_LB])
                else:                       #MIDDLE OPENING
                    ass.prompt('Hide','IF(OR(Remove_Right,Start_LB==0),True,False)',[Remove_Right,Start_LB])
            else:
                if i == 1:                  #FIRST OPENING
                    ass.prompt('Hide','IF(Left_End_Condition!=3,IF(Remove_Right,True,False),True)',[Left_End_Condition,Remove_Right])
                elif i == product.opening_qty: #LAST OPENING
                    ass.prompt('Hide','IF(Right_End_Condition!=3,IF(Remove_Right,True,False),True)',[Right_End_Condition,Remove_Right])
                else:                       #MIDDLE OPENING
                    ass.prompt('Hide','IF(Remove_Right,True,False)',[Remove_Right])

        if "Top" in ass.obj_bp.mv.name_object:
            ass.x_dim('Height-Start_LB',[Height,Start_LB])
            
        if "Bottom" in ass.obj_bp.mv.name_object:
            ass.z_loc('IF(Floor,MILLIMETER(9.525),Product_Height-Height+MILLIMETER(9.525))',[Floor,Product_Height,Height])
            ass.x_dim('IF(Stop_LB>0,Stop_LB,Height)',[Height,Stop_LB])
                
        if "Front" in ass.obj_bp.mv.name_object:
            ass.y_loc("-Depth-IF(Add_Backing,Back_Thickness,0)+INCH(1.4567)",[Depth,Add_Backing,Back_Thickness])
        
        if "Rear" in ass.obj_bp.mv.name_object:
            ass.y_loc("-IF(Add_Backing,Back_Thickness,0)-INCH(1.4567)",[Add_Backing,Back_Thickness])
        
        if "Mid" in ass.obj_bp.mv.name_object:
            ass.y_loc("-IF(Add_Backing,Back_Thickness,0)-INCH(12)+INCH(1.4567)",[Add_Backing,Back_Thickness])
            if "Left" in ass.obj_bp.mv.name_object:
                if "Top" in ass.obj_bp.mv.name_object:
                    ass.prompt('Hide','IF(OR(Remove_Left,Start_LB==0),True,IF(Add_Mid,False,True))',[Remove_Left,Start_LB,Add_Mid])
                else:
                    ass.prompt('Hide','IF(Remove_Left,True,IF(Add_Mid,False,True))',[Remove_Left,Add_Mid])
            if "Right" in ass.obj_bp.mv.name_object:
                if "Top" in ass.obj_bp.mv.name_object:
                    ass.prompt('Hide','IF(OR(Remove_Right,Start_LB==0),True,IF(Add_Mid,False,True))',[Remove_Right,Start_LB,Add_Mid])
                else:
                    ass.prompt('Hide','IF(Remove_Right,True,IF(Add_Mid,False,True))',[Remove_Right,Add_Mid])

def add_panel_drilling(part,product,index):
    Width = part.get_var('dim_y','Width')
    Height = part.get_var('dim_x','Height')
    Panel_Thickness = product.get_var('Panel Thickness')
    
    if index == 1:
        Height = product.get_var("Opening " + str(index) + " Height",'Height')
        Width = product.get_var("Opening " + str(index) + " Depth",'Width')
        Stop_LB = product.get_var("Opening " + str(index) + " Stop LB",'Stop_LB')
        Start_LB = product.get_var("Opening " + str(index) + " Start LB",'Start_LB')
        Drill_Thru_5 = product.get_var("Opening " + str(index) + " Drill Thru Left",'Drill_Thru_5')
        Add_Mid = product.get_var("Opening " + str(index) + " Add Mid Drilling",'Add_Mid')
        Remove_5 = product.get_var("Opening " + str(index) + " Remove Left Drill",'Remove_5')
    else:
        Height = product.get_var("Opening " + str(index - 1) + " Height",'Height')
        Width = product.get_var("Opening " + str(index - 1) + " Depth",'Width')
        Stop_LB = product.get_var("Opening " + str(index - 1) + " Stop LB",'Stop_LB')
        Start_LB = product.get_var("Opening " + str(index - 1) + " Start LB",'Start_LB')
        Drill_Thru_5 = product.get_var("Opening " + str(index - 1) + " Drill Thru Right",'Drill_Thru_5')
        Add_Mid = product.get_var("Opening " + str(index - 1) + " Add Mid Drilling",'Add_Mid')
        Remove_5 = product.get_var("Opening " + str(index - 1) + " Remove Left Drill",'Remove_5')

    obj, token = part.add_machine_token('Drilling Front Bottom 5' ,'BORE','5')
    token.dim_in_x = unit.millimeter(9.5)
    token.dim_in_y = unit.inch(1.4567)
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Drill_Thru_5,Panel_Thickness,INCH(.5)))',[Drill_Thru_5,Panel_Thickness,Remove_5])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','IF(Stop_LB==0,Height,Stop_LB)',[Height,Stop_LB])
    token.end_dim_in_y  = unit.inch(1.4567)
    token.distance_between_holes = unit.millimeter(32) #7
    token.associative_dia = 0
    token.associative_depth = 0

    obj, token = part.add_machine_token('Drilling Rear Bottom 5' ,'BORE','5')
    token.dim_in_x = unit.millimeter(9.5)
    token.add_driver(obj, 'dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    token.dim_in_z = unit.inch(1) 
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Drill_Thru_5,Panel_Thickness,INCH(.5)))',[Drill_Thru_5,Panel_Thickness,Remove_5])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','IF(Stop_LB==0,Height,Stop_LB)',[Height,Stop_LB])
    token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    token.distance_between_holes = unit.millimeter(32) 
    token.associative_dia = 0 
    token.associative_depth = 0 

    obj, token = part.add_machine_token('Drilling Mid Bottom 5' ,'BORE','5')
    token.dim_in_x = unit.millimeter(9.5)
    token.dim_in_y = unit.inch(12 - 1.4567)
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Add_Mid,IF(Drill_Thru_5,Panel_Thickness,INCH(.5)),0))',[Drill_Thru_5,Add_Mid,Panel_Thickness,Remove_5])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','IF(Stop_LB==0,Height,Stop_LB)',[Height,Stop_LB])
    token.end_dim_in_y  = unit.inch(12 - 1.4567)
    token.distance_between_holes = unit.millimeter(32) #7
    token.associative_dia = 0 
    token.associative_depth = 0 
    
    #TOP
    
    obj, token = part.add_machine_token('Drilling Front Top 5' ,'BORE','5')
    token.add_driver(obj,'dim_in_x','Start_LB',[Start_LB])
    token.dim_in_y = unit.inch(1.4567)
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Start_LB>0,IF(Drill_Thru_5,Panel_Thickness,INCH(.5)),0))',[Drill_Thru_5,Panel_Thickness,Remove_5,Start_LB])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','Height',[Height])
    token.end_dim_in_y  = unit.inch(1.4567)
    token.distance_between_holes = unit.millimeter(32) #7
    token.associative_dia = 0 
    token.associative_depth = 0 

    obj, token = part.add_machine_token('Drilling Rear Top 5' ,'BORE','5')
    token.add_driver(obj,'dim_in_x','Start_LB',[Start_LB])
    token.add_driver(obj, 'dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    token.dim_in_z = unit.inch(1) 
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Start_LB>0,IF(Drill_Thru_5,Panel_Thickness,INCH(.5)),0))',[Drill_Thru_5,Panel_Thickness,Remove_5,Start_LB])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','Height',[Height])
    token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    token.distance_between_holes = unit.millimeter(32) 
    token.associative_dia = 0 
    token.associative_depth = 0 

    obj, token = part.add_machine_token('Drilling Mid Top 5' ,'BORE','5')
    token.add_driver(obj,'dim_in_x','Start_LB',[Start_LB])
    token.dim_in_y = unit.inch(12 - 1.4567)
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Add_Mid,IF(Start_LB>0,IF(Drill_Thru_5,Panel_Thickness,INCH(.5)),0),0))',[Drill_Thru_5,Panel_Thickness,Remove_5,Add_Mid,Start_LB])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','Height',[Height])
    token.end_dim_in_y  = unit.inch(12 - 1.4567)
    token.distance_between_holes = unit.millimeter(32) #7
    token.associative_dia = 0 
    token.associative_depth = 0 
    
    if index != 1 and index != product.opening_qty + 1:
        Height = product.get_var("Opening " + str(index) + " Height",'Height')
        Width = product.get_var("Opening " + str(index) + " Depth",'Width')
        Stop_LB_6 = product.get_var("Opening " + str(index) + " Stop LB",'Stop_LB_6')
        Start_LB_6 = product.get_var("Opening " + str(index) + " Start LB",'Start_LB_6')
        Drill_Thru_6 = product.get_var("Opening " + str(index) + " Drill Thru Left",'Drill_Thru_6')
        Add_Mid_6 = product.get_var("Opening " + str(index) + " Add Mid Drilling",'Add_Mid_6')
        Remove_6 = product.get_var("Opening " + str(index) + " Remove Left Drill",'Remove_6')

        obj, token = part.add_machine_token('Drilling Front Bottom 6' ,'BORE','6')
        token.dim_in_x = unit.millimeter(9.5)
        token.dim_in_y = unit.inch(1.4567)
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Drill_Thru_6,Panel_Thickness,INCH(.5)))',[Remove_6,Drill_Thru_6,Panel_Thickness])
        token.face_bore_dia = 5
        token.add_driver(obj,'end_dim_in_x','IF(Stop_LB_6==0,Height,Stop_LB_6)',[Height,Stop_LB_6])
        token.end_dim_in_y  = unit.inch(1.4567)
        token.distance_between_holes = unit.millimeter(32)
        token.associative_dia = 0 
        token.associative_depth = 0 
        
        obj, token = part.add_machine_token('Drilling Rear Bottom 6' ,'BORE','6')
        token.dim_in_x = unit.millimeter(9.5)
        token.add_driver(obj, 'dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Drill_Thru_6,Panel_Thickness,INCH(.5)))',[Remove_6,Drill_Thru_6,Panel_Thickness])
        token.face_bore_dia = 5 
        token.add_driver(obj,'end_dim_in_x','IF(Stop_LB_6==0,Height,Stop_LB_6)',[Height,Stop_LB_6])
        token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.distance_between_holes = unit.millimeter(32) 
        token.associative_dia = 0 
        token.associative_depth = 0 
        
        obj, token = part.add_machine_token('Drilling Mid Bottom 6' ,'BORE','6')
        token.dim_in_x = unit.millimeter(9.5)
        token.dim_in_y = unit.inch(12 - 1.4567)
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Add_Mid_6,IF(Drill_Thru_6,Panel_Thickness,INCH(.5)),0))',[Remove_6,Add_Mid_6,Drill_Thru_6,Panel_Thickness])
        token.face_bore_dia = 5
        token.add_driver(obj,'end_dim_in_x','IF(Stop_LB_6==0,Height,Stop_LB_6)',[Height,Stop_LB_6])
        token.end_dim_in_y  = unit.inch(12 - 1.4567)
        token.distance_between_holes = unit.millimeter(32)
        token.associative_dia = 0
        token.associative_depth = 0
        
        #TOP
        
        obj, token = part.add_machine_token('Drilling Front Top 6' ,'BORE','6')
        token.add_driver(obj,'dim_in_x','Start_LB_6',[Start_LB_6])
        token.dim_in_y = unit.inch(1.4567)
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Start_LB_6>0,IF(Drill_Thru_6,Panel_Thickness,INCH(.5)),0))',[Remove_6,Drill_Thru_6,Panel_Thickness,Start_LB_6])
        token.face_bore_dia = 5
        token.add_driver(obj,'end_dim_in_x','Height',[Height])
        token.end_dim_in_y  = unit.inch(1.4567)
        token.distance_between_holes = unit.millimeter(32)
        token.associative_dia = 0
        token.associative_depth = 0
        
        obj, token = part.add_machine_token('Drilling Rear Top 6' ,'BORE','6')
        token.add_driver(obj,'dim_in_x','Start_LB_6',[Start_LB_6])
        token.add_driver(obj, 'dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Start_LB_6>0,IF(Drill_Thru_6,Panel_Thickness,INCH(.5)),0))',[Remove_6,Drill_Thru_6,Panel_Thickness,Start_LB_6])
        token.face_bore_dia = 5 
        token.add_driver(obj,'end_dim_in_x','Height',[Height])
        token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.distance_between_holes = unit.millimeter(32) 
        token.associative_dia = 0
        token.associative_depth = 0
        
        obj, token = part.add_machine_token('Drilling Mid Top 6' ,'BORE','6')
        token.add_driver(obj,'dim_in_x','Start_LB_6',[Start_LB_6])
        token.dim_in_y = unit.inch(12 - 1.4567)
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Add_Mid_6,IF(Start_LB_6>0,IF(Drill_Thru_6,Panel_Thickness,INCH(.5)),0),0))',[Remove_6,Drill_Thru_6,Panel_Thickness,Start_LB_6,Add_Mid_6])
        token.face_bore_dia = 5
        token.add_driver(obj,'end_dim_in_x','Height',[Height])
        token.end_dim_in_y  = unit.inch(12 - 1.4567)
        token.distance_between_holes = unit.millimeter(32)
        token.associative_dia = 0
        token.associative_depth = 0

class Closet_Carcass(fd_types.Assembly):
    
    category_name = "Face Frame Closet Openings"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".openings"
    type_assembly = "PRODUCT"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'
    opening_qty = 4
    
    is_hanging = False
    
    def __init__(self):
        props = props_closet.get_scene_props().closet_defaults
        self.width = unit.inch(18) * self.opening_qty
        if self.is_hanging:
            self.height = unit.millimeter(float(props.hanging_height))
        else:
            self.height = unit.millimeter(float(props.panel_height))
        self.depth = props.panel_depth

    def draw(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.create_assembly()
        self.obj_bp.mv.product_type = "Closet"
        
        if defaults.export_subassemblies:
            self.obj_bp.mv.export_product_subassemblies = True            
        
        product_props = props_closet.get_object_props(self.obj_bp)
        product_props.is_closet = True
        
        add_opening_prompts(self)
        add_material_thickness_prompts(self)
        add_common_closet_prompts(self)
        add_machining_prompts(self)
        
        add_sides(self)
        panel = None
        if defaults.use_plant_on_top:
            add_plant_on_top(self, 1, panel)
        else:
            add_shelf(self,1,panel,is_top=True)
        add_shelf(self,1,panel,is_top=False)
        add_toe_kick(self,1,panel)
        add_cleat(self,1,panel)
        add_closet_opening(self,1,panel)
        add_backing(self,1,panel)
        if defaults.use_32mm_system:
            add_system_holes(self,1, panel)
            
        add_inside_dimension(self, 1, panel)
        
        for i in range(2,self.opening_qty+1):
            panel = add_panel(self,i,panel)
            if defaults.use_plant_on_top:
                add_plant_on_top(self, i, panel)
            else:
                add_shelf(self,i,panel,is_top=True)
            add_shelf(self,i,panel,is_top=False)
            add_toe_kick(self,i,panel)
            add_cleat(self,i,panel)
            add_closet_opening(self,i,panel)
            add_backing(self,i,panel)
            if defaults.use_32mm_system:
                add_system_holes(self,i, panel)
            add_inside_dimension(self, i, panel)

class PROMPTS_Opening_Starter(bpy.types.Operator):
    
    #TODO: Turn off equal width property if all but one equal options are checked.
    
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".openings"
    bl_label = "Opening Starter Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    tabs = bpy.props.EnumProperty(name="Tabs",
                        items=[('OPENINGS','Opening Sizes','Show the Width x Height x Depth for each opening'),
                               ('CONSTRUCTION','Construction Options','Show Additional Construction Options'),
                               ('MACHINING','Machining Options','Machining Options')],
                        default = 'OPENINGS')
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)
    depth_1 = bpy.props.FloatProperty(name="Depth 1",unit='LENGTH',precision=4)
    depth_2 = bpy.props.FloatProperty(name="Depth 2",unit='LENGTH',precision=4)
    height = bpy.props.EnumProperty(name="Height",
                          items=common_lists.PANEL_HEIGHTS,
                          default = '2131',
                          update=update_closet_height)
    
    Opening_1_Height = bpy.props.EnumProperty(name="Opening 1 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Opening_2_Height = bpy.props.EnumProperty(name="Opening 2 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Opening_3_Height = bpy.props.EnumProperty(name="Opening 3 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Opening_4_Height = bpy.props.EnumProperty(name="Opening 4 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Opening_5_Height = bpy.props.EnumProperty(name="Opening 5 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Opening_6_Height = bpy.props.EnumProperty(name="Opening 6 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Opening_7_Height = bpy.props.EnumProperty(name="Opening 7 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Opening_8_Height = bpy.props.EnumProperty(name="Opening 8 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '2131')
    
    Left_End_Condition = bpy.props.EnumProperty(name="Left Side",
                                       items=common_lists.END_CONDITIONS,
                                       default = 'WP')
    
    Right_End_Condition = bpy.props.EnumProperty(name="Right Side",
                                        items=common_lists.END_CONDITIONS,
                                        default = 'WP')
    
    product = None
    
    is_island = None
    is_single_island = None
    
    inserts = []

    def check(self, context):
        self.product.obj_x.location.x = self.width
        props = props_closet.get_scene_props()
        if props.closet_defaults.use_32mm_system:
            for i in range(1,9):
                opening_height = self.product.get_prompt("Opening " + str(i) + " Height")
                if opening_height:
                    height = eval("float(self.Opening_" + str(i) + "_Height)/1000")
                    opening_height.set_value(height)
            
#         if self.is_island:
#             self.product.obj_z.location.z = unit.millimeter(float(self.height))
#             depth_1 = self.product.get_prompt("Depth 1")
#             depth_2 = self.product.get_prompt("Depth 2")
#             back_thickness = self.product.get_prompt("Back Thickness")   
#             self.product.obj_y.location.y = -depth_1.value() - depth_2.value() - back_thickness.value()
#             if opening_1_depth:
#                 opening_1_depth.set_value(depth_1.value() + depth_2.value() + back_thickness.value())
#             if opening_2_depth:
#                 opening_2_depth.set_value(depth_1.value() + depth_2.value() + back_thickness.value())
#             if opening_3_depth:
#                 opening_3_depth.set_value(depth_1.value() + depth_2.value() + back_thickness.value())
#             if opening_4_depth:
#                 opening_4_depth.set_value(depth_1.value() + depth_2.value() + back_thickness.value())     
#                 
#         if self.is_single_island:
#             self.product.obj_z.location.z = unit.millimeter(float(self.height))
#             inside_depth = self.product.get_prompt("Inside Depth")
#             self.product.obj_y.location.y = -inside_depth.value()
#             if opening_1_depth:
#                 opening_1_depth.set_value(inside_depth.value())
#             if opening_2_depth:
#                 opening_2_depth.set_value(inside_depth.value())
#             if opening_3_depth:
#                 opening_3_depth.set_value(inside_depth.value())
#             if opening_4_depth:
#                 opening_4_depth.set_value(inside_depth.value())                            

        left_end_condition = self.product.get_prompt("Left End Condition")
        right_end_condition = self.product.get_prompt("Right End Condition")
        
        if left_end_condition:
            left_end_condition.set_value(self.Left_End_Condition)
        
        if right_end_condition:
            right_end_condition.set_value(self.Right_End_Condition)
        
        utils.run_calculators(self.product.obj_bp)
        #Hack I Dont know why i need to run calculators twice just for left right side removal
        utils.run_calculators(self.product.obj_bp)
        return True

    def execute(self, context):
        obj_list = []
        obj_list = utils.get_child_objects(self.product.obj_bp, obj_list)
        for obj in obj_list:
            if obj.type == 'EMPTY':
                obj.hide = True
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                utils.run_calculators(self.product.obj_bp)
        return {'FINISHED'}

    def set_default_heights(self):
        for i in range(1,9):
            opening_height_prompt = self.product.get_prompt("Opening " + str(i) + " Height")
            if opening_height_prompt:
                opening_height = round(unit.meter_to_millimeter(opening_height_prompt.value()),0)
                for index, height in enumerate(common_lists.PANEL_HEIGHTS):
                    if not opening_height >= int(height[0]):
                        exec('self.Opening_' + str(i) + '_Height = common_lists.PANEL_HEIGHTS[index - 1][0]')                                                                                                                                                                                                        
                        break

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        if self.product.obj_bp:
            self.set_default_heights()
            self.width = math.fabs(self.product.obj_x.location.x)
            new_list = []
            self.inserts = utils.get_insert_bp_list(self.product.obj_bp,new_list)
            left_end_condition = self.product.get_prompt("Left End Condition")
            right_end_condition = self.product.get_prompt("Right End Condition")
            self.is_island = self.product.get_prompt("Is Island")
            self.is_single_island = self.product.get_prompt("Inside Depth")
            if left_end_condition:
                self.Left_End_Condition = left_end_condition.value()
            if right_end_condition:
                self.Right_End_Condition = right_end_condition.value()
            if self.is_island:
                opening_1_height = self.product.get_prompt("Opening 1 Height")
                opening_1_depth = self.product.get_prompt("Opening 1 Depth")
                self.depth = opening_1_depth.value()
                self.height = self.convert_to_height(opening_1_height.value())
            if self.is_single_island:
                opening_1_height = self.product.get_prompt("Opening 1 Height")
                opening_1_depth = self.product.get_prompt("Opening 1 Depth")
                self.depth = opening_1_depth.value()
                self.height = self.convert_to_height(opening_1_height.value())
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=600)

    def convert_to_height(self,number):
        for index, height in enumerate(common_lists.PANEL_HEIGHTS):
            if not number * 1000 >= float(height[0]):
                return common_lists.PANEL_HEIGHTS[index - 1][0]

    def draw_product_size(self,layout):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row1.label('Width: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label('Width:')
            row1.prop(self,'width',text="")
            row1.prop(self.product.obj_x,'hide',text="")
        
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_z):
            row1.label('Hang Height: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label('Hang Height:')
            row1.prop(self.product.obj_z,'location',index=2,text="")
            row1.prop(self.product.obj_z,'hide',text="")
            row1 = col.row(align=True)
            row1.prop(self,'height',text="Set Height")
        
    def object_has_driver(self,obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True
            
    def draw_common_prompts(self,layout):
        box = layout.box()
        col = box.column(align=True)
        col.prop(self,'Left_End_Condition')
        col.prop(self,'Right_End_Condition')
        
    def draw_splitter_widths(self,layout):
        props = props_closet.get_scene_props()
        
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        row.label("Opening Name:")
        row.label("",icon='BLANK1')
        row.label("Width:")
        if not self.is_island or not self.is_single_island:
            row.label("Height:")
            row.label("Depth:")
        
        box = col.box()
        
        for i in range(1,9):
            width = self.product.get_prompt("Opening " + str(i) + " Width")
            height = self.product.get_prompt("Opening " + str(i) + " Height")
            depth = self.product.get_prompt("Opening " + str(i) + " Depth")
            floor = self.product.get_prompt("Opening " + str(i) + " Floor Mounted")
            if width:
                row = box.row()
                row.label( str(i) + ":")
                row.prop(width,'equal',text="")
                if width.equal:
                    row.label(str(unit.meter_to_active_unit(width.DistanceValue)) + '"')
                else:
                    row.prop(width,'DistanceValue',text="")
                row.prop(floor,floor.prompt_type,text="",icon='TRIA_DOWN' if floor.value() else 'TRIA_UP')
                if props.closet_defaults.use_32mm_system:
                    row.prop(self,'Opening_' + str(i) + '_Height',text="")
                else:
                    row.prop(height,'DistanceValue',text="")
                row.prop(depth,'DistanceValue',text="")
            
    def draw_ctf_options(self,layout):
        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("CTF Opening " + str(i))
            if prompt:
                prompts.append(prompt)
                
        row = layout.row()
        row.label("CTF:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

    def draw_cleat_options(self,layout):
        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("Add " + str(i) + " Cleat")
            if prompt:
                prompts.append(prompt)

        row = layout.row()
        row.label("Add Cleat:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

        for i, prompt in enumerate(prompts):
            if prompt.CheckBoxValue:
                loc_prompt = self.product.get_prompt("Cleat " + str(i + 1) + " Location")
                row = layout.row()
                row.label("Cleat " + str(i + 1) + " Location")
                row.prop(loc_prompt,"DistanceValue",text=str(i + 1))            
            
    def draw_construction_options(self,layout):
        box = layout.box()
        
        toe_kick_height = self.product.get_prompt("Toe Kick Height")
        toe_kick_setback = self.product.get_prompt("Toe Kick Setback")
        left_wall_filler = self.product.get_prompt("Left Side Wall Filler")
        right_wall_filler = self.product.get_prompt("Right Side Wall Filler")
        add_backing = self.product.get_prompt("Add Backing")
        add_top_accent_shelf = self.product.get_prompt("Add Top Accent Shelf")
        top_shelf_overhang = self.product.get_prompt("Top Shelf Overhang")
        crown_molding_height = self.product.get_prompt("Crown Molding Height")
        front_angle_height = self.product.get_prompt("Front Angle Height")
        front_angle_depth = self.product.get_prompt("Front Angle Depth")
        rear_angle_height = self.product.get_prompt("Rear Angle Height")
        rear_angle_depth = self.product.get_prompt("Rear Angle Depth")
        first_rear_notch_height = self.product.get_prompt("First Rear Notch Height")
        first_rear_notch_depth = self.product.get_prompt("First Rear Notch Depth")
        second_rear_notch_height = self.product.get_prompt("Second Rear Notch Height")
        second_rear_notch_depth = self.product.get_prompt("Second Rear Notch Depth")
                                
        crown_molding_depth = self.product.get_prompt("Front Angle Height")
        
        # SIDE OPTIONS:
        if left_wall_filler and right_wall_filler:
            split = box.split()
            col = split.column(align=True)
            col.label("Filler Options:")
            row = col.row()
            row.prop(left_wall_filler,'DistanceValue',text="Left Filler Amount")
            row = col.row()
            row.prop(right_wall_filler,'DistanceValue',text="Right Filler Amount")
            
        self.draw_ctf_options(box)
        self.draw_cleat_options(box)
        
        # CARCASS OPTIONS:
        col = box.column(align=True)
        col.label("Back Options:")
        row = col.row()
        if add_backing:
            row.prop(add_backing,'CheckBoxValue',text="Add Backing")     
            
        col = box.column(align=True)
        col.label("Top Options:")
        if front_angle_depth and front_angle_height:
            row = col.row()
            row.label("Angle Top Front:")
            row.prop(front_angle_height,front_angle_height.prompt_type,text="Height")
            row.prop(front_angle_depth,front_angle_depth.prompt_type,text="Depth")
            
        if rear_angle_depth and rear_angle_height:
            row = col.row()
            row.label("Angle Top Rear:")
            row.prop(rear_angle_height,rear_angle_height.prompt_type,text="Height")
            row.prop(rear_angle_depth,rear_angle_depth.prompt_type,text="Depth")
            
        if add_top_accent_shelf and top_shelf_overhang:
            row = col.row()
            row.prop(add_top_accent_shelf,'CheckBoxValue',text="Add Top Accent Shelf")
            row.prop(top_shelf_overhang,'DistanceValue',text="Top Shelf Overhang")
        
        if crown_molding_height and crown_molding_depth:
            row = col.row()
            row.prop(crown_molding_height,'DistanceValue',text="Crown Molding Height")
            row.prop(crown_molding_depth,'DistanceValue',text="Crown Molding Depth")
        
        col = box.column(align=True)
        col.label("Base Options:")        
        # TOE KICK OPTIONS
        if toe_kick_height and toe_kick_setback:
            row = col.row()
            row.label("Toe Kick")
            row.prop(toe_kick_height,toe_kick_height.prompt_type,text="Height")
            row.prop(toe_kick_setback,toe_kick_setback.prompt_type,text="Setback")
            
        if first_rear_notch_height and first_rear_notch_depth:
            row = col.row()
            row.label("1 Rear Notch:")
            row.prop(first_rear_notch_height,first_rear_notch_height.prompt_type,text="Height")
            row.prop(first_rear_notch_depth,first_rear_notch_depth.prompt_type,text="Depth")
            row = col.row()
            row.label("2 Rear Notch:")
            row.prop(second_rear_notch_height,second_rear_notch_height.prompt_type,text="Height")
            row.prop(second_rear_notch_depth,second_rear_notch_depth.prompt_type,text="Depth")

    def draw_new_machining_options(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Opening Name:")
        row.label("Top:")
        row.label("Bottom:")
        row.label("Mid Row:")
        row.label("Drill Thru:")
        row.label("Remove:")
        
        for i in range(1,9):
            stop_lb = self.product.get_prompt("Opening " + str(i) + " Stop LB")
            start_lb = self.product.get_prompt("Opening " + str(i) + " Start LB")
            drill_thru_left = self.product.get_prompt("Opening " + str(i) + " Drill Thru Left")
            drill_thru_right = self.product.get_prompt("Opening " + str(i) + " Drill Thru Right")
            add_mid = self.product.get_prompt("Opening " + str(i) + " Add Mid Drilling")
            remove_left_drill = self.product.get_prompt("Opening " + str(i) + " Remove Left Drill")
            remove_right_drill = self.product.get_prompt("Opening " + str(i) + " Remove Right Drill")
            
            if stop_lb:
                row = box.row(align=True)
                row.label('Opening ' + str(i) + ":")
#                 row.label(" ")
                row.prop(self,'height',text="")
                row.prop(self,'height',text="")
                row.label("",icon='BLANK1')
                row.label("",icon='BLANK1')
                row.label("",icon='BLANK1')
                row.prop(add_mid,'CheckBoxValue',text=" ")
                row.prop(drill_thru_left,'CheckBoxValue',text="")
                row.prop(drill_thru_right,'CheckBoxValue',text=" ")
                row.prop(remove_left_drill,'CheckBoxValue',text="")
                row.prop(remove_right_drill,'CheckBoxValue',text="")
                row.label("",icon='BLANK1')
                row.label("",icon='BLANK1')

    def draw_machining_options(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Opening Name:")
        row.label("",icon='BLANK1')
        row.label("Mid Row:")
        row.label("Drill Thru:")
        row.label("Remove:")
        
        for i in range(1,9):
            stop_lb = self.product.get_prompt("Opening " + str(i) + " Stop LB")
            start_lb = self.product.get_prompt("Opening " + str(i) + " Start LB")
            drill_thru_left = self.product.get_prompt("Opening " + str(i) + " Drill Thru Left")
            drill_thru_right = self.product.get_prompt("Opening " + str(i) + " Drill Thru Right")
            add_mid = self.product.get_prompt("Opening " + str(i) + " Add Mid Drilling")
            remove_left_drill = self.product.get_prompt("Opening " + str(i) + " Remove Left Drill")
            remove_right_drill = self.product.get_prompt("Opening " + str(i) + " Remove Right Drill")
            
            if stop_lb:
                row = box.row(align=True)
                row.label('Opening ' + str(i) + ":")
#                 row.label(" ")
                row.prop(add_mid,'CheckBoxValue',text=" ")
#                 row.prop(stop_lb,'DistanceValue',text="Stop")
#                 row.prop(start_lb,'DistanceValue',text="Start")
#                 row.label(" ")
                row.prop(drill_thru_left,'CheckBoxValue',text="")
                row.prop(drill_thru_right,'CheckBoxValue',text=" ")
#                 row.label(" ")
                row.prop(remove_left_drill,'CheckBoxValue',text="")
                row.prop(remove_right_drill,'CheckBoxValue',text="")
                
    def draw_product_placment(self,layout):
        box = layout.box()
        row = box.row()
        row.label('Location:')
        row.prop(self.product.obj_bp,'location',text="")
        row.label('Rotation:')
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="")
        
    def draw_island_depths(self,layout):
        if self.is_single_island:
            inside_depth = self.product.get_prompt("Inside Depth")
            box = layout.box()
            col = box.column(align=True)
            col.prop(inside_depth,'DistanceValue',text="Inside Depth")            
        else:
            depth_1 = self.product.get_prompt("Depth 1")
            depth_2 = self.product.get_prompt("Depth 2")
            
            box = layout.box()
            col = box.column(align=True)
            col.prop(depth_1,'DistanceValue',text="Depth 1")
            col.prop(depth_2,'DistanceValue',text="Depth 2")
        
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:

                box = layout.box()
                box.label(self.product.obj_bp.mv.name_object,icon='LATTICE_DATA')
                
                split = box.split(percentage=.5)
                self.draw_product_size(split)
                if self.is_island or self.is_single_island:
                    self.draw_island_depths(split)
                else:
                    self.draw_common_prompts(split)
                row = box.row()
                row.prop(self,'tabs',expand=True)
                if self.tabs == 'OPENINGS':
                    self.draw_splitter_widths(box)
                elif self.tabs == 'CONSTRUCTION':
                    self.draw_construction_options(box)
                else:
                    self.draw_new_machining_options(box)
                self.draw_product_placment(box)        
                
bpy.utils.register_class(PROMPTS_Opening_Starter)
