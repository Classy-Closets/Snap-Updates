import math

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, EnumProperty

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts


class Flat_Molding(sn_types.Assembly):
    """Flat molding"""

    type_assembly = "PRODUCT"
    id_prompt = "sn_closets.prompts_flat_molding"
    drop_id = "sn_closets.top_drop"
    show_in_library = True

    library_name = ""
    category_name = ""

    def add_prompts(self):
        self.add_prompt("Extend To Left Panel", 'CHECKBOX', True)
        self.add_prompt("Extend To Right Panel", 'CHECKBOX', True)
        self.add_prompt("Exposed Left", 'CHECKBOX', True)
        self.add_prompt("Exposed Right", 'CHECKBOX', True)
        self.add_prompt("Exposed Back", 'CHECKBOX', True)
        self.add_prompt("Return Left", 'CHECKBOX', False)
        self.add_prompt("Return Right", 'CHECKBOX', False)
        self.add_prompt("Extend Left Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Extend Right Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Front Overhang", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Molding Height", 'DISTANCE', sn_unit.inch(3))
        self.add_prompt("Molding Location", 'DISTANCE', sn_unit.inch(-24))
        self.add_prompt('Layered Crown', 'CHECKBOX', False)
        self.add_prompt('Layers', 'COMBOBOX', 0, ['1', '2'])
        common_prompts.add_thickness_prompts(self)

    def update(self):
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth
        self.obj_z.location.z = self.height

        # TODO: remove
        props = self.obj_bp.sn_closets
        props.is_crown_molding = True

        self.obj_bp["IS_BP_CROWN_MOLDING"] = True
        self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.obj_bp["ID_DROP"] = self.drop_id
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.obj_bp.snap.export_as_subassembly = False
        self.set_prompts()
        super().update()

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.add_prompts()

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Extend_Left = self.get_prompt('Extend To Left Panel').get_var('Extend_Left')        
        Extend_Right = self.get_prompt('Extend To Right Panel').get_var('Extend_Right')      
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        Extend_Left_Amount = self.get_prompt('Extend Left Amount').get_var()
        Extend_Right_Amount = self.get_prompt('Extend Right Amount').get_var()
        Front_Overhang = self.get_prompt('Front Overhang').get_var()
        Return_Left = self.get_prompt('Return Left').get_var()
        Return_Right = self.get_prompt('Return Right').get_var()
        Exposed_Left = self.get_prompt('Exposed Left').get_var()
        Exposed_Right = self.get_prompt('Exposed Right').get_var()
        Exposed_Back = self.get_prompt('Exposed Back').get_var()
        Molding_Height = self.get_prompt('Molding Height').get_var()
        Molding_Location = self.get_prompt('Molding Location').get_var()

        flat_crown = common_parts.add_flat_crown(self)
        flat_crown.obj_bp.snap.comment_2 = "1040"
        flat_crown.set_name("Flat Valance")
        flat_crown.loc_x(
            'IF(Extend_Left,0,Panel_Thickness/2)-Extend_Left_Amount',
            [Extend_Left, Extend_Left_Amount, Panel_Thickness])
        flat_crown.loc_y('-Depth-Front_Overhang+Panel_Thickness',
                         [Depth, Front_Overhang, Panel_Thickness])
        flat_crown.loc_z('Molding_Location', [Molding_Location])
        flat_crown.rot_x(value=math.radians(-90))
        flat_crown.dim_x(
            'Width'
            '-IF(Extend_Left,0,Panel_Thickness/2)'
            '-IF(Extend_Right,0,Panel_Thickness/2)'
            '+Extend_Left_Amount'
            '+Extend_Right_Amount',
            [Width, Extend_Left, Extend_Right, Panel_Thickness,
             Extend_Right_Amount, Extend_Left_Amount])
        flat_crown.dim_y('Molding_Height', [Molding_Height])
        flat_crown.dim_z('-Panel_Thickness', [Panel_Thickness])
        flat_crown.get_prompt('Exposed Left').set_formula('Exposed_Left', [Exposed_Left])
        flat_crown.get_prompt('Exposed Left').set_formula('Exposed_Right', [Exposed_Right])
        flat_crown.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])

        left_return = common_parts.add_cleat(self)
        left_return.obj_bp.snap.comment_2 = "1040"
        left_return.set_name("Left")
        left_return.loc_x('Panel_Thickness-Extend_Left_Amount', [Panel_Thickness, Extend_Left_Amount])
        left_return.loc_y('-Depth-Front_Overhang+Panel_Thickness', [Depth, Front_Overhang, Panel_Thickness])
        left_return.loc_z('Molding_Location-Molding_Height', [Molding_Location, Molding_Height])
        left_return.rot_x(value=math.radians(90))
        left_return.rot_z(value=math.radians(90))
        left_return.dim_x('Depth-Panel_Thickness+Front_Overhang', [Depth, Panel_Thickness, Front_Overhang])
        left_return.dim_y('Molding_Height', [Molding_Height])
        left_return.dim_z('-Panel_Thickness', [Panel_Thickness])
        left_return.get_prompt('Hide').set_formula('IF(Return_Left,False,True) or Hide', [Return_Left,self.hide_var])

        right_return = common_parts.add_cleat(self)
        right_return.obj_bp.snap.comment_2 = "1040"
        right_return.set_name("Right")
        right_return.loc_x('Width+Extend_Right_Amount', [Width, Extend_Right_Amount])
        right_return.loc_y('-Depth-Front_Overhang+Panel_Thickness', [Depth, Front_Overhang, Panel_Thickness])
        right_return.loc_z('Molding_Location-Molding_Height', [Molding_Location, Molding_Height])
        right_return.rot_x(value=math.radians(90))
        right_return.rot_z(value=math.radians(90))
        right_return.dim_x('Depth-Panel_Thickness+Front_Overhang', [Depth, Panel_Thickness, Front_Overhang])
        right_return.dim_y('Molding_Height', [Molding_Height])
        right_return.dim_z('-Panel_Thickness', [Panel_Thickness])
        right_return.get_prompt('Hide').set_formula('IF(Return_Right,False,True) or Hide', [Return_Right,self.hide_var])

        self.update()


