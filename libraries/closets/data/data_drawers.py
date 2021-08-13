import os
import math

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty


from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts
from ..common import common_lists

LOCK_DRAWER_TYPES=[('0','None','None'),
                   ('1','Top','Top'),
                   ('2','Left','Left'),
                   ('3','Right','Right')]
FILE_RAIL_TYPES=[('0', 'Letter', 'Letter'),
                 ('1', 'Legal', 'Legal')]
FILE_DIRECTION_TYPES=[('0','Front to Back','Front to Back'),
                      ('1', 'Lateral', 'Lateral')]


class Drawer_Stack(sn_types.Assembly):
    """ This drawer insert allows users to specify the quanity of drawers
        and the height of each indiviual drawer front height then the top
        shelf is automatically placed based on the heights. The remaining
        space is filled with an opening. The drawer max is 6.
    """
    type_assembly = "INSERT"
    id_prompt = "sn_closets.drawer_prompts"
    drop_id = "sn_closets.insert_drawer_drop"
    placement_type = "SPLITTER"
    show_in_library = True
    category_name = "Closet Products - Drawers"
    mirror_y = False

    is_pull_out_tray = False
    number_of_drawers = 3 #1-9
    upper_interior = None
    upper_exterior = None
    drawer_front_ppt_obj = None
    stack_height_ppt_obj = None
    backing_gap_ppt_obj = None
    overlay_ppt_obj = None

    def add_prompts(self):
        common_prompts.add_thickness_prompts(self)
        self.overlay_ppt_obj = common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_drawer_pull_prompts(self)
        common_prompts.add_drawer_box_prompts(self)
        self.add_prompt("Open", 'PERCENTAGE', 0)
        self.add_prompt("Lift Drawers From Bottom", 'CHECKBOX', False)
        self.add_prompt("Bottom Drawer Space", 'DISTANCE', 0)
        self.add_prompt("Remove Bottom Shelf", 'CHECKBOX', True)
        self.add_prompt("Remove Top Shelf", 'CHECKBOX', True)
        self.add_prompt("Shelf Thickness", 'DISTANCE', sn_unit.inch(0.75))
        self.add_prompt("Drawer Quantity", 'QUANTITY', self.number_of_drawers)
        # self.add_prompt("Drawer Stack Height", 'DISTANCE', 0)
        # self.add_prompt("Drawer Stack Backing Gap", 'DISTANCE', 0)
        self.add_prompt("Use Mirror", 'CHECKBOX', False)
        self.add_prompt("Cleat Location", 'COMBOBOX', 0, ["Above", "Below", "None"])
        self.add_prompt("Cleat Height", 'DISTANCE', sn_unit.inch(3.64))
        self.add_prompt("Default Middle KD Depth", 'DISTANCE', sn_unit.inch(6))
        self.add_prompt("Full Overlay", 'CHECKBOX', False)
        self.add_prompt("Max Height For Centered Pulls", 'DISTANCE', sn_unit.millimeter(315.95))
        self.add_prompt("Large Drawer Pull Height", 'DISTANCE', sn_unit.millimeter(93.98))
        self.add_prompt("Standard Drawer Rear Gap", 'DISTANCE', sn_unit.inch(1.25))
        self.add_prompt("Deep Drawer Rear Gap", 'DISTANCE', sn_unit.inch(2))
        self.add_prompt("Extra Deep Drawer Box", 'DISTANCE', sn_unit.inch(16))
        self.add_prompt("Small Drawer Face", 'DISTANCE', sn_unit.millimeter(123.95))
        self.add_prompt("Large Drawer Face", 'DISTANCE', sn_unit.millimeter(315.95))
        self.add_prompt("Four Hole Box Difference", 'DISTANCE', sn_unit.inch(2.88))
        self.add_prompt("Three Hole Box Difference", 'DISTANCE', sn_unit.inch(1.62))
        self.add_prompt("Pard Has Bottom KD", 'CHECKBOX', False)
        self.add_prompt("Above Hamper Or Base Doors", 'CHECKBOX', False)
        self.add_prompt("Six Hole", 'DISTANCE', sn_unit.inch(7.4))
        self.add_prompt("Seven Hole", 'DISTANCE', sn_unit.inch(8.66))
        self.add_prompt("Double Box Height", 'DISTANCE', sn_unit.inch(2))
        self.add_prompt("Locked Double Box Height", 'DISTANCE', sn_unit.inch(2.68))
        self.add_prompt("Above Hamper Or Base Doors", 'CHECKBOX', False)

    def add_drawer_box_prompts(self, drawer_num):
        self.add_prompt("Lock " + str(drawer_num) + " Drawer", 'COMBOBOX', 0, ["None", "Top", "Left", "Right"])
        self.add_prompt("File Rail Type " + str(drawer_num), 'COMBOBOX', 0, ['Letter', 'Legal'])
        self.add_prompt("File Rail Direction " + str(drawer_num), 'COMBOBOX', 0, ['Front to Back', 'Lateral'])
        self.add_prompt("Use File Rail " + str(drawer_num), 'CHECKBOX', False)
        self.add_prompt("Use Double Drawer " + str(drawer_num), 'CHECKBOX', False)

    def add_drawers(self):
        dim_x = self.obj_x.snap.get_var("location.x", "dim_x")
        dim_y = self.obj_y.snap.get_var("location.y", "dim_y")
        Left_Overlay = self.get_prompt("Left Overlay").get_var('Left_Overlay')
        Right_Overlay = self.get_prompt("Right Overlay").get_var('Right_Overlay')
        #Bottom_Overlay = self.get_prompt("Bottom Overlay")
        Horizontal_Gap = self.overlay_ppt_obj.snap.get_prompt("Horizontal Gap").get_var()
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Door_to_Cabinet_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_to_Cabinet_Gap')
        Open = self.get_prompt("Open").get_var('Open')
        Drawer_Quantity = self.get_prompt("Drawer Quantity").get_var('Drawer_Quantity')
        Drawer_Stack_Height = self.stack_height_ppt_obj.snap.get_prompt("Drawer Stack Height").get_var('Drawer_Stack_Height')
        Center_Pulls_on_Drawers = self.get_prompt("Center Pulls on Drawers").get_var('Center_Pulls_on_Drawers')
        Drawer_Pull_From_Top = self.get_prompt("Drawer Pull From Top").get_var('Drawer_Pull_From_Top')
        Use_Double_Pulls = self.get_prompt("Use Double Pulls").get_var('Use_Double_Pulls')
        Drawer_Box_Slide_Gap = self.get_prompt("Drawer Box Slide Gap").get_var('Drawer_Box_Slide_Gap')
        Drawer_Box_Bottom_Gap = self.get_prompt("Drawer Box Bottom Gap").get_var('DBBG')
        # Drawer_Box_Rear_Gap = self.get_prompt("Drawer Box Rear Gap").get_var('Drawer_Box_Rear_Gap')
        Drawer_Box_Top_Gap = self.get_prompt("Drawer Box Top Gap").get_var('DBTG')
        Division_Thickness = self.get_prompt("Division Thickness").get_var('Division_Thickness')
        Lift_Drawers_From_Bottom = self.get_prompt("Lift Drawers From Bottom").get_var('Lift_Drawers_From_Bottom')
        Bottom_Drawer_Space = self.get_prompt("Bottom Drawer Space").get_var('Bottom_Drawer_Space')
        No_Pulls = self.get_prompt("No Pulls").get_var('No_Pulls')

        Shelf_Thickness = self.get_prompt("Shelf Thickness").get_var('Shelf_Thickness')
        Remove_Top_Shelf = self.get_prompt("Remove Top Shelf").get_var('Remove_Top_Shelf')
        Top_Overlay = self.get_prompt("Top Overlay").get_var('Top_Overlay')

        Full_Overlay = self.get_prompt("Full Overlay").get_var('Full_Overlay')
        Default_Middle_KD_Depth = self.get_prompt("Default Middle KD Depth").get_var('Default_Middle_KD_Depth')
        Max_Height_For_Centered_Pulls = self.get_prompt("Max Height For Centered Pulls").get_var('Max_Height_For_Centered_Pulls')
        Large_Drawer_Pull_Height = self.get_prompt("Large Drawer Pull Height").get_var('Large_Drawer_Pull_Height')
        Standard_Drawer_Rear_Gap = self.get_prompt("Standard Drawer Rear Gap").get_var('Standard_Drawer_Rear_Gap')
        Deep_Drawer_Rear_Gap = self.get_prompt("Deep Drawer Rear Gap").get_var('Deep_Drawer_Rear_Gap')
        EDDB = self.get_prompt("Extra Deep Drawer Box").get_var('EDDB')
        SDF = self.get_prompt("Small Drawer Face").get_var("SDF")
        #LDF = self.get_prompt("Large Drawer Face", "LDF")
        FHBD = self.get_prompt("Four Hole Box Difference").get_var("FHBD")
        THBD = self.get_prompt("Three Hole Box Difference").get_var("THBD")
        SDFOD = self.get_prompt("Single Door Full Overlay Difference").get_var("SDFOD")
        AHOBD = self.get_prompt("Above Hamper Or Base Doors").get_var('AHOBD')
        DBH = self.get_prompt("Double Box Height").get_var("DBH")
        LDBH = self.get_prompt("Locked Double Box Height").get_var("LDBH")
        Six_Hole = self.get_prompt("Six Hole").get_var('Six_Hole')
        Seven_Hole = self.get_prompt("Seven Hole").get_var('Seven_Hole')

        prev_drawer_empty = None

        for i in range(1, self.number_of_drawers):
            DF_Height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(i) + " Height").get_var("DF_Height")
            Lock_Drawer = self.get_prompt("Lock " + str(i) + " Drawer").get_var("Lock_Drawer")
            FR_Type = self.get_prompt("File Rail Type " + str(i)).get_var("FR_Type")
            FR_Direction = self.get_prompt("File Rail Direction " + str(i)).get_var("FR_Direction")
            Use_FR = self.get_prompt("Use File Rail " + str(i)).get_var("Use_FR")
            UDD = self.get_prompt("Use Double Drawer " + str(i)).get_var('UDD')

            front_empty = self.add_empty("Drawer Front Height")
            if prev_drawer_empty:
                prev_drawer_z_loc = prev_drawer_empty.snap.get_var('location.z','prev_drawer_z_loc')
                front_empty.snap.loc_z('prev_drawer_z_loc-DF_Height-Horizontal_Gap',[prev_drawer_z_loc,DF_Height,Horizontal_Gap])
            else:
                front_empty.snap.loc_z('Drawer_Stack_Height-DF_Height+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                                  [Drawer_Stack_Height,DF_Height,Lift_Drawers_From_Bottom,Bottom_Drawer_Space,Top_Overlay])               

            df_z_loc = front_empty.snap.get_var('location.z','df_z_loc')

            front = common_parts.add_drawer_front(self)
            front.loc_x('IF(Full_Overlay,dim_x+(Right_Overlay*2),dim_x+Right_Overlay)',[dim_x,Right_Overlay,Full_Overlay])
            front.loc_y('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            front.loc_z('df_z_loc',[df_z_loc])
            front.rot_x(value=math.radians(90))
            front.rot_y(value=math.radians(-90))
            front.dim_x('DF_Height',[DF_Height])
            front.dim_y('IF(Full_Overlay,(dim_x+(Shelf_Thickness*2)-SDFOD),dim_x+Left_Overlay+Right_Overlay)',[dim_x,Left_Overlay,Right_Overlay,Full_Overlay,Shelf_Thickness,SDFOD])
            front.dim_z('Front_Thickness',[Front_Thickness])
            front.get_prompt('No Pulls').set_formula('No_Pulls',[No_Pulls])
            front.get_prompt('Use Double Pulls').set_formula('Use_Double_Pulls',[Use_Double_Pulls])
            front.get_prompt('Center Pulls on Drawers').set_formula('Center_Pulls_on_Drawers',[Center_Pulls_on_Drawers])
            front.get_prompt('Drawer Pull From Top').set_formula('Drawer_Pull_From_Top',[Drawer_Pull_From_Top])
            front.add_prompt("Left Overlay", 'DISTANCE', 0)
            front.add_prompt("Right Overlay", 'DISTANCE', 0)
            front.get_prompt('Left Overlay').set_formula('Left_Overlay',[Left_Overlay])
            front.get_prompt('Right Overlay').set_formula('Right_Overlay',[Right_Overlay])

            l_pull = common_parts.add_drawer_pull(self)
            l_pull.set_name("Drawer Pull")
            l_pull.loc_x('-Left_Overlay',[Left_Overlay])
            l_pull.loc_y('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            l_pull.loc_z('df_z_loc',[df_z_loc])
            l_pull.rot_x(value=math.radians(90))
            l_pull.dim_x('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            l_pull.dim_y('DF_Height',[DF_Height])
            l_pull.dim_z('Front_Thickness',[Front_Thickness])
            l_pull.get_prompt("Pull X Location").set_formula('IF(DF_Height<Max_Height_For_Centered_Pulls,DF_Height/2,Large_Drawer_Pull_Height)',[Max_Height_For_Centered_Pulls,DF_Height,Large_Drawer_Pull_Height])
            l_pull.get_prompt("Pull Z Location").set_formula('IF(Use_Double_Pulls,(dim_x/4),(dim_x/2))+Right_Overlay',[Use_Double_Pulls,dim_x,Right_Overlay])
            l_pull.get_prompt('Hide').set_formula('IF(No_Pulls,True,False) or Hide',[No_Pulls,self.hide_var])

            r_pull = common_parts.add_drawer_pull(self)
            r_pull.set_name("Drawer Pull")
            r_pull.loc_x('-Left_Overlay',[Left_Overlay])
            r_pull.loc_y('-Door_to_Cabinet_Gap-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Front_Thickness])
            r_pull.loc_z('df_z_loc',[df_z_loc])
            r_pull.rot_x(value=math.radians(90))
            r_pull.dim_x('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            r_pull.dim_y('DF_Height',[DF_Height])
            r_pull.dim_z('Front_Thickness',[Front_Thickness])
            r_pull.get_prompt("Pull X Location").set_formula('IF(DF_Height<Max_Height_For_Centered_Pulls,DF_Height/2,Large_Drawer_Pull_Height)',[Large_Drawer_Pull_Height,Max_Height_For_Centered_Pulls,Center_Pulls_on_Drawers,DF_Height,Drawer_Pull_From_Top])
            r_pull.get_prompt("Pull Z Location").set_formula('dim_x-(dim_x/4)+Right_Overlay',[dim_x,Right_Overlay])
            r_pull.get_prompt('Hide').set_formula('IF(No_Pulls,True,IF(Use_Double_Pulls,False,True)) or Hide',[No_Pulls,Use_Double_Pulls,self.hide_var])
            
            drawer = common_parts.add_drawer(self)
            drawer.set_name("Drawer Box")
            drawer.loc_x('Drawer_Box_Slide_Gap', [Drawer_Box_Slide_Gap])
            drawer.loc_y('-Door_to_Cabinet_Gap-(dim_y*Open)', [Door_to_Cabinet_Gap, dim_y, Open, Front_Thickness])
            drawer.loc_z('df_z_loc+DBBG', [df_z_loc, Drawer_Box_Bottom_Gap])
            drawer.dim_x('dim_x-(Drawer_Box_Slide_Gap*2)', [dim_x, Drawer_Box_Slide_Gap])
            drawer.dim_y(
                'IF(Use_FR,IF(FR_Direction == 1,IF(FR_Type == 0,INCH(14),INCH(17)),IF(dim_y <= EDDB, dim_y-Standard_Drawer_Rear_Gap, dim_y-Deep_Drawer_Rear_Gap)),'
                'IF(dim_y <= EDDB, dim_y-Standard_Drawer_Rear_Gap, dim_y-Deep_Drawer_Rear_Gap))',
                [dim_y, EDDB, Standard_Drawer_Rear_Gap, Deep_Drawer_Rear_Gap, Use_FR, FR_Direction, FR_Type])
            drawer.dim_z(
                ("IF(DF_Height<SDF,DF_Height-THBD,IF(OR(Lock_Drawer==2,Lock_Drawer==3),IF(UDD,LDBH,DF_Height-DBTG-DBBG),"
                 "IF(DF_Height==SDF,DF_Height-FHBD,IF(UDD,DBH,IF(DF_Height<INCH(4.89),DF_Height-DBTG-DBBG-INCH(0.68),DF_Height-DBTG-DBBG)))))"),
                [DF_Height, SDF, Drawer_Box_Top_Gap, Drawer_Box_Bottom_Gap, FHBD, THBD, Lock_Drawer, LDBH, DBH, UDD])
            drawer.get_prompt('Use File Rail').set_formula('Use_FR',[Use_FR])
            drawer.get_prompt('File Rail Type').set_formula('FR_Type',[FR_Type])
            drawer.get_prompt('File Rail Direction').set_formula('FR_Direction',[FR_Direction])

            double_drawer = common_parts.add_drawer(self)
            double_drawer.set_name("Drawer Box")
            double_drawer.loc_x('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
            double_drawer.loc_y('-Door_to_Cabinet_Gap-(dim_y*(Open/2))', [Door_to_Cabinet_Gap, dim_y, Open, Front_Thickness])
            double_drawer.loc_z('df_z_loc+DBBG+Shelf_Thickness+IF(OR(Lock_Drawer==2,Lock_Drawer==3),LDBH,DBH)',
                                [df_z_loc, Drawer_Box_Bottom_Gap, Lock_Drawer, DBH, LDBH, Shelf_Thickness])
            double_drawer.dim_x('dim_x-(Drawer_Box_Slide_Gap*2)', [dim_x, Drawer_Box_Slide_Gap])
            double_drawer.dim_y('IF(dim_y <= EDDB, dim_y-Standard_Drawer_Rear_Gap, dim_y-Deep_Drawer_Rear_Gap)',
                                [dim_y, EDDB, Standard_Drawer_Rear_Gap, Deep_Drawer_Rear_Gap])
            double_drawer.dim_z("DBH",[DBH])
            double_drawer.get_prompt('Hide').set_formula("IF(AND(DF_Height >= Six_Hole,DF_Height <= Seven_Hole,dim_y >= "+ str(sn_unit.inch(15.99)) +"),IF(UDD,False,True),True) or Hide",[UDD,DF_Height,Six_Hole,Seven_Hole,dim_y, self.hide_var])
            double_drawer.get_prompt('Use File Rail').set_formula('Use_FR',[Use_FR])
            double_drawer.get_prompt('File Rail Type').set_formula('FR_Type',[FR_Type])
            double_drawer.get_prompt('File Rail Direction').set_formula('FR_Direction',[FR_Direction])
            
            prev_drawer_empty = front_empty
            
            drawer_z_loc = drawer.obj_z.snap.get_var('location.z','drawer_z_loc')
            drawer_z_dim = drawer.obj_z.snap.get_var('location.z','drawer_z_dim')
             
            drawer_lock = common_parts.add_lock(self)
            drawer_lock.loc_x('IF(Lock_Drawer==2,-Division_Thickness,IF(Lock_Drawer==3,dim_x+Division_Thickness,dim_x/2))',[Lock_Drawer,dim_x,Division_Thickness])
            drawer_lock.loc_y('IF(Lock_Drawer==1,-Front_Thickness-Door_to_Cabinet_Gap-(dim_y*Open),+INCH(.75))',[Lock_Drawer,Front_Thickness,Door_to_Cabinet_Gap,Open,dim_y])
            drawer_lock.loc_z(
                'df_z_loc+IF(UDD,DF_Height-DBTG-DBBG,DF_Height)-INCH(.5)',
                [df_z_loc,UDD,DF_Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])    
            drawer_lock.rot_z('IF(Lock_Drawer==2,radians(-90),IF(Lock_Drawer==3,radians(90),0))',[Lock_Drawer])
            drawer_lock.get_prompt('Hide').set_formula('IF(Lock_Drawer>0,False,True)',[Lock_Drawer])

            KD_Shelf = common_parts.add_shelf(self)
            KD_Shelf.loc_x(value = 0)
            KD_Shelf.loc_y('Default_Middle_KD_Depth', [Default_Middle_KD_Depth])
            KD_Shelf.loc_z('df_z_loc+DF_Height-Top_Overlay',[df_z_loc,DF_Height,Top_Overlay])
            KD_Shelf.rot_x(value=math.radians(180))
            KD_Shelf.dim_x('dim_x',[dim_x])
            KD_Shelf.dim_y('Default_Middle_KD_Depth', [Default_Middle_KD_Depth])
            KD_Shelf.dim_z('-Shelf_Thickness',[Shelf_Thickness])
            KD_Shelf.get_prompt('Is Locked Shelf').set_value(value=True)
            KD_Shelf.get_prompt('Hide').set_value(value=True)
            KD_Shelf.dim_y('IF(Lock_Drawer>0, dim_y, Default_Middle_KD_Depth) or Hide',  [self.hide_var, Lock_Drawer, dim_y, Default_Middle_KD_Depth])
            KD_Shelf.loc_y('IF(Lock_Drawer>0, dim_y, Default_Middle_KD_Depth)', [Lock_Drawer, dim_y, Default_Middle_KD_Depth])

            if(i==1):
                KD_Shelf.dim_y('dim_y', [dim_y])
                KD_Shelf.loc_y('dim_y', [dim_y])
                KD_Shelf.get_prompt('Hide').set_formula('IF(Remove_Top_Shelf,True,IF(Lock_Drawer>0,False,True))',[Remove_Top_Shelf,Lock_Drawer])
            if(i==2):
                KD_Shelf.get_prompt('Hide').set_formula('IF(AHOBD,True,IF( Drawer_Quantity-1 == 2,False,IF( Drawer_Quantity-1 == 3,False,IF(Lock_Drawer>0,False,True)))) or Hide',  [self.hide_var, Drawer_Quantity, Lock_Drawer,AHOBD])
                
            if(i==3):
                KD_Shelf.get_prompt('Hide').set_formula('IF(Drawer_Quantity-1 == 4,False,IF(Drawer_Quantity-1 == 5,False,IF(Drawer_Quantity-1 == 7,False,IF(Lock_Drawer>0,False,True)))) or Hide',  [self.hide_var, Drawer_Quantity, Lock_Drawer])
                
            if(i==4):
                KD_Shelf.get_prompt('Hide').set_formula('IF(Drawer_Quantity-1 == 6,False,IF(Drawer_Quantity-1 == 8,False,IF(Lock_Drawer>0,False,True))) or Hide',  [self.hide_var, Drawer_Quantity, Lock_Drawer])
                
            if(i==5):
                KD_Shelf.get_prompt('Hide').set_formula('IF(Drawer_Quantity-1 == 7,False,IF(Lock_Drawer>0,False,True))',[Lock_Drawer,Drawer_Quantity])
                
            if(i==6):
                KD_Shelf.get_prompt('Hide').set_formula('IF(Drawer_Quantity-1 == 8,False,IF(Lock_Drawer>0,False,True))',[Lock_Drawer,Drawer_Quantity])
                
            if(i==7):
                KD_Shelf.get_prompt('Hide').set_formula('IF(Lock_Drawer>0,False,True)',[Lock_Drawer])
                
            if(i==8):
                KD_Shelf.get_prompt('Hide').set_formula('IF(Lock_Drawer>0,False,True)',[Lock_Drawer])

    def update(self):
        super().update()

        self.obj_bp["IS_BP_DRAWER_STACK"] = True        
        self.obj_bp.snap.export_as_subassembly = True
        
        props = self.obj_bp.sn_closets
        props.is_drawer_stack_bp = True # TODO: remove

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.add_prompts()

        drawer_front_prompts = []
        height_formula = ""

        self.drawer_front_ppt_obj = self.add_empty("OBJ_PROMPTS_Drawer_Fronts")
        self.drawer_front_ppt_obj.empty_display_size = .01

        for i in range(1,self.number_of_drawers):
            self.add_drawer_box_prompts(i)
            self.drawer_front_ppt_obj.snap.add_prompt('DISTANCE', "Drawer " + str(i) + " Height")
            df_prompt = self.drawer_front_ppt_obj.snap.get_prompt("Drawer {} Height".format(str(i)))
            df_prompt.set_value(sn_unit.millimeter(187.96))
            df = df_prompt.get_var('df{}'.format(str(i)))
            drawer_front_prompts.append(df)
            height_formula += "df{}+".format(str(i))

        height_formula += "(hg*(dq-1))-Bottom_Overlay-Top_Overlay+MILLIMETER(3.3919922)"

        Top_Overlay = self.get_prompt("Top Overlay").get_var('Top_Overlay')
        Bottom_Overlay = self.get_prompt("Bottom Overlay").get_var('Bottom_Overlay')
        drawer_front_prompts.append(Top_Overlay)
        drawer_front_prompts.append(Bottom_Overlay)
        dq = self.get_prompt("Drawer Quantity").get_var('dq')
        drawer_front_prompts.append(dq)
        hg = self.overlay_ppt_obj.snap.get_prompt("Horizontal Gap").get_var('hg')
        drawer_front_prompts.append(hg)

        self.stack_height_ppt_obj = self.add_empty("OBJ_PROMPTS_Drawer_Stack_Height")
        self.stack_height_ppt_obj.empty_display_size = .01        
        stack_height_prompt = self.stack_height_ppt_obj.snap.add_prompt('DISTANCE', "Drawer Stack Height")

        stack_height_prompt.set_formula(
            height_formula, # ? Change height to allow correct door heights
            drawer_front_prompts)

        dim_x = self.obj_x.snap.get_var("location.x", "dim_x")
        dim_y = self.obj_y.snap.get_var("location.y", "dim_y")
        dim_z = self.obj_z.snap.get_var("location.z", "dim_z")
        
        Drawer_Stack_Height = self.stack_height_ppt_obj.snap.get_prompt("Drawer Stack Height").get_var('Drawer_Stack_Height')
        Shelf_Thickness = self.get_prompt("Shelf Thickness").get_var('Shelf_Thickness')
        Lift_Drawers_From_Bottom = self.get_prompt("Lift Drawers From Bottom").get_var('Lift_Drawers_From_Bottom')
        Bottom_Drawer_Space = self.get_prompt("Bottom Drawer Space").get_var('Bottom_Drawer_Space')
        Remove_Top_Shelf = self.get_prompt("Remove Top Shelf").get_var('Remove_Top_Shelf')
        Remove_Bottom_Shelf = self.get_prompt("Remove Bottom Shelf").get_var('Remove_Bottom_Shelf')
        Cleat_Location = self.get_prompt("Cleat Location").get_var('Cleat_Location')
        Cleat_Height = self.get_prompt("Cleat Height").get_var('Cleat_Height')

        backing_gap_prompt = self.add_prompt("Drawer Stack Backing Gap", 'DISTANCE', 0, prompt_obj=self.add_prompt_obj("Backing_Gap"))
        backing_gap_prompt.set_formula(
            'Drawer_Stack_Height+Shelf_Thickness*2-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
            [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space,Cleat_Location])  
        
        self.add_drawers()
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Bottom Cleat")
        cleat.loc_y('dim_y',[dim_y])
        cleat.loc_z('Drawer_Stack_Height+IF(Cleat_Location==0,Shelf_Thickness,0)-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space,Cleat_Location])
        cleat.rot_x(value=math.radians(-90))
        cleat.dim_x('dim_x',[dim_x])
        cleat.dim_y('IF(Cleat_Location==0,-Cleat_Height,Cleat_Height)', [Cleat_Height, Cleat_Location])
        cleat.dim_z('-Shelf_Thickness',[Shelf_Thickness])
        cleat.get_prompt("Hide").set_formula("IF(Cleat_Location==2,True,False) or Hide", [Cleat_Location,self.hide_var])
        cleat.get_prompt('Use Cleat Cover').set_formula('IF(Cleat_Location==0,True,False)', [Cleat_Location])     
        
        top_shelf = common_parts.add_shelf(self)
        top_shelf.loc_y('dim_y', [dim_y])
        top_shelf.loc_z('Drawer_Stack_Height-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        top_shelf.rot_x(value=math.radians(180))
        top_shelf.dim_x('dim_x',[dim_x])
        top_shelf.dim_y('dim_y',[dim_y])
        top_shelf.dim_z('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.get_prompt('Hide').set_formula('IF(Remove_Top_Shelf,False,True) or Hide',[Remove_Top_Shelf,self.hide_var])
        top_shelf.get_prompt('Is Locked Shelf').set_value(value=True)
        
        top_shelf_z_loc = top_shelf.obj_bp.snap.get_var('location.z','top_shelf_z_loc')
        
        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.loc_y('dim_y', [dim_y])
        bottom_shelf.loc_z('IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)-Shelf_Thickness',
                        [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        bottom_shelf.rot_x(value=math.radians(180))
        bottom_shelf.dim_x('dim_x',[dim_x])
        bottom_shelf.dim_y('dim_y',[dim_y])
        bottom_shelf.dim_z('-Shelf_Thickness',[Shelf_Thickness])
        bottom_shelf.get_prompt('Hide').set_formula('IF(Remove_Bottom_Shelf,False,True) or Hide',[Remove_Bottom_Shelf,self.hide_var])
        bottom_shelf.get_prompt('Is Locked Shelf').set_value(value=True)
        
        opening = common_parts.add_opening(self)
        opening.loc_z('top_shelf_z_loc+Shelf_Thickness',[top_shelf_z_loc,Shelf_Thickness])
        opening.dim_x('dim_x',[dim_x])
        opening.dim_y('dim_y',[dim_y])
        opening.dim_z('dim_z-top_shelf_z_loc-Shelf_Thickness',[dim_z,top_shelf_z_loc,Shelf_Thickness])
        
        if self.upper_exterior:
            opening.obj_bp.snap.exterior_open = False
            
            self.upper_exterior.draw()
            self.upper_exterior.obj_bp.parent = self.obj_bp
            self.upper_exterior.loc_z('top_shelf_z_loc',[top_shelf_z_loc])
            self.upper_exterior.dim_x('dim_x',[dim_x])
            self.upper_exterior.dim_y('dim_y',[dim_y])
            self.upper_exterior.dim_z('dim_z-top_shelf_z_loc',[dim_z,top_shelf_z_loc])
        
        if self.upper_interior:
            opening.obj_bp.snap.interior_open = False
            
            self.upper_interior.draw()
            self.upper_interior.obj_bp.parent = self.obj_bp
            self.upper_interior.loc_z('top_shelf_z_loc',[top_shelf_z_loc])
            self.upper_interior.dim_x('dim_x',[dim_x])
            self.upper_interior.dim_y('dim_y',[dim_y])
            self.upper_interior.dim_z('dim_z-top_shelf_z_loc',[dim_z,top_shelf_z_loc])          
        
        self.update()
           
class PROMPTS_Drawer_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.drawer_prompts"
    bl_label = "Drawer Prompt" 
    bl_description = "This shows all of the available drawer options"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name")
    
    assembly = None
    part = None
    
    drawer_quantity: EnumProperty(name="Drawer Quantity",
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
    
    drawer_1_height: EnumProperty(name="Drawer 1 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_2_height: EnumProperty(name="Drawer 2 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_3_height: EnumProperty(name="Drawer 3 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_4_height: EnumProperty(name="Drawer 4 Height",
                                   items=common_lists.FRONT_HEIGHTS)

    drawer_5_height: EnumProperty(name="Drawer 5 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_6_height: EnumProperty(name="Drawer 6 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_7_height: EnumProperty(name="Drawer 7 Height",
                                   items=common_lists.FRONT_HEIGHTS)

    drawer_8_height: EnumProperty(name="Drawer 8 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    lock_1_drawer: EnumProperty(name="Lock 1 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0')    
    
    lock_2_drawer: EnumProperty(name="Lock 2 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0')    
    
    lock_3_drawer: EnumProperty(name="Lock 3 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0')    
    
    lock_4_drawer: EnumProperty(name="Lock 4 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0')    
    
    lock_5_drawer: EnumProperty(name="Lock 5 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0')    
    
    lock_6_drawer: EnumProperty(name="Lock 6 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0')

    lock_7_drawer: EnumProperty(name="Lock 7 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0') 

    lock_8_drawer: EnumProperty(name="Lock 8 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default='0')

    file_rail_type_1: EnumProperty(name="File Rail Type 1",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_1: EnumProperty(name="File Rail Direction 1",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')
    file_rail_type_2: EnumProperty(name="File Rail Type 2",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_2: EnumProperty(name="File Rail Direction 2",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')                         
    file_rail_type_3: EnumProperty(name="File Rail Type 3",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_3: EnumProperty(name="File Rail Direction 3",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')                         
    file_rail_type_4: EnumProperty(name="File Rail Type 4",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_4: EnumProperty(name="File Rail Direction 4",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')                         
    file_rail_type_5: EnumProperty(name="File Rail Type 5",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_5: EnumProperty(name="File Rail Direction 5",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')                         
    file_rail_type_6: EnumProperty(name="File Rail Type 6",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_6: EnumProperty(name="File Rail Direction 6",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')                         
    file_rail_type_7: EnumProperty(name="File Rail Type 7",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_7: EnumProperty(name="File Rail Direction 7",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')                         
    file_rail_type_8: EnumProperty(name="File Rail Type 8",
                                              items=FILE_RAIL_TYPES,
                                              default='0')
    file_rail_direction_8: EnumProperty(name="File Rail Direction 8",
                                                   items=FILE_DIRECTION_TYPES,
                                                   default='0')                         

    bottom_offset: EnumProperty(name="Bottom Offset",
                                   items=common_lists.DRAWER_BOTTOM_OFFSETS,
                                   default='160')

    cleat_location: EnumProperty(
        name="Cleat Location",
        items=[
            ('0', 'Above', 'Above'),
            ('1', 'Below', 'Below'),
            ('2', 'None', 'None')],
        default='0')

    front_heights = []
    
    drawer_qty_prompt = None
    drawer_front_ppt_obj = None
    cleat_loc_prompt = None

    cleat_location: EnumProperty(
        name="Cleat Location",
        items=[
            ('0', 'Above', 'Above'),
            ('1', 'Below', 'Below'),
            ('2', 'None', 'None')],
        default='0')
    
    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
        # sn_utils.run_calculators(sn_utils.get_parent_assembly_bp(self.assembly.obj_bp))
        # sn_utils.run_calculators(sn_utils.get_parent_assembly_bp(self.assembly.obj_bp))
        return {'FINISHED'}
        
    def check(self, context):
        if self.cleat_loc_prompt:
            self.cleat_loc_prompt.set_value(int(self.cleat_location))     

        if self.drawer_qty_prompt:
            props = bpy.context.scene.sn_closets
            
            self.drawer_qty_prompt.quantity_value = int(self.drawer_quantity)
            small_drawer_face = self.assembly.get_prompt("Small Drawer Face")
            large_drawer_face = self.assembly.get_prompt("Large Drawer Face")
            six_hole = self.assembly.get_prompt("Six Hole")
            seven_hole = self.assembly.get_prompt("Seven Hole")

            if self.cleat_loc_prompt:
                self.cleat_loc_prompt.set_value(int(self.cleat_location))
                
            for i in range(1,self.drawer_qty_prompt.get_value()):
                drawer_height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer")
                slide_type = self.assembly.get_prompt("Drawer " + str(i) + " Slide Type") #DONT REMOVE USED in exec
                use_file_rail = self.assembly.get_prompt("Use File Rail " + str(i))
                file_rail_type = self.assembly.get_prompt("File Rail Type " + str(i))
                file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(i))
                use_double_drawer = self.assembly.get_prompt("Use Double Drawer " + str(i))
                bottom_offset = self.assembly.get_prompt("Bottom Drawer Space")
                extra_deep_drawer_box = self.assembly.get_prompt("Extra Deep Drawer Box")
                if self.assembly.obj_y.location.y<=extra_deep_drawer_box.get_value():
                    drawer_box_rear_gap = self.assembly.get_prompt("Standard Drawer Rear Gap")
                else:
                    drawer_box_rear_gap = self.assembly.get_prompt("Deep Drawer Rear Gap")                
                width = self.assembly.obj_x.location.x - sn_unit.inch(2)
                depth = self.assembly.obj_y.location.y - drawer_box_rear_gap.get_value()
                letter = sn_unit.inch(12.5)
                legal = sn_unit.inch(15.5)

                if props.closet_defaults.use_32mm_system: 
                    if drawer_height:
                        exec("drawer_height.set_value(sn_unit.inch(float(self.drawer_" + str(i) + "_height) / 25.4))")
                    if bottom_offset:
                        bottom_offset.set_value(sn_unit.inch(float(self.bottom_offset)/25.4))
                
                if lock_drawer:
                    exec("lock_drawer.set_value(int(self.lock_" + str(i) + "_drawer))")
                if slide_type:
                    exec("slide_type.set_value(self.drawer_" + str(i) + "_slide)")
                if file_rail_type:
                    exec("file_rail_type.set_value(int(self.file_rail_type_" + str(i) + "))")

                    if drawer_height.get_value() <= small_drawer_face.get_value():
                        lock_drawer.set_value(0)

                    if(drawer_height.get_value() >= large_drawer_face.get_value() and (width >= letter or depth >= letter)):
                        if(use_file_rail.get_value()):
                            if(width < letter):
                                if(depth < legal):
                                    exec("self.file_rail_type_" + str(i) + "= str(0)")
                                    file_rail_type.set_value(0)
                                    exec("self.file_rail_direction_" + str(i) + "= str(1)")
                                    file_rail_direction.set_value(1)
                                else:
                                    exec("file_rail_direction_" + str(i) + "= str(1)")
                                    file_rail_direction.set_value(1)

                            elif(width < legal):
                                if(depth < letter):
                                    exec("self.file_rail_type_" + str(i) + "= str(0)")
                                    file_rail_type.set_value(0)
                                    exec("self.file_rail_direction_" + str(i) + "= str(0)")
                                    file_rail_direction.set_value(0)

                                elif(depth < legal):
                                    exec("self.file_rail_type_" + str(i) + "= str(0)")
                                    file_rail_type.set_value(0)
                                else:
                                    if(file_rail_direction.get_value() == 0):
                                        exec("self.file_rail_type_" + str(i) + "= str(0)")
                                        file_rail_type.set_value(0)
                            else:
                                if(depth < letter):
                                    exec("self.file_rail_direction_" + str(i) + "= str(0)")
                                    file_rail_direction.set_value(0)
                                elif(depth < legal):
                                    if(file_rail_direction.get_value() == 1):
                                        exec("self.file_rail_type_" + str(i) + "= str(0)")
                                        file_rail_type.set_value(0)
                    else:
                        use_file_rail.set_value(False)

                if file_rail_direction:
                    exec("file_rail_direction.set_value(int(self.file_rail_direction_" + str(i) + "))")
                if(drawer_height.get_value() < small_drawer_face.get_value()):
                    lock_drawer.set_value(0)
                if(drawer_height.get_value() < six_hole.get_value() or drawer_height.get_value() > seven_hole.get_value() or self.assembly.obj_y.location.y < sn_unit.inch(15.99)):
                    use_double_drawer.set_value(False)                    

            pard_has_bottom_KD = self.assembly.get_prompt("Pard Has Bottom KD")
            remove_bottom_shelf = self.assembly.get_prompt("Remove Bottom Shelf")
            lift_drawers_from_bottom = self.assembly.get_prompt("Lift Drawers From Bottom")
            parent_assembly = sn_types.Assembly(self.assembly.obj_bp.parent)
            RBS = parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + self.assembly.obj_bp.sn_closets.opening_name)
            if(lift_drawers_from_bottom.get_value()):
                pard_has_bottom_KD.set_value(False)
            elif(RBS):
                if(RBS.get_value()):
                    pard_has_bottom_KD.set_value(True)
            if(pard_has_bottom_KD.get_value()):
                remove_bottom_shelf.set_value(False)

        self.assign_mirror_material(self.assembly.obj_bp)

        #sn_utils.run_calculators(self.assembly.obj_bp)

        bpy.ops.snap.update_scene_from_pointers()
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport

        # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
        # sn_utils.run_calculators(sn_utils.get_parent_assembly_bp(self.assembly.obj_bp))
        # sn_utils.run_calculators(sn_utils.get_parent_assembly_bp(self.assembly.obj_bp))
        closet_props.update_render_materials(self, context)
        return True

    def get_front_heights(self):
        self.front_heights = []
        for front in common_lists.FRONT_HEIGHTS:
            self.front_heights.append(front[0])

    def set_properties_from_prompts(self):
        props = bpy.context.scene.sn_closets
        bottom_offset = self.assembly.get_prompt("Bottom Drawer Space").get_value()
        self.cleat_loc_prompt = self.assembly.get_prompt('Cleat Location')

        if bottom_offset:
            self.bottom_offset = str(round(sn_unit.meter_to_millimeter(bottom_offset)))
        
        self.get_front_heights()
        
        self.drawer_qty_prompt = self.assembly.get_prompt("Drawer Quantity")
        if self.drawer_qty_prompt:
            self.drawer_quantity = str(self.drawer_qty_prompt.quantity_value)

        self.cleat_loc_prompt = self.assembly.get_prompt('Cleat Location')
        if self.cleat_loc_prompt:
            self.cleat_location = str(self.cleat_loc_prompt.combobox_index)
                    
            for i in range(1,self.drawer_qty_prompt.get_value()):
                drawer_height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer") #DONT REMOVE USED in exec
                file_rail_type = self.assembly.get_prompt("File Rail Type " + str(i)) #DONT REMOVE USED in exec
                file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(i)) #DONT REMOVE USED in exec

                if lock_drawer and file_rail_type and file_rail_direction:
                    exec("self.lock_" + str(i) + "_drawer = LOCK_DRAWER_TYPES[lock_drawer.get_value()][0]")
                    exec("self.file_rail_type_" + str(i) + " = FILE_RAIL_TYPES[file_rail_type.get_value()][0]")
                    exec("self.file_rail_direction_" + str(i) + " = FILE_DIRECTION_TYPES[file_rail_direction.get_value()][0]")

                if props.closet_defaults.use_32mm_system: 
                    if drawer_height:
                        value = str(round(drawer_height.distance_value * 1000,4))
                        if value in self.front_heights:
                            exec("self.drawer_" + str(i) + "_height = value")

        if self.cleat_loc_prompt:
            self.cleat_location = str(self.cleat_loc_prompt.combobox_index)

    def assign_mirror_material(self,obj):
        use_mirror = self.assembly.get_prompt("Use Mirror")
        if use_mirror.get_value():
            if obj.snap.type_mesh == 'BUYOUT':
                for mat_slot in obj.snap.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Mirror'  
        else:
            if obj.snap.type_mesh == 'BUYOUT':
                for mat_slot in obj.snap.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Glass'  

        for child in obj.children:
            self.assign_mirror_material(child)

    def invoke(self,context,event):
        obj = bpy.data.objects[context.object.name]
        self.assembly = self.get_insert()

        # Get drawer front prompts obj
        for child in self.assembly.obj_bp.children:
            if "OBJ_PROMPTS_Drawer_Fronts" in child.name:
                self.drawer_front_ppt_obj = child

        obj_assembly_bp = sn_utils.get_assembly_bp(obj)
        self.part = sn_types.Assembly(obj_assembly_bp)

        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=450)
    
    def draw_drawer_heights(self,layout):
        col = layout.column(align=True)
        props = bpy.context.scene.sn_closets
              
        drawer_quantity = self.assembly.get_prompt("Drawer Quantity")
        small_drawer_face = self.assembly.get_prompt("Small Drawer Face")
        large_drawer_face = self.assembly.get_prompt("Large Drawer Face")
        six_hole = self.assembly.get_prompt("Six Hole")
        seven_hole = self.assembly.get_prompt("Seven Hole")
        
        if drawer_quantity:
            for i in range(1,drawer_quantity.get_value()):
                
                drawer_height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer")

                file_rail_type = self.assembly.get_prompt("File Rail Type " + str(i))
                file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(i))
                use_file_rail = self.assembly.get_prompt("Use File Rail " + str(i))
                use_double_drawer = self.assembly.get_prompt("Use Double Drawer " + str(i))
                extra_deep_drawer_box = self.assembly.get_prompt("Extra Deep Drawer Box")
                if(drawer_height and lock_drawer and file_rail_type and file_rail_direction and use_file_rail and extra_deep_drawer_box):
                    if(self.assembly.obj_y.location.y<=extra_deep_drawer_box.get_value()):
                        drawer_box_rear_gap = self.assembly.get_prompt("Standard Drawer Rear Gap")
                    else:
                        drawer_box_rear_gap = self.assembly.get_prompt("Deep Drawer Rear Gap")

                    width = self.assembly.obj_x.location.x - sn_unit.inch(2)
                    depth = self.assembly.obj_y.location.y - drawer_box_rear_gap.get_value()
                    letter = sn_unit.inch(12.5)
                    legal = sn_unit.inch(15.5)

                    if drawer_height and drawer_quantity.get_value() >= i:
                        box = col.box()
                        row = box.row()

                        col_1 = row.column()
                        if props.closet_defaults.use_32mm_system:  
                            col_1.label(text="Drawer " + str(i) + " Height:")
                            col_1.prop(self,'drawer_' + str(i) + '_height',text="")
                        else:
                            col_1.prop(drawer_height, "distance_value", text=drawer_height.name)
                        
                        if(drawer_height.get_value() >= small_drawer_face.get_value()):
                            col_2 = row.column()
                            col_2.label(text="Lock:")
                            col_2.prop(self,'lock_' + str(i) + '_drawer',text="")

                        if(drawer_height and six_hole and seven_hole):
                            if(drawer_height.get_value() >= six_hole.get_value() and drawer_height.get_value() <= seven_hole.get_value() and self.assembly.obj_y.location.y >= sn_unit.inch(15.99)):
                                col_3 = row.column(align=True)
                                col_3.label(text="Double Jewelry Drawer")
                                col_3.prop(use_double_drawer,"checkbox_value",text="")

                        if(drawer_height.get_value() >= large_drawer_face.get_value() and (width >= letter or depth >= letter)):
                            col_3 = row.column(align=True)
                            col_3.prop(use_file_rail, "checkbox_value", text="File Rail")

                            if(use_file_rail.get_value()):
                                if(width < letter):
                                    if(depth < legal):
                                        col_3.label(text="Letter")
                                        col_3.label(text="Lateral")
                                    else:
                                        col_3.prop(self, 'file_rail_type_' + str(i), text="")
                                        col_3.label(text="Lateral")

                                elif(width < legal):
                                    if(depth < letter):
                                        col_3.label(text="Letter")
                                        col_3.label(text="Front to Back")

                                    elif(depth < legal):
                                        col_3.label(text="Letter")
                                        col_3.prop(self, 'file_rail_direction_' + str(i), text="")

                                    else:
                                        if(file_rail_direction.get_value() == 0):
                                            col_3.label(text="Letter")
                                            col_3.prop(self, 'file_rail_direction_' + str(i), text="")
                                        else:
                                            col_3.prop(self, 'file_rail_type_' + str(i), text="")
                                            col_3.prop(self, 'file_rail_direction_' + str(i), text="")
                                else:
                                    if(depth < letter):
                                        col_3.prop(self, 'file_rail_type_' + str(i), text="")
                                        col_3.label(text="Front to Back")

                                    elif(depth < legal):
                                        if(file_rail_direction.get_value() == 1):
                                            col_3.label(text="Letter")
                                            col_3.prop(self, 'file_rail_direction_' + str(i), text="")
                                        else:
                                            col_3.prop(self, 'file_rail_type_' + str(i), text="")
                                            col_3.prop(self, 'file_rail_direction_' + str(i), text="")
                                    else:
                                        col_3.prop(self, 'file_rail_type_' + str(i), text="")
                                        col_3.prop(self, 'file_rail_direction_' + str(i), text="")

    def is_glass_front(self):
        if "Glass" in self.part.obj_bp.snap.comment:
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
                    use_double_pulls = self.assembly.get_prompt('Use Double Pulls')
                    remove_top_shelf = self.assembly.get_prompt('Remove Top Shelf')
                    remove_bottom_shelf = self.assembly.get_prompt('Remove Bottom Shelf')
                    lift_drawers_from_bottom = self.assembly.get_prompt('Lift Drawers From Bottom')
                    no_pulls = self.assembly.get_prompt('No Pulls')
                    use_mirror = self.assembly.get_prompt("Use Mirror")
                    cleat_loc = self.assembly.get_prompt("Cleat Location")

                    propbox = box.box()
                    propbox.label(text="Options:",icon='SCRIPT')
                    
                    row = propbox.row()
                    row.label(text="Open Drawers")
                    row.prop(open_drawer,'factor_value',text="")

                    row = propbox.row()
                    row.label(text="Drawer Rear Gap")

                    if extra_deep_drawer_box and standard_drawer_rear_gap and deep_drawer_rear_gap:
                        if(drawer_depth<=extra_deep_drawer_box.get_value()):
                            row.prop(standard_drawer_rear_gap,"distance_value",text="")
                        else:
                            row.prop(deep_drawer_rear_gap,"distance_value",text="")

                    row = propbox.row()
                    if cleat_loc:
                        row.label(text="Cleat Location")
                        row.prop(self, "cleat_location", expand=True)

                    row = propbox.row()
                    if lift_drawers_from_bottom:
                        #lift_drawers_from_bottom.draw_prompt(row,text="Suspended Drawers",split_text=False)
                        row.prop(lift_drawers_from_bottom, "checkbox_value", text="Suspended Drawers")

                    if lift_drawers_from_bottom.get_value():
                        row.prop(self,'bottom_offset')

                    row = propbox.row()
                    if use_double_pulls:
                        #use_double_pulls.draw_prompt(row,split_text=False)
                        row.prop(use_double_pulls, "checkbox_value", text=use_double_pulls.name)
                    if no_pulls:
                        #no_pulls.draw_prompt(row,split_text=False)
                        row.prop(no_pulls, "checkbox_value", text=no_pulls.name)
                    
                    row = propbox.row()
                    if remove_top_shelf:
                        row.prop(remove_top_shelf,"checkbox_value",text="Top KD")
                    if remove_bottom_shelf:
                        row.prop(remove_bottom_shelf,"checkbox_value",text="Bottom KD")
                    if full_overlay:
                        row = propbox.row()
                        row.prop(full_overlay, "checkbox_value", text="Full Overlay")            

                    if self.is_glass_front():
                        row = propbox.row()
                        #use_mirror.draw_prompt(row,split_text=False)
                        row.prop(use_mirror, "checkbox_value", text=use_mirror.name)

                    self.draw_drawer_heights(box)

class OPS_Drawer_Drop(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.insert_drawer_drop"
    bl_label = "Custom drag and drop for drawers insert"
    
    def execute(self, context):
        return super().execute(context)

    def confirm_placement(self, context):
        super().confirm_placement(context)
        self.set_backing_bottom_gap(self.insert.obj_bp, self.selected_opening)
        self.set_drawer_cleat_hide(self.insert.obj_bp, self.selected_opening)
        self.set_bottom_KD(self.insert.obj_bp, self.selected_opening)
        self.set_above_hamper_or_base_door(self.insert.obj_bp)
        context.view_layer.objects.active = self.insert.obj_bp
        # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
        sn_utils.run_calculators(self.insert.obj_bp)
        sn_utils.run_calculators(self.insert.obj_bp)
        # TOP LEVEL PRODUCT RECAL
        sn_utils.run_calculators(sn_utils.get_closet_bp(self.insert.obj_bp))
        sn_utils.run_calculators(sn_utils.get_closet_bp(self.insert.obj_bp))

        bpy.context.window.cursor_set('DEFAULT')

    def set_drawer_cleat_hide(self, insert_bp, selected_opening):
        drawer_assembly = sn_types.Assembly(insert_bp)
        carcass_bp = sn_utils.get_closet_bp(insert_bp)
        carcass_assembly = sn_types.Assembly(carcass_bp)
        opening_name = selected_opening.obj_bp.sn_closets.opening_name
        back_thickness_ppt = carcass_assembly.get_prompt("Opening " + opening_name + " Center Backing Thickness")
        if back_thickness_ppt:
            Back_Thickness = back_thickness_ppt.get_var("Back_Thickness")
        cleat_location_ppt = drawer_assembly.get_prompt("Cleat Location")
        if cleat_location_ppt:
            Cleat_Location = drawer_assembly.get_prompt("Cleat Location").get_var()

        has_counter_top = False
        for child in carcass_bp.children:
            if "IS_BP_COUNTERTOP" in child:
                has_counter_top = True

        if has_counter_top or "IS_BP_ISLAND" in carcass_bp:
            cleat_location_ppt.set_value(1)  # Setting Cleat Location to Below
            return

        Hide = drawer_assembly.get_prompt("Hide").get_var()

        for child in insert_bp.children:
            if child.sn_closets.is_cleat_bp:
                cleat_assembly = sn_types.Assembly(child)
                cleat_assembly.get_prompt('Hide').set_formula('IF(OR(Cleat_Location==2,Back_Thickness==1),True,False) or Hide', [Back_Thickness, Cleat_Location, Hide])

    def set_backing_bottom_gap(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.sn_closets.opening_name
        carcass_bp = sn_utils.get_closet_bp(insert_bp)
        drawer_assembly = sn_types.Assembly(insert_bp)        
        Drawer_Stack_Backing_Gap = drawer_assembly.get_prompt('Drawer Stack Backing Gap').get_var()

        for child in carcass_bp.children:
            if child.sn_closets.is_back_bp:
                if child.sn_closets.opening_name == opening_name:
                    back_assembly = sn_types.Assembly(child)
                    bottom_insert_gap = back_assembly.get_prompt('Bottom Insert Gap')

                    if bottom_insert_gap:
                        bottom_insert_gap.set_formula('Drawer_Stack_Backing_Gap', [Drawer_Stack_Backing_Gap])
    
    def set_above_hamper_or_base_door(self, insert_bp):
        drawer_assembly = sn_types.Assembly(insert_bp)
        above_hamper_or_base_door = drawer_assembly.get_prompt("Above Hamper Or Base Doors")
        parent_bp = sn_utils.get_parent_assembly_bp(insert_bp)

        if(above_hamper_or_base_door):
            if(parent_bp.sn_closets.is_door_bp):
                door_assembly = sn_types.Assembly(parent_bp)
                door_type = door_assembly.get_prompt("Door Type")
                if(door_type):
                    if(door_type.get_value() == 'Base'):
                        above_hamper_or_base_door.set_value(True)
            elif(parent_bp.sn_closets.is_hamper_bp):
                above_hamper_or_base_door.set_value(True)
            else:
                for child in parent_bp.children:
                    if(child.sn_closets.is_door_insert_bp):
                        door_assembly = sn_types.Assembly(child)
                        door_type = door_assembly.get_prompt("Door Type")
                        if(door_type):
                            if(door_type.get_value() == 'Base'):
                                above_hamper_or_base_door.set_value(True)
                    elif(child.sn_closets.is_hamper_insert_bp):
                        above_hamper_or_base_door.set_value(True)

    def set_bottom_KD(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.sn_closets.opening_name
        carcass_bp = sn_utils.get_closet_bp(insert_bp)
        drawer_assembly = sn_types.Assembly(insert_bp)   
        carcass_assembly = sn_types.Assembly(carcass_bp)
        ppt_floor_mounted = carcass_assembly.get_prompt("Opening " + str(opening_name) + " Floor Mounted")
        ppt_remove_bottom_shelf = carcass_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(opening_name))

        if ppt_floor_mounted and ppt_remove_bottom_shelf:
            if ppt_floor_mounted.get_value() or ppt_remove_bottom_shelf.get_value():
                drawer_assembly.get_prompt("Pard Has Bottom KD").set_value(True)

bpy.utils.register_class(PROMPTS_Drawer_Prompts)
bpy.utils.register_class(OPS_Drawer_Drop)
