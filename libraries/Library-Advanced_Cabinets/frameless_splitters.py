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

ROOT_DIR = path.dirname(__file__)
CUTPARTS_DIR = path.join(ROOT_DIR,"Cabinet Assemblies","Cut Parts")
PART_WITH_EDGEBANDING = path.join(CUTPARTS_DIR,"Part with Edgebanding.blend")

#---------ASSEMBLY INSTRUCTIONS
        
class Vertical_Splitters(fd_types.Assembly):
    
    library_name = "Frameless Cabinet Splitters"
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
    
    remove_splitter_1 = False
    remove_splitter_2 = False
    remove_splitter_3 = False
    remove_splitter_4 = False
    remove_splitter_5 = False
    remove_splitter_6 = False
    remove_splitter_7 = False
    remove_splitter_8 = False
    remove_splitter_9 = False
    
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
        self.add_prompt(name="Left Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        
        Thickness = self.get_var('Thickness')
        
        self.calculator_deduction("Thickness*(" + str(self.vertical_openings) +"-1)",[Thickness])
        
    def add_insert(self,insert,index,z_loc_vars=[],z_loc_expression=""):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        open_var = eval("self.get_var('Opening " + str(index) + " Height')")
        z_dim_expression = "Opening_" + str(index) + "_Height"
        
        if insert:
            if not insert.obj_bp:
                insert.draw()
            insert.obj_bp.parent = self.obj_bp
            insert.x_loc(value = 0)
            insert.y_loc(value = 0)
            if index == self.vertical_openings:
                insert.z_loc(value = 0)
            else:
                insert.z_loc(z_loc_expression,z_loc_vars)
            insert.x_rot(value = 0)
            insert.y_rot(value = 0)
            insert.z_rot(value = 0)
            insert.x_dim('Width',[Width])
            insert.y_dim('Depth',[Depth])
            insert.z_dim(z_dim_expression,[open_var])
            if index == 1:
                # ALLOW DOOR TO EXTEND TO TOP OF VALANCE
                extend_top_amount = insert.get_prompt("Extend Top Amount")
                if extend_top_amount:
                    Extend_Top_Amount = self.get_var("Extend Top Amount")
                    insert.prompt('Extend Top Amount','Extend_Top_Amount',[Extend_Top_Amount])
            
            if index == self.vertical_openings:
                # ALLOW DOOR TO EXTEND TO BOTTOM OF VALANCE
                extend_bottom_amount = insert.get_prompt("Extend Bottom Amount")
                if extend_bottom_amount:
                    Extend_Bottom_Amount = self.get_var("Extend Bottom Amount")
                    insert.prompt('Extend Bottom Amount','Extend_Bottom_Amount',[Extend_Bottom_Amount])
        
    def get_opening(self,index):
        opening = self.add_opening()
        opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
        opening.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
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
        Thickness = self.get_var('Thickness')
        
        previous_splitter = None
        
        for i in range(1,self.vertical_openings):

            z_loc_vars = []
            open_var = eval("self.get_var('Opening " + str(i) + " Height')")
            z_loc_vars.append(open_var)
            
            if previous_splitter:
                z_loc = previous_splitter.get_var("loc_z","Splitter_Z_Loc")
                z_loc_vars.append(z_loc)
                
            splitter = self.add_assembly(PART_WITH_EDGEBANDING)
            splitter.set_name("Splitter " + str(i))
            splitter.x_loc(value = 0)
            splitter.y_loc(value = 0)
            if previous_splitter:
                z_loc_vars.append(Thickness)
                splitter.z_loc('Splitter_Z_Loc-Opening_' + str(i) + '_Height-Thickness',z_loc_vars)
            else:
                z_loc_vars.append(Height)
                splitter.z_loc('Height-Opening_' + str(i) + '_Height',z_loc_vars)
            splitter.x_rot(value = 0)
            splitter.y_rot(value = 0)
            splitter.z_rot(value = 0)
            splitter.x_dim('Width',[Width])
            splitter.y_dim('Depth',[Depth])
            splitter.z_dim('-Thickness',[Thickness])
            remove_splitter = eval("self.remove_splitter_" + str(i))
            if remove_splitter:
                splitter.prompt('Hide',value=True)
            splitter.cutpart("Cabinet_Shelf")
            splitter.edgebanding('Cabinet_Body_Edges',l2 = True)
            cabinet_machining.add_drilling(splitter)
            
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
        
        self.add_prompts()
        
        self.add_splitters()
        
        self.update()
        
class Horizontal_Splitters(fd_types.Assembly):
    
    library_name = "Frameless Cabinet Splitters"
    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".splitter_prompts"
    mirror_y = False
  
    open_name = ""

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
    
        self.add_prompt(name="Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
        
        Thickness = self.get_var('Thickness')
        
        self.calculator_deduction("Thickness*(" + str(self.horizontal_openings) +"-1)",[Thickness])
        
    def add_insert(self,insert,index,x_loc_vars=[],x_loc_expression=""):
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        open_var = eval("self.get_var('Opening " + str(index) + " Width')")
        x_dim_expression = "Opening_" + str(index) + "_Width"
        
        if insert:
            if not insert.obj_bp:
                insert.draw()

            insert.obj_bp.parent = self.obj_bp
            if index == 1:
                insert.x_loc(value = 0)
            else:
                print(index,x_loc_expression)
                insert.x_loc(x_loc_expression,x_loc_vars)
            insert.y_loc(value = 0)
            insert.z_loc(value = 0)
            insert.x_rot(value = 0)
            insert.y_rot(value = 0)
            insert.z_rot(value = 0)
            insert.x_dim(x_dim_expression,[open_var])
            insert.y_dim('Depth',[Depth])
            insert.z_dim('Height',[Height])
        
    def get_opening(self,index):
        opening = self.add_opening()
        opening.set_name("Opening " + str(index))
        opening.add_tab(name='Material Thickness',tab_type='HIDDEN')
        opening.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        opening.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        opening.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=0)
        
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))
        
        if interior:
            opening.obj_bp.mv.interior_open = False
        
        if exterior:
            opening.obj_bp.mv.exterior_open = False
            
        return opening
        
    def add_splitters(self):
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Thickness = self.get_var('Thickness')
        
        previous_splitter = None
        
        for i in range(1,self.horizontal_openings):
            
            x_loc_vars = []
            open_var = eval("self.get_var('Opening " + str(i) + " Width')")
            x_loc_vars.append(open_var)
            
            if previous_splitter:
                x_loc = previous_splitter.get_var("loc_x","Splitter_X_Loc")
                x_loc_vars.append(x_loc)
                x_loc_vars.append(Thickness)

            splitter = self.add_assembly(PART_WITH_EDGEBANDING)
            splitter.set_name("Splitter " + str(i))
            if previous_splitter:
                splitter.x_loc("Splitter_X_Loc+Thickness+Opening_" + str(i) + "_Width",x_loc_vars)
            else:
                splitter.x_loc("Opening_" + str(i) + "_Width",[open_var])
                
            splitter.y_loc(value = 0)
            splitter.z_loc(value = 0)
            splitter.x_rot(value = 0)
            splitter.y_rot(value = -90)
            splitter.z_rot(value = 0)
            splitter.x_dim('Height',[Height])
            splitter.y_dim('Depth',[Depth])
            splitter.z_dim('-Thickness',[Thickness])
            splitter.cutpart("Cabinet_Shelf")
            splitter.edgebanding('Cabinet_Body_Edges',l2 = True)

            previous_splitter = splitter

            exterior = eval('self.exterior_' + str(i))
            self.add_insert(exterior, i, x_loc_vars, "Splitter_X_Loc+Thickness")
            
            interior = eval('self.interior_' + str(i))
            self.add_insert(interior, i, x_loc_vars, "Splitter_X_Loc+Thickness")
            
            opening = self.get_opening(i)
            self.add_insert(opening, i, x_loc_vars, "Splitter_X_Loc+Thickness")
            
        insert_x_loc_vars = []
        insert_x_loc = previous_splitter.get_var("loc_x","Splitter_X_Loc")
        insert_x_loc_vars.append(insert_x_loc)
        insert_x_loc_vars.append(Thickness)

        #ADD LAST INSERT
        last_exterior = eval('self.exterior_' + str(self.horizontal_openings))
        self.add_insert(last_exterior, self.horizontal_openings,insert_x_loc_vars, "Splitter_X_Loc+Thickness")
          
        last_interior = eval('self.interior_' + str(self.horizontal_openings))
        self.add_insert(last_interior, self.horizontal_openings,insert_x_loc_vars, "Splitter_X_Loc+Thickness")

        last_opening = self.get_opening(self.horizontal_openings)
        self.add_insert(last_opening, self.horizontal_openings,insert_x_loc_vars, "Splitter_X_Loc+Thickness")
        
    def draw(self):
        self.create_assembly()
        
        self.add_prompts()
        
        self.add_splitters()
        
        self.update()
        

        
#---------INSERTS        

class INSERT_2_Horizontal_Openings(Horizontal_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "2 Horizontal Openings"
        self.horizontal_openings = 2
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_3_Horizontal_Openings(Horizontal_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "3 Horizontal Openings"
        self.horizontal_openings = 3
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_4_Horizontal_Openings(Horizontal_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "4 Horizontal Openings"
        self.horizontal_openings = 4
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_5_Horizontal_Openings(Horizontal_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "5 Horizontal Openings"
        self.horizontal_openings = 5
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_2_Vertical_Openings(Vertical_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "2 Vertical Openings"
        self.vertical_openings = 2
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_3_Vertical_Openings(Vertical_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "3 Vertical Openings"
        self.vertical_openings = 3
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_4_Vertical_Openings(Vertical_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "4 Vertical Openings"
        self.vertical_openings = 4
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        
class INSERT_5_Vertical_Openings(Vertical_Splitters):
    
    def __init__(self):
        self.category_name = "Splitters"
        self.assembly_name = "5 Vertical Openings"
        self.vertical_openings = 5
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)