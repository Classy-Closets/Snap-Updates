"""
Microvellum 
Entry Doors
Stores the logic and product defs for entry doors.
"""

import bpy
import math
import os
import fd_library
from mv import fd_types, unit, utils


LIBRARY_NAMESPACE = "lm_entry_doors"
DOOR_FRAME_PATH = os.path.join(os.path.dirname(__file__),"Door Frames")
DOOR_PANEL = os.path.join(os.path.dirname(__file__),"Door Panels")
DOOR_HANDLE = os.path.join(os.path.dirname(__file__),"Door Handles","Door_Handle.blend")
HINGE = os.path.join(os.path.dirname(__file__),"Door Hardware","Hinge.blend")
LATCH = os.path.join(os.path.dirname(__file__),"Door Hardware","Latch.blend")
MATERIAL_FILE = os.path.join(os.path.dirname(__file__),"materials","materials.blend")

SINGLE_PANEL_WIDTH = unit.inch(42)
DOUBLE_PANEL_WIDTH = unit.inch(84)
DOOR_HEIGHT = unit.inch(83)
DOOR_DEPTH = unit.inch(6)
HANDLE_HEIGHT = unit.inch(37)

class Entry_Door(fd_types.Assembly):
    library_name = "Entry Doors"
    category_name = ""
    assembly_name = ""
    property_id = LIBRARY_NAMESPACE + ".entry_door_prompts"
    plan_draw_id = LIBRARY_NAMESPACE + ".draw_plan"
    type_assembly = "PRODUCT"
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0
    
    door_frame = ""
    door_panel = ""
    double_door = False
    
    def add_hardware(self, panel_assembly, no_latch=False):
        Width = panel_assembly.get_var("dim_x", "Width")
        Height = panel_assembly.get_var("dim_z", "Height")
        Depth = panel_assembly.get_var("dim_y", "Depth")
        Hinge_Offset = self.get_var("Hinge Placement", 'Hinge_Offset')
        
        hinge_bottom = self.add_object(HINGE)
        hinge_bottom.obj.parent = panel_assembly.obj_bp
        hinge_bottom.set_name("Bottom Hinge")
        hinge_bottom.z_loc("Hinge_Offset", [Hinge_Offset])
        hinge_bottom.y_rot(value=-90)
        hinge_bottom.assign_material("Hinge Color", MATERIAL_FILE, "Chrome")
        
        hinge_top = self.add_object(HINGE)
        hinge_top.obj.parent = panel_assembly.obj_bp
        hinge_top.set_name("Top Hinge")
        hinge_top.z_loc("Height-Hinge_Offset", [Hinge_Offset, Height])
        hinge_top.y_rot(value=-90)
        hinge_top.assign_material("Hinge Color", MATERIAL_FILE, "Chrome")
        
        if not no_latch:
            latch = self.add_object(LATCH)
            latch.obj.parent = panel_assembly.obj_bp
            latch.set_name("Latch")
            latch.x_loc("Width", [Width])
            latch.y_loc("Depth*0.5", [Depth])
            latch.z_loc(value=HANDLE_HEIGHT)
            latch.y_rot(value=90)
            latch.assign_material("Latch Color", MATERIAL_FILE, "Chrome")
    
    def draw(self):
        self.create_assembly()
        self.obj_bp["ISENTRYDOOR"] = True
        self.obj_bp.mv.dont_export = True
        
        if self.door_panel != "":
            self.add_tab(name='Main Options', tab_type='VISIBLE')
            self.add_tab(name='Formulas', tab_type='HIDDEN')
            self.add_prompt(name="Reverse Swing", prompt_type='CHECKBOX', value=False, tab_index=0)
            self.add_prompt(name="Door Rotation", prompt_type='ANGLE', value=0.0, tab_index=0)
            self.add_prompt(name="Hinge Placement", prompt_type='DISTANCE', value=unit.inch(18.0), tab_index=1)
            
            if self.double_door != True:
                self.add_prompt(name="Door Swing", prompt_type='COMBOBOX', items=["Left Swing", "Right Swing"], value=0, tab_index=0)
        
        Width = self.get_var('dim_x', 'Width')
        Height = self.get_var('dim_z', 'Height')
        Depth = self.get_var('dim_y', 'Depth')
        Door_Rotation = self.get_var('Door Rotation')
        Reverse_Swing = self.get_var("Reverse Swing")
        
        if self.double_door != True:
            Swing = self.get_var('Door Swing')

        door_frame = self.add_assembly(os.path.join(DOOR_FRAME_PATH,self.door_frame))
        door_frame.set_name("Door Frame")
        door_frame.x_dim('Width', [Width])
        door_frame.y_dim('Depth', [Depth])
        door_frame.z_dim('Height', [Height])
        door_frame.assign_material("Frame", MATERIAL_FILE, "White")   
        door_frame.draw_as_hidden_line()
        
        if self.door_panel != "":
            door_panel = self.add_assembly(os.path.join(DOOR_PANEL,self.door_panel))
            door_panel.set_name("Door Panel")
            
            if self.double_door != True:
                door_panel.x_loc('IF(Door_Swing==1,Width-INCH(3),INCH(3))',[Width, Swing])
                door_panel.y_loc('IF(Reverse_Swing,IF(Door_Swing==0,INCH(1.75),0),IF(Door_Swing==0,Depth,Depth-INCH(1.75)))',[Swing, Reverse_Swing, Depth])
                door_panel.z_rot('IF(Door_Swing==1,radians(180)+IF(Reverse_Swing,Door_Rotation,-Door_Rotation),IF(Reverse_Swing,-Door_Rotation,Door_Rotation))',
                                 [Door_Rotation, Swing, Reverse_Swing])
                
            else:
                door_panel.x_loc(value = unit.inch(3))
                door_panel.y_loc('Depth-IF(Reverse_Swing,INCH(4.25),INCH(0))',[Reverse_Swing, Depth])
                door_panel.z_rot('IF(Reverse_Swing,-Door_Rotation,Door_Rotation)',[Door_Rotation, Reverse_Swing])                

            door_panel.x_dim('Width-INCH(6)',[Width])
            door_panel.z_dim('Height-INCH(3.25)',[Height])
            door_panel.assign_material("Door", MATERIAL_FILE, "White")
            door_panel.assign_material("Glass", MATERIAL_FILE, "Glass")
            self.add_hardware(door_panel)
            
            door_handle = self.add_object(DOOR_HANDLE)
            door_handle.obj.parent = door_panel.obj_bp
            door_handle.set_name("Door Handle")
            door_handle.x_loc('Width-INCH(9)',[Width])
            door_handle.y_loc(value = unit.inch(-0.875))
            door_handle.z_loc(value = HANDLE_HEIGHT)
            door_handle.assign_material("Handle Color", MATERIAL_FILE, "Chrome")

        if self.double_door == True:
            door_panel.x_dim('(Width-INCH(6))*0.5',[Width])
            door_handle.x_loc('(Width*0.5)-INCH(6)',[Width])
        
            door_panel_right = self.add_assembly(os.path.join(DOOR_PANEL,self.door_panel))
            door_panel_right.set_name("Door Panel Right")
            door_panel_right.x_loc('Width-INCH(3)',[Width])
            door_panel_right.y_loc('Depth-INCH(1.75)-IF(Reverse_Swing,INCH(4.25),INCH(0))',[Reverse_Swing, Depth])
            door_panel_right.z_rot('radians(180)+IF(Reverse_Swing,Door_Rotation,-Door_Rotation)',[Door_Rotation, Reverse_Swing])
            door_panel_right.x_dim('(Width-INCH(6))*0.5',[Width])
            door_panel_right.z_dim('Height-INCH(3.25)',[Height])     
            door_panel_right.assign_material("Door", MATERIAL_FILE, "White")   
            door_panel_right.assign_material("Glass", MATERIAL_FILE, "Glass")
            self.add_hardware(door_panel_right, no_latch=True)  
                
            Dpr_Width = door_panel_right.get_var('dim_x','Dpr_Width')
            
            door_handle_right = self.add_object(DOOR_HANDLE)
            door_handle_right.set_name("Door Handle Right")
            door_handle_right.obj.parent = door_panel_right.obj_bp
            door_handle_right.x_loc('Dpr_Width-INCH(3)', [Dpr_Width])
            door_handle_right.y_loc(value = unit.inch(-0.875))
            door_handle_right.z_loc(value = HANDLE_HEIGHT)
            door_handle_right.assign_material("Handle Color", MATERIAL_FILE, "Chrome")
                
        self.update()
     
  