class Flat_Crown(Flat_Molding):

    def update(self):
        super().update()

        # TODO: remove
        props = self.obj_bp.sn_closets
        props.is_flat_crown_bp = True

        self.obj_bp["IS_BP_FLAT_CROWN"] = True
        self.obj_bp.snap.export_as_subassembly = False

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.add_prompts()
        self.add_prompt("Extend To Ceiling", 'CHECKBOX', False)
        self.add_prompt("Distance From Ceiling", 'DISTANCE', 0)
        self.add_prompt("Top KD Holes Down", 'COMBOBOX', 0, ["None", 'One', 'Two'])
        self.add_prompt('Show Layered Molding', 'CHECKBOX', False)
        self.add_prompt('Number of Layers', 'COMBOBOX', 0, ['1', '2'])
        self.add_prompt('Topshelf Exists', 'CHECKBOX', False)

        Show_Layered = self.get_prompt('Show Layered Molding').get_var('Show_Layered')
        Layer_Num = self.get_prompt('Number of Layers').get_var('Layer_Num')

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Extend_Left = self.get_prompt('Extend To Left Panel').get_var('Extend_Left')        
        Extend_Right = self.get_prompt('Extend To Right Panel').get_var('Extend_Right')
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        Extend_Left_Amount = self.get_prompt('Extend Left Amount').get_var()
        Extend_Right_Amount = self.get_prompt('Extend Right Amount').get_var()
        Front_Overhang = self.get_prompt('Front Overhang').get_var()
        Return_Left = self.get_prompt('Return Left').get_var()
        Return_Right = self.get_prompt('Return Right').get_var()
        Exposed_Left = self.get_prompt('Exposed Left').get_var()
        Exposed_Right = self.get_prompt('Exposed Right').get_var()
        Exposed_Back = self.get_prompt('Exposed Back').get_var()
        Molding_Height = self.get_prompt('Molding Height').get_var()
        Molding_Location = self.get_prompt('Molding Location').get_var()
        Topshelf_Exists = self.get_prompt('Topshelf Exists').get_var()

        ETC = self.get_prompt('Extend To Ceiling').get_var('ETC')
        DFC = self.get_prompt('Distance From Ceiling').get_var('DFC')
        TKDHD = self.get_prompt('Top KD Holes Down').get_var('TKDHD')

        flat_crown = common_parts.add_flat_crown(self)
        flat_crown.obj_bp.snap.comment_2 = "1038"
        flat_crown.set_name("Flat Crown")
        flat_crown.loc_x(
            'IF(Return_Left,-Panel_Thickness+' + str(sn_unit.millimeter(0.1)) + ',0)'
            '-Extend_Left_Amount',
            [Extend_Left, Extend_Left_Amount, Panel_Thickness, Return_Left])
        flat_crown.loc_y('-Depth-Front_Overhang+IF(Show_Layered,INCH(3.64)-INCH(0.75),0)', [Depth, Front_Overhang, Show_Layered, Molding_Height])
        flat_crown.loc_z('IF(Show_Layered,IF(Topshelf_Exists,INCH(0.75),0),IF(ETC,DFC,Molding_Height+Molding_Location))', [Molding_Height, Molding_Location, ETC, DFC, Show_Layered, Topshelf_Exists])
        flat_crown.rot_x(expression='IF(Show_Layered,radians(-180),radians(-90))', variables=[Show_Layered])

        flat_crown.dim_x(
            'Width+Extend_Left_Amount+Extend_Right_Amount'
            '+IF(Return_Right,Panel_Thickness-' + str(sn_unit.millimeter(0.1)) + ',0)'
            '+IF(Return_Left,Panel_Thickness-' + str(sn_unit.millimeter(0.1)) + ',0)',
            [Width, Extend_Left, Extend_Right, Panel_Thickness, Extend_Right_Amount,
             Extend_Left_Amount, Return_Right, Return_Left])
        flat_crown.dim_y('IF(Show_Layered,INCH(3.64),IF(ETC,IF(TKDHD == 1,INCH(1.26),IF(TKDHD == 2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height))',
                         [Molding_Height, ETC, DFC, TKDHD, Show_Layered])
        flat_crown.dim_z('-Panel_Thickness', [Panel_Thickness])
        flat_crown.get_prompt('Exposed Left').set_formula('Exposed_Left', [Exposed_Left])
        flat_crown.get_prompt('Exposed Right').set_formula('Exposed_Right', [Exposed_Right])
        flat_crown.get_prompt('Exposed Front').set_formula('IF(Show_Layered,True, False)', [Show_Layered])
        flat_crown.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])
        flat_crown.get_prompt('Hide').set_formula('Hide', [self.hide_var])
        flat_crown.get_prompt('C1 Miter Inset').set_formula('IF(AND(Show_Layered,Return_Left),INCH(3.64),0)', [Show_Layered, Return_Left])
        flat_crown.get_prompt('C4 Miter Inset').set_formula('IF(AND(Show_Layered,Return_Right),INCH(3.64),0)', [Show_Layered, Return_Right])

        left_return = common_parts.add_flat_crown(self)
        left_return.obj_bp.snap.comment_2 = "1038"
        left_return.set_name("Left")
        left_return.loc_x('-Panel_Thickness-Extend_Left_Amount+IF(Show_Layered,INCH(3.64),0)', [Panel_Thickness, Extend_Left_Amount, Show_Layered, Molding_Height])
        left_return.loc_y(
            '-Depth-Front_Overhang-Panel_Thickness+' + str(sn_unit.millimeter(0.1)) + '',
            [Depth, Front_Overhang, Panel_Thickness])
        left_return.loc_z('IF(Show_Layered,IF(Topshelf_Exists,INCH(0.75),0),IF(ETC,DFC,Molding_Height+Molding_Location))', [Molding_Height, Molding_Location, ETC, DFC, Show_Layered, Topshelf_Exists])
        left_return.rot_x(expression='IF(Show_Layered,0,radians(90))', variables=[Show_Layered])
        left_return.rot_z(value=math.radians(90))
        left_return.dim_x(
            'Depth+Front_Overhang+Panel_Thickness-' + str(sn_unit.millimeter(0.1)) + '',
            [Depth, Panel_Thickness, Front_Overhang])
        left_return.dim_y(
            'IF(Show_Layered,INCH(3.64),IF(ETC,IF(TKDHD == 1,INCH(1.26),IF(TKDHD == 2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height) * -1)',
            [Molding_Height, ETC, DFC, TKDHD, Show_Layered])
        left_return.dim_z('Panel_Thickness', [Panel_Thickness])
        left_return.get_prompt('Hide').set_formula('IF(Return_Left,False,True) or Hide', [Return_Left,self.hide_var])
        #W
        left_return.get_prompt('Exposed Front').set_formula('IF(AND(Show_Layered,Exposed_Left),True, False)', [Show_Layered, Exposed_Left])
        left_return.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])
        left_return.get_prompt('C1 Miter Inset').set_formula('IF(Show_Layered,INCH(3.64),0)', [Show_Layered])

        right_return = common_parts.add_flat_crown(self)
        right_return.obj_bp.snap.comment_2 = "1038"
        right_return.set_name("Right")
        right_return.loc_x('Width+Extend_Right_Amount-IF(Show_Layered,-INCH(0.75)+INCH(3.64),0)', [Width, Extend_Right_Amount, Show_Layered, Molding_Height])
        right_return.loc_y(
            '-Depth-Front_Overhang-Panel_Thickness+' + str(sn_unit.millimeter(0.1)) + '',
            [Depth, Front_Overhang, Panel_Thickness])
        right_return.loc_z('IF(Show_Layered,IF(Topshelf_Exists,INCH(1.5),INCH(0.75)),IF(ETC,DFC,Molding_Height+Molding_Location))', [Molding_Height, Molding_Location, ETC, DFC, Show_Layered, Topshelf_Exists])
        right_return.rot_x(expression='IF(Show_Layered,radians(180),radians(90))', variables=[Show_Layered])
        right_return.rot_z(value=math.radians(90))
        right_return.dim_x(
            'Depth+Front_Overhang+Panel_Thickness-' + str(sn_unit.millimeter(0.1)) + '',
            [Depth, Panel_Thickness, Front_Overhang])
        right_return.dim_y(
            'IF(Show_Layered,INCH(3.64),IF(ETC,IF(TKDHD==1,INCH(1.26),IF(TKDHD==2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height)*-1)',
            [Molding_Height, ETC, DFC, TKDHD, Show_Layered])
        right_return.dim_z('Panel_Thickness', [Panel_Thickness])
        right_return.get_prompt('Hide').set_formula('IF(Return_Right,False,True) or Hide', [Return_Right,self.hide_var])
        right_return.get_prompt('Exposed Front').set_formula('IF(AND(Show_Layered,Exposed_Right),True, False)', [Show_Layered, Exposed_Right])         
        right_return.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])
        right_return.get_prompt('C1 Miter Inset').set_formula('IF(Show_Layered,INCH(3.64),0)', [Show_Layered])

        # # Layered Molding
        flat_crown = common_parts.add_flat_crown(self)
        flat_crown.obj_bp.snap.comment_2 = "1038"
        flat_crown.set_name("Flat Crown")
        flat_crown.loc_x(
            'IF(Return_Left,-(Panel_Thickness*2)+' + str(sn_unit.millimeter(0.1)) + ',0)'
            '-Extend_Left_Amount',
            [Extend_Left, Extend_Left_Amount, Panel_Thickness, Return_Left])
        flat_crown.loc_y('-Depth-Front_Overhang+IF(Show_Layered,INCH(3.64)-INCH(1.5),0)', [Depth, Front_Overhang, Show_Layered, Molding_Height])
        flat_crown.loc_z('IF(Show_Layered,IF(Topshelf_Exists,INCH(1.5),INCH(0.75)),IF(ETC,DFC,Molding_Height+Molding_Location))', [Molding_Height, Molding_Location, ETC, DFC, Show_Layered, Panel_Thickness, Topshelf_Exists])
        flat_crown.rot_x(expression='IF(Show_Layered,radians(-180),radians(-90))', variables=[Show_Layered])
        flat_crown.get_prompt('C1 Miter Inset').set_formula('IF(AND(Show_Layered,Return_Left),INCH(3.64),0)', [Show_Layered, Return_Left])
        flat_crown.get_prompt('C4 Miter Inset').set_formula('IF(AND(Show_Layered,Return_Right),INCH(3.64),0)', [Show_Layered, Return_Right])

        flat_crown.dim_x(
            'Width+Extend_Left_Amount+Extend_Right_Amount'
            '+IF(Return_Right,(Panel_Thickness*2)-' + str(sn_unit.millimeter(0.1)) + ',0)'
            '+IF(Return_Left,(Panel_Thickness*2)-' + str(sn_unit.millimeter(0.1)) + ',0)',
            [Width, Extend_Left, Extend_Right, Panel_Thickness, Extend_Right_Amount,
             Extend_Left_Amount, Return_Right, Return_Left])
        flat_crown.dim_y('IF(Show_Layered,INCH(3.64),IF(ETC,IF(TKDHD == 1,INCH(1.26),IF(TKDHD == 2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height))',
                         [Molding_Height, ETC, DFC, TKDHD, Show_Layered])
        flat_crown.dim_z('-Panel_Thickness', [Panel_Thickness])
        flat_crown.get_prompt('Exposed Left').set_formula('Exposed_Left', [Exposed_Left])
        flat_crown.get_prompt('Exposed Right').set_formula('Exposed_Right', [Exposed_Right])
        flat_crown.get_prompt('Exposed Front').set_formula('IF(Show_Layered,True, False)', [Show_Layered])
        flat_crown.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])
        flat_crown.get_prompt('Hide').set_formula('Hide or Layer_Num==0 or not Show_Layered', [self.hide_var,Layer_Num,Show_Layered])

        left_return = common_parts.add_flat_crown(self)
        left_return.obj_bp.snap.comment_2 = "1038"
        left_return.set_name("Left")
        left_return.loc_x('INCH(3.64)-Panel_Thickness-Extend_Left_Amount+IF(Show_Layered,-INCH(0.75),0)', [Panel_Thickness, Extend_Left_Amount, Show_Layered, Molding_Height])
        left_return.loc_y(
            '-Depth-Front_Overhang-Panel_Thickness+' + str(sn_unit.millimeter(0.1)) + '-INCH(0.75)',
            [Depth, Front_Overhang, Panel_Thickness])
        left_return.loc_z('IF(Show_Layered,IF(Topshelf_Exists,INCH(1.5),INCH(0.75)),IF(ETC,DFC,Molding_Height+Molding_Location))', [Molding_Height, Molding_Location, ETC, DFC, Show_Layered, Topshelf_Exists])
        left_return.rot_x(expression='IF(Show_Layered,radians(0),radians(90))', variables=[Show_Layered])
        left_return.rot_z(value=math.radians(90))
        left_return.dim_x(
            'Depth+Front_Overhang+Panel_Thickness-' + str(sn_unit.millimeter(0.1)) + '+INCH(0.75)',
            [Depth, Panel_Thickness, Front_Overhang])
        left_return.dim_y(
            'IF(Show_Layered,INCH(3.64),IF(ETC,IF(TKDHD == 1,INCH(1.26),IF(TKDHD == 2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height) * -1)',
            [Molding_Height, ETC, DFC, TKDHD, Show_Layered])
        left_return.dim_z('Panel_Thickness', [Panel_Thickness])
        left_return.get_prompt('Hide').set_formula('IF(Return_Left,False,True) or Hide or Layer_Num==0 or not Show_Layered', [Return_Left,self.hide_var,Layer_Num,Show_Layered])
        left_return.get_prompt('Exposed Front').set_formula('IF(AND(Show_Layered,Exposed_Left),True, False)', [Show_Layered, Exposed_Left])
        left_return.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])
        left_return.get_prompt('C1 Miter Inset').set_formula('IF(Show_Layered,INCH(3.64),0)', [Show_Layered])

        right_return = common_parts.add_flat_crown(self)
        right_return.obj_bp.snap.comment_2 = "1038"
        right_return.set_name("Right")
        right_return.loc_x('Width+Extend_Right_Amount-IF(Show_Layered,-INCH(1.5),0)-INCH(3.64)', [Width, Extend_Right_Amount,Show_Layered,Molding_Height])
        right_return.loc_y(
            '-Depth-Front_Overhang-Panel_Thickness+' + str(sn_unit.millimeter(0.1)) + '-INCH(0.75)',
            [Depth, Front_Overhang, Panel_Thickness])
        right_return.loc_z('IF(Show_Layered,IF(Topshelf_Exists,INCH(2.25),INCH(1.5)),IF(ETC,DFC,Molding_Height+Molding_Location))', [Molding_Height, Molding_Location, ETC, DFC, Show_Layered, Panel_Thickness, Topshelf_Exists])
        right_return.rot_x(expression='IF(Show_Layered,radians(180),radians(90))', variables=[Show_Layered])
        right_return.rot_z(value=math.radians(90))
        right_return.dim_x(
            'Depth+Front_Overhang+Panel_Thickness-' + str(sn_unit.millimeter(0.1)) + '+INCH(0.75)',
            [Depth, Panel_Thickness, Front_Overhang])
        right_return.dim_y(
            'IF(Show_Layered,INCH(3.64),IF(ETC,IF(TKDHD==1,INCH(1.26),IF(TKDHD==2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height)*-1)',
            [Molding_Height, ETC, DFC, TKDHD, Show_Layered])
        right_return.dim_z('Panel_Thickness', [Panel_Thickness])
        right_return.get_prompt('Hide').set_formula('IF(Return_Right,False,True) or Hide or Layer_Num==0 or not Show_Layered', [Return_Right,self.hide_var,Layer_Num,Show_Layered])
        right_return.get_prompt('Exposed Front').set_formula('IF(AND(Show_Layered,Exposed_Right),True, False)', [Show_Layered, Exposed_Right])
        right_return.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])
        right_return.get_prompt('C1 Miter Inset').set_formula('IF(Show_Layered,INCH(3.64),0)', [Show_Layered])

        self.update()


