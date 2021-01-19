import bpy
import math
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists
from . import data_base_assembly

def update_closet_height(self,context):
    ''' EVENT changes height for all closet openings
    '''
    obj_product_bp = utils.get_bp(context.active_object,'PRODUCT')
    product = fd_types.Assembly(obj_product_bp)
    product.obj_z.location.z = unit.millimeter(float(self.height))

class Closet_Island_Carcass(fd_types.Assembly):
    
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".island_openings"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'
    
    opening_qty = 4
    
    is_double_sided = False
    
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.width = unit.inch(18) * self.opening_qty
        self.height = unit.millimeter(float(defaults.island_panel_height))
        if self.is_double_sided:
            self.depth = defaults.panel_depth * 2 
        else:
            self.depth = defaults.panel_depth
    
    def add_opening_prompts(self):
        props = props_closet.get_scene_props().closet_defaults

        for i in range(1,self.opening_qty+1):
            self.add_prompt(name="Opening " + str(i) + " Width",
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=0,
                            equal=True)
        
    def add_island_prompts(self):
        props = props_closet.get_scene_props().closet_defaults
        
        self.add_prompt(name="Left Against Wall",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Right Against Wall",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="No Countertop",prompt_type='CHECKBOX',value=False,tab_index=1)
        
        if self.is_double_sided:
            self.add_prompt(name="Depth 1",prompt_type='DISTANCE',value=props.panel_depth,tab_index=1)
            self.add_prompt(name="Depth 2",prompt_type='DISTANCE',value=props.panel_depth,tab_index=1)
            
            Depth_1 = self.get_var('Depth 1')
            Depth_2 = self.get_var('Depth 2')
            Back_Thickness = self.get_var('Back Thickness')
            Panel_Thickness = self.get_var('Panel Thickness')
            
            self.y_dim('(Depth_1+Depth_2+Panel_Thickness)*-1',[Depth_1,Depth_2,Panel_Thickness])
            
    def add_sides(self):
        props = props_closet.get_scene_props()   
        
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Right_Side_Wall_Filler = self.get_var('Right Side Wall Filler')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Add_Backing = self.get_var('Add Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Panel_Thickness = self.get_var('Panel Thickness')
        
        left_side = common_parts.add_panel(self)
        left_side.x_dim('Product_Height',[Product_Height])
        left_side.y_dim('Product_Depth',[Product_Depth])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_side.y_loc('IF(Add_Backing,-Panel_Thickness,0)',[Add_Backing,Panel_Thickness])
        left_side.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        left_side.x_rot(value = 0)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
                
        right_side = common_parts.add_panel(self)
        right_side.x_dim('Product_Height',[Product_Height])
        right_side.y_dim('Product_Depth',[Product_Depth])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
        right_side.y_loc('IF(Add_Backing,-Panel_Thickness,0)',[Add_Backing,Panel_Thickness])
        right_side.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        right_side.x_rot(value = 0)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)

    def add_panel(self,index,previous_panel):
        props = props_closet.get_scene_props()
                
        PH = self.get_var('dim_z','PH')
        PD = self.get_var('dim_y','PD')
        Width = self.get_var('Opening ' + str(index-1) + ' Width',"Width")
        Panel_Thickness = self.get_var('Panel Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        
        panel = common_parts.add_panel(self)
        if previous_panel:
            Prev_Panel_X = previous_panel.get_var("loc_x",'Prev_Panel_X')
            Left_Side_Thickness = self.get_var('Left_Side_Thickness')
            panel.x_loc('Prev_Panel_X+Panel_Thickness+Width',[Prev_Panel_X,Panel_Thickness,Width])
        else:
            Left_Side_Thickness = self.get_var('Left Side Thickness')
            panel.x_loc('Left_Side_Thickness+Width+Panel_Thickness',[Left_Side_Thickness,Width,Panel_Thickness])
            
        if self.is_double_sided:
            panel.y_loc(value = 0)
        else:
            panel.y_loc(value = 0)
        panel.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        panel.x_rot(value = 0)
        panel.y_rot(value = -90)
        panel.z_rot(value = 0)
        panel.x_dim('PH',[PH]) 
        panel.y_dim('PD',[PD])
        panel.z_dim('Panel_Thickness',[Panel_Thickness])
        return panel
        
    def add_shelf(self,i,panel,is_top=False,is_rear=False):
        Product_Height = self.get_var('dim_z','Product_Height')
        Depth_1 = self.get_var('Depth 1')
        Depth_2 = self.get_var('Depth 2')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')

        shelf = common_parts.add_shelf(self)
        shelf.prompt("Is Locked Shelf",value=True)
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            shelf.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            shelf.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])
        
        if self.is_double_sided:
            shelf.y_loc(value = 0)
            shelf.y_dim("Product_Depth",[Product_Depth])
        else:
            shelf.y_loc(value = 0)
            shelf.y_dim("Product_Depth",[Product_Depth])
        
        if is_top:
            shelf.z_loc('Product_Height+Toe_Kick_Height',[Product_Height,Toe_Kick_Height])
            shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        else:
            shelf.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
            shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
            
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 0)
        shelf.x_dim('Width',[Width])
        
        if is_top:
            shelf.prompt("Drill On Top",value=True)
        else:
            shelf.prompt("Drill On Top",value=False)
    
    def add_toe_kick(self,i,panel,is_rear=False):
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')

        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        kick = common_parts.add_toe_kick(self)
        kick.x_dim("Width",[Width])
        kick.y_dim('-Toe_Kick_Height',[Toe_Kick_Height,Shelf_Thickness])
        kick.x_loc('X_Loc',[X_Loc])
        if is_rear:
            kick.y_loc('-Toe_Kick_Setback',[Product_Depth,Toe_Kick_Setback])
            kick.z_dim('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        else:
            kick.y_loc('Product_Depth+Toe_Kick_Setback',[Product_Depth,Toe_Kick_Setback])
            kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        kick.z_loc(value = 0)
        kick.x_rot(value = -90)
        kick.y_rot(value = 0)
        kick.z_rot(value = 0)
        
    def add_closet_opening(self,i,panel,is_rear=False):
        props = props_closet.get_scene_props().closet_defaults
        
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Depth_1 = self.get_var("Depth 1")
        Depth_2 = self.get_var("Depth 2")
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        
        opening = common_parts.add_section_opening(self)
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')

        opening.z_loc('Toe_Kick_Height+Shelf_Thickness',[Toe_Kick_Height,Shelf_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        if is_rear:
            opening.x_loc('X_Loc+Width',[X_Loc,Width])
            opening.y_loc(value = 0)
            opening.z_rot(value = 180)
            opening.y_dim("Depth_1",[Depth_1])
        else:
            opening.x_loc('X_Loc',[X_Loc])
            opening.y_loc('Product_Depth',[Product_Depth])
            opening.z_rot(value = 0)
            if self.is_double_sided:
                opening.y_dim("Depth_2",[Depth_2])
            else:
                opening.y_dim("fabs(Product_Depth)",[Product_Depth])
        opening.x_dim('Width',[Width])
        
        if props.use_plant_on_top:
            opening.z_dim('Product_Height-Shelf_Thickness',[Product_Height,Shelf_Thickness])
        else:
            opening.z_dim('Product_Height-(Shelf_Thickness*2)',[Product_Height,Shelf_Thickness])
        
    def add_inside_dimension(self,i,panel):
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            
        dim = fd_types.Dimension()
        dim.parent(self.obj_bp)
        dim.start_z(value = unit.inch(-4))
        dim.start_y(value = unit.inch(4))
        if panel:
            dim.start_x('X_Loc',[X_Loc])
        else:
            dim.start_x('X_Loc+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
        dim.end_x('Width',[Width])
        dim.set_color('IF(Width>INCH(42),3,0)',[Width])
    
    def add_thick_back(self):
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Width = self.get_var('dim_x','Product_Width')
        Back_Thickness = self.get_var('Back Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Panel_Thickness = self.get_var('Panel Thickness')
        
        backing = common_parts.add_back(self)
        backing.x_loc(value = 0)
        backing.y_loc(value = 0)
        backing.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        backing.x_rot(value = 90)
        backing.y_rot(value = 0)
        backing.z_rot(value = 0)
        backing.x_dim('Product_Width',[Product_Width])
        backing.y_dim("Product_Height",[Product_Height])
        backing.z_dim('-Panel_Thickness',[Panel_Thickness])
        
    def add_double_sided_back(self,i,panel):
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Width = self.get_var('dim_x','Product_Width')
        Back_Thickness = self.get_var('Back Thickness')
        Depth_1 = self.get_var('Depth 1')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Panel_Thickness = self.get_var('Panel Thickness')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            
        backing = common_parts.add_back(self)
        backing.x_loc('X_Loc',[X_Loc])
        backing.y_loc('-Depth_1',[Depth_1])
        backing.z_loc('Toe_Kick_Height + Panel_Thickness',[Toe_Kick_Height,Panel_Thickness])
        backing.x_rot(value = 90)
        backing.y_rot(value = 0)
        backing.z_rot(value = 0)
        backing.x_dim('Width',[Width])
        backing.y_dim("Product_Height-(Panel_Thickness*2)",[Product_Height,Panel_Thickness])
        backing.z_dim('Panel_Thickness',[Panel_Thickness])
        
    def add_counter_top(self):
        dim_x = self.get_var('dim_x')
        dim_z = self.get_var('dim_z')
        dim_y = self.get_var('dim_y')
        Deck_Overhang = self.get_var('Deck Overhang')
        Side_Deck_Overhang = self.get_var("Side Deck Overhang")
        Deck_Thickness = self.get_var('Deck Thickness')
        Countertop_Type = self.get_var('Countertop Type')
        Left_Against_Wall = self.get_var('Left Against Wall')
        Right_Against_Wall = self.get_var('Right Against Wall')
        Exposed_Back = self.get_var('Exposed Back')
        Toe_Kick_Height = self.get_var('Toe Kick Height') 
        No_Countertop = self.get_var('No Countertop')       
        
        granite_ctop = common_parts.add_countertop(self)
        granite_ctop.set_name("Granite Countertop")
        granite_ctop.x_loc('IF(Left_Against_Wall,0,-Side_Deck_Overhang)',[Left_Against_Wall,Side_Deck_Overhang])
        granite_ctop.y_loc('Deck_Overhang',[Deck_Overhang])
        granite_ctop.z_loc('dim_z+Toe_Kick_Height',[dim_z,Toe_Kick_Height])
        granite_ctop.x_rot(value = 0)
        granite_ctop.y_rot(value = 0)
        granite_ctop.z_rot(value = 0)
        granite_ctop.x_dim('dim_x+IF(Left_Against_Wall,0,Side_Deck_Overhang)+IF(Right_Against_Wall,0,Side_Deck_Overhang)',
                   [dim_x,Side_Deck_Overhang,Left_Against_Wall,Right_Against_Wall])
        granite_ctop.y_dim('dim_y-Deck_Overhang*2',[dim_y,Deck_Overhang])
        granite_ctop.z_dim('Deck_Thickness',[Deck_Thickness])
        granite_ctop.prompt("Hide","IF(No_Countertop,True,IF(Countertop_Type==2,False,True))",[Countertop_Type,No_Countertop])
        #granite_ctop.prompt("Exposed Left","IF(Left_Against_Wall,False,True)",[Left_Against_Wall])
        #granite_ctop.prompt("Exposed Right","IF(Right_Against_Wall,False,True)",[Right_Against_Wall])
        #granite_ctop.prompt("Exposed Back","Exposed_Back",[Exposed_Back])
                
        hpltop = common_parts.add_hpl_top(self)    
        hpltop.set_name("HPL Countertop")
        hpltop.x_loc('IF(Left_Against_Wall,0,-Side_Deck_Overhang)',[Left_Against_Wall,Side_Deck_Overhang])
        hpltop.y_loc('Deck_Overhang',[Deck_Overhang])
        hpltop.z_loc('dim_z+Toe_Kick_Height',[dim_z,Toe_Kick_Height])
        hpltop.x_rot(value = 0)
        hpltop.y_rot(value = 0)
        hpltop.z_rot(value = 0)
        hpltop.x_dim('dim_x+IF(Left_Against_Wall,0,Side_Deck_Overhang)+IF(Right_Against_Wall,0,Side_Deck_Overhang)',
                   [dim_x,Side_Deck_Overhang,Left_Against_Wall,Right_Against_Wall])
        hpltop.y_dim('dim_y-Deck_Overhang*2',[dim_y,Deck_Overhang])
        hpltop.z_dim('Deck_Thickness',[Deck_Thickness])
        hpltop.prompt("Hide","IF(No_Countertop,True,IF(Countertop_Type==1,False,True))",[Countertop_Type,No_Countertop])
        hpltop.prompt("Exposed Left","IF(Left_Against_Wall,False,True)",[Left_Against_Wall])
        hpltop.prompt("Exposed Right","IF(Right_Against_Wall,False,True)",[Right_Against_Wall])
        hpltop.prompt("Exposed Back","Exposed_Back",[Exposed_Back])

        melamine_deck = common_parts.add_plant_on_top(self)    
        melamine_deck.set_name("Melamine Countertop")
        melamine_deck.x_loc('IF(Left_Against_Wall,0,-Side_Deck_Overhang)',[Left_Against_Wall,Side_Deck_Overhang])
        melamine_deck.y_loc('Deck_Overhang',[Deck_Overhang])
        melamine_deck.z_loc('dim_z+Toe_Kick_Height',[dim_z,Toe_Kick_Height])
        melamine_deck.x_rot(value = 0)
        melamine_deck.y_rot(value = 0)
        melamine_deck.z_rot(value = 0)
        melamine_deck.x_dim('dim_x+IF(Left_Against_Wall,0,Side_Deck_Overhang)+IF(Right_Against_Wall,0,Side_Deck_Overhang)',[dim_x,Side_Deck_Overhang,Left_Against_Wall,Right_Against_Wall])
        melamine_deck.y_dim('dim_y-Deck_Overhang*2',[dim_y,Deck_Overhang])
        melamine_deck.z_dim('Deck_Thickness',[Deck_Thickness])   
        melamine_deck.prompt("Is Counter Top",value = True) 
        melamine_deck.prompt("Hide","IF(No_Countertop,True,IF(Countertop_Type==0,False,True))",[Countertop_Type,No_Countertop]) 
        melamine_deck.prompt("Exposed Left","IF(Left_Against_Wall,False,True)",[Left_Against_Wall])
        melamine_deck.prompt("Exposed Right","IF(Right_Against_Wall,False,True)",[Right_Against_Wall])
        melamine_deck.prompt("Exposed Back","Exposed_Back",[Exposed_Back])
        for child in melamine_deck.obj_bp.children:
            if child.cabinetlib.type_mesh == 'CUTPART':
                for mat_slot in child.cabinetlib.material_slots:
                    mat_slot.pointer_name = "Closet_Part_Edges"    
        
    def add_base_assembly(self):
#        Product_Depth = self.get_var('dim_y','Product_Depth')
#        Width =  self.get_var('dim_x','Width')
#        Toe_Kick_Height = self.get_var('Toe Kick Height')
#        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
#        Shelf_Thickness = self.get_var('Shelf Thickness')
#        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')
#        
#        base_assembly = data_base_assembly.Base_Assembly() 
#        base_assembly.draw()
#        base_assembly.obj_bp.parent = self.obj_bp
#        base_assembly.set_name("Toe Kick")
#        base_assembly.x_loc(value = 0)
#        base_assembly.y_loc('-Toe_Kick_Setback',[Toe_Kick_Setback])
#        base_assembly.z_loc(value = 0)
#        base_assembly.x_rot(value = 0)
#        base_assembly.y_rot(value = 0)
#        base_assembly.z_rot(value = 0)
#        base_assembly.x_dim('Width',[Width])
#        base_assembly.y_dim('Product_Depth+(Toe_Kick_Setback*2)',[Product_Depth,Toe_Kick_Setback])
#        base_assembly.z_dim('Toe_Kick_Height',[Toe_Kick_Height])       
        self.add_prompt(name="Cleat Width",prompt_type='DISTANCE',value=unit.inch(2.5),tab_index=1)
        Width = self.get_var('dim_x',"Width")
        Depth = self.get_var('dim_y',"Depth")
        Height = self.get_var('Toe Kick Height',"Height")
        Cleat_Width = self.get_var('Cleat Width')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Extend_Left_Amount = self.get_var('Extend Left Amount')
        Extend_Right_Amount = self.get_var('Extend Right Amount')
        Extend_Depth_Amount = self.get_var('Extend Depth Amount')
        
        toe_kick_front = common_parts.add_toe_kick(self)
        toe_kick_front.set_name("Toe Kick Front")
        toe_kick_front.obj_bp.mv.comment_2 = "1034"
        toe_kick_front.x_dim('Width-(Toe_Kick_Thickness*3)',[Width,Toe_Kick_Thickness])
        toe_kick_front.y_dim('-Height',[Height])
        toe_kick_front.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_front.x_loc('(Toe_Kick_Thickness*1.5)',[Toe_Kick_Thickness])
        toe_kick_front.y_loc('Depth+Toe_Kick_Setback',[Depth,Toe_Kick_Setback])
        toe_kick_front.z_loc(value = 0)
        toe_kick_front.x_rot(value = -90)
        toe_kick_front.y_rot(value = 0)
        toe_kick_front.z_rot(value = 0)
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.set_name("Toe Kick Back")
        if(self.is_double_sided):
            toe_kick.y_loc('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            toe_kick.y_loc('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        
        toe_kick.obj_bp.mv.comment_2 = "1034"
        toe_kick.x_dim('Width-(Toe_Kick_Thickness*3)',[Width,Toe_Kick_Thickness])
        toe_kick.y_dim('-Height',[Height])
        toe_kick.z_dim('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick.x_loc('(Toe_Kick_Thickness*1.5)',[Toe_Kick_Thickness])
        
        toe_kick.z_loc(value = 0)
        toe_kick.x_rot(value = -90)
        toe_kick.y_rot(value = 0)
        toe_kick.z_rot(value = 0)        
        
        left_toe_kick = common_parts.add_toe_kick_end_cap(self)
        if(self.is_double_sided):
            left_toe_kick.x_dim('-Depth-(Toe_Kick_Setback*2)',[Depth,Toe_Kick_Setback])
            left_toe_kick.y_loc('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            left_toe_kick.x_dim('-Depth-Toe_Kick_Setback+Toe_Kick_Thickness',[Depth,Toe_Kick_Setback,Toe_Kick_Thickness])
            left_toe_kick.y_loc('Toe_Kick_Thickness',[Toe_Kick_Thickness])

        left_toe_kick.y_dim('-Height',[Height])
        left_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        left_toe_kick.x_loc('(Toe_Kick_Thickness/2)',[Toe_Kick_Thickness])
        left_toe_kick.z_loc(value = 0)
        left_toe_kick.x_rot(value = -90)
        left_toe_kick.y_rot(value = 0)
        left_toe_kick.z_rot(value = -90)        
        
        right_toe_kick = common_parts.add_toe_kick_end_cap(self)
        if(self.is_double_sided):
            right_toe_kick.x_dim('-Depth-(Toe_Kick_Setback*2)',[Depth,Toe_Kick_Setback])
            right_toe_kick.y_loc('-Toe_Kick_Setback',[Toe_Kick_Setback])
        else:
            right_toe_kick.x_dim('-Depth-Toe_Kick_Setback+Toe_Kick_Thickness',[Depth,Toe_Kick_Setback,Toe_Kick_Thickness])
            right_toe_kick.y_loc('Toe_Kick_Thickness',[Toe_Kick_Thickness])

        
        right_toe_kick.y_dim('Height',[Height])
        right_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        
        right_toe_kick.x_loc('Width-(Toe_Kick_Thickness/2)',[Width,Toe_Kick_Thickness])
        right_toe_kick.z_loc(value = 0)
        right_toe_kick.x_rot(value = 90)
        right_toe_kick.y_rot(value = 0)
        right_toe_kick.z_rot(value = -90)
        
        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        toe_kick_stringer.x_dim('Width-(Toe_Kick_Thickness*3)',[Width,Toe_Kick_Thickness])
        toe_kick_stringer.y_dim('Cleat_Width',[Cleat_Width])
        toe_kick_stringer.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_stringer.x_loc('(Toe_Kick_Thickness*1.5)',[Toe_Kick_Thickness])
        toe_kick_stringer.y_loc('Depth+Toe_Kick_Thickness+Toe_Kick_Setback',[Depth,Toe_Kick_Thickness,Toe_Kick_Setback])
        toe_kick_stringer.z_loc('Height-Toe_Kick_Thickness',[Height,Toe_Kick_Thickness])
        toe_kick_stringer.x_rot(value = 0)
        toe_kick_stringer.y_rot(value = 0)
        toe_kick_stringer.z_rot(value = 0)
        
        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        if(self.is_double_sided):
            toe_kick_stringer.y_loc('-Toe_Kick_Setback-Toe_Kick_Thickness',[Toe_Kick_Setback,Toe_Kick_Thickness])
        else:
            toe_kick_stringer.y_loc(value = 0)

        toe_kick_stringer.x_dim('Width-(Toe_Kick_Thickness*3)',[Width,Toe_Kick_Thickness])
        toe_kick_stringer.y_dim('-Cleat_Width',[Cleat_Width])
        toe_kick_stringer.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_stringer.x_loc('(Toe_Kick_Thickness*1.5)',[Toe_Kick_Thickness])
        toe_kick_stringer.z_loc(value = 0)
        toe_kick_stringer.x_rot(value = 0)
        toe_kick_stringer.y_rot(value = 0)
        toe_kick_stringer.z_rot(value = 0)   
        
    def draw(self):
        defaults = props_closet.get_scene_props().closet_defaults

        self.create_assembly()
        self.obj_bp.mv.product_type = "Closet"
        product_props = props_closet.get_object_props(self.obj_bp)
        product_props.is_island = True
        
        if defaults.export_subassemblies:
            self.obj_bp.mv.export_product_subassemblies = True      
        
        self.add_tab(name='Opening Widths',tab_type='CALCULATOR',calc_type="XDIM") #0
        self.add_tab(name='Carcass Options',tab_type='VISIBLE') #1
        
        #ORDER OF PROMPTS ARE IMPORTANT
        self.add_opening_prompts()
        common_prompts.add_thickness_prompts(self) #MUST BE CALLED BEFORE add_island_prompts()
        self.add_island_prompts()
        common_prompts.add_toe_kick_prompts(self,prompt_tab=1)
        common_prompts.add_countertop_prompts(self,prompt_tab=1)
        
        Panel_Thickness = self.get_var('Panel Thickness')
        self.calculator_deduction("Panel_Thickness*(" + str(self.opening_qty) +"+1)",[Panel_Thickness])            
        
        self.add_base_assembly()
        
        self.add_sides()
        self.add_counter_top()
        if not self.is_double_sided:
            self.add_thick_back()
        panel = None
        self.add_shelf(1,panel,is_top=True)
        self.add_shelf(1,panel,is_top=False)
    
#         self.add_toe_kick(1,panel)
        self.add_closet_opening(1,panel)
        self.add_closet_opening(1,panel,is_rear=True)
        if self.is_double_sided:
#             self.add_toe_kick(1, panel, is_rear=True)
            self.add_double_sided_back(1, panel)
            #self.add_shelf(1,panel,is_top=True,is_rear=True)
            #self.add_shelf(1,panel,is_top=False,is_rear=True)                
        
        for i in range(2,self.opening_qty+1):
            panel = self.add_panel(i,panel)
            self.add_shelf(i,panel,is_top=True)
            self.add_shelf(i,panel,is_top=False)
#             self.add_toe_kick(i,panel)
            self.add_closet_opening(i,panel)
            if self.is_double_sided:
#                 self.add_toe_kick(i, panel, is_rear=True)
                self.add_double_sided_back(i, panel)
                self.add_closet_opening(i,panel,is_rear=True)
                

class PROMPTS_Opening_Starter(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".island_openings"
    bl_label = "Island Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    tabs = bpy.props.EnumProperty(name="Tabs",
                        items=[('OPENINGS','Opening Sizes','Show the Width x Height x Depth for each opening'),
                               ('CONSTRUCTION','Construction Options','Show Additional Construction Options')],
                        default = 'OPENINGS')
    
    current_location = bpy.props.FloatProperty(name="Current Location", default=0,subtype='DISTANCE')
    left_offset = bpy.props.FloatProperty(name="Left Offset", default=0,subtype='DISTANCE')
    right_offset = bpy.props.FloatProperty(name="Right Offset", default=0,subtype='DISTANCE')
    product_width = bpy.props.FloatProperty(name="Product Width", default=0,subtype='DISTANCE')    
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)
    height = bpy.props.EnumProperty(name="Height",
                          items=common_lists.PANEL_HEIGHTS,
                          default = '2131',
                          update=update_closet_height)
    
    product = None
    
    inserts = []
    
    def check(self, context):
        self.product.obj_x.location.x = self.width
        utils.run_calculators(self.product.obj_bp)
        depth_1 = self.product.get_prompt("Depth 1")
        if not depth_1:
            self.product.obj_y.location.y = -self.depth
        props_closet.update_render_materials(self, context)
        #Hack I Dont know why i need to run calculators twice just for left right side removal
#         utils.run_calculators(self.product.obj_bp)
        return True

    def set_product_defaults(self):
        self.product.obj_bp.location.x = self.selected_location + self.left_offset
        self.product.obj_x.location.x = self.default_width - (self.left_offset + self.right_offset)

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
        opening_height = round(unit.meter_to_millimeter(self.product.obj_z.location.z),0)
        for index, height in enumerate(common_lists.PANEL_HEIGHTS):
            if not opening_height >= int(height[0]):
                exec('self.height = common_lists.PANEL_HEIGHTS[index - 1][0]')                                                                                                                                                                                                        
                break

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        if self.product.obj_bp:
            self.width = math.fabs(self.product.obj_x.location.x)
            new_list = []
            self.inserts = utils.get_insert_bp_list(self.product.obj_bp,new_list)
            self.depth = math.fabs(self.product.obj_y.location.y)
            self.set_default_heights()

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=450)

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
            depth_1.draw_prompt(col)
            depth_2.draw_prompt(col)
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
        props = props_closet.get_scene_props()

        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        row.label("Opening Name:")
        row.label("",icon='BLANK1')
        row.label("Width:")
        
        box = col.box()
        
        for i in range(1,9):
            width = self.product.get_prompt("Opening " + str(i) + " Width")

            if width:
                row = box.row()
                row.label( str(i) + ":")
                if width.equal == False:
                    row.prop(width,'equal',text="")
                else:
                    if self.get_number_of_equal_widths() != 1:
                        row.prop(width,'equal',text="")
                    else:
                        row.label("",icon='BLANK1')
                if width.equal:
                    row.label(str(unit.meter_to_active_unit(width.DistanceValue)) + '"')
                else:
                    row.prop(width,'DistanceValue',text="")   
            
    def draw_construction_options(self,layout):
        box = layout.box()
        
        toe_kick_height = self.product.get_prompt("Toe Kick Height")
        toe_kick_setback = self.product.get_prompt("Toe Kick Setback")
        left_against_wall = self.product.get_prompt("Left Against Wall")
        right_against_wall = self.product.get_prompt("Right Against Wall")
        
        col = box.column(align=True)
        row = col.row()
        row.label("Against Wall:")   
        row.prop(left_against_wall,left_against_wall.prompt_type,text="Left")
        row.prop(right_against_wall,right_against_wall.prompt_type,text="Right")
        #left_against_wall.draw_prompt(row,text="Left",split_text=False)
        #right_against_wall.draw_prompt(row,text="Right",split_text=False)
        
        col = box.column(align=True)
        col.label("Base Options:")        
        # TOE KICK OPTIONS
        if toe_kick_height and toe_kick_setback:
            row = col.row()
            row.label("Toe Kick")
            row.prop(toe_kick_height,toe_kick_height.prompt_type,text="Height")
            row.prop(toe_kick_setback,toe_kick_setback.prompt_type,text="Setback")

        col = box.column(align=True)
        col.label("Top Options:")        

        Countertop_Type = self.product.get_prompt("Countertop Type")
        Countertop_Thickness = self.product.get_prompt("Countertop Thickness")
        HPL_Material_Name = self.product.get_prompt("HPL Material Name")
        HPL_Material_Number = self.product.get_prompt("HPL Material Number")
        Deck_Overhang = self.product.get_prompt("Deck Overhang")
        Side_Deck_Overhang = self.product.get_prompt("Side Deck Overhang")

        No_Countertop = self.product.get_prompt("No Countertop")

        if Deck_Overhang:
            row = col.row()
            Deck_Overhang.draw_prompt(row,text="Opening Overhang")
            Side_Deck_Overhang.draw_prompt(row,text="Side Overhang")
        row = col.row()
        #No_Countertop.draw_prompt(row)
        row.prop(No_Countertop,No_Countertop.prompt_type,text="No Countertop")
        if Countertop_Type and No_Countertop.value() == False:
            Countertop_Type.draw_prompt(col)

    def draw_product_placment(self,layout):
        box = layout.box()
        
        row = box.row(align=True)
        row.label('Location:')
        row.prop(self.product.obj_bp,'location',index=0,text="X")
        row.prop(self.product.obj_bp,'location',index=1,text="Y")
        
        row.label('Rotation:')
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="")
        
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                left_against_wall = self.product.get_prompt("Left Against Wall")
                box = layout.box()
                box.label(self.product.obj_bp.mv.name_object,icon='LATTICE_DATA')
                
                split = box.split(percentage=.5)
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
