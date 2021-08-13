from snap import sn_types, sn_unit
from os import path
import math
from .. import closet_props
from ..common import common_parts
import bpy

class Wood_Drawer_Box(sn_types.Assembly):
    
    type_assembly = "NONE"
    mirror_y = False
    
    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.obj_bp.snap.export_as_subassembly = True
        
        props = bpy.context.scene.sn_closets
        defaults = props.closet_defaults        
        
        obj_props = self.obj_bp.sn_closets
        obj_props.is_drawer_box_bp = True  # TODO: remove
        self.obj_bp["IS_BP_DRAWER_BOX"] = True
        
        self.add_prompt("Hide", 'CHECKBOX', False)
        self.add_prompt("Hide Drawer Sub Front", 'CHECKBOX', False)
        self.add_prompt("Drawer Side Thickness", 'DISTANCE', sn_unit.inch(.5))
        self.add_prompt("Front Back Thickness", 'DISTANCE', sn_unit.inch(.5))
        self.add_prompt("Drawer Bottom Thickness", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Drawer Box Bottom Dado Depth", 'DISTANCE', defaults.drawer_bottom_dado_depth)
        self.add_prompt("Drawer Bottom Z Location", 'DISTANCE', defaults.drawer_bottom_z_location)
        self.add_prompt("Applied Bottom", 'CHECKBOX', False)
        self.add_prompt("Applied Bottom Width Deduction", 'DISTANCE', 0)
        self.add_prompt("Applied Bottom Depth Deduction", 'DISTANCE', 0)
        self.add_prompt("Back Override Height", 'DISTANCE', 0)
        self.add_prompt("Override Height", 'DISTANCE', 0)
        self.add_prompt("Override Depth", 'DISTANCE', 0)
        self.add_prompt("Use Dovetail Construction", 'CHECKBOX', False)
        
        Drawer_Width = self.obj_x.snap.get_var('location.x','Drawer_Width')
        Drawer_Depth = self.obj_y.snap.get_var('location.y','Drawer_Depth')
        Drawer_Height = self.obj_z.snap.get_var('location.z','Drawer_Height')
        Drawer_Side_Thickness = self.get_prompt('Drawer Side Thickness').get_var('Drawer_Side_Thickness')
        Front_Back_Thickness = self.get_prompt('Front Back Thickness').get_var('Front_Back_Thickness')
        Drawer_Bottom_Thickness = self.get_prompt('Drawer Bottom Thickness').get_var('Drawer_Bottom_Thickness')
        Drawer_Box_Bottom_Dado_Depth = self.get_prompt('Drawer Box Bottom Dado Depth').get_var('Drawer_Box_Bottom_Dado_Depth')
        Drawer_Bottom_Z_Location = self.get_prompt('Drawer Bottom Z Location').get_var('Drawer_Bottom_Z_Location')
        Override_Height = self.get_prompt('Override Height').get_var('Override_Height')
        Override_Depth = self.get_prompt('Override Depth').get_var('Override_Depth')
        HSF = self.get_prompt('Hide Drawer Sub Front').get_var('HSF')
        Applied_Bottom = self.get_prompt('Applied Bottom').get_var('Applied_Bottom')
        Back_Override_Height = self.get_prompt('Back Override Height').get_var('Back_Override_Height')
        ABWD = self.get_prompt('Applied Bottom Width Deduction').get_var('ABWD')
        ABDD = self.get_prompt('Applied Bottom Depth Deduction').get_var('ABDD')
        Hide = self.get_prompt('Hide').get_var('Hide')
        Use_Dovetail_Construction = self.get_prompt('Use Dovetail Construction').get_var('Use_Dovetail_Construction')
        
        self.get_prompt('Drawer Side Thickness').set_value(value=sn_unit.inch(0.5))
        self.get_prompt('Front Back Thickness').set_value(value=sn_unit.inch(0.5))
        self.get_prompt('Drawer Bottom Thickness').set_value(value=sn_unit.inch(0.375))
        
        left_side = common_parts.add_drawer_side(self)
        left_side.set_name("Left Drawer Side")
        left_side.loc_y('IF(Use_Dovetail_Construction,INCH(.125),0) or Hide',[Use_Dovetail_Construction,self.hide_var])
        left_side.rot_x(value=math.radians(90))
        left_side.rot_z(value=math.radians(90))
        left_side.dim_x('IF(Use_Dovetail_Construction,IF(Override_Depth>0,Override_Depth,Drawer_Depth)-INCH(.25),IF(Override_Depth>0,Override_Depth,Drawer_Depth))',[Override_Depth,Drawer_Depth,Use_Dovetail_Construction,Drawer_Depth])
        left_side.dim_y('IF(Override_Height>0,Override_Height,Drawer_Height)',[Use_Dovetail_Construction,Override_Height,Drawer_Height])
        left_side.dim_z('Drawer_Side_Thickness',[Drawer_Side_Thickness])
        left_side.get_prompt('Hide').set_formula('Hide',[Hide])

        right_side = common_parts.add_drawer_side(self)
        right_side.set_name("Right Drawer Side")
        right_side.loc_x('Drawer_Width',[Drawer_Width])
        right_side.loc_y('IF(Use_Dovetail_Construction,INCH(.125),0)',[Use_Dovetail_Construction])
        right_side.rot_x(value=math.radians(90))
        right_side.rot_z(value=math.radians(90))
        right_side.dim_x('IF(Use_Dovetail_Construction,IF(Override_Depth>0,Override_Depth,Drawer_Depth)-INCH(.25),IF(Override_Depth>0,Override_Depth,Drawer_Depth))',[Override_Depth,Drawer_Depth,Use_Dovetail_Construction,Drawer_Depth])
        right_side.dim_y('IF(Override_Height>0,Override_Height,Drawer_Height)',[Override_Height,Use_Dovetail_Construction,Drawer_Height])
        right_side.dim_z('-Drawer_Side_Thickness',[Drawer_Side_Thickness])
        right_side.get_prompt('Hide').set_formula('Hide',[Hide])
        
        front = common_parts.add_drawer_sub_front(self)
        front.loc_x('IF(Use_Dovetail_Construction,INCH(.125),Drawer_Side_Thickness)',[Use_Dovetail_Construction,Drawer_Side_Thickness])
        front.rot_x(value=math.radians(90))
        front.dim_x('Drawer_Width-IF(Use_Dovetail_Construction,INCH(.25),(Drawer_Side_Thickness*2))',[Use_Dovetail_Construction,Drawer_Width,Drawer_Side_Thickness])
        front.dim_y('IF(Override_Height>0,Override_Height,Drawer_Height)',[Override_Height,Use_Dovetail_Construction,Drawer_Height])
        front.dim_z('-Front_Back_Thickness',[Front_Back_Thickness])
        front.get_prompt('Hide').set_formula('IF(HSF,True,Hide) or Hide',[HSF,Hide,self.hide_var])

        back = common_parts.add_drawer_back(self)
        back.loc_x('IF(Use_Dovetail_Construction,INCH(.125),Drawer_Side_Thickness)',[Use_Dovetail_Construction,Drawer_Side_Thickness])
        back.loc_y('IF(Override_Depth>0,Override_Depth,Drawer_Depth)',[Override_Depth,Drawer_Depth])
        back.loc_z('IF(Applied_Bottom,Drawer_Bottom_Thickness,0)',[Applied_Bottom,Drawer_Bottom_Thickness])
        back.rot_x(value=math.radians(90))
        back.dim_x('Drawer_Width-IF(Use_Dovetail_Construction,INCH(.25),(Drawer_Side_Thickness*2))',[Use_Dovetail_Construction,Drawer_Width,Drawer_Side_Thickness])
        back.dim_y('IF(Override_Height>0,Override_Height,Drawer_Height)',[Override_Height,Use_Dovetail_Construction,Drawer_Height])
        back.dim_z('Front_Back_Thickness',[Front_Back_Thickness])
        back.get_prompt('Hide').set_formula('Hide',[Hide])
        
        bottom = common_parts.add_drawer_bottom(self)
        bottom.loc_x('IF(Use_Dovetail_Construction,INCH(.375),0)',[Use_Dovetail_Construction,Drawer_Width])
        bottom.loc_y('IF(Use_Dovetail_Construction,INCH(.375),0)',[Use_Dovetail_Construction,Drawer_Width])
        bottom.loc_z('IF(Use_Dovetail_Construction,INCH(.5),-Drawer_Bottom_Thickness)',[Use_Dovetail_Construction,Drawer_Bottom_Thickness])
        bottom.rot_z(value=math.radians(90))
        bottom.dim_x('IF(Use_Dovetail_Construction,IF(Override_Depth>0,Override_Depth,Drawer_Depth)-INCH(.625),IF(Override_Depth>0,Override_Depth,Drawer_Depth))',[Override_Depth,Use_Dovetail_Construction,Drawer_Depth])
        bottom.dim_y('IF(Use_Dovetail_Construction,Drawer_Width-INCH(.625),Drawer_Width)*-1',[Use_Dovetail_Construction,Drawer_Width])
        bottom.dim_z('Drawer_Bottom_Thickness',[Drawer_Bottom_Thickness])
        bottom.get_prompt('Hide').set_formula('Hide',[Hide])
        
        # self.update()
        
        