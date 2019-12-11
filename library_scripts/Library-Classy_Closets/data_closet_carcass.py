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
    self.Opening_1_Height = self.height
    self.Opening_2_Height = self.height
    self.Opening_3_Height = self.height
    self.Opening_4_Height = self.height
    self.Opening_5_Height = self.height
    self.Opening_6_Height = self.height
    self.Opening_7_Height = self.height
    self.Opening_8_Height = self.height
    obj_product_bp = utils.get_bp(context.active_object,'PRODUCT')
    product = fd_types.Assembly(obj_product_bp)
#     product.obj_z.location.z = unit.millimeter(float(self.height))

    for i in range(1,10):
        opening_height = product.get_prompt("Opening " + str(i) + " Height")
        if opening_height:
            opening_height.set_value(unit.millimeter(float(self.height)))

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

            self.add_prompt(name="Opening " + str(i) + " Add Backing",
                               prompt_type='CHECKBOX',
                               value=False,
                               tab_index=1)

            self.add_prompt(
                name="Opening " + str(i) + " Inset Backing",
                prompt_type='CHECKBOX',
                value=True,
                tab_index=1
            )

            self.add_prompt(
                name="Opening " + str(i) + " Backing Thickness",
                prompt_type='COMBOBOX',
                items=['1/4"', '3/4"'],
                value=0,
                tab_index=1
            )

            self.add_prompt(name="Opening " + str(i) + " Backing Top Offset",
                               prompt_type='DISTANCE',
                               value=0,
                               tab_index=1)

            self.add_prompt(name="Opening " + str(i) + " Backing Bottom Offset",
                               prompt_type='DISTANCE',
                               value=0,
                               tab_index=1)

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
        left_filler.x_dim('IF(Extend_Left_Side,Height_Left_Side,Height_1)',[Height_1,Height_Left_Side,Extend_Left_Side])
        left_filler.y_dim('-Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_filler.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
        left_filler.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_filler.y_loc(value = 0)
        left_filler.z_loc('IF(Extend_Left_Side,(Loc_Left_Side-Height_Left_Side),IF(Floor_1,Toe_Kick_Height,Product_Height-Height_1))',[Loc_Left_Side,Floor_1,Height_Left_Side,Product_Height,Height_1,Toe_Kick_Height,Extend_Left_Side])
        left_filler.x_rot(value = 0)
        left_filler.y_rot(value = -90)
        left_filler.z_rot(value = -90)
        left_filler.prompt('Hide','IF(Left_Side_Wall_Filler==0,True,False)',[Left_Side_Wall_Filler])
        
        left_side = common_parts.add_panel(self)
        left_side.x_dim('IF(Extend_Left_Side,Height_Left_Side,Height_1)',[Height_1,Height_Left_Side,Extend_Left_Side])
        left_side.y_dim('-Depth_1+Left_End_Deduction',[Depth_1,Left_End_Deduction])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_side.y_loc(value = 0)
        left_side.z_loc('IF(Extend_Left_Side,(Loc_Left_Side-Height_Left_Side),IF(Floor_1,Toe_Kick_Height,Product_Height-Height_1))',[Loc_Left_Side,Floor_1,Height_Left_Side,Product_Height,Height_1,Toe_Kick_Height,Extend_Left_Side])
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
        right_filler.x_dim('IF(Extend_Right_Side,Height_Right_Side,Last_Height)',[Last_Height,Height_Right_Side,Extend_Right_Side])
        right_filler.y_dim('Right_Side_Wall_Filler',[Right_Side_Wall_Filler])
        right_filler.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
        right_filler.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
        right_filler.y_loc(value = 0)
        right_filler.z_loc('IF(Extend_Right_Side,(Loc_Right_Side-Height_Right_Side),IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height))',[Loc_Right_Side,Height_Right_Side,Last_Floor,Product_Height,Toe_Kick_Height,Last_Height,Extend_Right_Side])
        right_filler.x_rot(value = 0)
        right_filler.y_rot(value = -90)
        right_filler.z_rot(value = -90)
        right_filler.prompt('Hide','IF(Right_Side_Wall_Filler==0,True,False)',[Right_Side_Wall_Filler])
        
        right_side = common_parts.add_panel(self)
        right_side.x_dim('IF(Extend_Right_Side,Height_Right_Side,Last_Height)',[Last_Height,Height_Right_Side,Extend_Right_Side,Last_Floor])
        right_side.y_dim('-Last_Depth+Right_End_Deduction',[Last_Depth,Right_End_Deduction])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
        right_side.y_loc(value = 0)
        right_side.z_loc('IF(Extend_Right_Side,(Loc_Right_Side-Height_Right_Side),IF(Last_Floor,Toe_Kick_Height,Product_Height-Last_Height))',[Loc_Right_Side,Height_Right_Side,Last_Floor,Product_Height,Toe_Kick_Height,Last_Height,Extend_Right_Side])
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

        Add_Backing_L = self.get_var("Opening " + str(index-1) + " Add Backing", 'Add_Backing_L')
        Add_Backing_R = self.get_var("Opening " + str(index) + " Add Backing", 'Add_Backing_R')
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
            shelf.z_loc('IF(Floor,Height+Toe_Kick_Height,Product_Height)',[Floor,Height,Product_Height,Toe_Kick_Height])
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
        BT = self.get_var('Opening ' + str(i) + ' Backing Thickness', 'BT')        

        Dog_Ear_Each = self.get_var('Dog Ear Each')
        Rear_Angle_Height_All = self.get_var('Rear Angle Height', 'Rear_Angle_Height_All')
        Rear_Angle_Height_Left = self.get_var('Rear Angle ' + str(i) + ' Height', 'Rear_Angle_Height_Left')
        Rear_Angle_Height_Right = self.get_var('Rear Angle ' + str(i+1) + ' Height', 'Rear_Angle_Height_Right')  
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Top Cleat")
        cleat.obj_bp.mv.opening_name = str(i)
        cleat.y_loc(value = 0)
        cleat.z_loc('IF(Floor,Height+Toe_Kick_Height,Hanging_Height)-IF(Dog_Ear_Each,IF(Rear_Angle_Height_Left>Rear_Angle_Height_Right,Rear_Angle_Height_Left,Rear_Angle_Height_Right),Rear_Angle_Height_All)-IF(Remove_Top_Shelf,Shelf_Thickness,0)',
                    [Remove_Top_Shelf,Shelf_Thickness,Floor,Height,Toe_Kick_Height,Hanging_Height,Dog_Ear_Each,Rear_Angle_Height_All,Rear_Angle_Height_Left,Rear_Angle_Height_Right])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim(value=unit.inch(3.65))
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

        cleat.prompt('Hide','IF(OR(Add_Hanging_Rail,BT==1),True,False)', [Add_Hanging_Rail, BT])
    
    def add_bottom_cleat(self,i,panel):
        Hanging_Height = self.get_var('dim_z','Hanging_Height')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Add_Bottom_Cleat = self.get_var('Add ' + str(i) + ' Bottom Cleat','Add_Bottom_Cleat')
        Cleat_Location = self.get_var('Cleat ' + str(i) + ' Location','Cleat_Location')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted',"Floor")
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Remove_Bottom_Hanging_Shelf = self.get_var('Remove Bottom Hanging Shelf ' + str(i),'Remove_Bottom_Hanging_Shelf')
        BT = self.get_var('Opening ' + str(i) + ' Backing Thickness', 'BT')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Bottom Cleat")
        cleat.obj_bp.mv.opening_name = str(i)
        cleat.y_loc(value = 0)
        cleat.z_loc('IF(Floor,Toe_Kick_Height+Shelf_Thickness+Cleat_Location,Hanging_Height-Height+Cleat_Location+IF(Remove_Bottom_Hanging_Shelf,Shelf_Thickness,0))',
                    [Floor,Toe_Kick_Height,Remove_Bottom_Hanging_Shelf,Shelf_Thickness,Hanging_Height,Height,Cleat_Location])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim(value=unit.inch(-3.65))
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
    
        cleat.prompt('Hide','IF(OR(Add_Bottom_Cleat==False,BT==1),True,False)', [Add_Bottom_Cleat, BT])

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
        cleat.y_dim(value=unit.inch(-3.65))
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
        cleat.y_dim(value=unit.inch(-4))
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
        Add_Backing = self.get_var('Opening ' + str(i) + ' Add Backing', 'Add_Backing')
        Back_Thickness = self.get_var("Opening " + str(i) + " Backing Thickness", 'Back_Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        
        opening = common_parts.add_section_opening(self)
        opening.obj_bp.mv.opening_name = str(i)
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            opening.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            opening.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])
        opening.y_loc('-Depth',[Depth])
        opening.z_loc('IF(Floor,Toe_Kick_Height+Shelf_Thickness,Product_Height-Height+Shelf_Thickness)',
                      [Floor,Toe_Kick_Height,Shelf_Thickness,Product_Height,Height])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('Width',[Width])
        opening.y_dim("fabs(Depth)-IF(AND(Add_Backing,Back_Thickness==1),INCH(0.75),0)",[Depth, Back_Thickness, Add_Backing])

        if props.use_plant_on_top:
            opening.z_dim('Height-Shelf_Thickness',[Height,Shelf_Thickness,Floor,Toe_Kick_Height,Product_Height])
        else:
            opening.z_dim('Height-(Shelf_Thickness*2)',[Height,Shelf_Thickness,Floor,Toe_Kick_Height,Product_Height])        
        # if props.use_plant_on_top:
        #     opening.z_dim('Height-Shelf_Thickness-IF(Floor,Toe_Kick_Height,0)',[Height,Shelf_Thickness,Floor,Toe_Kick_Height,Product_Height])
        # else:
        #     opening.z_dim('Height-(Shelf_Thickness*2)-IF(Floor,Toe_Kick_Height,0)',[Height,Shelf_Thickness,Floor,Toe_Kick_Height,Product_Height])
        
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
    
    def add_backing(self,i,panel):
        scene_props = props_closet.get_scene_props().closet_defaults
        
        PH = self.get_var('dim_z','PH')
        Height = self.get_var('Opening ' + str(i) + ' Height','Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Floor = self.get_var('Opening ' + str(i) + ' Floor Mounted','Floor')
        Add_Backing = self.get_var('Opening ' + str(i) + ' Add Backing','Add_Backing')
        I_Back = self.get_var('Opening ' + str(i) + ' Inset Backing', 'I_Back')
        BT = self.get_var('Opening ' + str(i) + ' Backing Thickness', 'BT')
        B_Cleat = self.get_var('Add ' + str(i) + ' Bottom Cleat', 'B_Cleat')
        B_Cleat_Loc = self.get_var('Cleat ' + str(i) + ' Location', 'B_Cleat_Loc')
        TKH = self.get_var('Toe Kick Height', 'TKH')
        ST = self.get_var('Shelf Thickness', 'ST')
        T_Shelf = self.get_var('Remove Top Shelf ' + str(i), 'T_Shelf')
        B_Shelf = self.get_var('Remove Bottom Hanging Shelf ' + str(i), 'B_Shelf')

        self.prompt(
            "Opening " + str(i) + " Backing Top Offset",
            'IF(T_Shelf,ST+INCH(3.65),INCH(3.65))',
            [T_Shelf,ST]
        )

        self.prompt(
            "Opening " + str(i) + " Backing Bottom Offset",
            'IF(Floor,ST+IF(B_Cleat,B_Cleat_Loc+INCH(3.65),0),IF(B_Shelf,ST,0)+IF(B_Cleat,B_Cleat_Loc+INCH(3.65),0))',
            [Floor,B_Cleat,B_Cleat_Loc,ST,B_Shelf]            
        )
        
        backing = common_parts.add_back(self)
        backing.obj_bp.mv.opening_name = str(i)

        backing.add_prompt(
            name="Backing Insert Gap",
            prompt_type='DISTANCE',
            value=0,
            tab_index=0
        )

        backing.add_prompt(
            name="Backing Inset Amount",
            prompt_type='DISTANCE',
            value=unit.inch(0.25),
            tab_index=0
        )

        BIG = backing.get_var("Backing Insert Gap", 'BIG')
        IB = self.get_var("Opening " + str(i) + " Inset Backing", 'IB')
        BTO = self.get_var("Opening " + str(i) + " Backing Top Offset", 'BTO')
        BBO = self.get_var("Opening " + str(i) + " Backing Bottom Offset", 'BBO')
        BIA = backing.get_var("Backing Inset Amount", 'BIA')

        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            backing.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            backing.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])

        backing.y_loc(value = 0)
        backing.z_loc(
            'IF(Floor,TKH,PH-Height)+IF(BT==1,IF(IB,IF(B_Shelf,ST,0),0),IF(BIG>0,BIG,BBO)-IF(B_Cleat,BIA,0))',
            [Floor,TKH,PH,Height,IB,BBO,BIG,BIA,BT,ST,B_Shelf,B_Cleat]
        )

        backing.x_rot(value = -90)
        backing.y_rot(value = -90)
        backing.z_rot(value = 0)

        if scene_props.use_plant_on_top:
            backing.x_dim('Height-IF(Floor,TKH,0)',[Height,Floor,TKH,ST])
        else:
            backing.x_dim(
                'IF(BT==1,IF(I_Back,Height-IF(B_Shelf,ST,0)-IF(T_Shelf,ST,0),Height),Height-BTO-IF(BIG>0,BIG,BBO)+IF(B_Cleat,BIA*2,BIA))',
                [Height,BTO,BBO,BIG,BIA,BT,ST,B_Shelf,T_Shelf,I_Back,B_Cleat]
            )

        backing.y_dim("Width",[Width])
        backing.z_dim('IF(BT==0,INCH(-0.25),INCH(-0.75))',[BT])
        backing.prompt('Hide','IF(Add_Backing,False,True)',[Add_Backing])
        
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
        self.add_closet_opening(1,panel)
        self.add_backing(1,panel)
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
            self.add_closet_opening(i,panel)
            self.add_backing(i,panel)
            if defaults.show_panel_drilling:
                self.add_system_holes(i, panel)
            if defaults.add_top_cleat:
                self.add_top_cleat(i, panel)
            if defaults.add_bottom_cleat:
                self.add_bottom_cleat(i, panel)
            if defaults.add_mid_cleat:
                self.add_mid_cleat(i, panel)
                
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
                                             
    height = bpy.props.EnumProperty(name="Height",
                          items=common_lists.PANEL_HEIGHTS,
                          default = '1203',
                          update=update_closet_height)
    
    Height_Left_Side = bpy.props.EnumProperty(name="Height Left Side",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Height_Right_Side = bpy.props.EnumProperty(name="Height Right Side",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_1_Height = bpy.props.EnumProperty(name="Opening 1 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_2_Height = bpy.props.EnumProperty(name="Opening 2 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_3_Height = bpy.props.EnumProperty(name="Opening 3 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_4_Height = bpy.props.EnumProperty(name="Opening 4 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_5_Height = bpy.props.EnumProperty(name="Opening 5 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_6_Height = bpy.props.EnumProperty(name="Opening 6 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_7_Height = bpy.props.EnumProperty(name="Opening 7 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
    Opening_8_Height = bpy.props.EnumProperty(name="Opening 8 Height",
                                    items=common_lists.PANEL_HEIGHTS,
                                    default = '1203')
    
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

        #Temp fix for older library data
        #TODO: Find a more efficient solution for handling older library data versions
        if extend_left_side and height_left_side:
            height_left_side.set_value(unit.millimeter(float(self.Height_Left_Side)))

        #Temp fix for older library data
        #TODO: Find a more efficient solution for handling older library data versions
        if extend_right_side and height_right_side:
            height_right_side.set_value(unit.millimeter(float(self.Height_Right_Side)))

        if props.closet_defaults.use_32mm_system:
            for i in range(1,9):
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
        
        self.update_placement(context)
        
        utils.run_calculators(self.product.obj_bp)
        #Hack I Dont know why i need to run calculators twice just for left right side removal
        # utils.run_calculators(self.product.obj_bp)
        return True

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

    def set_default_heights(self):
        for i in range(1,9):
            opening_height_prompt = self.product.get_prompt("Opening " + str(i) + " Height")
            if opening_height_prompt:
                opening_height = round(unit.meter_to_millimeter(opening_height_prompt.value()),0)
                for index, height in enumerate(common_lists.PANEL_HEIGHTS):
                    if not opening_height >= int(height[0]):
                        exec('self.Opening_' + str(i) + '_Height = common_lists.PANEL_HEIGHTS[index - 1][0]')                                                                                                                                                                                                    
                        break
                    if index + 1 == len(common_lists.PANEL_HEIGHTS):
                        exec('self.Opening_' + str(i) + '_Height = common_lists.PANEL_HEIGHTS[index][0]')                        

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)

        if self.product.obj_bp:
            self.set_default_heights()
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
                self.height = self.convert_to_height(opening_1_height.value())
            if self.is_single_island:
                opening_1_height = self.product.get_prompt("Opening 1 Height")
                opening_1_depth = self.product.get_prompt("Opening 1 Depth")
                self.depth = opening_1_depth.value()
                self.height = self.convert_to_height(opening_1_height.value())



            #----------Initial setting of self.Height_Left_Side
            #Get Height Left Side value from selected product and convert to rounded int for setting Height_Left_Side
            height_left_side = self.product.get_prompt("Height Left Side")

            #IF "Height Left Side" exists
            #Temp fix for older library data
            #TODO: Find a more efficient solution for handling older library data versions            
            if height_left_side:
                prompt_val = height_left_side.value()
                height_left_side_mil = unit.meter_to_millimeter(prompt_val)
                int_height_left_side = int(round(height_left_side_mil))

                #Set Prompt Page initial value (self.Height_Left_Side)
                self.Height_Left_Side = str(int_height_left_side)

            #Get Height Right Side value from selected product and convert to rounded int for setting Height_Right_Side
            height_right_side = self.product.get_prompt("Height Right Side")

            #IF "Height Right Side" exists
            #Temp fix for older library data
            #TODO: Find a more efficient solution for handling older library data versions   
            if height_right_side:
                prompt_val = height_right_side.value()
                height_right_side_mil = unit.meter_to_millimeter(prompt_val)
                int_height_right_side = int(round(height_right_side_mil))

                #Set Prompt Page initial value (self.Height_Right_Side)
                self.Height_Right_Side = str(int_height_right_side)            

        self.current_location = self.product.obj_bp.location.x
        self.selected_location = self.product.obj_bp.location.x
        self.default_width = self.product.obj_x.location.x
        self.width = self.product.obj_x.location.x
        self.placement_on_wall = 'SELECTED_POINT'
        self.left_offset = 0
        self.right_offset = 0
                
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=600)

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
        if not self.is_island or not self.is_single_island:
            row.label("Height:")
            row.label("Depth:")
        
        box = col.box()
        
        for i in range(1,9):
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
        for i in range(1,9):
            prompt = self.product.get_prompt("CTF Opening " + str(i))
            if prompt:
                prompts.append(prompt)
                
        row = layout.row()
        row.label("Variable Section:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

    def draw_backing_options(self,layout):
        add_backing_prompts = []
        inset_prompts = []
        back_thickness_prompts = []

        for i in range(1,9):
            add_back = self.product.get_prompt("Opening " + str(i) + " Add Backing")
            back_thickness = self.product.get_prompt("Opening " + str(i) + " Backing Thickness")
            inset_back = self.product.get_prompt("Opening " + str(i) + " Inset Backing")            

            if add_back:
                add_backing_prompts.append(add_back)
            if back_thickness:
                back_thickness_prompts.append(back_thickness)
            if inset_back:
                inset_prompts.append(inset_back)

        row = layout.row()
        row.label("Full Back:")

        for i, prompt in enumerate(add_backing_prompts):
            col = row.column()
            col.prop(prompt, "CheckBoxValue", text=str(i + 1))

            if prompt.CheckBoxValue:
                #Disable for now TODO: 3/4" capping full back
                # if back_thickness_prompts[i].value() == '3/4"':
                #     col.prop(inset_prompts[i], "CheckBoxValue", text="Inset")

                back_thickness_prompts[i].draw_prompt(col, text="Thickness")

    def draw_cleat_options(self,layout):
        prompts = []
        for i in range(1,9):
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
            for i in range(1,9):
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
        for i in range(1,9):
            prompt = self.product.get_prompt("Remove Top Shelf " + str(i))
            if prompt:
                prompts.append(prompt)            
            
        row = layout.row()
        row.label("Top KD:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))      

    def draw_bottom_options(self,layout):
        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("Remove Bottom Hanging Shelf " + str(i))
            if prompt:
                prompts.append(prompt)            
            
        row = layout.row()
        row.label("Bottom KD:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))                    
            
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
        loc_left_side = self.product.get_prompt("Loc Left Side")
        loc_right_side = self.product.get_prompt("Loc Right Side")
        add_hanging_rail = self.product.get_prompt("Add Hanging Rail")
        left_end_deduction = self.product.get_prompt("Left End Deduction")
        right_end_deduction = self.product.get_prompt("Right End Deduction")
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
                row.prop(self,'Height_Left_Side',text="Left Panel Height")
                row.prop(loc_left_side,'DistanceValue',text="Left Panel Hang Height")
   
            if extend_right_side.CheckBoxValue:
                row = col.row()
                row.prop(self,'Height_Right_Side',text="Right Panel Height")
                row.prop(loc_right_side, 'DistanceValue',text="Right Panel Hang Height")
        
        self.draw_dogear_options(box)
        
        # CARCASS OPTIONS:
        col = box.column(align=True)
        col.label("Back Options:")
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
        
        dim = fd_types.Dimension()
        dim.parent(panel_mesh)
        dim.start_x(value = 0)
        dim.start_y(value = size[1]-unit.inch(3))
        dim.start_z(value = unit.inch(-100))
        dim.set_label(text)
        
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