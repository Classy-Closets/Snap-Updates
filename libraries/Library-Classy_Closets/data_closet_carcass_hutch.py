import bpy
import math
from mv import unit, fd_types, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_lists

def add_fixed_shelf_machining(part,product,index):
    Width = part.get_var('dim_y','Width')
    Length = part.get_var('dim_x','Length')
    if product:
        obj, left_token = part.add_machine_token('Left Drilling' ,'BORE','5')
        obj, right_token = part.add_machine_token('Right Drilling' ,'BORE','5')
        if index == 1:
            Left_End_Condition = product.get_var("Left End Condition")
            left_token.add_driver(obj,'dim_in_z','IF(Left_End_Condition==3,0,MILLIMETER(15))',[Left_End_Condition])
            right_token.add_driver(obj,'dim_in_z','IF(Left_End_Condition==3,0,MILLIMETER(15))',[Left_End_Condition])
        elif index == product.base_opening_qty + 1:
            Right_End_Condition = product.get_var("Right End Condition")
            left_token.add_driver(obj,'dim_in_z','IF(Right_End_Condition==3,0,MILLIMETER(15))',[Right_End_Condition])
            right_token.add_driver(obj,'dim_in_z','IF(Right_End_Condition==3,0,MILLIMETER(15))',[Right_End_Condition])
        else:
            left_token.dim_in_z = unit.inch(.5)
            right_token.dim_in_z = unit.inch(.5)
    else:
        obj, left_token = part.add_machine_token('Left Drilling' ,'BORE','5')
        obj, right_token = part.add_machine_token('Right Drilling' ,'BORE','5')
        left_token.dim_in_z = unit.inch(.5)
        right_token.dim_in_z = unit.inch(.5)
        
    left_token.dim_in_x = unit.millimeter(9)
    left_token.dim_in_y = unit.millimeter(37)
    left_token.face_bore_dia = 20
    left_token.end_dim_in_x  = unit.millimeter(9)
    left_token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    left_token.add_driver(obj,'distance_between_holes','fabs(Width)-(INCH(1.4567)*2)',[Width])
    left_token.associative_dia = 0
    left_token.associative_depth = 0
    
    right_token.add_driver(obj,'dim_in_x','Length-INCH(.354)',[Length])
    right_token.dim_in_y = unit.millimeter(37)
    right_token.face_bore_dia = 20
    right_token.add_driver(obj,'end_dim_in_x','Length-INCH(.354)',[Length])
    right_token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    right_token.add_driver(obj,'distance_between_holes','fabs(Width)-(INCH(1.4567)*2)',[Width])
    right_token.associative_dia = 0
    right_token.associative_depth = 0
    
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
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Drill_Thru_5,Panel_Thickness,MILLIMETER(15)))',[Drill_Thru_5,Panel_Thickness,Remove_5])
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
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Drill_Thru_5,Panel_Thickness,MILLIMETER(15)))',[Drill_Thru_5,Panel_Thickness,Remove_5])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','IF(Stop_LB==0,Height,Stop_LB)',[Height,Stop_LB])
    token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    token.distance_between_holes = unit.millimeter(32) 
    token.associative_dia = 0 
    token.associative_depth = 0 

    obj, token = part.add_machine_token('Drilling Mid Bottom 5' ,'BORE','5')
    token.dim_in_x = unit.millimeter(9.5)
    token.dim_in_y = unit.inch(12 - 1.4567)
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Add_Mid,IF(Drill_Thru_5,Panel_Thickness,MILLIMETER(15)),0))',[Drill_Thru_5,Add_Mid,Panel_Thickness,Remove_5])
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
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Start_LB>0,IF(Drill_Thru_5,Panel_Thickness,MILLIMETER(15)),0))',[Drill_Thru_5,Panel_Thickness,Remove_5,Start_LB])
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
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Start_LB>0,IF(Drill_Thru_5,Panel_Thickness,MILLIMETER(15)),0))',[Drill_Thru_5,Panel_Thickness,Remove_5,Start_LB])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','Height',[Height])
    token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
    token.distance_between_holes = unit.millimeter(32) 
    token.associative_dia = 0 
    token.associative_depth = 0 

    obj, token = part.add_machine_token('Drilling Mid Top 5' ,'BORE','5')
    token.add_driver(obj,'dim_in_x','Start_LB',[Start_LB])
    token.dim_in_y = unit.inch(12 - 1.4567)
    token.add_driver(obj,'dim_in_z','IF(Remove_5,0,IF(Add_Mid,IF(Start_LB>0,IF(Drill_Thru_5,Panel_Thickness,MILLIMETER(15)),0),0))',[Drill_Thru_5,Panel_Thickness,Remove_5,Add_Mid,Start_LB])
    token.face_bore_dia = 5
    token.add_driver(obj,'end_dim_in_x','Height',[Height])
    token.end_dim_in_y  = unit.inch(12 - 1.4567)
    token.distance_between_holes = unit.millimeter(32) #7
    token.associative_dia = 0 
    token.associative_depth = 0 
    
    if index != 1 and index != product.base_opening_qty + 1:
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
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Drill_Thru_6,Panel_Thickness,MILLIMETER(15)))',[Remove_6,Drill_Thru_6,Panel_Thickness])
        token.face_bore_dia = 5
        token.add_driver(obj,'end_dim_in_x','IF(Stop_LB_6==0,Height,Stop_LB_6)',[Height,Stop_LB_6])
        token.end_dim_in_y  = unit.inch(1.4567)
        token.distance_between_holes = unit.millimeter(32)
        token.associative_dia = 0 
        token.associative_depth = 0 
        
        obj, token = part.add_machine_token('Drilling Rear Bottom 6' ,'BORE','6')
        token.dim_in_x = unit.millimeter(9.5)
        token.add_driver(obj, 'dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Drill_Thru_6,Panel_Thickness,MILLIMETER(15)))',[Remove_6,Drill_Thru_6,Panel_Thickness])
        token.face_bore_dia = 5 
        token.add_driver(obj,'end_dim_in_x','IF(Stop_LB_6==0,Height,Stop_LB_6)',[Height,Stop_LB_6])
        token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.distance_between_holes = unit.millimeter(32) 
        token.associative_dia = 0 
        token.associative_depth = 0 
        
        obj, token = part.add_machine_token('Drilling Mid Bottom 6' ,'BORE','6')
        token.dim_in_x = unit.millimeter(9.5)
        token.dim_in_y = unit.inch(12 - 1.4567)
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Add_Mid_6,IF(Drill_Thru_6,Panel_Thickness,MILLIMETER(15)),0))',[Remove_6,Add_Mid_6,Drill_Thru_6,Panel_Thickness])
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
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Start_LB_6>0,IF(Drill_Thru_6,Panel_Thickness,MILLIMETER(15)),0))',[Remove_6,Drill_Thru_6,Panel_Thickness,Start_LB_6])
        token.face_bore_dia = 5
        token.add_driver(obj,'end_dim_in_x','Height',[Height])
        token.end_dim_in_y  = unit.inch(1.4567)
        token.distance_between_holes = unit.millimeter(32)
        token.associative_dia = 0
        token.associative_depth = 0
        
        obj, token = part.add_machine_token('Drilling Rear Top 6' ,'BORE','6')
        token.add_driver(obj,'dim_in_x','Start_LB_6',[Start_LB_6])
        token.add_driver(obj, 'dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Start_LB_6>0,IF(Drill_Thru_6,Panel_Thickness,MILLIMETER(15)),0))',[Remove_6,Drill_Thru_6,Panel_Thickness,Start_LB_6])
        token.face_bore_dia = 5 
        token.add_driver(obj,'end_dim_in_x','Height',[Height])
        token.add_driver(obj,'end_dim_in_y','fabs(Width)-INCH(1.4567)',[Width])
        token.distance_between_holes = unit.millimeter(32) 
        token.associative_dia = 0
        token.associative_depth = 0
        
        obj, token = part.add_machine_token('Drilling Mid Top 6' ,'BORE','6')
        token.add_driver(obj,'dim_in_x','Start_LB_6',[Start_LB_6])
        token.dim_in_y = unit.inch(12 - 1.4567)
        token.add_driver(obj,'dim_in_z','IF(Remove_6,0,IF(Add_Mid_6,IF(Start_LB_6>0,IF(Drill_Thru_6,Panel_Thickness,MILLIMETER(15)),0),0))',[Remove_6,Drill_Thru_6,Panel_Thickness,Start_LB_6,Add_Mid_6])
        token.face_bore_dia = 5
        token.add_driver(obj,'end_dim_in_x','Height',[Height])
        token.end_dim_in_y  = unit.inch(12 - 1.4567)
        token.distance_between_holes = unit.millimeter(32)
        token.associative_dia = 0
        token.associative_depth = 0

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

