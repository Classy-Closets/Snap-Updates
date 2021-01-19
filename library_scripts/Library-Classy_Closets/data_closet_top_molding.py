'''
Created on Jun 13, 2017

@author: Andrew
'''
import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from os import path
import math

class Flat_Crown(fd_types.Assembly):
    """ Base Cabinet Standard
    """

    property_id = props_closet.LIBRARY_NAME_SPACE + ".top_molding"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".top_drop"
    
    type_assembly = "PRODUCT"
    mirror_y = True
    
    def draw(self):
        self.create_assembly()
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_crown_molding = True
        props.is_flat_crown_bp = True
        
        self.add_tab(name='Top Options',tab_type='VISIBLE') #1
        self.add_prompt(name="Extend To Left Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Extend To Right Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Return Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Return Right",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Extend Left Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Extend Right Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Front Overhang",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Molding Height",prompt_type='DISTANCE',value=unit.inch(3),tab_index=1)
        self.add_prompt(name="Molding Location",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Extend To Ceiling",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Distance From Ceiling",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Top KD Holes Down",prompt_type='COMBOBOX',value=0,items=["None",'One','Two'],tab_index=1)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Extend_Left = self.get_var('Extend To Left Panel','Extend_Left')        
        Extend_Right = self.get_var('Extend To Right Panel','Extend_Right')      
        Panel_Thickness = self.get_var('Panel Thickness')
        Extend_Left_Amount = self.get_var('Extend Left Amount')
        Extend_Right_Amount = self.get_var('Extend Right Amount')
        Front_Overhang = self.get_var('Front Overhang')
        Return_Left = self.get_var('Return Left')
        Return_Right = self.get_var('Return Right')
        Exposed_Left = self.get_var('Exposed Left')
        Exposed_Right = self.get_var('Exposed Right')
        Exposed_Back = self.get_var('Exposed Back')
        Molding_Height = self.get_var('Molding Height')
        Molding_Location = self.get_var('Molding Location')
        ETC = self.get_var('Extend To Ceiling', 'ETC')
        DFC = self.get_var('Distance From Ceiling', 'DFC')
        TKDHD = self.get_var('Top KD Holes Down','TKDHD')
        
        flat_crown = common_parts.add_flat_crown(self)
        flat_crown.obj_bp.mv.comment_2 = "1038"
        flat_crown.set_name("Flat Crown")
        flat_crown.x_loc('IF(Return_Left,-Panel_Thickness+'+str(unit.millimeter(0.1))+',0)-Extend_Left_Amount',[Extend_Left,Extend_Left_Amount,Panel_Thickness,Return_Left])
        flat_crown.y_loc('-Depth-Front_Overhang', [Depth,Front_Overhang])
        flat_crown.z_loc('IF(ETC,DFC,Molding_Height+Molding_Location)',[Molding_Height,Molding_Location,ETC,DFC])
        flat_crown.x_rot(value = -90)
        flat_crown.y_rot(value = 0)
        flat_crown.z_rot(value = 0)
        flat_crown.x_dim('Width+Extend_Left_Amount+Extend_Right_Amount+IF(Return_Right,Panel_Thickness-'+str(unit.millimeter(0.1))+',0)+IF(Return_Left,Panel_Thickness-'+str(unit.millimeter(0.1))+',0)',
                  [Width,Extend_Left,Extend_Right,Panel_Thickness,Extend_Right_Amount,Extend_Left_Amount,Return_Right,Return_Left])
        flat_crown.y_dim('IF(ETC,IF(TKDHD == 1,INCH(1.26),IF(TKDHD == 2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height)',[Molding_Height,ETC,DFC,TKDHD])
        flat_crown.z_dim('-Panel_Thickness',[Panel_Thickness])
        flat_crown.prompt('Exposed Left','Exposed_Left',[Exposed_Left])
        flat_crown.prompt('Exposed Right','Exposed_Right',[Exposed_Right])
        flat_crown.prompt('Exposed Back','Exposed_Back',[Exposed_Back])
        
        left_return = common_parts.add_flat_crown(self)
        left_return.obj_bp.mv.comment_2 = "1038"
        left_return.set_name("Left")
        left_return.x_loc('(-Panel_Thickness)-Extend_Left_Amount', [Panel_Thickness,Extend_Left_Amount])
        left_return.y_loc('-Depth-Front_Overhang-Panel_Thickness+'+str(unit.millimeter(0.1))+'', [Depth,Front_Overhang,Panel_Thickness])
        left_return.z_loc('IF(ETC,DFC,Molding_Height+Molding_Location)',[Molding_Height,Molding_Location,ETC,DFC])
        left_return.x_rot(value = 90)
        left_return.y_rot(value = 0)
        left_return.z_rot(value = 90)
        left_return.x_dim('Depth+Front_Overhang+Panel_Thickness-'+str(unit.millimeter(0.1))+'', [Depth,Panel_Thickness,Front_Overhang])
        left_return.y_dim('IF(ETC,IF(TKDHD == 1,INCH(1.26),IF(TKDHD == 2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height) * -1',[Molding_Height,ETC,DFC,TKDHD])
        left_return.z_dim('Panel_Thickness', [Panel_Thickness])
        left_return.prompt('Hide','IF(Return_Left,False,True)',[Return_Left])
        left_return.prompt('Exposed Back','Exposed_Back',[Exposed_Back])
        
        right_return = common_parts.add_flat_crown(self)
        right_return.obj_bp.mv.comment_2 = "1038"
        right_return.set_name("Right")
        right_return.x_loc('Width+Extend_Right_Amount', [Width,Extend_Right_Amount])
        right_return.y_loc('-Depth-Front_Overhang-Panel_Thickness+'+str(unit.millimeter(0.1))+'', [Depth,Front_Overhang,Panel_Thickness])
        right_return.z_loc('IF(ETC,DFC,Molding_Height+Molding_Location)',[Molding_Height,Molding_Location,ETC,DFC])
        right_return.x_rot(value = 90)
        right_return.y_rot(value = 0)
        right_return.z_rot(value = 90)
        right_return.x_dim('Depth+Front_Overhang+Panel_Thickness-'+str(unit.millimeter(0.1))+'', [Depth,Panel_Thickness,Front_Overhang])
        right_return.y_dim('IF(ETC,IF(TKDHD == 1,INCH(1.26),IF(TKDHD == 2,INCH(2.52),0))+DFC+INCH(0.25),Molding_Height) * -1',[Molding_Height,ETC,DFC,TKDHD])
        right_return.z_dim('Panel_Thickness', [Panel_Thickness])
        right_return.prompt('Hide','IF(Return_Right,False,True)',[Return_Right])
        right_return.prompt('Exposed Back','Exposed_Back',[Exposed_Back])
        
        self.update()
        
class Flat_Valance_Full(fd_types.Assembly):
    """ Base Cabinet Standard
    """

    property_id = props_closet.LIBRARY_NAME_SPACE + ".top_molding"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".top_drop"
    
    type_assembly = "PRODUCT"
    mirror_y = True
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_crown_molding = True
        
        self.add_tab(name='Top Options',tab_type='VISIBLE') #1
        self.add_prompt(name="Extend To Left Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Extend To Right Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Return Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Return Right",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Extend Left Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Extend Right Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Front Overhang",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Molding Height",prompt_type='DISTANCE',value=unit.inch(3),tab_index=1)
        self.add_prompt(name="Molding Location",prompt_type='DISTANCE',value=unit.inch(-24),tab_index=1)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Extend_Left = self.get_var('Extend To Left Panel','Extend_Left')        
        Extend_Right = self.get_var('Extend To Right Panel','Extend_Right')      
        Panel_Thickness = self.get_var('Panel Thickness')
        Extend_Left_Amount = self.get_var('Extend Left Amount')
        Extend_Right_Amount = self.get_var('Extend Right Amount')
        Front_Overhang = self.get_var('Front Overhang')
        Return_Left = self.get_var('Return Left')
        Return_Right = self.get_var('Return Right')
        Exposed_Left = self.get_var('Exposed Left')
        Exposed_Right = self.get_var('Exposed Right')
        Exposed_Back = self.get_var('Exposed Back')
        Molding_Height = self.get_var('Molding Height')
        Molding_Location = self.get_var('Molding Location')
        
        flat_crown = common_parts.add_flat_crown(self)
        flat_crown.obj_bp.mv.comment_2 = "1040"
        flat_crown.set_name("Flat Valance")
        flat_crown.x_loc('IF(Extend_Left,0,Panel_Thickness/2)-Extend_Left_Amount',[Extend_Left,Extend_Left_Amount,Panel_Thickness])
        flat_crown.y_loc('-Depth-Front_Overhang+Panel_Thickness', [Depth,Front_Overhang,Panel_Thickness])
        flat_crown.z_loc('Molding_Location',[Molding_Location])
        flat_crown.x_rot(value = -90)
        flat_crown.y_rot(value = 0)
        flat_crown.z_rot(value = 0)
        flat_crown.x_dim('Width-IF(Extend_Left,0,Panel_Thickness/2)-IF(Extend_Right,0,Panel_Thickness/2)+Extend_Left_Amount+Extend_Right_Amount',
                  [Width,Extend_Left,Extend_Right,Panel_Thickness,Extend_Right_Amount,Extend_Left_Amount])
        flat_crown.y_dim('Molding_Height',[Molding_Height])
        flat_crown.z_dim('-Panel_Thickness',[Panel_Thickness])
        flat_crown.prompt('Exposed Left','Exposed_Left',[Exposed_Left])
        flat_crown.prompt('Exposed Right','Exposed_Right',[Exposed_Right])
        flat_crown.prompt('Exposed Back','Exposed_Back',[Exposed_Back])
        
        left_return = common_parts.add_cleat(self)
        left_return.obj_bp.mv.comment_2 = "1040"
        left_return.set_name("Left")
        left_return.x_loc('Panel_Thickness-Extend_Left_Amount', [Panel_Thickness,Extend_Left_Amount])
        left_return.y_loc('-Depth-Front_Overhang+Panel_Thickness', [Depth,Front_Overhang,Panel_Thickness])
        left_return.z_loc('Molding_Location-Molding_Height',[Molding_Location,Molding_Height])
        left_return.x_rot(value = 90)
        left_return.y_rot(value = 0)
        left_return.z_rot(value = 90)
        left_return.x_dim('Depth-Panel_Thickness+Front_Overhang', [Depth,Panel_Thickness,Front_Overhang])
        left_return.y_dim('Molding_Height', [Molding_Height])
        left_return.z_dim('-Panel_Thickness', [Panel_Thickness])
        left_return.prompt('Hide','IF(Return_Left,False,True)',[Return_Left])
        
        right_return = common_parts.add_cleat(self)
        right_return.obj_bp.mv.comment_2 = "1040"
        right_return.set_name("Right")
        right_return.x_loc('Width+Extend_Right_Amount', [Width,Extend_Right_Amount])
        right_return.y_loc('-Depth-Front_Overhang+Panel_Thickness', [Depth,Front_Overhang,Panel_Thickness])
        right_return.z_loc('Molding_Location-Molding_Height',[Molding_Location,Molding_Height])
        right_return.x_rot(value = 90)
        right_return.y_rot(value = 0)
        right_return.z_rot(value = 90)
        right_return.x_dim('Depth-Panel_Thickness+Front_Overhang', [Depth,Panel_Thickness,Front_Overhang])
        right_return.y_dim('Molding_Height', [Molding_Height])
        right_return.z_dim('-Panel_Thickness', [Panel_Thickness])
        right_return.prompt('Hide','IF(Return_Right,False,True)',[Return_Right])
        
        self.update()        
        
class Flat_Valance_Single(fd_types.Assembly):
    """ Base Cabinet Standard
    """

    property_id = props_closet.LIBRARY_NAME_SPACE + ".top_molding"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".top_drop"
    
    type_assembly = "PRODUCT"
    mirror_y = True
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_crown_molding = True
        
        self.add_tab(name='Top Options',tab_type='VISIBLE') #1
        self.add_prompt(name="Extend To Left Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Extend To Right Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Return Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Return Right",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Extend Left Amount",prompt_type='DISTANCE',value=unit.inch(-0.75),tab_index=1)
        self.add_prompt(name="Extend Right Amount",prompt_type='DISTANCE',value=unit.inch(-0.75),tab_index=1)
        self.add_prompt(name="Front Overhang",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Molding Height",prompt_type='DISTANCE',value=unit.inch(3),tab_index=1)
        self.add_prompt(name="Molding Location",prompt_type='DISTANCE',value=unit.inch(-24),tab_index=1)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Extend_Left = self.get_var('Extend To Left Panel','Extend_Left')        
        Extend_Right = self.get_var('Extend To Right Panel','Extend_Right')      
        Panel_Thickness = self.get_var('Panel Thickness')
        Extend_Left_Amount = self.get_var('Extend Left Amount')
        Extend_Right_Amount = self.get_var('Extend Right Amount')
        Front_Overhang = self.get_var('Front Overhang')
        Return_Left = self.get_var('Return Left')
        Return_Right = self.get_var('Return Right')
        Exposed_Left = self.get_var('Exposed Left')
        Exposed_Right = self.get_var('Exposed Right')
        Exposed_Back = self.get_var('Exposed Back')
        Molding_Height = self.get_var('Molding Height')
        Molding_Location = self.get_var('Molding Location')
        
        flat_crown = common_parts.add_flat_crown(self)
        flat_crown.obj_bp.mv.comment_2 = "1040"
        flat_crown.set_name("Flat Valance")
        flat_crown.x_loc('IF(Extend_Left,0,Panel_Thickness/2)-Extend_Left_Amount',[Extend_Left,Extend_Left_Amount,Panel_Thickness])
        flat_crown.y_loc('-Depth-Front_Overhang+Panel_Thickness', [Depth,Front_Overhang,Panel_Thickness])
        flat_crown.z_loc('Molding_Location',[Molding_Location])
        flat_crown.x_rot(value = -90)
        flat_crown.y_rot(value = 0)
        flat_crown.z_rot(value = 0)
        flat_crown.x_dim('Width-IF(Extend_Left,0,Panel_Thickness/2)-IF(Extend_Right,0,Panel_Thickness/2)+Extend_Left_Amount+Extend_Right_Amount',
                  [Width,Extend_Left,Extend_Right,Panel_Thickness,Extend_Right_Amount,Extend_Left_Amount])
        flat_crown.y_dim('Molding_Height',[Molding_Height])
        flat_crown.z_dim('-Panel_Thickness',[Panel_Thickness])
        flat_crown.prompt('Exposed Left','Exposed_Left',[Exposed_Left])
        flat_crown.prompt('Exposed Right','Exposed_Right',[Exposed_Right])
        flat_crown.prompt('Exposed Back','Exposed_Back',[Exposed_Back])
        
        left_return = common_parts.add_cleat(self)
        left_return.obj_bp.mv.comment_2 = "1040"
        left_return.set_name("Left")
        left_return.x_loc('Panel_Thickness-Extend_Left_Amount', [Panel_Thickness,Extend_Left_Amount])
        left_return.y_loc('-Depth-Front_Overhang+Panel_Thickness', [Depth,Front_Overhang,Panel_Thickness])
        left_return.z_loc('Molding_Location-Molding_Height',[Molding_Location,Molding_Height])
        left_return.x_rot(value = 90)
        left_return.y_rot(value = 0)
        left_return.z_rot(value = 90)
        left_return.x_dim('Depth-Panel_Thickness+Front_Overhang', [Depth,Panel_Thickness,Front_Overhang])
        left_return.y_dim('Molding_Height', [Molding_Height])
        left_return.z_dim('-Panel_Thickness', [Panel_Thickness])
        left_return.prompt('Hide','IF(Return_Left,False,True)',[Return_Left])
        
        right_return = common_parts.add_cleat(self)
        right_return.obj_bp.mv.comment_2 = "1040"
        right_return.set_name("Right")
        right_return.x_loc('Width+Extend_Right_Amount', [Width,Extend_Right_Amount])
        right_return.y_loc('-Depth-Front_Overhang+Panel_Thickness', [Depth,Front_Overhang,Panel_Thickness])
        right_return.z_loc('Molding_Location-Molding_Height',[Molding_Location,Molding_Height])
        right_return.x_rot(value = 90)
        right_return.y_rot(value = 0)
        right_return.z_rot(value = 90)
        right_return.x_dim('Depth-Panel_Thickness+Front_Overhang', [Depth,Panel_Thickness,Front_Overhang])
        right_return.y_dim('Molding_Height', [Molding_Height])
        right_return.z_dim('-Panel_Thickness', [Panel_Thickness])
        right_return.prompt('Hide','IF(Return_Right,False,True)',[Return_Right])
        
        self.update()               
        
class PROMPTS_Prompts_Bottom_Support(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".top_molding"
    bl_label = "Top Prompts"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    insert = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        etc = self.insert.get_prompt("Extend To Ceiling")
        if etc:
            if(self.insert.get_prompt("Molding Height").value() < unit.inch(3) or etc.value()):
                self.insert.get_prompt("Exposed Back").set_value(False)
    
        dfc = self.insert.get_prompt("Distance From Ceiling")
        if(etc):
            if(etc.value()):
                parent_assembly = fd_types.Assembly(self.insert.obj_bp.parent)
                if(dfc):
                    if(parent_assembly.obj_bp.parent):
                        for child in parent_assembly.obj_bp.parent.children:
                            if(child.mv.type == "VPDIMZ"):
                                dfc.set_value(child.location[2] - parent_assembly.obj_z.location.z)
                                print(dfc.value())
                tkdhd = self.insert.get_prompt('Top KD Holes Down')
                for i in range(0, 9):
                    remove_top_shelf = parent_assembly.get_prompt('Remove Top Shelf ' + str(i))
                    top_KD_vertical_offset = parent_assembly.get_prompt("Top KD " + str(i) + ' Vertical Offset')
                    if(remove_top_shelf and top_KD_vertical_offset):
                        remove_top_shelf.set_value(True)
                        if(tkdhd):
                            if(tkdhd.value() == "One"):
                                top_KD_vertical_offset.set_value(unit.inch(1.26))
                            elif(tkdhd.value() == "Two"):
                                top_KD_vertical_offset.set_value(unit.inch(2.56))
                            else:
                                top_KD_vertical_offset.set_value(0)
            else:
                for i in range(0, 9):
                    parent_assembly = fd_types.Assembly(self.insert.obj_bp.parent)
                    top_KD_vertical_offset = parent_assembly.get_prompt("Top KD " + str(i) + ' Vertical Offset')
                    if(top_KD_vertical_offset):
                        top_KD_vertical_offset.set_value(0)

        props_closet.update_render_materials(self, context)

#         self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
#         self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.insert = self.get_insert()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))
        
    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(self.insert.obj_bp.mv.name_object)
        box = layout.box()
        
        molding_height = self.insert.get_prompt("Molding Height")
        extend_to_ceiling = self.insert.get_prompt("Extend To Ceiling")
        extend_left = self.insert.get_prompt("Extend To Left Panel")
        extend_right = self.insert.get_prompt("Extend To Right Panel")
        exposed_left = self.insert.get_prompt("Exposed Left")
        exposed_right = self.insert.get_prompt("Exposed Right")
        return_left = self.insert.get_prompt("Return Left")
        return_right = self.insert.get_prompt("Return Right")      
        exposed_back = self.insert.get_prompt("Exposed Back")      
        extend_left_amount = self.insert.get_prompt("Extend Left Amount")
        extend_right_amount = self.insert.get_prompt("Extend Right Amount")
        front_overhang = self.insert.get_prompt("Front Overhang")
        top_shelf = self.insert.get_prompt("Top Shelf")
        molding_location = self.insert.get_prompt('Molding Location')
        tkdhd = self.insert.get_prompt('Top KD Holes Down')
        
        
#         row = box.row()
#         row.label("Width")
#         row.prop(self.insert.obj_x,'location',index=0,text="")
        if(extend_to_ceiling):
            row = box.row()
            extend_to_ceiling.draw_prompt(row)
            if(extend_to_ceiling.value() and fd_types.Assembly(self.insert.obj_bp.parent).get_prompt("Top KD 1 Vertical Offset")):
                row = box.row()
                tkdhd.draw_prompt(row,text="Top KD Holes Down: ", split_text=True)
            else:
                row = box.row()
                molding_height.draw_prompt(row)
                row = box.row()
                molding_location.draw_prompt(row)
        else:
            row = box.row()
            molding_height.draw_prompt(row)
            row = box.row()
            molding_location.draw_prompt(row)
#         row = box.row()
#         top_shelf.draw_prompt(row)        
                
#         row = box.row()
#         row.label("Full Overlay Panel:")
#         extend_left.draw_prompt(row,text="Left",split_text=False)
#         extend_right.draw_prompt(row,text="Right",split_text=False)
        row = box.row()
        row.label("Extend Ends")
        extend_left_amount.draw_prompt(row,text="Left",split_text=False)
        extend_right_amount.draw_prompt(row,text="Right",split_text=False)
        row = box.row()
        row.label("Exposed Edges")
        exposed_left.draw_prompt(row,text="Left",split_text=False)
        exposed_right.draw_prompt(row,text="Right",split_text=False)
        if extend_to_ceiling:
            if(molding_height.value() >= unit.inch(3) and extend_to_ceiling.value() == False ):
                exposed_back.draw_prompt(row,text="Top",split_text=False)    
        else:
            exposed_back.draw_prompt(row,text="Top",split_text=False)  
        row = box.row()
        row.label("End Returns")
        return_left.draw_prompt(row,text="Left Return",split_text=False)
        return_right.draw_prompt(row,text="Right Return",split_text=False)
        row = box.row()
        front_overhang.draw_prompt(row)

bpy.utils.register_class(PROMPTS_Prompts_Bottom_Support)

class DROP_OPERATOR_Place_Top(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".top_drop"
    bl_label = "Place Top"
    bl_description = "This places the top."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    product = None
    
    selected_panel = None
    
    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.product = fd_types.Assembly(bp)
        utils.set_wireframe(self.product.obj_bp,True)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.product:
            utils.delete_object_and_children(self.product.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def get_distance_between_panels(self,panel_1,panel_2):
        
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
        
        return utils.calc_distance((x1,y1,z1),(x2,y2,z1))  #DONT CALCULATE Z DIFFERENCE

    def product_drop(self,context,event):
        selected_panel = None
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        
        sel_product_bp = utils.get_bp(selected_obj,'PRODUCT')
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)
        
        if sel_assembly_bp:
            props = props_closet.get_object_props(sel_assembly_bp)
            if props.is_panel_bp:
                selected_obj.select = True
                selected_panel = fd_types.Assembly(sel_assembly_bp)
                
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel:
            selected_panel = fd_types.Assembly(sel_assembly_bp)
            utils.set_wireframe(self.product.obj_bp,False)
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            context.scene.objects.active = self.product.obj_bp
            self.product.obj_bp.select = True
            dist = self.get_distance_between_panels(self.selected_panel, selected_panel)
            self.product.obj_x.location.x = dist
            self.product.obj_bp.mv.type_group = 'INSERT'
            self.product.obj_bp.location.z = self.selected_panel.obj_bp.location.z + self.selected_panel.obj_x.location.x
            if(math.fabs(self.selected_panel.obj_y.location.y) <= math.fabs(selected_panel.obj_y.location.y)):
                self.product.obj_y.location.y = math.fabs(self.selected_panel.obj_y.location.y)
            else:
                self.product.obj_y.location.y = math.fabs(selected_panel.obj_y.location.y)
            for child in self.product.obj_bp.parent.children:
                if not child.hide:
                    if(child.mv.type == 'BPASSEMBLY'):
                        if(child.lm_closets.is_closet_top_bp):
                            ts_assembly = fd_types.Assembly(child)
                            ts_overhang  = ts_assembly.get_prompt("Front Overhang")
                            fc_overhang = self.product.get_prompt("Front Overhang")
                            self.product.obj_y.location.y = math.fabs(ts_assembly.obj_y.location.y)
                            if(ts_overhang and fc_overhang):
                                fc_overhang.set_value(ts_overhang.value())


            return {'FINISHED'}
            
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel == None:
            self.selected_panel = selected_panel
            utils.set_wireframe(self.product.obj_bp,False)
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            context.scene.objects.active = self.product.obj_bp
            self.product.obj_bp.parent = sel_product_bp
            
            if self.selected_panel.obj_z.location.z > 0:
                #CENTER OR RIGHT PANEL SELECTED
                self.product.obj_bp.location = self.selected_panel.obj_bp.location
                self.product.obj_bp.location.x -= self.selected_panel.obj_z.location.z
            else:
                #LEFT PANEL SELECTED
                self.product.obj_bp.location = self.selected_panel.obj_bp.location
            
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.product_drop(context,event)      

bpy.utils.register_class(DROP_OPERATOR_Place_Top)