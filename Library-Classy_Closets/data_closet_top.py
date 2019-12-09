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

class Top(fd_types.Assembly):
    """ Base Cabinet Standard
    """

    property_id = props_closet.LIBRARY_NAME_SPACE + ".top"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".top_drop"
    
    type_assembly = "PRODUCT"
    mirror_y = True
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_closet_top_bp = True
        
        self.add_tab(name='Top Options',tab_type='VISIBLE') #1
        self.add_prompt(name="Extend To Left Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Extend To Right Panel",prompt_type='CHECKBOX',value=True,tab_index=1)
        self.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Extend Left Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Extend Right Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Front Overhang",prompt_type='DISTANCE',value=unit.inch(.5),tab_index=1)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Extend_Left = self.get_var('Extend To Left Panel','Extend_Left')        
        Extend_Right = self.get_var('Extend To Right Panel','Extend_Right')      
        Panel_Thickness = self.get_var('Panel Thickness')
        Extend_Left_Amount = self.get_var('Extend Left Amount')
        Extend_Right_Amount = self.get_var('Extend Right Amount')
        Front_Overhang = self.get_var('Front Overhang')
        Exposed_Left = self.get_var('Exposed Left')
        Exposed_Right = self.get_var('Exposed Right')
        Exposed_Back = self.get_var('Exposed Back')
        
        top = common_parts.add_plant_on_top(self)
        top.obj_bp.mv.comment_2 = "1024"
        top.set_name("Top")
        top.x_loc('IF(Extend_Left,0,Panel_Thickness/2)-Extend_Left_Amount',[Extend_Left,Extend_Left_Amount,Panel_Thickness])
        top.y_loc(value = 0)
        top.z_loc(value = 0)
        top.x_rot(value = 180)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.x_dim('Width-IF(Extend_Left,0,Panel_Thickness/2)-IF(Extend_Right,0,Panel_Thickness/2)+Extend_Left_Amount+Extend_Right_Amount',
                  [Width,Extend_Left,Extend_Right,Panel_Thickness,Extend_Right_Amount,Extend_Left_Amount])
        top.y_dim('Depth+Front_Overhang',[Depth,Front_Overhang])
        top.z_dim('-Panel_Thickness',[Panel_Thickness])
        top.prompt('Exposed Left','Exposed_Left',[Exposed_Left])
        top.prompt('Exposed Right','Exposed_Right',[Exposed_Right])
        top.prompt('Exposed Back','Exposed_Back',[Exposed_Back])
        
        self.update()
        
class PROMPTS_Prompts_Bottom_Support(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".top"
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
        
        extend_left = self.insert.get_prompt("Extend To Left Panel")
        extend_right = self.insert.get_prompt("Extend To Right Panel")
        exposed_left = self.insert.get_prompt("Exposed Left")
        exposed_right = self.insert.get_prompt("Exposed Right")      
        exposed_back = self.insert.get_prompt("Exposed Back")      
        extend_left_amount = self.insert.get_prompt("Extend Left Amount")
        extend_right_amount = self.insert.get_prompt("Extend Right Amount")
        front_overhang = self.insert.get_prompt("Front Overhang")
               
#         row = box.row()
#         row.label("Width:")
#         row.prop(self.insert.obj_x,'location',index=0,text="")

        row = box.row()
        extend_left_amount.draw_prompt(row,text="Extend Left:",split_text=True)
        row = box.row()
        extend_right_amount.draw_prompt(row,text="Extend Right:",split_text=True)
        
        row = box.row()
        front_overhang.draw_prompt(row,text="Extend Front:",split_text=True)
        
        row = box.row()
        row.label("Exposed Edges:")
        exposed_left.draw_prompt(row,text="Left",split_text=False)
        exposed_right.draw_prompt(row,text="Right",split_text=False)       
        exposed_back.draw_prompt(row,text="Back",split_text=False)    

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
            self.product.obj_y.location.y = math.fabs(self.selected_panel.obj_y.location.y)
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