#---------PRODUCT TEMPLATES    
    
class Hutch(fd_types.Assembly):

    property_id = props_closet.LIBRARY_NAME_SPACE + ".hutch_prompts"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_hutch"
    type_assembly = "PRODUCT"

    opening_qty = 4
    
    def __init__(self):
        props = props_closet.get_scene_props().closet_defaults
        self.width = unit.inch(18) * self.opening_qty
        self.height = unit.inch(60)
        self.depth = props.panel_depth
    
    def add_prompt_tabs(self):
        self.add_tab(name='Base Opening Widths', tab_type='CALCULATOR', calc_type="XDIM")# 0
        self.add_tab(name='Carcass Options', tab_type='VISIBLE')# 1
        self.add_tab(name='Formulas', tab_type='HIDDEN')# 2            
    
    def add_opening_prompts(self):
        for i in range(1, self.opening_qty + 1):
            self.add_prompt(name="Opening {} Width".format(str(i)),
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=0,
                            equal=True)
             
            self.add_prompt(name="Opening {} Depth".format(str(i)),
                            prompt_type='DISTANCE',
                            value=self.depth,
                            tab_index=1)
        
    def add_carcass_prompts(self):
        self.add_prompt(name='Opening Heights', prompt_type='DISTANCE', value=unit.inch(23.0), tab_index=2)
        self.add_prompt(name="Add Backing", prompt_type='CHECKBOX', value=True, tab_index=1)
        self.add_prompt(name="Panel Thickness", prompt_type='DISTANCE', value=unit.inch(0.75), tab_index=1)
        
        pt = self.get_var('Panel Thickness', 'pt')
        prompts = [pt]
        double_panels = '0'
        
        for i in range(2, self.opening_qty + 1):
            p_name  = "Double Center Panel {}".format(i - 1)
            p_alias = 'dp{}'.format(i - 1)
            
            self.add_prompt(name=p_name,
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=1)
            
            prompts.append(self.get_var(p_name, p_alias))
            double_panels += '+{}'.format(p_alias)
            
        expr = 'pt*({}+1)+pt*({})'.format(str(self.opening_qty), str(double_panels))
        self.calculator_deduction(expr, prompts)            
        
    def add_sides(self):
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z', 'Product_Height')
        Panel_Thickness = self.get_var('Panel Thickness')
        Depth_1 = self.get_var('Opening 1 Depth','Depth_1')
        Last_Depth = self.get_var('Opening {} Depth'.format(self.opening_qty), 'Last_Depth')
        
        left_side = common_parts.add_panel(self)
        left_side.x_dim('Product_Height',[Product_Height])
        left_side.y_dim('-Depth_1',[Depth_1])
        left_side.z_dim('-Panel_Thickness',[Panel_Thickness])
        left_side.x_loc(value=0)
        left_side.y_loc(value=0)
        left_side.z_loc(value=0)
        left_side.x_rot(value=0)
        left_side.y_rot(value=-90)
        left_side.z_rot(value=0)
        left_side.obj_bp.mv.opening_name = str(1)
        
        right_side = common_parts.add_panel(self)
        right_side.x_dim('Product_Height',[Product_Height])
        right_side.y_dim('-Last_Depth',[Last_Depth])
        right_side.z_dim('Panel_Thickness',[Panel_Thickness])
        right_side.x_loc('Product_Width',[Product_Width])
        right_side.y_loc(value=0)
        right_side.z_loc(value=0)
        right_side.x_rot(value=0)
        right_side.y_rot(value=-90)
        right_side.z_rot(value=0)
        right_side.obj_bp.mv.opening_name = str(self.opening_qty + 1)
        
    def add_top(self, index, prev_panel):
        Product_Height = self.get_var('dim_z', 'Product_Height')
        Panel_Thickness = self.get_var('Panel Thickness')
        Width = self.get_var('Opening {} Width'.format(str(index)), "Width")
        Depth = self.get_var('Opening {} Depth'.format(str(index)), "Depth")
        
        top = common_parts.add_shelf(self)
        if prev_panel:
            Prev_Panel_X = prev_panel.get_var('loc_x', 'Prev_Panel_X')
            D_Panel = self.get_var('Double Center Panel {}'.format(str(index - 1)), 'D_Panel')            
            top.x_loc('Prev_Panel_X+IF(D_Panel,Panel_Thickness,0)', [Prev_Panel_X, Panel_Thickness, D_Panel])
        else:
            top.x_loc('Panel_Thickness', [Panel_Thickness]) 
        top.y_loc(value=0)
        top.z_loc('Product_Height-Panel_Thickness', [Product_Height, Panel_Thickness])
        top.x_rot(value=0)
        top.y_rot(value=0)
        top.z_rot(value=0)
        top.x_dim('Width', [Width])
        top.y_dim('-Depth', [Depth])
        top.z_dim('Panel_Thickness', [Panel_Thickness])
    
    def add_bottom(self, index, prev_panel):
        Product_Height = self.get_var('dim_z', 'Product_Height')
        Panel_Thickness = self.get_var('Panel Thickness')
        Opening_Heights = self.get_var('Opening Heights', 'Opening_Heights')
        Width = self.get_var('Opening {} Width'.format(str(index)), 'Width')
        Depth = self.get_var('Opening {} Depth'.format(str(index)), 'Depth')
        
        bottom = common_parts.add_shelf(self)
        if prev_panel:
            Prev_Panel_X = prev_panel.get_var('loc_x', 'Prev_Panel_X')
            D_Panel = self.get_var('Double Center Panel {}'.format(str(index - 1)), 'D_Panel')
            bottom.x_loc('Prev_Panel_X+IF(D_Panel,Panel_Thickness,0)', [Prev_Panel_X, Panel_Thickness, D_Panel])
        else:
            bottom.x_loc('Panel_Thickness', [Panel_Thickness]) 
        bottom.y_loc(value=0)
        bottom.z_loc('Product_Height-Opening_Heights', [Product_Height, Opening_Heights])
        bottom.x_rot(value=0)
        bottom.y_rot(value=0)
        bottom.z_rot(value=0)
        bottom.x_dim('Width', [Width])
        bottom.y_dim('-Depth', [Depth])
        bottom.z_dim('Panel_Thickness', [Panel_Thickness])

    def add_back(self):
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Height = self.get_var('dim_z', 'Product_Height')
        Panel_Thickness = self.get_var('Panel Thickness')
        Opening_Heights = self.get_var('Opening Heights', 'Opening_Heights')
        Add_Backing = self.get_var('Add Backing')
        
        back = common_parts.add_back(self)
        back.x_loc('Panel_Thickness', [Panel_Thickness])
        back.y_loc(value=0)
        back.z_loc(value=0)
        back.x_rot(value=90)
        back.y_rot(value=0)
        back.z_rot(value=0)
        back.x_dim('Product_Width-Panel_Thickness*2', [Product_Width, Panel_Thickness])
        back.y_dim('Product_Height-Opening_Heights', [Product_Height, Opening_Heights])
        back.z_dim('Panel_Thickness', [Panel_Thickness])
        back.prompt('Hide', 'IF(Add_Backing,False,True)', [Add_Backing])
        
    def add_panel(self, index, prev_panel):
        Product_Height = self.get_var('dim_z', 'Product_Height')       
        Opening_Heights = self.get_var('Opening Heights', 'Opening_Heights')
        Width = self.get_var('Opening {} Width'.format(str(index-1)), 'Width')
        Depth = self.get_var('Opening {} Depth'.format(str(index-1)), 'Depth')
        Next_Depth = self.get_var('Opening {} Depth'.format(str(index)), 'Next_Depth')
        Panel_Thickness = self.get_var('Panel Thickness')
        D_Panel = self.get_var('Double Center Panel {}'.format(str(index-1)), 'D_Panel')
        Prev_D_Panel = self.get_var('Double Center Panel {}'.format(str(index-2)), 'Prev_D_Panel')
        
        panel = common_parts.add_panel(self)
        if prev_panel:
            Prev_Panel_X = prev_panel.get_var('loc_x', 'Prev_Panel_X')
            panel.x_loc('Prev_Panel_X+Width+Panel_Thickness*IF(Prev_D_Panel,2,1)', 
                        [Prev_Panel_X, Panel_Thickness, Width, Prev_D_Panel])
        else:
            panel.x_loc('Panel_Thickness*2+Width', [Panel_Thickness, Width])
        panel.y_loc(value=0)
        panel.z_loc('Product_Height-Opening_Heights', [Product_Height, Opening_Heights])
        panel.x_rot(value=0)
        panel.y_rot(value=-90)
        panel.z_rot(value=0)
        panel.x_dim('Opening_Heights', [Opening_Heights])
        panel.y_dim('IF(D_Panel,-Depth,-max(Depth,Next_Depth))', [Depth, Next_Depth, D_Panel])
        panel.z_dim('Panel_Thickness', [Panel_Thickness])

        panel_2 = common_parts.add_panel(self)
        if prev_panel:
            panel_2.x_loc('Prev_Panel_X+Width+Panel_Thickness*IF(Prev_D_Panel,3,2)', 
                          [Prev_Panel_X, Panel_Thickness, Width, Prev_D_Panel])
        else:
            panel_2.x_loc('Panel_Thickness*3+Width', [Panel_Thickness, Width])
        panel_2.y_loc(value=0)
        panel_2.z_loc('Product_Height-Opening_Heights', [Product_Height, Opening_Heights])
        panel_2.x_rot(value=0)
        panel_2.y_rot(value=-90)
        panel_2.z_rot(value=0)
        panel_2.x_dim('Opening_Heights', [Opening_Heights])
        panel_2.y_dim('-Next_Depth', [Next_Depth])
        panel_2.z_dim('Panel_Thickness', [Panel_Thickness])
        panel_2.prompt('Hide', 'IF(D_Panel,False,True)', [D_Panel])  
        
        return panel
                
    def add_hutch_opening(self, index, prev_panel):
        Product_Height = self.get_var('dim_z', 'Product_Height')
        Opening_Heights = self.get_var('Opening Heights', 'Opening_Heights')     
        Width = self.get_var('Opening {} Width'.format(str(index)), 'Width')
        Depth = self.get_var('Opening {} Depth'.format(str(index)), 'Depth')
        Prev_D_Panel = self.get_var('Double Center Panel {}'.format(str(index-1)), 'Prev_D_Panel')
        Panel_Thickness = self.get_var('Panel Thickness')
        
        opening = common_parts.add_section_opening(self)
        opening.set_name("opening {}".format(str(index)))
        if prev_panel:
            Prev_Panel_X = prev_panel.get_var('loc_x', 'Prev_Panel_X')
            opening.x_loc('Prev_Panel_X+IF(Prev_D_Panel,Panel_Thickness,0)', [Prev_Panel_X, Prev_D_Panel, Panel_Thickness])
        else:
            opening.x_loc('Panel_Thickness', [Panel_Thickness])
        opening.y_loc('-Depth', [Depth])
        opening.z_loc('Product_Height-Opening_Heights+Panel_Thickness', [Product_Height, Opening_Heights, Panel_Thickness])
        opening.x_rot(value=0)
        opening.y_rot(value=0)
        opening.z_rot(value=0)
        opening.x_dim('Width', [Width])
        opening.y_dim('Depth', [Depth])
        opening.z_dim('Opening_Heights-Panel_Thickness*2', [Opening_Heights, Panel_Thickness])

    def draw(self):
        defaults = props_closet.get_scene_props().closet_defaults
        
        self.create_assembly()
        self.obj_bp.mv.product_type = "Closet"
        props = props_closet.get_object_props(self.obj_bp)
        props.is_closet = True
        props.is_hutch = True
        
        if defaults.export_subassemblies:
            self.obj_bp.mv.export_product_subassemblies = True              
        
        self.add_prompt_tabs()
        self.add_carcass_prompts()
        self.add_opening_prompts()
        
        panel = None
        
        self.add_sides()
        self.add_back()
        self.add_top(1, panel)
        self.add_bottom(1, panel)
        self.add_hutch_opening(1, panel)        
        
        for i in range (2, self.opening_qty + 1):
            panel = self.add_panel(i, panel)
            self.add_top(i, panel)
            self.add_bottom(i, panel)
            self.add_hutch_opening(i, panel)
            