class Sliding_Doors(fd_types.Assembly):
    library_name = "Entry Doors"
    category_name = ""
    assembly_name = ""
    property_id = LIBRARY_NAMESPACE + ".entry_door_prompts"
    plan_draw_id = LIBRARY_NAMESPACE + ".draw_plan"
    type_assembly = "PRODUCT"
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0
    
    door_frame = ""
    door_panel = ""
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.dont_export = True
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas', tab_type='HIDDEN')
        
        self.add_prompt(name="Open Left Door", prompt_type='PERCENTAGE', value=0, tab_index=0)
        self.add_prompt(name="Open Right Door", prompt_type='PERCENTAGE', value=0, tab_index=0)
        self.add_prompt(name="Frame Width",prompt_type='DISTANCE',value=unit.inch(3.0), tab_index=1)
        self.add_prompt(name="Panel Depth",prompt_type='DISTANCE',value=unit.inch(1.75), tab_index=1)
        self.add_prompt(name="Door to Door Gap",prompt_type='DISTANCE',value=unit.inch(0.125), tab_index=1)
        self.add_prompt(name="Door Panel Overlap",prompt_type='DISTANCE',value=unit.inch(1.5), tab_index=1)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Frame_Width = self.get_var('Frame Width', 'Frame_Width')
        Panel_Depth = self.get_var('Panel Depth', 'Panel_Depth')
        Dtd_Gap = self.get_var('Door to Door Gap', 'Dtd_Gap')
        Panel_Overlap = self.get_var('Door Panel Overlap', 'Panel_Overlap')
        Open_L_Door = self.get_var('Open Left Door', 'Open_L_Door')
        Open_R_Door = self.get_var('Open Right Door', 'Open_R_Door')

        door_frame = self.add_assembly(os.path.join(DOOR_FRAME_PATH,self.door_frame))
        door_frame.set_name("Door Frame")
        door_frame.x_dim('Width',[Width])
        door_frame.y_dim('Depth',[Depth])
        door_frame.z_dim('Height',[Height])
        door_frame.assign_material("Frame", MATERIAL_FILE, "White")   
        
        door_panel = self.add_assembly(os.path.join(DOOR_PANEL,self.door_panel))
        door_panel.set_name("Door Panel")
        door_panel.x_loc('Frame_Width+Open_L_Door*((Width-Frame_Width*2)*0.5-Panel_Overlap*0.5)', [Width, Frame_Width, Panel_Overlap, Open_L_Door])
        door_panel.y_loc('(Depth*0.5)-(Dtd_Gap*0.5)', [Depth, Dtd_Gap])
        door_panel.x_dim('(Width-Frame_Width*2)/2+Panel_Overlap*0.5',[Width, Frame_Width, Panel_Overlap])
        door_panel.z_dim('Height-INCH(3.25)',[Height])
        door_panel.prompt('No Hardware', value=True)
        door_panel.assign_material("Door", MATERIAL_FILE, "White")
        door_panel.assign_material("Glass", MATERIAL_FILE, "Glass")
        
        door_panel_right = self.add_assembly(os.path.join(DOOR_PANEL,self.door_panel))
        door_panel_right.set_name("Door Panel Right")
        door_panel_right.x_loc('(Frame_Width+(Width-Frame_Width*2)/2-Panel_Overlap*0.5)-Open_R_Door*((Width-Frame_Width*2)*0.5-Panel_Overlap*0.5)',
                               [Width, Frame_Width, Open_R_Door, Panel_Overlap])
        door_panel_right.y_loc('(Depth*0.5)+Panel_Depth+(Dtd_Gap*0.5)', [Depth, Dtd_Gap, Panel_Depth])
        door_panel_right.x_dim('(Width-Frame_Width*2)/2+Panel_Overlap*0.5',[Width, Frame_Width, Panel_Overlap])
        door_panel_right.z_dim('Height-INCH(3.25)',[Height])
        door_panel_right.prompt('No Hardware', value=True)
        door_panel_right.assign_material("Door",MATERIAL_FILE,"White")   
        door_panel_right.assign_material("Glass",MATERIAL_FILE,"Glass")  
                
        self.update()

        
