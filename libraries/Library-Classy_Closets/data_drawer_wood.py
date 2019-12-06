from mv import fd_types, unit
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts

class Wood_Drawer_Box(fd_types.Assembly):
    
    type_assembly = "NONE"
    mirror_y = False
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_scene_props()
        defaults = props.closet_defaults        
        
        obj_props = props_closet.get_object_props(self.obj_bp)
        obj_props.is_drawer_box_bp = True
        
        self.add_tab(name='Drawer Box Options',tab_type='VISIBLE')
        self.add_prompt(name="Hide",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Hide Drawer Sub Front",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Drawer Side Thickness",prompt_type='DISTANCE',value=unit.inch(.5),tab_index=0)
        self.add_prompt(name="Front Back Thickness",prompt_type='DISTANCE',value=unit.inch(.5),tab_index=0)
        self.add_prompt(name="Drawer Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Drawer Box Bottom Dado Depth",prompt_type='DISTANCE',value=defaults.drawer_bottom_dado_depth,tab_index=0)
        self.add_prompt(name="Drawer Bottom Z Location",prompt_type='DISTANCE',value=defaults.drawer_bottom_z_location,tab_index=0)
        self.add_prompt(name="Applied Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Applied Bottom Width Deduction",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Applied Bottom Depth Deduction",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Back Override Height",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Override Height",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Override Depth",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Use Dovetail Construction",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        Drawer_Width = self.get_var('dim_x','Drawer_Width')
        Drawer_Depth = self.get_var('dim_y','Drawer_Depth')
        Drawer_Height = self.get_var('dim_z','Drawer_Height')
        Drawer_Side_Thickness = self.get_var('Drawer Side Thickness')
        Front_Back_Thickness = self.get_var('Front Back Thickness')
        Drawer_Bottom_Thickness = self.get_var('Drawer Bottom Thickness')
        Drawer_Box_Bottom_Dado_Depth = self.get_var('Drawer Box Bottom Dado Depth')
        Drawer_Bottom_Z_Location = self.get_var('Drawer Bottom Z Location')
        Override_Height = self.get_var('Override Height')
        Override_Depth = self.get_var('Override Depth')
        HSF = self.get_var('Hide Drawer Sub Front','HSF')
        Applied_Bottom = self.get_var('Applied Bottom')
        Back_Override_Height = self.get_var('Back Override Height')
        ABWD = self.get_var('Applied Bottom Width Deduction','ABWD')
        ABDD = self.get_var('Applied Bottom Depth Deduction','ABDD')
        Hide = self.get_var('Hide')
        Use_Dovetail_Construction = self.get_var('Use Dovetail Construction')
        
        self.prompt('Drawer Side Thickness','THICKNESS(sgi,"Drawer_Part")',[sgi])
        self.prompt('Front Back Thickness','THICKNESS(sgi,"Drawer_Part")',[sgi])
        self.prompt('Drawer Bottom Thickness','THICKNESS(sgi,"Drawer_Bottom")',[sgi])
        
        left_side = common_parts.add_drawer_side(self)
        left_side.set_name("Left Drawer Side")
        left_side.x_loc(value = 0)
        left_side.y_loc('IF(Use_Dovetail_Construction,INCH(.125),0)',[Use_Dovetail_Construction])
        left_side.z_loc(value = 0)
        left_side.x_rot(value = 90)
        left_side.y_rot(value = 0)
        left_side.z_rot(value = 90)
        left_side.x_dim('IF(Use_Dovetail_Construction,IF(Override_Depth>0,Override_Depth,Drawer_Depth)-INCH(.25),IF(Override_Depth>0,Override_Depth,Drawer_Depth))',[Override_Depth,Drawer_Depth,Use_Dovetail_Construction,Drawer_Depth])
        left_side.y_dim('IF(Override_Height>0,Override_Height,Drawer_Height)',[Use_Dovetail_Construction,Override_Height,Drawer_Height])
        left_side.z_dim('Drawer_Side_Thickness',[Drawer_Side_Thickness])
        left_side.prompt('Hide','Hide',[Hide])

        right_side = common_parts.add_drawer_side(self)
        right_side.set_name("Right Drawer Side")
        right_side.x_loc('Drawer_Width',[Drawer_Width])
        right_side.y_loc('IF(Use_Dovetail_Construction,INCH(.125),0)',[Use_Dovetail_Construction])
        right_side.z_loc(value = 0)
        right_side.x_rot(value = 90)
        right_side.y_rot(value = 0)
        right_side.z_rot(value = 90)
        right_side.x_dim('IF(Use_Dovetail_Construction,IF(Override_Depth>0,Override_Depth,Drawer_Depth)-INCH(.25),IF(Override_Depth>0,Override_Depth,Drawer_Depth))',[Override_Depth,Drawer_Depth,Use_Dovetail_Construction,Drawer_Depth])
        right_side.y_dim('IF(Override_Height>0,Override_Height,Drawer_Height)',[Override_Height,Use_Dovetail_Construction,Drawer_Height])
        right_side.z_dim('-Drawer_Side_Thickness',[Drawer_Side_Thickness])
        right_side.prompt('Hide','Hide',[Hide])
        
        front = common_parts.add_drawer_sub_front(self)
        front.x_loc('IF(Use_Dovetail_Construction,INCH(.125),Drawer_Side_Thickness)',[Use_Dovetail_Construction,Drawer_Side_Thickness])
        front.y_loc(value = 0)
        front.z_loc(value = 0)
        front.x_rot(value = 90)
        front.y_rot(value = 0)
        front.z_rot(value = 0)
        front.x_dim('Drawer_Width-IF(Use_Dovetail_Construction,INCH(.25),(Drawer_Side_Thickness*2))',[Use_Dovetail_Construction,Drawer_Width,Drawer_Side_Thickness])
        front.y_dim('IF(Override_Height>0,Override_Height,Drawer_Height)',[Override_Height,Use_Dovetail_Construction,Drawer_Height])
        front.z_dim('-Front_Back_Thickness',[Front_Back_Thickness])
        front.prompt('Hide','IF(HSF,True,Hide)',[HSF,Hide])

        back = common_parts.add_drawer_back(self)
        back.x_loc('IF(Use_Dovetail_Construction,INCH(.125),Drawer_Side_Thickness)',[Use_Dovetail_Construction,Drawer_Side_Thickness])
        back.y_loc('IF(Override_Depth>0,Override_Depth,Drawer_Depth)',[Override_Depth,Drawer_Depth])
        back.z_loc('IF(Applied_Bottom,Drawer_Bottom_Thickness,0)',[Applied_Bottom,Drawer_Bottom_Thickness])
        back.x_rot(value = 90)
        back.y_rot(value = 0)
        back.z_rot(value = 0)
        back.x_dim('Drawer_Width-IF(Use_Dovetail_Construction,INCH(.25),(Drawer_Side_Thickness*2))',[Use_Dovetail_Construction,Drawer_Width,Drawer_Side_Thickness])
        back.y_dim('IF(Override_Height>0,Override_Height,Drawer_Height)',[Override_Height,Use_Dovetail_Construction,Drawer_Height])
        back.z_dim('Front_Back_Thickness',[Front_Back_Thickness])
        back.prompt('Hide','Hide',[Hide])
        
        bottom = common_parts.add_drawer_bottom(self)
        bottom.x_loc('IF(Use_Dovetail_Construction,INCH(.375),-INCH(.05))',[Use_Dovetail_Construction,Drawer_Width])
        bottom.y_loc('IF(Use_Dovetail_Construction,INCH(.375),0)',[Use_Dovetail_Construction,Drawer_Width])
        bottom.z_loc('IF(Use_Dovetail_Construction,INCH(.5),-Drawer_Bottom_Thickness)',[Use_Dovetail_Construction,Drawer_Bottom_Thickness])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 90)
        bottom.x_dim('IF(Use_Dovetail_Construction,IF(Override_Depth>0,Override_Depth,Drawer_Depth)-INCH(.625),IF(Override_Depth>0,Override_Depth,Drawer_Depth))',[Override_Depth,Use_Dovetail_Construction,Drawer_Depth])
        bottom.y_dim('IF(Use_Dovetail_Construction,Drawer_Width-INCH(.625),Drawer_Width+INCH(.1))*-1',[Use_Dovetail_Construction,Drawer_Width])
        bottom.z_dim('Drawer_Bottom_Thickness',[Drawer_Bottom_Thickness])
        bottom.prompt('Hide','Hide',[Hide])
        
        self.update()
        
