"""
Microvellum 
Exteriors
Stores the logic and insert defs for all exterior components for cabinets and closets.
Doors, Drawers, Hampers
"""

import bpy
from mv import fd_types, unit, utils
from os import path
from . import cabinet_pulls
from . import drawer_boxes
from . import cabinet_properties

ROOT_PATH = path.join(path.dirname(__file__),"Cabinet Assemblies")

DIVISION = path.join(ROOT_PATH,"Cut Parts","Part with Edgebanding.blend")
DOOR = path.join(ROOT_PATH,"Cut Parts","Part with Edgebanding.blend")
DRAWER_FRONT = path.join(ROOT_PATH,"Cut Parts","Part with Edgebanding.blend")
FALSE_FRONT = path.join(ROOT_PATH,"Cut Parts","Part with Edgebanding.blend")
DRAWER_SLIDE = path.join(ROOT_PATH,"Hardware","Drawer Slide.blend")
HARDWOOD = path.join(ROOT_PATH,"Face Frames","Hardwood.blend")
WIRE_BASKET = path.join(ROOT_PATH,"Hardware","Wire Basket.blend")
BUYOUT_DRAWER_BOX = path.join(ROOT_PATH,"Drawer Boxes","Buyout Drawer Box.blend")

#---------FUNCTIONS

def add_common_door_prompts(assembly):
    props = cabinet_properties.get_scene_props().exterior_defaults
    
    door_location = 0
    
    if assembly.door_type == 'Base':
        door_location = 0
    elif assembly.door_type == 'Tall':
        door_location = 1
    else:
        door_location = 2
    
    assembly.add_prompt(name="Door Rotation",prompt_type='ANGLE',value=0,tab_index=0)
    
    assembly.add_prompt(name="Open Door",prompt_type='PERCENTAGE',value=0,tab_index=0)
    
    if assembly.door_swing in {"Left Swing","Right Swing"}:
        assembly.add_prompt(name="Door Swing",prompt_type='COMBOBOX',value=0,tab_index=0,items=['Left','Right'],columns=2)
        
        assembly.add_prompt(name="Left Swing",prompt_type='CHECKBOX',value=True if assembly.door_swing == 'Left Swing' else False,tab_index=0)
        assembly.add_prompt(name="Right Swing",prompt_type='CHECKBOX',value=False,tab_index=1) # CALCULATED
        
        #CALCULATE RIGHT SWING PROMPT NEEDED FOR MV EXPORT
        Door_Swing = assembly.get_var("Door Swing")
        assembly.prompt('Left Swing','IF(Door_Swing==0,True,False)',[Door_Swing])
        assembly.prompt('Right Swing','IF(Door_Swing==1,True,False)',[Door_Swing])
        
    assembly.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=props.inset_door,tab_index=0)
    assembly.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=props.inset_reveal,tab_index=0)
    assembly.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=props.door_to_cabinet_gap,tab_index=0)
    assembly.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=props.no_pulls,tab_index=0)
    assembly.add_prompt(name="Pull Rotation",prompt_type='ANGLE',value=props.pull_rotation,tab_index=0)
    assembly.add_prompt(name="Pull From Edge",prompt_type='DISTANCE',value=props.pull_from_edge,tab_index=0)
    assembly.add_prompt(name="Pull Location",prompt_type='COMBOBOX',value=door_location,tab_index=0,items=['Base','Tall','Upper'],columns=3)
    assembly.add_prompt(name="Base Pull Location",prompt_type='DISTANCE',value=props.base_pull_location,tab_index=0)
    assembly.add_prompt(name="Tall Pull Location",prompt_type='DISTANCE',value=props.tall_pull_location,tab_index=0)
    assembly.add_prompt(name="Upper Pull Location",prompt_type='DISTANCE',value=props.upper_pull_location,tab_index=0)
    assembly.add_prompt(name="Lock Door",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Pull Length",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Door Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Edgebanding Thickness",prompt_type='DISTANCE',value=unit.inch(.02),tab_index=1)
    
    sgi = assembly.get_var('cabinetlib.spec_group_index','sgi')
    
    assembly.prompt('Door Thickness','THICKNESS(sgi,"Cabinet_Door")',[sgi])
    assembly.prompt('Edgebanding Thickness','EDGE_THICKNESS(sgi,"Cabinet_Door_Edges")',[sgi])
    