class PROMPTS_prompts_flat_molding(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.prompts_flat_molding"
    bl_label = "Flat Crown Prompt"
    bl_options = {'UNDO'}

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)
    layer_num: EnumProperty(name='Number of Layers', items=(('0','1','1'),('1','2','2')))
    TKHD_VAR: EnumProperty(
        name="Top KD Holes Down",
        items=[
            ('0', 'None', 'None'),
            ('1', 'One', 'One'),
            ('2', 'Two', 'Two')],
        default='0'
    )

    insert = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        etc = self.insert.get_prompt("Extend To Ceiling")
        if etc:
            if(self.insert.get_prompt("Molding Height").get_value() < sn_unit.inch(3) or etc.get_value()):
                self.insert.get_prompt("Exposed Back").set_value(False)

        dfc = self.insert.get_prompt("Distance From Ceiling")
        tkdhd = self.insert.get_prompt('Top KD Holes Down')
        if tkdhd:
            tkdhd.set_value(int(self.TKHD_VAR))

        layer_num = self.insert.get_prompt('Number of Layers')
        if layer_num:
            if layer_num.get_value() != float(self.layer_num):
                layer_num.set_value(float(self.layer_num))
        if etc and dfc:
            if etc.get_value():
                wall_bp = sn_utils.get_wall_bp(self.insert.obj_bp)
                wall = sn_types.Assembly(wall_bp)
                closet_bp = sn_utils.get_closet_bp(self.insert.obj_bp)
                closet = sn_types.Assembly(closet_bp)
                if wall.obj_bp:
                    dfc.set_value(wall.obj_z.location.z - self.insert.obj_bp.location.z)

                tkdhd = self.insert.get_prompt('Top KD Holes Down')
                for i in range(0, 9):
                    remove_top_shelf = closet.get_prompt('Remove Top Shelf ' + str(i))
                    top_KD_vertical_offset = closet.get_prompt("Top KD " + str(i) + ' Vertical Offset')
                    if remove_top_shelf and top_KD_vertical_offset:
                        remove_top_shelf.set_value(True)
                        if tkdhd:
                            if tkdhd.get_value() == 1:
                                top_KD_vertical_offset.set_value(sn_unit.inch(1.26))
                            elif tkdhd.get_value() == 2:
                                top_KD_vertical_offset.set_value(sn_unit.inch(2.56))
                            else:
                                top_KD_vertical_offset.set_value(0)
            else:
                for i in range(0, 9):
                    parent_assembly = sn_types.Assembly(self.insert.obj_bp.parent)
                    top_KD_vertical_offset = parent_assembly.get_prompt("Top KD " + str(i) + ' Vertical Offset')
                    if top_KD_vertical_offset:
                        top_KD_vertical_offset.set_value(0)

            if (self.insert.get_prompt("Show Layered Molding")):
                for obj in self.insert.obj_bp.children:
                    if obj.get('IS_BP_FLAT_CROWN'):
                        obj['IS_BP_LAYERED_CROWN'] = self.insert.get_prompt("Show Layered Molding").get_value()

        TE_Prompt = self.insert.get_prompt('Topshelf Exists')
        if TE_Prompt:
            TE_Prompt.set_value(self.has_topshelf)

            ts_assembly = None
            for child in self.insert.obj_bp.parent.children:
                if not child.hide_get():
                    if 'IS_BP_CLOSET_TOP' in child:
                        ts_assembly = sn_types.Assembly(child)

            if ts_assembly:
                ts_overhang = ts_assembly.get_prompt("Front Overhang")
                fc_overhang = self.insert.get_prompt("Front Overhang")
                self.insert.obj_y.location.y = math.fabs(ts_assembly.obj_y.location.y)
                if(ts_overhang and fc_overhang):
                    fc_overhang.set_value(ts_overhang.get_value())

        closet_props.update_render_materials(self, context)


        # self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        # self.update_product_size()
        
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.insert = self.get_insert()
        tkdhd = self.insert.get_prompt('Top KD Holes Down')
        if tkdhd:
            self.TKHD_VAR = str(tkdhd.get_value())
        self.layered_crown = self.insert.get_prompt('Layered Crown').get_value()
        if self.insert.get_prompt('Number of Layers'):
            self.layer_num = str(self.insert.get_prompt('Number of Layers').get_value())
        wm = context.window_manager

        # check if topshelf exists
        self.has_topshelf = False
        for child in self.insert.obj_bp.parent.children:
            if not child.hide_get():
                if 'IS_BP_CLOSET_TOP' in child:
                    self.has_topshelf = True
                    break

        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(450))

    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(text=self.insert.obj_bp.name)
        box = layout.box()

        molding_height = self.insert.get_prompt("Molding Height")
        extend_to_ceiling = self.insert.get_prompt("Extend To Ceiling")
        exposed_left = self.insert.get_prompt("Exposed Left")
        exposed_right = self.insert.get_prompt("Exposed Right")
        return_left = self.insert.get_prompt("Return Left")
        return_right = self.insert.get_prompt("Return Right")
        exposed_back = self.insert.get_prompt("Exposed Back")
        extend_left_amount = self.insert.get_prompt("Extend Left Amount")
        extend_right_amount = self.insert.get_prompt("Extend Right Amount")
        front_overhang = self.insert.get_prompt("Front Overhang")
        molding_location = self.insert.get_prompt('Molding Location')
        tkdhd = self.insert.get_prompt('Top KD Holes Down')
        show_layered = self.insert.get_prompt('Show Layered Molding')
        layer_num = self.insert.get_prompt('Number of Layers')
        if extend_to_ceiling:
            row = box.row()
            row.prop(extend_to_ceiling, "checkbox_value", text=extend_to_ceiling.name)
            parent_assembly = sn_types.Assembly(self.insert.obj_bp.parent)
            top_kd_1_vertical_offset = parent_assembly.get_prompt("Top KD 1 Vertical Offset")

            if extend_to_ceiling.get_value() and top_kd_1_vertical_offset:
                row = box.row()
                row.label(text='Top KD Holes Down')
                row.prop(self, 'TKHD_VAR', expand=True)
            else:
                if show_layered and not show_layered.get_value():
                    row = box.row()
                    row.prop(molding_height, "distance_value", text=molding_height.name)
                row = box.row()
                row.prop(molding_location, "distance_value", text=molding_location.name)
        else:
            if show_layered and not show_layered.get_value():
                row = box.row()
                row.prop(molding_height, "distance_value", text=molding_height.name)
            row = box.row()
            row.prop(molding_location, "distance_value", text=molding_location.name)

        row = box.row()
        row.label(text="Extend Ends")
        row.prop(extend_left_amount, "distance_value", text="Left")
        row.prop(extend_right_amount, "distance_value", text="Right")
        row = box.row()
        row.label(text="Exposed Edges")
        row.prop(exposed_left, "checkbox_value", text="Left")
        row.prop(exposed_right, "checkbox_value", text="Right")

        if extend_to_ceiling:
            if(molding_height.get_value() >= sn_unit.inch(3) and extend_to_ceiling.get_value() is False):
                row.prop(exposed_back, "checkbox_value", text="Top")
        else:
            row.prop(exposed_back, "checkbox_value", text="Top")

        row = box.row()
        row.label(text="End Returns")
        row.prop(return_left, "checkbox_value", text="Left Return")
        row.prop(return_right, "checkbox_value", text="Right Return")
        row = box.row()
        row.prop(front_overhang, "distance_value", text=front_overhang.name)
        if show_layered:
            row = box.row()
            row.prop(show_layered, 'checkbox_value', text='Layered Crown')
            if show_layered.get_value():
                row.label(text='Number of Layers')
                row.prop(self, 'layer_num', expand=True)
            