class Tie_Drawer_Box(fd_types.Assembly):
    
    type_assembly = "NONE"
    mirror_y = False
    
    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Drawer Box Options',tab_type='VISIBLE')
        self.add_prompt(name="Drawer Part Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        
        Drawer_Width = self.get_var('dim_x','Drawer_Width')
        Drawer_Depth = self.get_var('dim_y','Drawer_Depth')
        Drawer_Height = self.get_var('dim_z','Drawer_Height')
        Drawer_Part_Thickness = self.get_var('Drawer Part Thickness')
        Division_Thickness = self.get_var('Division Thickness')
        
        top = common_parts.add_tie_drawer_top_or_bottom(self)
        top.set_name("Tie Drawer Top")
        top.x_loc('Drawer_Width',[Drawer_Width])
        top.y_loc(value = 0)
        top.z_loc('Drawer_Height',[Drawer_Height])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 90)
        top.x_dim('Drawer_Depth',[Drawer_Depth])
        top.y_dim('Drawer_Width',[Drawer_Width])
        top.z_dim('-Drawer_Part_Thickness',[Drawer_Part_Thickness])

        bottom = common_parts.add_tie_drawer_top_or_bottom(self)
        bottom.set_name("Tie Drawer Bottom")
        bottom.x_loc('Drawer_Width',[Drawer_Width])
        bottom.y_loc(value = 0)
        bottom.z_loc(value = 0)
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 90)
        bottom.x_dim('Drawer_Depth',[Drawer_Depth])
        bottom.y_dim('Drawer_Width',[Drawer_Width])
        bottom.z_dim('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        bottom.cutpart("Drawer_Part")
        bottom.edgebanding('Drawer_Box_Edge',l1 = True)

        front = common_parts.add_drawer_sub_front_or_back(self)
        front.set_name("Tie Drawer Sub Front")
        front.x_loc('Drawer_Width',[Drawer_Width])
        front.y_loc(value = 0)
        front.z_loc('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        front.x_rot(value = 90)
        front.y_rot(value = -90)
        front.z_rot(value = 0)
        front.x_dim('Drawer_Height-(Drawer_Part_Thickness*2)',[Drawer_Height,Drawer_Part_Thickness])
        front.y_dim('Drawer_Width',[Drawer_Width])
        front.z_dim('-Drawer_Part_Thickness',[Drawer_Part_Thickness])
        
        back = common_parts.add_drawer_sub_front_or_back(self)
        back.set_name("Tie Drawer Back")
        back.x_loc('Drawer_Width',[Drawer_Width])
        back.y_loc('Drawer_Depth',[Drawer_Depth])
        back.z_loc('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        back.x_rot(value = 90)
        back.y_rot(value = -90)
        back.z_rot(value = 0)
        back.x_dim('Drawer_Height-(Drawer_Part_Thickness*2)',[Drawer_Height,Drawer_Part_Thickness])
        back.y_dim('Drawer_Width',[Drawer_Width])
        back.z_dim('Drawer_Part_Thickness',[Drawer_Part_Thickness])

        division = common_parts.add_tie_drawer_division(self)
        division.set_name("Tie Drawer Division")
        division.x_loc('(Drawer_Width/2)-(Drawer_Part_Thickness/2)',[Drawer_Width,Drawer_Part_Thickness])
        division.y_loc('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        division.z_loc('Drawer_Height-Drawer_Part_Thickness',[Drawer_Height,Drawer_Part_Thickness])
        division.x_rot(value = 90)
        division.y_rot(value = 90)
        division.z_rot(value = 90)
        division.x_dim('Drawer_Height-(Drawer_Part_Thickness*2)',[Drawer_Height,Drawer_Part_Thickness])
        division.y_dim('Drawer_Depth-(Drawer_Part_Thickness*2)',[Drawer_Depth,Drawer_Part_Thickness])
        division.z_dim('Division_Thickness',[Division_Thickness])

        self.update()                
        