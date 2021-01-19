import bpy
import math
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

def update_closet_height(self,context):
    ''' EVENT changes height for all closet openings
    '''

    if self.init_height_list:return

    self.Opening_1_Height = self.height
    self.Opening_2_Height = self.height
    self.Opening_3_Height = self.height
    self.Opening_4_Height = self.height
    self.Opening_5_Height = self.height
    self.Opening_6_Height = self.height
    self.Opening_7_Height = self.height
    self.Opening_8_Height = self.height
    self.Opening_9_Height = self.height
    obj_product_bp = utils.get_bp(context.active_object,'PRODUCT')
    product = fd_types.Assembly(obj_product_bp)

    for i in range(1,10):
        opening_height = product.get_prompt("Opening " + str(i) + " Height")
        if opening_height:
            opening_height.set_value(unit.millimeter(float(self.height)))


class PanelHeights:
    def __init__(self, start, max, start_hole_amt):
        self.max = max
        self.start = start
        self.hole_amt = start_hole_amt
    
    def __iter__(self):
        self.num = self.start
        return self
        
    def __next__(self):
        if(self.num > self.max):
            raise StopIteration

        mm = self.num
        inch = round(self.num/25.4,2)
        name = '{}H-{}"'.format(str(self.hole_amt),str(inch))
        self.num += 32
        self.hole_amt += 1

        return ((str(mm), name, ""))


def get_panel_heights(self, context):
    mat_type = context.scene.db_materials.materials.get_mat_type()
    start = 115 #Millimeter
    max_height = 2419 #Millimeter
    start_hole_amt = 3
    
    if mat_type.name == 'Oversized Material' or mat_type.type_code == 1:
        mat_color = mat_type.get_mat_color()
        max_height = mat_color.oversize_max_len

    panel_heights = PanelHeights(start, max_height, start_hole_amt)
    panel_heights_iter = iter(panel_heights)
    panel_heights_list = list(panel_heights_iter)

    return panel_heights_list


