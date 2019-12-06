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
    
    if assembly.door_swing in {"Left Swing","Right Swing"}:
        assembly.add_prompt(name="Left Swing",prompt_type='CHECKBOX',value=True if assembly.door_swing == 'Left Swing' else False,tab_index=0)
        assembly.add_prompt(name="Right Swing",prompt_type='CHECKBOX',value=False,tab_index=1) # CALCULATED
        
        #CALCULATE RIGHT SWING PROMPT NEEDED FOR MV EXPORT
        Left_Swing = assembly.get_var("Left Swing")
        assembly.prompt('Right Swing','IF(Left_Swing,True,False)',[Left_Swing])
        
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
    assembly.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Horizontal Grain",prompt_type='CHECKBOX',value=props.horizontal_grain_on_drawer_fronts,tab_index=0)
    assembly.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)

    assembly.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0) 
    assembly.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)   
    assembly.add_prompt(name="Drawer Box Top Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
    assembly.add_prompt(name="Drawer Box Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
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
    
    assembly.prompt('Top Overlay','IF(inset,-ir,IF(hot,(tt/2)-(vg/2),tt-tr))',[inset,ir,hot,tt,tr,vg])
    assembly.prompt('Bottom Overlay','IF(inset,-ir,IF(hob,(bt/2)-(vg/2),bt-br))',[inset,ir,hob,bt,br,vg])
    assembly.prompt('Left Overlay','IF(inset,-ir,IF(hol,(lst/2)-(vg/2),lst-lr))',[inset,ir,hol,lst,lr,vg])
    assembly.prompt('Right Overlay','IF(inset,-ir,IF(hor,(rst/2)-(vg/2),rst-rr))',[inset,ir,hor,rst,rr,vg])
        
def add_face_frame_overlay_prompts(assembly):
    assembly.add_prompt(name="Mid Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
    assembly.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    assembly.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    assembly.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    assembly.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
    
    #INHERITED
    assembly.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=0,tab_index=1)    

class FF_Doors(fd_types.Assembly):
    
    library_name = "Face Frame Cabinet Inserts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".door_prompts"
    door_type = "" # {Base, Tall, Upper}
    door_swing = "" # {Left Swing, Right Swing, Double Door, Flip up}

    def add_doors_prompts(self):
        
        self.add_tab(name='Door Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_door_prompts(self)
        
        add_face_frame_overlay_prompts(self)
        
        #For Diagonal Corner Cabinet
        self.add_prompt(name="Door Y Offset",prompt_type='DISTANCE',value=0,tab_index=1)
        
    def set_standard_drivers(self,assembly):
        Height = self.get_var('dim_z','Height')
        Inset_Front = self.get_var("Inset Front")
        Inset_Reveal = self.get_var("Inset Reveal")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Door_Thickness = self.get_var("Door Thickness")
        Frame_Top_Gap = self.get_var("Frame Top Gap")
        Frame_Bottom_Gap = self.get_var("Frame Bottom Gap")
        Frame_Thickness = self.get_var("Frame Thickness")
        #For Diagonal Corner Cabinet
        Door_Y_Offset = self.get_var("Door Y Offset")        
        
        
        assembly.y_loc('IF(Inset_Front,Door_Y_Offset,-Door_to_Cabinet_Gap-Frame_Thickness)',[Inset_Front,Door_to_Cabinet_Gap,Door_Thickness,Frame_Thickness,Door_Y_Offset])
        assembly.z_loc('IF(Inset_Front,Frame_Bottom_Gap+Inset_Reveal,Frame_Bottom_Gap-Bottom_Overlay)',
                       [Inset_Front,Frame_Bottom_Gap,Inset_Reveal,Frame_Bottom_Gap,Bottom_Overlay])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = -90)
        assembly.x_dim('Height-(Frame_Top_Gap+Frame_Bottom_Gap)+IF(Inset_Front,-(Inset_Reveal*2),Bottom_Overlay+Top_Overlay)',
                       [Inset_Front,Height,Top_Overlay,Bottom_Overlay,Frame_Top_Gap,Frame_Bottom_Gap,Inset_Reveal])
        assembly.z_dim('Door_Thickness',[Door_Thickness])
        
    def set_pull_drivers(self,assembly):
        self.set_standard_drivers(assembly)
        
        Height = self.get_var('dim_z','Height')
        Pull_Length = assembly.get_var("Pull Length")
        Pull_From_Edge = self.get_var("Pull From Edge")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        
        assembly.prompt("Pull X Location",'Pull_From_Edge',[Pull_From_Edge])
        if self.door_type == "Base":
            assembly.prompt("Pull Z Location",'Base_Pull_Location+(Pull_Length/2)',[Base_Pull_Location,Pull_Length])
        if self.door_type == "Tall":
            assembly.prompt("Pull Z Location",'Height-Tall_Pull_Location+(Pull_Length/2)+World_Z',[Height,World_Z,Tall_Pull_Location,Pull_Length])
        if self.door_type == "Upper":
            assembly.prompt("Pull Z Location",'Height-Upper_Pull_Location-(Pull_Length/2)',[Height,Upper_Pull_Location,Pull_Length])
    
    def draw(self):
        self.create_assembly()
        
        self.add_doors_prompts()
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Inset_Front = self.get_var("Inset Front")
        Inset_Reveal = self.get_var("Inset Reveal")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Door_Rotation = self.get_var("Door Rotation")
        Mid_Rail_Width = self.get_var("Mid Rail Width")
        No_Pulls = self.get_var("No Pulls")
        Left_Swing = self.get_var("Left Swing")
        
        Frame_Left_Gap = self.get_var("Frame Left Gap")
        Frame_Right_Gap = self.get_var("Frame Right Gap")
        Frame_Top_Gap = self.get_var("Frame Top Gap")
        Frame_Bottom_Gap = self.get_var("Frame Bottom Gap")
        
        left_door = self.add_assembly(DOOR)
        left_door.set_name("Left Cabinet Door")
        self.set_standard_drivers(left_door)
        left_door.x_loc('Frame_Left_Gap+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Frame_Left_Gap,Left_Overlay,Inset_Front,Inset_Reveal])
        left_door.z_rot('radians(90)-Door_Rotation',[Door_Rotation])
        if self.door_swing == "Double Door":
            left_door.y_dim('(((Width-(Frame_Left_Gap+Frame_Right_Gap)-Mid_Rail_Width)/2)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay)))*-1',
                            [Width,Frame_Left_Gap,Frame_Right_Gap,Left_Overlay,Right_Overlay,Mid_Rail_Width,Inset_Reveal,Inset_Front])
        else:
            left_door.y_dim('(Width-(Frame_Left_Gap+Frame_Right_Gap)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay)))*-1',
                            [Width,Frame_Left_Gap,Frame_Right_Gap,Left_Overlay,Right_Overlay,Inset_Front,Inset_Reveal])
            left_door.prompt("Hide",'IF(Left_Swing,False,True)',[Left_Swing])
        left_door.cutpart("Cabinet_Door")
        left_door.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        left_door.obj_bp.mv.is_cabinet_door = True
        
        left_pull = cabinet_pulls.Standard_Pull()
        left_pull.door_type = self.door_type
        left_pull.door_swing = "Left Swing"
        left_pull.draw()
        left_pull.set_name(left_pull.pull_name)
        left_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(left_pull)
        left_pull.x_loc('Frame_Left_Gap+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Frame_Left_Gap,Left_Overlay,Inset_Front,Inset_Reveal])
        left_pull.z_rot('radians(90)-Door_Rotation',[Door_Rotation])
        if self.door_swing == 'Double Door':
            left_pull.y_dim('(((Width-(Frame_Left_Gap+Frame_Right_Gap)-Mid_Rail_Width)/2)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay)))*-1',
                            [Width,Frame_Left_Gap,Frame_Right_Gap,Left_Overlay,Right_Overlay,Mid_Rail_Width,Inset_Reveal,Inset_Front])
            left_pull.prompt('Hide','IF(No_Pulls,True,False)',[No_Pulls])
        else:
            left_pull.y_dim('(Width-(Frame_Left_Gap+Frame_Right_Gap)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay)))*-1',
                            [Width,Frame_Left_Gap,Frame_Right_Gap,Left_Overlay,Right_Overlay,Inset_Front,Inset_Reveal])
            left_pull.prompt('Hide','IF(Left_Swing,IF(No_Pulls,True,False),True)',[Left_Swing,No_Pulls])
        
        right_door = self.add_assembly(DOOR)
        right_door.set_name("Right Cabinet Door")
        self.set_standard_drivers(right_door)
        right_door.x_loc('Width-Frame_Right_Gap+IF(Inset_Front,-Inset_Reveal,Right_Overlay)',[Width,Frame_Right_Gap,Right_Overlay,Inset_Front,Inset_Reveal])
        right_door.z_rot('radians(90)+Door_Rotation',[Door_Rotation])
        if self.door_swing == "Double Door":
            right_door.y_dim('((Width-(Frame_Left_Gap+Frame_Right_Gap)-Mid_Rail_Width)/2)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay))',
                             [Width,Frame_Left_Gap,Frame_Right_Gap,Left_Overlay,Right_Overlay,Mid_Rail_Width,Inset_Front,Inset_Reveal])
        else:
            right_door.y_dim('Width-(Frame_Left_Gap+Frame_Right_Gap)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay))',
                             [Width,Frame_Left_Gap,Frame_Right_Gap,Inset_Front,Inset_Reveal,Left_Overlay,Right_Overlay])
            right_door.prompt("Hide",'IF(Left_Swing,True,False)',[Left_Swing])
        right_door.cutpart("Cabinet_Door")
        right_door.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        right_door.obj_bp.mv.is_cabinet_door = True
        
        right_pull = cabinet_pulls.Standard_Pull()
        right_pull.door_type = self.door_type
        right_pull.door_swing = "Left Swing"
        right_pull.draw()
        right_pull.set_name(right_pull.pull_name)
        right_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(right_pull)
        right_pull.x_loc('Width-Frame_Right_Gap+IF(Inset_Front,-Inset_Reveal,Right_Overlay)',[Width,Frame_Right_Gap,Right_Overlay,Inset_Front,Inset_Reveal])
        right_pull.z_rot('radians(90)+Door_Rotation',[Door_Rotation])
        if self.door_swing == "Double Door":
            right_pull.y_dim('((Width-(Frame_Left_Gap+Frame_Right_Gap)-Mid_Rail_Width)/2)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay))',
                             [Width,Frame_Left_Gap,Frame_Right_Gap,Left_Overlay,Right_Overlay,Mid_Rail_Width,Inset_Front,Inset_Reveal])
            right_pull.prompt('Hide','IF(No_Pulls,True,False)',[No_Pulls])
        else:
            right_pull.y_dim('Width-(Frame_Left_Gap+Frame_Right_Gap)+IF(Inset_Front,-(Inset_Reveal*2),(Left_Overlay+Right_Overlay))',
                             [Width,Frame_Left_Gap,Frame_Right_Gap,Inset_Front,Inset_Reveal,Left_Overlay,Right_Overlay])
            right_pull.prompt('Hide','IF(Left_Swing,True,IF(No_Pulls,True,False))',[Left_Swing,No_Pulls])
        
        if self.door_swing == "Double Door":
            frame_opening = self.add_assembly(HARDWOOD)  
            frame_opening.set_name("Frame Opening")
            frame_opening.x_loc('Frame_Left_Gap+((Width-(Frame_Left_Gap+Frame_Right_Gap))/2)-(Mid_Rail_Width/2)',[Frame_Left_Gap,Width,Frame_Right_Gap,Mid_Rail_Width])
            frame_opening.y_loc(value = 0)
            frame_opening.z_loc('Frame_Bottom_Gap',[Frame_Bottom_Gap])
            frame_opening.x_rot(value = 0)
            frame_opening.y_rot(value = -90)
            frame_opening.z_rot(value = -90)
            frame_opening.x_dim('Height-(Frame_Top_Gap+Frame_Bottom_Gap)',[Height,Frame_Top_Gap,Frame_Bottom_Gap])
            frame_opening.y_dim('Mid_Rail_Width',[Mid_Rail_Width])
            frame_opening.z_dim(value = unit.inch(-.75))
            frame_opening.material('Exposed_Exterior_Surface')
            frame_opening.solid_stock("Hardwood")
            frame_opening.edgebanding('Cabinet_Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        
        self.update()

class FF_Pie_Cut_Doors(fd_types.Assembly):
    
    library_name = "Face Frame Cabinet Inserts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".door_prompts"
    door_type = "" # {Base, Tall, Upper}
    door_swing = "" # {Left Swing, Right Swing, Double Door, Flip up}    
    
    def add_doors_prompts(self):
        self.add_tab(name='Door Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_door_prompts(self)
        
        add_face_frame_overlay_prompts(self)        
        
        #CALCULATED
        self.add_prompt(name="Right Side Depth",prompt_type="DISTANCE",value=unit.inch(23),tab_index=0)
        self.add_prompt(name="Left Side Depth",prompt_type="DISTANCE",value=unit.inch(23),tab_index=0)
        
        
    def set_shared_drivers(self,assembly,left_side=True):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Left_Side_Depth = self.get_var("Left Side Depth")
        Right_Side_Depth = self.get_var("Right Side Depth")
        Inset_Front = self.get_var("Inset Front")
        Inset_Reveal = self.get_var("Inset Reveal")
        Door_Thickness = self.get_var("Door Thickness")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")        
        Frame_Left_Gap = self.get_var("Frame Left Gap")
        Frame_Right_Gap = self.get_var("Frame Right Gap")
        Frame_Top_Gap = self.get_var("Frame Top Gap")
        Frame_Bottom_Gap = self.get_var("Frame Bottom Gap")
        
        if left_side == True:
            assembly.x_loc("Left_Side_Depth+IF(Inset_Front,-Door_Thickness,Door_to_Cabinet_Gap)",
                           [Left_Side_Depth,Door_to_Cabinet_Gap,Inset_Front,Door_Thickness])     
            assembly.y_loc("Depth+Frame_Left_Gap-IF(Inset_Front,-Inset_Reveal,Left_Overlay)",
                           [Depth,Left_Overlay,Inset_Front,Inset_Reveal,Frame_Left_Gap])         
            assembly.z_loc("Frame_Bottom_Gap+IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)",
                           [Inset_Front,Bottom_Overlay,Inset_Reveal,Frame_Bottom_Gap])   
            
            assembly.y_rot(value=-90)
            assembly.z_rot(value=180)    
            
            assembly.x_dim("Height-Frame_Bottom_Gap-Frame_Top_Gap+IF(Inset_Front,-Inset_Reveal*2,Bottom_Overlay+Top_Overlay)",
                           [Height,Inset_Front,Bottom_Overlay,Top_Overlay,Inset_Reveal,Frame_Bottom_Gap,Frame_Top_Gap])  
        
        else:
            assembly.x_loc("Left_Side_Depth+IF(Inset_Front,0,Door_Thickness+Door_to_Cabinet_Gap)",
                           [Left_Side_Depth,Door_Thickness,Door_to_Cabinet_Gap,Inset_Front])
            assembly.y_loc("-Right_Side_Depth-IF(Inset_Front,-Door_Thickness,Door_to_Cabinet_Gap)",
                           [Right_Side_Depth,Door_to_Cabinet_Gap,Door_Thickness,Inset_Front])        
            assembly.z_loc("Frame_Bottom_Gap+IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)",
                           [Inset_Front,Bottom_Overlay,Inset_Reveal,Frame_Bottom_Gap])        
        
            assembly.y_rot(value=-90)
            assembly.z_rot(value=90)     
            
            assembly.x_dim("Height-Frame_Bottom_Gap-Frame_Top_Gap+IF(Inset_Front,-Inset_Reveal*2,Bottom_Overlay+Top_Overlay)",
                           [Height,Inset_Front,Bottom_Overlay,Top_Overlay,Inset_Reveal,Frame_Bottom_Gap,Frame_Top_Gap])
            assembly.y_dim("(-Width+Left_Side_Depth+Frame_Right_Gap)+IF(Inset_Front,Inset_Reveal,+Door_Thickness+Door_to_Cabinet_Gap-Right_Overlay)",
                           [Width,Left_Side_Depth,Door_Thickness,Right_Overlay,Inset_Front,Door_to_Cabinet_Gap,Inset_Reveal,Frame_Right_Gap])             
                   
    def set_pull_drivers(self,assembly): 
        Height = self.get_var('dim_z','Height')
        Pull_Length = assembly.get_var("Pull Length")
        Pull_From_Edge = self.get_var("Pull From Edge")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        
        assembly.prompt("Pull X Location",'Pull_From_Edge',[Pull_From_Edge])
        
        if self.door_type == "Base":
            assembly.prompt("Pull Z Location",'Base_Pull_Location+(Pull_Length/2)',[Base_Pull_Location,Pull_Length])
        if self.door_type == "Tall":
            assembly.prompt("Pull Z Location",'Tall_Pull_Location+(Pull_Length/2)',[Tall_Pull_Location,Pull_Length])
        if self.door_type == "Upper":
            assembly.prompt("Pull Z Location",'Height-Upper_Pull_Location-(Pull_Length/2)',[Height,Upper_Pull_Location,Pull_Length])
    
    def draw(self):
        self.create_assembly()
        
        self.add_doors_prompts()
        
        Depth = self.get_var('dim_y','Depth')
        Left_Overlay = self.get_var("Left Overlay")
        Left_Swing = self.get_var("Left Swing")
        No_Pulls = self.get_var("No Pulls")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Door_Thickness = self.get_var("Door Thickness")
        Inset_Front = self.get_var("Inset Front")
        Right_Side_Depth = self.get_var("Right Side Depth")
        Frame_Left_Gap = self.get_var("Frame Left Gap")
        
        #LEFT DOOR
        left_door = self.add_assembly(DOOR)  
        left_door.set_name("Left Cabinet Door")
        left_door.cutpart("Cabinet_Door")
        left_door.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        self.set_shared_drivers(left_door,True)
        left_door.y_dim("(Depth+Right_Side_Depth+Door_Thickness+Door_to_Cabinet_Gap+Frame_Left_Gap)-IF(Inset_Front,Door_Thickness,Left_Overlay)",
                        [Depth,Right_Side_Depth,Door_Thickness,Inset_Front,Left_Overlay,Door_to_Cabinet_Gap,Frame_Left_Gap])
        left_door.obj_bp.mv.is_cabinet_door = True
        
        #LEFT PULL
        left_pull = cabinet_pulls.Standard_Pull()
        left_pull.door_type = self.door_type
        left_pull.draw()
        left_pull.set_name(left_pull.pull_name)
        left_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(left_pull)
        self.set_shared_drivers(left_pull,True)
        left_pull.z_dim("Door_Thickness",[Door_Thickness])  
        left_pull.prompt("Hide","IF(No_Pulls,True,IF(Left_Swing,True,False))",[No_Pulls,Left_Swing])

        #RIGHT DOOR
        right_door = self.add_assembly(DOOR)  
        right_door.set_name("Right Cabinet Door")
        right_door.cutpart("Cabinet_Door")
        right_door.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        self.set_shared_drivers(right_door,False)
        right_door.obj_bp.mv.is_cabinet_door = True
        
        #RIGHT PULL
        right_pull = cabinet_pulls.Standard_Pull()
        right_pull.door_type = self.door_type
        right_pull.draw()
        right_pull.set_name(right_pull.pull_name)
        right_pull.obj_bp.parent = self.obj_bp
        self.set_pull_drivers(right_pull) 
        self.set_shared_drivers(right_pull,False)
        right_pull.z_dim("Door_Thickness",[Door_Thickness])
        right_pull.prompt("Hide","IF(No_Pulls,True,IF(Left_Swing,False,True))",[No_Pulls,Left_Swing])   
           
        self.update()    
        
class FF_Drawer(fd_types.Assembly):
    
    library_name = "Face Frame Cabinet Inserts"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".drawer_prompts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    
    door_type = "Drawer"
    direction = 'Vertical'
    add_drawer = True
    add_pull = True
    add_slide = False
    use_buyout_box = True
    
    def add_drawer_prompts(self):
        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_drawer_prompts(self)
        
        add_face_frame_overlay_prompts(self)
        
        self.add_prompt(name="Drawer Slide Quantity",prompt_type='QUANTITY',value=1,tab_index=1)

        #CALCULATIONS
        Frame_Left_Gap = self.get_var("Frame Left Gap")
        Frame_Right_Gap = self.get_var("Frame Right Gap")
        Inset_Front = self.get_var("Inset Front")
        Inset_Reveal = self.get_var("Inset Reveal")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        
        self.add_prompt(name="Left Drawer Front Extension",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Right Drawer Front Extension",prompt_type='DISTANCE',value=0,tab_index=1)
        self.prompt('Left Drawer Front Extension','-Frame_Left_Gap+IF(Inset_Front,Inset_Reveal,Left_Overlay)',[Frame_Left_Gap,Inset_Front,Inset_Reveal,Left_Overlay])
        self.prompt('Right Drawer Front Extension','-Frame_Right_Gap+IF(Inset_Front,Inset_Reveal,Right_Overlay)',[Frame_Right_Gap,Inset_Front,Inset_Reveal,Right_Overlay])
        
    def draw(self):

        self.create_assembly()
        self.add_drawer_prompts()
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        Frame_Thickness = self.get_var('Frame Thickness')
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Front_Thickness = self.get_var("Front Thickness")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        No_Pulls = self.get_var("No Pulls")
        Frame_Left_Gap = self.get_var("Frame Left Gap")
        Frame_Right_Gap = self.get_var("Frame Right Gap")
        Inset_Front = self.get_var("Inset Front")
        Inset_Reveal = self.get_var("Inset Reveal")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Horizontal_Grain = self.get_var("Horizontal Grain")
        Open = self.get_var("Open")
        Left_Drawer_Front_Extension = self.get_var("Left Drawer Front Extension")
        Right_Drawer_Front_Extension = self.get_var("Right Drawer Front Extension")
        
        if self.add_drawer:
            if self.use_buyout_box:
                drawer = self.add_assembly(BUYOUT_DRAWER_BOX)
                drawer.material('Drawer_Box_Surface')
            else:
                drawer = drawer_boxes.Wood_Drawer_Box()
                drawer.draw()
                drawer.obj_bp.parent = self.obj_bp
            drawer.set_name("Left Drawer Box")
            drawer.x_loc('Frame_Left_Gap+Drawer_Box_Slide_Gap',[Frame_Left_Gap,Drawer_Box_Slide_Gap])
            drawer.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Front_Thickness,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness]) 
            drawer.z_loc('Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap])
            drawer.x_rot(value = 0)
            drawer.y_rot(value = 0)
            drawer.z_rot(value = 0)
            drawer.x_dim('Width-Frame_Left_Gap-Frame_Right_Gap-(Drawer_Box_Slide_Gap)*2',[Width,Frame_Left_Gap,Frame_Right_Gap,Drawer_Box_Slide_Gap])
            drawer.y_dim('IF(Inset_Front,Depth-Drawer_Box_Rear_Gap,Depth+Frame_Thickness+Door_to_Cabinet_Gap-Drawer_Box_Rear_Gap)',[Inset_Front,Frame_Thickness,Door_to_Cabinet_Gap,Depth,Drawer_Box_Rear_Gap])
            drawer.z_dim('Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap-Frame_Top_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap,Frame_Top_Gap])
        
            if self.add_slide:
                drawer_z_loc = drawer.get_var("loc_z","drawer_z_loc")
                drawer_x_loc = drawer.get_var("loc_x","drawer_x_loc")
                drawer_width = drawer.get_var("dim_x","drawer_width")
                 
                l_slide = self.add_assembly(DRAWER_SLIDE)
                l_slide.set_name("Drawer Slide")
                l_slide.x_loc('drawer_x_loc',[drawer_x_loc])
                l_slide.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
                l_slide.z_loc('drawer_z_loc',[drawer_z_loc])
                l_slide.x_rot(value = 0)
                l_slide.y_rot(value = 0)
                l_slide.z_rot(value = 90)
                l_slide.x_dim('Depth-Drawer_Box_Rear_Gap-IF(Inset_Front,Front_Thickness,0)',[Depth,Drawer_Box_Rear_Gap,Inset_Front,Front_Thickness])
                l_slide.y_dim(value = unit.inch(.25))
                l_slide.z_dim(value = unit.inch(.5))
 
                r_slide = self.add_assembly(DRAWER_SLIDE)
                r_slide.set_name("Drawer Slide")
                r_slide.x_loc('drawer_x_loc+drawer_width',[drawer_x_loc,drawer_width])
                r_slide.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Front_Thickness,Depth,Open])
                r_slide.z_loc('drawer_z_loc',[drawer_z_loc])
                r_slide.x_rot(value = 0)
                r_slide.y_rot(value = 0)
                r_slide.z_rot(value = 90)
                r_slide.x_dim('Depth-Drawer_Box_Rear_Gap-IF(Inset_Front,Front_Thickness,0)',[Depth,Drawer_Box_Rear_Gap,Inset_Front,Front_Thickness])
                r_slide.y_dim(value = unit.inch(-.25))
                r_slide.z_dim(value = unit.inch(.5))
        
        front_width = 'Width-Frame_Left_Gap-Frame_Right_Gap+IF(Inset_Front,-(Inset_Reveal)*2,Right_Overlay+Left_Overlay)'
        front_height = 'Height-(Frame_Top_Gap+Frame_Bottom_Gap)+IF(Inset_Front,-(Inset_Reveal)*2,Top_Overlay+Bottom_Overlay)'
        size_vars = [Horizontal_Grain,Width,Inset_Front,Inset_Reveal,Frame_Left_Gap,Frame_Right_Gap,Right_Overlay,Left_Overlay,Height,Top_Overlay,Bottom_Overlay,Frame_Top_Gap,Frame_Bottom_Gap]
        
        front = self.add_assembly(DRAWER_FRONT)
        front.set_name("Left Drawer Front")
        front.x_loc('Frame_Left_Gap+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Frame_Left_Gap,Inset_Front,Inset_Reveal,Left_Overlay])
        front.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness])
        front.z_loc('IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)',[Inset_Front,Inset_Reveal,Bottom_Overlay])
        front.x_rot('IF(Horizontal_Grain,radians(90),0)',[Horizontal_Grain])
        front.y_rot('IF(Horizontal_Grain,0,radians(-90))',[Horizontal_Grain])
        front.z_rot('IF(Horizontal_Grain,0,radians(90))',[Horizontal_Grain])
        front.x_dim('IF(Horizontal_Grain,' + front_width + ',' + front_height + ')',size_vars)
        front.y_dim('IF(Horizontal_Grain,' + front_height + ',(' + front_width + ')*-1)',size_vars)
        front.z_dim('Front_Thickness',[Front_Thickness])
        front.cutpart("Cabinet_Drawer_Front")
        front.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        front.obj_bp.mv.is_cabinet_drawer_front = True
        
        if self.add_pull:
            pull = cabinet_pulls.Standard_Pull()
            pull.door_type = self.door_type
            pull.draw()
            pull.obj_bp.parent = self.obj_bp
            pull.set_name(pull.pull_name)
            pull.x_loc('Frame_Left_Gap+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Frame_Left_Gap,Inset_Front,Inset_Reveal,Left_Overlay])
            pull.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness])
            pull.z_loc('IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)',[Inset_Front,Inset_Reveal,Bottom_Overlay])
            pull.x_rot(value = 90)
            pull.y_rot(value = 0)
            pull.z_rot(value = 0)
            pull.x_dim('Width-Frame_Left_Gap-Frame_Right_Gap+IF(Inset_Front,-(Inset_Reveal)*2,Right_Overlay+Left_Overlay)',[Width,Inset_Front,Inset_Reveal,Frame_Left_Gap,Frame_Right_Gap,Right_Overlay,Left_Overlay,Inset_Reveal,Inset_Front])
            pull.y_dim('Height-(Frame_Top_Gap+Frame_Bottom_Gap)+IF(Inset_Front,-(Inset_Reveal)*2,Top_Overlay+Bottom_Overlay)',[Height,Inset_Front,Inset_Reveal,Top_Overlay,Bottom_Overlay,Frame_Top_Gap,Frame_Bottom_Gap])
            pull.z_dim('Front_Thickness',[Front_Thickness])
            pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
            pull.prompt("Pull Z Location",'((Width+Left_Drawer_Front_Extension+Right_Drawer_Front_Extension)/2)',[Width,Left_Drawer_Front_Extension,Right_Drawer_Front_Extension])
            pull.prompt("Hide",'IF(No_Pulls,True,False)',[No_Pulls])
            
        self.update()
        
class FF_Horizontal_Drawers(fd_types.Assembly):
    
    library_name = "Face Frame Cabinet Inserts"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".drawer_prompts"
    type_assembly = 'INSERT'
    placement_type = "EXTERIOR"
    
    door_type = "Drawer"
    direction = 'Vertical'
    add_drawer = True
    add_pull = True
    use_buyout_box = True

    def add_drawer_prompts(self):

        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        add_common_drawer_prompts(self)
        
        add_face_frame_overlay_prompts(self)
        
        self.add_prompt(name="Drawer Slide Quantity",prompt_type='QUANTITY',value=2,tab_index=1)
        
    def draw(self):

        self.create_assembly()
        self.add_drawer_prompts()
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Mid_Rail_Width = self.get_var('Mid Rail Width')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        Frame_Thickness = self.get_var('Frame Thickness')
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Front_Thickness = self.get_var("Front Thickness")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        No_Pulls = self.get_var("No Pulls")
        Frame_Left_Gap = self.get_var("Frame Left Gap")
        Frame_Right_Gap = self.get_var("Frame Right Gap")
        Inset_Front = self.get_var("Inset Front")
        Inset_Reveal = self.get_var("Inset Reveal")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Horizontal_Grain = self.get_var("Horizontal Grain")
        Open = self.get_var("Open")
        
        mid_stile = self.add_assembly(HARDWOOD)
        mid_stile.set_name("Mid Rail")
        mid_stile.x_loc('Frame_Left_Gap+(Width-Mid_Rail_Width-Frame_Left_Gap-Frame_Right_Gap)/2',[Width,Mid_Rail_Width,Frame_Left_Gap,Frame_Right_Gap])
        mid_stile.y_loc('-Frame_Thickness',[Frame_Thickness])
        mid_stile.z_loc(value = 0)
        mid_stile.x_rot(value = 0)
        mid_stile.y_rot(value = -90)
        mid_stile.z_rot(value = 90)
        mid_stile.x_dim('Height-Frame_Top_Gap-Frame_Bottom_Gap',[Height,Frame_Top_Gap,Frame_Bottom_Gap])
        mid_stile.y_dim('-Mid_Rail_Width',[Mid_Rail_Width])
        mid_stile.z_dim('-Frame_Thickness',[Frame_Thickness])
        mid_stile.material('Exposed_Exterior_Surface')
        mid_stile.solid_stock("Hardwood")
        
        Mid_Stile_X = mid_stile.get_var('loc_x','Mid_Stile_X')
        Mid_Stile_Width = mid_stile.get_var('dim_y','Mid_Stile_Width')
        
        if self.add_drawer:
            if self.use_buyout_box:
                left_drawer = self.add_assembly(BUYOUT_DRAWER_BOX)
                left_drawer.material('Drawer_Box_Surface')
            else:
                left_drawer = drawer_boxes.Wood_Drawer_Box()
                left_drawer.draw()
                left_drawer.obj_bp.parent = self.obj_bp
            left_drawer.set_name("Left Drawer Box")
            left_drawer.x_loc('Frame_Left_Gap+Drawer_Box_Slide_Gap',[Frame_Left_Gap,Drawer_Box_Slide_Gap])
            left_drawer.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Front_Thickness,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness]) 
            left_drawer.z_loc('Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap])
            left_drawer.x_rot(value = 0)
            left_drawer.y_rot(value = 0)
            left_drawer.z_rot(value = 0)
            left_drawer.x_dim('Mid_Stile_X-Frame_Left_Gap-(Drawer_Box_Slide_Gap)*2',[Mid_Stile_X,Frame_Left_Gap,Drawer_Box_Slide_Gap])
            left_drawer.y_dim('IF(Inset_Front,Depth-Drawer_Box_Rear_Gap,Depth+Frame_Thickness+Door_to_Cabinet_Gap-Drawer_Box_Rear_Gap)',[Inset_Front,Frame_Thickness,Door_to_Cabinet_Gap,Depth,Drawer_Box_Rear_Gap])
            left_drawer.z_dim('Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap-Frame_Top_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap,Frame_Top_Gap])
            
            if self.use_buyout_box:
                right_drawer = self.add_assembly(BUYOUT_DRAWER_BOX)
                right_drawer.material('Drawer_Box_Surface')
            else:
                right_drawer = drawer_boxes.Wood_Drawer_Box()
                right_drawer.draw()
                right_drawer.obj_bp.parent = self.obj_bp
            right_drawer.set_name("Right Drawer Box")
            right_drawer.x_loc('Mid_Stile_X+fabs(Mid_Stile_Width)+Drawer_Box_Slide_Gap',[Mid_Stile_X,Mid_Stile_Width,Drawer_Box_Slide_Gap])
            right_drawer.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Front_Thickness,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness])
            right_drawer.z_loc('Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap])
            right_drawer.x_rot(value = 0)
            right_drawer.y_rot(value = 0)
            right_drawer.z_rot(value = 0)
            right_drawer.x_dim('Mid_Stile_X-Frame_Left_Gap-(Drawer_Box_Slide_Gap)*2',[Mid_Stile_X,Frame_Left_Gap,Drawer_Box_Slide_Gap])
            right_drawer.y_dim('IF(Inset_Front,Depth-Drawer_Box_Rear_Gap,Depth+Frame_Thickness+Door_to_Cabinet_Gap-Drawer_Box_Rear_Gap)',[Inset_Front,Frame_Thickness,Door_to_Cabinet_Gap,Depth,Drawer_Box_Rear_Gap])
            right_drawer.z_dim('Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap-Frame_Top_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap,Frame_Top_Gap])
        
        front_width = "Mid_Stile_X-Frame_Left_Gap+IF(Inset_Front,-(Inset_Reveal)*2,Right_Overlay+Left_Overlay)"
        front_height = "Height-(Frame_Top_Gap+Frame_Bottom_Gap)+IF(Inset_Front,-(Inset_Reveal)*2,Top_Overlay+Bottom_Overlay)"
        size_vars = [Horizontal_Grain,Frame_Top_Gap,Frame_Bottom_Gap,Mid_Stile_X,Height,Inset_Front,Inset_Reveal,Top_Overlay,Bottom_Overlay,Frame_Left_Gap,Right_Overlay,Left_Overlay]
        
        left_front = self.add_assembly(DRAWER_FRONT)
        left_front.set_name("Left Drawer Front")
        left_front.x_loc('Frame_Left_Gap+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Frame_Left_Gap,Inset_Front,Inset_Reveal,Left_Overlay])
        left_front.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness])
        left_front.z_loc('IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)',[Inset_Front,Inset_Reveal,Bottom_Overlay])
        left_front.x_rot('IF(Horizontal_Grain,radians(90),0)',[Horizontal_Grain])
        left_front.y_rot('IF(Horizontal_Grain,0,radians(-90))',[Horizontal_Grain])
        left_front.z_rot('IF(Horizontal_Grain,0,radians(90))',[Horizontal_Grain])
        left_front.x_dim('IF(Horizontal_Grain,' + front_width + ',' + front_height + ')',size_vars)
        left_front.y_dim('IF(Horizontal_Grain,' + front_height + ',(' + front_width + ')*-1)',size_vars)
        left_front.z_dim('Front_Thickness',[Front_Thickness])
        left_front.cutpart("Cabinet_Drawer_Front")
        left_front.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        left_front.obj_bp.mv.is_cabinet_drawer_front = True
        
        right_front = self.add_assembly(DRAWER_FRONT)
        right_front.set_name("Left Drawer Front")
        right_front.x_loc('Mid_Stile_X+fabs(Mid_Stile_Width)+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Mid_Stile_X,Inset_Front,Inset_Reveal,Mid_Stile_Width,Left_Overlay])
        right_front.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness])
        right_front.z_loc('IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)',[Inset_Front,Inset_Reveal,Bottom_Overlay])
        right_front.x_rot('IF(Horizontal_Grain,radians(90),0)',[Horizontal_Grain])
        right_front.y_rot('IF(Horizontal_Grain,0,radians(-90))',[Horizontal_Grain])
        right_front.z_rot('IF(Horizontal_Grain,0,radians(90))',[Horizontal_Grain])
        right_front.x_dim('IF(Horizontal_Grain,' + front_width + ',' + front_height + ')',size_vars)
        right_front.y_dim('IF(Horizontal_Grain,' + front_height + ',(' + front_width + ')*-1)',size_vars)
        right_front.z_dim('Front_Thickness',[Front_Thickness])
        right_front.cutpart("Cabinet_Drawer_Front")
        right_front.edgebanding('Door_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
        right_front.obj_bp.mv.is_cabinet_drawer_front = True

        if self.add_pull:
            left_pull = cabinet_pulls.Standard_Pull()
            left_pull.door_type = self.door_type
            left_pull.draw()
            left_pull.obj_bp.parent = self.obj_bp
            left_pull.set_name(left_pull.pull_name)
            left_pull.x_loc('Frame_Left_Gap+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Frame_Left_Gap,Inset_Front,Inset_Reveal,Left_Overlay])
            left_pull.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness])
            left_pull.z_loc('IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)',[Inset_Front,Inset_Reveal,Bottom_Overlay])
            left_pull.x_rot(value = 90)
            left_pull.y_rot(value = 0)
            left_pull.z_rot(value = 0)
            left_pull.x_dim('Mid_Stile_X-Frame_Left_Gap+IF(Inset_Front,-(Inset_Reveal)*2,Right_Overlay+Left_Overlay)',
                            [Mid_Stile_X,Inset_Front,Inset_Reveal,Frame_Left_Gap,Right_Overlay,Left_Overlay,Inset_Reveal,Inset_Front])
            left_pull.y_dim('Height-(Frame_Top_Gap+Frame_Bottom_Gap)+IF(Inset_Front,-(Inset_Reveal)*2,Top_Overlay+Bottom_Overlay)',
                            [Height,Inset_Front,Inset_Reveal,Top_Overlay,Bottom_Overlay,Frame_Top_Gap,Frame_Bottom_Gap])
            left_pull.z_dim('Front_Thickness',[Front_Thickness])
            left_pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
            left_pull.prompt("Pull Z Location",'(Mid_Stile_X-Frame_Left_Gap+IF(Inset_Front,-(Inset_Reveal)*2,Right_Overlay+Left_Overlay))/2',
                             [Mid_Stile_X,Inset_Front,Inset_Reveal,Frame_Left_Gap,Right_Overlay,Left_Overlay,Inset_Reveal,Inset_Front])
            left_pull.prompt("Hide",'IF(No_Pulls,True,False)',[No_Pulls])
    
            right_pull = cabinet_pulls.Standard_Pull()
            right_pull.door_type = self.door_type
            right_pull.draw()
            right_pull.obj_bp.parent = self.obj_bp
            right_pull.set_name(right_pull.pull_name)
            right_pull.x_loc('Mid_Stile_X+fabs(Mid_Stile_Width)+IF(Inset_Front,Inset_Reveal,-Left_Overlay)',[Mid_Stile_X,Inset_Front,Inset_Reveal,Mid_Stile_Width,Left_Overlay])
            right_pull.y_loc('IF(Inset_Front,0,-Door_to_Cabinet_Gap-Frame_Thickness)-(Depth*Open)',[Inset_Front,Door_to_Cabinet_Gap,Depth,Open,Frame_Thickness])
            right_pull.z_loc('IF(Inset_Front,Inset_Reveal,-Bottom_Overlay)',[Inset_Front,Inset_Reveal,Bottom_Overlay])
            right_pull.x_rot(value = 90)
            right_pull.y_rot(value = 0)
            right_pull.z_rot(value = 0)
            right_pull.x_dim('Mid_Stile_X-Frame_Left_Gap+IF(Inset_Front,-(Inset_Reveal)*2,Right_Overlay+Left_Overlay)',
                             [Mid_Stile_X,Inset_Front,Inset_Reveal,Frame_Left_Gap,Right_Overlay,Left_Overlay,Inset_Reveal,Inset_Front])
            right_pull.y_dim('Height-(Frame_Top_Gap+Frame_Bottom_Gap)+IF(Inset_Front,-(Inset_Reveal)*2,Top_Overlay+Bottom_Overlay)',
                             [Height,Inset_Front,Inset_Reveal,Top_Overlay,Bottom_Overlay,Frame_Top_Gap,Frame_Bottom_Gap])
            right_pull.z_dim('Front_Thickness',[Front_Thickness])
            right_pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
            right_pull.prompt("Pull Z Location",'(Mid_Stile_X-Frame_Left_Gap+IF(Inset_Front,-(Inset_Reveal)*2,Right_Overlay+Left_Overlay))/2',
                              [Mid_Stile_X,Inset_Front,Inset_Reveal,Frame_Left_Gap,Right_Overlay,Left_Overlay,Inset_Reveal,Inset_Front])
            right_pull.prompt("Hide",'IF(No_Pulls,True,False)',[No_Pulls])
        
        self.update()
        
#---------INSERTS

class INSERT_Base_Single_Door_FF(FF_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Single Door FF"
        self.door_type = "Base"
        self.door_swing = "Left Swing"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Base_Double_Door_FF(FF_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Double Door FF"
        self.door_type = "Base"
        self.door_swing = "Double Door"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Tall_Single_Door_FF(FF_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Tall Single Door FF"
        self.door_type = "Tall"
        self.door_swing = "Left Swing"
        self.width = unit.inch(18)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)
        
class INSERT_Tall_Double_Door_FF(FF_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Tall Double Door FF"
        self.door_type = "Tall"
        self.door_swing = "Double Door"
        self.width = unit.inch(36)
        self.height = unit.inch(84)
        self.depth = unit.inch(23)
        
class INSERT_Upper_Single_Door_FF(FF_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Upper Single Door FF"
        self.door_type = "Upper"
        self.door_swing = "Left Swing"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_Upper_Double_Door_FF(FF_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Upper Double Door FF"
        self.door_type = "Upper"
        self.door_swing = "Double Door"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)

class INSERT_1_Drawer_FF(FF_Drawer):
    
    def __init__(self):
        self.category_name = "Drawers"
        self.assembly_name = "1 Drawer FF"
        self.door_type = "Drawer"
        self.width = unit.inch(18)
        self.height = unit.inch(6)
        self.depth = unit.inch(19)
        self.mirror_y = False
        
class INSERT_Horizontal_Drawers_FF(FF_Horizontal_Drawers):
    
    def __init__(self):
        self.category_name = "Drawers"
        self.assembly_name = "Horizontal Drawers FF"
        self.width = unit.inch(36)
        self.height = unit.inch(6)
        self.depth = unit.inch(20)
        self.mirror_y = False
        
class INSERT_Base_Pie_Cut_Door_FF(FF_Pie_Cut_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Base Pie Cut Door FF"
        self.door_type = "Base"
        self.door_swing = "Left Swing"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(36)
        
class INSERT_Upper_Pie_Cut_Door_FF(FF_Pie_Cut_Doors):
    
    def __init__(self):
        self.category_name = "Doors"
        self.assembly_name = "Upper Pie Cut Door FF"
        self.door_type = "Upper"
        self.door_swing = "Left Swing"
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(36)
