import os
import math
import time

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty


from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts
from ..common import common_lists

SLIDE_TYPE = [('0', 'Sidemount', 'Sidemount'),
              ('1', 'Undermount', 'Undermount')]
SIDEMOUNT_OPTIONS = [('0', 'Hafele BB Sidemount Slides', 'Hafele BB Sidemount Slides'),
                     ('1', 'HR BB Soft Close Sidemount Slides', 'HR BB Soft Close Sidemount Slides')]
UNDERMOUNT_OPTIONS = [('0', 'Hettich 4D Undermount Slides', 'Hettich 4D Undermount Slides'),
                      ('1', 'Hettich V6 Undermount Slide', 'Hettich V6 Undermount Slide'),
                      ('2', 'Blumotion Undermount Slides', 'Blumotion Undermount Slides'),
                      ('3', 'King Slide Undermount Slides', 'King Slide Undermount Slides')]
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
    category_name = "Products - Drawers"
    mirror_y = False

    is_pull_out_tray = False
    number_of_drawers = 3 #1-9
    upper_interior = None
    upper_exterior = None
    drawer_front_ppt_obj = None
    stack_height_ppt_obj = None
    backing_gap_ppt_obj = None
    overlay_ppt_obj = None

    r_pull = None
    drawer_boxes = []
    locks = []
    dbl_drawer_boxes = []

    def __init__(self, obj_bp=None):
        super().__init__(obj_bp=obj_bp)
        self.drawer_boxes = []
        self.locks = []
        self.dbl_drawer_boxes = []

        self.get_drawer_locks()
        self.get_drawer_boxes()
        self.get_dbl_drawer_boxes()

    def get_shelves(self):
        for child in self.obj_bp.children:
            if child.get("IS_SHELF"):
                shelf = sn_types.Assembly(child)
                is_locked_shelf = shelf.get_prompt("Is Locked Shelf")
                if is_locked_shelf:
                    if not is_locked_shelf.get_value():
                        self.shelves.append(sn_types.Assembly(child))

    def get_drawer_locks(self):
        self.locks = self.get_all_locks()

    def get_drawer_boxes(self):
        for child in self.obj_bp.children:
            if child.get("IS_DRAWER_BOX"):
                box = sn_types.Assembly(child)
                self.drawer_boxes.append(box)

    def get_dbl_drawer_boxes(self):
        self.get_dbl_drawer_boxes = self.get_all_dbl_drawer_boxes()

    def add_prompts(self):
        common_prompts.add_thickness_prompts(self)
        self.overlay_ppt_obj = common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_drawer_pull_prompts(self)
        common_prompts.add_drawer_box_prompts(self)
        self.add_prompt("Open", 'PERCENTAGE', 0)
        self.add_prompt("Lift Drawers From Bottom", 'CHECKBOX', False)
        self.add_prompt("Bottom Drawer Space", 'DISTANCE', 0)
        self.add_prompt("Remove Bottom Shelf", 'CHECKBOX', False)
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
        self.add_prompt("Use Dovetail Drawer", 'CHECKBOX', False)
        self.add_prompt("Slide Type", 'COMBOBOX', 0, ["Sidemount", "Undermount"])
        self.add_prompt("Sidemount Options", 'COMBOBOX', 0, ["Hafele BB Sidemount Slides", "HR BB Soft Close Sidemount Slides"])
        self.add_prompt("Undermount Options", 'COMBOBOX', 0, 
                        ["Hettich 4D Undermount Slides", "Hettich V6 Undermount Slide",
                        "Blumotion Undermount Slides", "King Slide Undermount Slides"])
        self.add_prompt("Twenty-One Inches", 'DISTANCE', sn_unit.inch(21))
        self.add_prompt("Eighteen Inches", 'DISTANCE', sn_unit.inch(18))
        self.add_prompt("Fifteen Inches", 'DISTANCE', sn_unit.inch(15))
        self.add_prompt("Twelve Inches", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Nine Inches", 'DISTANCE', sn_unit.inch(9))
        self.add_prompt("Thick Adjustable Shelves", 'CHECKBOX', bpy.context.scene.sn_closets.closet_defaults.thick_adjustable_shelves)


    def add_drawer_box_prompts(self, drawer_num):
        self.add_prompt("Add Drawer Boxes", 'CHECKBOX', False)
        self.add_prompt("Lock " + str(drawer_num) + " Drawer", 'COMBOBOX', 0, ["None", "Top", "Left", "Right"])
        self.add_prompt("File Rail Type " + str(drawer_num), 'COMBOBOX', 0, ['Letter', 'Legal'])
        self.add_prompt("File Rail Direction " + str(drawer_num), 'COMBOBOX', 0, ['Front to Back', 'Lateral'])
        self.add_prompt("Use File Rail " + str(drawer_num), 'CHECKBOX', False)
        self.add_prompt("Use Double Drawer " + str(drawer_num), 'CHECKBOX', False)
        self.add_prompt("Has Jewelry Insert " + str(drawer_num), 'CHECKBOX', False)
        self.add_prompt("Has Sliding Insert " + str(drawer_num), 'CHECKBOX', False)
        self.add_prompt("Jewelry Insert Type " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_TYPE_LIST)
        self.add_prompt("Insert Placement X " + str(drawer_num), 'COMBOBOX', 0, common_lists.PLACEMENT_X)
        self.add_prompt("Insert Placement Y " + str(drawer_num), 'COMBOBOX', 0, common_lists.PLACEMENT_Y)
        self.add_prompt("Jewelry Insert 18in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_18IN_LIST)
        self.add_prompt("Jewelry Insert 21in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_21IN_LIST)
        self.add_prompt("Jewelry Insert 24in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_24IN_LIST)
        self.add_prompt("Upper Jewelry Insert Velvet Liner 18in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_LIST)
        self.add_prompt("Upper Jewelry Insert Velvet Liner 21in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_LIST)
        self.add_prompt("Upper Jewelry Insert Velvet Liner 24in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_LIST)
        self.add_prompt("Lower Jewelry Insert Velvet Liner 18in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_LIST)
        self.add_prompt("Lower Jewelry Insert Velvet Liner 21in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_LIST)
        self.add_prompt("Lower Jewelry Insert Velvet Liner 24in " + str(drawer_num), 'COMBOBOX', 0, common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_LIST)
        self.add_prompt("Sliding Insert 18in " + str(drawer_num), 'COMBOBOX', 0, common_lists.SLIDING_INSERTS_18IN_LIST)
        self.add_prompt("Sliding Insert 21in " + str(drawer_num), 'COMBOBOX', 0, common_lists.SLIDING_INSERTS_21IN_LIST)
        self.add_prompt("Sliding Insert 24in " + str(drawer_num), 'COMBOBOX', 0, common_lists.SLIDING_INSERTS_24IN_LIST)
        self.add_prompt("Velvet Liner " + str(drawer_num), 'COMBOBOX', 0, common_lists.VELVET_LINERS_LIST)

    def get_drawer_front(self, drawer_num):
        for drawer_front in self.get_all_drawer_fronts():
            if drawer_front.obj_bp.get("DRAWER_NUM") == drawer_num:
                return drawer_front

    def get_all_drawer_fronts(self):
        return [sn_types.Assembly(obj) for obj in self.obj_bp.children if "IS_BP_DRAWER_FRONT" in obj]

    def get_lock(self, drawer_num):
        for lock in self.get_all_locks():
            if lock.obj_bp.get("DRAWER_NUM") == drawer_num:
                return lock

    def get_all_locks(self):
        return [sn_types.Assembly(obj) for obj in self.obj_bp.children if "IS_BP_LOCK" in obj]

    def get_dbl_drawer_box(self, drawer_num):
        for box in self.get_all_dbl_drawer_boxes():
            if box.obj_bp.get("DRAWER_NUM") == drawer_num:
                return box

    def get_all_dbl_drawer_boxes(self):
        return [sn_types.Assembly(obj) for obj in self.obj_bp.children if "IS_BP_DBL_DRAWER_BOX" in obj]

    def add_right_pull(self):
        dim_x = self.obj_x.snap.get_var("location.x", "dim_x")
        dim_y = self.obj_y.snap.get_var("location.y", "dim_y")
        Hide = self.get_prompt("Hide").get_var()
        Left_Overlay = self.get_prompt("Left Overlay").get_var('Left_Overlay')
        Door_to_Cabinet_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_to_Cabinet_Gap')
        Open = self.get_prompt("Open").get_var('Open')
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Right_Overlay = self.get_prompt("Right Overlay").get_var('Right_Overlay')
        Use_Double_Pulls = self.get_prompt("Use Double Pulls").get_var('Use_Double_Pulls')
        No_Pulls = self.get_prompt("No Pulls").get_var('No_Pulls')
        Center_Pulls_on_Drawers = self.get_prompt("Center Pulls on Drawers").get_var('Center_Pulls_on_Drawers')
        Drawer_Pull_From_Top = self.get_prompt("Drawer Pull From Top").get_var('Drawer_Pull_From_Top')
        Max_Height_For_Centered_Pulls = self.get_prompt(
            "Max Height For Centered Pulls").get_var('Max_Height_For_Centered_Pulls')
        Large_Drawer_Pull_Height = self.get_prompt("Large Drawer Pull Height").get_var('Large_Drawer_Pull_Height')

        for front in self.get_all_drawer_fronts():
            front_z = front.obj_bp.snap.get_var("location.z", "front_z")
            DF_Height = front.obj_x.snap.get_var("location.x", "DF_Height")

            self.r_pull = common_parts.add_drawer_pull(self)
            self.r_pull.set_name("Drawer Pull")
            self.r_pull.loc_x('-Left_Overlay', [Left_Overlay])
            self.r_pull.loc_y('-Door_to_Cabinet_Gap-(dim_y*Open)', [Door_to_Cabinet_Gap, dim_y, Open, Front_Thickness])
            self.r_pull.loc_z('front_z', [front_z])
            self.r_pull.rot_x(value=math.radians(90))
            self.r_pull.dim_x('dim_x+Left_Overlay+Right_Overlay', [dim_x, Left_Overlay, Right_Overlay])
            self.r_pull.dim_y('DF_Height', [DF_Height])
            self.r_pull.dim_z('Front_Thickness', [Front_Thickness])
            self.r_pull.get_prompt("Pull X Location").set_formula(
                'IF(DF_Height<Max_Height_For_Centered_Pulls,DF_Height/2,Large_Drawer_Pull_Height)',
                [Large_Drawer_Pull_Height, Max_Height_For_Centered_Pulls,
                 Center_Pulls_on_Drawers, DF_Height, Drawer_Pull_From_Top])
            self.r_pull.get_prompt("Pull Z Location").set_formula(
                'dim_x-(dim_x/4)+Right_Overlay',
                [dim_x, Right_Overlay])
            self.r_pull.get_prompt('Hide').set_formula(
                'IF(No_Pulls,True,IF(Use_Double_Pulls,False,True)) or Hide',
                [No_Pulls, Use_Double_Pulls, Hide])

    def add_drawer_boxes(self):
        dim_x = self.obj_x.snap.get_var("location.x", "dim_x")
        y = self.obj_y.snap.get_var("location.y", "y")
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Door_to_Cabinet_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_to_Cabinet_Gap')
        Open = self.get_prompt("Open").get_var('Open')
        Drawer_Box_Slide_Gap = self.get_prompt("Drawer Box Slide Gap").get_var('Drawer_Box_Slide_Gap')
        Drawer_Box_Bottom_Gap = self.get_prompt("Drawer Box Bottom Gap").get_var('DBBG')
        Drawer_Box_Top_Gap = self.get_prompt("Drawer Box Top Gap").get_var('DBTG')
        SDF = self.get_prompt("Small Drawer Face").get_var("SDF")
        FHBD = self.get_prompt("Four Hole Box Difference").get_var("FHBD")
        THBD = self.get_prompt("Three Hole Box Difference").get_var("THBD")
        DBH = self.get_prompt("Double Box Height").get_var("DBH")
        LDBH = self.get_prompt("Locked Double Box Height").get_var("LDBH")
        S = self.get_prompt("Standard Drawer Rear Gap").get_var('S')
        D = self.get_prompt("Deep Drawer Rear Gap").get_var('D')
        E = self.get_prompt("Extra Deep Drawer Box").get_var('E')

        # I was extremely desperate to reduce how many characters are in the drawer.dim_y in order to get it to parse
        TO = self.get_prompt("Twenty-One Inches").get_var('TO')
        ET = self.get_prompt("Eighteen Inches").get_var('ET')
        F = self.get_prompt("Fifteen Inches").get_var('F')
        T = self.get_prompt("Twelve Inches").get_var('T')
        N = self.get_prompt("Nine Inches").get_var('N')

        for front in self.get_all_drawer_fronts():
            drawer_num = front.obj_bp.get("DRAWER_NUM")
            df_z_loc = front.obj_bp.snap.get_var("location.z", "df_z_loc")
            DF_Height = front.obj_x.snap.get_var("location.x", "DF_Height")
            Lock_Drawer = self.get_prompt("Lock " + str(drawer_num) + " Drawer").get_var("Lock_Drawer")
            FRT = self.get_prompt("File Rail Type " + str(drawer_num)).get_var("FRT")
            FRD = self.get_prompt("File Rail Direction " + str(drawer_num)).get_var("FRD")
            UFR = self.get_prompt("Use File Rail " + str(drawer_num)).get_var("UFR")
            UDD = self.get_prompt("Use Double Drawer " + str(drawer_num)).get_var('UDD')
            UD = self.get_prompt("Use Dovetail Drawer").get_var("UD")
            ST = self.get_prompt("Slide Type").get_var("ST")

            drawer = common_parts.add_drawer(self)
            drawer.obj_bp["IS_DRAWER_BOX"] = True
            drawer.obj_bp["DRAWER_NUM"] = drawer_num
            self.drawer_boxes.append(drawer)
            drawer.set_name("Drawer Box")
            drawer.loc_x('Drawer_Box_Slide_Gap', [Drawer_Box_Slide_Gap])
            drawer.loc_y('-Door_to_Cabinet_Gap-(y*Open)', [Door_to_Cabinet_Gap, y, Open, Front_Thickness])
            drawer.loc_z('df_z_loc+DBBG', [df_z_loc, Drawer_Box_Bottom_Gap])
            drawer.dim_x('dim_x-(Drawer_Box_Slide_Gap*2)', [dim_x, Drawer_Box_Slide_Gap])
            # I had to reduce characters a TON to get this to work. If there is a better solution, please let me know.
            # This was the only way I could find of achieving this without causing a dependency cycle.
            # Please ask me, Teddy Ruth, if you need to figure out what is even going on here
            drawer.dim_y(
                "IF(UFR,"
                "IF(FRD==1,"
                "IF(FRT==0,0.3556,0.4318),"  # 0.3556==INCH(14), 0.4318==INCH(17)
                "IF(y<=E,y-S,y-D)),"
                "IF(UD,"
                "IF(ST==1,"
                "CHECK(IF(y<=E,y-S,y-D)+0.0001,TO,ET,F,T,N)," # 0.0001 is there because otherwise I get a rounding error when we check what should be the same inch
                "IF(IF(y<=E,y-S,y-D)<0.3048,0.27305,"  # 0.3048==INCH(12), 0.27305==INCH(10.75)
                "IF(IF(y<=E,y-S,y-D)>0.6096,0.5588,"  # 0.6096==INCH(24), 0.5588==INCH(22)
                "IF(y<=E,y-S,y-D)))),"
                "IF(y<=E,y-S,y-D)))",
                [y, E, S, D, UFR, FRD, FRT, UD, ST, TO, ET, F, T, N])
            drawer.dim_z(
                ("IF(DF_Height<SDF,DF_Height-THBD,"
                 "IF(OR(Lock_Drawer==2,Lock_Drawer==3),IF(UDD,LDBH,DF_Height-DBTG-DBBG),"
                 "IF(DF_Height==SDF,DF_Height-FHBD,"
                 "IF(UDD,DBH,IF(DF_Height<INCH(4.89),DF_Height-DBTG-DBBG-INCH(0.68),DF_Height-DBTG-DBBG)))))"),
                 [DF_Height, SDF, Drawer_Box_Top_Gap, Drawer_Box_Bottom_Gap, FHBD, THBD, Lock_Drawer, LDBH, DBH, UDD])
            drawer.get_prompt('Use File Rail').set_formula('UFR', [UFR])
            drawer.get_prompt('File Rail Type').set_formula('FRT', [FRT])
            drawer.get_prompt('File Rail Direction').set_formula('FRD', [FRD])
            drawer.get_prompt('Use Dovetail Construction').set_formula('UD', [UD])
            drawer.get_prompt('Drawer Front Height').set_formula('DF_Height', [DF_Height])
            drawer.get_prompt('Slide Type').set_formula('ST', [ST])

    def add_lock(self, drawer_num):
        dim_x = self.obj_x.snap.get_var("location.x", "dim_x")
        dim_y = self.obj_y.snap.get_var("location.y", "dim_y")
        Division_Thickness = self.get_prompt("Division Thickness").get_var('Division_Thickness')
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Door_to_Cabinet_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_to_Cabinet_Gap')
        Drawer_Box_Top_Gap = self.get_prompt("Drawer Box Top Gap").get_var('DBTG')
        Drawer_Box_Bottom_Gap = self.get_prompt("Drawer Box Bottom Gap").get_var('DBBG')
        Lock_Drawer = self.get_prompt("Lock " + str(drawer_num) + " Drawer").get_var("Lock_Drawer")
        UDD = self.get_prompt("Use Double Drawer " + str(drawer_num)).get_var('UDD')
        Open = self.get_prompt("Open").get_var('Open')

        front = self.get_drawer_front(drawer_num)
        df_z_loc = front.obj_bp.snap.get_var("location.z", "df_z_loc")
        DF_Height = front.obj_x.snap.get_var("location.x", "DF_Height")

        drawer_lock = common_parts.add_lock(self)
        drawer_lock.obj_bp["DRAWER_NUM"] = drawer_num
        drawer_lock.loc_x(
            'IF(Lock_Drawer==2,-Division_Thickness,IF(Lock_Drawer==3,dim_x+Division_Thickness,dim_x/2))',
            [Lock_Drawer, dim_x, Division_Thickness])
        drawer_lock.loc_y(
            'IF(Lock_Drawer==1,-Front_Thickness-Door_to_Cabinet_Gap-(dim_y*Open),+INCH(.75))',
            [Lock_Drawer, Front_Thickness, Door_to_Cabinet_Gap, Open, dim_y])
        drawer_lock.loc_z(
            'df_z_loc+IF(UDD,DF_Height-DBTG-DBBG,DF_Height)-INCH(.5)',
            [df_z_loc, UDD, DF_Height, Drawer_Box_Top_Gap, Drawer_Box_Bottom_Gap])
        drawer_lock.rot_z('IF(Lock_Drawer==2,radians(-90),IF(Lock_Drawer==3,radians(90),0))', [Lock_Drawer])
        drawer_lock.get_prompt('Hide').set_formula('IF(Lock_Drawer>0,False,True)', [Lock_Drawer])

    def add_dbl_drawer_box(self, drawer_num):
        dim_x = self.obj_x.snap.get_var("location.x", "dim_x")
        dim_y = self.obj_y.snap.get_var("location.y", "dim_y")
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Door_to_Cabinet_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_to_Cabinet_Gap')
        Open = self.get_prompt("Open").get_var('Open')
        Drawer_Box_Slide_Gap = self.get_prompt("Drawer Box Slide Gap").get_var('Drawer_Box_Slide_Gap')
        Drawer_Box_Bottom_Gap = self.get_prompt("Drawer Box Bottom Gap").get_var('DBBG')
        DBH = self.get_prompt("Double Box Height").get_var("DBH")
        LDBH = self.get_prompt("Locked Double Box Height").get_var("LDBH")
        Standard_Drawer_Rear_Gap = self.get_prompt("Standard Drawer Rear Gap").get_var('Standard_Drawer_Rear_Gap')
        Deep_Drawer_Rear_Gap = self.get_prompt("Deep Drawer Rear Gap").get_var('Deep_Drawer_Rear_Gap')
        EDDB = self.get_prompt("Extra Deep Drawer Box").get_var('EDDB')
        Shelf_Thickness = self.get_prompt("Shelf Thickness").get_var('Shelf_Thickness')
        Six_Hole = self.get_prompt("Six Hole").get_var('Six_Hole')
        Seven_Hole = self.get_prompt("Seven Hole").get_var('Seven_Hole')
        hide_var = self.get_prompt("Hide").get_var()

        front = self.get_drawer_front(drawer_num)
        df_z_loc = front.obj_bp.snap.get_var("location.z", "df_z_loc")
        DF_Height = front.obj_x.snap.get_var("location.x", "DF_Height")
        Lock_Drawer = self.get_prompt("Lock " + str(drawer_num) + " Drawer").get_var("Lock_Drawer")
        FR_Type = self.get_prompt("File Rail Type " + str(drawer_num)).get_var("FR_Type")
        FR_Direction = self.get_prompt("File Rail Direction " + str(drawer_num)).get_var("FR_Direction")
        Use_FR = self.get_prompt("Use File Rail " + str(drawer_num)).get_var("Use_FR")
        UDD = self.get_prompt("Use Double Drawer " + str(drawer_num)).get_var('UDD')

        double_drawer = common_parts.add_drawer(self)
        double_drawer.obj_bp["IS_BP_DBL_DRAWER_BOX"] = True
        double_drawer.obj_bp["DRAWER_NUM"] = drawer_num
        double_drawer.set_name("Drawer Box")
        double_drawer.loc_x('Drawer_Box_Slide_Gap', [Drawer_Box_Slide_Gap])
        double_drawer.loc_y(
            '-Door_to_Cabinet_Gap-(dim_y*(Open/2))', [Door_to_Cabinet_Gap, dim_y, Open, Front_Thickness])
        double_drawer.loc_z(
            'df_z_loc+DBBG+Shelf_Thickness+IF(OR(Lock_Drawer==2,Lock_Drawer==3),LDBH,DBH)',
            [df_z_loc, Drawer_Box_Bottom_Gap, Lock_Drawer, DBH, LDBH, Shelf_Thickness])
        double_drawer.dim_x('dim_x-(Drawer_Box_Slide_Gap*2)', [dim_x, Drawer_Box_Slide_Gap])
        double_drawer.dim_y('IF(dim_y <= EDDB, dim_y-Standard_Drawer_Rear_Gap, dim_y-Deep_Drawer_Rear_Gap)',
                            [dim_y, EDDB, Standard_Drawer_Rear_Gap, Deep_Drawer_Rear_Gap])
        double_drawer.dim_z("DBH",[DBH])
        double_drawer.get_prompt('Hide').set_formula(
            "IF(AND(DF_Height >= Six_Hole,DF_Height <= Seven_Hole,dim_y >= " + str(sn_unit.inch(15.99)) + "),"
            "IF(UDD,False,True),True) or Hide",
            [UDD, DF_Height, Six_Hole, Seven_Hole, dim_y, hide_var])
        double_drawer.get_prompt('Use File Rail').set_formula('Use_FR', [Use_FR])
        double_drawer.get_prompt('File Rail Type').set_formula('FR_Type', [FR_Type])
        double_drawer.get_prompt('File Rail Direction').set_formula('FR_Direction', [FR_Direction])

    def add_drawers(self):
        dim_x = self.obj_x.snap.get_var("location.x", "dim_x")
        dim_y = self.obj_y.snap.get_var("location.y", "dim_y")
        Left_Overlay = self.get_prompt("Left Overlay").get_var('Left_Overlay')
        Right_Overlay = self.get_prompt("Right Overlay").get_var('Right_Overlay')
        Horizontal_Gap = self.overlay_ppt_obj.snap.get_prompt("Horizontal Gap").get_var()
        Front_Thickness = self.get_prompt("Front Thickness").get_var('Front_Thickness')
        Door_to_Cabinet_Gap = self.get_prompt("Door to Cabinet Gap").get_var('Door_to_Cabinet_Gap')
        Open = self.get_prompt("Open").get_var('Open')
        Drawer_Quantity = self.get_prompt("Drawer Quantity").get_var('Drawer_Quantity')
        Drawer_Stack_Height = self.stack_height_ppt_obj.snap.get_prompt("Drawer Stack Height").get_var('Drawer_Stack_Height')
        Center_Pulls_on_Drawers = self.get_prompt("Center Pulls on Drawers").get_var('Center_Pulls_on_Drawers')
        Drawer_Pull_From_Top = self.get_prompt("Drawer Pull From Top").get_var('Drawer_Pull_From_Top')
        Use_Double_Pulls = self.get_prompt("Use Double Pulls").get_var('Use_Double_Pulls')
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
        SDFOD = self.get_prompt("Single Door Full Overlay Difference").get_var("SDFOD")
        AHOBD = self.get_prompt("Above Hamper Or Base Doors").get_var('AHOBD')
        TAS = self.get_prompt("Thick Adjustable Shelves").get_var('TAS')

        prev_drawer_empty = None

        for i in range(1, self.number_of_drawers):
            DF_Height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(i) + " Height").get_var("DF_Height")
            Lock_Drawer = self.get_prompt("Lock " + str(i) + " Drawer").get_var("Lock_Drawer")

            front_empty = self.add_empty("Drawer Front Height")
            if prev_drawer_empty:
                prev_drawer_z_loc = prev_drawer_empty.snap.get_var('location.z','prev_drawer_z_loc')
                front_empty.snap.loc_z('prev_drawer_z_loc-DF_Height-Horizontal_Gap',[prev_drawer_z_loc,DF_Height,Horizontal_Gap])
            else:
                front_empty.snap.loc_z('Drawer_Stack_Height-DF_Height+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                                  [Drawer_Stack_Height,DF_Height,Lift_Drawers_From_Bottom,Bottom_Drawer_Space,Top_Overlay])               
            df_z_loc = front_empty.snap.get_var('location.z','df_z_loc')
            prev_drawer_empty = front_empty

            front = common_parts.add_drawer_front(self)
            front.obj_bp["DRAWER_NUM"] = i
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

            KD_Shelf = common_parts.add_shelf(self)
            IBEKD = KD_Shelf.get_prompt('Is Bottom Exposed KD').get_var('IBEKD')
            KD_Shelf.loc_y('Default_Middle_KD_Depth', [Default_Middle_KD_Depth])
            KD_Shelf.loc_z('df_z_loc+DF_Height-Top_Overlay',[df_z_loc,DF_Height,Top_Overlay])
            KD_Shelf.rot_x(value=math.radians(180))
            KD_Shelf.dim_x('dim_x',[dim_x])
            KD_Shelf.dim_y('Default_Middle_KD_Depth', [Default_Middle_KD_Depth])
            # KD_Shelf.dim_z('IF(AND(TAS,IBEKD==False), INCH(1),Shelf_Thickness) *-1', [Shelf_Thickness, TAS, IBEKD])
            KD_Shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness, TAS, IBEKD])
            KD_Shelf.get_prompt('Is Locked Shelf').set_value(value=True)
            KD_Shelf.get_prompt("Is Forced Locked Shelf").set_value(value=True)
            KD_Shelf.get_prompt('Hide').set_value(value=True)
            KD_Shelf.dim_y('IF(Lock_Drawer>0, dim_y, Default_Middle_KD_Depth) or Hide',  [self.hide_var, Lock_Drawer, dim_y, Default_Middle_KD_Depth])
            KD_Shelf.loc_y('IF(Lock_Drawer>0, dim_y, Default_Middle_KD_Depth)', [Lock_Drawer, dim_y, Default_Middle_KD_Depth])

            if(i==1):
                KD_Shelf.dim_y('dim_y', [dim_y])
                KD_Shelf.loc_y('dim_y', [dim_y])
                KD_Shelf.get_prompt('Hide').set_formula('IF(Remove_Top_Shelf,True,IF(Lock_Drawer>0,False,True))',[Remove_Top_Shelf,Lock_Drawer])
            if(i==2):
                KD_Shelf.get_prompt('Hide').set_formula('IF(AHOBD,IF(Lock_Drawer>0,False,True),IF(Drawer_Quantity-1 == 2,False,IF( Drawer_Quantity-1 == 3,False,IF(Lock_Drawer>0,False,True)))) or Hide', [self.hide_var, Drawer_Quantity, Lock_Drawer, AHOBD])
                
            if(i==3):
                KD_Shelf.get_prompt('Hide').set_formula('IF(Drawer_Quantity-1 == 4,False,IF(Drawer_Quantity-1 == 5,False,IF(Drawer_Quantity-1 == 7,False,IF(Lock_Drawer>0,False,True)))) or Hide', [self.hide_var, Drawer_Quantity, Lock_Drawer, AHOBD])
                
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

        self.drawer_front_ppt_obj = self.add_prompt_obj("OBJ_PROMPTS_Drawer_Fronts")
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
        TAS = self.get_prompt("Thick Adjustable Shelves").get_var('TAS')

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
        IBEKD = top_shelf.get_prompt('Is Bottom Exposed KD').get_var('IBEKD')
        top_shelf.loc_y('dim_y', [dim_y])
        top_shelf.loc_z('Drawer_Stack_Height-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        top_shelf.rot_x(value=math.radians(180))
        top_shelf.dim_x('dim_x',[dim_x])
        top_shelf.dim_y('dim_y',[dim_y])
        # top_shelf.dim_z('IF(AND(TAS,IBEKD==False), INCH(1),Shelf_Thickness) *-1', [Shelf_Thickness, TAS, IBEKD])
        top_shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness, TAS, IBEKD])
        top_shelf.dim_z('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.get_prompt('Hide').set_formula('IF(Remove_Top_Shelf,False,True) or Hide',[Remove_Top_Shelf,self.hide_var])
        top_shelf.get_prompt('Is Locked Shelf').set_value(value=True)
        top_shelf.get_prompt("Is Forced Locked Shelf").set_value(value=True)
        
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
        bottom_shelf.get_prompt("Is Forced Locked Shelf").set_value(value=True)
        
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
    
    has_jewelry_insert_1: BoolProperty(name="Has Jewelry Insert 1",
                                       default=False)

    has_jewelry_insert_2: BoolProperty(name="Has Jewelry Insert 2",
                                       default=False)

    has_jewelry_insert_3: BoolProperty(name="Has Jewelry Insert 3",
                                       default=False)

    has_jewelry_insert_4: BoolProperty(name="Has Jewelry Insert 4",
                                       default=False)

    has_jewelry_insert_5: BoolProperty(name="Has Jewelry Insert 5",
                                       default=False)

    has_jewelry_insert_6: BoolProperty(name="Has Jewelry Insert 6",
                                       default=False)

    has_jewelry_insert_7: BoolProperty(name="Has Jewelry Insert 7",
                                       default=False)

    has_jewelry_insert_8: BoolProperty(name="Has Jewelry Insert 8",
                                       default=False)
    
    has_sliding_insert_1: BoolProperty(name="Has Sliding Insert 1",
                                       default=False)

    has_sliding_insert_2: BoolProperty(name="Has Sliding Insert 2",
                                       default=False)

    has_sliding_insert_3: BoolProperty(name="Has Sliding Insert 3",
                                       default=False)

    has_sliding_insert_4: BoolProperty(name="Has Sliding Insert 4",
                                       default=False)

    has_sliding_insert_5: BoolProperty(name="Has Sliding Insert 5",
                                       default=False)

    has_sliding_insert_6: BoolProperty(name="Has Sliding Insert 6",
                                       default=False)

    has_sliding_insert_7: BoolProperty(name="Has Sliding Insert 7",
                                       default=False)

    has_sliding_insert_8: BoolProperty(name="Has Sliding Insert 8",
                                       default=False)

    jewelry_insert_type_1: EnumProperty(name="Jewelry Insert Type 1", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    jewelry_insert_type_2: EnumProperty(name="Jewelry Insert Type 2", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    jewelry_insert_type_3: EnumProperty(name="Jewelry Insert Type 3", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    jewelry_insert_type_4: EnumProperty(name="Jewelry Insert Type 4", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    jewelry_insert_type_5: EnumProperty(name="Jewelry Insert Type 5", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    jewelry_insert_type_6: EnumProperty(name="Jewelry Insert Type 6", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    jewelry_insert_type_7: EnumProperty(name="Jewelry Insert Type 7", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    jewelry_insert_type_8: EnumProperty(name="Jewelry Insert Type 8", 
                                       items=common_lists.JEWELRY_TYPE_OPTIONS,
                                       default='0')

    insert_placement_x_1: EnumProperty(name="Insert Placement X 1", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_1: EnumProperty(name="Insert Placement Y 1", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    insert_placement_x_2: EnumProperty(name="Insert Placement X 2", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_2: EnumProperty(name="Insert Placement Y 2", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    insert_placement_x_3: EnumProperty(name="Insert Placement X 3", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_3: EnumProperty(name="Insert Placement Y 3", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    insert_placement_x_4: EnumProperty(name="Insert Placement X 4", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_4: EnumProperty(name="Insert Placement Y 4", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    insert_placement_x_5: EnumProperty(name="Insert Placement X 5", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_5: EnumProperty(name="Insert Placement Y 5", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    insert_placement_x_6: EnumProperty(name="Insert Placement X 6", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_6: EnumProperty(name="Insert Placement Y 6", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    insert_placement_x_7: EnumProperty(name="Insert Placement X 7", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_7: EnumProperty(name="Insert Placement Y 7", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    insert_placement_x_8: EnumProperty(name="Insert Placement X 8", 
                                       items=common_lists.PLACEMENT_OPTIONS_X,
                                       default='0')

    insert_placement_y_8: EnumProperty(name="Insert Placement Y 8", 
                                       items=common_lists.PLACEMENT_OPTIONS_Y,
                                       default='0')

    jewelry_insert_18in_1: EnumProperty(name="Jewelry Insert 18in 1", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_1: EnumProperty(name="Jewelry Insert 21in 1", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_1: EnumProperty(name="Jewelry Insert 24in 1", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    jewelry_insert_18in_2: EnumProperty(name="Jewelry Insert 18in 2", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_2: EnumProperty(name="Jewelry Insert 21in 2", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_2: EnumProperty(name="Jewelry Insert 24in 2", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    jewelry_insert_18in_3: EnumProperty(name="Jewelry Insert 18in 3", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_3: EnumProperty(name="Jewelry Insert 21in 3", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_3: EnumProperty(name="Jewelry Insert 24in 3", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    jewelry_insert_18in_4: EnumProperty(name="Jewelry Insert 18in 4", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_4: EnumProperty(name="Jewelry Insert 21in 4", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_4: EnumProperty(name="Jewelry Insert 24in 4", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    jewelry_insert_18in_5: EnumProperty(name="Jewelry Insert 18in 5", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_5: EnumProperty(name="Jewelry Insert 21in 5", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_5: EnumProperty(name="Jewelry Insert 24in 5", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    jewelry_insert_18in_6: EnumProperty(name="Jewelry Insert 18in 6", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_6: EnumProperty(name="Jewelry Insert 21in 6", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_6: EnumProperty(name="Jewelry Insert 24in 6", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    jewelry_insert_18in_7: EnumProperty(name="Jewelry Insert 18in 7", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_7: EnumProperty(name="Jewelry Insert 21in 7", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_7: EnumProperty(name="Jewelry Insert 24in 7", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    jewelry_insert_18in_8: EnumProperty(name="Jewelry Insert 18in 8", 
                                        items=common_lists.JEWELRY_INSERTS_18IN_OPTIONS, 
                                        default='0')

    jewelry_insert_21in_8: EnumProperty(name="Jewelry Insert 21in 8", 
                                        items=common_lists.JEWELRY_INSERTS_21IN_OPTIONS, 
                                        default='0')

    jewelry_insert_24in_8: EnumProperty(name="Jewelry Insert 24in 8", 
                                        items=common_lists.JEWELRY_INSERTS_24IN_OPTIONS, 
                                        default='0')

    upper_jewelry_insert_velvet_liner_18in_1: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 1",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_1: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 1",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_1: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 1",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_1: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 1",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_1: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 1",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_1: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 1",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_18in_2: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 2",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_2: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 2",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_2: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 2",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_2: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 2",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_2: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 2",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_2: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 2",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_18in_3: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 3",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_3: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 3",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_3: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 3",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_3: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 3",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_3: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 3",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_3: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 3",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_18in_4: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 4",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_4: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 4",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_4: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 4",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_4: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 4",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_4: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 4",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_4: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 4",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_18in_5: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 5",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_5: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 5",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_5: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 5",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_5: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 5",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_5: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 5",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_5: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 5",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_18in_6: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 6",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_6: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 6",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_6: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 6",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_6: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 6",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_6: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 6",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_6: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 6",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_18in_7: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 7",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_7: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 7",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_7: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 7",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_7: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 7",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_7: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 7",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_7: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 7",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_18in_8: EnumProperty(name="Upper Jewelry Insert Velvet Liner 18in 8",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_18in_8: EnumProperty(name="Lower Jewelry Insert Velvet Liner 18in 8",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_21in_8: EnumProperty(name="Upper Jewelry Insert Velvet Liner 21in 8",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_21in_8: EnumProperty(name="Lower Jewelry Insert Velvet Liner 21in 8",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS,
                                                     default='0')

    upper_jewelry_insert_velvet_liner_24in_8: EnumProperty(name="Upper Jewelry Insert Velvet Liner 24in 8",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')
    
    lower_jewelry_insert_velvet_liner_24in_8: EnumProperty(name="Lower Jewelry Insert Velvet Liner 24in 8",
                                                     items=common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS,
                                                     default='0')

    sliding_insert_18in_1: EnumProperty(name="Sliding Insert 18in 1",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_1: EnumProperty(name="Sliding Insert 21in 1",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_1: EnumProperty(name="Sliding Insert 24in 1",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    sliding_insert_18in_2: EnumProperty(name="Sliding Insert 18in 2",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_2: EnumProperty(name="Sliding Insert 21in 2",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_2: EnumProperty(name="Sliding Insert 24in 2",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    sliding_insert_18in_3: EnumProperty(name="Sliding Insert 18in 3",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_3: EnumProperty(name="Sliding Insert 21in 3",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_3: EnumProperty(name="Sliding Insert 24in 3",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    sliding_insert_18in_4: EnumProperty(name="Sliding Insert 18in 4",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_4: EnumProperty(name="Sliding Insert 21in 4",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_4: EnumProperty(name="Sliding Insert 24in 4",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    sliding_insert_18in_5: EnumProperty(name="Sliding Insert 18in 5",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_5: EnumProperty(name="Sliding Insert 21in 5",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_5: EnumProperty(name="Sliding Insert 24in 5",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    sliding_insert_18in_6: EnumProperty(name="Sliding Insert 18in 6",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_6: EnumProperty(name="Sliding Insert 21in 6",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_6: EnumProperty(name="Sliding Insert 24in 6",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    sliding_insert_18in_7: EnumProperty(name="Sliding Insert 18in 7",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_7: EnumProperty(name="Sliding Insert 21in 7",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_7: EnumProperty(name="Sliding Insert 24in 7",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    sliding_insert_18in_8: EnumProperty(name="Sliding Insert 18in 8",
                                        items=common_lists.SLIDING_INSERTS_18IN_OPTIONS,
                                        default='0')

    sliding_insert_21in_8: EnumProperty(name="Sliding Insert 21in 8",
                                        items=common_lists.SLIDING_INSERTS_21IN_OPTIONS,
                                        default='0')

    sliding_insert_24in_8: EnumProperty(name="Sliding Insert 24in 8",
                                        items=common_lists.SLIDING_INSERTS_24IN_OPTIONS,
                                        default='0')

    velvet_liner_1: EnumProperty(name="Velvet Liner 1",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
                                 default='0')

    velvet_liner_2: EnumProperty(name="Velvet Liner 2",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
                                 default='0')

    velvet_liner_3: EnumProperty(name="Velvet Liner 3",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
                                 default='0')

    velvet_liner_4: EnumProperty(name="Velvet Liner 4",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
                                 default='0')

    velvet_liner_5: EnumProperty(name="Velvet Liner 5",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
                                 default='0')

    velvet_liner_6: EnumProperty(name="Velvet Liner 6",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
                                 default='0')

    velvet_liner_7: EnumProperty(name="Velvet Liner 7",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
                                 default='0')

    velvet_liner_8: EnumProperty(name="Velvet Liner 8",
                                 items=common_lists.VELVET_LINERS_OPTIONS,
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

    slide_type: EnumProperty(
        name="Slide Type",
        items=SLIDE_TYPE,
        default='0')

    sidemount_options: EnumProperty(
        name="Sidemount Options",
        items=SIDEMOUNT_OPTIONS,
        default='0')

    undermount_options: EnumProperty(
        name="Undermount Options",
        items=UNDERMOUNT_OPTIONS,
        default='0')

    front_heights = []

    drawer_qty_prompt = None
    drawer_front_ppt_obj = None
    cleat_loc_prompt = None
    set_default_slide = False

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
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}

    def update_pulls(self, context):
        use_dbl_pulls = self.assembly.get_prompt("Use Double Pulls")

        if use_dbl_pulls.get_value() and self.assembly.r_pull is None:
            self.assembly.add_right_pull()
        elif not use_dbl_pulls.get_value() and self.assembly.r_pull:
            sn_utils.delete_object_and_children(self.assembly.r_pull.obj_bp)
            self.assembly.r_pull = None

    def update_drawer_boxes(self, context):
        add_drawers_ppt = self.assembly.get_prompt("Add Drawer Boxes")
        open_drawers_ppt = self.assembly.get_prompt("Open")

        if add_drawers_ppt.get_value() and not self.assembly.drawer_boxes:
            self.assembly.add_drawer_boxes()
            self.assembly.update()
            open_drawers_ppt.set_value(1.0)
            bpy.ops.object.select_all(action='DESELECT')
        elif not add_drawers_ppt.get_value() and self.assembly.drawer_boxes:
            for assembly in self.assembly.drawer_boxes:
                sn_utils.delete_object_and_children(assembly.obj_bp)
            self.assembly.drawer_boxes.clear()
            open_drawers_ppt.set_value(0)

    def update_dbl_drawer_box(self, drawer_num):
        add_drawers_ppt = self.assembly.get_prompt("Add Drawer Boxes")
        use_double_drawer = self.assembly.get_prompt("Use Double Drawer " + str(drawer_num))
        dbl_drawer = self.assembly.get_dbl_drawer_box(drawer_num)
        six_hole = self.assembly.get_prompt("Six Hole")
        seven_hole = self.assembly.get_prompt("Seven Hole")
        drawer_height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(drawer_num) + " Height")

        dbl_drawer_conditions = [
            drawer_height.get_value() < six_hole.get_value(),
            drawer_height.get_value() > seven_hole.get_value(),
            self.assembly.obj_y.location.y < sn_unit.inch(15.99)]

        if any(dbl_drawer_conditions):
            use_double_drawer.set_value(False)        

        if add_drawers_ppt.get_value() and not dbl_drawer and use_double_drawer.get_value():
            self.assembly.add_dbl_drawer_box(drawer_num)
        elif add_drawers_ppt.get_value() and dbl_drawer and not use_double_drawer.get_value():
            sn_utils.delete_object_and_children(dbl_drawer.obj_bp)

    def update_lock(self, drawer_num):
        lock_drawer = self.assembly.get_prompt("Lock " + str(drawer_num) + " Drawer")
        lock = self.assembly.get_lock(drawer_num)
        small_drawer_face = self.assembly.get_prompt("Small Drawer Face")
        drawer_height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(drawer_num) + " Height")

        if lock_drawer:
            exec("lock_drawer.set_value(int(self.lock_" + str(drawer_num) + "_drawer))")

            if drawer_height.get_value() < small_drawer_face.get_value():
                lock_drawer.set_value(0)

            if not lock and lock_drawer.get_value():
                self.assembly.add_lock(drawer_num)
            elif lock and not lock_drawer.get_value():
                sn_utils.delete_object_and_children(lock.obj_bp)

    def update_cleat_loc(self):
        if self.cleat_loc_prompt:
            self.cleat_loc_prompt.set_value(int(self.cleat_location))

    def update_file_rail_type(self, drawer_num):
        small_drawer_face = self.assembly.get_prompt("Small Drawer Face")
        large_drawer_face = self.assembly.get_prompt("Large Drawer Face")        
        drawer_height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(drawer_num) + " Height")
        lock_drawer = self.assembly.get_prompt("Lock " + str(drawer_num) + " Drawer")
        use_file_rail = self.assembly.get_prompt("Use File Rail " + str(drawer_num))
        file_rail_type = self.assembly.get_prompt("File Rail Type " + str(drawer_num))
        file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(drawer_num))
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

        exec("file_rail_type.set_value(int(self.file_rail_type_" + str(drawer_num) + "))")

        if(drawer_height.get_value() >= large_drawer_face.get_value() and (width >= letter or depth >= letter)):
            if(use_file_rail.get_value()):
                if(width < letter):
                    if(depth < legal):
                        exec("self.file_rail_type_" + str(drawer_num) + "= str(0)")
                        file_rail_type.set_value(0)
                        exec("self.file_rail_direction_" + str(drawer_num) + "= str(1)")
                        file_rail_direction.set_value(1)
                    else:
                        exec("file_rail_direction_" + str(drawer_num) + "= str(1)")
                        file_rail_direction.set_value(1)

                elif(width < legal):
                    if(depth < letter):
                        exec("self.file_rail_type_" + str(drawer_num) + "= str(0)")
                        file_rail_type.set_value(0)
                        exec("self.file_rail_direction_" + str(drawer_num) + "= str(0)")
                        file_rail_direction.set_value(0)

                    elif(depth < legal):
                        exec("self.file_rail_type_" + str(drawer_num) + "= str(0)")
                        file_rail_type.set_value(0)
                    else:
                        if(file_rail_direction.get_value() == 0):
                            exec("self.file_rail_type_" + str(drawer_num) + "= str(0)")
                            file_rail_type.set_value(0)
                else:
                    if(depth < letter):
                        exec("self.file_rail_direction_" + str(drawer_num) + "= str(0)")
                        file_rail_direction.set_value(0)
                    elif(depth < legal):
                        if(file_rail_direction.get_value() == 1):
                            exec("self.file_rail_type_" + str(drawer_num) + "= str(0)")
                            file_rail_type.set_value(0)
        else:
            use_file_rail.set_value(False)

    def update_kd_shelf(self):
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
        
        bp = self.assembly.obj_bp
        old_kd_prompt_name = self.kd_prompt.name
        old_kd_prompt_value = self.kd_prompt.get_value()

        if lift_drawers_from_bottom.get_value():
            self.kd_prompt = self.assembly.get_prompt('Remove Bottom Shelf')
        elif bp and bp.parent:
            parent_assembly = sn_types.Assembly(bp.parent)
            if bp.parent.sn_closets and hasattr(bp.parent.sn_closets, 'opening_name') and 'Section' in bp.parent.name:
                self.kd_prompt = parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + bp.parent.sn_closets.opening_name)
            else:
                self.kd_prompt = parent_assembly.get_prompt('Remove Top Shelf')
                if not self.kd_prompt:
                    self.kd_prompt = self.assembly.get_prompt('Remove Bottom Shelf')
        
        # if we are going from drawer to pard
        if old_kd_prompt_name == 'Remove Bottom Shelf' and \
            self.kd_prompt.name != 'Remove Bottom Shelf':
            if old_kd_prompt_value or self.kd_prompt.get_value():
                self.kd_prompt.set_value(True)
                self.assembly.get_prompt('Remove Bottom Shelf').set_value(False)
            else:
                self.kd_prompt.set_value(False)
                self.assembly.get_prompt('Remove Bottom Shelf').set_value(False)
        # if we are going from pard to drawer
        if old_kd_prompt_name != 'Remove Bottom Shelf' and \
            self.kd_prompt.name == 'Remove Bottom Shelf':
            if old_kd_prompt_value or self.kd_prompt.get_value():
                self.kd_prompt.set_value(True)
                self.assembly.get_prompt('Remove Bottom Shelf').set_value(True)
            else:
                self.kd_prompt.set_value(False)
                self.assembly.get_prompt('Remove Bottom Shelf').set_value(False)

    def update_dovetail_defaults(self):
        """
        This function is designed to set the slide to Undermount Hettich 4D slides 
        and to set the drawer rear gap to 1"
        when the user swaps to Dovetail Drawer Boxes.
        """
        use_dovetail_drawer = self.assembly.get_prompt("Use Dovetail Drawer")
        slide_type = self.assembly.get_prompt("Slide Type")
        undermount_options = self.assembly.get_prompt("Undermount Options")
        standard_drawer_box_rear_gap = self.assembly.get_prompt("Standard Drawer Rear Gap")
        deep_drawer_box_rear_gap = self.assembly.get_prompt("Deep Drawer Rear Gap")
        prompts = [use_dovetail_drawer, slide_type, undermount_options, standard_drawer_box_rear_gap, deep_drawer_box_rear_gap]

        if all(prompts):
            if use_dovetail_drawer.get_value() and not self.set_default_slide:
                self.set_default_slide = True
                slide_type.set_value(1)
                self.slide_type = '1'
                undermount_options.set_value(0)
                self.undermount_options = '0'
                standard_drawer_box_rear_gap.set_value(sn_unit.inch(1))
                deep_drawer_box_rear_gap.set_value(sn_unit.inch(1))
            elif self.set_default_slide and not use_dovetail_drawer.get_value():
                self.set_default_slide = False
                if slide_type.get_value() == 1:
                    standard_drawer_box_rear_gap.set_value(sn_unit.inch(1.25))
                    deep_drawer_box_rear_gap.set_value(sn_unit.inch(2))

            if slide_type.get_value() == 0 and self.slide_type == '1' and use_dovetail_drawer.get_value():
                standard_drawer_box_rear_gap.set_value(sn_unit.inch(1))
                deep_drawer_box_rear_gap.set_value(sn_unit.inch(1))
            elif slide_type.get_value() == 1 and self.slide_type == '0' and use_dovetail_drawer.get_value():
                standard_drawer_box_rear_gap.set_value(sn_unit.inch(1.25))
                deep_drawer_box_rear_gap.set_value(sn_unit.inch(2))



    def check(self, context):
        start_time = time.perf_counter()
        props = bpy.context.scene.sn_closets
        self.update_pulls(context)
        self.update_drawer_boxes(context)
        self.update_cleat_loc()
        self.update_dovetail_defaults()

        if self.drawer_qty_prompt:
            self.drawer_qty_prompt.quantity_value = int(self.drawer_quantity)
            slide_type = self.assembly.get_prompt("Slide Type")
            sidemount_options = self.assembly.get_prompt("Sidemount Options")
            undermount_options = self.assembly.get_prompt("Undermount Options")
            dovetail_drawer = self.assembly.get_prompt("Use Dovetail Drawer")
            slide_prompts = [slide_type, sidemount_options, undermount_options, dovetail_drawer]
            if all(slide_prompts):
                if not dovetail_drawer.get_value():
                    slide_type.set_value(0)
                    self.slide_type = "0"
                else:
                    slide_type.set_value(int(self.slide_type))
                sidemount_options.set_value(int(self.sidemount_options))
                undermount_options.set_value(int(self.undermount_options))

            for i in range(1, self.drawer_qty_prompt.get_value()):
                drawer_height = self.drawer_front_ppt_obj.snap.get_prompt("Drawer " + str(i) + " Height")
                bottom_offset = self.assembly.get_prompt("Bottom Drawer Space")
                slide_type = self.assembly.get_prompt("Drawer " + str(i) + " Slide Type") #DONT REMOVE USED in exec
                file_rail_type = self.assembly.get_prompt("File Rail Type " + str(i))
                file_rail_direction = self.assembly.get_prompt("File Rail Direction " + str(i))
                has_jewelry_insert = self.assembly.get_prompt("Has Jewelry Insert " + str(i))
                has_sliding_insert = self.assembly.get_prompt("Has Sliding Insert " + str(i))
                jewelry_insert_type = self.assembly.get_prompt("Jewelry Insert Type " + str(i)) #DONT REMOVE USED in exec
                jewelry_insert_18in = self.assembly.get_prompt("Jewelry Insert 18in " + str(i)) #DONT REMOVE USED in exec
                jewelry_insert_21in = self.assembly.get_prompt("Jewelry Insert 21in " + str(i)) #DONT REMOVE USED in exec
                jewelry_insert_24in = self.assembly.get_prompt("Jewelry Insert 24in " + str(i)) #DONT REMOVE USED in exec
                upper_jewelry_insert_velvet_liner_18_in = self.assembly.get_prompt("Upper Jewelry Insert Velvet Liner 18in " + str(i)) #DONT REMOVE USED in exec
                upper_jewelry_insert_velvet_liner_21_in = self.assembly.get_prompt("Upper Jewelry Insert Velvet Liner 21in " + str(i)) #DONT REMOVE USED in exec
                upper_jewelry_insert_velvet_liner_24_in = self.assembly.get_prompt("Upper Jewelry Insert Velvet Liner 24in " + str(i)) #DONT REMOVE USED in exec
                lower_jewelry_insert_velvet_liner_18_in = self.assembly.get_prompt("Lower Jewelry Insert Velvet Liner 18in " + str(i)) #DONT REMOVE USED in exec
                lower_jewelry_insert_velvet_liner_21_in = self.assembly.get_prompt("Lower Jewelry Insert Velvet Liner 21in " + str(i)) #DONT REMOVE USED in exec
                lower_jewelry_insert_velvet_liner_24_in = self.assembly.get_prompt("Lower Jewelry Insert Velvet Liner 24in " + str(i)) #DONT REMOVE USED in exec
                
                sliding_insert_18in = self.assembly.get_prompt("Sliding Insert 18in " + str(i)) #DONT REMOVE USED in exec
                sliding_insert_21in = self.assembly.get_prompt("Sliding Insert 21in " + str(i)) #DONT REMOVE USED in exec
                sliding_insert_24in = self.assembly.get_prompt("Sliding Insert 24in " + str(i)) #DONT REMOVE USED in exec
                velvet_liner = self.assembly.get_prompt("Velvet Liner " + str(i)) #DONT REMOVE USED in exec
                insert_placement_x = self.assembly.get_prompt("Insert Placement X " + str(i))
                insert_placement_y = self.assembly.get_prompt("Insert Placement Y " + str(i))

                if props.closet_defaults.use_32mm_system:
                    if drawer_height:
                        if dovetail_drawer:
                            exec("drawer_height.set_value(float(self.drawer_" + str(i) + "_height))")
                            # If it is a three hole dovetail drawer, force it to be a 4 hole dovetail drawer
                            if dovetail_drawer.get_value() and drawer_height.get_value() <= 91.948:
                                exec("self.drawer_" + str(i) + "_height =  str(123.952)")
                        exec("drawer_height.set_value(sn_unit.inch(float(self.drawer_" + str(i) + "_height) / 25.4))")
                    if bottom_offset:
                        bottom_offset.set_value(sn_unit.inch(float(self.bottom_offset)/25.4))
                if slide_type:
                    exec("slide_type.set_value(self.drawer_" + str(i) + "_slide)")
                if file_rail_type:
                    self.update_file_rail_type(i)
                if file_rail_direction:
                    exec(f"file_rail_type.set_value(int(self.file_rail_type_{str(i)}))")
                if has_jewelry_insert:
                    exec(f"has_jewelry_insert.set_value(self.has_jewelry_insert_{str(i)})")
                if has_sliding_insert:
                    exec(f"has_sliding_insert.set_value(self.has_sliding_insert_{str(i)})")
                if jewelry_insert_type:
                    exec(f"jewelry_insert_type.set_value(int(self.jewelry_insert_type_{str(i)}))")
                if jewelry_insert_18in:
                    exec(f"jewelry_insert_18in.set_value(int(self.jewelry_insert_18in_{str(i)}))")
                if jewelry_insert_21in:
                    exec(f"jewelry_insert_21in.set_value(int(self.jewelry_insert_21in_{str(i)}))")
                if jewelry_insert_24in:
                    exec(f"jewelry_insert_24in.set_value(int(self.jewelry_insert_24in_{str(i)}))")
                if upper_jewelry_insert_velvet_liner_18_in:
                    exec(f"upper_jewelry_insert_velvet_liner_18_in.set_value(int(self.upper_jewelry_insert_velvet_liner_18in_{str(i)}))")
                if upper_jewelry_insert_velvet_liner_21_in:
                    exec(f"upper_jewelry_insert_velvet_liner_21_in.set_value(int(self.upper_jewelry_insert_velvet_liner_21in_{str(i)}))")
                if upper_jewelry_insert_velvet_liner_24_in:
                    exec(f"upper_jewelry_insert_velvet_liner_24_in.set_value(int(self.upper_jewelry_insert_velvet_liner_24in_{str(i)}))")
                if lower_jewelry_insert_velvet_liner_18_in:
                    exec(f"lower_jewelry_insert_velvet_liner_18_in.set_value(int(self.lower_jewelry_insert_velvet_liner_18in_{str(i)}))")
                if lower_jewelry_insert_velvet_liner_21_in:
                    exec(f"lower_jewelry_insert_velvet_liner_21_in.set_value(int(self.lower_jewelry_insert_velvet_liner_21in_{str(i)}))")
                if lower_jewelry_insert_velvet_liner_24_in:
                    exec(f"lower_jewelry_insert_velvet_liner_24_in.set_value(int(self.lower_jewelry_insert_velvet_liner_24in_{str(i)}))")
                if sliding_insert_18in:
                    exec(f"sliding_insert_18in.set_value(int(self.sliding_insert_18in_{str(i)}))")
                if sliding_insert_21in:
                    exec(f"sliding_insert_21in.set_value(int(self.sliding_insert_21in_{str(i)}))")
                if sliding_insert_24in:
                    exec(f"sliding_insert_24in.set_value(int(self.sliding_insert_24in_{str(i)}))")
                if velvet_liner:
                    exec(f"velvet_liner.set_value(int(self.velvet_liner_{str(i)}))")
                if insert_placement_x:
                    exec(f"insert_placement_x.set_value(int(self.insert_placement_x_{str(i)}))")
                if insert_placement_y:
                    exec(f"insert_placement_y.set_value(int(self.insert_placement_y_{str(i)}))")
                

                self.update_lock(i)
                self.update_dbl_drawer_box(i)

            self.update_kd_shelf()

        self.assign_mirror_material(self.assembly.obj_bp)
        bpy.ops.snap.update_scene_from_pointers()
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        closet_props.update_render_materials(self, context)

        self.assembly.obj_bp.select_set(True)

        print("{} : Check Time --- {} seconds ---".format(
            self.bl_idname,
            round(time.perf_counter() - start_time, 8)))
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
        
        slide_type = self.assembly.get_prompt("Slide Type")
        sidemount_options = self.assembly.get_prompt("Sidemount Options")
        undermount_options = self.assembly.get_prompt("Undermount Options")
        use_dovetail_drawer = self.assembly.get_prompt("Use Dovetail Drawer")
        slide_prompts = [slide_type, sidemount_options, undermount_options, use_dovetail_drawer]
        if all(slide_prompts):
            self.slide_type = SLIDE_TYPE[slide_type.get_value()][0]
            self.sidemount_options = SIDEMOUNT_OPTIONS[sidemount_options.get_value()][0]
            self.undermount_options = UNDERMOUNT_OPTIONS[undermount_options.get_value()][0]
            self.set_default_slide = use_dovetail_drawer.get_value()


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
                has_jewelry_insert = self.assembly.get_prompt(f"Has Jewelry Insert {str(i)}")
                has_sliding_insert = self.assembly.get_prompt(f"Has Sliding Insert {str(i)}")
                jewelry_insert_type = self.assembly.get_prompt(f"Jewelry Insert Type {str(i)}") #DONT REMOVE USED in exec
                jewelry_insert_18in = self.assembly.get_prompt(f"Jewelry Insert 18in {str(i)}") #DONT REMOVE USED in exec
                jewelry_insert_21in = self.assembly.get_prompt(f"Jewelry Insert 21in {str(i)}") #DONT REMOVE USED in exec
                jewelry_insert_24in = self.assembly.get_prompt(f"Jewelry Insert 24in {str(i)}") #DONT REMOVE USED in exec
                upper_jewelry_insert_velvet_liner_18in = self.assembly.get_prompt(f"Upper Jewelry Insert Velvet Liner 18in {str(i)}") #DONT REMOVE USED in exec
                upper_jewelry_insert_velvet_liner_21in = self.assembly.get_prompt(f"Upper Jewelry Insert Velvet Liner 21in {str(i)}") #DONT REMOVE USED in exec
                upper_jewelry_insert_velvet_liner_24in = self.assembly.get_prompt(f"Upper Jewelry Insert Velvet Liner 24in {str(i)}") #DONT REMOVE USED in exec
                lower_jewelry_insert_velvet_liner_18in = self.assembly.get_prompt(f"Lower Jewelry Insert Velvet Liner 18in {str(i)}") #DONT REMOVE USED in exec
                lower_jewelry_insert_velvet_liner_21in = self.assembly.get_prompt(f"Lower Jewelry Insert Velvet Liner 21in {str(i)}") #DONT REMOVE USED in exec
                lower_jewelry_insert_velvet_liner_24in = self.assembly.get_prompt(f"Lower Jewelry Insert Velvet Liner 24in {str(i)}") #DONT REMOVE USED in exec
                sliding_insert_18in = self.assembly.get_prompt(f"Sliding Insert 18in {str(i)}") #DONT REMOVE USED in exec
                sliding_insert_21in = self.assembly.get_prompt(f"Sliding Insert 21in {str(i)}") #DONT REMOVE USED in exec
                sliding_insert_24in = self.assembly.get_prompt(f"Sliding Insert 24in {str(i)}") #DONT REMOVE USED in exec
                velvet_liner = self.assembly.get_prompt(f"Velvet Liner {str(i)}") #DONT REMOVE USED in exec
                insert_placement_x = self.assembly.get_prompt(f"Insert Placement X {str(i)}") #DONT REMOVE USED in exec
                insert_placement_y = self.assembly.get_prompt(f"Insert Placement Y {str(i)}") #DONT REMOVE USED in exec

                if lock_drawer and file_rail_type and file_rail_direction:
                    exec("self.lock_" + str(i) + "_drawer = LOCK_DRAWER_TYPES[lock_drawer.get_value()][0]")
                    exec("self.file_rail_type_" + str(i) + " = FILE_RAIL_TYPES[file_rail_type.get_value()][0]")
                    exec("self.file_rail_direction_" + str(i) + " = FILE_DIRECTION_TYPES[file_rail_direction.get_value()][0]")

                if props.closet_defaults.use_32mm_system: 
                    if drawer_height:
                        value = str(round(drawer_height.distance_value * 1000,4))
                        if value in self.front_heights:
                            exec("self.drawer_" + str(i) + "_height = value")
                
                if has_jewelry_insert:
                    exec(f"self.has_jewelry_insert_{str(i)} = has_jewelry_insert.get_value()")
                
                if has_sliding_insert:
                    exec(f"self.has_sliding_insert_{str(i)} = has_sliding_insert.get_value()")

                if jewelry_insert_type:
                    exec(f"self.jewelry_insert_type_{str(i)} = common_lists.JEWELRY_TYPE_OPTIONS[jewelry_insert_type.get_value()][0]")

                if jewelry_insert_18in:
                    exec(f"self.jewelry_insert_18in_{str(i)} = common_lists.JEWELRY_INSERTS_18IN_OPTIONS[jewelry_insert_18in.get_value()][0]")

                if jewelry_insert_21in:
                    exec(f"self.jewelry_insert_21in_{str(i)} = common_lists.JEWELRY_INSERTS_21IN_OPTIONS[jewelry_insert_21in.get_value()][0]")

                if jewelry_insert_24in:
                    exec(f"self.jewelry_insert_24in_{str(i)} = common_lists.JEWELRY_INSERTS_24IN_OPTIONS[jewelry_insert_24in.get_value()][0]")

                if upper_jewelry_insert_velvet_liner_18in:
                    exec(f"self.upper_jewelry_insert_velvet_liner_18in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS[upper_jewelry_insert_velvet_liner_18in.get_value()][0]")

                if upper_jewelry_insert_velvet_liner_21in:
                    exec(f"self.upper_jewelry_insert_velvet_liner_21in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS[upper_jewelry_insert_velvet_liner_21in.get_value()][0]")

                if upper_jewelry_insert_velvet_liner_24in:
                    exec(f"self.upper_jewelry_insert_velvet_liner_24in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS[upper_jewelry_insert_velvet_liner_24in.get_value()][0]")
                
                if lower_jewelry_insert_velvet_liner_18in:
                    exec(f"self.lower_jewelry_insert_velvet_liner_18in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS[lower_jewelry_insert_velvet_liner_18in.get_value()][0]")

                if lower_jewelry_insert_velvet_liner_21in:
                    exec(f"self.lower_jewelry_insert_velvet_liner_21in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS[lower_jewelry_insert_velvet_liner_21in.get_value()][0]")

                if lower_jewelry_insert_velvet_liner_24in:
                    exec(f"self.lower_jewelry_insert_velvet_liner_24in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS[lower_jewelry_insert_velvet_liner_24in.get_value()][0]")

                if sliding_insert_18in:
                    exec(f"self.sliding_insert_18in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS[sliding_insert_18in.get_value()][0]")

                if sliding_insert_21in:
                    exec(f"self.sliding_insert_21in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS[sliding_insert_21in.get_value()][0]")

                if sliding_insert_24in:
                    exec(f"self.sliding_insert_24in_{str(i)} = common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS[sliding_insert_24in.get_value()][0]")

                if velvet_liner:
                    exec(f"self.velvet_liner_{str(i)} = common_lists.VELVET_LINERS_OPTIONS[velvet_liner.get_value()][0]")

                if insert_placement_x:
                    exec(f"self.insert_placement_x_{str(i)} = common_lists.PLACEMENT_OPTIONS_X[insert_placement_x.get_value()][0]")

                if insert_placement_y:
                    exec(f"self.insert_placement_y_{str(i)} = common_lists.PLACEMENT_OPTIONS_Y[insert_placement_y.get_value()][0]")


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
        bp = sn_utils.get_drawer_stack_bp(obj)
        self.assembly = Drawer_Stack(bp)

        # Get drawer front prompts obj
        for child in self.assembly.obj_bp.children:
            if "OBJ_PROMPTS_Drawer_Fronts" in child.name:
                self.drawer_front_ppt_obj = child

        # we want to use the object below's top kd as our bottom kd
        if bp and bp.parent:
            parent_assembly = sn_types.Assembly(bp.parent)
            if bp.parent.sn_closets and hasattr(bp.parent.sn_closets, 'opening_name') and 'Section' in bp.parent.name:
                self.kd_prompt = parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + bp.parent.sn_closets.opening_name)
            else:
                self.kd_prompt = parent_assembly.get_prompt('Remove Top Shelf')
                if not self.kd_prompt:
                    self.kd_prompt = self.assembly.get_prompt('Remove Bottom Shelf')

        else:
            self.kd_prompt = None

        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=700)
    
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
                has_jewelry_insert = self.assembly.get_prompt("Has Jewelry Insert " + str(i))
                has_sliding_insert = self.assembly.get_prompt("Has Sliding Insert " + str(i))
                jewelry_insert_type = self.assembly.get_prompt("Jewelry Insert Type " + str(i))
                extra_deep_drawer_box = self.assembly.get_prompt("Extra Deep Drawer Box")
                is_dbl_jwl = use_double_drawer.get_value()
                has_jwl_ins = has_jewelry_insert.get_value()
                has_sld_ins = has_sliding_insert.get_value()
                drw_H = round(sn_unit.meter_to_millimeter(
                                drawer_height.get_value()), 3)
                f4H = float(common_lists.FRONT_HEIGHTS[1][0])
                f5H = float(common_lists.FRONT_HEIGHTS[2][0])
                f6H = float(common_lists.FRONT_HEIGHTS[3][0])
                f7H = float(common_lists.FRONT_HEIGHTS[4][0])
                # If drawer is changed from 6H to 7H it resets existing 
                # options
                if drw_H == f7H and has_jwl_ins:
                    drawer_7_height = '219.964'
                    exec(f"self.has_jewelry_insert_{str(i)} = False")
                    exec("self.drawer_" + str(i) + "_height = drawer_7_height")
                if(drawer_height and lock_drawer and file_rail_type and file_rail_direction and use_file_rail and extra_deep_drawer_box):
                    if(self.assembly.obj_y.location.y<=extra_deep_drawer_box.get_value()):
                        drawer_box_rear_gap = self.assembly.get_prompt("Standard Drawer Rear Gap")
                    else:
                        drawer_box_rear_gap = self.assembly.get_prompt("Deep Drawer Rear Gap")

                    width = self.assembly.obj_x.location.x - sn_unit.inch(2)
                    depth = self.assembly.obj_y.location.y - drawer_box_rear_gap.get_value()
                    letter = sn_unit.inch(12.5)
                    legal = sn_unit.inch(15.5)
                    # Appears for an existing Double Jewelry Drawer
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
                                velvet_depth = 16
                                width_metric = self.assembly.obj_x.location.x
                                width_in = round(
                                    sn_unit.meter_to_inch(width_metric), 1)
                                depth_metric = self.assembly.obj_y.location.y
                                depth_in = round(
                                    sn_unit.meter_to_inch(depth_metric), 1)
                                velvet = depth_in < velvet_depth
                                jwlry_ins = depth_in >= velvet_depth
                                
                                has_ji_ins = has_jewelry_insert.get_value()
                                db_jwl_conditions = (drw_H == f7H or drw_H == f6H) and depth_in <= 24 and width_in <= 33
                                if not has_ji_ins and not has_jwl_ins and db_jwl_conditions:
                                    if not has_sld_ins:
                                        col_3 = row.column(align=True)
                                        col_3.label(text="Double Jewelry Drawer")
                                        col_3.prop(use_double_drawer,"checkbox_value",text="")
                                    col_4 = row.column(align=True)
                                    # Double Jewelry option
                                    if is_dbl_jwl and jwlry_ins and width_in >= 18 and width_in < 21 and not has_sld_ins:
                                        exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[0][0]')
                                        # These are the options from
                                        # JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS
                                        velvet_options = [3,5,6]
                                        placement_options = [1,2]
                                        upper_chosen_insert = self.assembly.get_prompt(
                                            f'Upper Jewelry Insert Velvet Liner 18in {i}').get_value()
                                        lower_chosen_insert = self.assembly.get_prompt(
                                            f'Lower Jewelry Insert Velvet Liner 18in {i}').get_value()
                                        is_upper_velvet = upper_chosen_insert in velvet_options
                                        is_lower_velvet = lower_chosen_insert in velvet_options
                                        is_upper_placement = upper_chosen_insert in placement_options
                                        is_lower_placement = lower_chosen_insert in placement_options
                                        any_placement = is_upper_placement or is_lower_placement
                                        col_4.label(text=f'Upper Jewelry Insert')
                                        col_4.prop(self,f'upper_jewelry_insert_velvet_liner_18in_{i}',text="")
                                        col_4.label(text=f'Lower Jewelry Insert')
                                        col_4.prop(self,f'lower_jewelry_insert_velvet_liner_18in_{i}',text="")
                                        if (width_in != 18 or depth_in > 16) and any_placement:
                                            col_5 = row.column(align=True)
                                            explain = ''
                                            if is_upper_placement and is_lower_placement:
                                                explain = '- (Both)'
                                            elif is_lower_placement and not is_upper_placement:
                                                explain = '- (Lower)'
                                            elif is_upper_placement and not is_lower_placement:
                                                explain = '- (Upper)'
                                            col_5.label(text=f'Placement {explain}')
                                            if width_in != 18:
                                                col_5.prop(self,f'insert_placement_x_{i}',text="")
                                            if depth_in > 16:
                                                col_5.prop(self,f'insert_placement_y_{i}',text="")
                                    elif is_dbl_jwl and jwlry_ins and width_in >= 21 and width_in < 24 and not has_sld_ins:
                                        exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[0][0]')
                                        # These are the options from
                                        # JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS
                                        velvet_options = [5,6,7]
                                        placement_options = [1,2,3,4]
                                        upper_chosen_insert = self.assembly.get_prompt(
                                            f'Upper Jewelry Insert Velvet Liner 21in {i}').get_value()
                                        lower_chosen_insert = self.assembly.get_prompt(
                                            f'Lower Jewelry Insert Velvet Liner 21in {i}').get_value()
                                        is_upper_velvet = upper_chosen_insert in velvet_options
                                        is_lower_velvet = lower_chosen_insert in velvet_options
                                        is_upper_placement = upper_chosen_insert in placement_options
                                        is_lower_placement = lower_chosen_insert in placement_options
                                        any_placement = is_upper_placement or is_lower_placement
                                        col_4.label(text=f'Upper Jewelry Insert')
                                        col_4.prop(self,f'upper_jewelry_insert_velvet_liner_21in_{i}',text="")
                                        col_4.label(text=f'Lower Jewelry Insert')
                                        col_4.prop(self,f'lower_jewelry_insert_velvet_liner_21in_{i}',text="")
                                        if (width_in != 21 or depth_in > 16) and any_placement:
                                            col_5 = row.column(align=True)
                                            explain = ''
                                            if is_upper_placement and is_lower_placement:
                                                explain = '- (Both)'
                                            elif is_lower_placement and not is_upper_placement:
                                                explain = '- (Lower)'
                                            elif is_upper_placement and not is_lower_placement:
                                                explain = '- (Upper)'
                                            col_5.label(text=f'Placement {explain}')
                                            if width_in != 21:
                                                col_5.prop(self,f'insert_placement_x_{i}',text="")
                                            if depth_in > 16:
                                                col_5.prop(self,f'insert_placement_y_{i}',text="")
                                    elif is_dbl_jwl and jwlry_ins and width_in >= 24 and not has_sld_ins:
                                        exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[0][0]')
                                        # These are the options from
                                        # JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS
                                        velvet_options = [5,6,7]
                                        placement_options = [1,2,3,4]
                                        upper_chosen_insert = self.assembly.get_prompt(
                                            f'Upper Jewelry Insert Velvet Liner 24in {i}').get_value()
                                        lower_chosen_insert = self.assembly.get_prompt(
                                            f'Lower Jewelry Insert Velvet Liner 24in {i}').get_value()
                                        is_upper_velvet = upper_chosen_insert in velvet_options
                                        is_lower_velvet = lower_chosen_insert in velvet_options
                                        is_upper_placement = upper_chosen_insert in placement_options
                                        is_lower_placement = lower_chosen_insert in placement_options
                                        any_placement = is_upper_placement or is_lower_placement
                                        col_4.label(text=f'Upper Jewelry Insert')
                                        col_4.prop(self,f'upper_jewelry_insert_velvet_liner_24in_{i}',text="")
                                        col_4.label(text=f'Lower Jewelry Insert')
                                        col_4.prop(self,f'lower_jewelry_insert_velvet_liner_24in_{i}',text="")
                                        if (width_in != 24 or depth_in > 16) and any_placement:
                                            col_5 = row.column(align=True)
                                            explain = ''
                                            if is_upper_placement and is_lower_placement:
                                                explain = '- (Both)'
                                            elif is_lower_placement and not is_upper_placement:
                                                explain = '- (Lower)'
                                            elif is_upper_placement and not is_lower_placement:
                                                explain = '- (Upper)'
                                            col_5.label(text=f'Placement {explain}')
                                            if width_in != 24:
                                                col_5.prop(self,f'insert_placement_x_{i}',text="")
                                            if depth_in > 16:
                                                col_5.prop(self,f'insert_placement_y_{i}',text="")

                        if(drawer_height):
                            velvet_depth = 16
                            non_std_heights = drw_H == f4H or drw_H == f5H or drw_H == f6H
                            not_dbl_drw = not use_double_drawer.get_value()
                            width_metric = self.assembly.obj_x.location.x
                            depth_metric = self.assembly.obj_y.location.y
                            width_in = round(
                                sn_unit.meter_to_inch(width_metric), 1)
                            depth_in = round(
                                sn_unit.meter_to_inch(depth_metric), 1)
                            # Height Checks
                            std_height = drw_H == f6H or drw_H == f5H
                            std_widths = width_in in [18, 21, 24]
                            is_std_opng = std_height and std_widths and depth_in >= 16
                            non_std_jwlry_ins = not is_std_opng and depth_in >= 16 and non_std_heights
                            non_std_velvet = not is_std_opng and depth_in < 16 and non_std_heights
                            velvet = depth_in < velvet_depth
                            jwlry_ins = depth_in >= velvet_depth                            
                            if not is_dbl_jwl and non_std_heights:
                                col_3 = row.column(align=True)
                                col_3.label(text='Jewelry Insert')
                                col_3.prop(self,f'has_jewelry_insert_{i}',text="")
                            if is_std_opng and not is_dbl_jwl:
                                if 24 >= depth_in >= 16:
                                    col_3.label(text='Sliding Insert')
                                    col_3.prop(self,f'has_sliding_insert_{i}',text="")
                                if not_dbl_drw and width_in == 18:
                                    exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[1][0]')
                                    col_4 = row.column(align=True)
                                    if has_jwl_ins:
                                        col_4.label(text='Jewelry Insert')
                                        col_4.prop(self,f'jewelry_insert_18in_{i}',text="")
                                    if has_sld_ins:
                                        col_4.label(text='Sliding Insert')
                                        col_4.prop(self,f'sliding_insert_18in_{i}',text="")
                                    if depth_in > 16 and (has_jwl_ins or has_sld_ins):
                                        col_5 = row.column(align=True)
                                        col_5.label(text='Placement')
                                        col_5.prop(self,f'insert_placement_y_{i}',text="")
                                elif not_dbl_drw and width_in == 21:
                                    exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[1][0]')
                                    col_4 = row.column(align=True)
                                    if has_jwl_ins:
                                        col_4.label(text='Jewelry Insert')
                                        col_4.prop(self,f'jewelry_insert_21in_{i}',text="")
                                    if has_sld_ins:
                                        col_4.label(text='Sliding Insert')
                                        col_4.prop(self,f'sliding_insert_21in_{i}',text="")
                                    if depth_in > 16 and (has_jwl_ins or has_sld_ins):
                                        col_5 = row.column(align=True)
                                        col_5.label(text='Placement')
                                        col_5.prop(self,f'insert_placement_y_{i}',text="")
                                elif not_dbl_drw and width_in == 24:
                                    exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[1][0]')
                                    col_4 = row.column(align=True)
                                    if has_jwl_ins:
                                        col_4.label(text='Jewelry Insert')
                                        col_4.prop(self,f'jewelry_insert_24in_{i}',text="")
                                    if has_sld_ins:
                                        col_4.label(text='Sliding Insert')
                                        col_4.prop(self,f'sliding_insert_24in_{i}',text="")
                                    if depth_in > 16 and (has_jwl_ins or has_sld_ins):
                                        col_5 = row.column(align=True)
                                        col_5.label(text='Placement')
                                        col_5.prop(self,f'insert_placement_y_{i}',text="")
                            elif non_std_jwlry_ins and not non_std_velvet:
                                if not_dbl_drw and depth_in >= 16 and width_in >= 18 and width_in < 21 and has_jwl_ins:
                                    exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[2][0]')
                                    col_4 = row.column(align=True)
                                    col_4.label(text='Jewelry Insert')
                                    col_4.prop(self,f'lower_jewelry_insert_velvet_liner_18in_{i}',text="")
                                    chosen_insert = self.assembly.get_prompt(
                                        f'Lower Jewelry Insert Velvet Liner 18in {i}').get_value()
                                    # These are the options from
                                    # JEWELRY_INSERTS_VELVET_LINERS_18IN_OPTIONS
                                    if chosen_insert == 0:
                                        exec(f'self.lower_jewelry_insert_velvet_liner_18in_{i} = \'1\' ')
                                        chosen_insert = 1
                                    if chosen_insert in [1, 2, 3]:
                                        col_5 = row.column(align=True)
                                        if not std_widths or depth_in > 16:
                                            col_5.label(text='Placement')
                                        if not std_widths:
                                            col_5.prop(self,f'insert_placement_x_{i}',text="")
                                        if depth_in > 16:
                                            col_5.prop(self,f'insert_placement_y_{i}',text="")
                                elif not_dbl_drw and depth_in >= 16 and width_in >= 21 and width_in < 24 and has_jwl_ins:
                                    exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[2][0]')
                                    col_4 = row.column(align=True)
                                    col_4.label(text='Jewelry Insert')
                                    col_4.prop(self,f'lower_jewelry_insert_velvet_liner_21in_{i}',text="")
                                    chosen_insert = self.assembly.get_prompt(
                                        f'Lower Jewelry Insert Velvet Liner 21in {i}').get_value()
                                    # These are the options from
                                    # JEWELRY_INSERTS_VELVET_LINERS_21IN_OPTIONS
                                    if chosen_insert == 0:
                                        exec(f'self.lower_jewelry_insert_velvet_liner_21in_{i} = \'1\' ')
                                        chosen_insert = 1
                                    if chosen_insert in [1, 2, 3, 4]:
                                        col_5 = row.column(align=True)
                                        if not std_widths or depth_in > 16:
                                            col_5.label(text='Placement')
                                        if not std_widths:
                                            col_5.prop(self,f'insert_placement_x_{i}',text="")
                                        if depth_in > 16:
                                            col_5.prop(self,f'insert_placement_y_{i}',text="")
                                elif not_dbl_drw and depth_in >= 16 and width_in >= 24 and has_jwl_ins:
                                    exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[2][0]')
                                    col_4 = row.column(align=True)
                                    col_4.label(text='Jewelry Insert')
                                    col_4.prop(self,f'lower_jewelry_insert_velvet_liner_24in_{i}',text="")
                                    chosen_insert = self.assembly.get_prompt(
                                        f'Lower Jewelry Insert Velvet Liner 24in {i}').get_value()
                                    # These are the options from
                                    # JEWELRY_INSERTS_VELVET_LINERS_24IN_OPTIONS
                                    if chosen_insert == 0:
                                        exec(f'self.lower_jewelry_insert_velvet_liner_24in_{i} = \'1\' ')
                                        chosen_insert = 1
                                    if chosen_insert in [1, 2, 3, 4]:
                                        col_5 = row.column(align=True)
                                        if not std_widths or depth_in > 16:
                                            col_5.label(text='Placement')
                                        if not std_widths:
                                            col_5.prop(self,f'insert_placement_x_{i}',text="")
                                        if depth_in > 16:
                                            col_5.prop(self,f'insert_placement_y_{i}',text="")
                            elif has_jwl_ins and not_dbl_drw and non_std_velvet:
                                exec(f'self.jewelry_insert_type_{i} = common_lists.JEWELRY_TYPE_OPTIONS[3][0]')
                                col_4 = row.column(align=True)
                                col_4.label(text=f'Velvet Liner')
                                col_4.prop(self,f'velvet_liner_{i}',text="")
        
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

    # def is_glass_front(self):
    #     if "Glass" in self.part.obj_bp.snap.comment:
    #         return True
    #     else:
    #         return False

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                if self.drawer_qty_prompt:
                    open_drawer = self.assembly.get_prompt('Open')
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
                    use_dovetail_drawer = self.assembly.get_prompt("Use Dovetail Drawer")
                    add_drawer_boxes_ppt = self.assembly.get_prompt("Add Drawer Boxes")

                    box = layout.box()
                    propbox = box.box()
                    propbox.label(text="Options:", icon='SCRIPT')

                    row = propbox.row()
                    if use_dovetail_drawer:
                        if use_dovetail_drawer.get_value():
                            row.label(text="Minimum Drawer Rear Gap")
                        else:
                            row.label(text="Drawer Rear Gap")
                    else:
                        row.label(text="Drawer Rear Gap")

                    if extra_deep_drawer_box and standard_drawer_rear_gap and deep_drawer_rear_gap:
                        if(drawer_depth <= extra_deep_drawer_box.get_value()):
                            row.prop(standard_drawer_rear_gap, "distance_value", text="")
                        else:
                            row.prop(deep_drawer_rear_gap, "distance_value", text="")

                    row = propbox.row()
                    if cleat_loc:
                        row.label(text="Cleat Location")
                        row.prop(self, "cleat_location", expand=True)

                    row = propbox.row()
                    if lift_drawers_from_bottom:
                        row.prop(lift_drawers_from_bottom, "checkbox_value", text="Suspended Drawers")

                    if lift_drawers_from_bottom.get_value():
                        row.prop(self,'bottom_offset')

                    row = propbox.row()
                    if use_double_pulls:
                        row.prop(use_double_pulls, "checkbox_value", text=use_double_pulls.name)
                    if no_pulls:
                        row.prop(no_pulls, "checkbox_value", text=no_pulls.name)
                    
                    row = propbox.row()
                    if remove_top_shelf:
                        row.prop(remove_top_shelf,"checkbox_value",text="Top KD")
                    parent_assembly = sn_types.Assembly(self.assembly.obj_bp.parent)

                    if lift_drawers_from_bottom.get_value():
                        bottom_shelf = self.assembly.get_prompt('Remove Bottom Shelf')
                        row.prop(bottom_shelf, "checkbox_value", text="Bottom KD")
                    elif self.kd_prompt:
                        row.prop(self.kd_prompt, "checkbox_value", text="Bottom KD")
                    if full_overlay:
                        row = propbox.row()
                        row.prop(full_overlay, "checkbox_value", text="Full Overlay")

                    if use_dovetail_drawer:
                        row = propbox.row()
                        row.prop(use_dovetail_drawer, "checkbox_value", text="Dovetail Drawer")

                    row = propbox.row()
                    row.prop(add_drawer_boxes_ppt, "checkbox_value", text="Open Drawers")

                    propbox = box.box()
                    row = propbox.row()
                    column_1 = row.column()
                    column_1.label(text="Slide Type")
                    if use_dovetail_drawer:
                        if use_dovetail_drawer.get_value():
                            column_1.prop(self, "slide_type", text="")
                        else:
                            column_1.label(text="Sidemount")
                    else:
                        column_1.label(text="Sidemount")
                    column_2 = row.column()

                    if self.slide_type == '0':
                        column_2.label(text="Sidemount Options")
                        column_2.prop(self, "sidemount_options", text="")
                    else:
                        column_2.label(text="Undermount Options")
                        column_2.prop(self, "undermount_options", text="")

                    self.draw_drawer_heights(box)


class OPS_Drawer_Drop(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.insert_drawer_drop"
    bl_label = "Custom drag and drop for drawers insert"
    adjacent_cant_be_deeper = True
    
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
        parent_bp = insert_bp.parent
        if(above_hamper_or_base_door):
            if(parent_bp.get("IS_BP_DOOR_INSERT")):
                door_assembly = sn_types.Assembly(parent_bp)
                door_type = door_assembly.get_prompt("Door Type")
                if(door_type):
                    if(door_type.get_value() == 0):
                        above_hamper_or_base_door.set_value(True)
            elif(parent_bp.get("IS_BP_HAMPER")):
                above_hamper_or_base_door.set_value(True)

    def set_bottom_KD(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.sn_closets.opening_name
        if insert_bp and insert_bp.parent:
            # if the object is the carcass, we use the bottom. else, we use the top kd
            parent_assembly = sn_types.Assembly(insert_bp.parent)
            insert_assembly = sn_types.Assembly(insert_bp)
            if insert_bp.parent.sn_closets and hasattr(insert_bp.parent.sn_closets, 'opening_name') and 'Section' in insert_bp.parent.name:
                parent_assembly.get_prompt('Remove Bottom Hanging Shelf ' + opening_name).set_value(True)
            else:
                prompt = parent_assembly.get_prompt('Remove Top Shelf')
                if prompt:
                    prompt.set_value(True)
                else:
                    insert_assembly.get_prompt('Remove Bottom Shelf').set_value(True)


bpy.utils.register_class(PROMPTS_Drawer_Prompts)
bpy.utils.register_class(OPS_Drawer_Drop)
