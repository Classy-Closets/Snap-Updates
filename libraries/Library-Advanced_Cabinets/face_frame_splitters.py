"""
Microvellum 
Splitters
Stores the logic and insert defs for the splitter library
"""

import bpy
from os import path
from mv import fd_types, unit, utils
from . import cabinet_machining
from . import cabinet_properties

ROOT_PATH = path.join(path.dirname(__file__),"Cabinet Assemblies")
CUTPARTS_DIR = path.join(ROOT_PATH,"Cut Parts")
PART_WITH_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with Edgebanding.blend")
HARDWOOD = path.join(ROOT_PATH,"Face Frames","Hardwood.blend")

#---------ASSEMBLY INSTRUCTIONS

class Vertical_FF_Splitters(fd_types.Assembly):
    
    library_name = "Face Frame Cabinet Splitters"
    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".splitter_prompts"
    mirror_y = False
    
    open_name = ""
    
    vertical_openings = 2 #1-10
    opening_1_height = 0
    opening_2_height = 0
    opening_3_height = 0
    opening_4_height = 0
    opening_5_height = 0
    opening_6_height = 0
    opening_7_height = 0
    opening_8_height = 0
    opening_9_height = 0
    opening_10_height = 0
    
    interior_1 = None
    exterior_1 = None
    interior_2 = None
    exterior_2 = None
    interior_3 = None
    exterior_3 = None
    interior_4 = None
    exterior_4 = None
    interior_5 = None
    exterior_5 = None
    interior_6 = None
    exterior_6 = None
    interior_7 = None
    exterior_7 = None
    interior_8 = None
    exterior_8 = None
    interior_9 = None
    exterior_9 = None
    interior_10 = None
    exterior_10 = None
    interior_11 = None
    exterior_11 = None
    
    def add_prompts(self):
        self.add_tab(name='Opening Heights',tab_type='CALCULATOR',calc_type="ZDIM")    
        self.add_tab(name='Formulas',tab_type='HIDDEN')    
        
        for i in range(1,self.vertical_openings+1):
        
            size = eval("self.opening_" + str(i) + "_height")
        
            self.add_prompt(name="Opening " + str(i) + " Height",
                            prompt_type='DISTANCE',
                            value=size,
                            tab_index=0,
                            equal=True if size == 0 else False)
    
        self.add_prompt(name="Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        
        Rail_Width = self.get_var('Rail Width')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        
        self.calculator_deduction("Rail_Width*(" + str(self.vertical_openings) +"-1)+Frame_Top_Gap+Frame_Bottom_Gap",[Rail_Width,Frame_Top_Gap,Frame_Bottom_Gap])
        
    def add_insert(self,insert,index,z_loc_vars=[],z_loc_expression=""):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Frame_Thickness = self.get_var('Frame Thickness')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        Frame_Right_Gap = self.get_var('Frame Right Gap')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        open_var = eval("self.get_var('Opening " + str(index) + " Height')")
        z_dim_expression = "Opening_" + str(index) + "_Height"

        if insert:
            if not insert.obj_bp:
                insert.draw()
            insert.obj_bp.parent = self.obj_bp
            insert.x_loc(value = 0)
            insert.y_loc(value = 0)
            if index == self.vertical_openings:
                insert.z_loc('-Frame_Bottom_Gap',[Frame_Bottom_Gap])
            else:
                insert.z_loc(z_loc_expression,z_loc_vars)
            insert.x_rot(value = 0)
            insert.y_rot(value = 0)
            insert.z_rot(value = 0)
            insert.x_dim('Width',[Width])
            insert.y_dim('Depth',[Depth])
            
            insert.prompt("Frame Thickness","Frame_Thickness",[Frame_Thickness])
            insert.prompt("Frame Left Gap","Frame_Left_Gap",[Frame_Left_Gap])
            insert.prompt("Frame Right Gap","Frame_Right_Gap",[Frame_Right_Gap])
            
            if index == 1:
                # TOP
                z_dim_vars = []
                z_dim_vars.append(open_var)
                z_dim_vars.append(Frame_Top_Gap)
                insert.z_dim("Opening_" + str(index) + "_Height+Frame_Top_Gap",z_dim_vars)
                insert.prompt("Frame Top Gap","Frame_Top_Gap",[Frame_Top_Gap])
            elif index == self.vertical_openings:
                # BOTTOM
                z_dim_vars = []
                z_dim_vars.append(open_var)
                z_dim_vars.append(Frame_Bottom_Gap)
                insert.z_dim("Opening_" + str(index) + "_Height+Frame_Bottom_Gap",z_dim_vars)
                insert.prompt("Frame Bottom Gap","Frame_Bottom_Gap",[Frame_Bottom_Gap])
            else:
                # MIDDLE
                insert.z_dim(z_dim_expression,[open_var]) 
    
    def get_opening(self,index):
        opening = self.add_opening()
        opening.set_name("Opening " + str(index))
        opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
        opening.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))
        
        if interior:
            opening.obj_bp.mv.interior_open = False
        
        if exterior:
            opening.obj_bp.mv.exterior_open = False
            
        return opening
        
    def add_splitters(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Rail_Width = self.get_var('Rail Width')
        Thickness = self.get_var('Thickness')
        Frame_Thickness = self.get_var('Frame Thickness')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        Frame_Right_Gap = self.get_var('Frame Right Gap')
        
        previous_splitter = None
        
        for i in range(1,self.vertical_openings):
            z_loc_vars = []
            open_var = eval("self.get_var('Opening " + str(i) + " Height')")
            z_loc_vars.append(open_var)
            
            if previous_splitter:
                z_loc = previous_splitter.get_var("loc_z","Splitter_Z_Loc")
                z_loc_vars.append(z_loc)

            splitter = self.add_assembly(HARDWOOD)
            splitter.set_name("Mid Rail " + str(i))
            splitter.x_loc('Frame_Left_Gap',[Frame_Left_Gap])
            splitter.y_loc('-Frame_Thickness',[Frame_Thickness])
            if previous_splitter:
                z_loc_vars.append(Rail_Width)
                splitter.z_loc('Splitter_Z_Loc-Opening_' + str(i) + '_Height-Rail_Width',z_loc_vars)
            else:
                z_loc_vars.append(Height)
                z_loc_vars.append(Frame_Top_Gap)
                splitter.z_loc('Height-Frame_Top_Gap-Opening_' + str(i) + '_Height',z_loc_vars)
            splitter.x_rot(value = 90)
            splitter.y_rot(value = 0)
            splitter.z_rot(value = 0)
            splitter.x_dim('Width-(Frame_Left_Gap+Frame_Right_Gap)',[Width,Frame_Left_Gap,Frame_Right_Gap])
            splitter.y_dim('-Rail_Width',[Rail_Width])
            splitter.z_dim('-Thickness',[Thickness])
            splitter.material('Exposed_Exterior_Surface')
            splitter.solid_stock("Hardwood")
            
            previous_splitter = splitter
            
            opening_z_loc_vars = []
            opening_z_loc = previous_splitter.get_var("loc_z","Splitter_Z_Loc")
            opening_z_loc_vars.append(opening_z_loc)
            
            exterior = eval('self.exterior_' + str(i))
            self.add_insert(exterior, i, opening_z_loc_vars, "Splitter_Z_Loc")
            
            interior = eval('self.interior_' + str(i))
            self.add_insert(interior, i, opening_z_loc_vars, "Splitter_Z_Loc")
            
            opening = self.get_opening(i)
            self.add_insert(opening, i, opening_z_loc_vars, "Splitter_Z_Loc")

        #ADD LAST INSERT
        bottom_exterior = eval('self.exterior_' + str(self.vertical_openings))
        self.add_insert(bottom_exterior, self.vertical_openings)
        
        bottom_interior = eval('self.interior_' + str(self.vertical_openings))
        self.add_insert(bottom_interior, self.vertical_openings)

        bottom_opening = self.get_opening(self.vertical_openings)
        self.add_insert(bottom_opening, self.vertical_openings)
            
    def draw(self):
        self.create_assembly()
        
        if self.vertical_openings == 1:
            pass
        else:
            self.add_prompts()
            self.add_splitters()
        
        self.update()

class Vertical_FF_Notched_Splitters(fd_types.Assembly):
    
    library_name = "Face Frame Cabinet Splitters"
    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".splitter_prompts"
    mirror_y = False
  
    open_name = ""
    
    vertical_openings = 2 #1-10
    opening_1_height = 0
    opening_2_height = 0
    opening_3_height = 0
    opening_4_height = 0
    opening_5_height = 0
    opening_6_height = 0
    opening_7_height = 0
    opening_8_height = 0
    opening_9_height = 0
    opening_10_height = 0
    
    interior_1 = None
    exterior_1 = None
    interior_2 = None
    exterior_2 = None
    interior_3 = None
    exterior_3 = None
    interior_4 = None
    exterior_4 = None
    interior_5 = None
    exterior_5 = None
    interior_6 = None
    exterior_6 = None
    interior_7 = None
    exterior_7 = None
    interior_8 = None
    exterior_8 = None
    interior_9 = None
    exterior_9 = None
    interior_10 = None
    exterior_10 = None
    interior_11 = None
    exterior_11 = None
    
    def add_prompts(self):
        self.add_tab(name='Opening Heights',tab_type='CALCULATOR',calc_type="ZDIM")    
        self.add_tab(name='Formulas',tab_type='HIDDEN')    
        
        for i in range(1,self.vertical_openings+1):
        
            size = eval("self.opening_" + str(i) + "_height")
        
            self.add_prompt(name="Opening " + str(i) + " Height",
                            prompt_type='DISTANCE',
                            value=size,
                            tab_index=0,
                            equal=True if size == 0 else False)
    
        self.add_prompt(name="Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        
        #----------W
        self.add_prompt(name="Right Side Depth",prompt_type='DISTANCE',value=unit.inch(23),tab_index=1)
        self.add_prompt(name="Left Side Depth",prompt_type='DISTANCE',value=unit.inch(23),tab_index=1)
        #----------W
        
        Rail_Width = self.get_var('Rail Width')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        
        self.calculator_deduction("Rail_Width*(" + str(self.vertical_openings) +"-1)+Frame_Top_Gap+Frame_Bottom_Gap",[Rail_Width,Frame_Top_Gap,Frame_Bottom_Gap])
        
    def add_insert(self,insert,index,z_loc_vars=[],z_loc_expression=""):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Frame_Thickness = self.get_var('Frame Thickness')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        Frame_Right_Gap = self.get_var('Frame Right Gap')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        open_var = eval("self.get_var('Opening " + str(index) + " Height')")
        z_dim_expression = "Opening_" + str(index) + "_Height"

        if insert:
            if not insert.obj_bp:
                insert.draw()
            insert.obj_bp.parent = self.obj_bp
            insert.x_loc(value = 0)
            insert.y_loc(value = 0)
            if index == self.vertical_openings:
                insert.z_loc('-Frame_Bottom_Gap',[Frame_Bottom_Gap])
            else:
                insert.z_loc(z_loc_expression,z_loc_vars)
            insert.x_rot(value = 0)
            insert.y_rot(value = 0)
            insert.z_rot(value = 0)
            insert.x_dim('Width',[Width])
            insert.y_dim('Depth',[Depth])
            
            insert.prompt("Frame Thickness","Frame_Thickness",[Frame_Thickness])
            insert.prompt("Frame Left Gap","Frame_Left_Gap",[Frame_Left_Gap])
            insert.prompt("Frame Right Gap","Frame_Right_Gap",[Frame_Right_Gap])
            
            if index == 1:
                # TOP
                z_dim_vars = []
                z_dim_vars.append(open_var)
                z_dim_vars.append(Frame_Top_Gap)
                insert.z_dim("Opening_" + str(index) + "_Height+Frame_Top_Gap",z_dim_vars)
                insert.prompt("Frame Top Gap","Frame_Top_Gap",[Frame_Top_Gap])
            elif index == self.vertical_openings:
                # BOTTOM
                z_dim_vars = []
                z_dim_vars.append(open_var)
                z_dim_vars.append(Frame_Bottom_Gap)
                insert.z_dim("Opening_" + str(index) + "_Height+Frame_Bottom_Gap",z_dim_vars)
                insert.prompt("Frame Bottom Gap","Frame_Bottom_Gap",[Frame_Bottom_Gap])
            else:
                # MIDDLE
                insert.z_dim(z_dim_expression,[open_var]) 
    
    def get_opening(self,index):
        opening = self.add_opening()
        opening.set_name("Opening " + str(index))
        opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
        opening.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))
        
        if interior:
            opening.obj_bp.mv.interior_open = False
        
        if exterior:
            opening.obj_bp.mv.exterior_open = False
            
        return opening
        
    def add_splitters(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Left_Side_Depth = self.get_var('Left Side Depth','Left_Side_Depth')
        Right_Side_Depth = self.get_var('Right Side Depth','Right_Side_Depth')
        Rail_Width = self.get_var('Rail Width')
        Thickness = self.get_var('Thickness')
        Frame_Thickness = self.get_var('Frame Thickness')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        Frame_Right_Gap = self.get_var('Frame Right Gap')
        
        previous_splitter = None
        
        for i in range(1,self.vertical_openings):
            z_loc_vars = []
            open_var = eval("self.get_var('Opening " + str(i) + " Height')")
            z_loc_vars.append(open_var)
            
            if previous_splitter:
                z_loc = previous_splitter.get_var("loc_z","Splitter_Z_Loc")
                z_loc_vars.append(z_loc)

            splitter_l = self.add_assembly(HARDWOOD)
            splitter_l.set_name("Mid Rail Left" + str(i))
            splitter_l.x_loc('Left_Side_Depth+Frame_Left_Gap',[Frame_Left_Gap,Left_Side_Depth])
            splitter_l.y_loc('Depth',[Depth])
            if previous_splitter:
                z_loc_vars.append(Rail_Width)
                splitter_l.z_loc('Splitter_Z_Loc-Opening_' + str(i) + '_Height-Rail_Width',z_loc_vars)
            else:
                z_loc_vars.append(Height)
                z_loc_vars.append(Frame_Top_Gap)
                splitter_l.z_loc('Height-Frame_Top_Gap-Opening_' + str(i) + '_Height',z_loc_vars)
            splitter_l.x_rot(value = 90)
            splitter_l.y_rot(value = 0)
            splitter_l.z_rot(value = 90)
            
            splitter_l.x_dim('-Depth-Right_Side_Depth',[Depth,Right_Side_Depth])
            splitter_l.y_dim('-Rail_Width',[Rail_Width])
            splitter_l.z_dim('-Thickness',[Thickness])
            splitter_l.material('Exposed_Exterior_Surface')
            splitter_l.solid_stock("Hardwood")
            
            splitter_r = self.add_assembly(HARDWOOD)
            splitter_r.set_name("Mid Rail Right" + str(i))
            
            splitter_r.x_loc("Width-Frame_Right_Gap",[Width,Frame_Right_Gap])
            splitter_r.y_loc("-Right_Side_Depth",[Right_Side_Depth])
            
            if previous_splitter:
                z_loc_vars.append(Rail_Width)
                splitter_r.z_loc('Splitter_Z_Loc-Opening_' + str(i) + '_Height-Rail_Width',z_loc_vars)
            else:
                z_loc_vars.append(Height)
                z_loc_vars.append(Frame_Top_Gap)
                splitter_r.z_loc('Height-Frame_Top_Gap-Opening_' + str(i) + '_Height',z_loc_vars)
            
            splitter_r.x_rot(value = 90)
            splitter_r.y_rot(value = 0)
            splitter_r.z_rot(value = -180) 
            
            splitter_r.x_dim("Width-Left_Side_Depth",[Width,Left_Side_Depth])
            splitter_r.y_dim('-Rail_Width',[Rail_Width])
            splitter_r.z_dim("-Thickness",[Thickness])
            splitter_r.material('Exposed_Exterior_Surface')
            splitter_r.solid_stock("Hardwood")
            
            previous_splitter = splitter_l     
            
            opening_z_loc_vars = []
            opening_z_loc = previous_splitter.get_var("loc_z","Splitter_Z_Loc")
            opening_z_loc_vars.append(opening_z_loc)
            
            exterior = eval('self.exterior_' + str(i))
            self.add_insert(exterior, i, opening_z_loc_vars, "Splitter_Z_Loc")
            
            interior = eval('self.interior_' + str(i))
            self.add_insert(interior, i, opening_z_loc_vars, "Splitter_Z_Loc")
            
            opening = self.get_opening(i)
            self.add_insert(opening, i, opening_z_loc_vars, "Splitter_Z_Loc")

        #ADD LAST INSERT
        bottom_exterior = eval('self.exterior_' + str(self.vertical_openings))
        self.add_insert(bottom_exterior, self.vertical_openings)
        
        bottom_interior = eval('self.interior_' + str(self.vertical_openings))
        self.add_insert(bottom_interior, self.vertical_openings)

        bottom_opening = self.get_opening(self.vertical_openings)
        self.add_insert(bottom_opening, self.vertical_openings)
            
    def draw(self):
        self.create_assembly()
        
        if self.vertical_openings == 1:
            pass
        else:
            self.add_prompts()
            self.add_splitters()
        
        self.update()
        
class Horizontal_FF_Splitters(fd_types.Assembly):
    
    library_name = "Face Frame Cabinet Splitters"
    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".splitter_prompts"
    mirror_y = False
  
    open_name = ""
    carcass_type = "" # {Base, Tall, Upper, Sink, Suspended}
    
    horizontal_openings = 2 #1-10
    opening_1_width = 0
    opening_2_width = 0
    opening_3_width = 0
    opening_4_width = 0
    opening_5_width = 0
    opening_6_width = 0
    opening_7_width = 0
    opening_8_width = 0
    opening_9_width = 0
    opening_10_width = 0
    
    interior_1 = None
    exterior_1 = None
    interior_2 = None
    exterior_2 = None
    interior_3 = None
    exterior_3 = None
    interior_4 = None
    exterior_4 = None
    interior_5 = None
    exterior_5 = None
    interior_6 = None
    exterior_6 = None
    interior_7 = None
    exterior_7 = None
    interior_8 = None
    exterior_8 = None
    interior_9 = None
    exterior_9 = None
    interior_10 = None
    exterior_10 = None
    interior_11 = None
    exterior_11 = None
    
    def add_prompts(self):
        self.add_tab(name='Opening Widths',tab_type='CALCULATOR',calc_type="XDIM")    
        self.add_tab(name='Formulas',tab_type='HIDDEN')    
        
        for i in range(1,self.horizontal_openings+1):
        
            size = eval("self.opening_" + str(i) + "_width")
        
            self.add_prompt(name="Opening " + str(i) + " Width",
                            prompt_type='DISTANCE',
                            value=size,
                            tab_index=0,
                            equal=True if size == 0 else False)
    
        self.add_prompt(name="Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Rail Width",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        
        Rail_Width = self.get_var('Rail Width')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        Frame_Right_Gap = self.get_var('Frame Right Gap')
        
        self.calculator_deduction("Frame_Left_Gap+Frame_Right_Gap+Rail_Width*(" + str(self.horizontal_openings) +"-1)",[Rail_Width,Frame_Left_Gap,Frame_Right_Gap])
        
    def add_insert(self,insert,index,x_loc_vars=[],x_loc_expression=""):
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Frame_Thickness = self.get_var('Frame Thickness')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        Frame_Right_Gap = self.get_var('Frame Right Gap')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        open_var = eval("self.get_var('Opening " + str(index) + " Width')")
        x_dim_expression = "Opening_" + str(index) + "_Width"

        if insert:
            if not insert.obj_bp:
                insert.draw()
            insert.obj_bp.parent = self.obj_bp
            if index == 1:
                insert.x_loc(value = 0)
            else:
                insert.x_loc(x_loc_expression,x_loc_vars)
            insert.y_loc(value = 0)
            insert.z_loc(value = 0)
            insert.x_rot(value = 0)
            insert.y_rot(value = 0)
            insert.z_rot(value = 0)
            insert.y_dim('Depth',[Depth])
            insert.z_dim('Height',[Height])
            insert.prompt("Frame Thickness","Frame_Thickness",[Frame_Thickness])
            insert.prompt("Frame Top Gap","Frame_Top_Gap",[Frame_Top_Gap])
            insert.prompt("Frame Bottom Gap","Frame_Bottom_Gap",[Frame_Bottom_Gap])
            
            if index == 1:
                # LEFT
                x_dim_vars = []
                x_dim_vars.append(open_var)
                x_dim_vars.append(Frame_Left_Gap)
                insert.x_dim("Opening_" + str(index) + "_Width+Frame_Left_Gap",x_dim_vars)
                insert.prompt("Frame Left Gap","Frame_Left_Gap",[Frame_Left_Gap])
            elif index == self.horizontal_openings:
                # RIGHT
                x_dim_vars = []
                x_dim_vars.append(open_var)
                x_dim_vars.append(Frame_Right_Gap)
                insert.x_dim("Opening_" + str(index) + "_Width+Frame_Right_Gap",x_dim_vars)
                insert.prompt("Frame Right Gap","Frame_Right_Gap",[Frame_Right_Gap])
            else:
                # MIDDLE
                insert.x_dim(x_dim_expression,[open_var]) 
    
    def get_opening(self,index):
        opening = self.add_opening()
        opening.set_name("Opening " + str(index))
        opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
        opening.add_prompt(name="Frame Thickness",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Left Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Right Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Top Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Frame Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        Frame_Thickness = self.get_var('Frame Thickness')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        Frame_Right_Gap = self.get_var('Frame Right Gap')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        
        opening.prompt("Frame Top Gap","Frame_Top_Gap",[Frame_Top_Gap])
        opening.prompt("Frame Bottom Gap","Frame_Bottom_Gap",[Frame_Bottom_Gap])
        opening.prompt("Frame Thickness","Frame_Thickness",[Frame_Thickness])
        
        #TODO: Calculate logic for left and right frame gap. 
        if index == 1: #IS LEFT
            opening.prompt("Frame Left Gap","Frame_Left_Gap",[Frame_Left_Gap])
        else:
            pass #TODO: Calculate if splitter is turned on to calculate gap
         
        if index == self.horizontal_openings: #IS RIGHT
            opening.prompt("Frame Right Gap","Frame_Right_Gap",[Frame_Right_Gap])
        else:
            pass #TODO: Calculate if splitter is turned on to calculate gap
        
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))
        
        if interior:
            opening.obj_bp.mv.interior_open = False
        
        if exterior:
            opening.obj_bp.mv.exterior_open = False
            
        return opening
        
    def add_splitters(self):
        Height = self.get_var('dim_z','Height')
        Rail_Width = self.get_var('Rail Width')
        Thickness = self.get_var('Thickness')
        Frame_Thickness = self.get_var('Frame Thickness')
        Frame_Top_Gap = self.get_var('Frame Top Gap')
        Frame_Bottom_Gap = self.get_var('Frame Bottom Gap')
        Frame_Left_Gap = self.get_var('Frame Left Gap')
        
        previous_splitter = None
        
        for i in range(1,self.horizontal_openings):
            x_loc_vars = []
            open_var = eval("self.get_var('Opening " + str(i) + " Width')")
            x_loc_vars.append(open_var)
            
            if previous_splitter:
                x_loc = previous_splitter.get_var("loc_x","Splitter_X_Loc")
                x_loc_vars.append(x_loc)
                x_loc_vars.append(Rail_Width)

            splitter = self.add_assembly(HARDWOOD)
            splitter.set_name("Mid Rail " + str(i))
            if previous_splitter:
                splitter.x_loc('Splitter_X_Loc+Opening_' + str(i) + '_Width+Rail_Width',x_loc_vars)
            else:
                x_loc_vars.append(Frame_Left_Gap)
                splitter.x_loc('Opening_' + str(i) + '_Width+Frame_Left_Gap',x_loc_vars)
            splitter.y_loc('-Frame_Thickness',[Frame_Thickness])
            splitter.z_loc('Frame_Bottom_Gap',[Frame_Bottom_Gap])
            splitter.x_rot(value = 90)
            splitter.y_rot(value = -90)
            splitter.z_rot(value = 0)
            splitter.x_dim('Height-(Frame_Top_Gap+Frame_Bottom_Gap)',[Height,Frame_Top_Gap,Frame_Bottom_Gap])
            splitter.y_dim('-Rail_Width',[Rail_Width])
            splitter.z_dim('-Thickness',[Thickness])
            splitter.material('Exposed_Exterior_Surface')
            splitter.solid_stock("Hardwood")
            
            previous_splitter = splitter
            
            exterior = eval('self.exterior_' + str(i))
            self.add_insert(exterior, i, x_loc_vars, "Splitter_X_Loc+Rail_Width")
            
            interior = eval('self.interior_' + str(i))
            self.add_insert(interior, i, x_loc_vars, "Splitter_X_Loc+Rail_Width")
            
            opening = self.get_opening(i)
            self.add_insert(opening, i, x_loc_vars, "Splitter_X_Loc+Rail_Width")
            
        opening_x_loc_vars = []
        opening_x_loc_vars.append(previous_splitter.get_var("loc_x","Splitter_X_Loc"))
        opening_x_loc_vars.append(Rail_Width)
            
        #ADD LAST INSERT
        last_exterior = eval('self.exterior_' + str(self.horizontal_openings))
        self.add_insert(last_exterior, self.horizontal_openings,opening_x_loc_vars, "Splitter_X_Loc+Rail_Width")
        
        last_interior = eval('self.interior_' + str(self.horizontal_openings))
        self.add_insert(last_interior, self.horizontal_openings,opening_x_loc_vars, "Splitter_X_Loc+Rail_Width")

        last_opening = self.get_opening(self.horizontal_openings)
        self.add_insert(last_opening, self.horizontal_openings,opening_x_loc_vars, "Splitter_X_Loc+Rail_Width")

    def draw(self):
        self.create_assembly()
        
        self.add_prompts()
        self.add_splitters()
        
        self.update()
        
#---------INSERTS        

class INSERT_2_Vertical_Openings_FF(Vertical_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "2 Vertical Openings FF"
        self.vertical_openings = 2
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_3_Vertical_Openings_FF(Vertical_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "3 Vertical Openings FF"
        self.vertical_openings = 3
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_4_Vertical_Openings_FF(Vertical_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "4 Vertical Openings FF"
        self.vertical_openings = 4
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_5_Vertical_Openings_FF(Vertical_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "5 Vertical Openings FF"
        self.vertical_openings = 5
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_2_Vertical_Notched_Openings_1_FF(Vertical_FF_Notched_Splitters):
    
    def __init__(self): 
        self.category_name = "Splitters"
        self.assembly_name = "2 Vertical Notched Openings FF"
        self.vertical_openings = 2
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(-36)               
        
class INSERT_3_Vertical_Notched_Openings_FF(Vertical_FF_Notched_Splitters):
    
    def __init__(self): 
        self.category_name = "Splitters"
        self.assembly_name = "3 Vertical Notched Openings FF"
        self.vertical_openings = 3
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(-36)     
        
class INSERT_4_Vertical_Notched_Openings_FF(Vertical_FF_Notched_Splitters):
    
    def __init__(self): 
        self.category_name = "Splitters"
        self.assembly_name = "4 Vertical Notched Openings FF"
        self.vertical_openings = 4
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(-36)         
        
class INSERT_5_Vertical_Notched_Openings_FF(Vertical_FF_Notched_Splitters):
    
    def __init__(self): 
        self.category_name = "Splitters"
        self.assembly_name = "5 Vertical Notched Openings FF"
        self.vertical_openings = 5
        self.width = unit.inch(36)
        self.height = unit.inch(34)
        self.depth = unit.inch(-36)             
        
class INSERT_2_Horizontal_Openings_FF(Horizontal_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "2 Horizontal Openings FF"
        self.horizontal_openings = 2
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_3_Horizontal_Openings_FF(Horizontal_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "3 Horizontal Openings FF"
        self.horizontal_openings = 3
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_4_Horizontal_Openings_FF(Horizontal_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "4 Horizontal Openings FF"
        self.horizontal_openings = 4
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_5_Horizontal_Openings_FF(Horizontal_FF_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "5 Horizontal Openings FF"
        self.horizontal_openings = 5
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
    