class Pocket_Doors(fd_types.Assembly):
    library_name = "Entry Doors"
    category_name = ""
    assembly_name = ""
    property_id = LIBRARY_NAMESPACE + ".entry_door_prompts"
    plan_draw_id = LIBRARY_NAMESPACE + ".draw_plan"
    type_assembly = "PRODUCT"
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0
    
    door_frame = ""
    door_panel = ""
    
    double_door = False
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.dont_export = True
            
        self.add_tab(name='Main Options', tab_type='VISIBLE')
        self.add_tab(name='Formulas', tab_type='HIDDEN')
        
        self.add_prompt(name="Open Door", prompt_type='PERCENTAGE', value=0, tab_index=0)
        self.add_prompt(name="Frame Width", prompt_type='DISTANCE', value=unit.inch(3.25), tab_index=1)
        self.add_prompt(name="Panel Depth",prompt_type='DISTANCE',value=unit.inch(1.75), tab_index=1)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Open_Door = self.get_var('Open Door')
        Frame_Width = self.get_var('Frame Width')
        Panel_Depth = self.get_var('Panel Depth')

        door_frame = self.add_assembly(os.path.join(DOOR_FRAME_PATH,self.door_frame))
        door_frame.set_name("Door Frame")
        door_frame.x_dim('Width', [Width])
        door_frame.y_dim('Depth', [Depth])
        door_frame.z_dim('Height', [Height])
        door_frame.assign_material("Frame", MATERIAL_FILE, "White")   
        
        door_panel = self.add_assembly(os.path.join(DOOR_PANEL,self.door_panel))
        door_panel.set_name("Door Panel")
        door_panel.y_loc('Depth*0.5+Panel_Depth*0.5', [Depth, Panel_Depth])
        door_panel.z_dim('Height-INCH(3.25)', [Height])
        door_panel.prompt('No Hardware', value=True)
        
        if not self.double_door:
            door_panel.x_loc('Frame_Width-Open_Door*(Width-Frame_Width*2)', [Width, Frame_Width, Open_Door])
            door_panel.x_dim('(Width-Frame_Width*2)', [Width, Frame_Width])
        else:
            door_panel.x_loc('Frame_Width-Open_Door*((Width-Frame_Width*2)*0.5)', [Width, Frame_Width, Open_Door])
            door_panel.x_dim('(Width-Frame_Width*2)*0.5', [Width, Frame_Width])
        
        door_panel.assign_material("Door", MATERIAL_FILE, "White")
        door_panel.assign_material("Glass", MATERIAL_FILE, "Glass")
        
        if self.double_door:
            door_panel_right = self.add_assembly(os.path.join(DOOR_PANEL,self.door_panel))
            door_panel_right.set_name("Door Panel Right")
            door_panel_right.x_loc('Width*0.5+(Open_Door*(Width*0.5-Frame_Width))',
                                   [Width, Frame_Width, Open_Door])
            door_panel_right.y_loc('Depth*0.5+Panel_Depth*0.5', [Depth, Panel_Depth])
            door_panel_right.x_dim('(Width-Frame_Width*2)*0.5',[Width, Frame_Width])
            door_panel_right.z_dim('Height-INCH(3.25)', [Height])
            door_panel_right.prompt('No Hardware', value=True)
            door_panel_right.assign_material("Door", MATERIAL_FILE, "White")   
            door_panel_right.assign_material("Glass", MATERIAL_FILE, "Glass")
                
        self.update()

        
