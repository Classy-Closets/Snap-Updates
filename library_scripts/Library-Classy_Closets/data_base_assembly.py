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
        self.add_prompt(name="Extend Depth Amount",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Variable Width",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Variable Height",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Is Island TK",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="TK Skin Thickness",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=1)
        self.add_prompt(name="Has TK Skin",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Left Return",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Right Return",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Deeper TK Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Deeper TK Right",prompt_type='CHECKBOX',value=False,tab_index=1)

        Width = self.get_var('dim_x',"Width")
        Depth = self.get_var('dim_y',"Depth")
        Height = self.get_var('dim_z',"Height")
        Cleat_Width = self.get_var('Cleat Width')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')
        Extend_Left_Amount = self.get_var('Extend Left Amount')
        Extend_Right_Amount = self.get_var('Extend Right Amount')
        Extend_Depth_Amount = self.get_var('Extend Depth Amount')
        TK_Skin_Thickness = self.get_var("TK Skin Thickness")
        Has_TK_Skin = self.get_var("Has TK Skin")
        Left_Return = self.get_var("Left Return")
        Right_Return = self.get_var("Right Return")
        DTKL = self.get_var("Deeper TK Left",'DTKL')
        DTKR = self.get_var("Deeper TK Right",'DTKR')
        
        toe_kick_front = common_parts.add_toe_kick(self)
        toe_kick_front.set_name("Toe Kick Front")
        toe_kick_front.obj_bp.mv.comment_2 = "1034"
        toe_kick_front.x_dim('Width-(Toe_Kick_Thickness*3)+Extend_Left_Amount+Extend_Right_Amount-IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))-IF(DTKR,-TK_Skin_Thickness,IF(Right_Return,TK_Skin_Thickness,0))',[Width,Toe_Kick_Thickness,Extend_Right_Amount,Extend_Left_Amount,Left_Return,Right_Return,TK_Skin_Thickness,DTKL,DTKR])
        toe_kick_front.y_dim('-Height',[Height])
        toe_kick_front.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_front.x_loc('(Toe_Kick_Thickness*1.5)-Extend_Left_Amount+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))',[Toe_Kick_Thickness,Extend_Left_Amount,TK_Skin_Thickness,Left_Return,DTKL])
        toe_kick_front.y_loc('Depth-Extend_Depth_Amount',[Depth,Extend_Depth_Amount])
        toe_kick_front.z_loc(value = 0)
        toe_kick_front.x_rot(value = -90)
        toe_kick_front.y_rot(value = 0)
        toe_kick_front.z_rot(value = 0)
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.set_name("Toe Kick Back")
        toe_kick.obj_bp.mv.comment_2 = "1034"
        toe_kick.x_dim('Width-(Toe_Kick_Thickness*3)+Extend_Left_Amount+Extend_Right_Amount-IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))-IF(DTKR,-TK_Skin_Thickness,IF(Right_Return,TK_Skin_Thickness,0))',[Width,Toe_Kick_Thickness,Extend_Left_Amount,Extend_Right_Amount,Left_Return,Right_Return,TK_Skin_Thickness,DTKL,DTKR])
        toe_kick.y_dim('-Height',[Height])
        toe_kick.z_dim('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick.x_loc('(Toe_Kick_Thickness*1.5)-Extend_Left_Amount+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))',[Extend_Left_Amount,Toe_Kick_Thickness,TK_Skin_Thickness,Left_Return,DTKL])
        toe_kick.y_loc(value = 0)
        toe_kick.z_loc(value = 0)
        toe_kick.x_rot(value = -90)
        toe_kick.y_rot(value = 0)
        toe_kick.z_rot(value = 0)        
        
        left_toe_kick = common_parts.add_toe_kick_end_cap(self)
        left_toe_kick.x_dim('-Depth+Extend_Depth_Amount',[Depth,Extend_Depth_Amount])
        left_toe_kick.y_dim('-Height',[Height])
        left_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        left_toe_kick.y_loc(value = 0)
        left_toe_kick.x_loc('-Extend_Left_Amount+(Toe_Kick_Thickness/2)+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))',[Extend_Left_Amount,Toe_Kick_Thickness,Left_Return,TK_Skin_Thickness,DTKL])
        left_toe_kick.z_loc(value = 0)
        left_toe_kick.x_rot(value = -90)
        left_toe_kick.y_rot(value = 0)
        left_toe_kick.z_rot(value = -90)        
        
        right_toe_kick = common_parts.add_toe_kick_end_cap(self)
        right_toe_kick.x_dim('-Depth+Extend_Depth_Amount',[Depth,Extend_Depth_Amount])
        right_toe_kick.y_dim('Height',[Height])
        right_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        right_toe_kick.y_loc(value = 0)
        right_toe_kick.x_loc('Width+Extend_Right_Amount-(Toe_Kick_Thickness/2)-IF(DTKR,-TK_Skin_Thickness,IF(Right_Return,TK_Skin_Thickness,0))',[Extend_Right_Amount,Width,Toe_Kick_Thickness,Right_Return,TK_Skin_Thickness,DTKR])
        right_toe_kick.z_loc(value = 0)
        right_toe_kick.x_rot(value = 90)
        right_toe_kick.y_rot(value = 0)
        right_toe_kick.z_rot(value = -90)
        
        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        toe_kick_stringer.x_dim('Width-(Toe_Kick_Thickness*3)+Extend_Left_Amount+Extend_Right_Amount-IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))-IF(DTKR,-TK_Skin_Thickness,IF(Right_Return,TK_Skin_Thickness,0))',[Extend_Left_Amount,Extend_Right_Amount,Width,Toe_Kick_Thickness,Left_Return,Right_Return,TK_Skin_Thickness,DTKL,DTKR])
        toe_kick_stringer.y_dim('Cleat_Width',[Cleat_Width])
        toe_kick_stringer.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_stringer.x_loc('(Toe_Kick_Thickness*1.5)-Extend_Left_Amount+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))',[Extend_Left_Amount,Toe_Kick_Thickness,TK_Skin_Thickness,Left_Return,DTKL])
        toe_kick_stringer.y_loc('Depth+Toe_Kick_Thickness-Extend_Depth_Amount',[Depth,Toe_Kick_Thickness,Extend_Depth_Amount])
        toe_kick_stringer.z_loc('Height-Toe_Kick_Thickness',[Height,Toe_Kick_Thickness])
        toe_kick_stringer.x_rot(value = 0)
        toe_kick_stringer.y_rot(value = 0)
        toe_kick_stringer.z_rot(value = 0)
        
        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        toe_kick_stringer.x_dim('Width-(Toe_Kick_Thickness*3)+Extend_Left_Amount+Extend_Right_Amount-IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))-IF(DTKR,-TK_Skin_Thickness,IF(Right_Return,TK_Skin_Thickness,0))',[Extend_Left_Amount,Extend_Right_Amount,Width,Toe_Kick_Thickness,Left_Return,Right_Return,TK_Skin_Thickness,DTKL,DTKR])
        toe_kick_stringer.y_dim('-Cleat_Width',[Cleat_Width])
        toe_kick_stringer.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_stringer.x_loc('(Toe_Kick_Thickness*1.5)-Extend_Left_Amount+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))',[Extend_Left_Amount,Toe_Kick_Thickness,TK_Skin_Thickness,Left_Return,DTKL])
        toe_kick_stringer.y_loc('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_stringer.z_loc(value = 0)
        toe_kick_stringer.x_rot(value = 0)
        toe_kick_stringer.y_rot(value = 0)
        toe_kick_stringer.z_rot(value = 0)  

        toe_kick_skin = common_parts.add_toe_kick_skin(self)
        toe_kick_skin.x_dim('Width-(Toe_Kick_Thickness)+Extend_Left_Amount+Extend_Right_Amount+IF(AND(DTKL,Left_Return),TK_Skin_Thickness,0)+IF(AND(DTKR,Right_Return),TK_Skin_Thickness,0)',[Width,Toe_Kick_Thickness,Extend_Right_Amount,Extend_Left_Amount,DTKL,DTKR,TK_Skin_Thickness,Left_Return,Right_Return])
        toe_kick_skin.y_dim('-Height',[Height])
        toe_kick_skin.z_dim('TK_Skin_Thickness',[TK_Skin_Thickness])
        toe_kick_skin.x_loc('(Toe_Kick_Thickness*0.5)-Extend_Left_Amount-IF(AND(DTKL,Left_Return),TK_Skin_Thickness,0)',[Toe_Kick_Thickness,Extend_Left_Amount,DTKL,TK_Skin_Thickness,Left_Return]) 
        toe_kick_skin.y_loc('Depth-Extend_Depth_Amount-TK_Skin_Thickness',[Depth,Extend_Depth_Amount,TK_Skin_Thickness])
        toe_kick_skin.z_loc(value = 0)
        toe_kick_skin.x_rot(value = -90)
        toe_kick_skin.y_rot(value = 0)
        toe_kick_skin.z_rot(value = 0)
        toe_kick_skin.prompt('Hide',"IF(Has_TK_Skin,False,True)",[Has_TK_Skin])

        left_skin_return = common_parts.add_toe_kick_skin(self)
        left_skin_return.set_name("Toe Kick Skin Left Return")
        left_skin_return.x_dim('-Depth+Extend_Depth_Amount',[Depth,Extend_Depth_Amount])
        left_skin_return.y_dim('-Height',[Height])
        left_skin_return.z_dim('TK_Skin_Thickness',[TK_Skin_Thickness])
        left_skin_return.x_loc('-Extend_Left_Amount+(Toe_Kick_Thickness/2)-IF(DTKL,TK_Skin_Thickness,0)',[Extend_Left_Amount,Toe_Kick_Thickness,DTKL,TK_Skin_Thickness])
        left_skin_return.y_loc(value = 0)
        left_skin_return.z_loc(value = 0)
        left_skin_return.z_loc(value = 0)
        left_skin_return.x_rot(value = -90)
        left_skin_return.y_rot(value = 0)
        left_skin_return.z_rot(value = -90)
        left_skin_return.prompt('Hide',"IF(Left_Return,False,True)",[Left_Return])

        right_skin_return = common_parts.add_toe_kick_skin(self)
        right_skin_return.set_name("Toe Kick Skin Right Return")
        right_skin_return.x_dim('-Depth+Extend_Depth_Amount',[Depth,Extend_Depth_Amount])
        right_skin_return.y_dim('-Height',[Height])
        right_skin_return.z_dim('TK_Skin_Thickness',[TK_Skin_Thickness])
        right_skin_return.x_loc('Width+Extend_Right_Amount-(Toe_Kick_Thickness/2)-IF(DTKR,0,TK_Skin_Thickness)',[Extend_Right_Amount,Width,Toe_Kick_Thickness,TK_Skin_Thickness,DTKR])
        right_skin_return.y_loc(value = 0)
        right_skin_return.z_loc(value = 0)
        right_skin_return.z_loc(value = 0)
        right_skin_return.x_rot(value = -90)
        right_skin_return.y_rot(value = 0)
        right_skin_return.z_rot(value = -90)
        right_skin_return.prompt('Hide',"IF(Right_Return,False,True)",[Right_Return])
         
        
    def draw(self):
        self.create_assembly()    
        self.obj_bp.mv.export_as_subassembly = True
        self.obj_bp.lm_closets.is_toe_kick_insert_bp = True
        
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

        ex_depth_amount = self.product.get_prompt("Extend Depth Amount")
        ex_depth_amount.draw_prompt(box)

        variable_width = self.product.get_prompt("Variable Width")
        variable_width.draw_prompt(box)

        variable_height = self.product.get_prompt("Variable Height")
        variable_height.draw_prompt(box)

        has_tk_skin = self.product.get_prompt("Has TK Skin")
        left_return = self.product.get_prompt("Left Return")
        right_return = self.product.get_prompt("Right Return")
        deeper_tk_left = self.product.get_prompt("Deeper TK Left")
        deeper_tk_right = self.product.get_prompt("Deeper TK Right")
        
        if(has_tk_skin):
            box = layout.box()
            box.label('1/4" Toe Kick Skin Options')
            row = box.row()
            has_tk_skin.draw_prompt(row,text = 'Add 1/4" Toe Kick Skin: ')
            if(has_tk_skin.value()):
                if(left_return and right_return):
                    row = box.row()
                    row.label('1/4" Skin Returns')
                    left_return.draw_prompt(row,split_text=False)
                    right_return.draw_prompt(row,split_text=False)
                    row = box.row()
                    row.label('Deeper Adjacent Toe Kicks: ')
                    deeper_tk_left.draw_prompt(row,text='Left',split_text=False)
                    deeper_tk_right.draw_prompt(row,text='Right',split_text=False)
        
class DROP_OPERATOR_Place_Base_Assembly(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_base_assembly"
    bl_label = "Place Base Assembly"
    bl_description = "This places the base assembly"
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    product = None
    
    selected_panel_1 = None
    
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
        selected_panel_2 = None
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        
        sel_product_bp = utils.get_bp(selected_obj,'PRODUCT')
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)
        
        if sel_assembly_bp:
            props = props_closet.get_object_props(sel_assembly_bp)
            if props.is_panel_bp:
                selected_obj.select = True
                selected_panel_2 = fd_types.Assembly(sel_assembly_bp)
                
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel_1:
            selected_panel_2 = fd_types.Assembly(sel_assembly_bp)
            if selected_panel_2 and selected_panel_2.obj_bp:
                utils.set_wireframe(self.product.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.product.obj_bp
                self.product.obj_bp.select = True

                panel_1_bp = self.selected_panel_1.obj_bp
                carcass_product_bp = utils.get_parent_assembly_bp(panel_1_bp)
                carcass_assembly = fd_types.Assembly(carcass_product_bp)
                
                Toe_Kick_Setback = carcass_assembly.get_var("Toe Kick Setback")
                Panel_Thickness = carcass_assembly.get_var("Panel Thickness")
                P1_X_Loc = self.selected_panel_1.get_var('loc_x','P1_X_Loc')
                P2_X_Loc = selected_panel_2.get_var('loc_x','P2_X_Loc')

                self.product.x_loc('IF(P1_X_Loc>0,P1_X_Loc-Panel_Thickness,0)',[P1_X_Loc,Panel_Thickness])
                self.product.x_dim('P2_X_Loc-IF(P1_X_Loc>0,P1_X_Loc-Panel_Thickness,0)',[P1_X_Loc,P2_X_Loc,Panel_Thickness])

                panel_depth_1 = abs(self.selected_panel_1.obj_y.location.y)
                panel_depth_2 = abs(selected_panel_2.obj_y.location.y)
                Panel_Depth_1 = self.selected_panel_1.get_var('dim_y', 'Panel_Depth_1')
                Panel_Depth_2 = selected_panel_2.get_var('dim_y', 'Panel_Depth_2')

                if panel_depth_1 > panel_depth_2:
                    self.product.y_dim('Panel_Depth_2+Toe_Kick_Setback',[Panel_Depth_2,Toe_Kick_Setback])
                else:
                    self.product.y_dim('Panel_Depth_1+Toe_Kick_Setback',[Panel_Depth_1,Toe_Kick_Setback])

                self.product.obj_bp.mv.type_group = 'INSERT'
                self.product.obj_bp.location.z = 0

                return {'FINISHED'}
            else:
                return {'RUNNING_MODAL'}
            
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel_1 == None:
            self.selected_panel_1 = selected_panel_2
            if self.selected_panel_1 and self.selected_panel_1.obj_bp:
                utils.set_wireframe(self.product.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.product.obj_bp
                self.product.obj_bp.parent = sel_product_bp
                
                if self.selected_panel_1.obj_z.location.z > 0:
                    #CENTER OR RIGHT PANEL SELECTED
                    self.product.obj_bp.location = self.selected_panel_1.obj_bp.location
                    self.product.obj_bp.location.x -= self.selected_panel_1.obj_z.location.z
                else:
                    #LEFT PANEL SELECTED
                    self.product.obj_bp.location = self.selected_panel_1.obj_bp.location
                    
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