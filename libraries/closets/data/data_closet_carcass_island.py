import math
from snap.sn_unit import inch

import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty

from snap import sn_types, sn_unit, sn_utils
from os import path
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts
from ..common import common_lists
from . import data_base_assembly


def update_closet_height(self,context):
    ''' EVENT changes height for all closet openings
    '''
    obj_product_bp = sn_utils.get_bp(context.active_object,'PRODUCT')
    product = sn_types.Assembly(obj_product_bp)
    product.obj_z.location.z = sn_unit.millimeter(float(self.height))


class Closet_Island_Carcass(sn_types.Assembly):
    
    type_assembly = "PRODUCT"
    id_prompt = "sn_closets.island_openings"
    plan_draw_id = "sn_closets.draw_plan"
    show_in_library = True
    category_name = ""
    
    opening_qty = 4
    calculator = None
    is_double_sided = False
    
    def __init__(self):
        defaults = bpy.context.scene.sn_closets.closet_defaults
        self.width = sn_unit.inch(18) * self.opening_qty
        self.height = sn_unit.millimeter(float(defaults.island_panel_height))
        if self.is_double_sided:
            self.depth = defaults.panel_depth * 2 
        else:
            self.depth = defaults.panel_depth
    
    def add_opening_prompts(self):
        for i in range(1, self.opening_qty + 1):
            calc_prompt = self.calculator.add_calculator_prompt("Opening " + str(i) + " Width")
            calc_prompt.equal = True            
            self.add_prompt("Opening " + str(i) + " Depth", 'DISTANCE', self.depth)            
        
    def add_island_prompts(self):
        props = bpy.context.scene.sn_closets.closet_defaults
        
        self.add_prompt("Left Against Wall", 'CHECKBOX', False)
        self.add_prompt("Right Against Wall", 'CHECKBOX', False)
        self.add_prompt("Exposed Back", 'CHECKBOX', True)
        self.add_prompt("No Countertop", 'CHECKBOX', False)
        self.add_prompt("Add TK Skin", 'CHECKBOX', False)
        self.add_prompt("TK Skin Thickness", 'DISTANCE', sn_unit.inch(0.25))

        if self.is_double_sided:
            self.add_prompt("Depth 1", 'DISTANCE', props.panel_depth)
            self.add_prompt("Depth 2", 'DISTANCE', props.panel_depth)
            
            Depth_1 = self.get_prompt('Depth 1').get_var()
            Depth_2 = self.get_prompt('Depth 2').get_var()
            Back_Thickness = self.get_prompt('Back Thickness').get_var()
            Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
            
            self.dim_y('(Depth_1+Depth_2+Panel_Thickness)*-1',[Depth_1,Depth_2,Panel_Thickness])
            
    def add_sides(self):
        props = bpy.context.scene.sn_closets   
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var('Toe_Kick_Height')
        Product_Height = self.obj_z.snap.get_var('location.z','Product_Height')
        Product_Width = self.obj_x.snap.get_var('location.x','Product_Width')
        Product_Depth = self.obj_y.snap.get_var('location.y','Product_Depth')
        Left_Side_Thickness = self.get_prompt('Left Side Thickness').get_var()
        Right_Side_Thickness = self.get_prompt('Right Side Thickness').get_var()
        #Add_Backing = self.get_prompt('Add Backing').get_var()
        Back_Thickness = self.get_prompt('Back Thickness').get_var()

        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()

        left_side = common_parts.add_panel(self)
        left_side.obj_bp['PARTITION_NUMBER'] = 0
        left_side.dim_x('Product_Height',[Product_Height])
        left_side.dim_y('Product_Depth',[Product_Depth])
        left_side.dim_z('-Left_Side_Thickness',[Left_Side_Thickness])
        #left_side.loc_y('IF(Add_Backing,-Panel_Thickness,0)',[Add_Backing,Panel_Thickness])
        left_side.loc_z('Toe_Kick_Height',[Toe_Kick_Height])
        left_side.rot_y(value=math.radians(-90))
                
        right_side = common_parts.add_panel(self)
        right_side.obj_bp['PARTITION_NUMBER'] = self.opening_qty
        right_side.dim_x('Product_Height',[Product_Height])
        right_side.dim_y('Product_Depth',[Product_Depth])
        right_side.dim_z('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.loc_x('Product_Width',[Product_Width])
        #right_side.loc_y('IF(Add_Backing,-Panel_Thickness,0)',[Add_Backing,Panel_Thickness])
        right_side.loc_z('Toe_Kick_Height',[Toe_Kick_Height])
        right_side.rot_y(value=math.radians(-90))

    def add_panel(self,index,previous_panel):                
        PH = self.obj_z.snap.get_var('location.z','PH')
        PD = self.obj_y.snap.get_var('location.y','PD')
        width_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(index - 1)))
        Width = eval("width_prompt.get_var(self.calculator.name, 'Width')".format(str(index))) 
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var()
        
        panel = common_parts.add_panel(self)
        if previous_panel:
            Prev_Panel_X = previous_panel.obj_bp.snap.get_var("location.x", 'Prev_Panel_X')
            Left_Side_Thickness = self.get_prompt('Left Side Thickness').get_var()
            panel.loc_x('Prev_Panel_X+Panel_Thickness+Width',[Prev_Panel_X,Panel_Thickness,Width])
        else:
            Left_Side_Thickness = self.get_prompt('Left Side Thickness').get_var()
            panel.loc_x('Left_Side_Thickness+Width+Panel_Thickness',[Left_Side_Thickness,Width,Panel_Thickness])

        panel.loc_z('Toe_Kick_Height',[Toe_Kick_Height])
        panel.rot_y(value=math.radians(-90))
        panel.dim_x('PH',[PH]) 
        panel.dim_y('PD',[PD])
        panel.dim_z('Panel_Thickness',[Panel_Thickness])
        return panel
        
    def add_shelf(self,i,panel,is_top=False,is_rear=False):
        Product_Height = self.obj_z.snap.get_var('location.z','Product_Height')
        Product_Depth = self.obj_y.snap.get_var('location.y','Product_Depth')
        width_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(self.calculator.name, 'Width')".format(str(i)))        
        # Depth_1 = self.get_prompt('Depth 1').get_var()
        # Depth_2 = self.get_prompt('Depth 2').get_var()
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var()
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var()

        shelf = common_parts.add_shelf(self)
        shelf.get_prompt("Is Locked Shelf").set_value(value=True)
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
            shelf.loc_x('X_Loc', [X_Loc])
        else:
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            shelf.loc_x('X_Loc', [X_Loc])
        
        shelf.dim_y("Product_Depth",[Product_Depth])
        
        if is_top:
            shelf.loc_z('Product_Height+Toe_Kick_Height',[Product_Height,Toe_Kick_Height])
            shelf.dim_z('-Shelf_Thickness',[Shelf_Thickness])
        else:
            shelf.loc_z('Toe_Kick_Height',[Toe_Kick_Height])
            shelf.dim_z('Shelf_Thickness',[Shelf_Thickness])

        shelf.dim_x('Width',[Width])
        
        if is_top:
            shelf.get_prompt("Drill On Top").set_value(value=True)
        else:
            shelf.get_prompt("Drill On Top").set_value(value=False)
    
    def add_toe_kick(self,i,panel,is_rear=False):
        Product_Depth = self.obj_y.snap.get_var('location.y','Product_Depth')
        width_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(self.calculator.name, 'Width')".format(str(i)))
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')

        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        kick = common_parts.add_toe_kick(self)
        kick.dim_x("Width",[Width])
        kick.dim_y('-Toe_Kick_Height',[Toe_Kick_Height,Shelf_Thickness])
        kick.loc_x('X_Loc',[X_Loc])
        if is_rear:
            kick.loc_y('-Toe_Kick_Setback',[Product_Depth,Toe_Kick_Setback])
            kick.dim_z('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        else:
            kick.loc_y('Product_Depth+Toe_Kick_Setback',[Product_Depth,Toe_Kick_Setback])
            kick.dim_z('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        kick.rot_x(value=math.radians(-90))
        
    def add_closet_opening(self,i,panel,is_rear=False):
        props = bpy.context.scene.sn_closets.closet_defaults
        
        Product_Height = self.obj_z.snap.get_var('location.z','Product_Height')
        Product_Depth = self.obj_y.snap.get_var('location.y','Product_Depth')
        width_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(self.calculator.name, 'Width')".format(str(i)))        
        Shelf_Thickness = self.get_prompt('Shelf Thickness').get_var()
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var()
        
        opening = common_parts.add_section_opening(self)
        
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
        else:
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')

        opening.loc_z('Toe_Kick_Height+Shelf_Thickness',[Toe_Kick_Height,Shelf_Thickness])
        if is_rear:
            opening.loc_x('X_Loc+Width',[X_Loc,Width])
            opening.rot_z(value=math.radians(180))
            if self.is_double_sided:
                Depth_1 = self.get_prompt('Depth 1').get_var()
                opening.dim_y("Depth_1",[Depth_1])
        else:
            opening.loc_x('X_Loc',[X_Loc])
            opening.loc_y('Product_Depth',[Product_Depth])
            if self.is_double_sided:
                Depth_2 = self.get_prompt('Depth 2').get_var()
                opening.dim_y("Depth_2",[Depth_2])
            else:
                opening.dim_y("fabs(Product_Depth)",[Product_Depth])
        opening.dim_x('Width',[Width])
        
        if props.use_plant_on_top:
            opening.dim_z('Product_Height-Shelf_Thickness',[Product_Height,Shelf_Thickness])
        else:
            opening.dim_z('Product_Height-(Shelf_Thickness*2)',[Product_Height,Shelf_Thickness])
        
    def add_inside_dimension(self,i,panel):
        width_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(self.calculator.name, 'Width')".format(str(i)))
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            
        dim = sn_types.Dimension()
        dim.parent(self.obj_bp)
        dim.start_z(value = sn_unit.inch(-4))
        dim.start_y(value = sn_unit.inch(4))
        if panel:
            dim.start_x('X_Loc',[X_Loc])
        else:
            dim.start_x('X_Loc+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
        dim.end_x('Width',[Width])
        dim.set_color('IF(Width>INCH(42),3,0)',[Width])
    
    def add_thick_back(self):
        Product_Height = self.obj_z.snap.get_var('location.z','Product_Height')
        Product_Width = self.obj_x.snap.get_var('location.x','Product_Width')
        Back_Thickness = self.get_prompt('Back Thickness').get_var()
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var()
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        
        backing = common_parts.add_back(self)
        backing.loc_z('Toe_Kick_Height',[Toe_Kick_Height])
        backing.rot_x(value=math.radians(90))
        backing.dim_x('Product_Width',[Product_Width])
        backing.dim_y("Product_Height",[Product_Height])
        backing.dim_z('-Panel_Thickness',[Panel_Thickness])
        
    def add_double_sided_back(self,i,panel):
        width_prompt = eval("self.calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
        Width = eval("width_prompt.get_var(self.calculator.name, 'Width')".format(str(i)))
        Product_Height = self.obj_z.snap.get_var('location.z','Product_Height')
        Product_Width = self.obj_x.snap.get_var('location.x','Product_Width')
        Back_Thickness = self.get_prompt('Back Thickness').get_var()
        Depth_1 = self.get_prompt('Depth 1').get_var()
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var()
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        
        if panel:
            X_Loc = panel.obj_bp.snap.get_var('location.x','X_Loc')
        else:
            X_Loc = self.get_prompt('Left Side Thickness').get_var('X_Loc')
            
        backing = common_parts.add_back(self)
        backing.loc_x('X_Loc',[X_Loc])
        backing.loc_y('-Depth_1',[Depth_1])
        backing.loc_z('Toe_Kick_Height + Panel_Thickness',[Toe_Kick_Height,Panel_Thickness])
        backing.rot_x(value=math.radians(90))
        backing.dim_x('Width',[Width])
        backing.dim_y("Product_Height-(Panel_Thickness*2)",[Product_Height,Panel_Thickness])
        backing.dim_z('Panel_Thickness',[Panel_Thickness])
        
    def add_counter_top(self):
        dim_x = self.obj_x.snap.get_var('location.x', 'dim_x')
        dim_z = self.obj_z.snap.get_var('location.z', 'dim_z')
        dim_y = self.obj_y.snap.get_var('location.y', 'dim_y')
        Deck_Overhang = self.get_prompt('Deck Overhang').get_var()
        Side_Deck_Overhang = self.get_prompt("Side Deck Overhang").get_var()
        Deck_Thickness = self.get_prompt('Deck Thickness').get_var()
        Countertop_Type = self.get_prompt('Countertop Type').get_var()
        Left_Against_Wall = self.get_prompt('Left Against Wall').get_var()
        Right_Against_Wall = self.get_prompt('Right Against Wall').get_var()
        Exposed_Back = self.get_prompt('Exposed Back').get_var()
        Toe_Kick_Height = self.get_prompt('Toe Kick Height').get_var()
        No_Countertop = self.get_prompt('No Countertop').get_var()     
        
        granite_ctop = common_parts.add_countertop(self)
        granite_ctop.set_name("Granite Countertop")
        granite_ctop.loc_x('IF(Left_Against_Wall,0,-Side_Deck_Overhang)',[Left_Against_Wall,Side_Deck_Overhang])
        granite_ctop.loc_y('Deck_Overhang',[Deck_Overhang])
        granite_ctop.loc_z('dim_z+Toe_Kick_Height',[dim_z,Toe_Kick_Height])
        granite_ctop.dim_x('dim_x+IF(Left_Against_Wall,0,Side_Deck_Overhang)+IF(Right_Against_Wall,0,Side_Deck_Overhang)',
                   [dim_x,Side_Deck_Overhang,Left_Against_Wall,Right_Against_Wall])
        granite_ctop.dim_y('dim_y-Deck_Overhang*2',[dim_y,Deck_Overhang])
        granite_ctop.dim_z('Deck_Thickness',[Deck_Thickness])
        granite_ctop.get_prompt("Hide").set_formula(
            "IF(No_Countertop,True,IF(Countertop_Type==2,False,True)) or Hide",[Countertop_Type,No_Countertop, self.hide_var])
                
        hpltop = common_parts.add_hpl_top(self)    
        hpltop.set_name("HPL Countertop")
        hpltop.loc_x('IF(Left_Against_Wall,0,-Side_Deck_Overhang)',[Left_Against_Wall,Side_Deck_Overhang])
        hpltop.loc_y('Deck_Overhang',[Deck_Overhang])
        hpltop.loc_z('dim_z+Toe_Kick_Height',[dim_z,Toe_Kick_Height])
        hpltop.dim_x('dim_x+IF(Left_Against_Wall,0,Side_Deck_Overhang)+IF(Right_Against_Wall,0,Side_Deck_Overhang)',
                   [dim_x,Side_Deck_Overhang,Left_Against_Wall,Right_Against_Wall])
        hpltop.dim_y('dim_y-Deck_Overhang*2',[dim_y,Deck_Overhang])
        hpltop.dim_z('Deck_Thickness',[Deck_Thickness])
        hpltop.get_prompt("Hide").set_formula("IF(No_Countertop,True,IF(Countertop_Type==1,False,True)) or Hide",[Countertop_Type,No_Countertop,self.hide_var])
        hpltop.get_prompt("Exposed Left").set_formula("IF(Left_Against_Wall,False,True)",[Left_Against_Wall])
        hpltop.get_prompt("Exposed Right").set_formula("IF(Right_Against_Wall,False,True)",[Right_Against_Wall])
        hpltop.get_prompt("Exposed Back").set_formula("Exposed_Back",[Exposed_Back])

        melamine_deck = common_parts.add_plant_on_top(self)  
        melamine_deck.obj_bp["IS_BP_COUNTERTOP"] = True
        melamine_deck.set_name("Melamine Countertop")
        melamine_deck.loc_x('IF(Left_Against_Wall,0,-Side_Deck_Overhang)',[Left_Against_Wall,Side_Deck_Overhang])
        melamine_deck.loc_y('Deck_Overhang',[Deck_Overhang])
        melamine_deck.loc_z('dim_z+Toe_Kick_Height',[dim_z,Toe_Kick_Height])
        melamine_deck.dim_x('dim_x+IF(Left_Against_Wall,0,Side_Deck_Overhang)+IF(Right_Against_Wall,0,Side_Deck_Overhang)',[dim_x,Side_Deck_Overhang,Left_Against_Wall,Right_Against_Wall])
        melamine_deck.dim_y('dim_y-Deck_Overhang*2',[dim_y,Deck_Overhang])
        melamine_deck.dim_z('Deck_Thickness',[Deck_Thickness])   
        melamine_deck.get_prompt("Is Countertop").set_value(value=True) 
        melamine_deck.get_prompt("Hide").set_formula(
            "IF(No_Countertop,True,IF(Countertop_Type==0,False,True)) or Hide",[Countertop_Type,No_Countertop,self.hide_var]) 
        melamine_deck.get_prompt("Exposed Left").set_formula("IF(Left_Against_Wall,False,True)",[Left_Against_Wall])
        melamine_deck.get_prompt("Exposed Right").set_formula("IF(Right_Against_Wall,False,True)",[Right_Against_Wall])
        melamine_deck.get_prompt("Exposed Back").set_formula("Exposed_Back",[Exposed_Back])
        melamine_deck.obj_bp.sn_closets.is_countertop_bp = True
        for child in melamine_deck.obj_bp.children:
            if child.snap.type_mesh == 'CUTPART':
                for mat_slot in child.snap.material_slots:
                    mat_slot.pointer_name = "Closet_Part_Edges"    
        
    def add_base_assembly(self):
        self.add_prompt("Cleat Width", 'DISTANCE', sn_unit.inch(2.5))
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Height = self.get_prompt('Toe Kick Height').get_var("Height")
        Cleat_Width = self.get_prompt('Cleat Width').get_var()
        Toe_Kick_Thickness = self.get_prompt('Toe Kick Thickness').get_var()
        Toe_Kick_Setback = self.get_prompt('Toe Kick Setback').get_var()
        # Extend_Left_Amount = self.get_prompt('Extend Left Amount').get_var()
        # Extend_Right_Amount = self.get_prompt('Extend Right Amount').get_var()
        # Extend_Depth_Amount = self.get_prompt('Extend Depth Amount').get_var()
        Add_TK_Skin = self.get_prompt('Add TK Skin').get_var()
        TK_Skin_Thickness = self.get_prompt('TK Skin Thickness').get_var()
        Left_Against_Wall = self.get_prompt('Left Against Wall').get_var()
        Right_Against_Wall = self.get_prompt('Right Against Wall').get_var()    
        
        toe_kick_front = common_parts.add_toe_kick(self)
        toe_kick_front.set_name("Toe Kick Front")
        toe_kick_front.obj_bp.snap.comment_2 = "1034"
        false_exp =\
            "Width-(Toe_Kick_Thickness*3)-IF(Add_TK_Skin,IF(Left_Against_Wall,0,TK_Skin_Thickness),0)"+\
            "-IF(Add_TK_Skin,IF(Right_Against_Wall,0,TK_Skin_Thickness),0)"
        toe_kick_front.dim_x(
            "IF(Width>INCH(98.25),INCH(96),"+false_exp+")",
            [Width,Toe_Kick_Thickness,Left_Against_Wall,Right_Against_Wall,Add_TK_Skin,TK_Skin_Thickness])
        toe_kick_front.dim_y('-Height',[Height])
        toe_kick_front.dim_z('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_front.loc_x(
            "(Toe_Kick_Thickness*1.5)+IF(Add_TK_Skin,IF(Left_Against_Wall,0,TK_Skin_Thickness),0)",
            [Toe_Kick_Thickness,Add_TK_Skin,Left_Against_Wall,TK_Skin_Thickness])
        toe_kick_front.loc_y('Depth+Toe_Kick_Setback',[Depth,Toe_Kick_Setback])
        toe_kick_front.rot_x(value=math.radians(-90))
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.set_name("Toe Kick Back")
        if(self.is_double_sided):
            toe_kick.loc_y('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            toe_kick.loc_y('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        
        toe_kick.obj_bp.snap.comment_2 = "1034"
        toe_kick.dim_x(
            "IF(Width>INCH(98.25),INCH(96),"+false_exp+")",
            [Width,Toe_Kick_Thickness,Left_Against_Wall,Right_Against_Wall,Add_TK_Skin,TK_Skin_Thickness])
        toe_kick.dim_y('-Height', [Height])
        toe_kick.dim_z('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick.loc_x(
            '(Toe_Kick_Thickness*1.5)+IF(Add_TK_Skin,IF(Left_Against_Wall,0,TK_Skin_Thickness),0)',
            [Toe_Kick_Thickness, Add_TK_Skin, Left_Against_Wall, TK_Skin_Thickness])
        toe_kick.rot_x(value=math.radians(-90))
      
        
        left_toe_kick = common_parts.add_toe_kick_end_cap(self)
        if(self.is_double_sided):
            left_toe_kick.dim_x('-Depth-(Toe_Kick_Setback*2)',[Depth,Toe_Kick_Setback])
            left_toe_kick.loc_y('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            left_toe_kick.dim_x('-Depth-Toe_Kick_Setback+Toe_Kick_Thickness',[Depth,Toe_Kick_Setback,Toe_Kick_Thickness])
            left_toe_kick.loc_y('Toe_Kick_Thickness',[Toe_Kick_Thickness])

        left_toe_kick.dim_y('-Height',[Height])
        left_toe_kick.dim_z('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        left_toe_kick.loc_x(
            '(Toe_Kick_Thickness/2)+IF(Add_TK_Skin,IF(Left_Against_Wall,0,TK_Skin_Thickness),0)',
            [Toe_Kick_Thickness, Add_TK_Skin, TK_Skin_Thickness, Left_Against_Wall])
        left_toe_kick.rot_x(value=math.radians(-90))
        left_toe_kick.rot_z(value=math.radians(-90))        
        
        right_toe_kick = common_parts.add_toe_kick_end_cap(self)
        if(self.is_double_sided):
            right_toe_kick.dim_x('-Depth-(Toe_Kick_Setback*2)',[Depth,Toe_Kick_Setback])
            right_toe_kick.loc_y('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            right_toe_kick.dim_x('-Depth-Toe_Kick_Setback+Toe_Kick_Thickness',[Depth,Toe_Kick_Setback,Toe_Kick_Thickness])
            right_toe_kick.loc_y('Toe_Kick_Thickness',[Toe_Kick_Thickness])

        
        right_toe_kick.dim_y('Height',[Height])
        right_toe_kick.dim_z('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        right_toe_kick.loc_x('IF(Width>INCH(98.25),'
            'INCH(98.25)-(Toe_Kick_Thickness/2)-IF(Add_TK_Skin,IF(Right_Against_Wall,0,TK_Skin_Thickness),0),'
            'Width-(Toe_Kick_Thickness/2)-IF(Add_TK_Skin,IF(Right_Against_Wall,0,TK_Skin_Thickness),0))',
            [Width, Toe_Kick_Thickness, Add_TK_Skin, Right_Against_Wall, TK_Skin_Thickness])
        right_toe_kick.rot_x(value=math.radians(90))
        right_toe_kick.rot_z(value=math.radians(-90))
        
        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        toe_kick_stringer.dim_x('IF(Width>INCH(98.25),'
            'INCH(98.25)-(Toe_Kick_Thickness*3),'
            'Width-(Toe_Kick_Thickness*3))',[Width,Toe_Kick_Thickness])
        toe_kick_stringer.dim_y('Cleat_Width',[Cleat_Width])
        toe_kick_stringer.dim_z('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_stringer.loc_x('(Toe_Kick_Thickness*1.5)',[Toe_Kick_Thickness])
        toe_kick_stringer.loc_y('Depth+Toe_Kick_Thickness+Toe_Kick_Setback',[Depth,Toe_Kick_Thickness,Toe_Kick_Setback])
        toe_kick_stringer.loc_z('Height-Toe_Kick_Thickness',[Height,Toe_Kick_Thickness])

        
        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        if(self.is_double_sided):
            toe_kick_stringer.loc_y('-Toe_Kick_Setback-Toe_Kick_Thickness',[Toe_Kick_Setback,Toe_Kick_Thickness])
        false_exp =\
            "Width-(Toe_Kick_Thickness*3)-IF(Add_TK_Skin,IF(Left_Against_Wall,0,TK_Skin_Thickness),0)"+\
            "-IF(Add_TK_Skin,IF(Right_Against_Wall,0,TK_Skin_Thickness),0)"
        toe_kick_stringer.dim_x(
            "IF(Width>INCH(98.25),INCH(96),"+false_exp+")",
            [Width,Toe_Kick_Thickness,Left_Against_Wall,Right_Against_Wall,Add_TK_Skin,TK_Skin_Thickness])
        toe_kick_stringer.dim_y('-Cleat_Width', [Cleat_Width])
        toe_kick_stringer.dim_z('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_stringer.loc_x(
            '(Toe_Kick_Thickness*1.5)+IF(Add_TK_Skin,IF(Left_Against_Wall,0,TK_Skin_Thickness),0)',
            [Toe_Kick_Thickness, Add_TK_Skin, Left_Against_Wall, TK_Skin_Thickness])

        front_tk_skin = common_parts.add_toe_kick_skin(self)
        front_tk_skin.dim_x('IF(Width>INCH(98.25),'
            'INCH(98.25)-(Toe_Kick_Thickness),'
            'Width-(Toe_Kick_Thickness))',
            [Width,Toe_Kick_Thickness,TK_Skin_Thickness,Right_Against_Wall,Left_Against_Wall])
        front_tk_skin.dim_y('-Height',[Height])
        front_tk_skin.dim_z('TK_Skin_Thickness',[TK_Skin_Thickness])
        front_tk_skin.loc_x('(Toe_Kick_Thickness*1.5)-Toe_Kick_Thickness',[Toe_Kick_Thickness,TK_Skin_Thickness,Left_Against_Wall])
        front_tk_skin.loc_y('Depth+Toe_Kick_Setback-TK_Skin_Thickness',[Depth,Toe_Kick_Setback,TK_Skin_Thickness])
        front_tk_skin.rot_x(value=math.radians(-90))
        front_tk_skin.get_prompt("Hide").set_formula('IF(Add_TK_Skin,False,True) or Hide',[Add_TK_Skin,self.hide_var])

        if(self.is_double_sided):
            back_tk_skin = common_parts.add_toe_kick_skin(self)
            back_tk_skin.dim_x('IF(Width>INCH(98.25),'
                'INCH(98.25)-(Toe_Kick_Thickness)-IF(Left_Against_Wall,TK_Skin_Thickness,0)-IF(Right_Against_Wall,TK_Skin_Thickness,0),'
                'Width-(Toe_Kick_Thickness)-IF(Left_Against_Wall,TK_Skin_Thickness,0)-IF(Right_Against_Wall,TK_Skin_Thickness,0))',
                [Width, Toe_Kick_Thickness, TK_Skin_Thickness, Left_Against_Wall, Right_Against_Wall])
            back_tk_skin.dim_y('-Height', [Height])
            back_tk_skin.dim_z('-TK_Skin_Thickness',[TK_Skin_Thickness])
            back_tk_skin.loc_x(
                '(Toe_Kick_Thickness*1.5)-Toe_Kick_Thickness+IF(Left_Against_Wall,TK_Skin_Thickness,0)',
                [Toe_Kick_Thickness, TK_Skin_Thickness, Left_Against_Wall])
            back_tk_skin.loc_y('-Toe_Kick_Setback+TK_Skin_Thickness',[Toe_Kick_Setback,TK_Skin_Thickness])
            back_tk_skin.rot_x(value=math.radians(-90))
            back_tk_skin.get_prompt("Hide").set_formula('IF(Add_TK_Skin,False,True) or Hide',[Add_TK_Skin,self.hide_var]) 
        
        left_tk_skin = common_parts.add_toe_kick_skin(self)
        if(self.is_double_sided):
            left_tk_skin.dim_x('-Depth-(Toe_Kick_Setback*2)',[Depth,Toe_Kick_Setback])
            left_tk_skin.loc_y('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            left_tk_skin.dim_x('-Depth-Toe_Kick_Setback+Toe_Kick_Thickness',[Depth,Toe_Kick_Setback,Toe_Kick_Thickness])
            left_tk_skin.loc_y('Toe_Kick_Thickness',[Toe_Kick_Thickness])

        left_tk_skin.dim_y('-Height',[Height])
        left_tk_skin.dim_z('TK_Skin_Thickness',[TK_Skin_Thickness])
        left_tk_skin.loc_x('(Toe_Kick_Thickness/2)',[Toe_Kick_Thickness,TK_Skin_Thickness])
        left_tk_skin.rot_x(value=math.radians(-90))
        left_tk_skin.rot_z(value=math.radians(-90))  
        left_tk_skin.get_prompt("Hide").set_formula(
            'IF(Left_Against_Wall,True,IF(Add_TK_Skin,False,True)) or Hide',
            [Add_TK_Skin, Left_Against_Wall,self.hide_var])

        right_tk_skin = common_parts.add_toe_kick_skin(self)
        if(self.is_double_sided):
            right_tk_skin.dim_x('-Depth-(Toe_Kick_Setback*2)',[Depth,Toe_Kick_Setback])
            right_tk_skin.loc_y('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            right_tk_skin.dim_x('-Depth-Toe_Kick_Setback+Toe_Kick_Thickness',[Depth,Toe_Kick_Setback,Toe_Kick_Thickness])
            right_tk_skin.loc_y('Toe_Kick_Thickness',[Toe_Kick_Thickness])

        right_tk_skin.dim_y('Height',[Height])
        right_tk_skin.dim_z('TK_Skin_Thickness',[TK_Skin_Thickness])
        right_tk_skin.loc_x('IF(Width>INCH(98.25),'
            'INCH(98.25)-(Toe_Kick_Thickness/2),'
            'Width-(Toe_Kick_Thickness/2))',
            [Width,Toe_Kick_Thickness,TK_Skin_Thickness])
        right_tk_skin.rot_x(value=math.radians(90))
        right_tk_skin.rot_z(value=math.radians(-90))
        right_tk_skin.get_prompt("Hide").set_formula(
            'IF(Right_Against_Wall,True,IF(Add_TK_Skin,False,True)) or Hide',
            [Add_TK_Skin, Right_Against_Wall,self.hide_var])

    def add_opening_widths_calculator(self):
        calc_distance_obj = self.add_empty('Calc Distance Obj')
        calc_distance_obj.empty_display_size = .001

        self.calculator = self.obj_prompts.snap.add_calculator(
            "Opening Widths Calculator",
            calc_distance_obj)

    def set_calculator_distance(self):
        Product_Width = self.obj_x.snap.get_var('location.x', 'Product_Width')
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        self.calculator.set_total_distance(
            "Product_Width-Panel_Thickness*(" + str(self.opening_qty) +"+1)",
            [Product_Width, Panel_Thickness])
    
    def update(self):
        self.obj_x.location.x = self.width
        self.obj_z.location.z = self.height
        self.obj_y.location.y = -self.depth

        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["IS_BP_ISLAND"] = True
        self.obj_bp["ID_PROMPT"] = self.id_prompt 
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.set_prompts()

        calculator = self.get_calculator('Opening Widths Calculator')
        if calculator:
            bpy.context.view_layer.update()
            calculator.calculate()
        super().update()

    def draw(self):
        defaults = bpy.context.scene.sn_closets.closet_defaults

        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.obj_bp['product_type'] = "Closet"
        product_props = self.obj_bp.sn_closets
        product_props.is_island = True
        
        if defaults.export_subassemblies:
            self.obj_bp.snap.export_product_subassemblies = True

        #ORDER OF PROMPTS ARE IMPORTANT
        self.add_opening_widths_calculator()
        self.add_opening_prompts()
        common_prompts.add_thickness_prompts(self) #MUST BE CALLED BEFORE add_island_prompts()
        self.set_calculator_distance()
        self.add_island_prompts()
        common_prompts.add_toe_kick_prompts(self,prompt_tab=1)
        common_prompts.add_countertop_prompts(self)         
        
        self.add_base_assembly()
        self.add_sides()
        self.add_counter_top()
        if not self.is_double_sided:
            self.add_thick_back()
        panel = None
        self.add_shelf(1,panel,is_top=True)
        self.add_shelf(1,panel,is_top=False)
    
        # self.add_toe_kick(1,panel)
        self.add_closet_opening(1,panel)
        self.add_closet_opening(1,panel,is_rear=True)
        if self.is_double_sided:
            # self.add_toe_kick(1, panel, is_rear=True)
            self.add_double_sided_back(1, panel)
            #self.add_shelf(1,panel,is_top=True,is_rear=True)
            #self.add_shelf(1,panel,is_top=False,is_rear=True)                
        
        for i in range(2,self.opening_qty+1):
            panel = self.add_panel(i,panel)
            panel.obj_bp['PARTITION_NUMBER'] = (i - 1)
            self.add_shelf(i,panel,is_top=True)
            self.add_shelf(i,panel,is_top=False)
            # self.add_toe_kick(i,panel)
            self.add_closet_opening(i,panel)
            if self.is_double_sided:
                # self.add_toe_kick(i, panel, is_rear=True)
                self.add_double_sided_back(i, panel)
                self.add_closet_opening(i,panel,is_rear=True)
        
        self.update()
                

class PROMPTS_Opening_Starter(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.island_openings"
    bl_label = "Island Prompts" 
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name")
    
    tabs: EnumProperty(name="Tabs",
                        items=[('OPENINGS','Opening Sizes','Show the Width x Height x Depth for each opening'),
                               ('CONSTRUCTION','Construction Options','Show Additional Construction Options')],
                        default = 'OPENINGS')
    
    current_location: FloatProperty(name="Current Location", default=0,subtype='DISTANCE')
    left_offset: FloatProperty(name="Left Offset", default=0,subtype='DISTANCE')
    right_offset: FloatProperty(name="Right Offset", default=0,subtype='DISTANCE')
    product_width: FloatProperty(name="Product Width", default=0,subtype='DISTANCE')    
    
    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)
    height: EnumProperty(name="Height",
                          items=common_lists.PANEL_HEIGHTS,
                          default = '2131',
                          update=update_closet_height)

    countertop_type_ppt = None
    countertop_type: EnumProperty(
        name="Countertop Type",
        items=[
            ('0', 'Granite', 'Granite'),
            ('1', 'HPL', 'HPL'),
            ('2', 'Melamine', 'Melamine')],
        default='0')                          
    
    product = None
    
    inserts = []

    def set_countertop_type_ppt(self):
        if self.countertop_type_ppt:
            self.countertop_type_ppt.set_value(int(self.countertop_type))
    
    def check(self, context):
        toe_kick_height =\
            self.product.get_prompt("Toe Kick Height").distance_value
        if toe_kick_height <= inch(3):
            self.product.get_prompt("Toe Kick Height").set_value(inch(3))
            bpy.ops.snap.log_window('INVOKE_DEFAULT',
                                    message="Minimum Toe Kick Height is 3\"",
                                    icon="ERROR")
        self.product.obj_x.location.x = self.width
        self.run_calculators(self.product.obj_bp)
        self.set_countertop_type_ppt()
        depth_1 = self.product.get_prompt("Depth 1")
        if not depth_1:
            self.product.obj_y.location.y = -self.depth
        closet_props.update_render_materials(self, context)
        return True

    def set_product_defaults(self):
        self.product.obj_bp.location.x = self.selected_location + self.left_offset
        self.product.obj_x.location.x = self.default_width - (self.left_offset + self.right_offset)

    def execute(self, context):
        obj_list = []
        obj_list = sn_utils.get_child_objects(self.product.obj_bp, obj_list)
        for obj in obj_list:
            if obj.type == 'EMPTY':
                obj.hide_set(True)
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                self.run_calculators(self.product.obj_bp)
        return {'FINISHED'}

    def set_default_heights(self):
        opening_height = round(sn_unit.meter_to_millimeter(self.product.obj_z.location.z),0)
        for index, height in enumerate(common_lists.PANEL_HEIGHTS):
            if not opening_height >= int(height[0]):
                exec('self.height = common_lists.PANEL_HEIGHTS[index - 1][0]')                                                                                                                                                                                                        
                break

    def invoke(self,context,event):
        obj = bpy.data.objects[context.object.name]
        obj_product_bp = sn_utils.get_bp(obj,'PRODUCT')
        self.product = sn_types.Assembly(obj_product_bp)

        self.run_calculators(self.product.obj_bp)

        if self.product.obj_bp:
            self.width = math.fabs(self.product.obj_x.location.x)
            new_list = []
            self.inserts = sn_utils.get_insert_bp_list(self.product.obj_bp,new_list)
            self.depth = math.fabs(self.product.obj_y.location.y)
            self.set_default_heights()
            self.countertop_type_ppt = self.product.get_prompt("Countertop Type")

            if self.countertop_type_ppt:
                self.countertop_type = str(self.countertop_type_ppt.get_value())

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=500)

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
            row1.label(text='Width: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label(text='Width:')
            row1.prop(self,'width',text="")
        
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_z):
            pass
        else:
            row1 = col.row(align=True)
            row1.prop(self,'height',text="Set Height")
        
    def object_has_driver(self,obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True
            
    def draw_common_prompts(self,layout):
        depth_1 = self.product.get_prompt("Depth 1")
        depth_2 = self.product.get_prompt("Depth 2")
        box = layout.box()
        col = box.column(align=True)        
        if depth_1 and depth_2:
            col.prop(depth_1, "distance_value", text=depth_1.name)
            col.prop(depth_2, "distance_value", text=depth_2.name)
        else:
            col.prop(self,'depth')
        
    def get_number_of_equal_widths(self):
        number_of_equal_widths = 0
        
        for i in range(1,9):
            width = self.product.get_prompt("Opening " + str(i) + " Width")
            if width:
                number_of_equal_widths += 1 if width.equal else 0
            else:
                break
            
        return number_of_equal_widths
        
    def draw_splitter_widths(self,layout):
        props = bpy.context.scene.sn_closets

        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        row.label(text="Opening Name:")
        row.label(text="",icon='BLANK1')
        row.label(text="Width:")
        
        box = col.box()
        
        for i in range(1,9):
            width = self.product.get_prompt("Opening " + str(i) + " Width")

            if width:
                row = box.row()
                row.label(text= str(i) + ":")
                if width.equal == False:
                    row.prop(width,'equal',text="")
                else:
                    if self.get_number_of_equal_widths() != 1:
                        row.prop(width,'equal',text="")
                    else:
                        row.label(text="",icon='BLANK1')
                if width.equal:
                    row.label(text=str(sn_unit.meter_to_active_unit(width.distance_value)) + '"')
                else:
                    row.prop(width,'distance_value',text="")   
            
    def draw_construction_options(self,layout):
        box = layout.box()
        
        toe_kick_height = self.product.get_prompt("Toe Kick Height")
        toe_kick_setback = self.product.get_prompt("Toe Kick Setback")
        left_against_wall = self.product.get_prompt("Left Against Wall")
        right_against_wall = self.product.get_prompt("Right Against Wall")
        add_tk_skin = self.product.get_prompt("Add TK Skin")
        
        col = box.column(align=True)
        row = col.row()
        row.label(text="Against Wall:")   
        row.prop(left_against_wall, "checkbox_value", text="Left")
        row.prop(right_against_wall, "checkbox_value", text="Right")
        
        col = box.column(align=True)
        col.label(text="Base Options:")        
        # TOE KICK OPTIONS
        if toe_kick_height and toe_kick_setback:
            row = col.row()
            row.label(text="Toe Kick")
            row.prop(toe_kick_height, "distance_value", text="Height")
            row.prop(toe_kick_setback, "distance_value", text="Setback")
            if add_tk_skin:
                row = col.row()
                row.prop(add_tk_skin, "checkbox_value", text="Add Toe Kick Skin")            

        col = box.column(align=True)
        col.label(text="Top Options:")        
        Countertop_Thickness = self.product.get_prompt("Countertop Thickness")
        HPL_Material_Name = self.product.get_prompt("HPL Material Name")
        HPL_Material_Number = self.product.get_prompt("HPL Material Number")
        Deck_Overhang = self.product.get_prompt("Deck Overhang")
        Side_Deck_Overhang = self.product.get_prompt("Side Deck Overhang")
        No_Countertop = self.product.get_prompt("No Countertop")

        if Deck_Overhang:
            row = col.row()
            row.prop(Deck_Overhang, "distance_value", text="Opening Overhang")
            row.prop(Side_Deck_Overhang, "distance_value", text="Side Overhang")
        row = col.row()
        row.prop(No_Countertop,"checkbox_value",text="No Countertop")
        row = col.row(align=True)
        if self.countertop_type_ppt and No_Countertop.get_value() == False:
            sn_utils.draw_enum(self, layout, 'countertop_type', 'Countertop Types', 3)

    def draw_product_placment(self,layout):
        box = layout.box()
        
        row = box.row(align=True)
        row.label(text='Location:')
        row.prop(self.product.obj_bp,'location',index=0,text="X")
        row.prop(self.product.obj_bp,'location',index=1,text="Y")
        
        row.label(text='Rotation:')
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="")
        
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                left_against_wall = self.product.get_prompt("Left Against Wall")
                box = layout.box()
                box.label(text=self.product.obj_bp.snap.name_object,icon='LATTICE_DATA')
                
                split = box.split(factor=.5)
                self.draw_product_size(split)
                self.draw_common_prompts(split)
                row = box.row()
                if(left_against_wall):
                    row.prop(self,'tabs',expand=True)
                    if self.tabs == 'OPENINGS':
                        self.draw_splitter_widths(box)
                    elif self.tabs == 'CONSTRUCTION':
                        self.draw_construction_options(box)
                    else:
                        pass
                    self.draw_product_placment(box)        
                
bpy.utils.register_class(PROMPTS_Opening_Starter)