def add_common_drawer_prompts(assembly):
    props = cabinet_properties.get_scene_props().exterior_defaults
    
    assembly.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=props.no_pulls,tab_index=0)
    assembly.add_prompt(name="Center Pulls on Drawers",prompt_type='CHECKBOX',value=props.center_pulls_on_drawers,tab_index=0)
    assembly.add_prompt(name="Drawer Pull From Top",prompt_type='DISTANCE',value=props.drawer_pull_from_top,tab_index=0)
    assembly.add_prompt(name="Pull Double Max Span",prompt_type='DISTANCE',value=unit.inch(30),tab_index=0)
    assembly.add_prompt(name="Lock From Top",prompt_type='DISTANCE',value=unit.inch(1.0),tab_index=0)
    assembly.add_prompt(name="Lock Drawer",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=props.inset_door,tab_index=0)
    assembly.add_prompt(name="Horizontal Grain",prompt_type='CHECKBOX',value=props.horizontal_grain_on_drawer_fronts,tab_index=0)
    assembly.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)
    
    assembly.add_prompt(name="Open Drawers",prompt_type='PERCENTAGE',value=0,tab_index=0)
    
    assembly.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0) 
    assembly.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)   
    assembly.add_prompt(name="Drawer Box Top Gap",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)
    assembly.add_prompt(name="Drawer Box Bottom Gap",prompt_type='DISTANCE',value=unit.inch(1),tab_index=0)
    assembly.add_prompt(name="Drawer Box Slide Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
    assembly.add_prompt(name="Drawer Box Rear Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
    
    assembly.add_prompt(name="Front Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    assembly.add_prompt(name="Edgebanding Thickness",prompt_type='DISTANCE',value=unit.inch(.02),tab_index=1)
    
    sgi = assembly.get_var('cabinetlib.spec_group_index','sgi')
    
    assembly.prompt('Front Thickness','THICKNESS(sgi,"Cabinet_Door")',[sgi])
    assembly.prompt('Edgebanding Thickness','EDGE_THICKNESS(sgi,"Cabinet_Door_Edges")',[sgi])
    
def add_frameless_overlay_prompts(assembly):
    props = cabinet_properties.get_scene_props().exterior_defaults
    assembly.add_prompt(name="Half Overlay Top",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Half Overlay Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Half Overlay Left",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Half Overlay Right",prompt_type='CHECKBOX',value=False,tab_index=0)
    
    assembly.add_prompt(name="Horizontal Gap",prompt_type='DISTANCE',value=props.vertical_gap,tab_index=0)
    assembly.add_prompt(name="Vertical Gap",prompt_type='DISTANCE',value=props.vertical_gap,tab_index=0)
    assembly.add_prompt(name="Top Reveal",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
    assembly.add_prompt(name="Bottom Reveal",prompt_type='DISTANCE',value=0,tab_index=0)
    assembly.add_prompt(name="Left Reveal",prompt_type='DISTANCE',value=props.left_reveal,tab_index=0)
    assembly.add_prompt(name="Right Reveal",prompt_type='DISTANCE',value=props.right_reveal,tab_index=0)

    #CALCULATED
    assembly.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
    assembly.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
    assembly.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
    assembly.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
    assembly.add_prompt(name="Division Overlay",prompt_type='DISTANCE',value=unit.inch(.6875),tab_index=1)
    
    #INHERITED
    assembly.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    assembly.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
    
    inset = assembly.get_var("Inset Front",'inset')
    ir = assembly.get_var("Inset Reveal",'ir')
    tr = assembly.get_var("Top Reveal",'tr')
    br = assembly.get_var("Bottom Reveal",'br')
    lr = assembly.get_var("Left Reveal",'lr')
    rr = assembly.get_var("Right Reveal",'rr')
    vg = assembly.get_var("Vertical Gap",'vg')
    hot = assembly.get_var("Half Overlay Top",'hot')
    hob = assembly.get_var("Half Overlay Bottom",'hob')
    hol = assembly.get_var("Half Overlay Left",'hol')
    hor = assembly.get_var("Half Overlay Right",'hor')
    tt = assembly.get_var("Top Thickness",'tt')
    lst = assembly.get_var("Left Side Thickness",'lst')
    rst = assembly.get_var("Right Side Thickness",'rst')
    bt = assembly.get_var("Bottom Thickness",'bt')
    dt = assembly.get_var("Division Thickness",'dt')
    
    assembly.prompt('Top Overlay','IF(inset,-ir,IF(hot,(tt/2)-(vg/2),tt-tr))',[inset,ir,hot,tt,tr,vg])
    assembly.prompt('Bottom Overlay','IF(inset,-ir,IF(hob,(bt/2)-(vg/2),bt-br))',[inset,ir,hob,bt,br,vg])
    assembly.prompt('Left Overlay','IF(inset,-ir,IF(hol,(lst/2)-(vg/2),lst-lr))',[inset,ir,hol,lst,lr,vg])
    assembly.prompt('Right Overlay','IF(inset,-ir,IF(hor,(rst/2)-(vg/2),rst-rr))',[inset,ir,hor,rst,rr,vg])
    assembly.prompt('Division Overlay','IF(inset,-ir,(dt/2)-(vg/2))',[inset,ir,dt,vg])
    
def add_drawer_front(insert):
    pass

class Doors(fd_types.Assembly):
    
    library_name = "Frameless Cabinet Inserts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".door_prompts"
    door_type = "" # {Base, Tall, Upper}
    door_swing = "" # {Left Swing, Right Swing, Double Door, Flip up}

    false_front_qty = 0 # 0, 1, 2

    def add_doors_prompts(self):

        self.add_tab(name='Door Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_door_prompts(self)
        add_frameless_overlay_prompts(self)
        if self.false_front_qty > 0:
            self.add_prompt(name="False Front Height",prompt_type='DISTANCE',value=unit.inch(6),tab_index=0)

    def set_standard_drivers(self,assembly):
        Height = self.get_var('dim_z','Height')
        Inset_Front = self.get_var("Inset Front")
        Door_Gap = self.get_var("Door to Cabinet Gap",'Door_Gap')
        tt = self.get_var("Top Thickness",'tt')
        bt = self.get_var("Bottom Thickness",'bt')
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        Door_Thickness = self.get_var("Door Thickness")
        False_Front_Height = self.get_var("False Front Height")
        Vertical_Gap = self.get_var("Vertical Gap")
        
        assembly.y_loc('IF(Inset_Front,Door_Thickness,-Door_Gap)',[Inset_Front,Door_Gap,Door_Thickness])
        assembly.z_loc('IF(OR(eba==0,Inset_Front==True),-Bottom_Overlay,-eba)',
                       [Inset_Front,eba,bt,Bottom_Overlay])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = -90)
        if self.false_front_qty > 0:
            assembly.x_dim('Height+IF(OR(eta==0,Inset_Front==True),Top_Overlay,eta)+IF(OR(eba==0,Inset_Front==True),Bottom_Overlay,eba)-False_Front_Height-Vertical_Gap',
                           [Inset_Front,Height,Top_Overlay,Bottom_Overlay,eta,eba,tt,bt,False_Front_Height,Vertical_Gap])
        else:
            assembly.x_dim('Height+IF(OR(eta==0,Inset_Front==True),Top_Overlay,eta)+IF(OR(eba==0,Inset_Front==True),Bottom_Overlay,eba)',
                           [Inset_Front,Height,Top_Overlay,Bottom_Overlay,eta,eba,tt,bt])
        assembly.z_dim('Door_Thickness',[Door_Thickness])
        
    def set_pull_drivers(self,assembly):
        self.set_standard_drivers(assembly)
        
        Height = self.get_var('dim_z','Height')
        Pull_Length = assembly.get_var("Pull Length")
        Pull_From_Edge = self.get_var("Pull From Edge")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        
        assembly.prompt("Pull X Location",'Pull_From_Edge',[Pull_From_Edge])
        if self.door_type == "Base":
            assembly.prompt("Pull Z Location",'Base_Pull_Location+(Pull_Length/2)',[Base_Pull_Location,Pull_Length])
        if self.door_type == "Tall":
            assembly.prompt("Pull Z Location",'Height-Tall_Pull_Location+(Pull_Length/2)+World_Z',[Height,World_Z,Tall_Pull_Location,Pull_Length])
        if self.door_type == "Upper":
            assembly.prompt("Pull Z Location",'Height+(eta+eba)-Upper_Pull_Location-(Pull_Length/2)',[Height,eta,eba,Upper_Pull_Location,Pull_Length])
    
    def draw(self):
        self.create_assembly()
        
        self.add_doors_prompts()
        
        Height = self.get_var('dim_z','Height')
        Width = self.get_var('dim_x','Width')
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Left_Swing = self.get_var("Left Swing")
        Vertical_Gap = self.get_var("Vertical Gap")
        Door_Rotation = self.get_var("Door Rotation")
        No_Pulls = self.get_var("No Pulls")
        False_Front_Height = self.get_var("False Front Height")
        Door_Thickness = self.get_var("Door Thickness")
        eta = self.get_var("Extend Top Amount",'eta')
        Open_Door = self.get_var("Open Door")
        
        if self.false_front_qty > 0:
            false_front = self.add_assembly(FALSE_FRONT)  
            false_front.set_name("False Front")
            false_front.x_loc('-Left_Overlay',[Left_Overlay])
            false_front.y_loc(value = 0)
            false_front.z_loc('Height+eta',[Height,eta])
            false_front.x_rot(value = 90)
            false_front.y_rot(value = 0)
            false_front.z_rot(value = 0)
            if self.false_front_qty > 1:
                false_front.x_dim('(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
            else:
                false_front.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
            false_front.y_dim('-False_Front_Height',[False_Front_Height])
            false_front.z_dim('Door_Thickness',[Door_Thickness])
            false_front.cutpart("Cabinet_Door")
            false_front.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
            false_front.obj_bp.mv.is_cabinet_drawer_front = True
            
            if self.false_front_qty > 1:
                false_front_2 = self.add_assembly(FALSE_FRONT)
                false_front_2.set_name("False Front")
                false_front_2.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
                false_front_2.y_loc(value = 0)
                false_front_2.z_loc('Height+eta',[Height,eta])
                false_front_2.x_rot(value = 90)
                false_front_2.y_rot(value = 0)
                false_front_2.z_rot(value = 0)
                if self.false_front_qty > 1:
                    false_front_2.x_dim('((Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2)*-1',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
                else:
                    false_front_2.x_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
                false_front_2.y_dim('-False_Front_Height',[False_Front_Height])
                false_front_2.z_dim('Door_Thickness',[Door_Thickness])
                false_front_2.cutpart("Cabinet_Door")
                false_front_2.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
                false_front_2.obj_bp.mv.is_cabinet_drawer_front = True
                
        #LEFT DOOR
        left_door = self.add_assembly(DOOR)
        left_door.set_name("Cabinet Left Door")
        self.set_standard_drivers(left_door)
        left_door.x_loc('-Left_Overlay',[Left_Overlay])
        left_door.z_rot('radians(90)-(radians(120)*Open_Door)',[Open_Door])
        if self.door_swing == 'Double Door':
            left_door.y_dim('((Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2)*-1',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
        else:
            left_door.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
            left_door.prompt('Hide','IF(Left_Swing,False,True)',[Left_Swing])
        left_door.cutpart("Cabinet_Door")
        left_door.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        left_door.obj_bp.mv.is_cabinet_door = True
        
        #LEFT PULL
        left_pull = cabinet_pulls.Standard_Pull()
        left_pull.door_type = self.door_type
        left_pull.door_swing = "Left Swing"
        left_pull.draw()
        left_pull.set_name(left_pull.pull_name)
        left_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(left_pull)
        left_pull.x_loc('-Left_Overlay',[Left_Overlay])
        left_pull.z_rot('radians(90)-(radians(120)*Open_Door)',[Open_Door])
        if self.door_swing == 'Double Door':
            left_pull.y_dim('((Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2)*-1',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
            left_pull.prompt('Hide','IF(No_Pulls,True,False)',[No_Pulls])
        else:
            left_pull.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
            left_pull.prompt('Hide','IF(Left_Swing,IF(No_Pulls,True,False),True)',[Left_Swing,No_Pulls])
            
        #RIGHT DOOR
        right_door = self.add_assembly(DOOR)  
        right_door.set_name("Cabinet Right Door")
        self.set_standard_drivers(right_door)
        right_door.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
        right_door.z_rot('radians(90)+(radians(120)*Open_Door)',[Open_Door])
        if self.door_swing == 'Double Door':
            right_door.y_dim('(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
        else:
            right_door.y_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
            right_door.prompt('Hide','IF(Left_Swing,True,False)',[Left_Swing])
        right_door.cutpart("Cabinet_Door")
        right_door.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        right_door.obj_bp.mv.is_cabinet_door = True
        
        #RIGHT PULL
        right_pull = cabinet_pulls.Standard_Pull()
        right_pull.door_type = self.door_type
        right_pull.door_swing = "Right Swing"
        right_pull.draw()
        right_pull.set_name(right_pull.pull_name)
        right_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(right_pull)
        right_pull.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
        right_pull.z_rot('radians(90)+(radians(120)*Open_Door)',[Open_Door])
        if self.door_swing == "Double Door":
            right_pull.y_dim('(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2',[Width,Left_Overlay,Right_Overlay,Vertical_Gap])
            right_pull.prompt('Hide','IF(No_Pulls,True,False)',[No_Pulls])
        else:
            right_pull.y_dim('(Width+Left_Overlay+Right_Overlay)',[Width,Left_Overlay,Right_Overlay])
            right_pull.prompt('Hide','IF(Left_Swing,True,IF(No_Pulls,True,False))',[Left_Swing,No_Pulls])
        
        self.update()
        
class Pie_Cut_Doors(fd_types.Assembly):
    
    library_name = "Frameless Cabinet Inserts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".door_prompts"
    door_type = "" # {Base, Tall, Upper}
    door_swing = "" # {Left Swing, Right Swing, Double Door, Flip up}

    def add_doors_prompts(self):
        self.add_tab(name='Door Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_door_prompts(self)
        add_frameless_overlay_prompts(self)
        
    def set_standard_drivers(self,assembly):
        Height = self.get_var('dim_z','Height')
        Inset_Front = self.get_var("Inset Front")
        tt = self.get_var("Top Thickness",'tt')
        bt = self.get_var("Bottom Thickness",'bt')
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        Door_Thickness = self.get_var("Door Thickness")
        
        assembly.z_loc('IF(OR(eba==0,Inset_Front==True),-Bottom_Overlay,-eba)',
                       [Inset_Front,eba,bt,Bottom_Overlay])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = -90)
        assembly.z_rot(value = 90)
        assembly.x_dim('Height+IF(OR(eta==0,Inset_Front==True),Top_Overlay,eta)+IF(OR(eba==0,Inset_Front==True),Bottom_Overlay,eba)',
                       [Inset_Front,Height,Top_Overlay,Bottom_Overlay,eta,eba,tt,bt])
        assembly.z_dim('Door_Thickness',[Door_Thickness])
        
    def set_pull_drivers(self,assembly):
        self.set_standard_drivers(assembly)
        
        Height = self.get_var('dim_z','Height')
        Pull_Length = assembly.get_var("Pull Length")
        Pull_From_Edge = self.get_var("Pull From Edge")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        
        assembly.prompt("Pull X Location",'Pull_From_Edge',[Pull_From_Edge])
        if self.door_type == "Base":
            assembly.prompt("Pull Z Location",'Base_Pull_Location+(Pull_Length/2)',[Base_Pull_Location,Pull_Length])
        if self.door_type == "Tall":
            assembly.prompt("Pull Z Location",'Tall_Pull_Location+(Pull_Length/2)',[Tall_Pull_Location,Pull_Length])
        if self.door_type == "Upper":
            assembly.prompt("Pull Z Location",'Height+(eta+eba)-Upper_Pull_Location-(Pull_Length/2)',[Height,eta,eba,Upper_Pull_Location,Pull_Length])
    
    def draw(self):
        self.create_assembly()
        
        self.add_doors_prompts()
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Left_Swing = self.get_var("Left Swing")
        No_Pulls = self.get_var("No Pulls")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Door_Thickness = self.get_var("Door Thickness")
        Inset_Front = self.get_var("Inset Front")
        
        #LEFT DOOR
        left_door = self.add_assembly(DOOR)  
        left_door.set_name("Left Cabinet Door")
        self.set_standard_drivers(left_door)
        left_door.x_loc('IF(Inset_Front,-Door_Thickness,Door_to_Cabinet_Gap)',[Door_to_Cabinet_Gap,Door_Thickness,Inset_Front])
        left_door.y_loc('Depth-Left_Overlay',[Depth,Left_Overlay])
        left_door.x_rot(value = 90)
        left_door.y_dim('(fabs(Depth)+Left_Overlay-IF(Inset_Front,0,Door_Thickness+Door_to_Cabinet_Gap))*-1',[Depth,Left_Overlay,Inset_Front,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        left_door.cutpart("Cabinet_Door")
        left_door.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        left_door.obj_bp.mv.is_cabinet_door = True
        
        #LEFT PULL
        left_pull = cabinet_pulls.Standard_Pull()
        left_pull.door_type = self.door_type
        left_pull.draw()
        left_pull.set_name(left_pull.pull_name)
        left_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(left_pull)
        left_pull.x_loc('IF(Inset_Front,-Door_Thickness,Door_to_Cabinet_Gap)',[Door_to_Cabinet_Gap,Door_Thickness,Inset_Front])
        left_pull.y_loc('-Door_to_Cabinet_Gap',[Door_to_Cabinet_Gap])
        left_pull.x_rot(value = 90)
        left_pull.y_dim('fabs(Depth)+Left_Overlay-Door_Thickness-Door_to_Cabinet_Gap',[Depth,Left_Overlay,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        left_pull.prompt('Hide','IF(Left_Swing,True,IF(No_Pulls,True,False))',[Left_Swing,No_Pulls])
        
        #RIGHT DOOR
        right_door = self.add_assembly(DOOR)  
        right_door.set_name("Right Cabinet Door")
        self.set_standard_drivers(right_door)
        right_door.x_loc('IF(Inset_Front,0,Door_to_Cabinet_Gap+Door_Thickness)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_door.y_loc('IF(Inset_Front,Door_Thickness,-Door_to_Cabinet_Gap)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_door.y_dim('(Width+Right_Overlay-IF(Inset_Front,0,Door_Thickness+Door_to_Cabinet_Gap))*-1',[Width,Inset_Front,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        right_door.cutpart("Cabinet_Door")
        right_door.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        right_door.obj_bp.mv.is_cabinet_door = True
        
        #RIGHT PULL
        right_pull = cabinet_pulls.Standard_Pull()
        right_pull.door_type = self.door_type
        right_pull.draw()
        right_pull.set_name(right_pull.pull_name)
        right_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(right_pull)
        right_pull.x_loc('IF(Inset_Front,0,Door_to_Cabinet_Gap+Door_Thickness)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_pull.y_loc('IF(Inset_Front,Door_Thickness,-Door_to_Cabinet_Gap)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness])
        right_pull.y_dim('(Width+Right_Overlay-IF(Inset_Front,0,Door_Thickness+Door_to_Cabinet_Gap))*-1',[Width,Inset_Front,Right_Overlay,Door_Thickness,Door_to_Cabinet_Gap])
        right_pull.prompt('Hide','IF(Left_Swing,IF(No_Pulls,True,False),True)',[Left_Swing,No_Pulls])
        
        self.update()
        
class Vertical_Drawers(fd_types.Assembly):
    library_name = "Frameless Cabinet Inserts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".drawer_prompts"
    
    drawer_qty = 1
    
    front_heights = []
    
    add_pull = True
    add_drawer = True
    use_buyout_box = True
    
    def add_common_prompts(self):
        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_drawer_prompts(self)
        add_frameless_overlay_prompts(self)
    
    def add_drawer_front(self,i,prev_drawer_empty):
        Drawer_Front_Height = self.get_var("Drawer Front " + str(i) + " Height","Drawer_Front_Height")
        Depth = self.get_var("dim_y","Depth")
        Height = self.get_var("dim_z","Height")
        Width = self.get_var("dim_x","Width")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Vertical_Gap = self.get_var("Vertical Gap")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Front_Thickness = self.get_var("Front Thickness")
        No_Pulls = self.get_var("No Pulls")
        Inset_Front = self.get_var("Inset Front")
        Horizontal_Grain = self.get_var("Horizontal Grain")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Open_Drawers = self.get_var("Open Drawers")
        
        front_empty = self.add_empty()
        
        if prev_drawer_empty:
            prev_drawer_z_loc = prev_drawer_empty.get_var('loc_z','prev_drawer_z_loc')
            front_empty.z_loc('prev_drawer_z_loc-Drawer_Front_Height-Vertical_Gap',[prev_drawer_z_loc,Drawer_Front_Height,Vertical_Gap])
        else:
            front_empty.z_loc('Height-Drawer_Front_Height+Top_Overlay',[Height,Drawer_Front_Height,Top_Overlay])        
        
        drawer_z_loc = front_empty.get_var("loc_z","drawer_z_loc")
        
        drawer_front = self.add_assembly(DRAWER_FRONT)
        drawer_front.set_name("Drawer Front")
        drawer_front.x_loc('-Left_Overlay',[Left_Overlay])
        drawer_front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open_Drawers)',
                           [Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open_Drawers])
        drawer_front.z_loc('drawer_z_loc',[drawer_z_loc])
        drawer_front.x_rot('IF(Horizontal_Grain,radians(90),0)',[Horizontal_Grain])
        drawer_front.y_rot('IF(Horizontal_Grain,0,radians(-90))',[Horizontal_Grain])
        drawer_front.z_rot('IF(Horizontal_Grain,0,radians(90))',[Horizontal_Grain])
        drawer_front.x_dim('IF(Horizontal_Grain,(Width+Left_Overlay+Right_Overlay),Drawer_Front_Height)',
                           [Horizontal_Grain,Drawer_Front_Height,Width,Left_Overlay,Right_Overlay])
        drawer_front.y_dim('IF(Horizontal_Grain,Drawer_Front_Height,(Width+Left_Overlay+Right_Overlay)*-1)',
                           [Horizontal_Grain,Drawer_Front_Height,Width,Left_Overlay,Right_Overlay])        
        drawer_front.z_dim('Front_Thickness',[Front_Thickness])
        drawer_front.cutpart("Cabinet_Drawer_Front")
        drawer_front.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        drawer_front.obj_bp.mv.is_cabinet_drawer_front = True
        
        if self.add_pull:
            pull = cabinet_pulls.Standard_Pull()
            pull.door_type = self.door_type
            pull.draw()
            pull.set_name(pull.pull_name)
            pull.obj_bp.parent = self.obj_bp
            pull.x_loc('-Left_Overlay',[Left_Overlay])
            pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open_Drawers)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open_Drawers])
            pull.z_loc('drawer_z_loc',[drawer_z_loc])
            pull.x_rot(value = 90)
            pull.y_rot(value = 0)
            pull.z_rot(value = 0)
            pull.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
            pull.y_dim('Drawer_Front_Height',[Drawer_Front_Height])
            pull.z_dim('Front_Thickness',[Front_Thickness])
            pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
            pull.prompt("Pull Z Location",'(Width/2)+Right_Overlay',[Width,Right_Overlay])
            pull.prompt("Hide",'IF(No_Pulls,True,False)',[No_Pulls])        
        
        if self.add_drawer:
            if self.use_buyout_box:
                drawer = self.add_assembly(BUYOUT_DRAWER_BOX)
                drawer.material('Drawer_Box_Surface')
            else:
                drawer = drawer_boxes.Wood_Drawer_Box()
                drawer.draw()
                drawer.obj_bp.parent = self.obj_bp
            drawer.set_name("Drawer Box " + str(i))
            drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
            drawer.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open_Drawers)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open_Drawers])
            drawer.z_loc('drawer_z_loc+Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap,drawer_z_loc])
            drawer.x_rot(value = 0)
            drawer.y_rot(value = 0)
            drawer.z_rot(value = 0)
            drawer.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
            drawer.y_dim('Depth-Drawer_Box_Rear_Gap-IF(Inset_Front,Front_Thickness,0)',[Depth,Drawer_Box_Rear_Gap,Inset_Front,Front_Thickness])
            drawer.z_dim('Drawer_Front_Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap',[Drawer_Front_Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])        
        
        return front_empty
        
    def draw(self):
        self.create_assembly()
        self.add_common_prompts()

        self.add_tab(name='Drawer Front Heights',tab_type='CALCULATOR',calc_type="ZDIM")
        
        drawer = None
        for i in range(self.drawer_qty):
            equal = True
            height = 0
            if len(self.front_heights) >= i + 1:
                equal = True if self.front_heights[i] == 0 else False
                height = self.front_heights[i]
            self.add_prompt(name="Drawer Front " + str(i+1) + " Height",
                            prompt_type='DISTANCE',
                            value=height,
                            tab_index=2,
                            equal=equal)
            drawer = self.add_drawer_front(i+1,drawer)
            
        Vertical_Gap = self.get_var("Vertical Gap")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
                    
        self.calculator_deduction("Vertical_Gap*(" + str(self.drawer_qty) +"-1)-Top_Overlay-Bottom_Overlay",
                                  [Vertical_Gap,Top_Overlay,Bottom_Overlay])
        
        self.update()        
        
class Horizontal_Drawers(fd_types.Assembly):
    library_name = "Frameless Cabinet Inserts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".drawer_prompts"
    
    drawer_qty = 1
    
    front_heights = []
    
    add_pull = True
    add_drawer = True
    use_buyout_box = True
    
    def add_common_prompts(self):
        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_drawer_prompts(self)
        add_frameless_overlay_prompts(self)
    
    def add_drawer_front(self,i,prev_drawer_empty):
        Depth = self.get_var("dim_y","Depth")
        Height = self.get_var("dim_z","Height")
        Width = self.get_var("dim_x","Width")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Division_Overlay = self.get_var("Division Overlay")
        Vertical_Gap = self.get_var("Vertical Gap")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Front_Thickness = self.get_var("Front Thickness")
        No_Pulls = self.get_var("No Pulls")
        Inset_Front = self.get_var("Inset Front")
        Horizontal_Grain = self.get_var("Horizontal Grain")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Open_Drawers = self.get_var("Open Drawers")
        
        front_empty = self.add_empty()
        
        drawer_front_width = '((Left_Overlay+Right_Overlay+Width-(Vertical_Gap*' + str(self.drawer_qty - 1) + '))/' + str(self.drawer_qty) + ')'
        
        if prev_drawer_empty:
            prev_drawer_x_loc = prev_drawer_empty.get_var('loc_x','prev_drawer_x_loc')
            front_empty.x_loc('prev_drawer_x_loc+Vertical_Gap+' + drawer_front_width,
                              [prev_drawer_x_loc,Width,Vertical_Gap,Left_Overlay,Right_Overlay])
        else:
            front_empty.x_loc('-Left_Overlay',[Left_Overlay])
        
        drawer_x_loc = front_empty.get_var("loc_x","drawer_x_loc")
        
        drawer_front = self.add_assembly(DRAWER_FRONT)
        drawer_front.set_name("Drawer Front")
        drawer_front.x_loc('drawer_x_loc',[drawer_x_loc])
        drawer_front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open_Drawers)',
                           [Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open_Drawers])
        drawer_front.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        drawer_front.x_rot('IF(Horizontal_Grain,radians(90),0)',[Horizontal_Grain])
        drawer_front.y_rot('IF(Horizontal_Grain,0,radians(-90))',[Horizontal_Grain])
        drawer_front.z_rot('IF(Horizontal_Grain,0,radians(90))',[Horizontal_Grain])
        drawer_front.x_dim('IF(Horizontal_Grain,' + drawer_front_width + ',Height+Top_Overlay+Bottom_Overlay)',
                           [Horizontal_Grain,Height,Width,Top_Overlay,Bottom_Overlay,Width,Vertical_Gap,Left_Overlay,Right_Overlay])
        drawer_front.y_dim('IF(Horizontal_Grain,Height+Top_Overlay+Bottom_Overlay,(' + drawer_front_width + ')*-1)',
                           [Horizontal_Grain,Height,Width,Top_Overlay,Bottom_Overlay,Width,Vertical_Gap,Left_Overlay,Right_Overlay])       
        drawer_front.z_dim('Front_Thickness',[Front_Thickness])
        drawer_front.cutpart("Cabinet_Drawer_Front")
        drawer_front.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        drawer_front.obj_bp.mv.is_cabinet_drawer_front = True
        
        if self.add_pull:
            pull = cabinet_pulls.Standard_Pull()
#             pull.door_type = self.door_type
            pull.draw()
            pull.set_name(pull.pull_name)
            pull.obj_bp.parent = self.obj_bp
            pull.x_loc('drawer_x_loc',[drawer_x_loc])
            pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open_Drawers)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open_Drawers])
            pull.z_loc('-Bottom_Overlay',[Bottom_Overlay])
            pull.x_rot(value = 90)
            pull.y_rot(value = 0)
            pull.z_rot(value = 0)
            pull.x_dim(drawer_front_width,[Left_Overlay,Right_Overlay,Width,Vertical_Gap])
            pull.y_dim('Height+Top_Overlay+Bottom_Overlay',[Height,Top_Overlay,Bottom_Overlay])
            pull.z_dim('Front_Thickness',[Front_Thickness])
            pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
            pull.prompt("Pull Z Location",drawer_front_width + "/2",[Left_Overlay,Right_Overlay,Width,Vertical_Gap])
            pull.prompt("Hide",'IF(No_Pulls,True,False)',[No_Pulls])        
         
        if self.add_drawer:
            if self.use_buyout_box:
                drawer = self.add_assembly(BUYOUT_DRAWER_BOX)
                drawer.material('Drawer_Box_Surface')
            else:
                drawer = drawer_boxes.Wood_Drawer_Box()
                drawer.draw()
                drawer.obj_bp.parent = self.obj_bp
            drawer.set_name("Drawer Box " + str(i))
            if i == 1: #FIRST
                drawer.x_loc('drawer_x_loc+Left_Overlay+Drawer_Box_Slide_Gap',[drawer_x_loc,Left_Overlay,Drawer_Box_Slide_Gap])
                drawer.x_dim(drawer_front_width + "-Left_Overlay-Division_Overlay-(Drawer_Box_Slide_Gap*2)",[Left_Overlay,Division_Overlay,Right_Overlay,Width,Vertical_Gap,Drawer_Box_Slide_Gap])
            elif i == self.drawer_qty: #LAST
                drawer.x_loc('drawer_x_loc+Division_Overlay+Drawer_Box_Slide_Gap',[drawer_x_loc,Division_Overlay,Drawer_Box_Slide_Gap])
                drawer.x_dim(drawer_front_width + "-Right_Overlay-Division_Overlay-(Drawer_Box_Slide_Gap*2)",[Left_Overlay,Right_Overlay,Division_Overlay,Width,Vertical_Gap,Drawer_Box_Slide_Gap])
            else: #MIDDLE
                drawer.x_loc('drawer_x_loc+Division_Overlay+Drawer_Box_Slide_Gap',[drawer_x_loc,Division_Overlay,Drawer_Box_Slide_Gap])
                drawer.x_dim(drawer_front_width + '-(Division_Overlay*2)-(Drawer_Box_Slide_Gap*2)',[Left_Overlay,Right_Overlay,Division_Overlay,Width,Vertical_Gap,Drawer_Box_Slide_Gap])
            drawer.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open_Drawers)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open_Drawers])
            drawer.z_loc('Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap])
            drawer.x_rot(value = 0)
            drawer.y_rot(value = 0)
            drawer.z_rot(value = 0)
            drawer.y_dim('Depth-Drawer_Box_Rear_Gap-IF(Inset_Front,Front_Thickness,0)',[Depth,Drawer_Box_Rear_Gap,Inset_Front,Front_Thickness])
            drawer.z_dim('Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])        
        
        return front_empty
        
    def draw(self):
        self.create_assembly()
        self.add_common_prompts()
        
        drawer = None
        for i in range(self.drawer_qty):
            drawer = self.add_drawer_front(i+1,drawer)

            if i != 0:
                drawer_x_loc = drawer.get_var('loc_x','drawer_x_loc')
                Height = self.get_var('dim_z',"Height")
                Depth = self.get_var('dim_y',"Depth")
                Division_Thickness = self.get_var("Division Thickness")
                Inset_Front = self.get_var("Inset Front")
                Front_Thickness = self.get_var("Front Thickness")
                Vertical_Gap = self.get_var("Vertical Gap")
                
                division = self.add_assembly(DIVISION)
                division.set_name("Drawer Division")
                division.x_loc('drawer_x_loc-(Division_Thickness/2)-(Vertical_Gap/2)',[drawer_x_loc,Division_Thickness,Vertical_Gap])
                division.y_loc('IF(Inset_Front,Front_Thickness,0)',[Inset_Front,Front_Thickness])
                division.z_loc(value = 0)
                division.x_rot(value = 90)
                division.y_rot(value = 0)
                division.z_rot(value = 90)
                division.x_dim('Depth-IF(Inset_Front,Front_Thickness,0)',[Depth,Inset_Front,Front_Thickness])
                division.y_dim('Height',[Height])
                division.z_dim('Division_Thickness',[Division_Thickness])
                division.cutpart("Cabinet_Division")

        self.update()
        
class Tilt_Out_Hamper(fd_types.Assembly):

    library_name = "Frameless Cabinet Inserts"
    placement_type = "EXTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".hamper_prompts"
    type_assembly = "INSERT"
    mirror_y = False
    
    def add_common_prompts(self):
        props = cabinet_properties.get_scene_props().exterior_defaults

        self.add_tab(name='Hamper Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_frameless_overlay_prompts(self)
        
        self.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Center Pulls on Drawers",prompt_type='CHECKBOX',value=props.center_pulls_on_drawers,tab_index=0)
        self.add_prompt(name="Drawer Pull From Top",prompt_type='DISTANCE',value=props.drawer_pull_from_top,tab_index=0)
        self.add_prompt(name="Pull Double Max Span",prompt_type='DISTANCE',value=unit.inch(30),tab_index=0)
        self.add_prompt(name="Lock From Top",prompt_type='DISTANCE',value=unit.inch(1.0),tab_index=0)
        self.add_prompt(name="Lock Drawer",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)

    def draw(self):
        
        self.create_assembly()
        
        self.add_common_prompts()
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Front_Thickness = self.get_var("Front Thickness")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Open = self.get_var("Open")
        Inset_Front = self.get_var("Inset Front")
        
        front = self.add_assembly(DOOR)
        front.set_name("Hamper Door")
        front.x_loc('-Left_Overlay',[Left_Overlay])
        front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)',[Door_to_Cabinet_Gap,Inset_Front,Front_Thickness])
        front.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        front.x_rot(value = 0)
        front.y_rot('radians(-90)-(Open*.5)',[Open])
        front.z_rot(value = 90)
        front.x_dim('Height+Top_Overlay+Bottom_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        front.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
        front.z_dim('Front_Thickness',[Front_Thickness])
        front.cutpart("Cabinet_Door")
        front.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        front.obj_bp.mv.is_cabinet_door = True
        
        pull = cabinet_pulls.Standard_Pull()
        pull.door_type = "Drawer"
        pull.draw()
        pull.set_name('Cabinet Pull')
        pull.obj_bp.parent = self.obj_bp
        pull.set_name(pull.pull_name)
        pull.x_loc('-Left_Overlay',[Left_Overlay])
        pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)',[Door_to_Cabinet_Gap,Inset_Front,Front_Thickness])
        pull.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        pull.x_rot('radians(90)+(Open*.5)',[Open])
        pull.y_rot(value = 0)
        pull.z_rot(value = 0)
        pull.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
        pull.y_dim('Height+Top_Overlay+Bottom_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        pull.z_dim('Front_Thickness',[Front_Thickness])
        pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
        pull.prompt("Pull Z Location",'(Width/2)+Right_Overlay',[Width,Right_Overlay])
        
        basket_1 = self.add_assembly(WIRE_BASKET)
        basket_1.set_name("Hamper Basket")
        basket_1.x_loc(value = 0)
        basket_1.y_loc(value = 0)
        basket_1.z_loc(value = 0)
        basket_1.x_rot('Open*.5',[Open])
        basket_1.y_rot(value = 0)
        basket_1.z_rot(value = 0)
        basket_1.x_dim('Width',[Width])
        basket_1.y_dim('Depth',[Depth])
        basket_1.z_dim('Height-INCH(8)',[Height])
        basket_1.material('Wire Basket')
        
        self.update()
        


#---------INSERTS

class INSERT_Base_Single_Door(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Single Door"
        self.door_type = "Base"
        self.door_swing = "Left Swing"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Base_Single_Door_With_False_Front(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Single Door with False Front"
        self.door_type = "Base"
        self.door_swing = "Left Swing"
        self.false_front_qty = 1
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Base_Double_Door(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Double Door"
        self.door_type = "Base"
        self.door_swing = "Double Door"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Base_Double_Door_With_False_Front(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Double Door with False Front"
        self.door_type = "Base"
        self.door_swing = "Double Door"
        self.false_front_qty = 1
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Base_Double_Door_With_2_False_Front(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Double Door with 2 False Front"
        self.door_type = "Base"
        self.door_swing = "Double Door"
        self.false_front_qty = 2
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Tall_Single_Door(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Tall Single Door"
        self.door_type = "Tall"
        self.door_swing = "Left Swing"
        self.width = unit.inch(18)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)

class INSERT_Tall_Double_Door(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Tall Double Door"
        self.door_type = "Tall"
        self.door_swing = "Double Door"
        self.width = unit.inch(36)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)
    
class INSERT_Upper_Single_Door(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Upper Single Door"
        self.door_type = "Upper"
        self.door_swing = "Left Swing"
        self.width = unit.inch(18)
        self.height = unit.inch(42)
        self.depth = unit.inch(23)

class INSERT_Upper_Double_Door(Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Upper Double Door"
        self.door_type = "Upper"
        self.door_swing = "Double Door"
        self.width = unit.inch(36)
        self.height = unit.inch(42)
        self.depth = unit.inch(23)
        
class INSERT_1_Drawer(Vertical_Drawers):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().exterior_defaults
        self.category_name = "Drawers"
        self.assembly_name = "1 Drawer"
        self.door_type = "Drawer"
        self.width = unit.inch(18)
        self.height = unit.inch(6)
        self.depth = unit.inch(19)
        self.mirror_y = False
        self.use_buyout_box = props.use_buyout_drawer_boxes
        
class INSERT_2_Drawer_Stack(Vertical_Drawers):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().exterior_defaults
        self.category_name = "Drawers"
        self.assembly_name = "2 Drawer Stack"
        self.door_type = "Drawer"
        self.direction = 'Vertical'
        self.drawer_qty = 2
        self.width = unit.inch(18)
        self.height = unit.inch(6*2)
        self.depth = unit.inch(19)
        self.mirror_y = False
        self.use_buyout_box = props.use_buyout_drawer_boxes
        
class INSERT_3_Drawer_Stack(Vertical_Drawers):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().exterior_defaults
        self.category_name = "Drawers"
        self.assembly_name = "3 Drawer Stack"
        self.door_type = "Drawer"
        self.direction = 'Vertical'
        self.drawer_qty = 3
        self.width = unit.inch(18)
        self.height = unit.inch(6*3)
        self.depth = unit.inch(19)
        self.mirror_y = False
        self.use_buyout_box = props.use_buyout_drawer_boxes
        
class INSERT_4_Drawer_Stack(Vertical_Drawers):
    
    def __init__(self):
        props = cabinet_properties.get_scene_props().exterior_defaults
        self.category_name = "Drawers"
        self.assembly_name = "4 Drawer Stack"
        self.door_type = "Drawer"
        self.direction = 'Vertical'
        self.drawer_qty = 4
        self.width = unit.inch(18)
        self.height = unit.inch(6*4)
        self.depth = unit.inch(19)
        self.mirror_y = False
        self.use_buyout_box = props.use_buyout_drawer_boxes
        
class INSERT_Horizontal_Drawers(Horizontal_Drawers):
     
    def __init__(self):
        self.category_name = "Drawers"
        self.assembly_name = "Horizontal Drawers"
        self.width = unit.inch(36)
        self.height = unit.inch(6)
        self.depth = unit.inch(20)
        self.mirror_y = False
        self.drawer_qty = 2
        
class INSERT_Base_Pie_Cut_Door(Pie_Cut_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Pie Cut Door"
        self.door_type = "Base"
        self.door_swing = "Left Swing"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Upper_Pie_Cut_Door(Pie_Cut_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Upper Pie Cut Door"
        self.door_type = "Upper"
        self.door_swing = "Left Swing"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
#---------INSERT: TILT-OUT HAMPER

class INSERT_Tilt_Out_Hamper(Tilt_Out_Hamper):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Tilt Out Hamper"
        self.width = unit.inch(25)
        self.height = unit.inch(25)
        self.depth = unit.inch(19)
        