class DROP_OPERATOR_Place_Top(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.top_drop"
    bl_label = "Place Top"
    bl_description = "This places the top."
    bl_options = {'UNDO'}

    objects = []
    selected_panel_1 = None
    selected_panel_2 = None

    def execute(self, context):
        self.objects = [obj for obj in context.visible_objects if obj.parent and obj.parent.sn_closets.is_panel_bp]
        return super().execute(context)

    def get_distance_between_panels(self, panel_1, panel_2):    
        if panel_1.obj_z.location.z > 0:
            obj_1 = panel_1.obj_z
        else:
            obj_1 = panel_1.obj_bp

        if panel_2.obj_z.location.z > 0:
            obj_2 = panel_2.obj_bp
        else:
            obj_2 = panel_2.obj_z

        x1 = obj_1.matrix_world[0][3]
        y1 = obj_1.matrix_world[1][3]
        z1 = obj_1.matrix_world[2][3]

        x2 = obj_2.matrix_world[0][3]
        y2 = obj_2.matrix_world[1][3]
        z2 = obj_2.matrix_world[2][3]

        # DONT CALCULATE Z DIFFERENCE
        return sn_utils.calc_distance((x1, y1, z1), (x2, y2, z1))

    def insert_drop(self, context, event):
        selected_point, selected_obj, _ = sn_utils.get_selection_point(context, event, objects=self.objects)
        bpy.ops.object.select_all(action='DESELECT')

        if selected_obj is not None:

            sel_product_bp = sn_utils.get_bp(selected_obj, 'PRODUCT')
            sel_assembly_bp = sn_utils.get_assembly_bp(selected_obj)

            if sel_assembly_bp:
                if 'IS_BP_PANEL' in sel_assembly_bp:
                    selected_obj.select_set(True)
                    hover_panel = sn_types.Assembly(selected_obj.parent)

                    if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                        if not self.selected_panel_1:
                            self.selected_panel_1 = hover_panel
                            sn_utils.set_wireframe(self.asset.obj_bp, False)
                            bpy.context.window.cursor_set('DEFAULT')
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = self.asset.obj_bp
                            self.asset.obj_bp.parent = sel_product_bp

                            if self.selected_panel_1.obj_z.location.z > 0:
                                # CENTER OR RIGHT PANEL SELECTED
                                self.asset.obj_bp.location = self.selected_panel_1.obj_bp.location
                                self.asset.obj_bp.location.x -= self.selected_panel_1.obj_z.location.z
                            else:
                                # LEFT PANEL SELECTED
                                self.asset.obj_bp.location = self.selected_panel_1.obj_bp.location

                            return {'RUNNING_MODAL'}

                        if not self.selected_panel_2:
                            self.selected_panel_2 = hover_panel

                            if self.selected_panel_2.obj_bp.parent is not None:
                                pard = sn_types.Assembly(self.selected_panel_2.obj_bp)
                                Base_Height = self.selected_panel_2.obj_bp.snap.get_var('location.z', 'Base_Height')
                                Height = self.selected_panel_2.obj_x.snap.get_var('location.x', 'Height')
                                self.asset.obj_bp.snap.loc_z("Height+Base_Height", [Height, Base_Height])

                            sn_utils.set_wireframe(self.asset.obj_bp, False)
                            bpy.context.window.cursor_set('DEFAULT')
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = self.asset.obj_bp
                            self.asset.obj_bp.select_set(True)
                            dist = self.get_distance_between_panels(self.selected_panel_1, self.selected_panel_2)
                            self.asset.obj_x.location.x = dist
                            self.asset.obj_bp.snap.type_group = 'INSERT'
                            self.asset.obj_bp.location.z = self.selected_panel_1.obj_bp.location.z + self.selected_panel_1.obj_x.location.x
                            if(math.fabs(self.selected_panel_1.obj_y.location.y) <= math.fabs(self.selected_panel_2.obj_y.location.y)):
                                self.asset.obj_y.location.y = math.fabs(self.selected_panel_1.obj_y.location.y)
                            else:
                                self.asset.obj_y.location.y = math.fabs(self.selected_panel_2.obj_y.location.y)
                            for child in self.asset.obj_bp.parent.children:
                                if not child.hide_get():
                                    if 'IS_BP_CLOSET_TOP' in child:
                                        ts_assembly = sn_types.Assembly(child)
                                        ts_overhang = ts_assembly.get_prompt("Front Overhang")
                                        fc_overhang = self.asset.get_prompt("Front Overhang")
                                        self.asset.obj_y.location.y = math.fabs(ts_assembly.obj_y.location.y)
                                        if(ts_overhang and fc_overhang):
                                            fc_overhang.set_value(ts_overhang.get_value())

                                        ts_left_extend = ts_assembly.get_prompt('Extend Left Amount')
                                        ts_right_extend = ts_assembly.get_prompt('Extend Right Amount')
                                        if ts_left_extend and ts_right_extend:
                                            if ts_left_extend.get_value() > 0:
                                                sn_utils.set_prompt_if_exists(self.asset, 'Extend Left Amount', ts_left_extend.get_value())
                                            if ts_right_extend.get_value() > 0:
                                                sn_utils.set_prompt_if_exists(self.asset, 'Extend Right Amount', ts_right_extend.get_value())

                                        ts_exposed_right = ts_assembly.get_prompt('Exposed Right')
                                        if ts_exposed_right:
                                            sn_utils.set_prompt_if_exists(self.asset, 'Return Right', ts_exposed_right.get_value())
                                        
                                        ts_exposed_left = ts_assembly.get_prompt('Exposed Left')
                                        if ts_exposed_left:
                                            sn_utils.set_prompt_if_exists(self.asset, 'Return Left', ts_exposed_left.get_value())

                                        

                            parent = sn_types.Assembly(obj_bp=self.asset.obj_bp.parent)
                            Width = parent.obj_x.snap.get_var('location.x', 'Width')
                            Left_Side_Wall_Filler =\
                                parent.get_prompt(
                                    'Left Side Wall Filler')
                            Right_Side_Wall_Filler =\
                                parent.get_prompt(
                                    'Right Side Wall Filler')
                            if not (Right_Side_Wall_Filler and Left_Side_Wall_Filler):
                                return self.finish(context)
                            left_filler = Left_Side_Wall_Filler.get_value()
                            right_filler = Right_Side_Wall_Filler.get_value()
                            partition_width =\
                                parent.obj_x.location.x - left_filler - right_filler
                            if round(partition_width, 2) == round(dist, 2):
                                self.asset.dim_x('Width', [Width])
                                self.asset.loc_x('0', [])
                            return self.finish(context)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        bpy.ops.object.select_all(action='DESELECT')
        # context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        self.reset_selection()

        if self.event_is_cancel_command(event):
            context.area.header_text_set(None)
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return self.insert_drop(context, event)

bpy.utils.register_class(PROMPTS_prompts_flat_molding)
bpy.utils.register_class(DROP_OPERATOR_Place_Top)
