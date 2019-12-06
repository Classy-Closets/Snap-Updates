"""
Microvellum 
Interiors
Stores the logic and insert defs for all interior components for cabinets and closets.
Shelves, Dividers, Divisions, Rollouts, Wire Baskets, Hanging Rods
"""

import bpy
from mv import utils, unit, fd_types
from . import drawer_boxes
from . import cabinet_machining
from . import cabinet_properties
from os import path

ROOT_PATH = path.join(path.dirname(__file__),"Cabinet Assemblies")

SHELVES = path.join(ROOT_PATH,"Shelves","Shelves.blend")
SHELF = path.join(ROOT_PATH,"Cut Parts","Part with Edgebanding.blend")
DIVIDER = path.join(ROOT_PATH,"Cut Parts","Part with Edgebanding.blend")
DIVISION = path.join(ROOT_PATH,"Cut Parts","Part with Edgebanding.blend")
ADJ_MACHINING = path.join(ROOT_PATH,"Machining","Adjustable Shelf Holes.blend")

def add_adj_shelf_machining(part,insert):
    
    Width = insert.get_var('dim_x','Width')
    Height = insert.get_var('dim_z','Height')
    Depth = insert.get_var('dim_y','Depth')
    Part_Width = part.get_var('dim_y','Part_Width')
    Part_Z_Loc = part.get_var('loc_z','Part_Z_Loc')
    Adj_Shelf_Setback = insert.get_var("Adj Shelf Setback")
    Space_From_Front = insert.get_var("Space From Front")
    Space_From_Rear = insert.get_var("Space From Rear")
    Space_From_Top = insert.get_var("Space From Top")
    Space_From_Bottom = insert.get_var("Space From Bottom")
    Shelf_Hole_Spacing = insert.get_var("Shelf Hole Spacing")
    Shelf_Clip_Gap = insert.get_var("Shelf Clip Gap")
    Adj_Shelf_Qty = insert.get_var("Adj Shelf Qty")
    
    tokens = []
    tokens.append(part.add_machine_token('Left Shelf Drilling' ,'SHELF','3'))
    tokens.append(part.add_machine_token('Right Shelf Drilling' ,'SHELF','4'))

    for token in tokens:
        token[1].add_driver(token[0],'space_from_bottom','Part_Z_Loc-Space_From_Bottom',[Part_Z_Loc,Space_From_Bottom])
        token[1].add_driver(token[0],'dim_to_first_row','Space_From_Front',[Space_From_Front])
        token[1].face_bore_depth = unit.inch(.5)
        token[1].add_driver(token[0],'space_from_top','Height-Part_Z_Loc-Space_From_Top',[Height,Part_Z_Loc,Space_From_Top])
        token[1].add_driver(token[0],'dim_to_second_row','fabs(Part_Width)-Space_From_Rear',[Part_Width,Space_From_Rear])
        token[1].face_bore_dia = 5
        token[1].shelf_hole_spacing = unit.millimeter(32)
        token[1].add_driver(token[0],'shelf_clip_gap','Shelf_Clip_Gap',[Shelf_Clip_Gap])
        token[1].reverse_direction = False

#---------ASSEMBLY INSTRUCTIONS
    
