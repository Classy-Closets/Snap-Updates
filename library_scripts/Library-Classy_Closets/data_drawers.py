import bpy
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

LOCK_DRAWER_TYPES=[('None','None','None'),
                   ('Top','Top','Top'),
                   ('Left','Left','Left'),
                   ('Right','Right','Right')]
FILE_RAIL_TYPES=[('Letter', 'Letter', 'Letter'),
                 ('Legal', 'Legal', 'Legal')]
FILE_DIRECTION_TYPES=[('Front to Back','Front to Back','Front to Back'),
                      ('Lateral', 'Lateral', 'Lateral')]

class Drawer_Stack(fd_types.Assembly):
    """ This drawer insert allows users to specify the quanity of drawers
        and the height of each indiviual drawer front height then the top 
        shelf is automatically placed based on the heights. The remaining 
        space is filled with an opening. The drawer max is 6.
    """
    property_id = props_closet.LIBRARY_NAME_SPACE + ".drawer_prompts"
    placement_type = "SPLITTER"
    type_assembly = "INSERT"
    mirror_y = False
    
    is_pull_out_tray = False

    number_of_drawers = 3 #1-9
    
    upper_interior = None
    upper_exterior = None
    
    def add_drawers(self):
        dim_x = self.get_var("dim_x")
        dim_y = self.get_var("dim_y")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Horizontal_Gap = self.get_var("Horizontal Gap")
        
        Front_Thickness = self.get_var("Front Thickness")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Open = self.get_var("Open")
        Drawer_Quantity = self.get_var("Drawer Quantity")
        Drawer_Stack_Height = self.get_var("Drawer Stack Height")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Use_Double_Pulls = self.get_var("Use Double Pulls")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Division_Thickness = self.get_var("Division Thickness")
        Lift_Drawers_From_Bottom = self.get_var("Lift Drawers From Bottom")
        Bottom_Drawer_Space = self.get_var("Bottom Drawer Space")
        No_Pulls = self.get_var("No Pulls")

        Shelf_Thickness = self.get_var("Shelf Thickness")
        Remove_Top_Shelf = self.get_var("Remove Top Shelf")
        Top_Overlay = self.get_var("Top Overlay")

        Full_Overlay = self.get_var("Full Overlay")
        Default_Middle_KD_Depth = self.get_var("Default Middle KD Depth")
        Max_Height_For_Centered_Pulls = self.get_var("Max Height For Centered Pulls")
        Large_Drawer_Pull_Height = self.get_var("Large Drawer Pull Height")
        Standard_Drawer_Rear_Gap = self.get_var("Standard Drawer Rear Gap")
        Deep_Drawer_Rear_Gap = self.get_var("Deep Drawer Rear Gap")
        Extra_Deep_Drawer_Box = self.get_var("Extra Deep Drawer Box")
        SDF = self.get_var("Small Drawer Face", "SDF")
        LDF = self.get_var("Large Drawer Face", "LDF")
        FHBD = self.get_var("Four Hole Box Difference", "FHBD")
        THBD = self.get_var("Three Hole Box Difference", "THBD")
        SDFOD = self.get_var("Single Door Full Overlay Difference", "SDFOD")
        AHOBD = self.get_var("Above Hamper Or Base Doors",'AHOBD')
        DBH = self.get_var("Double Box Height", "DBH")
        LDBH = self.get_var("Locked Double Box Height", "LDBH")
        Six_Hole = self.get_var("Six Hole")
        Seven_Hole = self.get_var("Seven Hole")

        prev_drawer_empty = None
        
        for i in range(1,self.number_of_drawers):
            DF_Height = self.get_var("Drawer " + str(i) + " Height","DF_Height")
            Lock_Drawer = self.get_var("Lock " + str(i) + " Drawer","Lock_Drawer")
            FR_Type = self.get_var("File Rail Type " + str(i), "FR_Type")
            FR_Direction = self.get_var("File Rail Direction " + str(i), "FR_Direction")
            Use_FR = self.get_var("Use File Rail " + str(i), "Use_FR")
            UDD = self.get_var("Use Double Drawer " + str(i), 'UDD')

            front_empty = self.add_empty()
            if prev_drawer_empty:
                prev_drawer_z_loc = prev_drawer_empty.get_var('loc_z','prev_drawer_z_loc')
                front_empty.z_loc('prev_drawer_z_loc-DF_Height-Horizontal_Gap',[prev_drawer_z_loc,DF_Height,Horizontal_Gap])
            else:
                front_empty.z_loc('Drawer_Stack_Height-DF_Height+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                                  [Drawer_Stack_Height,DF_Height,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])               
            
            df_z_loc = front_empty.get_var('loc_z','df_z_loc')
            
            front = common_parts.add_drawer_front(self)
            front.x_loc('IF(Full_Overlay,dim_x+(Right_Overlay*2),dim_x+Right_Overlay)',[dim_x,Right_Overlay,Full_Overlay])
            front.y_loc('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            front.z_loc('df_z_loc',[df_z_loc])
            front.x_rot(value = 90)
            front.y_rot(value = -90)
            front.z_rot(value = 0)
            front.x_dim('DF_Height',[DF_Height])
            front.y_dim('IF(Full_Overlay,(dim_x+(Shelf_Thickness*2)-SDFOD),dim_x+Left_Overlay+Right_Overlay)',[dim_x,Left_Overlay,Right_Overlay,Full_Overlay,Shelf_Thickness,SDFOD])
            front.z_dim('Front_Thickness',[Front_Thickness])
            front.prompt('No Pulls','No_Pulls',[No_Pulls])
            front.prompt('Use Double Pulls','Use_Double_Pulls',[Use_Double_Pulls])
            front.prompt('Center Pulls on Drawers','Center_Pulls_on_Drawers',[Center_Pulls_on_Drawers])
            front.prompt('Drawer Pull From Top','Drawer_Pull_From_Top',[Drawer_Pull_From_Top])
            front.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            front.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            front.prompt('Left Overlay','Left_Overlay',[Left_Overlay])
            front.prompt('Right Overlay','Right_Overlay',[Right_Overlay])            
            
            # front = common_parts.add_drawer_front(self)
            # front.x_loc('-Left_Overlay',[Left_Overlay])
            # front.y_loc('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            # front.z_loc('df_z_loc',[df_z_loc])
            # front.x_rot(value = 90)
            # front.y_rot(value = 0)
            # front.z_rot(value = 0)
            # front.x_dim('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            # front.y_dim('DF_Height',[DF_Height])
            # front.z_dim('Front_Thickness',[Front_Thickness])
            # front.prompt('Hide','IF(Drawer_Quantity>' + str(i-1) + ',False,True)',[Drawer_Quantity])
            # front.prompt('No Pulls','No_Pulls',[No_Pulls])
            # front.prompt('Use Double Pulls','Use_Double_Pulls',[Use_Double_Pulls])
            # front.prompt('Center Pulls on Drawers','Center_Pulls_on_Drawers',[Center_Pulls_on_Drawers])
            # front.prompt('Drawer Pull From Top','Drawer_Pull_From_Top',[Drawer_Pull_From_Top])
            # front.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            # front.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            # front.prompt('Left Overlay','Left_Overlay',[Left_Overlay])
            # front.prompt('Right Overlay','Right_Overlay',[Right_Overlay])
            
            l_pull = common_parts.add_drawer_pull(self)
            l_pull.set_name("Drawer Pull")
            l_pull.x_loc('-Left_Overlay',[Left_Overlay])
            l_pull.y_loc('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            l_pull.z_loc('df_z_loc',[df_z_loc])
            l_pull.x_rot(value = 90)
            l_pull.y_rot(value = 0)
            l_pull.z_rot(value = 0)
            l_pull.x_dim('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            l_pull.y_dim('DF_Height',[DF_Height])
            l_pull.z_dim('Front_Thickness',[Front_Thickness])
            l_pull.prompt("Pull X Location",'IF(DF_Height<Max_Height_For_Centered_Pulls,DF_Height/2,Large_Drawer_Pull_Height)',[Max_Height_For_Centered_Pulls,DF_Height,Large_Drawer_Pull_Height])
            l_pull.prompt("Pull Z Location",'IF(Use_Double_Pulls,(dim_x/4),(dim_x/2))+Right_Overlay',[Use_Double_Pulls,dim_x,Right_Overlay])
            l_pull.prompt('Hide','IF(No_Pulls,True,False)',[No_Pulls])
            
            r_pull = common_parts.add_drawer_pull(self)
            r_pull.set_name("Drawer Pull")
            r_pull.x_loc('-Left_Overlay',[Left_Overlay])
            r_pull.y_loc('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            r_pull.z_loc('df_z_loc',[df_z_loc])
            r_pull.x_rot(value = 90)
            r_pull.y_rot(value = 0)
            r_pull.z_rot(value = 0)
            r_pull.x_dim('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            r_pull.y_dim('DF_Height',[DF_Height])
            r_pull.z_dim('Front_Thickness',[Front_Thickness])
            r_pull.prompt("Pull X Location",'IF(DF_Height<Max_Height_For_Centered_Pulls,DF_Height/2,Large_Drawer_Pull_Height)',[Large_Drawer_Pull_Height,Max_Height_For_Centered_Pulls,Center_Pulls_on_Drawers,DF_Height,Drawer_Pull_From_Top])
            r_pull.prompt("Pull Z Location",'dim_x-(dim_x/4)+Right_Overlay',[dim_x,Right_Overlay])
            r_pull.prompt('Hide','IF(No_Pulls,True,IF(Use_Double_Pulls,False,True))',[No_Pulls,Use_Double_Pulls])
            
            drawer = common_parts.add_drawer(self)
            drawer.set_name("Drawer Box")
            drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
            drawer.y_loc('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            #drawer.z_loc('df_z_loc+Drawer_Box_Bottom_Gap+IF(' + Drawer_Quantity== str(i) + ',Bottom_Overlay,0)',[df_z_loc,Drawer_Box_Bottom_Gap,Bottom_Overlay])
            drawer.z_loc('df_z_loc+Drawer_Box_Bottom_Gap',[df_z_loc,Drawer_Box_Bottom_Gap])
            drawer.x_rot(value = 0)
            drawer.y_rot(value = 0)
            drawer.z_rot(value = 0)
            drawer.x_dim('dim_x-(Drawer_Box_Slide_Gap*2)',[dim_x,Drawer_Box_Slide_Gap])
            drawer.y_dim('IF(dim_y <= Extra_Deep_Drawer_Box, dim_y-Standard_Drawer_Rear_Gap, dim_y-Deep_Drawer_Rear_Gap)',[dim_y, Extra_Deep_Drawer_Box, Standard_Drawer_Rear_Gap, Deep_Drawer_Rear_Gap])

            drawer.z_dim("IF(DF_Height<SDF,DF_Height-THBD,IF(OR(Lock_Drawer==2,Lock_Drawer==3),IF(UDD,LDBH,DF_Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap),IF(DF_Height==SDF,DF_Height-FHBD,IF(UDD,DBH,DF_Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap))))", [DF_Height,SDF,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap,FHBD,THBD,Lock_Drawer,LDBH,DBH,UDD])
            
            drawer.prompt('Use File Rail','Use_FR',[Use_FR])
            drawer.prompt('File Rail Type','FR_Type',[FR_Type])
            drawer.prompt('File Rail Direction','FR_Direction',[FR_Direction])

            double_drawer = common_parts.add_drawer(self)
            double_drawer.set_name("Drawer Box")
            double_drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
            double_drawer.y_loc('-Door_to_Cabinet_Gap-(dim_y*(Open/2))',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            double_drawer.z_loc('df_z_loc+Drawer_Box_Bottom_Gap+Shelf_Thickness+IF(OR(Lock_Drawer==2,Lock_Drawer==3),LDBH,DBH)',[df_z_loc,Drawer_Box_Bottom_Gap,Lock_Drawer,DBH,LDBH,Shelf_Thickness])
            double_drawer.x_rot(value = 0)
            double_drawer.y_rot(value = 0)
            double_drawer.z_rot(value = 0)
            double_drawer.x_dim('dim_x-(Drawer_Box_Slide_Gap*2)',[dim_x,Drawer_Box_Slide_Gap])
            double_drawer.y_dim('IF(dim_y <= Extra_Deep_Drawer_Box, dim_y-Standard_Drawer_Rear_Gap, dim_y-Deep_Drawer_Rear_Gap)',[dim_y, Extra_Deep_Drawer_Box, Standard_Drawer_Rear_Gap, Deep_Drawer_Rear_Gap])

            double_drawer.z_dim("DBH",[DBH])

            double_drawer.prompt('Hide', "IF(AND(DF_Height >= Six_Hole,DF_Height <= Seven_Hole,dim_y >= "+ str(unit.inch(15.99)) +"),IF(UDD,False,True),True)",[UDD,DF_Height,Six_Hole,Seven_Hole,dim_y])
            
            double_drawer.prompt('Use File Rail','Use_FR',[Use_FR])
            double_drawer.prompt('File Rail Type','FR_Type',[FR_Type])
            double_drawer.prompt('File Rail Direction','FR_Direction',[FR_Direction])
            
            prev_drawer_empty = front_empty
            
            drawer_z_loc = drawer.get_var('loc_z','drawer_z_loc')
            drawer_z_dim = drawer.get_var('dim_z','drawer_z_dim')
             
            drawer_lock = common_parts.add_lock(self)
            drawer_lock.x_loc('IF(Lock_Drawer==2,-Division_Thickness,IF(Lock_Drawer==3,dim_x+Division_Thickness,dim_x/2))',[Lock_Drawer,dim_x,Division_Thickness])
            drawer_lock.y_loc('IF(Lock_Drawer==1,-Front_Thickness-Door_to_Cabinet_Gap-(dim_y*Open),+INCH(.75))',[Lock_Drawer,Front_Thickness,Door_to_Cabinet_Gap,Open,dim_y])
            drawer_lock.z_loc('drawer_z_loc+IF(UDD,DF_Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap,drawer_z_dim)-INCH(.5)',[drawer_z_loc,drawer_z_dim,UDD,DF_Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])    
            drawer_lock.y_rot(value = 0)
            drawer_lock.z_rot('IF(Lock_Drawer==2,radians(-90),IF(Lock_Drawer==3,radians(90),0))',[Lock_Drawer])
            drawer_lock.prompt('Hide', 'IF(Lock_Drawer>0,False,True)',[Lock_Drawer])


            KD_Shelf = common_parts.add_shelf(self)
            KD_Shelf.x_loc(value = 0)
            KD_Shelf.y_loc('Default_Middle_KD_Depth', [Default_Middle_KD_Depth])
            KD_Shelf.z_loc('df_z_loc+DF_Height-Top_Overlay',[df_z_loc,DF_Height,Top_Overlay])
            KD_Shelf.x_rot(value = 180)
            KD_Shelf.y_rot(value = 0)
            KD_Shelf.z_rot(value = 0)
            KD_Shelf.x_dim('dim_x',[dim_x])
            KD_Shelf.y_dim('Default_Middle_KD_Depth', [Default_Middle_KD_Depth])
            KD_Shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])

            KD_Shelf.prompt('Is Locked Shelf',value=True)
            KD_Shelf.prompt('Hide', value = True)

            KD_Shelf.y_dim('IF(Lock_Drawer>0, dim_y, Default_Middle_KD_Depth)', [Lock_Drawer, dim_y, Default_Middle_KD_Depth])
            KD_Shelf.y_loc('IF(Lock_Drawer>0, dim_y, Default_Middle_KD_Depth)', [Lock_Drawer, dim_y, Default_Middle_KD_Depth])

            if(i==1):
                KD_Shelf.y_dim('dim_y', [dim_y])
                KD_Shelf.y_loc('dim_y', [dim_y])
                KD_Shelf.prompt('Hide', 'IF(Remove_Top_Shelf,True,IF(Lock_Drawer>0,False,True))',[Remove_Top_Shelf,Lock_Drawer])
            if(i==2):
                KD_Shelf.prompt('Hide', 'IF(AHOBD,True,IF( Drawer_Quantity-1 == 2,False,IF( Drawer_Quantity-1 == 3,False,IF(Lock_Drawer>0,False,True))))', [Drawer_Quantity, Lock_Drawer,AHOBD])
                
            if(i==3):
                KD_Shelf.prompt('Hide', 'IF(Drawer_Quantity-1 == 4,False,IF(Drawer_Quantity-1 == 5,False,IF(Drawer_Quantity-1 == 7,False,IF(Lock_Drawer>0,False,True))))', [Drawer_Quantity, Lock_Drawer])
                
            if(i==4):
                KD_Shelf.prompt('Hide', 'IF(Drawer_Quantity-1 == 6,False,IF(Drawer_Quantity-1 == 8,False,IF(Lock_Drawer>0,False,True)))', [Drawer_Quantity, Lock_Drawer])
                
            if(i==5):
                KD_Shelf.prompt('Hide', 'IF(Drawer_Quantity-1 == 7,False,IF(Lock_Drawer>0,False,True))',[Lock_Drawer,Drawer_Quantity])
                
            if(i==6):
                KD_Shelf.prompt('Hide', 'IF(Drawer_Quantity-1 == 8,False,IF(Lock_Drawer>0,False,True))',[Lock_Drawer,Drawer_Quantity])
                
            if(i==7):
                KD_Shelf.prompt('Hide', 'IF(Lock_Drawer>0,False,True)',[Lock_Drawer])
                
            if(i==8):
                KD_Shelf.prompt('Hide', 'IF(Lock_Drawer>0,False,True)',[Lock_Drawer])

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_drawer_stack_bp = True
        
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_drawer_pull_prompts(self)
        common_prompts.add_drawer_box_prompts(self)
        
        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)
        self.add_prompt(name="Lift Drawers From Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Bottom Drawer Space",prompt_type='DISTANCE',value=0,tab_index=0)     
        self.add_prompt(name="Remove Bottom Shelf",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Remove Top Shelf",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Drawer Quantity",prompt_type='QUANTITY',value=self.number_of_drawers,tab_index=0)
        self.add_prompt(name="Drawer Stack Height",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Drawer Stack Backing Gap",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Use Mirror",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Cleat Location", prompt_type='COMBOBOX', items=["Above", "Below", "None"], value=0, tab_index=0, columns=3)
        self.add_prompt(name="Cleat Height",prompt_type='DISTANCE',value=unit.inch(3.64),tab_index=0)

        self.add_prompt(name="Default Middle KD Depth",prompt_type='DISTANCE',value=unit.inch(6),tab_index=1)
        self.add_prompt(name="Full Overlay",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Max Height For Centered Pulls",prompt_type='DISTANCE',value=unit.millimeter(315.95),tab_index=1)
        self.add_prompt(name="Large Drawer Pull Height",prompt_type='DISTANCE',value=unit.millimeter(93.98),tab_index=1)
        self.add_prompt(name="Standard Drawer Rear Gap",prompt_type='DISTANCE',value=unit.inch(1.25),tab_index=0)
        self.add_prompt(name="Deep Drawer Rear Gap",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
        self.add_prompt(name="Extra Deep Drawer Box",prompt_type='DISTANCE',value=unit.inch(16),tab_index=1)
        self.add_prompt(name="Small Drawer Face",prompt_type='DISTANCE',value=unit.millimeter(123.95),tab_index=1)
        self.add_prompt(name="Large Drawer Face",prompt_type='DISTANCE',value=unit.millimeter(315.95),tab_index=1)
        self.add_prompt(name="Four Hole Box Difference",prompt_type='DISTANCE',value=unit.inch(2.88),tab_index=1)
        self.add_prompt(name="Three Hole Box Difference",prompt_type='DISTANCE',value=unit.inch(1.62),tab_index=1)
        self.add_prompt(name="Pard Has Bottom KD",prompt_type='CHECKBOX',value=False,tab_index=1)

        self.add_prompt(name="Above Hamper Or Base Doors",prompt_type='CHECKBOX',value=False,tab_index=0)

        self.add_prompt(name="Six Hole",prompt_type='DISTANCE',value=unit.inch(7.4),tab_index=1)
        self.add_prompt(name="Seven Hole",prompt_type='DISTANCE',value=unit.inch(8.66),tab_index=1)
        self.add_prompt(name="Double Box Height",prompt_type='DISTANCE',value=unit.inch(2),tab_index=1)
        self.add_prompt(name="Locked Double Box Height",prompt_type='DISTANCE',value=unit.inch(2.68),tab_index=1)

        self.add_prompt(name="Above Hamper Or Base Doors",prompt_type='CHECKBOX',value=False,tab_index=0)

        for i in range(1,self.number_of_drawers):
            self.add_prompt(name="Lock " + str(i) + " Drawer",prompt_type='COMBOBOX',items=["None","Top","Left","Right"],value=0,tab_index=0,columns=4)        
            self.add_prompt(name="Drawer " + str(i) + " Height",prompt_type='DISTANCE',value=unit.millimeter(91.95),tab_index=0)
            self.add_prompt(name="File Rail Type " + str(i),prompt_type='COMBOBOX',value=0,items=['Letter', 'Legal'],tab_index=1)
            self.add_prompt(name="File Rail Direction " + str(i),prompt_type='COMBOBOX',value=0,items=['Front to Back','Lateral'],tab_index=1)
            self.add_prompt(name="Use File Rail " + str(i),prompt_type='CHECKBOX',value=False,tab_index=1)
            self.add_prompt(name="Use Double Drawer " + str(i),prompt_type='CHECKBOX',value=False,tab_index=1)
        
        dim_x = self.get_var("dim_x")
        dim_y = self.get_var("dim_y")
        dim_z = self.get_var("dim_z")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Drawer_Stack_Height = self.get_var("Drawer Stack Height")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        dq = self.get_var("Drawer Quantity",'dq')
        df1 = self.get_var("Drawer 1 Height",'df1')
        df2 = self.get_var("Drawer 2 Height",'df2')
        df3 = self.get_var("Drawer 3 Height",'df3')
        df4 = self.get_var("Drawer 4 Height",'df4')
        df5 = self.get_var("Drawer 5 Height",'df5')
        df6 = self.get_var("Drawer 6 Height",'df6')
        df7 = self.get_var("Drawer 7 Height",'df7')
        df8 = self.get_var("Drawer 8 Height",'df8')
        hg = self.get_var("Horizontal Gap",'hg')
        Lift_Drawers_From_Bottom = self.get_var("Lift Drawers From Bottom")
        Bottom_Drawer_Space = self.get_var("Bottom Drawer Space")
        Remove_Top_Shelf = self.get_var("Remove Top Shelf")
        Remove_Bottom_Shelf = self.get_var("Remove Bottom Shelf")
        Cleat_Location = self.get_var("Cleat Location")
        Cleat_Height = self.get_var("Cleat Height")

        self.prompt(
            'Drawer Stack Backing Gap',
            'Drawer_Stack_Height+Shelf_Thickness*2-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
            [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space,Cleat_Location]
        )
        
        self.prompt('Drawer Stack Height',
                    'df1+IF(dq>1,df2+hg,0)+IF(dq>2,df3+hg,0)+IF(dq>3,df4+hg,0)+IF(dq>4,df5+hg,0)+IF(dq>5,df6+hg,0)+IF(dq>6,df7+hg,0)+IF(dq>7,df8+hg,0)-Bottom_Overlay+MILLIMETER(.85688)', # ? Change height to allow correct door heights
                    [df1,df2,df3,df4,df5,df6,df7,df8,dq,hg,Bottom_Overlay])
        
        self.add_drawers()
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Bottom Cleat")
        cleat.x_loc(value = 0)
        cleat.y_loc('dim_y',[dim_y])
        cleat.z_loc('Drawer_Stack_Height+IF(Cleat_Location==0,Shelf_Thickness,0)-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space,Cleat_Location])
        cleat.x_rot(value=-90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0) 
        cleat.x_dim('dim_x',[dim_x])
        cleat.y_dim('IF(Cleat_Location==0,-Cleat_Height,Cleat_Height)', [Cleat_Height, Cleat_Location])
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        cleat.prompt("Hide", "IF(Cleat_Location==2,True,False)", [Cleat_Location])
        cleat.prompt('Use Cleat Cover', 'IF(Cleat_Location==0,True,False)', [Cleat_Location])     
        
        top_shelf = common_parts.add_shelf(self)
        top_shelf.x_loc(value = 0)
        top_shelf.y_loc('dim_y', [dim_y])
        top_shelf.z_loc('Drawer_Stack_Height-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        top_shelf.x_rot(value = 180)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 0)
        top_shelf.x_dim('dim_x',[dim_x])
        top_shelf.y_dim('dim_y',[dim_y])
        top_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.prompt('Hide','IF(Remove_Top_Shelf,False,True)',[Remove_Top_Shelf])
        top_shelf.prompt('Is Locked Shelf',value=True)
        
        '''
        second_shelf = common_parts.add_shelf(self)
        second_shelf.x_loc(value = 0)
        second_shelf.y_loc(value = 0)
        second_shelf.z_loc('IF(dq==4,df4,IF(dq==5,df5,IF(dq==6,df6,0)))-Bottom_Overlay+Shelf_Thickness-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                           [dq,df4,df5,df6,Bottom_Overlay,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        second_shelf.x_rot(value = 0)
        second_shelf.y_rot(value = 0)
        second_shelf.z_rot(value = 0)
        second_shelf.x_dim('dim_x',[dim_x])
        second_shelf.y_dim('dim_y',[dim_y])
        second_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        second_shelf.prompt('Hide','IF(dq>3,False,True)',[dq])
        second_shelf.prompt('Is Locked Shelf',value=True)
        '''
        
        top_shelf_z_loc = top_shelf.get_var('loc_z','top_shelf_z_loc')
        
        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.x_loc(value = 0)
        bottom_shelf.y_loc('dim_y', [dim_y])
        bottom_shelf.z_loc('IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)-Shelf_Thickness',
                        [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        bottom_shelf.x_rot(value = 180)
        bottom_shelf.y_rot(value = 0)
        bottom_shelf.z_rot(value = 0)
        bottom_shelf.x_dim('dim_x',[dim_x])
        bottom_shelf.y_dim('dim_y',[dim_y])
        bottom_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        bottom_shelf.prompt('Hide','IF(Remove_Bottom_Shelf,False,True)',[Remove_Bottom_Shelf])
        bottom_shelf.prompt('Is Locked Shelf',value=True)
        
        opening = common_parts.add_opening(self)
        opening.x_loc(value = 0)
        opening.y_loc(value = 0)
        opening.z_loc('top_shelf_z_loc+Shelf_Thickness',[top_shelf_z_loc,Shelf_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('dim_x',[dim_x])
        opening.y_dim('dim_y',[dim_y])
        opening.z_dim('dim_z-top_shelf_z_loc-Shelf_Thickness',[dim_z,top_shelf_z_loc,Shelf_Thickness])
        
        if self.upper_exterior:
            opening.obj_bp.mv.exterior_open = False
            
            self.upper_exterior.draw()
            self.upper_exterior.obj_bp.parent = self.obj_bp
            self.upper_exterior.x_loc(value = 0)
            self.upper_exterior.y_loc(value = 0)
            self.upper_exterior.z_loc('top_shelf_z_loc',[top_shelf_z_loc])
            self.upper_exterior.x_rot(value = 0)
            self.upper_exterior.y_rot(value = 0)
            self.upper_exterior.z_rot(value = 0)
            self.upper_exterior.x_dim('dim_x',[dim_x])
            self.upper_exterior.y_dim('dim_y',[dim_y])
            self.upper_exterior.z_dim('dim_z-top_shelf_z_loc',[dim_z,top_shelf_z_loc])
        
        if self.upper_interior:
            opening.obj_bp.mv.interior_open = False
            
            self.upper_interior.draw()
            self.upper_interior.obj_bp.parent = self.obj_bp
            self.upper_interior.x_loc(value = 0)
            self.upper_interior.y_loc(value = 0)
            self.upper_interior.z_loc('top_shelf_z_loc',[top_shelf_z_loc])
            self.upper_interior.x_rot(value = 0)
            self.upper_interior.y_rot(value = 0)
            self.upper_interior.z_rot(value = 0)
            self.upper_interior.x_dim('dim_x',[dim_x])
            self.upper_interior.y_dim('dim_y',[dim_y])
            self.upper_interior.z_dim('dim_z-top_shelf_z_loc',[dim_z,top_shelf_z_loc])          
        
        #self.update()
           
class PROMPTS_Drawer_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".drawer_prompts"
    bl_label = "Drawer Prompts" 
    bl_description = "This shows all of the available drawer options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    part = None
    
    drawer_quantity = bpy.props.EnumProperty(name="Drawer Quantity",
                                   items=[('1',"1",'1'),
                                          ('2',"2",'2'),
                                          ('3',"3",'3'),
                                          ('4',"4",'4'),
                                          ('5',"5",'5'),
                                          ('6',"6",'6'),
                                          ('7',"7",'7'),
                                          ('8',"8",'8'),
                                          ('9',"9",'9')],
                                   default = '3')
    
    drawer_1_height = bpy.props.EnumProperty(name="Drawer 1 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_2_height = bpy.props.EnumProperty(name="Drawer 2 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_3_height = bpy.props.EnumProperty(name="Drawer 3 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_4_height = bpy.props.EnumProperty(name="Drawer 4 Height",
                                   items=common_lists.FRONT_HEIGHTS)

    drawer_5_height = bpy.props.EnumProperty(name="Drawer 5 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_6_height = bpy.props.EnumProperty(name="Drawer 6 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_7_height = bpy.props.EnumProperty(name="Drawer 7 Height",
                                   items=common_lists.FRONT_HEIGHTS)

    drawer_8_height = bpy.props.EnumProperty(name="Drawer 8 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    lock_1_drawer = bpy.props.EnumProperty(name="Lock 1 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_2_drawer = bpy.props.EnumProperty(name="Lock 2 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_3_drawer = bpy.props.EnumProperty(name="Lock 3 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_4_drawer = bpy.props.EnumProperty(name="Lock 4 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_5_drawer = bpy.props.EnumProperty(name="Lock 5 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_6_drawer = bpy.props.EnumProperty(name="Lock 6 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')

    lock_7_drawer = bpy.props.EnumProperty(name="Lock 7 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None') 

    lock_8_drawer = bpy.props.EnumProperty(name="Lock 8 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')

    file_rail_type_1 = bpy.props.EnumProperty(name="File Rail Type 1",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_1 = bpy.props.EnumProperty(name="File Rail Direction 1",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')
    file_rail_type_2 = bpy.props.EnumProperty(name="File Rail Type 2",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_2 = bpy.props.EnumProperty(name="File Rail Direction 2",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')                         
    file_rail_type_3 = bpy.props.EnumProperty(name="File Rail Type 3",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_3 = bpy.props.EnumProperty(name="File Rail Direction 3",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')                         
    file_rail_type_4 = bpy.props.EnumProperty(name="File Rail Type 4",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_4 = bpy.props.EnumProperty(name="File Rail Direction 4",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')                         
    file_rail_type_5 = bpy.props.EnumProperty(name="File Rail Type 5",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_5 = bpy.props.EnumProperty(name="File Rail Direction 5",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')                         
    file_rail_type_6 = bpy.props.EnumProperty(name="File Rail Type 6",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_6 = bpy.props.EnumProperty(name="File Rail Direction 6",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')                         
    file_rail_type_7 = bpy.props.EnumProperty(name="File Rail Type 7",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_7 = bpy.props.EnumProperty(name="File Rail Direction 7",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')                         
    file_rail_type_8 = bpy.props.EnumProperty(name="File Rail Type 8",
                                              items=FILE_RAIL_TYPES,
                                              default = 'Letter')
    file_rail_direction_8 = bpy.props.EnumProperty(name="File Rail Direction 8",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default = 'Front to Back')                         
                             
    
    bottom_offset = bpy.props.EnumProperty(name="Bottom Offset",
                                   items=common_lists.DRAWER_BOTTOM_OFFSETS)

    front_heights = []
    
    drawer_qty_prompt = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        return {'FINISHED'}
        
    def check(self, context):
        if self.drawer_qty_prompt:
            props = props_closet.get_scene_props()
            
            self.drawer_qty_prompt.QuantityValue = int(self.drawer_quantity)
            small_drawer_face = self.assembly.get_prompt("Small Drawer Face")
            large_drawer_face = self.assembly.get_prompt("Large Drawer Face")
            six_hole = self.assembly.get_prompt("Six Hole")
            seven_hole = self.assembly.get_prompt("Seven Hole")
                
            for i in range(1,self.drawer_qty_prompt.value()):
                drawer_height = self.assembly.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer")
                slide_type = self.assembly.get_prompt("Drawer " + str(i) + " Slide Type") #DONT REMOVE USED in exec
                file_rail_type = self.assembly.get_prompt("File Rail Type " + str(i))
                file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(i))
                use_double_drawer = self.assembly.get_prompt("Use Double Drawer " + str(i))
                bottom_offset = self.assembly.get_prompt("Bottom Drawer Space")
                if props.closet_defaults.use_32mm_system: 
                    if drawer_height:
                        if not drawer_height.equal:
                            exec("drawer_height.set_value(unit.inch(float(self.drawer_" + str(i) + "_height) / 25.4))")
                    if bottom_offset:
                        bottom_offset.set_value(unit.inch(float(self.bottom_offset)/25.4))

                if lock_drawer:
                    exec("lock_drawer.set_value(self.lock_" + str(i) + "_drawer)")
                if slide_type:
                    exec("slide_type.set_value(self.drawer_" + str(i) + "_slide)")
                if file_rail_type:
                    exec("file_rail_type.set_value(self.file_rail_type_" + str(i) + ")")
                if file_rail_direction:
                    exec("file_rail_direction.set_value(self.file_rail_direction_" + str(i) + ")")
                if(drawer_height.value() < small_drawer_face.value()):
                    lock_drawer.set_value("None")
                if(drawer_height.value() < six_hole.value() or drawer_height.value() > seven_hole.value() or self.assembly.obj_y.location.y < unit.inch(15.99)):
                    use_double_drawer.set_value(False)                    

            pard_has_bottom_KD = self.assembly.get_prompt("Pard Has Bottom KD")
            remove_bottom_shelf = self.assembly.get_prompt("Remove Bottom Shelf")
            lift_drawers_from_bottom = self.assembly.get_prompt("Lift Drawers From Bottom")
            parent_assembly = fd_types.Assembly(self.assembly.obj_bp.parent)
            RBS = parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + self.assembly.obj_bp.mv.opening_name)
            if(lift_drawers_from_bottom.value()):
                pard_has_bottom_KD.set_value(False)
            elif(RBS):
                if(RBS.value()):
                    pard_has_bottom_KD.set_value(True)
            if(pard_has_bottom_KD.value()):
                remove_bottom_shelf.set_value(False)

        self.assign_mirror_material(self.assembly.obj_bp)
        utils.run_calculators(self.assembly.obj_bp)
        bpy.ops.cabinetlib.update_scene_from_pointers()
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport

        # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        props_closet.update_render_materials(self, context)
        return True

    def get_front_heights(self):
        self.front_heights = []
        for front in common_lists.FRONT_HEIGHTS:
            self.front_heights.append(front[0])

    def set_properties_from_prompts(self):
        props = props_closet.get_scene_props()
        bottom_offset = self.assembly.get_prompt("Bottom Drawer Space").value()

        if bottom_offset:
            self.bottom_offset = str(round(unit.meter_to_millimeter(bottom_offset)))
        
        self.get_front_heights()
        
        self.drawer_qty_prompt = self.assembly.get_prompt("Drawer Quantity")
        if self.drawer_qty_prompt:
            self.drawer_quantity = str(self.drawer_qty_prompt.QuantityValue)
                    
            for i in range(1,self.drawer_qty_prompt.value()):
                drawer_height = self.assembly.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer") #DONT REMOVE USED in exec
                file_rail_type = self.assembly.get_prompt("File Rail Type " + str(i)) #DONT REMOVE USED in exec
                file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(i)) #DONT REMOVE USED in exec
                exec("self.lock_" + str(i) + "_drawer = lock_drawer.value()")
                exec("self.file_rail_type_" + str(i) + " = file_rail_type.value()")
                exec("self.file_rail_direction_" + str(i) + " = file_rail_direction.value()")
                if props.closet_defaults.use_32mm_system:  
                    if drawer_height:
                        value = str(round(drawer_height.DistanceValue * 1000,3))
                        if value in self.front_heights:
                            exec("self.drawer_" + str(i) + "_height = value")

    def assign_mirror_material(self,obj):
        use_mirror = self.assembly.get_prompt("Use Mirror")
        if use_mirror.value():
            if obj.cabinetlib.type_mesh == 'BUYOUT':
                for mat_slot in obj.cabinetlib.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Mirror'  
        else:
            if obj.cabinetlib.type_mesh == 'BUYOUT':
                for mat_slot in obj.cabinetlib.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Glass'  

        for child in obj.children:
            self.assign_mirror_material(child)

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_assembly_bp = utils.get_assembly_bp(obj)
        self.part = fd_types.Assembly(obj_assembly_bp)
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=450)
    
    def draw_drawer_heights(self,layout):
        col = layout.column(align=True)
        props = props_closet.get_scene_props()
              
        drawer_quantity = self.assembly.get_prompt("Drawer Quantity")
        small_drawer_face = self.assembly.get_prompt("Small Drawer Face")
        large_drawer_face = self.assembly.get_prompt("Large Drawer Face")
        six_hole = self.assembly.get_prompt("Six Hole")
        seven_hole = self.assembly.get_prompt("Seven Hole")
        
        if drawer_quantity:
            for i in range(1,drawer_quantity.value()):
                
                drawer_height = self.assembly.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer")

                file_rail_type = self.assembly.get_prompt("File Rail Type " + str(i))
                file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(i))
                use_file_rail = self.assembly.get_prompt("Use File Rail " + str(i))
                use_double_drawer = self.assembly.get_prompt("Use Double Drawer " + str(i))
                extra_deep_drawer_box = self.assembly.get_prompt("Extra Deep Drawer Box")
                if(drawer_height and lock_drawer and file_rail_type and file_rail_direction and use_file_rail and extra_deep_drawer_box):
                    if(self.assembly.obj_y.location.y<=extra_deep_drawer_box.value()):
                        drawer_box_rear_gap = self.assembly.get_prompt("Standard Drawer Rear Gap")
                    else:
                        drawer_box_rear_gap = self.assembly.get_prompt("Deep Drawer Rear Gap")

                    width = self.assembly.obj_x.location.x - unit.inch(2)
                    depth = self.assembly.obj_y.location.y - drawer_box_rear_gap.value()
                    letter = unit.inch(12.5)
                    legal = unit.inch(15.5)

                    if drawer_height and drawer_quantity.value() >= i:
                        box = col.box()
                        row = box.row()

                        col_1 = row.column()
                        if props.closet_defaults.use_32mm_system:  
                            col_1.label("Drawer " + str(i) + " Height:")
                            col_1.prop(self,'drawer_' + str(i) + '_height',text="")
                        else:
                            drawer_height.draw_prompt(col_1)

                        
                        if(drawer_height.value() >= small_drawer_face.value()):
                            col_2 = row.column()
                            col_2.label("Lock:")
                            col_2.prop(self,'lock_' + str(i) + '_drawer',text="")
                        else:
                            lock_drawer.set_value('None')

                        if(drawer_height and six_hole and seven_hole):
                            if(drawer_height.value() >= six_hole.value() and drawer_height.value() <= seven_hole.value() and self.assembly.obj_y.location.y >= unit.inch(15.99)):
                                col_3 = row.column(align=True)
                                col_3.label("Double Jewelry Drawer")
                                col_3.prop(use_double_drawer,"CheckBoxValue",text="")

                        if(drawer_height.value()>=large_drawer_face.value() and (width >= letter or depth >= letter)):
                            col_3 = row.column(align=True)
                            #row.label("File Rail:")
                            col_3.prop(use_file_rail,"CheckBoxValue",text="File Rail")
                        
                            if(use_file_rail.value()):
                                if(width<letter):
                                    if(depth<legal):

                                        col_3.label("Letter")
                                        exec("file_rail_type_" +str(i)+"= 'Letter'")
                                        file_rail_type.set_value('Letter')

                                        col_3.label("Lateral")
                                        exec("file_rail_direction_" +str(i)+"= 'Lateral'")
                                        file_rail_direction.set_value('Lateral')

                                    else:

                                        col_3.prop(self,'file_rail_type_' + str(i),text="")

                                        
                                        col_3.label("Lateral")
                                        exec("file_rail_direction_" +str(i)+"= 'Lateral'")
                                        file_rail_direction.set_value('Lateral')
                                    
                                elif(width<legal):
                                    if(depth<letter):

                                        col_3.label("Letter")
                                        exec("file_rail_type_" +str(i)+"= 'Letter'")
                                        file_rail_type.set_value('Letter')

                                        col_3.label("Front to Back")
                                        exec("file_rail_direction_" +str(i)+"= 'Front to Back'")
                                        file_rail_direction.set_value('Front to Back')

                                    elif(depth<legal):

                                        col_3.label("Letter")
                                        exec("file_rail_type_" +str(i)+"= 'Letter'")
                                        file_rail_type.set_value('Letter')

                                        col_3.prop(self,'file_rail_direction_' + str(i),text="")

                                    else:
                                        
                                        if(file_rail_direction.value() == 'Front to Back'):
                                            col_3.label("Letter")
                                            exec("file_rail_type_" +str(i)+"= 'Letter'")
                                            file_rail_type.set_value('Letter')

                                            col_3.prop(self,'file_rail_direction_' + str(i),text="")
                                        else:
                                            col_3.prop(self,'file_rail_type_' + str(i),text="")

                                            col_3.prop(self,'file_rail_direction_' + str(i),text="")
                                
                                else:
                                    if(depth<letter):

                                        col_3.prop(self,'file_rail_type_' + str(i),text="")

                                        col_3.label("Front to Back")
                                        exec("file_rail_direction_" +str(i)+"= 'Front to Back'")
                                        file_rail_direction.set_value('Front to Back')
                                    elif(depth<legal):
                                        if(file_rail_direction.value() == 'Lateral'):
                                            col_3.label("Letter")
                                            exec("file_rail_type_" +str(i)+"= 'Letter'")
                                            file_rail_type.set_value('Letter')

                                            col_3.prop(self,'file_rail_direction_' + str(i),text="")
                                        else:
                                            col_3.prop(self,'file_rail_type_' + str(i),text="")

                                            col_3.prop(self,'file_rail_direction_' + str(i),text="")
                                    else:
                                        col_3.prop(self,'file_rail_type_' + str(i),text="")

                                        col_3.prop(self,'file_rail_direction_' + str(i),text="")

                        else:
                            use_file_rail.set_value(False)


    def is_glass_front(self):
        if "Glass" in self.part.obj_bp.mv.comment:
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                if self.drawer_qty_prompt:
                    open_drawer = self.assembly.get_prompt('Open')
                    box = layout.box()

                    full_overlay = self.assembly.get_prompt('Full Overlay')
                    standard_drawer_rear_gap = self.assembly.get_prompt("Standard Drawer Rear Gap")
                    deep_drawer_rear_gap = self.assembly.get_prompt("Deep Drawer Rear Gap")
                    drawer_depth = self.assembly.obj_y.location.y
                    extra_deep_drawer_box = self.assembly.get_prompt("Extra Deep Drawer Box")

                    #hot = self.assembly.get_prompt('Half Overlay Top')
                    #hob = self.assembly.get_prompt('Half Overlay Bottom')
                    #hol = self.assembly.get_prompt('Half Overlay Left')
                    #hor = self.assembly.get_prompt('Half Overlay Right')
                    use_double_pulls = self.assembly.get_prompt('Use Double Pulls')
                    remove_top_shelf = self.assembly.get_prompt('Remove Top Shelf')
                    remove_bottom_shelf = self.assembly.get_prompt('Remove Bottom Shelf')
                    lift_drawers_from_bottom = self.assembly.get_prompt('Lift Drawers From Bottom')
                    no_pulls = self.assembly.get_prompt('No Pulls')
                    use_mirror = self.assembly.get_prompt("Use Mirror")
                    cleat_loc = self.assembly.get_prompt("Cleat Location")

                    propbox = box.box()
                    propbox.label("Options:",icon='SCRIPT')
                    
                    row = propbox.row()
                    row.label("Open Drawers")
                    row.prop(open_drawer,'PercentageValue',text="")

                    row = propbox.row()
                    row.label("Drawer Rear Gap")
                    if(drawer_depth<=extra_deep_drawer_box.value()):
                        row.prop(standard_drawer_rear_gap,"DistanceValue",text="")
                    else:
                        row.prop(deep_drawer_rear_gap,"DistanceValue",text="")

                    row = propbox.row()
                    if cleat_loc:
                        cleat_loc.draw_prompt(row, text="Cleat Location")

                    row = propbox.row()
                    if lift_drawers_from_bottom:
                        lift_drawers_from_bottom.draw_prompt(row,text="Suspended Drawers",split_text=False)

                    if lift_drawers_from_bottom.value():
                        row.prop(self,'bottom_offset',text="")

                    row = propbox.row()
                    if use_double_pulls:
                        use_double_pulls.draw_prompt(row,split_text=False)
                    if no_pulls:
                        no_pulls.draw_prompt(row,split_text=False)
                    
                    row = propbox.row()
                    if remove_top_shelf:
                        row.prop(remove_top_shelf,"CheckBoxValue",text="Top KD")
                    if remove_bottom_shelf:
                        row.prop(remove_bottom_shelf,"CheckBoxValue",text="Bottom KD")
                    
                    row = propbox.row()
                    row = propbox.row()
                    full_overlay.draw_prompt(row,split_text=False,text="Full Overlay")
                    #row.label("Half Overlays:")
                    #hot.draw_prompt(row,split_text=False,text="Top")
                    #hob.draw_prompt(row,split_text=False,text="Bottom")
                    #hol.draw_prompt(row,split_text=False,text="Left")
                    #hor.draw_prompt(row,split_text=False,text="Right")    
                    #half_overlay.draw_prompt(row,split_text=False,text="Half")                

                    if self.is_glass_front():
                        row = propbox.row()
                        use_mirror.draw_prompt(row,split_text=False)

                    self.draw_drawer_heights(box)

class OPS_Drawer_Drop(bpy.types.Operator):
    bl_idname = "closets.insert_drawer_drop"
    bl_label = "Custom drag and drop for drawers insert"

    object_name = bpy.props.StringProperty(name="Object Name")
    product_name = bpy.props.StringProperty(name="Product Name")
    category_name = bpy.props.StringProperty(name="Category Name")
    library_name = bpy.props.StringProperty(name="Library Name")

    insert = None
    default_z_loc = 0.0
    default_height = 0.0
    default_depth = 0.0
    
    openings = []
    objects = []
    
    header_text = "Place Insert   (Esc, Right Click) = Cancel Command  :  (Left Click) = Place Insert"
    
    def execute(self, context):
        return {'FINISHED'}

    def __del__(self):
        bpy.context.area.header_text_set()

    def set_wire_and_xray(self, obj, turn_on):
        if turn_on:
            obj.draw_type = 'WIRE'
        else:
            obj.draw_type = 'TEXTURED'
        obj.show_x_ray = turn_on
        for child in obj.children:
            self.set_wire_and_xray(child,turn_on)

    def get_insert(self,context):
        bpy.ops.object.select_all(action='DESELECT')
        
        if self.object_name in bpy.data.objects:
            bp = bpy.data.objects[self.object_name]
            self.insert = fd_types.Assembly(bp)
        
        if not self.insert:
            lib = context.window_manager.cabinetlib.lib_inserts[self.library_name]
            blend_path = os.path.join(lib.lib_path,self.category_name,self.product_name + ".blend")
            obj_bp = None

            if os.path.exists(blend_path):
                obj_bp = utils.get_group(blend_path)
                self.insert = fd_types.Assembly(obj_bp)
            else:
                self.insert = utils.get_insert_class(context,self.library_name,self.category_name,self.product_name)
    
            if obj_bp:
                pass
            #TODO: SET UP UPDATE OPERATOR
                    # self.insert.update(obj_bp)
            else:
                self.insert.draw()
                self.insert.update()
            
        self.show_openings()
        utils.init_objects(self.insert.obj_bp)
        self.default_z_loc = self.insert.obj_bp.location.z
        self.default_height = self.insert.obj_z.location.z
        self.default_depth = self.insert.obj_y.location.y

    def invoke(self,context,event):
        self.insert = None
        context.window.cursor_set('WAIT')
        self.get_insert(context)
        self.set_wire_and_xray(self.insert.obj_bp, True)
        if self.insert is None:
            bpy.ops.fd_general.error('INVOKE_DEFAULT',message="Could Not Find Insert Class: " + "\\" + self.library_name + "\\" + self.category_name + "\\" + self.product_name)
            return {'CANCELLED'}
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.insert:
            utils.delete_object_and_children(self.insert.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def show_openings(self):
        #Clear  to avoid old/duplicate openings
        self.objects.clear()
        insert_type = self.insert.obj_bp.mv.placement_type
        for obj in  bpy.context.scene.objects:
            #Check to avoid opening that is part of the dropped insert
            if utils.get_parent_assembly_bp(obj) == self.insert.obj_bp:
                continue

            if obj.layers[0]: #Make sure wall is not hidden
                opening = None
                if obj.mv.type_group == 'OPENING':
                    if insert_type in {'INTERIOR','SPLITTER'}:
                        opening = fd_types.Assembly(obj) if obj.mv.interior_open else None
                    if insert_type == 'EXTERIOR':
                        opening = fd_types.Assembly(obj) if obj.mv.exterior_open else None
                    if opening:
                        cage = opening.get_cage()
                        opening.obj_x.hide = True
                        opening.obj_y.hide = True
                        opening.obj_z.hide = True
                        cage.hide_select = False
                        cage.hide = False
                        self.objects.append(cage)

    def selected_opening(self,selected_obj):
        if selected_obj:
            opening = fd_types.Assembly(selected_obj.parent)
            if opening.obj_bp.parent:
                if self.insert.obj_bp.parent is not opening.obj_bp.parent:
                    self.insert.obj_bp.parent = opening.obj_bp.parent
                    self.insert.obj_bp.location = opening.obj_bp.location
                    self.insert.obj_bp.rotation_euler = opening.obj_bp.rotation_euler
                    self.insert.obj_x.location.x = opening.obj_x.location.x
                    self.insert.obj_y.location.y = opening.obj_y.location.y
                    self.insert.obj_z.location.z = opening.obj_z.location.z
                    utils.run_calculators(self.insert.obj_bp)
                    return opening
            
    def set_opening_name(self,obj,name):
        obj.mv.opening_name = name
        for child in obj.children:
            self.set_opening_name(child, name)
        
    def place_insert(self,opening):
        if self.insert.obj_bp.mv.placement_type == 'INTERIOR':
            opening.obj_bp.mv.interior_open = False
        if self.insert.obj_bp.mv.placement_type == 'EXTERIOR':
            opening.obj_bp.mv.exterior_open = False
        if self.insert.obj_bp.mv.placement_type == 'SPLITTER':
            opening.obj_bp.mv.interior_open = False
            opening.obj_bp.mv.exterior_open = False

        utils.copy_assembly_drivers(opening,self.insert)
        self.set_opening_name(self.insert.obj_bp, opening.obj_bp.mv.opening_name)
        self.set_wire_and_xray(self.insert.obj_bp, False)
        
        for obj in self.objects:
            obj.hide = True
            obj.hide_render = True
            obj.hide_select = True

    def insert_drop(self,context,event):
        if len(self.objects) == 0:
            bpy.ops.fd_general.error('INVOKE_DEFAULT',message="There are no openings in this scene.")
            return self.cancel_drop(context,event)
        else:
            selected_point, selected_obj = utils.get_selection_point(context,event,objects=self.objects)
            bpy.ops.object.select_all(action='DESELECT')
            selected_opening = self.selected_opening(selected_obj)
            if selected_opening:
                selected_obj.select = True
    
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.place_insert(selected_opening)
                    self.set_backing_bottom_gap(self.insert.obj_bp, selected_opening)
                    self.set_drawer_cleat_hide(self.insert.obj_bp, selected_opening)
                    self.set_bottom_KD(self.insert.obj_bp,selected_opening)
                    self.set_above_hamper_or_base_door(self.insert.obj_bp)
                    context.scene.objects.active = self.insert.obj_bp
                    # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
                    utils.run_calculators(self.insert.obj_bp)
                    utils.run_calculators(self.insert.obj_bp)
                    # TOP LEVEL PRODUCT RECAL
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))

                    bpy.context.window.cursor_set('DEFAULT')
                    
                    return {'FINISHED'}

            return {'RUNNING_MODAL'}

    def set_drawer_cleat_hide(self, insert_bp, selected_opening):
        drawer_assembly = fd_types.Assembly(insert_bp)
        carcass_bp = utils.get_parent_assembly_bp(insert_bp)
        carcass_assembly = fd_types.Assembly(carcass_bp)
        opening_name = selected_opening.obj_bp.mv.opening_name
        Back_Thickness = carcass_assembly.get_var("Opening " + opening_name + " Backing Thickness", "Back_Thickness")
        Cleat_Location = drawer_assembly.get_var("Cleat Location")

        for child in insert_bp.children:
            if child.lm_closets.is_cleat_bp:
                cleat_assembly = fd_types.Assembly(child)
                cleat_assembly.prompt('Hide', 'IF(OR(Cleat_Location==2,Back_Thickness==1),True,False)', [Back_Thickness, Cleat_Location])

    def set_backing_bottom_gap(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.mv.opening_name
        carcass_bp = utils.get_parent_assembly_bp(insert_bp)
        drawer_assembly = fd_types.Assembly(insert_bp)        
        Drawer_Stack_Backing_Gap = drawer_assembly.get_var('Drawer Stack Backing Gap')

        for child in carcass_bp.children:
            if child.lm_closets.is_back_bp:
                if child.mv.opening_name == opening_name:
                    back_assembly = fd_types.Assembly(child)
                    bottom_insert_gap = back_assembly.get_prompt('Bottom Insert Gap')

                    if bottom_insert_gap:
                        back_assembly.prompt('Bottom Insert Gap', 'Drawer_Stack_Backing_Gap', [Drawer_Stack_Backing_Gap])
    
    def set_above_hamper_or_base_door(self, insert_bp):
        drawer_assembly = fd_types.Assembly(insert_bp)
        above_hamper_or_base_door = drawer_assembly.get_prompt("Above Hamper Or Base Doors")
        parent_bp = utils.get_parent_assembly_bp(insert_bp)

        if(above_hamper_or_base_door):
            if(parent_bp.lm_closets.is_door_bp):
                door_assembly = fd_types.Assembly(parent_bp)
                door_type = door_assembly.get_prompt("Door Type")
                if(door_type):
                    if(door_type.value() == 'Base'):
                        above_hamper_or_base_door.set_value(True)
            elif(parent_bp.lm_closets.is_hamper_bp):
                above_hamper_or_base_door.set_value(True)
            else:
                for child in parent_bp.children:
                    if(child.lm_closets.is_door_insert_bp):
                        door_assembly = fd_types.Assembly(child)
                        door_type = door_assembly.get_prompt("Door Type")
                        if(door_type):
                            if(door_type.value() == 'Base'):
                                above_hamper_or_base_door.set_value(True)
                    elif(child.lm_closets.is_hamper_insert_bp):
                        above_hamper_or_base_door.set_value(True)

    def set_bottom_KD(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.mv.opening_name
        carcass_bp = utils.get_parent_assembly_bp(insert_bp)
        drawer_assembly = fd_types.Assembly(insert_bp)   
        carcass_assembly = fd_types.Assembly(carcass_bp)
        if(carcass_assembly.get_prompt("Opening " + str(opening_name) + " Floor Mounted") and carcass_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(opening_name))):
            if(carcass_assembly.get_prompt("Opening " + str(opening_name) + " Floor Mounted").value() or carcass_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(opening_name)).value()):
                drawer_assembly.get_prompt("Pard Has Bottom KD").set_value(True)

    def modal(self, context, event):
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC','RIGHTMOUSE'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.insert_drop(context,event)


bpy.utils.register_class(PROMPTS_Drawer_Prompts)
bpy.utils.register_class(OPS_Drawer_Drop)