class Bi_Fold_Doors(fd_types.Assembly):
    library_name = "Entry Doors"
    category_name = ""
    assembly_name = ""
    property_id = LIBRARY_NAMESPACE + ".entry_door_prompts"
    plan_draw_id = LIBRARY_NAMESPACE + ".draw_plan"
    type_assembly = "PRODUCT"
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0
    
    door_frame = ""
    door_panel = ""
    
    double_door = False
    
    def add_single_door_hardware(self, panel_assembly, placement='left'):
        assert placement in ('left', 'right'), "Invalid arg - '{}'".format(placement)
        
        Width = panel_assembly.get_var("dim_x", "Width")
        Height = panel_assembly.get_var("dim_z", "Height")
        Hinge_Offset = self.get_var("Hinge Placement", 'Hinge_Offset')
        RS = self.get_var('Reverse Swing', 'RS')
        DS = self.get_var('Door Swing', 'DS')
        
        hinge_bottom = self.add_object(HINGE)
        hinge_bottom.obj.parent = panel_assembly.obj_bp
        hinge_bottom.set_name("Bottom Hinge")
        hinge_bottom.z_loc("Hinge_Offset", [Hinge_Offset])
        hinge_bottom.y_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(-90),radians(90))', [RS, DS])
        hinge_bottom.z_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])
        hinge_bottom.assign_material("Hinge Color", MATERIAL_FILE, "Chrome")
        
        hinge_top = self.add_object(HINGE)
        hinge_top.obj.parent = panel_assembly.obj_bp
        hinge_top.set_name("Top Hinge")
        hinge_top.z_loc("Height-Hinge_Offset", [Hinge_Offset, Height])
        hinge_top.y_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(-90),radians(90))', [RS, DS])
        hinge_top.z_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])
        hinge_top.assign_material("Hinge Color", MATERIAL_FILE, "Chrome")
        
        if placement == 'right':
            hinge_bottom.x_loc("Width", [Width])
            hinge_bottom.y_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(90),radians(-90))', [RS, DS])
            hinge_bottom.z_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])
            hinge_top.x_loc("Width", [Width])
            hinge_top.y_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(90),radians(-90))', [RS, DS])
            hinge_top.z_rot('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])
    
    def add_double_door_hardware(self, panel_assembly, placement='left'):
        assert placement in ('left', 'right'), "Invalid arg - '{}'".format(placement)
        
        Width = panel_assembly.get_var("dim_x", "Width")
        Height = panel_assembly.get_var("dim_z", "Height")
        Hinge_Offset = self.get_var("Hinge Placement", 'Hinge_Offset')
        
        hinge_bottom = self.add_object(HINGE)
        hinge_bottom.obj.parent = panel_assembly.obj_bp
        hinge_bottom.set_name("Bottom Hinge")
        hinge_bottom.z_loc("Hinge_Offset", [Hinge_Offset])
        hinge_bottom.y_rot(value=-90)
        hinge_bottom.assign_material("Hinge Color", MATERIAL_FILE, "Chrome")
        
        hinge_top = self.add_object(HINGE)
        hinge_top.obj.parent = panel_assembly.obj_bp
        hinge_top.set_name("Top Hinge")
        hinge_top.z_loc("Height-Hinge_Offset", [Hinge_Offset, Height])
        hinge_top.y_rot(value=-90)
        hinge_top.assign_material("Hinge Color", MATERIAL_FILE, "Chrome")
        
        if placement == 'right':
            hinge_bottom.x_loc("Width", [Width])
            hinge_bottom.y_rot(value=90)
            hinge_top.x_loc("Width", [Width])
            hinge_top.y_rot(value=90)            
    
    def set_materials(self, assembly):
        assembly.assign_material("Door", MATERIAL_FILE, "White")
        assembly.assign_material("Glass", MATERIAL_FILE, "Glass")
        
    def set_mirror_modifier(self, assembly, mod_name, mirror_obj):
        for child in assembly.obj_bp.children:
            if child.type == 'MESH':
                child.modifiers.new(mod_name, 'MIRROR')
                child.modifiers[mod_name].mirror_object = mirror_obj       
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.dont_export = True
            
        self.add_tab(name='Main Options', tab_type='VISIBLE')
        self.add_tab(name='Formulas', tab_type='HIDDEN')
        
        self.add_prompt(name="Open Door", prompt_type='PERCENTAGE', value=0, tab_index=0)
        self.add_prompt(name="Reverse Swing", prompt_type='CHECKBOX', tab_index=0)
        self.add_prompt(name="Frame Width", prompt_type='DISTANCE', value=unit.inch(3.25), tab_index=1)
        self.add_prompt(name="Panel Depth", prompt_type='DISTANCE', value=unit.inch(1.75), tab_index=1)
        self.add_prompt(name="Door Gap", prompt_type='DISTANCE', value=unit.inch(0.125), tab_index=1)
        self.add_prompt(name="Hinge Placement", prompt_type='DISTANCE', value=unit.inch(18.0), tab_index=1)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Open = self.get_var('Open Door', 'Open')
        Frame_Width = self.get_var('Frame Width')
        Panel_Depth = self.get_var('Panel Depth')
        Door_Gap = self.get_var('Door Gap')
        RS = self.get_var('Reverse Swing', 'RS')
        
        door_frame = self.add_assembly(os.path.join(DOOR_FRAME_PATH,self.door_frame))
        door_frame.set_name("Door Frame")
        door_frame.x_dim('Width', [Width])
        door_frame.y_dim('Depth', [Depth])
        door_frame.z_dim('Height', [Height])
        door_frame.assign_material("Frame", MATERIAL_FILE, "White")        
        
        if not self.double_door:
            self.add_prompt(name="Door Swing", prompt_type='COMBOBOX', items=["Left Swing", "Right Swing"], value=0, tab_index=0)
            DS = self.get_var('Door Swing', 'DS')
            
            door_panel_left_1 = self.add_assembly(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_1.set_name("Door Panel Left 1")
            door_panel_left_1.x_loc('IF(DS==0,Frame_Width+Panel_Depth*Open,Width-Frame_Width-Panel_Depth*Open)', [Frame_Width, Open, Panel_Depth, DS, Width])
            door_panel_left_1.y_loc('Depth*0.5+IF(RS,-Panel_Depth,Panel_Depth)*0.5', [Depth, Panel_Depth, RS])
            door_panel_left_1.x_dim('(Width-Frame_Width*2-Door_Gap*2)*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_1.y_dim('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),-Panel_Depth, Panel_Depth)', [RS, Panel_Depth, DS])
            door_panel_left_1.z_dim('Height-INCH(3.25)', [Height])
            door_panel_left_1.z_rot('IF(DS==0,0,radians(180))+radians(-90)*IF(OR(AND(RS,DS==0),AND(RS==False,DS==1)),-Open,Open)', [Open, RS, DS])
            door_panel_left_1.prompt('Hardware Config', value='Right')
            self.set_materials(door_panel_left_1)
            self.add_single_door_hardware(door_panel_left_1, placement='right')
            
            door_panel_left_2 = self.add_assembly(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_2.set_name("Door Panel Left 2")
            door_panel_left_2.obj_bp.parent = door_panel_left_1.obj_bp
            door_panel_left_2.x_loc('(Width-Frame_Width*2)*0.5+Door_Gap*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.x_dim('(Width-Frame_Width*2-Door_Gap*2)*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.y_dim('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),-Panel_Depth, Panel_Depth)', [RS, Panel_Depth, DS])
            door_panel_left_2.z_dim('Height-INCH(3.25)', [Height])
            door_panel_left_2.z_rot('radians(180)-(radians(180)-(radians(90)*IF(OR(AND(RS,DS==0),AND(RS==False,DS==1)),-Open,Open))*2)', [Open, RS, DS])
            door_panel_left_2.prompt('Hardware Config', value='Left')
            self.set_materials(door_panel_left_2)
            self.add_single_door_hardware(door_panel_left_2)
            
        else:
            mirror_obj = self.add_empty()
            mirror_obj.set_name("Mirror Object")
            mirror_obj.x_loc('Width*0.5', [Width])
                        
            door_panel_left_1 = self.add_assembly(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_1.set_name("Door Panel Left 1")
            door_panel_left_1.x_loc('IF(RS,Width-Frame_Width-Panel_Depth*Open,Frame_Width+Panel_Depth*Open)', [Frame_Width, Open, Panel_Depth, RS, Width])
            door_panel_left_1.y_loc('Depth*0.5+IF(RS,-Panel_Depth*0.5,Panel_Depth*0.5)', [Depth, Panel_Depth, RS])
            door_panel_left_1.x_dim('(Width-Frame_Width*2-Door_Gap*2)*0.25', [Width, Frame_Width, Door_Gap])
            door_panel_left_1.z_dim('Height-INCH(3.25)', [Height])
            door_panel_left_1.z_rot('IF(RS,radians(180),0)+radians(-90)*Open', [Open, RS])
            door_panel_left_1.prompt('Hardware Config', value='Right')
            self.set_materials(door_panel_left_1)
            self.add_double_door_hardware(door_panel_left_1, placement='right')
            self.set_mirror_modifier(door_panel_left_1, "Mirror X", mirror_obj.obj)
            
            door_panel_left_2 = self.add_assembly(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_2.set_name("Door Panel Left 2")
            door_panel_left_2.obj_bp.parent = door_panel_left_1.obj_bp
            door_panel_left_2.x_loc('(Width-Frame_Width*2)*0.25+Door_Gap*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.x_dim('(Width-Frame_Width*2-Door_Gap*2)*0.25', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.z_dim('Height-INCH(3.25)', [Height])
            door_panel_left_2.z_rot('radians(180)-(radians(180)-(radians(90)*Open)*2)', [Open])
            door_panel_left_2.prompt('Hardware Config', value='Left')
            self.set_materials(door_panel_left_2)
            self.add_double_door_hardware(door_panel_left_2)
            self.set_mirror_modifier(door_panel_left_2, "Mirror X", mirror_obj.obj)
                       
        self.update()
        
        
class PROMPTS_Entry_Door_Prompts(bpy.types.Operator):
    bl_idname = LIBRARY_NAMESPACE + ".entry_door_prompts"
    bl_label = "Entry Door Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)

    door_rotation = bpy.props.FloatProperty(name="Door Rotation",subtype='ANGLE',min=0,max=math.radians(110))
    
    door_swing = bpy.props.EnumProperty(name="Door Swing",items=[('Left Swing',"Left Swing","Left Swing"),
                                                                 ('Right Swing',"Right Swing","Right Swing")])
    product = None
    
    open_door_prompt = None
    
    door_swing_prompt = None
    
    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        self.product.obj_x.location.x = self.width
         
        if self.product.obj_bp.mv.mirror_y:
            self.product.obj_y.location.y = -self.depth
        else:
            self.product.obj_y.location.y = self.depth
         
        if self.product.obj_bp.mv.mirror_z:
            self.product.obj_z.location.z = -self.height
        else:
            self.product.obj_z.location.z = self.height
             
        if self.open_door_prompt:
            self.open_door_prompt.set_value(self.door_rotation)
            
        if self.door_swing_prompt:
            self.door_swing_prompt.set_value(self.door_swing)            
             
        self.product.obj_bp.location = self.product.obj_bp.location
        self.product.obj_bp.location = self.product.obj_bp.location
            
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        if self.product.obj_bp:
            self.depth = math.fabs(self.product.obj_y.location.y)
            self.height = math.fabs(self.product.obj_z.location.z)
            self.width = math.fabs(self.product.obj_x.location.x)
            
            try:
                self.open_door_prompt = self.product.get_prompt("Door Rotation")
                self.door_rotation = self.open_door_prompt.value() 
            except:
                pass
            
            try:
                self.door_swing_prompt = self.product.get_prompt("Door Swing")  
                self.door_swing = self.door_swing_prompt.value()         
            except:
                pass
                
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=480)

    def draw_product_size(self,layout):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row1.label('Width: ' + str(unit.inch(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label('Width:')
            row1.prop(self,'width',text="")
            row1.prop(self.product.obj_x,'hide',text="")
        
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_z):
            row1.label('Height: ' + str(unit.inch(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label('Height:')
            row1.prop(self,'height',text="")
            row1.prop(self.product.obj_z,'hide',text="")
        
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_y):
            row1.label('Depth: ' + str(unit.inch(math.fabs(self.product.obj_y.location.y))))
        else:
            row1.label('Depth:')
            row1.prop(self,'depth',text="")
            row1.prop(self.product.obj_y,'hide',text="")
            
    def object_has_driver(self,obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True
            
    def draw_product_prompts(self,layout):

        if "Main Options" in self.product.obj_bp.mv.PromptPage.COL_MainTab:
            door_swing = self.product.get_prompt("Door Swing")
            reverse_swing = self.product.get_prompt("Reverse Swing")
            open_door = self.product.get_prompt("Open Door")
            open_left_door = self.product.get_prompt("Open Left Door")
            open_right_door = self.product.get_prompt("Open Right Door")
            
            box = layout.box()
            col = box.column(align=True)
            col.label("Main Options:")
            row = col.row()
            row.label("Open Door")
            
            if open_door:
                row.prop(open_door, "PercentageValue", text="")
            elif open_left_door:
                row.prop(open_left_door, "PercentageValue", text="Panel 1")
                row.prop(open_right_door, "PercentageValue", text="Panel 2")
            else:
                row.prop(self,'door_rotation',text="",slider=True)
                 
            if door_swing:
                col = box.column()
                row = col.row()                
                row.label("Door Swing")
                row.prop(self, 'door_swing',text="")
            col = box.column()
            
            if reverse_swing:
                row = col.row()                
                row.label("Reverse Swing")                
                row.prop(reverse_swing,'CheckBoxValue',text="")            
    
    def draw_product_placment(self,layout):
        box = layout.box()
        row = box.row()
        row.label('Location:')
        row.prop(self.product.obj_bp,'location',index=0,text="")

    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()
                
                split = box.split(percentage=.8)
                split.label(self.product.obj_bp.mv.name_object + " | " + self.product.obj_bp.cabinetlib.spec_group_name,icon='LATTICE_DATA')
                split.menu('MENU_Current_Cabinet_Menu',text="Menu",icon='DOWNARROW_HLT')
                
                self.draw_product_size(box)
                self.draw_product_prompts(box)
                self.draw_product_placment(box)        
        
  
class PRODUCT_Entry_Door_Frame(Entry_Door):
    
    def __init__(self):
        self.category_name = "Open Entry Ways"
        self.assembly_name = "Entry Door Frame"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        
        self.door_frame = "Door_Frame.blend"   
  
class PRODUCT_Entry_Door_Flat_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Flat Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"
  
class PRODUCT_Entry_Door_Double_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Double Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"
 
class PRODUCT_Entry_Door_Inset_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Inset Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"
 
class PRODUCT_Entry_Door_Glass_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Glass Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"
        
class PRODUCT_Entry_Door_Glass_Georgian_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Glass Georgian Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"
        
class PRODUCT_Entry_Door_Glass_Border_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Glass Border Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"
        
class PRODUCT_Entry_Double_Door_Double_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Double Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"
        
class PRODUCT_Entry_Double_Door_Flat_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Flat Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"        
        
class PRODUCT_Entry_Double_Door_Inset_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Inset Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"
        
class PRODUCT_Entry_Double_Door_Glass_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Glass Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"
        
class PRODUCT_Entry_Double_Door_Glass_Georgian_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Glass Georgian Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"
        
class PRODUCT_Entry_Double_Door_Glass_Border_Panel(Entry_Door):
    
    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Glass Border Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"
        
class PRODUCT_Sliding_Door_Flat_Panel(Sliding_Doors):
    
    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Flat Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"        
        
class PRODUCT_Sliding_Door_Inset_Panel(Sliding_Doors):
    
    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Inset Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"
        
class PRODUCT_Sliding_Door_Double_Panel(Sliding_Doors):
    
    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Double Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"
        
class PRODUCT_Sliding_Door_Glass_Panel(Sliding_Doors):
    
    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Glass Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"        
        
class PRODUCT_Sliding_Door_Glass_Georgian_Panel(Sliding_Doors):
    
    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Georgian Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"
        
class PRODUCT_Sliding_Door_Glass_Border_Panel(Sliding_Doors):
    
    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Glass Border Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"
        
class PRODUCT_Pocket_Door_Flat_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Flat Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"                
        
class PRODUCT_Pocket_Door_Inset_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Inset Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"
        
class PRODUCT_Pocket_Door_Double_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Double Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend" 
        
class PRODUCT_Pocket_Door_Glass_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Glass Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend" 
        
class PRODUCT_Pocket_Door_Glass_Georgian_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Glass Georgian Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend" 
        
class PRODUCT_Pocket_Door_Glass_Border_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Glass Border Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"
        
class PRODUCT_Pocket_Double_Door_Flat_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Flat Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Flat.blend"        
        
class PRODUCT_Pocket_Double_Door_Inset_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Inset Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Inset.blend"
        
class PRODUCT_Pocket_Double_Door_Double_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Double Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Double.blend"
        
class PRODUCT_Pocket_Double_Door_Glass_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Glass Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Glass.blend"
        
class PRODUCT_Pocket_Double_Door_Glass_Georgian_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Glass Georgian Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"
        
class PRODUCT_Pocket_Double_Door_Glass_Border_Panel(Pocket_Doors):
    
    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Glass Border Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"       
        
class PRODUCT_Bi_Fold_Door_Flat_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Flat Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"        
        
class PRODUCT_Bi_Fold_Door_Inset_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Inset Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"
        
class PRODUCT_Bi_Fold_Door_Double_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Double Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"        
        
class PRODUCT_Bi_Fold_Door_Glass_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Glass Panel"
        self.width = SINGLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"
                       
class PRODUCT_Bi_Fold_Double_Door_Flat_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Flat Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"   
        
class PRODUCT_Bi_Fold_Double_Door_Inset_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Inset Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"
        
class PRODUCT_Bi_Fold_Double_Door_Double_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Double Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"
        
class PRODUCT_Bi_Fold_Double_Door_Glass_Panel(Bi_Fold_Doors):
    
    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Glass Panel"
        self.width = DOUBLE_PANEL_WIDTH
        self.height = DOOR_HEIGHT
        self.depth = DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"
       
        
def register():
    bpy.utils.register_class(PROMPTS_Entry_Door_Prompts)