class PROMPTS_Hutch(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".hutch_prompts"
    bl_label = "Hutch Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    tabs = bpy.props.EnumProperty(name="Tabs",
                        items=[('OPENINGS','Opening Sizes','Show the Width x Height x Depth for each opening'),
                               ('CONSTRUCTION','Construction Options','Show Additional Construction Options')],
                               #('MACHINING','Machining Options','Machining Options')],
                        default = 'OPENINGS')
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)
    depth_1 = bpy.props.FloatProperty(name="Depth 1",unit='LENGTH',precision=4)
    depth_2 = bpy.props.FloatProperty(name="Depth 2",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height", unit='LENGTH', precision=4)

    Opening_1_Height = bpy.props.FloatProperty(name="Opening 1 Height", unit='LENGTH', precision=4)
    Opening_2_Height = bpy.props.FloatProperty(name="Opening 2 Height", unit='LENGTH', precision=4)
    Opening_3_Height = bpy.props.FloatProperty(name="Opening 3 Height", unit='LENGTH', precision=4)
    Opening_4_Height = bpy.props.FloatProperty(name="Opening 4 Height", unit='LENGTH', precision=4)
    Opening_5_Height = bpy.props.FloatProperty(name="Opening 5 Height", unit='LENGTH', precision=4)
    Opening_6_Height = bpy.props.FloatProperty(name="Opening 6 Height", unit='LENGTH', precision=4)
    Opening_7_Height = bpy.props.FloatProperty(name="Opening 7 Height", unit='LENGTH', precision=4)
    Opening_8_Height = bpy.props.FloatProperty(name="Opening 8 Height", unit='LENGTH', precision=4)
    
    Hutch_Height = bpy.props.EnumProperty(name="Hutch Height",
                                          items=common_lists.PANEL_HEIGHTS)       
    
    Opening_Heights = bpy.props.EnumProperty(name="Opening Heights",
                                             items=common_lists.PANEL_HEIGHTS)        
    
    Left_End_Condition = bpy.props.EnumProperty(name="Left Side",
                                       items=common_lists.END_CONDITIONS,
                                       default = 'WP')
    
    Right_End_Condition = bpy.props.EnumProperty(name="Right Side",
                                        items=common_lists.END_CONDITIONS,
                                        default = 'WP')
    
    product = None
    
    inserts = []
    
    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        self.product.obj_x.location.x = self.width
        self.product.obj_z.location.z = float(self.Hutch_Height) / 1000

        opening_heights = self.product.get_prompt("Opening Heights")
         
        if opening_heights:
            opening_heights.set_value(float(self.Opening_Heights) / 1000)

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
        height = self.product.get_prompt("Opening Heights")
        if height:
            open1_p_height = round(height.DistanceValue*1000,0)
            for index, height in enumerate(common_lists.PANEL_HEIGHTS):
                if not open1_p_height >= int(height[0]):
                    self.Opening_Heights = common_lists.PANEL_HEIGHTS[index - 1][0]
                    break
        
        hutch_height = round(self.product.obj_z.location.z*1000,0)
        for index, height in enumerate(common_lists.PANEL_HEIGHTS):
            if not hutch_height >= int(height[0]):
                self.Hutch_Height = common_lists.PANEL_HEIGHTS[index - 1][0]
                break
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        if self.product.obj_bp:
            self.set_default_heights()
            self.width = math.fabs(self.product.obj_x.location.x)
            self.height = math.fabs(self.product.obj_z.location.z)
            new_list = []
            self.inserts = utils.get_insert_bp_list(self.product.obj_bp, new_list)
            
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(480))

    def convert_to_height(self,number):
        for index, height in enumerate(common_lists.PANEL_HEIGHTS):
            if not number * 1000 >= float(height[0]):
                return common_lists.PANEL_HEIGHTS[index - 1][0]

    def draw_product_size(self,layout):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row.label('Width: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row.label('Width:')
            row.prop(self,'width',text="")
            
        row = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row.label('Height: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z))))
        else:
            row.label('Height:')
            row.prop(self,'Hutch_Height',text="")   
        
        row = col.row(align=True)
        row.label('Opening Heights:')
        row.prop(self,"Opening_Heights",text="")
        
        row = box.row(align=True)
        row.label("Location:")
        row.prop(self.product.obj_bp,'location',index=0,text="X")
        row.prop(self.product.obj_bp,'location',index=1,text="Y")
        row.prop(self.product.obj_bp,'location',index=2,text="Z")

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

        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        row.label("Opening Name:")
        row.label("",icon='BLANK1')
        row.label("Width:")
        #row.label("Height:")
        row.label("Depth:")
        
        box = col.box()
        
        for i in range(1,9):
            width = self.product.get_prompt("Opening " + str(i) + " Width")
            depth = self.product.get_prompt("Opening " + str(i) + " Depth")  
            if width:
                row = box.row()
                row.label(str(i) + " Section:")
                row.prop(width,'equal',text="")
                if width.equal:
                    row.label(str(unit.meter_to_active_unit(width.DistanceValue)) + '"')
                else:
                    row.prop(width,'DistanceValue',text="")
                    
                #row.prop(self,'Opening_' + str(i) + '_Height',text="")
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
        main_col = layout.column(align=True)
        add_backing = self.product.get_prompt("Add Backing")
        
        box = main_col.box()
        row = box.row()
        row.label("Back Options:")
        row.prop(add_backing, 'CheckBoxValue', text="Add Backing")
            
        for i in range(1, 8):
            d_panel = self.product.get_prompt("Double Center Panel {}".format(str(i)))
            
            if d_panel:
                d_panel.draw_prompt(box)           
            
    def draw_machining_options(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Opening Name:")
        row.label("",icon='BLANK1')
        row.label("Bottom:")
        row.label("Top:")
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
                row.prop(stop_lb,'DistanceValue',text="Stop")
                row.prop(start_lb,'DistanceValue',text="Stop")
                row.separator()
                row.prop(add_mid,'CheckBoxValue',text=" ")

                row.prop(drill_thru_left,'CheckBoxValue',text="")
                row.prop(drill_thru_right,'CheckBoxValue',text=" ")
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
                
                row = box.row()
                self.draw_product_size(row)
                row = box.row()
                row.prop(self,'tabs',expand=True)
                if self.tabs == 'OPENINGS':
                    self.draw_splitter_widths(box)
                elif self.tabs == 'CONSTRUCTION':
                    self.draw_construction_options(box)

class OPERATOR_Place_Hutch(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_hutch"
    bl_label = "Place Hutch"
    bl_description = "This allows you to place a hutch product."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None

    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.assembly = fd_types.Assembly(bp)
        utils.set_wireframe(self.assembly.obj_bp,True)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.assembly:
            utils.delete_object_and_children(self.assembly.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}
    
    def place_on_top_of_product(self,product,sel_assembly):
        scene_props = props_closet.get_scene_props()
        closet_defaults = scene_props.closet_defaults        
        obj_props = props_closet.get_object_props(product.obj_bp)
        sel_assembly_props = props_closet.get_object_props(sel_assembly.obj_bp)
        
        if sel_assembly_props.is_countertop_bp:
            ct_height = sel_assembly.obj_z.location.z
        else:
            ct_height = 0
        
        if product and obj_props.is_closet:
            heights = []
            depths = []
            
            for i in range(1,10):
                height = product.get_prompt("Opening " + str(i) + " Height")
                if height: 
                    heights.append(height.value())
                depth = product.get_prompt("Opening " + str(i) + " Depth")
                if depth: 
                    depths.append(depth.value())
            
            if len(heights) > 0: # Heights List cannot be empty the max function will throw an error
                self.assembly.obj_bp.parent = product.obj_bp
                self.assembly.obj_bp.location.z = max(heights) + ct_height
                self.assembly.obj_x.location.x = product.obj_x.location.x
                self.assembly.obj_z.location.z = unit.millimeter(float(closet_defaults.panel_height)) - max(heights) - ct_height
                utils.run_calculators(self.assembly.obj_bp)
    
    def hutch_drop(self,context,event):
        scene_props = props_closet.get_scene_props()
        closet_defaults = scene_props.closet_defaults
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        sel_product_bp = utils.get_bp(selected_obj,'PRODUCT')
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)
        sel_wall_bp = utils.get_wall_bp(selected_obj)
        
        self.assembly.obj_bp.location.x = 0
        
        if sel_product_bp and sel_assembly_bp:
            
            product = fd_types.Assembly(sel_product_bp)
            sel_assembly = fd_types.Assembly(sel_assembly_bp)
            obj_props = props_closet.get_object_props(product.obj_bp)
            
            if obj_props.is_countertop_bp or obj_props.is_closet:
                self.assembly.obj_bp.mv.dont_export = True # DONT EXPORT TWICE IF PARENTING TO PRODUCT
                self.place_on_top_of_product(product, sel_assembly)
                
        elif sel_wall_bp:
            loc_pos = sel_wall_bp.matrix_world.inverted() * selected_point
            
            self.assembly.obj_bp.parent = sel_wall_bp
            self.assembly.obj_bp.location.z = 0
            self.assembly.obj_bp.location.y = 0
            self.assembly.obj_bp.location.x = loc_pos[0]
            self.assembly.obj_bp.mv.dont_export = False # EXPORT IF PARENTING TO WALL
                
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            utils.set_wireframe(self.assembly.obj_bp,False)
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            context.scene.objects.active = self.assembly.obj_bp
            self.assembly.obj_bp.select = True
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.hutch_drop(context,event)

bpy.utils.register_class(PROMPTS_Hutch)
bpy.utils.register_class(OPERATOR_Place_Hutch)
