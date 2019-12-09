import bpy
import math
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts

class Base_Assembly(fd_types.Assembly):
    
    property_id = props_closet.LIBRARY_NAME_SPACE + ".toe_kick_prompts"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_base_assembly"
    type_assembly = "PRODUCT"

    def add_parts(self):
        
        self.add_prompt(name="Cleat Width",prompt_type='DISTANCE',value=unit.inch(2.5),tab_index=1)
        self.add_prompt(name="Extend Left Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Extend Right Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Variable Height",prompt_type='CHECKBOX',value=False,tab_index=1)
                
        Width = self.get_var('dim_x',"Width")
        Depth = self.get_var('dim_y',"Depth")
        Height = self.get_var('dim_z',"Height")
        Cleat_Width = self.get_var('Cleat Width')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')
        Extend_Left_Amount = self.get_var('Extend Left Amount')
        Extend_Right_Amount = self.get_var('Extend Right Amount')
        
        toe_kick_front = common_parts.add_toe_kick(self)
        toe_kick_front.obj_bp.mv.comment_2 = "1034"
        toe_kick_front.x_dim('Width-(Toe_Kick_Thickness*2)+Extend_Left_Amount+Extend_Right_Amount',[Width,Toe_Kick_Thickness,Extend_Right_Amount,Extend_Left_Amount])
        toe_kick_front.y_dim('-Height',[Height])
        toe_kick_front.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_front.x_loc('Toe_Kick_Thickness-Extend_Left_Amount',[Toe_Kick_Thickness,Extend_Left_Amount])
        toe_kick_front.y_loc('Depth',[Depth])
        toe_kick_front.z_loc(value = 0)
        toe_kick_front.x_rot(value = -90)
        toe_kick_front.y_rot(value = 0)
        toe_kick_front.z_rot(value = 0)
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.obj_bp.mv.comment_2 = "1034"
        toe_kick.x_dim('Width-(Toe_Kick_Thickness*2)+Extend_Left_Amount+Extend_Right_Amount',[Width,Toe_Kick_Thickness,Extend_Left_Amount,Extend_Right_Amount])
        toe_kick.y_dim('-Height',[Height])
        toe_kick.z_dim('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick.x_loc('Toe_Kick_Thickness-Extend_Left_Amount',[Extend_Left_Amount,Toe_Kick_Thickness])
        toe_kick.y_loc(value = 0)
        toe_kick.z_loc(value = 0)
        toe_kick.x_rot(value = -90)
        toe_kick.y_rot(value = 0)
        toe_kick.z_rot(value = 0)        
        
        left_toe_kick = common_parts.add_toe_kick(self)
        left_toe_kick.obj_bp.mv.comment_2 = "1033"
        left_toe_kick.x_dim('-Depth',[Depth])
        left_toe_kick.y_dim('-Height',[Height])
        left_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        left_toe_kick.y_loc(value = 0)
        left_toe_kick.x_loc('-Extend_Left_Amount',[Extend_Left_Amount])
        left_toe_kick.z_loc(value = 0)
        left_toe_kick.x_rot(value = -90)
        left_toe_kick.y_rot(value = 0)
        left_toe_kick.z_rot(value = -90)        
        
        right_toe_kick = common_parts.add_toe_kick(self)
        right_toe_kick.obj_bp.mv.comment_2 = "1033"
        right_toe_kick.x_dim('-Depth',[Depth])
        right_toe_kick.y_dim('Height',[Height])
        right_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        right_toe_kick.y_loc(value = 0)
        right_toe_kick.x_loc('Width+Extend_Right_Amount',[Extend_Right_Amount,Width,Toe_Kick_Thickness])
        right_toe_kick.z_loc(value = 0)
        right_toe_kick.x_rot(value = 90)
        right_toe_kick.y_rot(value = 0)
        right_toe_kick.z_rot(value = -90)
        
        toe_kick_cleat = common_parts.add_cleat(self)
        toe_kick_cleat.obj_bp.mv.comment_2 = "1035"
        toe_kick_cleat.x_dim('Width-(Toe_Kick_Thickness*2)+Extend_Left_Amount+Extend_Right_Amount',[Extend_Left_Amount,Extend_Right_Amount,Width,Toe_Kick_Thickness])
        toe_kick_cleat.y_dim('Cleat_Width',[Cleat_Width])
        toe_kick_cleat.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_cleat.x_loc('Toe_Kick_Thickness-Extend_Left_Amount',[Extend_Left_Amount,Toe_Kick_Thickness])
        toe_kick_cleat.y_loc('Depth+Toe_Kick_Thickness',[Depth,Toe_Kick_Thickness])
        toe_kick_cleat.z_loc('Height-Toe_Kick_Thickness',[Height,Toe_Kick_Thickness])
        toe_kick_cleat.x_rot(value = 0)
        toe_kick_cleat.y_rot(value = 0)
        toe_kick_cleat.z_rot(value = 0)
        
        toe_kick_cleat = common_parts.add_cleat(self)
        toe_kick_cleat.obj_bp.mv.comment_2 = "1035"
        toe_kick_cleat.x_dim('Width-(Toe_Kick_Thickness*2)+Extend_Left_Amount+Extend_Right_Amount',[Extend_Left_Amount,Extend_Right_Amount,Width,Toe_Kick_Thickness])
        toe_kick_cleat.y_dim('-Cleat_Width',[Cleat_Width])
        toe_kick_cleat.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_cleat.x_loc('Toe_Kick_Thickness-Extend_Left_Amount',[Extend_Left_Amount,Toe_Kick_Thickness])
        toe_kick_cleat.y_loc('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_cleat.z_loc(value = 0)
        toe_kick_cleat.x_rot(value = 0)
        toe_kick_cleat.y_rot(value = 0)
        toe_kick_cleat.z_rot(value = 0)           
        
    def draw(self):
        self.create_assembly()    
        self.obj_bp.mv.export_as_subassembly = True
        
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        self.add_parts()
        
        self.update()
        
        
class PROMPTS_Toe_Kick_Prompts(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".toe_kick_prompts"
    bl_label = "Toe Kick Prompts"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.product = self.get_insert()
        self.depth = math.fabs(self.product.obj_y.location.y)
        self.height = math.fabs(self.product.obj_z.location.z)
        self.width = math.fabs(self.product.obj_x.location.x)           
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(500))
        
    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(self.product.obj_bp.mv.name_object)
        self.draw_product_size(layout)
        
        box = layout.box()
        ex_left_amount = self.product.get_prompt("Extend Left Amount")
        ex_left_amount.draw_prompt(box)

        ex_right_amount = self.product.get_prompt("Extend Right Amount")
        ex_right_amount.draw_prompt(box)

        variable_height = self.product.get_prompt("Variable Height")
        variable_height.draw_prompt(box)
        
class DROP_OPERATOR_Place_Base_Assembly(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_base_assembly"
    bl_label = "Place Base Assembly"
    bl_description = "This places the base assembly"
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
            if selected_panel and selected_panel.obj_bp:
                utils.set_wireframe(self.product.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.product.obj_bp
                self.product.obj_bp.select = True
                dist = self.get_distance_between_panels(self.selected_panel, selected_panel)
                self.product.obj_x.location.x = dist
                self.product.obj_bp.mv.type_group = 'INSERT'
                self.product.obj_bp.location.z = 0
                self.product.obj_y.location.y = self.selected_panel.obj_y.location.y + unit.inch(2.5)
                return {'FINISHED'}
            else:
                return {'RUNNING_MODAL'}
            
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel == None:
            self.selected_panel = selected_panel
            if self.selected_panel and self.selected_panel.obj_bp:
                utils.set_wireframe(self.product.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.product.obj_bp
                self.product.obj_bp.parent = sel_product_bp
#                 self.product.obj_bp.parent = sel_product_bp.parent
#                 self.product.obj_bp.location.x = selected_panel.obj_bp.location.x
                
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

bpy.utils.register_class(DROP_OPERATOR_Place_Base_Assembly)
bpy.utils.register_class(PROMPTS_Toe_Kick_Prompts)    