class Closet_Carcass(fd_types.Assembly):
    
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".openings"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'

    opening_qty = 4
    
    is_hanging = False
    
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.width = unit.inch(18) * self.opening_qty
        if self.is_hanging:
            self.height = defaults.hanging_height
        else:
            self.height = unit.millimeter(float(defaults.panel_height))
        self.depth = defaults.panel_depth           
    
    def add_opening_prompts(self):
        props = props_closet.get_scene_props().closet_defaults
        
        self.add_tab(name='Opening Widths',tab_type='CALCULATOR',calc_type="XDIM") #0
        self.add_tab(name='Carcass Options',tab_type='VISIBLE') #1
        
        if self.is_hanging:
            floor_mounted = False
            panel_height = props.hanging_panel_height
        else:
            floor_mounted = True
            panel_height = props.panel_height        
         
        for i in range(1,self.opening_qty+1):
            self.add_prompt(name="Opening " + str(i) + " Width",
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=0,
                            equal=True)
            
            self.add_prompt(name="Opening " + str(i) + " Depth",
                            prompt_type='DISTANCE',
                            value=self.depth,
                            tab_index=1)
            
            self.add_prompt(name="Opening " + str(i) + " Height",
                            prompt_type='DISTANCE',
                            value=unit.millimeter(float(panel_height)),
                            tab_index=1)
    
            self.add_prompt(name="Opening " + str(i) + " Floor Mounted",
                               prompt_type='CHECKBOX',
                               value=floor_mounted,
                               tab_index=1)

            self.add_prompt(
                name="Opening " + str(i) + " Top Backing Thickness",
                prompt_type='COMBOBOX',
                items=['1/4"', '3/4"'],
                columns=2,
                value=0,
                tab_index=1
            )

            self.add_prompt(
                name="Opening " + str(i) + " Center Backing Thickness",
                prompt_type='COMBOBOX',
                items=['1/4"', '3/4"'],
                columns=2,                
                value=0,
                tab_index=1
            )

            self.add_prompt(
                name="Opening " + str(i) + " Bottom Backing Thickness",
                prompt_type='COMBOBOX',
                items=['1/4"', '3/4"'],
                columns=2,
                value=0,
                tab_index=1
            )

        self.add_tab(name='Machining Options',tab_type='VISIBLE') #2
        
        for i in range(1,self.opening_qty+1):

            self.add_prompt(name="Opening " + str(i) + " Stop LB",
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=2)
            
            self.add_prompt(name="Opening " + str(i) + " Start LB",
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=2)
            
            self.add_prompt(name="Opening " + str(i) + " Add Mid Drilling",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
            
            self.add_prompt(name="Opening " + str(i) + " Drill Thru Left",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
        
            self.add_prompt(name="Opening " + str(i) + " Drill Thru Right",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
        
            self.add_prompt(name="Opening " + str(i) + " Remove Left Drill",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
        
            self.add_prompt(name="Opening " + str(i) + " Remove Right Drill",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
    
    def set_panel_prompts(self, panel):
        
        loc_z = panel.get_var("loc_z")
        First_Rear_Notch_Height = self.get_var('First Rear Notch Height')
        First_Rear_Notch_Depth = self.get_var('First Rear Notch Depth')
        Second_Rear_Notch_Height = self.get_var('Second Rear Notch Height')
        Second_Rear_Notch_Depth = self.get_var('Second Rear Notch Depth')
            
        panel.prompt("First Rear Notch Height",'IF(loc_z<INCH(1),First_Rear_Notch_Height,0)',[loc_z,First_Rear_Notch_Height])
        panel.prompt("First Rear Notch Depth",'IF(loc_z<INCH(1),First_Rear_Notch_Depth,0)',[loc_z,First_Rear_Notch_Depth])
        panel.prompt("Second Rear Notch Height",'IF(loc_z<INCH(1),Second_Rear_Notch_Height,0)',[loc_z,Second_Rear_Notch_Height])
        panel.prompt("Second Rear Notch Depth",'IF(loc_z<INCH(1),Second_Rear_Notch_Depth,0)',[loc_z,Second_Rear_Notch_Depth])
        
    def add_sides(self):
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Width = self.get_var('dim_x','Product_Width')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Right_Side_Wall_Filler = self.get_var('Right Side Wall Filler')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Extend_Left_Side = self.get_var('Extend Left Side')
        Extend_Right_Side = self.get_var('Extend Right Side')
        Height_Left_Side = self.get_var('Height Left Side')
        Height_Right_Side = self.get_var('Height Right Side')
        Loc_Left_Side = self.get_var('Loc Left Side')
        Loc_Right_Side = self.get_var('Loc Right Side') 
        Left_End_Deduction = self.get_var('Left End Deduction')
        Right_End_Deduction = self.get_var('Right End Deduction')        
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Dog_Ear_Each = self.get_var('Dog Ear Each')
        
        Depth_1 = self.get_var('Opening 1 Depth','Depth_1')
        Height_1 = self.get_var('Opening 1 Height','Height_1')
        Floor_1 = self.get_var('Opening 1 Floor Mounted','Floor_1')
        Last_Depth = self.get_var('Opening ' + str(self.opening_qty) + ' Depth',"Last_Depth")
        Last_Height = self.get_var('Opening ' + str(self.opening_qty) + ' Height',"Last_Height")
        Last_Floor = self.get_var('Opening ' + str(self.opening_qty) + ' Floor Mounted',"Last_Floor")
        Add_Backing = self.get_var('Opening ' + str(1) + ' Add Backing', 'Add_Backing')
        Left_End_Condition = self.get_var('Left End Condition')
        Right_End_Condition = self.get_var('Right End Condition')
        # Stop_LB_First_Opening = self.get_var("Opening 1 Stop LB","Stop_LB_First_Opening")
        # Start_LB_First_Opening = self.get_var("Opening 1 Start LB","Start_LB_First_Opening")
        # Stop_LB_Last_Opening = self.get_var("Opening " + str(self.opening_qty) + " Stop LB","Stop_LB_Last_Opening")
        # Start_LB_Last_Opening = self.get_var("Opening " + str(self.opening_qty) + " Start LB","Start_LB_Last_Opening")

        #Left side panel is always '1'
        Front_Angle_Height = self.get_var('Front Angle ' + str(1) + ' Height', 'Front_Angle_Height')
        Front_Angle_Depth = self.get_var('Front Angle ' + str(1) + ' Depth', 'Front_Angle_Depth')
        Rear_Angle_Height = self.get_var('Rear Angle ' + str(1) + ' Height', 'Rear_Angle_Height')
        Rear_Angle_Depth = self.get_var('Rear Angle ' + str(1) + ' Depth', 'Rear_Angle_Depth')  

        Front_Angle_Height_All = self.get_var('Front Angle Height', 'Front_Angle_Height_All')
        Front_Angle_Depth_All = self.get_var('Front Angle Depth', 'Front_Angle_Depth_All')
        Rear_Angle_Height_All = self.get_var('Rear Angle Height', 'Rear_Angle_Height_All')
        Rear_Angle_Depth_All = self.get_var('Rear Angle Depth', 'Rear_Angle_Depth_All')          
        
        left_filler = common_parts.add_filler(self)
        left_filler.x_dim('IF(Extend_Left_Side,Height_1+Height_Left_Side,Height_1)',[Height_1,Height_Left_Side,Extend_Left_Side])
        left_filler.y_dim('-Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_filler.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
        left_filler.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_filler.y_loc("-Depth_1+Left_End_Deduction", [Depth_1, Left_End_Deduction])
        left_filler.z_loc('IF(Floor_1,Toe_Kick_Height,Product_Height-Height_1-IF(Extend_Left_Side,Height_Left_Side,0))',[Loc_Left_Side,Floor_1,Height_Left_Side,Product_Height,Height_1,Toe_Kick_Height,Extend_Left_Side])
        left_filler.x_rot(value = 0)
        left_filler.y_rot(value = -90)
        left_filler.z_rot(value = -90)
        left_filler.prompt('Hide','IF(OR(Left_Side_Wall_Filler==0,Left_End_Condition==3),True,False)',[Left_Side_Wall_Filler, Left_End_Condition])
        left_side = common_parts.add_panel(self)
        left_side.x_dim('IF(Extend_Left_Side,Height_1+Height_Left_Side,Height_1)',[Height_1,Height_Left_Side,Extend_Left_Side])
        left_side.y_dim('-Depth_1+Left_End_Deduction',[Depth_1,Left_End_Deduction])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_side.y_loc(value = 0)
        left_side.z_loc('IF(Extend_Left_Side,(Product_Height-Height_1-Height_Left_Side),IF(Floor_1,Toe_Kick_Height,Product_Height-Height_1))',[Loc_Left_Side,Floor_1,Height_Left_Side,Product_Height,Height_1,Toe_Kick_Height,Extend_Left_Side])
        left_side.x_rot(value = 0)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
        left_side.prompt('Hide','IF(Left_End_Condition==3,True,False)',[Left_End_Condition])
        left_side.prompt('Is Left End Panel','IF(Left_End_Condition==0,True,False)',[Left_End_Condition])
        left_side.prompt('Left Depth','0',[])
        left_side.prompt('Right Depth','Depth_1',[Depth_1])
        # left_side.prompt('Stop Drilling Bottom Left','0',[])
        # left_side.prompt('Stop Drilling Top Left','0',[])
        # left_side.prompt('Stop Drilling Bottom Right','Stop_LB_First_Opening',[Stop_LB_First_Opening])
        # left_side.prompt('Stop Drilling Top Right','Start_LB_First_Opening',[Start_LB_First_Opening])
        left_side.prompt('Place Hanging Hardware On Right',value=True)

        left_side.prompt("Front Chamfer Height",'IF(Dog_Ear_Each,Front_Angle_Height,Front_Angle_Height_All)',[Dog_Ear_Each, Front_Angle_Height_All, Front_Angle_Height])
        left_side.prompt("Front Chamfer Depth",'IF(Dog_Ear_Each,Front_Angle_Depth,Front_Angle_Depth_All)',[Dog_Ear_Each, Front_Angle_Depth_All, Front_Angle_Depth])
        left_side.prompt("Rear Chamfer Height",'IF(Dog_Ear_Each,Rear_Angle_Height,Rear_Angle_Height_All)',[Dog_Ear_Each, Rear_Angle_Height_All, Rear_Angle_Height])
        left_side.prompt("Rear Chamfer Depth",'IF(Dog_Ear_Each,Rear_Angle_Depth,Rear_Angle_Depth_All)',[Dog_Ear_Each, Rear_Angle_Depth_All, Rear_Angle_Depth])
        left_side.prompt("CatNum",'IF(Front_Angle_Height>INCH(0),1017,1004)',[Front_Angle_Height])

        self.set_panel_prompts(left_side)

        Add_Backing = self.get_var('Opening ' + str(self.opening_qty) + ' Add Backing', 'Add_Backing')

        right_filler = common_parts.add_filler(self)
        right_filler.x_dim('IF(Extend_Right_Side,Last_Height+Height_Right_Side,Last_Height)',[Last_Height,Height_Right_Side,Extend_Right_Side])
        right_filler.y_dim('Right_Side_Wall_Filler',[Right_Side_Wall_Filler])
        right_filler.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_filler.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
        right_filler.y_loc("-Last_Depth+Right_End_Deduction", [Last_Depth, Right_End_Deduction])
        right_filler.z_loc('IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height-IF(Extend_Right_Side,Height_Right_Side,0))',[Loc_Right_Side,Height_Right_Side,Last_Floor,Product_Height,Toe_Kick_Height,Last_Height,Extend_Right_Side])
        right_filler.x_rot(value = 0)
        right_filler.y_rot(value = -90)
        right_filler.z_rot(value = -90)
        right_filler.prompt('Hide','IF(OR(Right_Side_Wall_Filler==0,Right_End_Condition==3),True,False)',[Right_Side_Wall_Filler, Right_End_Condition])
        right_side = common_parts.add_panel(self)
        right_side.x_dim('IF(Extend_Right_Side,Last_Height+Height_Right_Side,Last_Height)',[Last_Height,Height_Right_Side,Extend_Right_Side,Last_Floor])
        right_side.y_dim('-Last_Depth+Right_End_Deduction',[Last_Depth,Right_End_Deduction])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
        right_side.y_loc(value = 0)
        right_side.z_loc('IF(Extend_Right_Side,(Product_Height-Last_Height-Height_Right_Side),IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height))',[Loc_Right_Side,Height_Right_Side,Last_Floor,Product_Height,Toe_Kick_Height,Last_Height,Extend_Right_Side])
        right_side.x_rot(value = 0)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)
        right_side.prompt('Hide','IF(Right_End_Condition==3,True,False)',[Right_End_Condition])
        right_side.prompt('Is Right End Panel','IF(Right_End_Condition==0,True,False)',[Right_End_Condition])
        right_side.prompt('Left Depth','Last_Depth',[Last_Depth])
        right_side.prompt('Right Depth','0',[])
        # right_side.prompt('Stop Drilling Bottom Left','Stop_LB_Last_Opening',[Stop_LB_Last_Opening])
        # right_side.prompt('Stop Drilling Top Left','Start_LB_Last_Opening',[Start_LB_Last_Opening])
        # right_side.prompt('Stop Drilling Bottom Right','0',[])
        # right_side.prompt('Stop Drilling Top Right','0',[])

        #Right side panel is always 'self.opening_qty + 1' (with 4 openings the 5th panel is the right side and last panel)
        Front_Angle_Height = self.get_var('Front Angle ' + str(self.opening_qty+1) + ' Height', 'Front_Angle_Height')
        Front_Angle_Depth = self.get_var('Front Angle ' + str(self.opening_qty+1) + ' Depth', 'Front_Angle_Depth')
        Rear_Angle_Height = self.get_var('Rear Angle ' + str(self.opening_qty+1) + ' Height', 'Rear_Angle_Height')
        Rear_Angle_Depth = self.get_var('Rear Angle ' + str(self.opening_qty+1) + ' Depth', 'Rear_Angle_Depth')

        right_side.prompt("Front Chamfer Height",'IF(Dog_Ear_Each,Front_Angle_Height,Front_Angle_Height_All)',[Dog_Ear_Each, Front_Angle_Height_All, Front_Angle_Height])
        right_side.prompt("Front Chamfer Depth",'IF(Dog_Ear_Each,Front_Angle_Depth,Front_Angle_Depth_All)',[Dog_Ear_Each, Front_Angle_Depth_All, Front_Angle_Depth])
        right_side.prompt("Rear Chamfer Height",'IF(Dog_Ear_Each,Rear_Angle_Height,Rear_Angle_Height_All)',[Dog_Ear_Each, Rear_Angle_Height_All, Rear_Angle_Height])
        right_side.prompt("Rear Chamfer Depth",'IF(Dog_Ear_Each,Rear_Angle_Depth,Rear_Angle_Depth_All)',[Dog_Ear_Each, Rear_Angle_Depth_All, Rear_Angle_Depth])
        right_side.prompt("CatNum",'IF(Front_Angle_Height>INCH(0),1017,1004)',[Front_Angle_Height])

        self.set_panel_prompts(right_side)

    def add_panel(self,index,previous_panel):
        PH = self.get_var('dim_z','PH')
        Width = self.get_var('Opening ' + str(index-1) + ' Width',"Width")
        Depth = self.get_var('Opening ' + str(index-1) + ' Depth',"Depth")
        H = self.get_var('Opening ' + str(index-1) + ' Height',"H")
        Floor = self.get_var('Opening ' + str(index-1) + ' Floor Mounted',"Floor")
        Next_Floor = self.get_var('Opening ' + str(index) + ' Floor Mounted',"Next_Floor")
        Next_Depth = self.get_var('Opening ' + str(index) + ' Depth',"Next_Depth")
        NH = self.get_var('Opening ' + str(index) + ' Height',"NH")
        # Stop_LB_Left_Opening = self.get_var("Opening " + str(index-1) + " Stop LB","Stop_LB_Left_Opening")
        # Start_LB_Left_Opening = self.get_var("Opening " + str(index-1) + " Start LB","Start_LB_Left_Opening")        
        # Stop_LB_Right_Opening = self.get_var("Opening " + str(index) + " Stop LB","Stop_LB_Right_Opening")
        # Start_LB_Right_Opening = self.get_var("Opening " + str(index) + " Start LB","Start_LB_Right_Opening")

        Panel_Thickness = self.get_var('Panel Thickness')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Dog_Ear_Each = self.get_var('Dog Ear Each')

        #In between panels can reference 'index' here
        Front_Angle_Height = self.get_var('Front Angle ' + str(index) + ' Height', 'Front_Angle_Height')
        Front_Angle_Depth = self.get_var('Front Angle ' + str(index) + ' Depth', 'Front_Angle_Depth')
        Rear_Angle_Height = self.get_var('Rear Angle ' + str(index) + ' Height', 'Rear_Angle_Height')
        Rear_Angle_Depth = self.get_var('Rear Angle ' + str(index) + ' Depth', 'Rear_Angle_Depth') 

        Front_Angle_Height_All = self.get_var('Front Angle Height', 'Front_Angle_Height_All')
        Front_Angle_Depth_All = self.get_var('Front Angle Depth', 'Front_Angle_Depth_All')
        Rear_Angle_Height_All = self.get_var('Rear Angle Height', 'Rear_Angle_Height_All')
        Rear_Angle_Depth_All = self.get_var('Rear Angle Depth', 'Rear_Angle_Depth_All')           
        
        panel = common_parts.add_panel(self)
        if previous_panel:
            Prev_Panel_X = previous_panel.get_var("loc_x",'Prev_Panel_X')
            Left_Side_Thickness = self.get_var('Left_Side_Thickness')
            panel.x_loc('Prev_Panel_X+Panel_Thickness+Width',[Prev_Panel_X,Panel_Thickness,Width])
        else:
            Left_Side_Thickness = self.get_var('Left Side Thickness')
            panel.x_loc('Left_Side_Thickness+Width+Left_Side_Wall_Filler+Panel_Thickness',
                        [Left_Side_Thickness,Width,Left_Side_Wall_Filler,Panel_Thickness])

        panel.y_loc(value = 0)
        panel.z_loc('min(IF(Floor,Toe_Kick_Height,IF(Next_Floor,Toe_Kick_Height,PH-H)),IF(Next_Floor,Toe_Kick_Height,IF(Floor,Toe_Kick_Height,PH-NH)))',
                    [Floor,Next_Floor,Toe_Kick_Height,H,PH,NH])
        panel.x_rot(value = 0)
        panel.y_rot(value = -90)
        panel.z_rot(value = 0)
        panel.x_dim('max(IF(Floor,H,IF(Next_Floor,PH-Toe_Kick_Height,H)),IF(Next_Floor,NH,IF(Floor,PH-Toe_Kick_Height,NH)))',
                    [Floor,Next_Floor,PH,H,NH,Toe_Kick_Height]) 
        panel.y_dim('-max(Depth,Next_Depth)',[Depth,Next_Depth])
        panel.z_dim('Panel_Thickness',[Panel_Thickness])
        panel.prompt('Left Depth','Depth',[Depth])
        panel.prompt('Right Depth','Next_Depth',[Next_Depth])
        # panel.prompt('Stop Drilling Bottom Left','Stop_LB_Left_Opening',[Stop_LB_Left_Opening])
        # panel.prompt('Stop Drilling Top Left','Start_LB_Left_Opening',[Start_LB_Left_Opening])
        # panel.prompt('Stop Drilling Bottom Right','Stop_LB_Right_Opening',[Stop_LB_Right_Opening])
        # panel.prompt('Stop Drilling Top Right','Start_LB_Right_Opening',[Start_LB_Right_Opening])

        panel.prompt("Front Chamfer Height",'IF(Dog_Ear_Each,Front_Angle_Height,Front_Angle_Height_All)',[Dog_Ear_Each, Front_Angle_Height_All, Front_Angle_Height])
        panel.prompt("Front Chamfer Depth",'IF(Dog_Ear_Each,Front_Angle_Depth,Front_Angle_Depth_All)',[Dog_Ear_Each, Front_Angle_Depth_All, Front_Angle_Depth])
        panel.prompt("Rear Chamfer Height",'IF(Dog_Ear_Each,Rear_Angle_Height,Rear_Angle_Height_All)',[Dog_Ear_Each, Rear_Angle_Height_All, Rear_Angle_Height])
        panel.prompt("Rear Chamfer Depth",'IF(Dog_Ear_Each,Rear_Angle_Depth,Rear_Angle_Depth_All)',[Dog_Ear_Each, Rear_Angle_Depth_All, Rear_Angle_Depth])
        panel.prompt("CatNum",'IF(Front_Angle_Height>INCH(0),1017,1004)',[Front_Angle_Height])

        self.set_panel_prompts(panel)
        return panel
    
    def add_plant_on_top(self,i,panel):
        """This function is not being used.

        'scene.lm_closets.use_plant_on_top' is set to False by default
        and is hidden from the closet options panel. 'add_shelf' function
        adds the top and bottom KD shelves.
        """
        Product_Height = self.get_var('dim_z','Product_Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Depth = self.get_var('Opening ' + str(i) + ' Depth','Depth')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        P_Depth = self.get_var('Opening ' + str(i-1) + ' Depth','P_Depth') 
        P_Height = self.get_var('Opening ' + str(i-1) + ' Height','P_Height')    
        N_Depth = self.get_var('Opening ' + str(i+1) + ' Depth','N_Depth') 
        N_Height = self.get_var('Opening ' + str(i+1) + ' Height','N_Height')       
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
        Add_Backing = self.get_var('Add Backing')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        PT = self.get_var('Panel Thickness','PT')
        Rear_Angle_Depth = self.get_var('Rear Angle Depth')
        Front_Angle_Depth = self.get_var('Front Angle Depth')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Right_Side_Wall_Filler = self.get_var('Right Side Wall Filler')
        Left_End_Condition = self.get_var('Left End Condition')
        Right_End_Condition = self.get_var('Right End Condition')
        Remove_Top_Shelf = self.get_var('Remove Top Shelf')  
        
        top = common_parts.add_plant_on_top(self)
        top.obj_bp.mv.opening_name = str(i)
        if i == 1:
            # FIRST
            left_offset = "IF(Left_End_Condition==3,0,PT)"
            right_offset = "IF(AND(N_Depth==Depth,N_Height==Height),PT/2,IF(OR(N_Depth<Depth,N_Height<Height),PT,0))"
            top.x_loc(value = 0)
            top.x_dim('Width+Left_Side_Wall_Filler+' + left_offset + '+' + right_offset,[Width,Left_Side_Wall_Filler,Depth,N_Depth,N_Height,Height,PT,Left_End_Condition])
        elif i == self.opening_qty:
            # LAST
            X_Loc = panel.get_var('loc_x','X_Loc')
            left_offset = "IF(AND(P_Depth==Depth,P_Height==Height),PT/2,IF(OR(P_Depth<Depth,P_Height<Height),PT,0))"
            right_offset = "IF(Right_End_Condition==3,0,PT)"
            top.x_loc("X_Loc-" + left_offset,[X_Loc,P_Depth,Depth,P_Height,Height,PT])
            top.x_dim('Width+Right_Side_Wall_Filler+' + right_offset + '+' + left_offset,[Width,Right_Side_Wall_Filler,Depth,P_Depth,P_Height,Height,PT,Right_End_Condition])
        else:
            # MIDDLE
            X_Loc = panel.get_var('loc_x','X_Loc')
            left_offset = "IF(AND(P_Depth==Depth,P_Height==Height),PT/2,IF(OR(P_Depth<Depth,P_Height<Height),PT,0))"
            right_offset = "IF(AND(N_Depth==Depth,N_Height==Height),PT/2,IF(OR(N_Depth<Depth,N_Height<Height),PT,0))"
            top.x_loc("X_Loc-" + left_offset,[X_Loc,P_Depth,Depth,P_Height,Height,PT])
            top.x_dim('Width+' + right_offset + "+" + left_offset,[Width,Left_Side_Wall_Filler,Depth,N_Depth,N_Height,P_Height,P_Depth,Height,PT])
        
        top.y_loc(value = 0)
        top.z_loc('IF(Floor,Height,Product_Height)',[Floor,Height,Product_Height])
        top.z_dim('Shelf_Thickness',[Shelf_Thickness])
        top.y_dim("-Depth+Rear_Angle_Depth+Front_Angle_Depth",[Depth,Rear_Angle_Depth,Front_Angle_Depth])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.prompt('Hide','Remove_Top_Shelf',[Remove_Top_Shelf])
        
    def add_shelf(self,i,panel,is_top=False):
        Product_Height = self.get_var('dim_z','Product_Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Depth = self.get_var('Opening ' + str(i) + ' Depth','Depth')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
        Remove_Bottom_Hanging_Shelf = self.get_var('Remove Bottom Hanging Shelf ' + str(i),'Remove_Bottom_Hanging_Shelf')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Rear_Angle_Depth = self.get_var('Rear Angle Depth')
        Front_Angle_Depth = self.get_var('Front Angle Depth')
        RN_1_H = self.get_var('First Rear Notch Height','RN_1_H')
        RN_1_D = self.get_var('First Rear Notch Depth','RN_1_D')
        RN_2_H = self.get_var('Second Rear Notch Height','RN_2_H')
        RN_2_D = self.get_var('Second Rear Notch Depth','RN_2_D')
        Left_End_Condition = self.get_var('Left End Condition')
        Right_End_Condition = self.get_var('Right End Condition')        
        Shelf_Gap = self.get_var('Shelf Gap')  
        Remove_Top_Shelf = self.get_var('Remove Top Shelf ' + str(i),'Remove_Top_Shelf')  
        Vertical_Offset = self.get_var("Top KD " + str(i) + " Vertical Offset",'Vertical_Offset')
        
        shelf = common_parts.add_shelf(self)
        shelf.obj_bp.mv.opening_name = str(i)
        shelf.prompt("Is Locked Shelf",value=True)
        
        Is_Locked_Shelf = shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = shelf.get_var('Adj Shelf Clip Gap')        
        
        if panel: #NOT FIRST SHELF
            X_Loc = panel.get_var('loc_x','X_Loc')
            shelf.x_loc('X_Loc+IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[X_Loc,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        else: #FIRST SHELF
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            shelf.x_loc('Left_Side_Wall_Filler+X_Loc+IF(Left_End_Condition==3,Shelf_Gap,False)+IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',
                        [Left_Side_Wall_Filler,X_Loc,Is_Locked_Shelf,Adj_Shelf_Clip_Gap,Left_End_Condition,Shelf_Gap])

        if is_top:
            shelf.y_loc(value=0)
            shelf.z_loc('IF(Floor,Height+Toe_Kick_Height,Product_Height)-Vertical_Offset',[Floor,Height,Product_Height,Toe_Kick_Height,Vertical_Offset])
            shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
            shelf.y_dim("-Depth+Rear_Angle_Depth+Front_Angle_Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)",
                        [Depth,Rear_Angle_Depth,Front_Angle_Depth,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
            shelf.prompt('Hide','IF(Remove_Top_Shelf,False,True)',[Remove_Top_Shelf])
        else:
            rear_notch_1_inset = "IF(Floor,IF(Toe_Kick_Height<RN_1_H,RN_1_D,0),0)"
            rear_notch_2_inset = "IF(Floor,IF(Toe_Kick_Height<RN_2_H,RN_2_D,0),0)"
            shelf.y_loc(rear_notch_1_inset + "-" + rear_notch_2_inset,[Floor,Toe_Kick_Height,RN_1_H,RN_2_H,RN_1_D,RN_2_D])
            shelf.z_loc('IF(Floor,Toe_Kick_Height,Product_Height-Height)',[Floor,Toe_Kick_Height,Product_Height,Height])
            shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
            shelf.y_dim("-Depth+" + rear_notch_1_inset + "+" + rear_notch_2_inset + "+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)",
                        [Floor,Depth,Toe_Kick_Height,RN_1_H,RN_2_H,RN_1_D,RN_2_D,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
            shelf.prompt('Hide','IF(Floor,False,IF(Remove_Bottom_Hanging_Shelf,False,True))',[Floor,Remove_Bottom_Hanging_Shelf])
            
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 0)
        
        if i == 1:
            shelf.prompt("Remove Left Holes",'IF(Left_End_Condition==3,True,False)',[Left_End_Condition])
            shelf.x_dim('Width-IF(Left_End_Condition==3,Shelf_Gap,0)-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Left_End_Condition,Shelf_Gap,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        elif i == self.opening_qty:
            shelf.prompt("Remove Right Holes",'IF(Right_End_Condition==3,True,False)',[Right_End_Condition])
            shelf.x_dim('Width-IF(Right_End_Condition==3,Shelf_Gap,0)-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Right_End_Condition,Shelf_Gap,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        else:
            shelf.x_loc('X_Loc+IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[X_Loc,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            
        if is_top:
            shelf.prompt("Drill On Top",value=True)
        else:
            shelf.prompt("Drill On Top",value=False)
    
    def add_hanging_rail(self):
    
        scene_props = props_closet.get_scene_props().closet_defaults
        
        PW = self.get_var('dim_x','PW')
        Product_Height = self.get_var('dim_z','Product_Height')
        Height = self.get_var('Opening 1 Height','Height')
        Floor = self.get_var('Opening 1 Floor Mounted','Floor')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        LC = self.get_var('Left End Condition','LC')
        RC = self.get_var('Right End Condition','RC')
        LF = self.get_var('Left Side Wall Filler','LF')
        RF = self.get_var('Right Side Wall Filler','RF')
        Add_Hanging_Rail = self.get_var('Add Hanging Rail')
        Hanging_Rail_Distance_From_Top = self.get_var('Hanging Rail Distance From Top')
        
        First_Opening_Width = self.get_var('Opening 1 Width','First_Opening_Width')
        Last_Opening_Width = self.get_var('Opening ' + str(self.opening_qty) + ' Width','Last_Opening_Width')
        
        rail = common_parts.add_hanging_rail(self)
        rail.x_loc('LF+IF(LC==0,MILLIMETER(9),0)+MILLIMETER(1)+IF(LC==3,First_Opening_Width,0)',
                   [LF,LC,First_Opening_Width])
        rail.y_loc(value = unit.inch(.01))
        if scene_props.use_plant_on_top:
            rail.z_loc('IF(Floor,Height,Product_Height)-Hanging_Rail_Distance_From_Top',[Floor,Height,Product_Height,Hanging_Rail_Distance_From_Top])
        else: 
            rail.z_loc('IF(Floor,Height,Product_Height-Shelf_Thickness)-Hanging_Rail_Distance_From_Top',[Floor,Height,Product_Height,Shelf_Thickness,Hanging_Rail_Distance_From_Top])
        rail.z_dim(value = -unit.inch(.125))
        rail.y_dim(value = unit.millimeter(32))
        rail.x_rot(value = -90)
        rail.y_rot(value = 0)
        rail.z_rot(value = 0)
        rail.x_dim('PW-LF-RF-IF(LC==0,MILLIMETER(9),0)-IF(RC==0,MILLIMETER(9),0)-MILLIMETER(2)-IF(LC==3,First_Opening_Width,0)-IF(RC==3,Last_Opening_Width,0)',
                   [PW,LF,RF,LC,RC,First_Opening_Width,Last_Opening_Width])
        rail.prompt("Hide",'IF(Add_Hanging_Rail,IF(PW-LF-RF-IF(LC==0,MILLIMETER(9),0)-IF(RC==0,MILLIMETER(9),0)-MILLIMETER(2)-IF(LC==3,First_Opening_Width,0)-IF(RC==3,Last_Opening_Width,0)<MILLIMETER(20),True,False),True)',
                    [Add_Hanging_Rail,PW,LF,RF,LC,RC,First_Opening_Width,Last_Opening_Width])
        rail.cutpart("Hanging_Rail")
    
    def add_cover_cleat_opening_name(self,assembly,opening_name):
        for child in assembly.obj_bp.children:
            if child.lm_closets.is_cleat_bp:
                child.mv.opening_name = opening_name

    def add_top_cleat(self,i,panel):
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Hanging_Height = self.get_var('dim_z','Hanging_Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Add_Hanging_Rail = self.get_var('Add Hanging Rail')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted',"Floor")
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Remove_Top_Shelf = self.get_var('Remove Top Shelf ' + str(i),'Remove_Top_Shelf')
        CBT = self.get_var('Opening ' + str(i) + ' Center Backing Thickness', 'CBT')
        TBT = self.get_var('Opening ' + str(i) + ' Top Backing Thickness', 'TBT')
        Cleat_Height = self.get_var("Cleat Height")
        TKDVO = self.get_var("Top KD " + str(i) + " Vertical Offset", 'TKDVO')      

        Dog_Ear_Each = self.get_var('Dog Ear Each')
        Rear_Angle_Height_All = self.get_var('Rear Angle Height', 'Rear_Angle_Height_All')
        Rear_Angle_Height_Left = self.get_var('Rear Angle ' + str(i) + ' Height', 'Rear_Angle_Height_Left')
        Rear_Angle_Height_Right = self.get_var('Rear Angle ' + str(i+1) + ' Height', 'Rear_Angle_Height_Right')

        for child in self.obj_bp.children:
            if child.lm_closets.is_back_bp and not child.lm_closets.is_hutch_back_bp:
                back_assembly = fd_types.Assembly(child)
                TOP = back_assembly.get_var("Top Section Backing", 'TOP')
                CTR = back_assembly.get_var("Center Section Backing", 'CTR')
                BTM = back_assembly.get_var("Bottom Section Backing", 'BTM')
                IS_SB = back_assembly.get_var("Is Single Back", 'IS_SB')                 
                B_Sec = back_assembly.get_var('Backing Sections', 'B_Sec')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Top Cleat")
        cleat.obj_bp.mv.opening_name = str(i)
        self.add_cover_cleat_opening_name(cleat, str(i))

        cleat.y_loc(value = 0)
        cleat.z_loc('IF(Floor,Height+Toe_Kick_Height,Hanging_Height)-IF(Dog_Ear_Each,IF(Rear_Angle_Height_Left>Rear_Angle_Height_Right,Rear_Angle_Height_Left,Rear_Angle_Height_Right),Rear_Angle_Height_All)-IF(Remove_Top_Shelf,Shelf_Thickness,0)-TKDVO',
                    [Remove_Top_Shelf,Shelf_Thickness,Floor,Height,Toe_Kick_Height,Hanging_Height,Dog_Ear_Each,Rear_Angle_Height_All,Rear_Angle_Height_Left,Rear_Angle_Height_Right,TKDVO])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim('Cleat_Height', [Cleat_Height])
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])

        if i == 1:
            cleat.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        elif i == self.opening_qty: #LAST OPENING
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        else:
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width])

        cleat.prompt(
            'Hide',
            'IF(OR(Add_Hanging_Rail,AND(B_Sec==1,CBT==1,CTR),AND(B_Sec>1,OR(AND(IS_SB,CBT==1,TOP),AND(IS_SB,CBT==1,TOP,CTR,BTM==False),AND(IS_SB==False,TOP,TBT==1)))),True,False)',
            [Add_Hanging_Rail,TBT,CBT,B_Sec,TOP,CTR,BTM,IS_SB]
        )

    def add_bottom_cleat(self,i,panel):
        Hanging_Height = self.get_var('dim_z','Hanging_Height')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        B_Cleat = self.get_var('Add ' + str(i) + ' Bottom Cleat','B_Cleat')
        Cleat_Location = self.get_var('Cleat ' + str(i) + ' Location','Cleat_Location')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted',"Floor")
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Remove_Bottom_Hanging_Shelf = self.get_var('Remove Bottom Hanging Shelf ' + str(i),'Remove_Bottom_Hanging_Shelf')
        CBT = self.get_var('Opening ' + str(i) + ' Center Backing Thickness', 'CBT')
        BBT = self.get_var('Opening ' + str(i) + ' Bottom Backing Thickness', 'BBT')                

        for child in self.obj_bp.children:
            if child.lm_closets.is_back_bp and not child.lm_closets.is_hutch_back_bp:
                back_assembly = fd_types.Assembly(child)

                TOP = back_assembly.get_var("Top Section Backing", 'TOP')
                CTR = back_assembly.get_var("Center Section Backing", 'CTR')
                BTM = back_assembly.get_var("Bottom Section Backing", 'BTM')
                IS_SB = back_assembly.get_var("Is Single Back", 'IS_SB')
                BIB = back_assembly.get_var("Bottom Insert Backing", 'BIB')
                BIG = back_assembly.get_var("Bottom Insert Gap", 'BIG')
                B_Sec = back_assembly.get_var('Backing Sections', 'B_Sec')
                SB = back_assembly.get_var("Single Back", 'SB')                                               
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Bottom Cleat")
        cleat.obj_bp.mv.opening_name = str(i)
        self.add_cover_cleat_opening_name(cleat, str(i))

        cleat.y_loc(value = 0)
        cleat.z_loc('IF(Floor,Toe_Kick_Height+Shelf_Thickness+Cleat_Location,Hanging_Height-Height+Cleat_Location+IF(Remove_Bottom_Hanging_Shelf,Shelf_Thickness,0))',
                    [Floor,Toe_Kick_Height,Remove_Bottom_Hanging_Shelf,Shelf_Thickness,Hanging_Height,Height,Cleat_Location])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim(value=unit.inch(-3.64))
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])

        if i == 1:
            cleat.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        elif i == self.opening_qty: #LAST OPENING
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        else:
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width])
    
        cleat.prompt(
            'Hide',
            'IF(OR(B_Cleat==False,AND(B_Sec==1,CBT==1,CTR,BIG==0),AND(B_Sec>1,AND(BIG==0,OR(AND(IS_SB,CBT==1,BTM),AND(IS_SB,CBT==1,BTM,CTR,TOP==False),AND(IS_SB==False,BTM,BBT==1))))),True,False)',
            [B_Cleat,CBT,BBT,B_Sec,SB,TOP,CTR,BTM,IS_SB,BIG]
        )

        cleat.prompt('Use Cleat Cover','IF(OR(BIB>0,BIG>0),False,True)', [BIB, BIG])    

    def add_mid_cleat(self,i,panel):
        Hanging_Height = self.get_var('dim_z','Hanging_Height')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')    
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Height_To_Add_Mid_Cleat = self.get_var('Height To Add Mid Cleat')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.obj_bp.mv.opening_name = str(i)
        cleat.y_loc(value = 0)
        cleat.z_loc('Hanging_Height-(Height)/2',[Hanging_Height,Height])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim(value=unit.inch(-3.64))
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        cleat.prompt('Hide','IF(Height>Height_To_Add_Mid_Cleat,False,True)',[Height,Height_To_Add_Mid_Cleat])
        if i == 1:
            cleat.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        elif i == self.opening_qty: #LAST OPENING
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        else:
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width])
    
    def add_toe_kick(self,i,panel):
        """This function is not being used.
        """        
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Depth = self.get_var('Opening ' + str(i) + ' Depth','Depth')
        Add_Backing = self.get_var('Add Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Left_End_Condition = self.get_var('Left End Condition')
        Right_End_Condition = self.get_var('Right End Condition')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')
        Floor_Mounted = self.get_var('Opening ' + str(i) + ' Floor Mounted','Floor_Mounted')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        kick = common_parts.add_toe_kick(self)
        kick.obj_bp.mv.opening_name = str(i)
        kick.y_dim('-Toe_Kick_Height',[Toe_Kick_Height,Shelf_Thickness])
        kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        kick.y_loc('-Depth+Toe_Kick_Setback-IF(Add_Backing,Back_Thickness,0)',[Depth,Toe_Kick_Setback,Add_Backing,Back_Thickness])
        kick.z_loc(value = 0)
        kick.x_rot(value = -90)
        kick.y_rot(value = 0)
        kick.z_rot(value = 0)
        kick.prompt("Hide",'IF(Floor_Mounted,False,True)',[Floor_Mounted])
        
        if i == 1 and self.opening_qty == 1: #ONLY ONE OPENING
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            kick.x_dim("Width+IF(Left_End_Condition!=3,0,Toe_Kick_Setback)+IF(Right_End_Condition!=3,0,Toe_Kick_Setback)",[Width,Left_End_Condition,Right_End_Condition,Toe_Kick_Setback])
            kick.x_loc("X_Loc-IF(Left_End_Condition!=3,0,Toe_Kick_Setback)+Left_Side_Wall_Filler",[X_Loc,Left_End_Condition,Toe_Kick_Setback,Left_Side_Wall_Filler])
        elif i == 1: #FIRST OPENING
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            kick.x_dim("Width+IF(Left_End_Condition!=3,0,Toe_Kick_Setback)",[Width,Left_End_Condition,Toe_Kick_Setback])
            kick.x_loc("X_Loc-IF(Left_End_Condition!=3,0,Toe_Kick_Setback)+Left_Side_Wall_Filler",[X_Loc,Left_End_Condition,Toe_Kick_Setback,Left_Side_Wall_Filler])
        elif i == self.opening_qty: #LAST OPENING
            kick.x_dim("Width+IF(Right_End_Condition!=3,0,Toe_Kick_Setback)",[Width,Right_End_Condition,Toe_Kick_Setback])
            kick.x_loc('X_Loc',[X_Loc])
        else: #MIDDLE OPENING
            kick.x_dim("Width",[Width])
            kick.x_loc('X_Loc',[X_Loc])
    
    def add_cleat(self,i,panel):
        """
        This function is no longer used
        Calls from draw() function are commented out
        add_top_cleat(), add_bottom_cleat(), and add_mid_cleat() are used insted
        """
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Add_Cleat = self.get_var('Add ' + str(i) + ' Cleat','Add_Cleat')
        Cleat_Location = self.get_var('Cleat ' + str(i) + ' Location','Cleat_Location')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.obj_bp.mv.opening_name = str(i)
        cleat.y_loc(value = 0)
        cleat.z_loc('Cleat_Location',[Cleat_Location])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim(value=unit.inch(-3.64))
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        cleat.prompt('Hide','IF(Add_Cleat,False,True)',[Add_Cleat])
        if i == 1:
            cleat.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler])
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        elif i == self.opening_qty: #LAST OPENING
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc])
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        else:
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc])
            cleat.x_dim('Width',[Width])
    
    def add_closet_opening(self,i,panel):
        props = props_closet.get_scene_props().closet_defaults
        
        Product_Height = self.get_var('dim_z','Product_Height')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Depth = self.get_var('Opening ' + str(i) + ' Depth','Depth')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Opening_Height_Difference = self.get_var("Opening Height Difference")
        BCL = self.get_var("Blind Corner Left",'BCL')
        BCR = self.get_var("Blind Corner Right",'BCR')
        BCLD = self.get_var("Blind Corner Left Depth",'BCLD')
        BCRD = self.get_var("Blind Corner Right Depth",'BCRD')
        TKDVO = self.get_var("Top KD " + str(i) + " Vertical Offset", 'TKDVO') 
        
        opening = common_parts.add_section_opening(self)
        opening.obj_bp.mv.opening_name = str(i)
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            #if(self.opening_qty==1):
                #opening.x_loc('IF(BCL,X_Loc+BCLD-Shelf_Thickness,IF(BCR,X_Loc+BCRD,X_Loc))',[X_Loc,BCL,BCR,BCLD,BCRD,Shelf_Thickness])
            #elif(i==1):
                #opening.x_loc('IF(BCL,X_Loc+BCLD-Shelf_Thickness,X_Loc)',[X_Loc,BCL,BCLD,Shelf_Thickness])
            #else:
            opening.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            #if(self.opening_qty==1):
                #opening.x_loc('IF(BCL,Left_Side_Wall_Filler+X_Loc+BCLD-Shelf_Thickness,IF(BCR,Left_Side_Wall_Filler+X_Loc+BCRD-Shelf_Thickness,Left_Side_Wall_Filler+X_Loc))',[X_Loc,BCL,BCR,BCLD,BCRD,Left_Side_Wall_Filler,Shelf_Thickness])
            #elif(i==1):
                #opening.x_loc('IF(BCL,Left_Side_Wall_Filler+X_Loc+BCLD-Shelf_Thickness,Left_Side_Wall_Filler+X_Loc)',[X_Loc,BCL,BCLD,Left_Side_Wall_Filler,Shelf_Thickness])
            #else:
            opening.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])
        opening.y_loc('-Depth',[Depth])
        opening.z_loc('IF(Floor,Toe_Kick_Height+Shelf_Thickness,Product_Height-Height+Shelf_Thickness)',
                      [Floor,Toe_Kick_Height,Shelf_Thickness,Product_Height,Height])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)

        #if(self.opening_qty==1):
            #opening.x_dim('IF(BCL,Width-BCLD+Shelf_Thickness,IF(BCR,Width-BCRD,Width))',[Width,BCL,BCR,BCLD,BCRD,Shelf_Thickness])
        #elif(i==1):
            #opening.x_dim('IF(BCL,Width-BCLD+Shelf_Thickness,Width)',[Width,BCL,BCLD,Shelf_Thickness])
        #elif(i==self.opening_qty):
            #opening.x_dim('IF(BCR,Width-BCRD+Shelf_Thickness,Width)',[Width,BCR,BCRD,Shelf_Thickness])
        #else:
        opening.x_dim('Width',[Width])

        opening.y_dim("fabs(Depth)",[Depth])
        opening.z_dim('Height-Opening_Height_Difference-TKDVO',[Height,Opening_Height_Difference,TKDVO])              
        opening.y_dim("fabs(Depth)",[Depth])
        
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
    
    def add_backing_cleat(self,i,panel,top_cleat=True,cover_cleat=False):
        Hanging_Height = self.get_var('dim_z','Hanging_Height')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')    
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Cleat_Height = self.get_var('Cleat Height', 'Cleat_Height')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Top Cleat" if top_cleat else "Bottom Cleat")
        cleat.obj_bp.mv.opening_name = str(i)
        self.add_cover_cleat_opening_name(cleat, str(i))

        cleat.x_rot(value=-90)

        if top_cleat:
            cleat.y_dim('Cleat_Height', [Cleat_Height])
        else:
            cleat.y_dim('-Cleat_Height', [Cleat_Height])


        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])

        if i == 1:
            cleat.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        elif i == self.opening_qty: #LAST OPENING
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        else:
            cleat.x_loc('X_Loc+INCH(.01)',[X_Loc]) #USED TO FIX DRAWER SIDE TOKEN
            cleat.x_dim('Width',[Width])        

        return cleat

    def add_backing(self,i,panel):
        PH = self.get_var('dim_z','PH')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
        BT = self.get_var('Opening ' + str(i) + ' Backing Thickness', 'BT')
        TBT = self.get_var('Opening ' + str(i) + ' Top Backing Thickness', 'TBT')
        CBT = self.get_var('Opening ' + str(i) + ' Center Backing Thickness', 'CBT')
        BBT = self.get_var('Opening ' + str(i) + ' Bottom Backing Thickness', 'BBT')
        B_Cleat = self.get_var('Add ' + str(i) + ' Bottom Cleat', 'B_Cleat')
        B_Cleat_Loc = self.get_var('Cleat ' + str(i) + ' Location', 'B_Cleat_Loc')
        CH = self.get_var('Cleat Height', 'CH')
        TKH = self.get_var('Toe Kick Height', 'TKH')
        ST = self.get_var('Shelf Thickness', 'ST')
        T_Shelf = self.get_var('Remove Top Shelf ' + str(i), 'T_Shelf')
        B_Shelf = self.get_var('Remove Bottom Hanging Shelf ' + str(i), 'B_Shelf')
        TKDVO = self.get_var("Top KD " + str(i) + " Vertical Offset", 'TKDVO') 
      
        backing = common_parts.add_back(self)
        backing.obj_bp.mv.opening_name = str(i)
        backing.add_prompt(name="Backing Sections",prompt_type='QUANTITY',value=1,tab_index=0)
        backing.add_prompt(name="Top Insert Backing",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="Bottom Insert Backing",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="Backing Top Offset",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="Backing Bottom Offset",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="Opening Bottom",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="1 Section Backing Z Location",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="1 Section Backing X Dimension",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="2 Section Backing Z Location with Top Insert",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="2 Section Backing X Dimension with Top Insert",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="2 Section Backing Z Location with Bottom Insert",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="2 Section Backing X Dimension with Bottom Insert",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="3 Section Backing Z Location",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="3 Section Backing X Dimension",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="Top Section Backing",prompt_type='CHECKBOX',value=False,tab_index=0)
        backing.add_prompt(name="Center Section Backing",prompt_type='CHECKBOX',value=False,tab_index=0)
        backing.add_prompt(name="Bottom Section Backing",prompt_type='CHECKBOX',value=False,tab_index=0)
        backing.add_prompt(name="Single Back",prompt_type='CHECKBOX',value=True,tab_index=0)
        backing.add_prompt(name="Is Single Back",prompt_type='CHECKBOX',value=False,tab_index=0)
        backing.add_prompt(name="Top Insert Gap",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="Bottom Insert Gap",prompt_type='DISTANCE',value=0,tab_index=0)
        backing.add_prompt(name="Backing Inset Amount",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=0)

        backing.add_prompt(
            name="2 Section Backing Config",
            prompt_type='COMBOBOX',
            items=['Full', 'Top', 'Bottom'],
            value=0,
            tab_index=0
        )        
        backing.add_prompt(
            name="3 Section Backing Config",
            prompt_type='COMBOBOX',
            items=['Full', 'Top', 'Bottom', 'Center', 'Top & Center', 'Bottom & Center', 'Top & Bottom'],
            value=0,
            tab_index=0
        )

        TOP = backing.get_var("Top Section Backing", 'TOP')
        CTR = backing.get_var("Center Section Backing", 'CTR')
        BTM = backing.get_var("Bottom Section Backing", 'BTM')
        SB = backing.get_var("Single Back", 'SB')
        IS_SB = backing.get_var("Is Single Back", 'IS_SB')
        TIB = backing.get_var("Top Insert Backing", 'TIB')
        BIB = backing.get_var("Bottom Insert Backing", 'BIB')
        TIG = backing.get_var("Top Insert Gap", 'TIG')
        BIG = backing.get_var("Bottom Insert Gap", 'BIG')
        BTO = backing.get_var("Backing Top Offset", 'BTO')
        BBO = backing.get_var("Backing Bottom Offset", 'BBO')
        BIA = backing.get_var("Backing Inset Amount", 'BIA')
        B_Sections = backing.get_var("Backing Sections", 'B_Sections')
        BZ1 = backing.get_var("1 Section Backing Z Location", 'BZ1')
        BX1 = backing.get_var("1 Section Backing X Dimension", 'BX1')
        BZ2T = backing.get_var("2 Section Backing Z Location with Top Insert", 'BZ2T')
        BX2T = backing.get_var("2 Section Backing X Dimension with Top Insert", 'BX2T')
        BZ2B = backing.get_var("2 Section Backing Z Location with Bottom Insert", 'BZ2B')
        BX2B = backing.get_var("2 Section Backing X Dimension with Bottom Insert", 'BX2B')
        BZ3 = backing.get_var("3 Section Backing Z Location", 'BZ3')
        BX3 = backing.get_var("3 Section Backing X Dimension", 'BX3')
        BC2 = backing.get_var("2 Section Backing Config", 'BC2')
        BC3 = backing.get_var("3 Section Backing Config", 'BC3')
        OB = backing.get_var("Opening Bottom", 'OB')

        backing.prompt('Backing Sections', 'IF(AND(TIB>0,BIB>0),3,IF(OR(TIB>0,BIB>0),2,1))', [TIB, BIB])
        backing.prompt('Opening Bottom', 'IF(Floor,TKH,PH-Height)', [Floor,TKH,PH,Height])

        backing.prompt(
            'Is Single Back',
            'IF(B_Sections==2,IF(AND(SB,TOP,BTM),True,False),IF(B_Sections==3,IF(OR(AND(SB,TOP,CTR,BTM),AND(SB,TOP,CTR),AND(SB,CTR,BTM)),True,False),True))',
            [SB,TOP,CTR,BTM,B_Sections]
        )

        backing.prompt(
            "Backing Top Offset",
            'IF(T_Shelf,ST,0)+IF(OR(AND(B_Sections==1,CTR,CBT==0),AND(B_Sections>1,IS_SB,CBT==0),AND(B_Sections>1,SB==False,TOP,TBT==0)),CH-BIA,0)',
            [T_Shelf,ST,CH,TOP,CTR,BTM,TBT,CBT,SB,BIA,IS_SB,B_Sections]
        )

        backing.prompt(
            "Backing Bottom Offset",
            'IF(BIG>0,BIG,B_Cleat_Loc)+IF(OR(Floor,B_Shelf),ST,0)+IF(OR(AND(B_Sections==1,CBT==0,CTR),AND(B_Sections>1,OR(AND(IS_SB,CBT==0),AND(IS_SB,CBT==0,BTM,CTR,TOP==False),AND(IS_SB==False,BTM,BBT==0)))),CH-BIA,0)',
            [Floor,B_Cleat,B_Cleat_Loc,ST,B_Shelf,CH,BIG,TOP,CTR,BTM,SB,CBT,BBT,BIA,B_Sections,IS_SB]            
        )

        #1 section
        backing.prompt(
            '1 Section Backing Z Location',
            'OB+IF(BIG>0,BIG+IF(CBT==0,CH-BIA,0),BBO)',
            [OB,BBO,BIG,CBT,CH,BIA]
        )
        backing.prompt(
            '1 Section Backing X Dimension',
            'Height-IF(TIG>0,TIG,BTO)-IF(BIG>0,BIG+IF(CBT==0,CH-BIA,0),BBO)',
            [Height,BTO,TIG,BBO,BIG,CH,BIA,CBT]
        )

        #2 section
        backing.prompt(
            '2 Section Backing Config',
            'IF(AND(TOP,BTM),0,IF(TOP,1,IF(BTM,2,0)))',
            [TOP,BTM]
        )

        #Top insert
        backing.prompt(
            '2 Section Backing Z Location with Top Insert',
            'IF(BC2==0,BZ1,IF(BC2==1,OB+Height-TIB+ST+IF(BT==0,CH-BIA,0),IF(BC2==2,IF(BT==0,OB+BBO-BIA,BZ1),BZ1)))',
            [Height,OB,BC2,BZ1,TIB,BBO,BIA,CH,ST,BT]
        )
        backing.prompt(
            '2 Section Backing X Dimension with Top Insert',
            'IF(BC2==0,BX1,IF(BC2==1,TIB-IF(BT==0,CH*2+BIA,ST)-IF(T_Shelf,ST,0),IF(BC2==2,Height-TIB-IF(BT==0,CH*2-BIA*2,0)-B_Cleat_Loc-IF(B_Shelf,ST,0),BX1)))',
            [BC2,Height,TIB,BIB,BX1,BIA,CH,B_Cleat_Loc,T_Shelf,B_Shelf,ST,BT]
        )

        #Bottom insert
        backing.prompt(
            '2 Section Backing Z Location with Bottom Insert',
            'IF(BC2==0,BZ1,IF(BC2==1,BIB+OB+IF(BT==0,CH-BIA,0),IF(BC2==2,OB+IF(BT==0,BBO-BIA,IF(B_Shelf,ST,0)),BZ1)))',
            [OB,BC2,BZ1,BIB,TIB,BBO,BIA,CH,BT,B_Shelf,ST]
        )
        backing.prompt(
            '2 Section Backing X Dimension with Bottom Insert',
            'IF(BC2==0,BX1,IF(BC2==1,Height-BIB-IF(BT==0,CH*2-BIA*2,0)-IF(T_Shelf,ST,0),IF(BC2==2,BIB-IF(BT==0,CH*2+BIA-B_Cleat_Loc,ST)-IF(B_Shelf,ST,0),BX1)))',
            [BC2,Height,TIB,BIB,BX1,BIA,CH,B_Cleat_Loc,T_Shelf,B_Shelf,ST,BT]
        )

        #3 section
        #[0:'Full', 1:'Top', 2:'Bottom', 3:'Center', 4:'Top & Center', 5:'Bottom & Center', 6:'Top & Bottom']
        backing.prompt(
            '3 Section Backing Config',
            'IF(AND(TOP,CTR,BTM),0,IF(AND(TOP,CTR),4,IF(AND(BTM,CTR),5,IF(AND(TOP,BTM),6,IF(TOP,1,IF(CTR,3,IF(BTM,2,0)))))))',
            [TOP,CTR,BTM]
        )

        backing.prompt(
            '3 Section Backing Z Location',
            'IF(OR(AND(BC3==0,IS_SB==False),BC3==3,BC3==4,AND(BC3==5,IS_SB==False)), OB+BIB+IF(CBT==0,CH-BIA,0) ,BZ1)',
            [OB,BC3,BZ1,BIB,TIB,BIA,Height,ST,CH,CBT,IS_SB]
        )
        
        backing.prompt(
            '3 Section Backing X Dimension',
            'IF(IS_SB,IF(BC3==0,BX1,IF(BC3==4,Height-BIB-BTO-IF(CBT==0,CH-BIA,0),IF(BC3==5,Height-TIB-BBO-IF(CBT==0,CH-BIA,0),BX1))),Height-TIB-BIB-IF(CBT==0,CH*2-BIA*2,0))',
            [BC3,Height,TIB,BIB,BX1,BIA,CH,B_Cleat_Loc,T_Shelf,B_Shelf,ST,CBT,IS_SB,BBO,BTO]
        )

        #Get X loc from opening panel
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            backing.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            backing.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])

        backing.y_loc(value=0)
        backing.z_loc(
            'IF(B_Sections==1,BZ1,IF(B_Sections==2,IF(TIB>0,BZ2T,IF(BIB>0,BZ2B,0)),IF(B_Sections==3,BZ3,0)))',
            [B_Sections,BZ1,BZ2T,BZ2B,BZ3,TIB,BIB,OB,Height,ST,CBT,CH,BIA]
        )

        backing.x_rot(value=-90)
        backing.y_rot(value=-90)
        backing.z_rot(value=0)

        backing.x_dim(
            'IF(B_Sections==1,BX1-TKDVO,IF(B_Sections==2,IF(TIB>0,BX2T,IF(BIB>0,BX2B,0)),IF(B_Sections==3,BX3,0)))',
            [B_Sections,BX1,BX2T,BX2B,BX3,TIB,BIB,Height,CBT,CH,BIA,TKDVO]
        )

        backing.y_dim("Width",[Width])
        backing.z_dim('IF(OR(AND(B_Sections==1,CBT==0),AND(B_Sections>1,CBT==0)),INCH(-0.25),INCH(-0.75))',[CBT, B_Sections])
        backing.prompt('Hide','IF(OR(AND(B_Sections==1,CTR),AND(B_Sections==2,SB,TOP,BTM),AND(B_Sections==3,CTR)),False,True)',[CTR,B_Sections,SB,TOP,BTM])

        #Top back
        top_backing = common_parts.add_back(self)
        top_backing.obj_bp.mv.opening_name = str(i)
        top_backing.obj_bp.lm_closets.is_back_bp = False
        top_backing.obj_bp.lm_closets.is_top_back_bp = True

        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            top_backing.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            top_backing.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])

        top_backing.y_loc(value=0)
        top_backing.z_loc(
            'IF(B_Sections>1,IF(TIB>0,OB+Height-TIB+ST+IF(TBT==0,CH-BIA,0),IF(BIB>0,BIB+OB+IF(TBT==0,CH-BIA,0),0)),0)',
            [B_Sections,OB,Height,TIB,CH,BIA,ST,TBT,BZ2T,BZ2B,BIB]
        )

        top_backing.x_rot(value=-90)
        top_backing.y_rot(value=-90)
        top_backing.z_rot(value=0)

        top_backing.x_dim(
            'IF(B_Sections==2,IF(TIB>0,TIB-IF(TBT==0,CH*2+BIA,ST)-IF(T_Shelf,ST,0),IF(BIB>0,Height-BIB-IF(TBT==0,CH*2-BIA*2,0)-IF(T_Shelf,ST,0),0)),IF(B_Sections==3,TIB-IF(TBT==0,CH*2-BIA*2,0)-ST-IF(T_Shelf,ST,0),0))-TKDVO',
            [B_Sections,BC3,Height,CH,ST,TIB,BIB,BIA,T_Shelf,TBT,BX2T,BX2B,TKDVO]
        )
        top_backing.y_dim("Width",[Width])
        top_backing.z_dim('IF(TBT==0,INCH(-0.25),INCH(-0.75))',[TBT])
        top_backing.prompt('Hide','IF(OR(B_Sections==1,TOP==False,AND(B_Sections>1,IS_SB)),True,False)',[B_Sections,TOP,CTR,BTM,IS_SB])

        #Bottom back
        bottom_backing = common_parts.add_back(self)
        bottom_backing.obj_bp.mv.opening_name = str(i)
        bottom_backing.obj_bp.lm_closets.is_back_bp = False
        bottom_backing.obj_bp.lm_closets.is_bottom_back_bp = True        

        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            bottom_backing.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            bottom_backing.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])

        bottom_backing.y_loc(value=0)
        bottom_backing.z_loc(
            'OB+BBO-IF(AND(B_Shelf,BIG>0),ST,0)',
            [B_Sections,OB,Height,TIB,CH,ST,BZ2T,BZ2B,BIB,BBT,BBO,B_Shelf,BIG,BIA]
        )

        bottom_backing.x_rot(value=-90)
        bottom_backing.y_rot(value=-90)
        bottom_backing.z_rot(value=0)
        bottom_backing.x_dim(
            'IF(B_Sections==3,IF(BBT==0,BIB-CH*2-BIA,BIB-ST)-IF(B_Shelf,ST,0), IF(TIB>0,Height-TIB-IF(BIG>0,BIG,0)+ST,BIB-IF(BIG>0,BIG,0))-IF(BBT==0,CH*2-BIA*2,0)-ST-IF(AND(B_Shelf,BIG==0),ST,0))',
            [B_Sections,Height,CH,ST,TIB,BIB,BIA,T_Shelf,TBT,BX2T,BX2B,BBT,B_Cleat_Loc,B_Shelf,BIG]
        )
        bottom_backing.y_dim("Width",[Width])
        bottom_backing.z_dim('IF(BBT==0,INCH(-0.25),INCH(-0.75))',[BBT])
        bottom_backing.prompt('Hide', 'IF(OR(B_Sections==1,BTM==False,AND(B_Sections>1,IS_SB)),True,False)', [B_Sections,TOP,BTM,IS_SB])                

        #Additional cleats for multi-section backing
        #BC3 - [0:'Full', 1:'Top', 2:'Bottom', 3:'Center', 4:'Top & Center', 5:'Bottom & Center', 6:'Top & Bottom']
        top_sec_bottom_cleat = self.add_backing_cleat(i, panel, top_cleat=False)
        top_sec_bottom_cleat.prompt(
            'Hide','IF(OR(TBT==1,TOP==False,B_Sections==1,AND(B_Sections>1,IS_SB)),True,False)',
            [B_Sections,TBT,TOP,BTM,IS_SB]
        )
        top_sec_bottom_cleat.z_loc('IF(B_Sections==2,IF(TIB>0,OB+Height-TIB+ST,IF(BIB>0,OB+BIB,0)),IF(B_Sections==3,OB+Height-TIB+ST,0))',[Height,OB,TIB,BIB,ST,B_Sections])

        mid_sec_top_cleat = self.add_backing_cleat(i, panel, top_cleat=True)
        mid_sec_top_cleat.prompt('Hide','IF(OR(AND(B_Sections==3,BC3==5,CTR,BTM,CBT==0,IS_SB),AND(B_Sections==3,CTR,CBT==0,IS_SB==False)),False,True)',[B_Sections,CTR,BTM,CBT,IS_SB,BC3])
        mid_sec_top_cleat.z_loc('OB+Height-TIB', [Height, OB, TIB])

        mid_sec_bottom_cleat = self.add_backing_cleat(i, panel, top_cleat=False)
        mid_sec_bottom_cleat.prompt('Hide','IF(AND(B_Sections==3,CTR,CBT==0,IS_SB==False),False,True)', [B_Sections, CTR, CBT, IS_SB])
        mid_sec_bottom_cleat.z_loc('OB+BIB', [OB, BIB])

        bottom_sec_top_cleat = self.add_backing_cleat(i, panel, top_cleat=True)
        bottom_sec_top_cleat.prompt(
            'Hide','IF(OR(BBT==1,BTM==False,B_Sections==1,AND(B_Sections>1,IS_SB)),True,False)',
            [B_Sections,BBT,TOP,BTM,IS_SB]
        )
        bottom_sec_top_cleat.z_loc('IF(B_Sections==2,IF(TIB>0,OB+Height-TIB,IF(BIB>0,OB+BIB-ST,0)),IF(B_Sections==3,OB+BIB-ST,0))', [Height, OB, TIB, BIB, ST, B_Sections])
        bottom_sec_top_cleat.prompt('Use Cleat Cover', 'IF(BIB>0,False,True)', [BIB])    

    def add_hutch_backing(self):
            Add_Hutch_Backing = self.get_var("Add Hutch Backing")
            Has_Capping_Bottom = self.get_var("Has Capping Bottom")
            Extend_Left_Side = self.get_var("Extend Left Side")
            Extend_Right_Side = self.get_var("Extend Right Side")
            Height_Left_Side = self.get_var("Height Left Side")
            Height_Right_Side = self.get_var("Height Right Side")
            Width = self.get_var('dim_x','Width')
            Product_Height = self.get_var('dim_z','Product_Height')
            Height_1 = self.get_var('Opening 1 Height','Height_1')
            Last_Height = self.get_var('Opening ' + str(self.opening_qty) + ' Height',"Last_Height")
            Panel_Thickness = self.get_var("Panel Thickness")

            hutch_backing = common_parts.add_back(self)
            hutch_backing.obj_bp.lm_closets.is_hutch_back_bp = True
            hutch_backing.obj_bp.mv.name_object = "Hutch Backing"
            hutch_backing.x_loc("Panel_Thickness",[Panel_Thickness])
            hutch_backing.y_loc(value = 0)
            hutch_backing.z_loc("Product_Height-IF(Height_1>=Last_Height,Height_1,Last_Height)-IF(Has_Capping_Bottom,Panel_Thickness,0)",[Product_Height,Height_1,Last_Height,Has_Capping_Bottom,Panel_Thickness])
            hutch_backing.x_rot(value=-90)
            hutch_backing.y_rot(value=0)
            hutch_backing.z_rot(value=0)
            hutch_backing.x_dim("Width-(Panel_Thickness*2)",[Width,Panel_Thickness])
            hutch_backing.y_dim("IF(Height_Left_Side>=Height_Right_Side,Height_Left_Side,Height_Right_Side)-IF(Has_Capping_Bottom,Panel_Thickness,0)",[Height_Left_Side,Height_Right_Side,Has_Capping_Bottom,Panel_Thickness])
            hutch_backing.z_dim("-Panel_Thickness",[Panel_Thickness])
            hutch_backing.prompt('Hide',"IF(OR(Extend_Left_Side,Extend_Right_Side),IF(Add_Hutch_Backing,False,True),True)",[Extend_Left_Side,Extend_Right_Side,Add_Hutch_Backing])

    def add_system_holes(self,i,panel):
        Product_Height = self.get_var('dim_z',"Product_Height")
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Depth = self.get_var('Opening ' + str(i) + ' Depth','Depth')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
        Add_Backing = self.get_var('Opening ' + str(i) + ' Add Backing', 'Add_Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Left_End_Condition = self.get_var('Left End Condition')
        Right_End_Condition = self.get_var('Right End Condition')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Front_Angle_Height = self.get_var('Front Angle Height')
        Front_Angle_Depth = self.get_var('Front Angle Depth')
        Rear_Angle_Height = self.get_var('Rear Angle Height')
        Rear_Angle_Depth = self.get_var('Rear Angle Depth')
        DDFF = self.get_var("Drilling Distance From Front",'DDFF')
        DDFR = self.get_var("Drilling Distance From Rear",'DDFR')
        Stop_LB = self.get_var("Opening " + str(i) + " Stop LB",'Stop_LB')
        Start_LB = self.get_var("Opening " + str(i) + " Start LB",'Start_LB')
        Drill_Thru_Left = self.get_var("Opening " + str(i) + " Drill Thru Left",'Drill_Thru_Left')
        Drill_Thru_Right = self.get_var("Opening " + str(i) + " Drill Thru Right",'Drill_Thru_Right')
        Add_Mid = self.get_var("Opening " + str(i) + " Add Mid Drilling",'Add_Mid')
        Remove_Left = self.get_var("Opening " + str(i) + " Remove Left Drill",'Remove_Left')
        Remove_Right = self.get_var("Opening " + str(i) + " Remove Right Drill",'Remove_Right')
        Panel_Thickness = self.get_var('Panel Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            
        ass_list = []
        
        lfb_holes = common_parts.add_line_bore_holes(self)
        lfb_holes.set_name("Left Front Bottom Holes " + str(i))
        ass_list.append(lfb_holes)
        lrb_holes = common_parts.add_line_bore_holes(self)
        lrb_holes.set_name("Left Rear Bottom Holes " + str(i))
        ass_list.append(lrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Right Front Bottom Holes " + str(i))
        ass_list.append(rfb_holes)
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Rear Bottom Holes " + str(i))
        ass_list.append(rrb_holes)
        lfb_holes = common_parts.add_line_bore_holes(self)
        lfb_holes.set_name("Left Front Top Holes " + str(i))
        ass_list.append(lfb_holes)
        lrb_holes = common_parts.add_line_bore_holes(self)
        lrb_holes.set_name("Left Rear Top Holes " + str(i))
        ass_list.append(lrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Right Front Top Holes " + str(i))
        ass_list.append(rfb_holes)
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Rear Top Holes " + str(i))
        ass_list.append(rrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Left Mid Top Holes " + str(i))
        ass_list.append(rfb_holes)
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Mid Top Holes " + str(i))
        ass_list.append(rrb_holes)
        rfb_holes = common_parts.add_line_bore_holes(self)
        rfb_holes.set_name("Left Mid Bottom Holes " + str(i))
        ass_list.append(rfb_holes)
        rrb_holes = common_parts.add_line_bore_holes(self)
        rrb_holes.set_name("Right Mid Bottom Holes " + str(i))
        ass_list.append(rrb_holes)
        
        ch_tfl_holes = common_parts.add_line_bore_holes(self)
        ch_tfl_holes.set_name("Chamfer Top Front Left Holes " + str(i))
        ch_tfl_holes.x_rot(value = 0)
        ch_tfl_holes.y_rot(value = 90)
        ch_tfl_holes.z_rot(value = 180)
        ch_tfl_holes.y_dim(value = 0)
        ch_tfl_holes.z_dim('IF(Drill_Thru_Left,Panel_Thickness+INCH(.02),INCH(.2))',[Drill_Thru_Left,Panel_Thickness])
        ch_tfl_holes.y_loc("-Depth-IF(Add_Backing,Back_Thickness,0)+Front_Angle_Depth+DDFF",[Depth,Add_Backing,Front_Angle_Depth,Back_Thickness,DDFF])
        ch_tfl_holes.x_dim('Front_Angle_Height',[Front_Angle_Height])
        ch_tfl_holes.z_loc('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])

        if panel:
            ch_tfl_holes.x_loc('X_Loc+INCH(.01)',[X_Loc])
        else:
            ch_tfl_holes.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler])
        
        if i == 1:                  #FIRST OPENING
            ch_tfl_holes.prompt('Hide','IF(Front_Angle_Height==0,True,IF(Left_End_Condition!=3,IF(Remove_Left,True,False),True))',[Front_Angle_Height,Left_End_Condition,Remove_Left])
        elif i == self.opening_qty: #LAST OPENING
            ch_tfl_holes.prompt('Hide','IF(Front_Angle_Height==0,True,IF(Right_End_Condition!=3,IF(Remove_Left,True,False),True))',[Front_Angle_Height,Right_End_Condition,Remove_Left])
        else:                       #MIDDLE OPENING
            ch_tfl_holes.prompt('Hide','IF(Front_Angle_Height==0,True,IF(Remove_Left,True,False))',[Front_Angle_Height,Remove_Left])    
            
        ch_tfr_holes = common_parts.add_line_bore_holes(self)
        ch_tfr_holes.set_name("Chamfer Top Front Right Holes " + str(i))
        ch_tfr_holes.x_rot(value = 0)
        ch_tfr_holes.y_rot(value = 90)
        ch_tfr_holes.z_rot(value = 180)
        ch_tfr_holes.y_dim(value = 0)
        ch_tfr_holes.z_dim('IF(Drill_Thru_Right,-Panel_Thickness-INCH(.02),-INCH(.2))',[Drill_Thru_Right,Panel_Thickness])
        ch_tfr_holes.y_loc("-Depth-IF(Add_Backing,Back_Thickness,0)+Front_Angle_Depth+DDFF",[Depth,Add_Backing,Front_Angle_Depth,Back_Thickness,DDFF])
        ch_tfr_holes.x_dim('Front_Angle_Height',[Front_Angle_Height])
        ch_tfr_holes.z_loc('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])
        
        if panel:
            ch_tfr_holes.x_loc('X_Loc+Width-INCH(.01)',[X_Loc,Width])
        else:
            ch_tfr_holes.x_loc('X_Loc+Left_Side_Wall_Filler+Width-INCH(.01)',[X_Loc,Width,Left_Side_Wall_Filler])        
        
        if i == 1:                  #FIRST OPENING
            ch_tfr_holes.prompt('Hide','IF(Front_Angle_Height==0,True,IF(Left_End_Condition!=3,IF(Remove_Right,True,False),True))',[Left_End_Condition,Remove_Right,Front_Angle_Height])
        elif i == self.opening_qty: #LAST OPENING
            ch_tfr_holes.prompt('Hide','IF(Front_Angle_Height==0,True,IF(Right_End_Condition!=3,IF(Remove_Right,True,False),True))',[Right_End_Condition,Remove_Right,Front_Angle_Height])
        else:                       #MIDDLE OPENING
            ch_tfr_holes.prompt('Hide','IF(Front_Angle_Height==0,True,IF(Remove_Right,True,False))',[Remove_Right,Front_Angle_Height])     
            
        ch_trl_holes = common_parts.add_line_bore_holes(self)
        ch_trl_holes.set_name("Chamfer Top Rear Left Holes " + str(i))
        ch_trl_holes.x_rot(value = 0)
        ch_trl_holes.y_rot(value = 90)
        ch_trl_holes.z_rot(value = 180)
        ch_trl_holes.y_dim(value = 0)
        ch_trl_holes.z_dim('IF(Drill_Thru_Left,Panel_Thickness+INCH(.02),INCH(.2))',[Drill_Thru_Left,Panel_Thickness])
        ch_trl_holes.y_loc("-IF(Add_Backing,Back_Thickness,0)-Rear_Angle_Depth-DDFR",[Depth,Add_Backing,Rear_Angle_Depth,Back_Thickness,DDFR])
        ch_trl_holes.x_dim('Rear_Angle_Height',[Rear_Angle_Height])
        ch_trl_holes.z_loc('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])

        if panel:
            ch_trl_holes.x_loc('X_Loc+INCH(.01)',[X_Loc])
        else:
            ch_trl_holes.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler])
        
        if i == 1:                  #FIRST OPENING
            ch_trl_holes.prompt('Hide','IF(Rear_Angle_Height==0,True,IF(Left_End_Condition!=3,IF(Remove_Left,True,False),True))',[Rear_Angle_Height,Left_End_Condition,Remove_Left])
        elif i == self.opening_qty: #LAST OPENING
            ch_trl_holes.prompt('Hide','IF(Rear_Angle_Height==0,True,IF(Right_End_Condition!=3,IF(Remove_Left,True,False),True))',[Rear_Angle_Height,Right_End_Condition,Remove_Left])
        else:                       #MIDDLE OPENING
            ch_trl_holes.prompt('Hide','IF(Rear_Angle_Height==0,True,IF(Remove_Left,True,False))',[Rear_Angle_Height,Remove_Left])    
            
        ch_trr_holes = common_parts.add_line_bore_holes(self)
        ch_trr_holes.set_name("Chamfer Top Rear Right Holes " + str(i))
        ch_trr_holes.x_rot(value = 0)
        ch_trr_holes.y_rot(value = 90)
        ch_trr_holes.z_rot(value = 180)
        ch_trr_holes.y_dim(value = 0)
        ch_trr_holes.z_dim('IF(Drill_Thru_Right,-Panel_Thickness-INCH(.02),-INCH(.2))',[Drill_Thru_Right,Panel_Thickness])
        ch_trr_holes.y_loc("-IF(Add_Backing,Back_Thickness,0)-Rear_Angle_Depth-DDFR",[Depth,Add_Backing,Rear_Angle_Depth,Back_Thickness,DDFR])
        ch_trr_holes.x_dim('Rear_Angle_Height',[Rear_Angle_Height])
        ch_trr_holes.z_loc('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Height,Product_Height])
        
        if panel:
            ch_trr_holes.x_loc('X_Loc+Width-INCH(.01)',[X_Loc,Width])
        else:
            ch_trr_holes.x_loc('X_Loc+Left_Side_Wall_Filler+Width-INCH(.01)',[X_Loc,Width,Left_Side_Wall_Filler])        
        
        if i == 1:                  #FIRST OPENING
            ch_trr_holes.prompt('Hide','IF(Rear_Angle_Height==0,True,IF(Left_End_Condition!=3,IF(Remove_Right,True,False),True))',[Left_End_Condition,Remove_Right,Rear_Angle_Height])
        elif i == self.opening_qty: #LAST OPENING
            ch_trr_holes.prompt('Hide','IF(Rear_Angle_Height==0,True,IF(Right_End_Condition!=3,IF(Remove_Right,True,False),True))',[Right_End_Condition,Remove_Right,Rear_Angle_Height])
        else:                       #MIDDLE OPENING
            ch_trr_holes.prompt('Hide','IF(Rear_Angle_Height==0,True,IF(Remove_Right,True,False))',[Remove_Right,Rear_Angle_Height])                  
        #Abbreviation for assembly ;)
        for ass in ass_list: 
            
            ass.x_rot(value = 0)
            ass.y_rot(value = -90)
            ass.z_rot(value = 0)
            ass.y_dim(value = 0)
            ass.prompt('Shelf Hole Spacing',value = unit.inch(1.2598))
            
            if "Left" in ass.obj_bp.mv.name_object:
                if panel:
                    ass.x_loc('X_Loc+INCH(.01)',[X_Loc])
                else:
                    ass.x_loc('X_Loc+Left_Side_Wall_Filler+INCH(.01)',[X_Loc,Left_Side_Wall_Filler])
                ass.z_dim('IF(Drill_Thru_Left,Panel_Thickness+INCH(.02),INCH(.2))',[Drill_Thru_Left,Panel_Thickness])

                if "Top" in ass.obj_bp.mv.name_object:
                    if i == 1:                  #FIRST OPENING
                        ass.prompt('Hide','IF(Left_End_Condition!=3,IF(OR(Remove_Left,Start_LB==0),True,False),True)',[Left_End_Condition,Remove_Left,Start_LB])
                    elif i == self.opening_qty: #LAST OPENING
                        ass.prompt('Hide','IF(Right_End_Condition!=3,IF(OR(Remove_Left,Start_LB==0),True,False),True)',[Right_End_Condition,Remove_Left,Start_LB])
                    else:                       #MIDDLE OPENING
                        ass.prompt('Hide','IF(OR(Remove_Left,Start_LB==0),True,False)',[Remove_Left,Start_LB])
                else:
                    if i == 1:                  #FIRST OPENING
                        ass.prompt('Hide','IF(Left_End_Condition!=3,IF(Remove_Left,True,False),True)',[Left_End_Condition,Remove_Left])
                    elif i == self.opening_qty: #LAST OPENING
                        ass.prompt('Hide','IF(Right_End_Condition!=3,IF(Remove_Left,True,False),True)',[Right_End_Condition,Remove_Left])
                    else:                       #MIDDLE OPENING
                        ass.prompt('Hide','IF(Remove_Left,True,False)',[Remove_Left])
            
            if "Right" in ass.obj_bp.mv.name_object:
                if panel:
                    ass.x_loc('X_Loc+Width-INCH(.01)',[X_Loc,Width])
                else:
                    ass.x_loc('X_Loc+Left_Side_Wall_Filler+Width-INCH(.01)',[X_Loc,Width,Left_Side_Wall_Filler])
                ass.z_dim('IF(Drill_Thru_Right,-Panel_Thickness-INCH(.02),-INCH(.2))',[Drill_Thru_Right,Panel_Thickness])

                if "Top" in ass.obj_bp.mv.name_object:
                    if i == 1:                  #FIRST OPENING
                        ass.prompt('Hide','IF(Left_End_Condition!=3,IF(OR(Remove_Right,Start_LB==0),True,False),True)',[Left_End_Condition,Remove_Right,Start_LB])
                    elif i == self.opening_qty: #LAST OPENING
                        ass.prompt('Hide','IF(Right_End_Condition!=3,IF(OR(Remove_Right,Start_LB==0),True,False),True)',[Right_End_Condition,Remove_Right,Start_LB])
                    else:                       #MIDDLE OPENING
                        ass.prompt('Hide','IF(OR(Remove_Right,Start_LB==0),True,False)',[Remove_Right,Start_LB])
                else:
                    if i == 1:                  #FIRST OPENING
                        ass.prompt('Hide','IF(Left_End_Condition!=3,IF(Remove_Right,True,False),True)',[Left_End_Condition,Remove_Right])
                    elif i == self.opening_qty: #LAST OPENING
                        ass.prompt('Hide','IF(Right_End_Condition!=3,IF(Remove_Right,True,False),True)',[Right_End_Condition,Remove_Right])
                    else:                       #MIDDLE OPENING
                        ass.prompt('Hide','IF(Remove_Right,True,False)',[Remove_Right])

            if "Top" in ass.obj_bp.mv.name_object:
                ass.y_rot(value = 90)
                ass.z_rot(value = 180)
                ass.z_loc('IF(Floor,Height,Product_Height)-MILLIMETER(9.525)',[Floor,Product_Height,Height])
                ass.x_dim('Start_LB',[Start_LB])

            if "Bottom" in ass.obj_bp.mv.name_object:
                ass.z_loc('IF(Floor,MILLIMETER(9.525)+Toe_Kick_Height,Product_Height-Height+MILLIMETER(9.525))',[Floor,Toe_Kick_Height,Product_Height,Height])
                if "Front" in ass.obj_bp.mv.name_object:
                    ass.x_dim('IF(Stop_LB>0,Stop_LB,Height-Front_Angle_Height)',[Height,Stop_LB,Front_Angle_Height])
                if "Rear" in ass.obj_bp.mv.name_object:
                    ass.x_dim('IF(Stop_LB>0,Stop_LB,Height-Rear_Angle_Height)',[Height,Stop_LB,Rear_Angle_Height])
                    
            if "Front" in ass.obj_bp.mv.name_object:
                ass.y_loc("-Depth-IF(Add_Backing,Back_Thickness,0)+DDFF",[Depth,Add_Backing,Back_Thickness,DDFF])
            
            if "Rear" in ass.obj_bp.mv.name_object:
                ass.y_loc("-IF(Add_Backing,Back_Thickness,0)-DDFR",[Add_Backing,Back_Thickness,DDFR])
            
            if "Mid" in ass.obj_bp.mv.name_object:
                ass.y_loc("-IF(Add_Backing,Back_Thickness,0)-INCH(12)+DDFF",[Add_Backing,Back_Thickness,DDFF])
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

    def add_blind_panel_holes(self,panel):
        Width = panel.get_var('dim_x','Width')
        Depth = panel.get_var("dim_y", 'Depth')
        Height = panel.get_var("dim_z", 'Height')
        DDFF = self.get_var("Drilling Distance From Front",'DDFF')
        left_bcp = panel.get_prompt("Is Left Blind Corner Panel")
        right_bcp = panel.get_prompt("Is Right Blind Corner Panel")
        Blind_Corner_Left = self.get_var("Blind Corner Left")
        Blind_Corner_Right = self.get_var("Blind Corner Right")        

        if left_bcp.value():
            rbf_holes = common_parts.add_line_bore_holes(panel)
            rbf_holes.set_name("Right Bottom Front Holes")

            rbf_holes.x_loc('-INCH(0.455)+MILLIMETER(9.5)+MILLIMETER(32)',[Depth, DDFF])
            rbf_holes.y_loc('Depth-DDFF',[Depth, DDFF])
            rbf_holes.z_loc('Height+INCH(0.01)',[Height])

            rbf_holes.x_rot(value=180)
            rbf_holes.y_rot(value=0)
            rbf_holes.z_rot(value=0)

            rbf_holes.x_dim('Width+INCH(0.455)-MILLIMETER(9.5)-MILLIMETER(32)',[Width])
            rbf_holes.y_dim(value=0)
            rbf_holes.z_dim(value=unit.inch(0.5))

            rbf_holes.prompt("Hide","IF(Blind_Corner_Left,False,True)",[Blind_Corner_Left])

        if right_bcp.value():
            lbf_holes = common_parts.add_line_bore_holes(panel)
            lbf_holes.set_name("Left Bottom Front Holes")

            lbf_holes.x_loc('-INCH(0.455)+MILLIMETER(9.5)+MILLIMETER(32)',[Depth, DDFF])
            lbf_holes.y_loc('Depth-DDFF',[Depth, DDFF])
            lbf_holes.z_loc(value=unit.inch(-0.01))

            lbf_holes.x_rot(value=0)
            lbf_holes.y_rot(value=0)
            lbf_holes.z_rot(value=0)

            lbf_holes.x_dim('Width+INCH(0.455)-MILLIMETER(9.5)-MILLIMETER(32)',[Width])
            lbf_holes.y_dim(value=0)
            lbf_holes.z_dim(value=unit.inch(0.5))

            lbf_holes.prompt("Hide", "IF(Blind_Corner_Right,False,True)",[Blind_Corner_Right])

    def add_blind_corners(self):
        Blind_Corner_Left = self.get_var("Blind Corner Left")
        Blind_Corner_Left_Depth = self.get_var("Blind Corner Left Depth")
        Blind_Corner_Right = self.get_var("Blind Corner Right")
        Blind_Corner_Right_Depth = self.get_var("Blind Corner Right Depth")
        First_Opening_Height = self.get_var("Opening 1 Height", "First_Opening_Height")
        Last_Opening_Height = self.get_var("Opening " + str(self.opening_qty) + " Height", "Last_Opening_Height")
        First_Opening_Depth = self.get_var("Opening 1 Depth", "First_Opening_Depth")
        Last_Opening_Depth = self.get_var("Opening " + str(self.opening_qty) + " Depth", "Last_Opening_Depth")
        First_Floor_Mounted = self.get_var('Opening 1 Floor Mounted','First_Floor_Mounted')
        Last_Floor_Mounted = self.get_var('Opening '+ str(self.opening_qty) +' Floor Mounted','Last_Floor_Mounted')
        Panel_Thickness = self.get_var("Panel Thickness")
        Width = self.get_var("dim_x", 'Width')
        Hanging_Height = self.get_var("dim_z",'Hanging_Height')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        BCHD = self.get_var("Blind Corner Height Difference","BCHD")

        #Left Blind Corner Panel
        left_blind_panel = common_parts.add_panel(self)
        left_blind_panel.x_loc(value=0)
        left_blind_panel.y_loc("-First_Opening_Depth-Panel_Thickness",[First_Opening_Depth,Panel_Thickness])
        left_blind_panel.z_loc('IF(First_Floor_Mounted,Toe_Kick_Height+(BCHD/2),Hanging_Height-First_Opening_Height+(BCHD/2))',
                                [First_Floor_Mounted,Toe_Kick_Height,BCHD,Hanging_Height,First_Opening_Height])

        left_blind_panel.x_rot(value=90)
        left_blind_panel.y_rot(value=-90)
        left_blind_panel.z_rot(value=180)

        left_blind_panel.x_dim("First_Opening_Height-BCHD",[First_Opening_Height,BCHD])
        left_blind_panel.y_dim("Blind_Corner_Left_Depth",[Blind_Corner_Left_Depth])
        left_blind_panel.z_dim("Panel_Thickness", [Panel_Thickness])

        left_blind_panel.prompt("Hide", "IF(Blind_Corner_Left, False, True)",[Blind_Corner_Left])
        left_blind_panel.prompt("Is Left Blind Corner Panel", value=True)
        left_blind_panel.prompt("CatNum",value=1004)
        left_blind_panel.obj_bp.mv.name_object = "Blind Corner Panel"
        left_blind_panel.obj_bp.lm_closets.is_panel_bp = False
        left_blind_panel.obj_bp.lm_closets.is_blind_corner_panel_bp = True
        self.add_blind_panel_holes(left_blind_panel)

        #Right Blind Corner Panel
        right_blind_panel = common_parts.add_panel(self)
        right_blind_panel.x_loc("Width",[Width])
        right_blind_panel.y_loc("-Last_Opening_Depth",[Last_Opening_Depth])
        right_blind_panel.z_loc('IF(Last_Floor_Mounted,Toe_Kick_Height+(BCHD/2),Hanging_Height-Last_Opening_Height+(BCHD/2))',
                                [Last_Floor_Mounted,Toe_Kick_Height,BCHD,Hanging_Height,Last_Opening_Height])

        right_blind_panel.x_rot(value=90)
        right_blind_panel.y_rot(value=-90)

        right_blind_panel.x_dim("Last_Opening_Height-BCHD",[Last_Opening_Height,BCHD])
        right_blind_panel.y_dim("Blind_Corner_Right_Depth",[Blind_Corner_Right_Depth])
        right_blind_panel.z_dim("Panel_Thickness", [Panel_Thickness])

        right_blind_panel.prompt("Hide", "IF(Blind_Corner_Right, False, True)",[Blind_Corner_Right])
        right_blind_panel.prompt("Is Right Blind Corner Panel", value=True)
        right_blind_panel.prompt("CatNum",value=1004)
        right_blind_panel.obj_bp.mv.name_object = "Blind Corner Panel"
        right_blind_panel.obj_bp.lm_closets.is_panel_bp = False
        right_blind_panel.obj_bp.lm_closets.is_blind_corner_panel_bp = True
        self.add_blind_panel_holes(right_blind_panel)

    def draw(self):
        defaults = props_closet.get_scene_props().closet_defaults
        
        self.create_assembly()
        self.obj_bp.mv.product_type = "Closet"
        self.obj_bp.mv.opening_name = str(self.opening_qty)
        
        if defaults.export_subassemblies:
            self.obj_bp.mv.export_product_subassemblies = True
        
        product_props = props_closet.get_object_props(self.obj_bp)
        product_props.is_closet = True
        
        self.add_opening_prompts()
        common_prompts.add_thickness_prompts(self)

        #when a carcass is added and drawn add_closet_carcass_prompts is called first
        common_prompts.add_closet_carcass_prompts(self)
        #self.add_machining_prompts()
        
        #This adds the the left and right side panels (first panel '1' and last panel 'self.opening_qty+2') 
        self.add_sides()
        self.add_hanging_rail()
        panel = None
        if defaults.use_plant_on_top:
            self.add_plant_on_top(1, panel)
        else:
            self.add_shelf(1,panel,is_top=True)
        self.add_shelf(1,panel,is_top=False)
        # self.add_toe_kick(1,panel)
        # self.add_cleat(1,panel)
        self.add_backing(1,panel)
        self.add_closet_opening(1,panel)
        self.add_hutch_backing()
        if defaults.show_panel_drilling:
            self.add_system_holes(1, panel)
        if defaults.add_top_cleat:
            self.add_top_cleat(1, panel)
        if defaults.add_bottom_cleat:
            self.add_bottom_cleat(1, panel)
        if defaults.add_mid_cleat:
            self.add_mid_cleat(1, panel)

        # self.add_inside_dimension( 1, panel)
        
        #This loop adds all the panels between first and last (left and right sides)
        for i in range(2,self.opening_qty+1):
            panel = self.add_panel(i,panel)
            if defaults.use_plant_on_top:
                self.add_plant_on_top( i, panel)
            else:
                self.add_shelf(i,panel,is_top=True)
            self.add_shelf(i,panel,is_top=False)
            # self.add_toe_kick(i,panel)
            # self.add_cleat(i,panel)
            self.add_backing(i,panel)
            self.add_closet_opening(i,panel)
            if defaults.show_panel_drilling:
                self.add_system_holes(i, panel)
            if defaults.add_top_cleat:
                self.add_top_cleat(i, panel)
            if defaults.add_bottom_cleat:
                self.add_bottom_cleat(i, panel)
            if defaults.add_mid_cleat:
                self.add_mid_cleat(i, panel)

        self.add_blind_corners()
                
            # self.add_inside_dimension(i, panel)


class PROMPTS_Opening_Starter(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".openings"
    bl_label = "Opening Starter Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    tabs = bpy.props.EnumProperty(name="Tabs",
                        items=[('OPENINGS','Opening Sizes','Show the Width x Height x Depth for each opening'),
                               ('CONSTRUCTION','Construction Options','Show Additional Construction Options')],
                               #('MACHINING','Machining Options','Machining Options')],
                        default = 'OPENINGS')
    
    placement_on_wall = bpy.props.EnumProperty(name="Placement on Wall",items=[('SELECTED_POINT',"Selected Point",""),
                                                                     ('FILL',"Fill",""),
                                                                     ('FILL_LEFT',"Fill Left",""),
                                                                     ('LEFT',"Left",""),
                                                                     ('CENTER',"Center",""),
                                                                     ('RIGHT',"Right",""),
                                                                     ('FILL_RIGHT',"Fill Right","")],default = 'SELECTED_POINT')
    
    quantity = bpy.props.IntProperty(name="Quantity",default=1)
    
    current_location = bpy.props.FloatProperty(name="Current Location", default=0,subtype='DISTANCE')
    left_offset = bpy.props.FloatProperty(name="Left Offset", default=0,subtype='DISTANCE')
    right_offset = bpy.props.FloatProperty(name="Right Offset", default=0,subtype='DISTANCE')
    product_width = bpy.props.FloatProperty(name="Product Width", default=0,subtype='DISTANCE')    
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)
    depth_1 = bpy.props.FloatProperty(name="Depth 1",unit='LENGTH',precision=4)
    depth_2 = bpy.props.FloatProperty(name="Depth 2",unit='LENGTH',precision=4)
    loc_left_side = bpy.props.FloatProperty(name="Loc Left Side",unit='LENGTH',precision=4)
    loc_right_side = bpy.props.FloatProperty(name="Loc Right Side",unit='LENGTH',precision=4)
                                             
    init_height_list = bpy.props.BoolProperty(name="Init Height List", default=True)
    default_height = bpy.props.StringProperty(name="Default Height", default='1203')

    height = bpy.props.EnumProperty(
        name="Height",
        items=get_panel_heights,
        update=update_closet_height
        )
    
    #Height_Left_Side = bpy.props.EnumProperty(
    #    name="Height Left Side",
    #    items=get_panel_heights
    #    )
    
    #Height_Right_Side = bpy.props.EnumProperty(
    #    name="Height Right Side",
    #    items=get_panel_heights
    #    )
    
    Opening_1_Height = bpy.props.EnumProperty(
        name="Opening 1 Height",
        items=get_panel_heights
        )
    
    Opening_2_Height = bpy.props.EnumProperty(
        name="Opening 2 Height",
        items=get_panel_heights
        )
    
    Opening_3_Height = bpy.props.EnumProperty(
        name="Opening 3 Height",
        items=get_panel_heights
        )
    
    Opening_4_Height = bpy.props.EnumProperty(
        name="Opening 4 Height",
        items=get_panel_heights
        )
    
    Opening_5_Height = bpy.props.EnumProperty(
        name="Opening 5 Height",
        items=get_panel_heights
        )
    
    Opening_6_Height = bpy.props.EnumProperty(
        name="Opening 6 Height",
        items=get_panel_heights
        )
    
    Opening_7_Height = bpy.props.EnumProperty(
        name="Opening 7 Height",
        items=get_panel_heights
        )
    
    Opening_8_Height = bpy.props.EnumProperty(
        name="Opening 8 Height",
        items=get_panel_heights,
        )

    Opening_9_Height = bpy.props.EnumProperty(
        name="Opening 9 Height",
        items=get_panel_heights,
        )
    
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
    
    default_width = 0
    selected_location = 0

    def check(self, context):
        self.product.obj_x.location.x = self.width
        props = props_closet.get_scene_props()

        #----------Called after a property is changed on the prompts page
        #Get props from product
        extend_left_side = self.product.get_prompt("Extend Left Side")
        extend_right_side = self.product.get_prompt("Extend Right Side")
        height_left_side = self.product.get_prompt("Height Left Side")
        height_right_side = self.product.get_prompt("Height Right Side")
        more_than_one_opening = self.product.get_prompt("Opening 2 Height")
        blind_corner_left = self.product.get_prompt("Blind Corner Left")
        blind_corner_right = self.product.get_prompt("Blind Corner Right")


        #Temp fix for older library data
        #TODO: Find a more efficient solution for handling older library data versions
        #if extend_left_side and height_left_side:
        #    height_left_side.set_value(unit.millimeter(float(self.Height_Left_Side)))

        #Temp fix for older library data
        #TODO: Find a more efficient solution for handling older library data versions
        #if extend_right_side and height_right_side:
        #    height_right_side.set_value(unit.millimeter(float(self.Height_Right_Side)))

        if props.closet_defaults.use_32mm_system:
            for i in range(1,10):
                opening_height = self.product.get_prompt("Opening " + str(i) + " Height")
                if opening_height:
                    height = eval("float(self.Opening_" + str(i) + "_Height)/1000")
                    opening_height.set_value(height)

        left_end_condition = self.product.get_prompt("Left End Condition")
        right_end_condition = self.product.get_prompt("Right End Condition")
        
        if left_end_condition:
            left_end_condition.set_value(self.Left_End_Condition)
        
        if right_end_condition:
            right_end_condition.set_value(self.Right_End_Condition)
        
        if blind_corner_left and blind_corner_right:
            if(more_than_one_opening):
                blind_corner_left.set_value(blind_corner_left.value())
                blind_corner_right.set_value(blind_corner_right.value())
            else:
                if(blind_corner_left.value()):
                    blind_corner_right.set_value(False)
                elif(blind_corner_right.value()):
                    blind_corner_left.set_value(False)
        
        self.update_opening_inserts()
        self.update_placement(context)
        
        utils.run_calculators(self.product.obj_bp)
        #Hack I Dont know why i need to run calculators twice just for left right side removal
        # utils.run_calculators(self.product.obj_bp)
        return True

    def update_opening_inserts(self):
        insert_bp = []
        capping_bottoms = 0
        for child in self.product.obj_bp.children:
            obj_props = child.lm_closets
            if obj_props.is_drawer_stack_bp or obj_props.is_hamper_insert_bp or obj_props.is_door_insert_bp or obj_props.is_closet_bottom_bp:
                insert_bp.append(child)
            for nchild in child.children:
                obj_props = nchild.lm_closets
                if obj_props.is_drawer_stack_bp or obj_props.is_hamper_insert_bp or obj_props.is_door_insert_bp or obj_props.is_closet_bottom_bp:
                    insert_bp.append(nchild)                    

        for obj_bp in insert_bp:
            insert = fd_types.Assembly(obj_bp)
            obj_props = obj_bp.lm_closets
            Cleat_Loc = insert.get_prompt("Cleat Location")
            Shelf_Backing_Setback = insert.get_prompt("Shelf Backing Setback")
            Remove_Bottom_Shelf = insert.get_prompt("Remove Bottom Shelf")
            Remove_Top_Shelf = insert.get_prompt("Remove Top Shelf")
            opening = insert.obj_bp.mv.opening_name

            if insert and opening:
                for child in self.product.obj_bp.children:
                    if child.lm_closets.is_back_bp and not child.lm_closets.is_hutch_back_bp:
                        if child.mv.opening_name == opening:
                            #Upadate for backing configurations
                            back_assembly = fd_types.Assembly(child)
                            B_Sec = back_assembly.get_prompt('Backing Sections')
                            TOP = back_assembly.get_prompt("Top Section Backing")
                            CTR = back_assembly.get_prompt("Center Section Backing")
                            BTM = back_assembly.get_prompt("Bottom Section Backing")
                            SB = back_assembly.get_prompt("Single Back")
                            TBT = self.product.get_prompt('Opening ' + str(opening) + ' Top Backing Thickness')
                            CBT = self.product.get_prompt('Opening ' + str(opening) + ' Center Backing Thickness')
                            BBT = self.product.get_prompt('Opening ' + str(opening) + ' Bottom Backing Thickness')
                            prompts = [B_Sec,TOP,CTR,BTM,SB,TBT,CBT,BBT,Cleat_Loc]

                            #For backwards compatability/older library data
                            if all(prompts):
                                #1 section backing drawer on bottom
                                if B_Sec.value() == 1:                                    
                                    if CTR.value() and CBT.value() == '3/4"':
                                        Cleat_Loc.set_value("None")
                                    elif(CTR.value() and CBT.value() == '1/4"'):
                                        Cleat_Loc.set_value("Above")
                                    
                                if B_Sec.value() == 2:
                                    single_back = SB.value() and TOP.value() and BTM.value()

                                    if obj_props.is_hamper_insert_bp:
                                        if single_back:
                                            Cleat_Loc.set_value("None")
                                            if CBT.value() == '1/4"':
                                                Shelf_Backing_Setback.set_value(unit.inch(0.25))
                                            else:
                                                Shelf_Backing_Setback.set_value(unit.inch(0.75))
                                        elif TOP.value() and TBT.value() == '3/4"':
                                            Cleat_Loc.set_value("None")
                                            Shelf_Backing_Setback.set_value(unit.inch(0))
                                        elif(TOP.value() and TBT.value() == '1/4"'):
                                            Shelf_Backing_Setback.set_value(unit.inch(0))
                                            Cleat_Loc.set_value("Above")
                                        else:
                                            Shelf_Backing_Setback.set_value(unit.inch(0))

                                        if obj_props.is_hamper_insert_bp:
                                            if single_back:
                                                Cleat_Loc.set_value("None")
                                                if CBT.value() == '1/4"':
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.25))
                                                else:
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.75))
                                            elif TOP.value() and TBT.value() == '3/4"':
                                                Cleat_Loc.set_value("None")
                                                Shelf_Backing_Setback.set_value(unit.inch(0))
                                            else:
                                                Shelf_Backing_Setback.set_value(unit.inch(0))
                                                Cleat_Loc.set_value("Above")

                                        if obj_props.is_drawer_stack_bp:
                                            if single_back:
                                                if CBT.value() == '1/4"':
                                                    Cleat_Loc.set_value("Above")
                                                else:
                                                    Cleat_Loc.set_value("None")

                                            elif BTM.value():
                                                if BBT.value() == '1/4"':
                                                    Cleat_Loc.set_value("Above")
                                                else:
                                                    Cleat_Loc.set_value("None")

                                        if obj_props.is_door_insert_bp:
                                            if single_back:
                                                if CBT.value() == '1/4"':
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.25))
                                                else:
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.75))
                                            else:
                                                Shelf_Backing_Setback.set_value(unit.inch(0))

                                    if B_Sec.value() == 3:
                                        full_back = SB.value() and TOP.value() and CTR.value() and BTM.value()
                                        top_ctr_back = SB.value() and TOP.value() and CTR.value()
                                        btm_ctr_back = SB.value() and BTM.value() and CTR.value()

                                        if obj_props.is_hamper_insert_bp:
                                            if full_back or btm_ctr_back:
                                                Cleat_Loc.set_value("None")
                                                if CBT.value() == '1/4"':
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.25))
                                                if CBT.value() == '3/4"':
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.75))
                                            elif top_ctr_back and CBT.value() == '3/4"':
                                                Cleat_Loc.set_value("None")
                                            elif CTR.value() and CBT.value() == '3/4"':
                                                Cleat_Loc.set_value("None")
                                            else:
                                                Cleat_Loc.set_value("Above")
                                                Shelf_Backing_Setback.set_value(unit.inch(0))

                                        # if obj_props.is_drawer_stack_bp:
                                        #     pass

                                        if obj_props.is_door_insert_bp:
                                            if full_back or top_ctr_back:
                                                if CBT.value() == '3/4"':
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.75))
                                                elif CBT.value() == '1/4"':
                                                    Shelf_Backing_Setback.set_value(unit.inch(0.25))
                                            else:
                                                Shelf_Backing_Setback.set_value(unit.inch(0))

                    if child.lm_closets.is_shelf_bp:
                        if child.mv.opening_name == opening:
                            RBS = self.product.get_prompt('Remove Bottom Hanging Shelf ' + str(opening))
                            RTS = self.product.get_prompt('Remove Top Shelf ' + str(opening))
                            floor = self.product.get_prompt("Opening " + str(opening) + " Floor Mounted")
                            prompts = [RBS,RTS,floor]

                            if all(prompts):
                                if obj_props.is_hamper_insert_bp:
                                   #For Hampers, Remove_Bottom_Shelf == True means that there is no bottom shelf
                                    if(RBS.value() or floor.value()):
                                        Remove_Bottom_Shelf.set_value(True)
                                    else:
                                        Remove_Bottom_Shelf.set_value(False)

                                if obj_props.is_drawer_stack_bp:
                                    #For Drawers, Remove_Bottom_Shelf == False means that there is no bottom shelf
                                    Lift_Drawers_From_Bottom = insert.get_prompt("Lift Drawers From Bottom")
                                    if((RBS.value() or floor.value()) and Lift_Drawers_From_Bottom.value() == False):
                                        Remove_Bottom_Shelf.set_value(False)
                                        insert.get_prompt("Pard Has Bottom KD").set_value(True)
                                    elif(Lift_Drawers_From_Bottom.value() == False):
                                        insert.get_prompt("Pard Has Bottom KD").set_value(False)        
                                    else:
                                        insert.get_prompt("Pard Has Bottom KD").set_value(False)                        

                                if obj_props.is_splitter_bp:
                                    #For Splitter, Remove_Bottom_Shelf == True means that there is no bottom shelf
                                    if(RBS.value() or floor.value()==False):
                                        Remove_Bottom_Shelf.set_value(True)


                                
                                    if obj_props.is_door_insert_bp:
                                        if full_back or top_ctr_back:
                                            if CBT.value() == '3/4"':
                                                Shelf_Backing_Setback.set_value(unit.inch(0.75))
                                            elif CBT.value() == '1/4"':
                                                Shelf_Backing_Setback.set_value(unit.inch(0.25))
                                        else:
                                            Shelf_Backing_Setback.set_value(unit.inch(0))

                    if child.lm_closets.is_closet_bottom_bp:
                        capping_bottom_assembly = fd_types.Assembly(child)
                        capping_bottoms += 1
                        extend_left_side = self.product.get_prompt("Extend Left Side")
                        extend_right_side = self.product.get_prompt("Extend Right Side")
                        height_left_side = self.product.get_prompt("Height Left Side")
                        height_right_side = self.product.get_prompt("Height Right Side")
                        left_partition_extended = capping_bottom_assembly.get_prompt("Left Partition Extended")
                        right_partition_extended = capping_bottom_assembly.get_prompt("Right Partition Extended")
                        left_partition_extension_height = capping_bottom_assembly.get_prompt("Left Partition Extension Height")
                        right_partition_extension_height = capping_bottom_assembly.get_prompt("Right Partition Extension Height")
                        against_left_wall = capping_bottom_assembly.get_prompt('Against Left Wall')
                        against_right_wall = capping_bottom_assembly.get_prompt('Against Right Wall')
                        prompts = [extend_left_side,extend_right_side,height_left_side,height_right_side,left_partition_extended,right_partition_extended,left_partition_extension_height,right_partition_extension_height,against_left_wall,against_right_wall]
                        if all(prompts):
                            left_partition_extended.set_value(extend_left_side.value())
                            right_partition_extended.set_value(extend_right_side.value())
                            left_partition_extension_height.set_value(height_left_side.value())
                            right_partition_extension_height.set_value(height_right_side.value())
                            if(extend_left_side.value() and height_left_side.value() > 0):
                                against_left_wall.set_value(False)
                            if(extend_right_side.value() and height_right_side.value() > 0):
                                against_right_wall.set_value(False)

        has_capping_bottom = self.product.get_prompt("Has Capping Bottom")
        if(has_capping_bottom):
            if(capping_bottoms > 0):
                has_capping_bottom.set_value(True)
            else:
                has_capping_bottom.set_value(False)

    def set_product_defaults(self):
        self.product.obj_bp.location.x = self.selected_location + self.left_offset
        self.product.obj_x.location.x = self.default_width - (self.left_offset + self.right_offset)

    def update_placement(self,context):
        left_x = self.product.get_collision_location('LEFT')
        right_x = self.product.get_collision_location('RIGHT')
        offsets = self.left_offset + self.right_offset
        if self.placement_on_wall == 'SELECTED_POINT':
            self.product.obj_bp.location.x = self.current_location
        if self.placement_on_wall == 'FILL':
            self.product.obj_bp.location.x = left_x + self.left_offset
            self.product.obj_x.location.x = (right_x - left_x - offsets) / self.quantity
        if self.placement_on_wall == 'LEFT':
            self.product.obj_bp.location.x = left_x + self.left_offset
            self.product.obj_x.location.x = self.width
        if self.placement_on_wall == 'RIGHT':
            if self.product.obj_bp.mv.placement_type == 'Corner':
                self.product.obj_bp.rotation_euler.z = math.radians(-90)
            self.product.obj_x.location.x = self.width
            self.product.obj_bp.location.x = (right_x - self.product.calc_width()) - self.right_offset
        # utils.run_calculators(self.product.obj_bp)        

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

    def set_default_heights(self, context):
        self.height = self.default_height
        self.init_height_list = False

        for i in range(1,10):
            opening_height_prompt = self.product.get_prompt("Opening " + str(i) + " Height")

            if opening_height_prompt:
                opening_height = round(unit.meter_to_millimeter(opening_height_prompt.value()),0)
                panel_heights = get_panel_heights(self, context)

                for index, height in enumerate(panel_heights):
                    if int(height[0]) == int(opening_height):
                        exec('self.Opening_' + str(i) + '_Height = str(height[0])')                     

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)

        if self.product.obj_bp:
            self.set_default_heights(context)
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
                self.height = self.convert_to_height(opening_1_height.value(),context)
            if self.is_single_island:
                opening_1_height = self.product.get_prompt("Opening 1 Height")
                opening_1_depth = self.product.get_prompt("Opening 1 Depth")
                self.depth = opening_1_depth.value()
                self.height = self.convert_to_height(opening_1_height.value(),context)


            #----------Initial setting of self.Height_Left_Side
            #Get Height Left Side value from selected product and convert to rounded int for setting Height_Left_Side
            #height_left_side = self.product.get_prompt("Height Left Side")

            #IF "Height Left Side" exists
            #Temp fix for older library data
            #TODO: Find a more efficient solution for handling older library data versions            
            #if height_left_side:
            #    prompt_val = height_left_side.value()
            #    height_left_side_mil = unit.meter_to_millimeter(prompt_val)
            #    int_height_left_side = int(round(height_left_side_mil))

                #Set Prompt Page initial value (self.Height_Left_Side)
            #    self.Height_Left_Side = str(int_height_left_side)

            #Get Height Right Side value from selected product and convert to rounded int for setting Height_Right_Side
            #height_right_side = self.product.get_prompt("Height Right Side")

            #IF "Height Right Side" exists
            #Temp fix for older library data
            #TODO: Find a more efficient solution for handling older library data versions   
            #if height_right_side:
            #    prompt_val = height_right_side.value()
            #    height_right_side_mil = unit.meter_to_millimeter(prompt_val)
            #    int_height_right_side = int(round(height_right_side_mil))

                #Set Prompt Page initial value (self.Height_Right_Side)
            #    self.Height_Right_Side = str(int_height_right_side)            

        self.current_location = self.product.obj_bp.location.x
        self.selected_location = self.product.obj_bp.location.x
        self.default_width = self.product.obj_x.location.x
        self.width = self.product.obj_x.location.x
        self.placement_on_wall = 'SELECTED_POINT'
        self.left_offset = 0
        self.right_offset = 0
                
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=600)

    def convert_to_height(self, number, context):
        panel_heights = get_panel_heights(self,context)
        for index, height in enumerate(panel_heights):
            if not number * 1000 >= float(height[0]):
                return panel_heights[index - 1][0]

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
        if self.Left_End_Condition == 'OFF' or self.Right_End_Condition == 'OFF':
            shelf_gap = self.product.get_prompt("Shelf Gap")
            shelf_gap.draw_prompt(col)
        
    def get_number_of_equal_widths(self):
        number_of_equal_widths = 0
        
        for i in range(1,10):
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
        if not self.is_island or not self.is_single_island:
            row.label("Height:")
            row.label("Depth:")
        
        box = col.box()
        
        for i in range(1,10):
            width = self.product.get_prompt("Opening " + str(i) + " Width")
            height = self.product.get_prompt("Opening " + str(i) + " Height")
            depth = self.product.get_prompt("Opening " + str(i) + " Depth")
            floor = self.product.get_prompt("Opening " + str(i) + " Floor Mounted")
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
                row.prop(floor,floor.prompt_type,text="",icon='TRIA_DOWN' if floor.value() else 'TRIA_UP')
                if props.closet_defaults.use_32mm_system:
                    row.prop(self,'Opening_' + str(i) + '_Height',text="")
                else:
                    row.prop(height,'DistanceValue',text="")
                row.prop(depth,'DistanceValue',text="")
                
    def draw_ctf_options(self,layout):
        prompts = []
        for i in range(1,10):
            prompt = self.product.get_prompt("CTF Opening " + str(i))
            if prompt:
                prompts.append(prompt)
                
        row = layout.row()
        row.label("Variable Section:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

    def draw_backing_options(self,layout):
        #Temp fix for older library data
        #TODO: Find a more efficient solution for handling older library data versions
        if self.product.get_prompt("Opening 1 Add Backing"):
            add_backing_prompts = []
            back_thickness_prompts = []
            for i in range(1,10):
                add_back = self.product.get_prompt("Opening " + str(i) + " Add Backing")
                back_thickness = self.product.get_prompt("Opening " + str(i) + " Backing Thickness")
                if add_back:
                    add_backing_prompts.append(add_back)
                if back_thickness:
                    back_thickness_prompts.append(back_thickness)
            row = layout.row()
            for i, prompt in enumerate(add_backing_prompts):
                col = row.column()
                col.prop(prompt, "CheckBoxValue", text=str(i + 1))
                if prompt.CheckBoxValue:
                    for child in self.product.obj_bp.children:
                        if child.lm_closets.is_back_bp:
                            if child.mv.opening_name == str(i + 1):
                                back_assembly = fd_types.Assembly(child)
                                backing_sections = back_assembly.get_prompt('Backing Sections')
                                if backing_sections and backing_sections.value() == 3:
                                    top_section = back_assembly.get_prompt("Top Section Backing")
                                    center_section = back_assembly.get_prompt("Center Section Backing")
                                    bottom_section = back_assembly.get_prompt("Bottom Section Backing")
                                    top_section.draw_prompt(col, text="Top", split_text=False)
                                    center_section.draw_prompt(col, text="Center", split_text=False)
                                    bottom_section.draw_prompt(col, text="Bottom", split_text=False)
                                elif backing_sections and backing_sections.value() == 2:
                                    top_section = back_assembly.get_prompt("Top Section Backing")
                                    bottom_section = back_assembly.get_prompt("Bottom Section Backing")
                                    top_section.draw_prompt(col, text="Top", split_text=False)
                                    bottom_section.draw_prompt(col, text="Bottom", split_text=False)
                    back_thickness_prompts[i].draw_prompt(col, text="Thickness")
            return

        top_back_thickness_prompts = []
        center_back_thickness_prompts = []
        bottom_back_thickness_prompts = []

        for i in range(1,10):
            top_back_thickness = self.product.get_prompt("Opening " + str(i) + " Top Backing Thickness")
            center_back_thickness = self.product.get_prompt("Opening " + str(i) + " Center Backing Thickness")
            bottom_back_thickness = self.product.get_prompt("Opening " + str(i) + " Bottom Backing Thickness")

            if top_back_thickness:
                top_back_thickness_prompts.append(top_back_thickness)
            if center_back_thickness:
                center_back_thickness_prompts.append(center_back_thickness)
            if bottom_back_thickness:
                bottom_back_thickness_prompts.append(bottom_back_thickness)

        row = layout.row()

        for i, prompt in enumerate(center_back_thickness_prompts):
            col = row.column(align=True)

            #Disable for now TODO: 3/4" capping full back
            # if back_thickness_prompts[i].value() == '3/4"':
            #     col.prop(inset_prompts[i], "CheckBoxValue", text="Inset")

            for child in self.product.obj_bp.children:
                if child.lm_closets.is_back_bp:
                    if child.mv.opening_name == str(i + 1):
                        back_assembly = fd_types.Assembly(child)
                        backing_sections = back_assembly.get_prompt('Backing Sections')
                        use_top = back_assembly.get_prompt("Top Section Backing")
                        use_center = back_assembly.get_prompt("Center Section Backing")
                        use_bottom = back_assembly.get_prompt("Bottom Section Backing")
                        single_back = back_assembly.get_prompt("Single Back")
                        is_single_back = back_assembly.get_prompt("Is Single Back")
                        
                        #1 Section
                        if backing_sections and backing_sections.value() == 1:                            
                            use_center.draw_prompt(col, text="Back " + str(i + 1), split_text=False)
                            if use_center.value() == True:
                                center_back_thickness_prompts[i].draw_prompt(col, text=" ")                              

                        #2 Section
                        if backing_sections and backing_sections.value() == 2:
                            show_single_back = use_top.value() and use_bottom.value()

                            #Single back
                            if show_single_back:
                                single_back.draw_prompt(col,text="Single Back", split_text=False)
                                if is_single_back.value():
                                    center_back_thickness_prompts[i].draw_prompt(col, text=" ")

                            #Top
                            use_top = back_assembly.get_prompt("Top Section Backing")
                            use_top.draw_prompt(col, text="Top " + str(i + 1), split_text=False)
                            if use_top.value() and not is_single_back.value():
                                top_back_thickness_prompts[i].draw_prompt(col, text=" ")

                            #Bottom
                            use_bottom = back_assembly.get_prompt("Bottom Section Backing")
                            use_bottom.draw_prompt(col, text="Bottom " + str(i + 1), split_text=False)
                            if use_bottom.value() and not is_single_back.value():
                                bottom_back_thickness_prompts[i].draw_prompt(col, text=" ")

                        #3 Section
                        if backing_sections and backing_sections.value() == 3:
                            single_back_config = [
                                use_top.value() and use_bottom.value() and use_center.value(),
                                use_top.value() and use_center.value(),
                                use_bottom.value() and use_center.value()
                            ]

                            if any(single_back_config):
                                single_back.draw_prompt(col,text="Single Back", split_text=False)
                                if single_back.value():
                                    center_back_thickness_prompts[i].draw_prompt(col, text=" ")                                

                            #Top
                            use_top = back_assembly.get_prompt("Top Section Backing")
                            use_top.draw_prompt(col, text="Top " + str(i + 1), split_text=False)
                            if use_top.value() and not is_single_back.value():
                                top_back_thickness_prompts[i].draw_prompt(col, text=" ")

                            #Center
                            use_center = back_assembly.get_prompt("Center Section Backing")
                            use_center.draw_prompt(col, text="Center " + str(i + 1), split_text=False)
                            if use_center.value() and not is_single_back.value():
                                center_back_thickness_prompts[i].draw_prompt(col, text=" ")

                            #Bottom
                            use_bottom = back_assembly.get_prompt("Bottom Section Backing")
                            use_bottom.draw_prompt(col, text="Bottom " + str(i + 1), split_text=False)
                            if use_bottom.value() and not is_single_back.value():
                                bottom_back_thickness_prompts[i].draw_prompt(col, text=" ")

    def draw_cleat_options(self,layout):
        prompts = []
        for i in range(1,10):
            prompt = self.product.get_prompt("Add " + str(i) + " Bottom Cleat")
            if prompt:
                prompts.append(prompt)

        row = layout.row()
        row.label("Bottom Cleat:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

        for i, prompt in enumerate(prompts):
            if prompt.CheckBoxValue:
                loc_prompt = self.product.get_prompt("Cleat " + str(i + 1) + " Location")
                row = layout.row()
                row.label("Cleat " + str(i + 1) + " Location")
                row.prop(loc_prompt,"DistanceValue",text=str(i + 1)) 

    def draw_dogear_options(self,layout):
        
        front_angle_height = self.product.get_prompt("Front Angle Height")
        front_angle_depth = self.product.get_prompt("Front Angle Depth")
        rear_angle_height = self.product.get_prompt("Rear Angle Height")
        rear_angle_depth = self.product.get_prompt("Rear Angle Depth")
                
        row = layout.row()
        row.label("Dog Ear Options:")        
        
        row = layout.row()     
        dog_ear_each = self.product.get_prompt("Dog Ear Each")  
        if dog_ear_each:
            row.prop(dog_ear_each,"CheckBoxValue",text="Dog Ear Each Partition") 
        
        if dog_ear_each.CheckBoxValue:        
            prompts = []
            for i in range(1,10):
                prompt = self.product.get_prompt("Dog Ear Partition " + str(i))
                if prompt:
                    prompts.append(prompt)
    
            # row = layout.row()
            # row.label("Dog Ear:")
            # for i, prompt in enumerate(prompts):
            #     row.prop(prompt,"CheckBoxValue",text=str(i + 1))
    
            for i, prompt in enumerate(prompts):
                # if prompt.CheckBoxValue:
                    
                    loc_prompt = self.product.get_prompt("Front Angle " + str(i + 1) + " Height")
                    row = layout.row()
                    row.label("Front Angle " + str(i + 1) + " Height")
                    row.prop(loc_prompt,"DistanceValue",text=str(i + 1))
                    
                    loc_prompt = self.product.get_prompt("Rear Angle " + str(i + 1) + " Height")
                    row.label("Rear Angle " + str(i + 1) + " Height")
                    row.prop(loc_prompt,"DistanceValue",text=str(i + 1)) 
                    
                    loc_prompt = self.product.get_prompt("Front Angle " + str(i + 1) + " Depth")
                    row = layout.row()
                    row.label("Front Angle " + str(i + 1) + " Depth")
                    row.prop(loc_prompt,"DistanceValue",text=str(i + 1)) 
                    
                    loc_prompt = self.product.get_prompt("Rear Angle " + str(i + 1) + " Depth")
                    row.label("Rear Angle " + str(i + 1) + " Depth")
                    row.prop(loc_prompt,"DistanceValue",text=str(i + 1))   
        else:
            if front_angle_depth and front_angle_height:
                row = layout.row()
                row.label("Dog Ear Front:")
                row.prop(front_angle_height,front_angle_height.prompt_type,text="Height")
                row.prop(front_angle_depth,front_angle_depth.prompt_type,text="Depth")
                 
            if rear_angle_depth and rear_angle_height:
                row = layout.row()
                row.label("Dog Ear Rear:")
                row.prop(rear_angle_height,rear_angle_height.prompt_type,text="Height")
                row.prop(rear_angle_depth,rear_angle_depth.prompt_type,text="Depth")      
                
    def draw_top_options(self,layout):
        prompts = []
        for i in range(1,10):
            prompt = self.product.get_prompt("Remove Top Shelf " + str(i))
            if prompt:
                prompts.append(prompt)            
            
        row = layout.row()
        row.label("Top KD:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))      

    def draw_bottom_options(self,layout):
        prompts = []
        for i in range(1,10):
            prompt = self.product.get_prompt("Remove Bottom Hanging Shelf " + str(i))
            if prompt:
                prompts.append(prompt)            
            
        row = layout.row()
        row.label("Bottom KD:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

    def draw_blind_corner_options(self,layout):
        blind_corner_left = self.product.get_prompt("Blind Corner Left")
        blind_corner_right = self.product.get_prompt("Blind Corner Right")
        blind_corner_left_depth = self.product.get_prompt("Blind Corner Left Depth")
        blind_corner_right_depth = self.product.get_prompt("Blind Corner Right Depth")
        opening_2_height = self.product.get_prompt("Opening 2 Height")

        if blind_corner_left and blind_corner_right:    
            row = layout.row()
            row.label("Blind Corner Options:")

            row = layout.row()
            row.prop(blind_corner_left, "CheckBoxValue", text="Left")
            if(blind_corner_left and blind_corner_left.value()):
                row.prop(blind_corner_left_depth, "DistanceValue", text="Depth: ")

            row = layout.row()
            row.prop(blind_corner_right, "CheckBoxValue", text="Right")
            if(blind_corner_right and blind_corner_right.value()):
                row.prop(blind_corner_right_depth, "DistanceValue", text="Depth: ")

    def draw_construction_options(self,layout):
        prompts = []
        box = layout.box()
        
        toe_kick_height = self.product.get_prompt("Toe Kick Height")
        toe_kick_setback = self.product.get_prompt("Toe Kick Setback")
        left_wall_filler = self.product.get_prompt("Left Side Wall Filler")
        right_wall_filler = self.product.get_prompt("Right Side Wall Filler")
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
        extend_left_side = self.product.get_prompt("Extend Left Side")
        extend_right_side = self.product.get_prompt("Extend Right Side")
        height_left_side = self.product.get_prompt("Height Left Side")
        height_right_side = self.product.get_prompt("Height Right Side")
        loc_left_side = self.product.get_prompt("Loc Left Side")
        loc_right_side = self.product.get_prompt("Loc Right Side")
        add_hanging_rail = self.product.get_prompt("Add Hanging Rail")
        left_end_deduction = self.product.get_prompt("Left End Deduction")
        right_end_deduction = self.product.get_prompt("Right End Deduction")
        add_hutch_backing = self.product.get_prompt("Add Hutch Backing")
        # remove_top_shelf = self.product.get_prompt("Remove Top Shelf")
        
        # SIDE OPTIONS:

        self.draw_ctf_options(box)
        
        # if remove_top_shelf:
        #     remove_top_shelf.draw_prompt(box,split_text=False)

        self.draw_top_options(box)  
        
        self.draw_cleat_options(box)          
        
        self.draw_bottom_options(box)        
                
        if left_wall_filler and right_wall_filler:
            split = box.split()
            col = split.column(align=True)
            col.label("Filler Options:")
            row = col.row()
            row.prop(left_wall_filler,'DistanceValue',text="Left Filler Amount")
            row.prop(left_end_deduction,'DistanceValue',text="Left End Deduction")
            row = col.row()
            row.prop(right_wall_filler,'DistanceValue',text="Right Filler Amount")
            row.prop(right_end_deduction,'DistanceValue',text="Right End Deduction")
            
            row = col.row()
            extend_left_side.draw_prompt(row,split_text=False)
            extend_right_side.draw_prompt(row,split_text=False)
            if extend_left_side.CheckBoxValue:
                row = col.row()
                row.prop(height_left_side,'DistanceValue',text="Left Partition Extension")
                #row.prop(loc_left_side,'DistanceValue',text="Left Partition Hang Height")
   
            if extend_right_side.CheckBoxValue:
                row = col.row()
                row.prop(height_right_side,'DistanceValue',text="Right Partition Extension")
                #row.prop(loc_right_side, 'DistanceValue',text="Right Partition Hang Height")
            if extend_left_side.CheckBoxValue or extend_right_side.CheckBoxValue:
                row = col.row()
                row.prop(add_hutch_backing,'CheckBoxValue',text="Add Hutch Backing")
        self.draw_dogear_options(box)
        
        # CARCASS OPTIONS:
        col = box.column(align=True)
        col.label("Full Back Options:")
        row = col.row()
        self.draw_backing_options(box)                             
            
        # col = box.column(align=True)
        # col.label("Dog Ear Options:")
        # if front_angle_depth and front_angle_height:
        #     row = col.row()
        #     row.label("Dog Ear Front:")
        #     row.prop(front_angle_height,front_angle_height.prompt_type,text="Height")
        #     row.prop(front_angle_depth,front_angle_depth.prompt_type,text="Depth")
            
        # if rear_angle_depth and rear_angle_height:
        #     row = col.row()
        #     row.label("Dog Ear Rear:")
        #     row.prop(rear_angle_height,rear_angle_height.prompt_type,text="Height")
        #     row.prop(rear_angle_depth,rear_angle_depth.prompt_type,text="Depth")

        self.draw_blind_corner_options(box)
            
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

    def draw_new_machining_options(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Opening Name:")
        row.label("Top:")
        row.label("Bottom:")
        row.label("Mid Row:")
        row.label("Drill Thru:")
        row.label("Remove:")
        
        for i in range(1,10):
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
        row.label("Bottom:")
        row.label("Top:")
        row.label("Mid Row:")
        row.label("Drill Thru:")
        row.label("Remove:")
        
        for i in range(1,10):
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
        
        row = box.row(align=True)
        row.label('Placement',icon='LATTICE_DATA')
        row.prop_enum(self, "placement_on_wall", 'SELECTED_POINT', icon='MAN_TRANS', text="Selected Point")
        row.prop_enum(self, "placement_on_wall", 'FILL', icon='ARROW_LEFTRIGHT', text="Fill")
        row.prop_enum(self, "placement_on_wall", 'LEFT', icon='TRIA_LEFT', text="Left") 
        row.prop_enum(self, "placement_on_wall", 'RIGHT', icon='TRIA_RIGHT', text="Right") 
        
        if self.placement_on_wall == 'FILL':
            row = box.row(align=True)
            row.label('Offset',icon='ARROW_LEFTRIGHT')
            row.prop(self, "left_offset", icon='TRIA_LEFT', text="Left") 
            row.prop(self, "right_offset", icon='TRIA_RIGHT', text="Right") 
        
        if self.placement_on_wall in 'LEFT':
            row = box.row(align=True)
            row.label('Offset',icon='BACK')
            row.prop(self, "left_offset", icon='TRIA_LEFT', text="Left")      
        
        if self.placement_on_wall in 'RIGHT':
            row = box.row(align=True)
            row.label('Offset',icon='FORWARD')
            row.prop(self, "right_offset", icon='TRIA_RIGHT', text="Right")          
        
        if self.placement_on_wall == 'SELECTED_POINT':
            row = box.row()
            row.label('Location:')
            row.prop(self,'current_location',text="")
        
        row.label('Move Off Wall:')
        row.prop(self.product.obj_bp,'location',index=1,text="")
            
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
                    self.draw_machining_options(box)
                self.draw_product_placment(box)        
                
class OPERATOR_Closet_Standard_Draw_Plan(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".draw_plan"
    bl_label = "Draw Closet Plan View"
    bl_description = "Creates the plan view for closets"
    
    object_name = bpy.props.StringProperty(name="Object Name",default="")
    
    product = None
    
    left_filler_amount = 0
    right_filler_amount = 0
    
    def add_opening(self,size,x_location):
        opening_mesh = utils.create_cube_mesh(self.product.obj_bp.mv.name_object,(size[0],size[1],size[2]))
        opening_mesh.parent = self.product.obj_bp.parent
        opening_mesh.location = self.product.obj_bp.location
        opening_mesh.location.x = x_location
        opening_mesh.rotation_euler = self.product.obj_bp.rotation_euler
        opening_mesh.mv.type = 'CAGE'
        
    def add_panel(self,size,x_location,text):
        panel_mesh = utils.create_cube_mesh(self.product.obj_bp.mv.name_object,(size[0],size[1],size[2]))
        panel_mesh.parent = self.product.obj_bp.parent
        panel_mesh.location = self.product.obj_bp.location
        panel_mesh.location.x = x_location
        panel_mesh.rotation_euler = self.product.obj_bp.rotation_euler
        panel_mesh.mv.type = 'CAGE'
        
        # dim = fd_types.Dimension()
        # dim.parent(panel_mesh)
        # dim.start_x(value = 0+unit.inch(2))
        # dim.start_y(value = size[1]-unit.inch(3))
        # dim.start_z(value = unit.inch(-100))
        # dim.set_label(text)

        
    def draw_closet_top(self,obj):
        props = props_closet.get_object_props(obj)
        if props.is_closet_top_bp:
            self.add_applied_top(obj)
        for child in obj.children:
            self.draw_closet_top(child)
        
    def add_applied_top(self,obj):
        top = fd_types.Assembly(obj)
        
        extend_left = top.get_prompt("Extend To Left Panel")
        extend_right = top.get_prompt("Extend To Right Panel")
        extend_left_amount = top.get_prompt("Extend Left Amount")
        extend_right_amount = top.get_prompt("Extend Right Amount")
        front_overhang = top.get_prompt("Front Overhang")
        panel_thickness = top.get_prompt("Panel Thickness")      
        
        overlay_left = 0 if extend_left.value() else -(panel_thickness.value()/2)
        overlay_right = 0 if extend_right.value() else -(panel_thickness.value()/2)
        
        length = top.obj_x.location.x + extend_left_amount.value() + extend_right_amount.value() + overlay_left + overlay_right
        width = -top.obj_y.location.y - front_overhang.value()
        
        closet_top = utils.create_cube_mesh(top.obj_bp.mv.name_object,(length,width,panel_thickness.value()))
        closet_top.parent = self.product.obj_bp.parent
        closet_top.location = self.product.obj_bp.location
        closet_top.location.x += top.obj_bp.location.x
        closet_top.location.x -= extend_left_amount.value() + overlay_left
        closet_top.rotation_euler = self.product.obj_bp.rotation_euler
        closet_top.mv.type = 'CAGE'
        
        for e in closet_top.data.edges:
            e.use_freestyle_mark = True
        closet_top.data.show_freestyle_edge_marks = True
                
    def execute(self, context):
        obj_bp = bpy.data.objects[self.object_name]

        self.product = fd_types.Assembly(obj_bp)
        thickness = self.product.get_prompt("Panel Thickness")
        l_thickness = self.product.get_prompt("Left Side Thickness")
        left_filler = self.product.get_prompt("Left Side Wall Filler")
        right_filler = self.product.get_prompt("Right Side Wall Filler")
        l_end = self.product.get_prompt("Left End Condition")
        r_end = self.product.get_prompt("Right End Condition")
        
        self.draw_closet_top(self.product.obj_bp)
        
        #LEFT FILLER
        if left_filler.value() > 0:
            section_depth = self.product.get_prompt("Opening 1 Depth")
            
            left_filler_obj = utils.create_cube_mesh(self.product.obj_bp.mv.name_object,(left_filler.value(),thickness.value(),self.product.obj_z.location.z))
            left_filler_obj.parent = self.product.obj_bp.parent
            left_filler_obj.location = self.product.obj_bp.location
            left_filler_obj.location.y = -section_depth.value()
            left_filler_obj.rotation_euler = self.product.obj_bp.rotation_euler
            left_filler_obj.mv.type = 'CAGE'
        
        x_placement = self.product.obj_bp.location.x + l_thickness.value() + left_filler.value()
        
        for i in range(1,10): # FOR EACH OPENING
            section_width = self.product.get_prompt("Opening " + str(i) + " Width")
            section_depth = self.product.get_prompt("Opening " + str(i) + " Depth")
            section_height = self.product.get_prompt("Opening " + str(i) + " Height")
            
            if section_width and section_depth:
                next_depth = self.product.get_prompt("Opening " + str(i + 1) + " Depth")
                prev_depth = self.product.get_prompt("Opening " + str(i - 1) + " Depth")
                
                depth = section_depth.value()
                if prev_depth:
                    if prev_depth.value() > section_depth.value():
                        depth = prev_depth.value()
                        
                if section_height:
                        
                    self.add_opening((section_width.value(),-section_depth.value(),section_height.value()), x_placement)
                    
                    if i == 1 and l_end.value() == 'OFF':
                        pass
                    else:
                        if i == 1:
                            text = str(int(unit.meter_to_active_unit(depth)))
                        else:
                            text = "" + str(int(unit.meter_to_active_unit(depth)))
                         
                        self.add_panel((thickness.value(),-depth,section_height.value()), x_placement - thickness.value(), text)
                         
                    x_placement += section_width.value() + thickness.value()
                    
                    if not next_depth:
                         
                        if r_end.value() != 'OFF':
                            #LAST PANEL
                            self.add_panel((thickness.value(),-section_depth.value(),section_height.value()),
                                            self.product.obj_bp.location.x + self.product.obj_x.location.x - thickness.value() - right_filler.value(), str(int(unit.meter_to_active_unit(section_depth.value()))))
    
                        #RIGHT FILLER
                        if right_filler.value() > 0:
                            right_filler_obj = utils.create_cube_mesh(self.product.obj_bp.mv.name_object,(-right_filler.value(),thickness.value(),self.product.obj_z.location.z))
                            right_filler_obj.parent = self.product.obj_bp.parent
                            right_filler_obj.location = self.product.obj_bp.location
                            right_filler_obj.location.x += self.product.obj_x.location.x
                            right_filler_obj.location.y -= section_depth.value()
                            right_filler_obj.rotation_euler = self.product.obj_bp.rotation_euler
                            right_filler_obj.mv.type = 'CAGE'

        return {'FINISHED'}
                
bpy.utils.register_class(PROMPTS_Opening_Starter)
bpy.utils.register_class(OPERATOR_Closet_Standard_Draw_Plan)