class Simple_Shelves(fd_types.Assembly):
    
    library_name = "Cabinet Interiors"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".interior_prompts"
    mirror_y = False
    
    carcass_type = "" # {Base, Tall, Upper, Sink, Suspended}
    open_name = ""
    shelf_qty = 1
    
    def add_common_prompts(self):
        self.add_tab(name='Interior Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')

        self.add_prompt(name="Shelf Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)

        self.add_prompt(name="Edgebanding Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.1),
                        tab_index=1)
    
#         sgi = self.get_var('cabinetlib.spec_group_index','sgi')
    
#         self.prompt('Edgebanding Thickness','EDGE_THICKNESS(sgi,"Cabinet_Interior_Edges' + self.open_name + '")',[sgi])
    
    def add_adj_prompts(self):
        props = cabinet_properties.get_scene_props().interior_defaults
        
        self.add_prompt(name="Shelf Qty",
                        prompt_type='QUANTITY',
                        value=self.shelf_qty,
                        tab_index=0)
        
        self.add_prompt(name="Shelf Setback",
                        prompt_type='DISTANCE',
                        value=props.adj_shelf_setback,
                        tab_index=0)

#         sgi = self.get_var('cabinetlib.spec_group_index','sgi')

#         self.prompt('Adjustable Shelf Thickness','THICKNESS(sgi,"Cabinet_Shelf' + self.open_name + '")',[sgi])

    def add_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Setback = self.get_var("Shelf Setback")
        Shelf_Thickness = self.get_var("Shelf Thickness")

        adj_shelf = self.add_assembly(SHELF)
        adj_shelf.set_name("Adjustable Shelf")
        adj_shelf.x_loc(value=0)
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc('((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))',[Height,Shelf_Thickness,Shelf_Qty])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width',[Width])
        adj_shelf.y_dim('-Depth+Shelf_Setback',[Depth,Shelf_Setback])
        adj_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(Shelf_Qty==0,True,False)',[Shelf_Qty])
        adj_shelf.prompt('Z Quantity','Shelf_Qty',[Shelf_Qty])
        adj_shelf.prompt('Z Offset','((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))',[Height,Shelf_Thickness,Shelf_Qty])
        adj_shelf.cutpart("Cabinet_Shelf")
        adj_shelf.edgebanding('Cabinet_Interior_Edges',l1 = True, w1 = True, l2 = True, w2 = True)

    def draw(self):
        self.create_assembly()
        
        self.add_common_prompts()
        self.add_adj_prompts()
        self.add_shelves()

        self.update()    
    
class Shelves(fd_types.Assembly):
    
    library_name = "Cabinet Interiors"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".interior_prompts"
    mirror_y = False
    
    carcass_type = "" # {Base, Tall, Upper, Sink, Suspended}
    open_name = ""
    shelf_qty = 1
    add_adjustable_shelves = True
    add_fixed_shelves = False
    
    def add_common_prompts(self):
        self.add_tab(name='Interior Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')

        self.add_prompt(name="Edgebanding Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
    
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
    
        self.prompt('Edgebanding Thickness','EDGE_THICKNESS(sgi,"Cabinet_Interior_Edges' + self.open_name + '")',[sgi])
    
    def add_adj_prompts(self):
        props = cabinet_properties.get_scene_props().interior_defaults
        
        self.add_prompt(name="Adj Shelf Qty",
                        prompt_type='QUANTITY',
                        value=self.shelf_qty,
                        tab_index=0)
        
        self.add_prompt(name="Adj Shelf Setback",
                        prompt_type='DISTANCE',
                        value=props.adj_shelf_setback,
                        tab_index=0)
        
        self.add_prompt(name="Space From Front",
                        prompt_type='DISTANCE',
                        value=unit.inch(1.5),
                        tab_index=0)
        
        self.add_prompt(name="Space From Rear",
                        prompt_type='DISTANCE',
                        value=unit.inch(1.5),
                        tab_index=0)
        
        self.add_prompt(name="Space From Top",
                        prompt_type='DISTANCE',
                        value=unit.inch(1.5),
                        tab_index=0)
        
        self.add_prompt(name="Space From Bottom",
                        prompt_type='DISTANCE',
                        value=unit.inch(1.5),
                        tab_index=0)
        
        self.add_prompt(name="Shelf Hole Spacing",
                        prompt_type='DISTANCE',
                        value=unit.inch(32/25.4),
                        tab_index=0)
        
        self.add_prompt(name="Shelf Clip Gap",
                        prompt_type='DISTANCE',
                        value=unit.inch(.125),
                        tab_index=0)

        self.add_prompt(name="Adjustable Shelf Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
        
        self.add_prompt(name="Shelf Pin Quantity",
                        prompt_type='QUANTITY',
                        value=0,
                        tab_index=1)

        sgi = self.get_var('cabinetlib.spec_group_index','sgi')

        self.prompt('Adjustable Shelf Thickness','THICKNESS(sgi,"Cabinet_Shelf' + self.open_name + '")',[sgi])

    def add_fixed_prompts(self):
        props = cabinet_properties.get_scene_props().interior_defaults

        self.add_prompt(name="Fixed Shelf Qty",
                        prompt_type='QUANTITY',
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Fixed Shelf Setback",
                        prompt_type='DISTANCE',
                        value=props.fixed_shelf_setback,
                        tab_index=0)
        
        self.add_prompt(name="Fixed Shelf Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')

        self.prompt('Fixed Shelf Thickness','THICKNESS(sgi,"Cabinet_Shelf' + self.open_name + '")',[sgi])
        
    def add_advanced_frameless_prompts(self):
        self.add_prompt(name="Shelf Row Quantity",
                        prompt_type='QUANTITY',
                        value=0,
                        tab_index=0)
        
        adj_qty = self.get_var('Adj Shelf Qty','adj_qty')
        fixed_qty = self.get_var('Fixed Shelf Qty','fixed_qty')
        
        self.prompt('Shelf Row Quantity','IF(adj_qty>fixed_qty,adj_qty,fixed_qty)',[adj_qty,fixed_qty])
        
    def add_adjustable_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Adj_Shelf_Qty = self.get_var("Adj Shelf Qty")
        Adj_Shelf_Setback = self.get_var("Adj Shelf Setback")
        Adjustable_Shelf_Thickness = self.get_var("Adjustable Shelf Thickness")
        Shelf_Clip_Gap = self.get_var("Shelf Clip Gap")

        for i in range(1,6):
            spacing = '((Height-(Adjustable_Shelf_Thickness*Adj_Shelf_Qty))/(Adj_Shelf_Qty+1))'
            adj_shelf = self.add_assembly(SHELF)
            adj_shelf.set_name("Adjustable Shelf")
            adj_shelf.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            adj_shelf.y_loc('Depth',[Depth])
            adj_shelf.z_loc('(' + spacing + ')*IF(' + str(i) + '>Adj_Shelf_Qty,0,' + str(i) + ')+IF(' + str(i) + '>Adj_Shelf_Qty,0,Adjustable_Shelf_Thickness*' + str(i - 1) + ')',
                            [Height,Adjustable_Shelf_Thickness,Adj_Shelf_Qty])
            adj_shelf.x_rot(value = 0)
            adj_shelf.y_rot(value = 0)
            adj_shelf.z_rot(value = 0)
            adj_shelf.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            adj_shelf.y_dim('-Depth+Adj_Shelf_Setback',[Depth,Adj_Shelf_Setback])
            adj_shelf.z_dim('Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            adj_shelf.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,False)',[Adj_Shelf_Qty])
            adj_shelf.cutpart("Cabinet_Shelf")
            adj_shelf.edgebanding('Cabinet_Interior_Edges',l1 = True, w1 = True, l2 = True, w2 = True)
            if i == 1:
                add_adj_shelf_machining(adj_shelf,self)
            
    def add_adjustable_shelf_holes(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Adj_Shelf_Setback = self.get_var("Adj Shelf Setback")
        Space_From_Front = self.get_var("Space From Front")
        Space_From_Rear = self.get_var("Space From Rear")
        Space_From_Top = self.get_var("Space From Top")
        Space_From_Bottom = self.get_var("Space From Bottom")
        Shelf_Hole_Spacing = self.get_var("Shelf Hole Spacing")
        Adj_Shelf_Qty = self.get_var("Adj Shelf Qty")
        
        shelf_holes = self.add_assembly(ADJ_MACHINING)
        shelf_holes.set_name("Adjustable Shelf Holes")
        shelf_holes.x_loc(value = 0)
        shelf_holes.y_loc('Adj_Shelf_Setback',[Adj_Shelf_Setback])
        shelf_holes.z_loc('',[])
        shelf_holes.x_rot(value = 0)
        shelf_holes.y_rot(value = 0)
        shelf_holes.z_rot(value = 0)
        shelf_holes.x_dim('Width',[Width])
        shelf_holes.y_dim('Depth-Adj_Shelf_Setback',[Depth,Adj_Shelf_Setback])
        shelf_holes.z_dim('Height',[Height])
        shelf_holes.prompt('Hide','IF(Adj_Shelf_Qty>0,False,True)',[Adj_Shelf_Qty])
        shelf_holes.prompt('Space From Bottom','Space_From_Bottom',[Space_From_Bottom])
        shelf_holes.prompt('Space From Top','Space_From_Top',[Space_From_Top])
        shelf_holes.prompt('Space From Front','Space_From_Front',[Space_From_Front])
        shelf_holes.prompt('Space From Rear','Space_From_Rear',[Space_From_Rear])
        shelf_holes.prompt('Shelf Hole Spacing','Shelf_Hole_Spacing',[Shelf_Hole_Spacing])
        
    def add_fixed_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Fixed_Shelf_Qty = self.get_var("Fixed Shelf Qty")
        Fixed_Shelf_Setback = self.get_var("Fixed Shelf Setback")
        Fixed_Shelf_Thickness = self.get_var("Fixed Shelf Thickness")

        for i in range(1,6):
            spacing = '((Height-(Fixed_Shelf_Thickness*Fixed_Shelf_Qty))/(Fixed_Shelf_Qty+1))'
            fix_shelf = self.add_assembly(SHELF)
            fix_shelf.set_name("Fixed Shelf")
            fix_shelf.x_loc(value = 0)
            fix_shelf.y_loc('Depth',[Depth])
            fix_shelf.z_loc('(' + spacing + ')*IF(' + str(i) + '>Fixed_Shelf_Qty,0,' + str(i) + ')+IF(' + str(i) + '>Fixed_Shelf_Qty,0,Fixed_Shelf_Thickness*' + str(i - 1) + ')',
                            [Height,Fixed_Shelf_Thickness,Fixed_Shelf_Qty])
            fix_shelf.x_rot(value = 0)
            fix_shelf.y_rot(value = 0)
            fix_shelf.z_rot(value = 0)
            fix_shelf.x_dim('Width',[Width])
            fix_shelf.y_dim('-Depth+Fixed_Shelf_Setback',[Depth,Fixed_Shelf_Setback])
            fix_shelf.z_dim('Fixed_Shelf_Thickness',[Fixed_Shelf_Thickness])
            fix_shelf.prompt('Hide','IF(' + str(i) + '>Fixed_Shelf_Qty,True,False)',[Fixed_Shelf_Qty])
            fix_shelf.cutpart("Cabinet_Shelf")
            fix_shelf.edgebanding('Cabinet_Interior_Edges',l1 = True)
            cabinet_machining.add_drilling(fix_shelf)
            
    def draw(self):
        self.create_assembly()
        
        self.add_common_prompts()
        
        if self.add_adjustable_shelves:
            self.add_adj_prompts()
            self.add_adjustable_shelves()
            self.add_adjustable_shelf_holes()
            
        if self.add_fixed_shelves:
            self.add_fixed_prompts()
            self.add_fixed_shelves()
            
        if self.add_adjustable_shelves and self.add_fixed_shelves:
            self.add_advanced_frameless_prompts()
            
        self.update()
        
class Dividers(fd_types.Assembly):
    
    library_name = "Cabinet Interiors"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".interior_prompts"
    mirror_y = False
    
    carcass_type = "" # {Base, Tall, Upper, Sink, Suspended}
    open_name = ""
    shelf_qty = 1
    add_adjustable_shelves = True
    add_fixed_shelves = False
    
    def add_common_prompts(self):
        self.add_tab(name='Interior Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')

        self.add_prompt(name="Fixed Shelf Qty",prompt_type='QUANTITY',value=self.shelf_qty,tab_index=0)
        self.add_prompt(name="Divider Qty Per Row",prompt_type='QUANTITY',value=2,tab_index=0)
        self.add_prompt(name="Divider Setback",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=0)
        
        self.add_prompt(name="Shelf Setback",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Divider Thickness",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=1)

        self.add_prompt(name="Edgebanding Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
    
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        
        self.prompt('Divider Thickness','THICKNESS(sgi,"Cabinet_Divider' + self.open_name +'")',[sgi])
        self.prompt('Shelf Thickness','THICKNESS(sgi,"Cabinet_Shelf' + self.open_name +'")',[sgi])
        self.prompt('Edgebanding Thickness','EDGE_THICKNESS(sgi,"Cabinet_Interior_Edges' + self.open_name + '")',[sgi])
    
    def add_dividers(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Shelf_Setback = self.get_var('Shelf Setback')
        Divider_Setback = self.get_var('Divider Setback')
        Divider_Thickness = self.get_var('Divider Thickness')
        Fixed_Shelf_Qty = self.get_var('Fixed Shelf Qty')
        Divider_Qty_Per_Row = self.get_var('Divider Qty Per Row')

        divider = self.add_assembly(DIVIDER)
        divider.set_name("Divider")
        divider.x_loc("Width-(Width/(Divider_Qty_Per_Row+1))+(Divider_Thickness/2)",[Width,Divider_Thickness,Divider_Qty_Per_Row])
        divider.y_loc("Depth",[Depth])
        divider.z_loc(value = 0)
        divider.x_rot(value = 0)
        divider.y_rot(value = -90)
        divider.z_rot(value = 0)
        divider.x_dim("(Height-(Shelf_Thickness*Fixed_Shelf_Qty))/(Fixed_Shelf_Qty+1)",[Height,Shelf_Thickness,Fixed_Shelf_Qty])
        divider.y_dim("(Depth*-1)+Divider_Setback+Shelf_Setback",[Depth,Divider_Setback,Shelf_Setback])
        divider.z_dim("Divider_Thickness",[Divider_Thickness])
        divider.prompt('Z Quantity','Divider_Qty_Per_Row',[Divider_Qty_Per_Row])
        divider.prompt('Z Offset','Width/(Divider_Qty_Per_Row+1)',[Width,Divider_Qty_Per_Row])
        divider.prompt('X Quantity','Fixed_Shelf_Qty+1',[Fixed_Shelf_Qty])
        divider.prompt('X Offset','Height/(Fixed_Shelf_Qty+1)+(Shelf_Thickness/(Fixed_Shelf_Qty+1))',[Height,Fixed_Shelf_Qty,Shelf_Thickness])
        divider.cutpart("Cabinet_Divider")
        divider.edgebanding('Cabinet_Interior_Edges',l1 = True)
        
    def add_fixed_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Fixed_Shelf_Qty = self.get_var("Fixed Shelf Qty")
        Shelf_Setback = self.get_var("Shelf Setback")
        Shelf_Thickness = self.get_var("Shelf Thickness")

        fix_shelf = self.add_assembly(SHELF)
        fix_shelf.set_name("Fixed Shelf")
        fix_shelf.y_loc("Depth",[Depth])
        fix_shelf.z_loc("(Height-(Shelf_Thickness*Fixed_Shelf_Qty))/(Fixed_Shelf_Qty+1)",[Height,Shelf_Thickness,Fixed_Shelf_Qty])
        fix_shelf.x_dim("Width",[Width])
        fix_shelf.y_dim("(Depth*-1)+Shelf_Setback",[Depth,Shelf_Setback])
        fix_shelf.z_dim("Shelf_Thickness",[Shelf_Thickness])
        fix_shelf.prompt('Hide','IF(Fixed_Shelf_Qty==0,True,False)',[Fixed_Shelf_Qty])
        fix_shelf.prompt('Z Quantity','Fixed_Shelf_Qty',[Fixed_Shelf_Qty])
        fix_shelf.prompt('Z Offset','Height/(Fixed_Shelf_Qty+1)+(Shelf_Thickness/(Fixed_Shelf_Qty+1))',[Height,Fixed_Shelf_Qty,Shelf_Thickness])
        fix_shelf.cutpart("Cabinet_Shelf")
        fix_shelf.edgebanding('Cabinet_Interior_Edges',l1 = True)

    def draw(self):
        self.create_assembly()
        
        self.add_common_prompts()
        self.add_fixed_shelves()
        self.add_dividers()
        
        self.update()
        
class Divisions(fd_types.Assembly):
    
    library_name = "Cabinet Interiors"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".interior_prompts"
    mirror_y = False
    
    carcass_type = "" # Base, Tall, Upper, Sink, Suspended
    open_name = ""
    shelf_qty = 1
    add_adjustable_shelves = True
    add_fixed_shelves = False
    
    def add_common_prompts(self):
        self.add_tab(name='Interior Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')

        self.add_prompt(name="Division Qty",prompt_type='QUANTITY',value=2,tab_index=0)
        self.add_prompt(name="Division Setback",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=0)
        self.add_prompt(name="Adj Shelf Rows",prompt_type='QUANTITY',value=2,tab_index=0)
        self.add_prompt(name="Fixed Shelf Rows",prompt_type='QUANTITY',value=0,tab_index=0)
        
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Shelf Setback",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=1)
        self.add_prompt(name="Shelf Holes Space From Bottom",prompt_type='DISTANCE',value=unit.inch(2.5),tab_index=1)
        self.add_prompt(name="Shelf Holes Space From Top",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Shelf Holes Front Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Shelf Holes Rear Setback",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Adjustable Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Fixed Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Shelf Clip Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=1)
        self.add_prompt(name="Shelf Hole Spacing",prompt_type='DISTANCE',value=unit.inch(1.25),tab_index=1)
        self.add_prompt(name="Shelf Pin Quantity",prompt_type='QUANTITY',value=0,tab_index=1)
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        Adj_Shelf_Rows = self.get_var('Adj Shelf Rows')
        Division_Qty = self.get_var('Division Qty')
        
        self.prompt('Shelf Pin Quantity','(Adj_Shelf_Rows*Division_Qty)*4',[Adj_Shelf_Rows,Division_Qty])
        self.prompt('Division Thickness','THICKNESS(sgi,"Cabinet_Division' + self.open_name +'")',[sgi])
        self.prompt('Fixed Shelf Thickness','THICKNESS(sgi,"Cabinet_Shelf' + self.open_name +'")',[sgi])
        self.prompt('Adjustable Shelf Thickness','THICKNESS(sgi,"Cabinet_Shelf' + self.open_name +'")',[sgi])
    
    def add_divisions(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Division_Qty = self.get_var('Division Qty')   
        Division_Thickness = self.get_var('Division Thickness')  
        Division_Setback = self.get_var('Division Setback') 
        
        #LOGIC
        division = self.add_assembly(DIVISION)
        division.set_name("Division")
        division.x_loc("Width-(Width-(Division_Thickness*Division_Qty))/(Division_Qty+1)",[Width,Division_Thickness,Division_Qty])
        division.y_loc("Depth",[Depth])
        division.z_loc(value = 0)
        division.x_rot(value = 0)
        division.y_rot(value = -90)
        division.z_rot(value = 0)
        division.x_dim("Height",[Height])
        division.y_dim("(Depth*-1)+Division_Setback",[Depth,Division_Setback])
        division.z_dim("Division_Thickness",[Division_Thickness])
        division.prompt('Hide','IF(Division_Qty==0,True,False)',[Division_Qty])
        division.prompt('Z Quantity','Division_Qty',[Division_Qty])
        division.prompt('Z Offset','((Width-(Division_Thickness*Division_Qty))/(Division_Qty+1))+Division_Thickness',[Division_Qty,Width,Division_Thickness])
        division.cutpart("Cabinet_Division")
        division.edgebanding('Cabinet_Interior_Edges',l1 = True)

    def add_fixed_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Division_Qty = self.get_var('Division Qty')   
        Division_Thickness = self.get_var('Division Thickness')  
        Division_Setback = self.get_var('Division Setback') 
        Shelf_Setback = self.get_var('Shelf Setback')
        Fixed_Shelf_Rows = self.get_var('Fixed Shelf Rows')
        Fixed_Shelf_Thickness = self.get_var('Fixed Shelf Thickness')
        
        fix_shelf = self.add_assembly(SHELF)
        fix_shelf.set_name("Fixed Shelf")
        fix_shelf.x_loc(value = 0)
        fix_shelf.y_loc("Depth",[Depth]) 
        fix_shelf.z_loc("(Height-(Fixed_Shelf_Thickness*Fixed_Shelf_Rows))/(Fixed_Shelf_Rows+1)",[Height,Fixed_Shelf_Thickness,Fixed_Shelf_Rows]) 
        fix_shelf.x_rot(value = 0)
        fix_shelf.y_rot(value = 0)
        fix_shelf.z_rot(value = 0)
        fix_shelf.x_dim("(Width-(Division_Thickness*Division_Qty))/(Division_Qty+1)",[Width,Division_Qty,Division_Thickness]) 
        fix_shelf.y_dim("(Depth*-1)+Shelf_Setback+Division_Setback",[Shelf_Setback,Depth,Division_Setback]) 
        fix_shelf.z_dim("Fixed_Shelf_Thickness",[Fixed_Shelf_Thickness]) 
        fix_shelf.prompt('Hide','IF(Fixed_Shelf_Rows==0,True,False)',[Fixed_Shelf_Rows])
        fix_shelf.prompt('Z Quantity','Fixed_Shelf_Rows',[Fixed_Shelf_Rows])
        fix_shelf.prompt('Z Offset','Height/(Fixed_Shelf_Rows+1)+(Fixed_Shelf_Thickness/(Fixed_Shelf_Rows+1))',[Height,Fixed_Shelf_Thickness,Fixed_Shelf_Rows])
        fix_shelf.prompt('X Quantity','Division_Qty+1',[Division_Qty])
        fix_shelf.prompt('X Offset','((Width-(Division_Thickness*Division_Qty))/(Division_Qty+1))+Division_Thickness',[Width,Division_Qty,Division_Thickness])
        fix_shelf.cutpart("Cabinet_Shelf")
        fix_shelf.edgebanding('Cabinet_Interior_Edges',l1 = True)

    def add_adj_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Division_Qty = self.get_var('Division Qty')   
        Division_Thickness = self.get_var('Division Thickness')  
        Division_Setback = self.get_var('Division Setback') 
        Shelf_Clip_Gap = self.get_var('Shelf Clip Gap') 
        Shelf_Setback = self.get_var('Shelf Setback')
        Adj_Shelf_Rows = self.get_var('Adj Shelf Rows')
        Adjustable_Shelf_Thickness = self.get_var('Adjustable Shelf Thickness')
        
        adj_shelf = self.add_assembly(SHELF)
        adj_shelf.set_name("Adjustable Shelf")
        adj_shelf.x_loc("Shelf_Clip_Gap",[Shelf_Clip_Gap])
        adj_shelf.y_loc("Depth",[Depth])
        adj_shelf.z_loc("(Height-(Adjustable_Shelf_Thickness*Adj_Shelf_Rows))/(Adj_Shelf_Rows+1)",[Height,Adjustable_Shelf_Thickness,Adj_Shelf_Rows])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim("(Width-(Division_Thickness*Division_Qty)-((Shelf_Clip_Gap*2)*(Division_Qty+1)))/(Division_Qty+1)",[Width,Division_Qty,Division_Thickness,Shelf_Clip_Gap])
        adj_shelf.y_dim("(Depth*-1)+Shelf_Setback+Division_Setback",[Depth,Shelf_Setback,Division_Setback])
        adj_shelf.z_dim("Adjustable_Shelf_Thickness",[Adjustable_Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(Adj_Shelf_Rows==0,True,False)',[Adj_Shelf_Rows])
        adj_shelf.prompt('Z Quantity','Adj_Shelf_Rows',[Adj_Shelf_Rows])
        adj_shelf.prompt('Z Offset','Height/(Adj_Shelf_Rows+1)+(Adjustable_Shelf_Thickness/(Adj_Shelf_Rows+1))',[Adj_Shelf_Rows,Height,Adjustable_Shelf_Thickness])
        adj_shelf.prompt('X Quantity','Division_Qty+1',[Division_Qty])
        adj_shelf.prompt('X Offset','((Width-(Division_Thickness*Division_Qty)-((Shelf_Clip_Gap*2)*(Division_Qty+1)))/(Division_Qty+1))+(Shelf_Clip_Gap*2)+Division_Thickness',[Width,Division_Thickness,Division_Qty,Shelf_Clip_Gap])
        adj_shelf.cutpart("Cabinet_Shelf")
        adj_shelf.edgebanding('Cabinet_Interior_Edges',l1 = True, w1 = True, l2 = True, w2 = True)

    def add_adj_shelf_machining(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Division_Qty = self.get_var('Division Qty')   
        Division_Thickness = self.get_var('Division Thickness')  
        Division_Setback = self.get_var('Division Setback') 
        Shelf_Setback = self.get_var('Shelf Setback')
        Adj_Shelf_Rows = self.get_var('Adj Shelf Rows')

        holes = self.add_assembly(ADJ_MACHINING)
        holes.set_name("Adjustable Shelf Holes")
        holes.x_loc(value = 0)
        holes.y_loc("Division_Setback+Shelf_Setback",[Division_Setback,Shelf_Setback])
        holes.z_loc(value = 0)
        holes.x_rot(value = 0)
        holes.y_rot(value = 0)
        holes.z_rot(value = 0)
        holes.x_dim("(Width-(Division_Thickness*Division_Qty))/(Division_Qty+1)",[Width,Division_Thickness,Division_Qty])
        holes.y_dim("fabs(Depth)-Division_Setback-Shelf_Setback",[Depth,Division_Setback,Shelf_Setback])
        holes.z_dim("Height",[Height])
        holes.prompt('Hide','IF(Adj_Shelf_Rows==0,True,False)',[Adj_Shelf_Rows])
        holes.prompt('Opening Quantity','Division_Qty+1',[Division_Qty])
        holes.prompt('Opening X Offset','(Width-(Division_Thickness*Division_Qty))/(Division_Qty+1)+Division_Thickness',[Width,Division_Thickness,Division_Qty])

    def draw(self):
        self.create_assembly()
        
        self.add_common_prompts()
        self.add_divisions()
        self.add_fixed_shelves()
        self.add_adj_shelves()
#         self.add_adj_shelf_machining()
        
        self.update()
        
class Rollouts(fd_types.Assembly):
    
    library_name = "Cabinet Interiors"
    type_assembly = "INSERT"
    placement_type = "INTERIOR"
    property_id = cabinet_properties.LIBRARY_NAME_SPACE + ".interior_prompts"
    mirror_y = False
    
    rollout_qty = 3
    
    def draw(self):
        self.create_assembly()

        self.add_tab(name='Rollout Options',tab_type='VISIBLE')
        
        self.add_prompt(name="Rollout Quantity",
                        prompt_type='QUANTITY',
                        value=self.rollout_qty,
                        tab_index=0)
        
        self.add_prompt(name="Rollout 1 Z Dim",
                        prompt_type='DISTANCE',
                        value=unit.inch(4),
                        tab_index=0)
        
        self.add_prompt(name="Rollout 2 Z Dim",
                        prompt_type='DISTANCE',
                        value=unit.inch(4),
                        tab_index=0)
        
        self.add_prompt(name="Rollout 3 Z Dim",
                        prompt_type='DISTANCE',
                        value=unit.inch(4),
                        tab_index=0)
        
        self.add_prompt(name="Rollout 4 Z Dim",
                        prompt_type='DISTANCE',
                        value=unit.inch(4),
                        tab_index=0)
        
        self.add_prompt(name="Bottom Gap",
                        prompt_type='DISTANCE',
                        value=unit.inch(1.7),
                        tab_index=0)
        
        self.add_prompt(name="Drawer Box Slide Gap",
                        prompt_type='DISTANCE',
                        value=unit.inch(2),
                        tab_index=0)

        self.add_prompt(name="Rollout Setback",
                        prompt_type='DISTANCE',
                        value=unit.inch(.5),
                        tab_index=0)
        
        self.add_prompt(name="Distance Between Rollouts",
                        prompt_type='DISTANCE',
                        value=unit.inch(2),
                        tab_index=0)

        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Rollout_1_Z_Dim = self.get_var('Rollout 1 Z Dim')
        Rollout_2_Z_Dim = self.get_var('Rollout 2 Z Dim')
        Rollout_3_Z_Dim = self.get_var('Rollout 3 Z Dim')
        Rollout_4_Z_Dim = self.get_var('Rollout 4 Z Dim')
        Bottom_Gap = self.get_var("Bottom Gap")
        Distance_Between_Rollouts = self.get_var("Distance Between Rollouts")
        Rollout_Quantity = self.get_var("Rollout Quantity")
        Rollout_Setback = self.get_var("Rollout Setback")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        
        rollout_1 = drawer_boxes.Wood_Drawer_Box()
        rollout_1.draw()
        rollout_1.obj_bp.parent = self.obj_bp
        rollout_1.set_name("Rollout 1")
        rollout_1.x_loc('Distance_Between_Rollouts',[Distance_Between_Rollouts])
        rollout_1.y_loc('Rollout_Setback',[Rollout_Setback])
        rollout_1.z_loc('Bottom_Gap',[Bottom_Gap])
        rollout_1.x_rot(value = 0)
        rollout_1.y_rot(value = 0)
        rollout_1.z_rot(value = 0)
        rollout_1.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
        rollout_1.y_dim('Depth',[Depth])
        rollout_1.z_dim('Rollout_1_Z_Dim',[Rollout_1_Z_Dim])
        
        rollout_2 = drawer_boxes.Wood_Drawer_Box()
        rollout_2.draw()
        rollout_2.obj_bp.parent = self.obj_bp
        rollout_2.set_name("Rollout 2")
        rollout_2.x_loc('Distance_Between_Rollouts',[Distance_Between_Rollouts])
        rollout_2.y_loc('Rollout_Setback',[Rollout_Setback])
        rollout_2.z_loc('Bottom_Gap+Rollout_1_Z_Dim+Distance_Between_Rollouts',[Bottom_Gap,Rollout_1_Z_Dim,Distance_Between_Rollouts])
        rollout_2.x_rot(value = 0)
        rollout_2.y_rot(value = 0)
        rollout_2.z_rot(value = 0)
        rollout_2.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
        rollout_2.y_dim('Depth',[Depth])
        rollout_2.z_dim('Rollout_2_Z_Dim',[Rollout_2_Z_Dim])
        rollout_2.prompt('Hide','IF(Rollout_Quantity>1,False,True)',[Rollout_Quantity])
        
        rollout_3 = drawer_boxes.Wood_Drawer_Box()
        rollout_3.draw()
        rollout_3.obj_bp.parent = self.obj_bp
        rollout_3.set_name("Rollout 3")
        rollout_3.x_loc('Distance_Between_Rollouts',[Distance_Between_Rollouts])
        rollout_3.y_loc('Rollout_Setback',[Rollout_Setback])
        rollout_3.z_loc('Bottom_Gap+Rollout_1_Z_Dim+Rollout_2_Z_Dim+(Distance_Between_Rollouts*2)',[Bottom_Gap,Rollout_1_Z_Dim,Rollout_2_Z_Dim,Distance_Between_Rollouts])
        rollout_3.x_rot(value = 0)
        rollout_3.y_rot(value = 0)
        rollout_3.z_rot(value = 0)
        rollout_3.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
        rollout_3.y_dim('Depth',[Depth])
        rollout_3.z_dim('Rollout_3_Z_Dim',[Rollout_3_Z_Dim])
        rollout_3.prompt('Hide','IF(Rollout_Quantity>2,False,True)',[Rollout_Quantity])

        rollout_4 = drawer_boxes.Wood_Drawer_Box()
        rollout_4.draw()
        rollout_4.obj_bp.parent = self.obj_bp
        rollout_4.set_name("Rollout 3")
        rollout_4.x_loc('Distance_Between_Rollouts',[Distance_Between_Rollouts])
        rollout_4.y_loc('Rollout_Setback',[Rollout_Setback])
        rollout_4.z_loc('Bottom_Gap+Rollout_1_Z_Dim+Rollout_2_Z_Dim+Rollout_3_Z_Dim+(Distance_Between_Rollouts*3)',[Bottom_Gap,Rollout_1_Z_Dim,Rollout_2_Z_Dim,Rollout_3_Z_Dim,Distance_Between_Rollouts])
        rollout_4.x_rot(value = 0)
        rollout_4.y_rot(value = 0)
        rollout_4.z_rot(value = 0)
        rollout_4.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
        rollout_4.y_dim('Depth',[Depth])
        rollout_4.z_dim('Rollout_4_Z_Dim',[Rollout_4_Z_Dim])
        rollout_4.prompt('Hide','IF(Rollout_Quantity>3,False,True)',[Rollout_Quantity])
        
        self.update()
        
#---------INSERTS
        
class INSERT_Simple_Shelves(Simple_Shelves):
    
    def __init__(self):
        self.category_name = "Standard"
        self.assembly_name = "Simple Shelves"
        self.carcass_type = "Base"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        self.shelf_qty = 1        
        
class INSERT_Shelves(Shelves):
    
    def __init__(self):
        self.category_name = "Standard"
        self.assembly_name = "Shelves"
        self.carcass_type = "Base"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        self.shelf_qty = 1
        
class INSERT_Base_Dividers(Dividers):
    
    def __init__(self):
        self.category_name = "Standard"
        self.assembly_name = "Dividers"
        self.carcass_type = "Base"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        self.shelf_qty = 1

class INSERT_Base_Divisions(Divisions):
    
    def __init__(self):
        self.category_name = "Standard"
        self.assembly_name = "Divisions"
        self.carcass_type = "Base"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        self.shelf_qty = 1

class INSERT_Rollouts(Rollouts):
    
    def __init__(self):
        self.category_name = "Standard"
        self.assembly_name = "Rollouts"
        self.carcass_type = "Base"
        self.width = unit.inch(18)
        self.height = unit.inch(34)
        self.depth = unit.inch(23)
        self.rollout_qty = 2
