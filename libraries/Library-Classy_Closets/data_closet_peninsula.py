import bpy
import math
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

class Peninsula_Carcass(fd_types.Assembly):
    
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".peninsula"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'
    
    def add_prompts(self):
        
        self.add_tab(name='Carcass Options',tab_type='VISIBLE')
        self.add_tab(name='Carcass Formulas',tab_type='VISIBLE')
        
        self.add_prompt(name="",prompt_type='DISTANCE',value=unit.inch(2.5),tab_index=1)
        
    def add_parts(self):
        
        common_prompts.add_thickness_prompts(self) 
        common_prompts.add_toe_kick_prompts(self)       
        
        Width = self.get_var('dim_x',"Width")
        Depth = self.get_var('dim_y',"Depth")
        Height = self.get_var('dim_z',"Height")
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Panel_Thickness = self.get_var('Panel Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
               
        rear_panel = common_parts.add_panel(self)
        rear_panel.x_dim('Height',[Height])
        rear_panel.y_dim('-Width',[Width])
        rear_panel.z_dim('Panel_Thickness',[Panel_Thickness])
        rear_panel.x_loc(value = 0)
        rear_panel.y_loc(value = 0)
        rear_panel.z_loc(value = 0)
        rear_panel.x_rot(value = 0)
        rear_panel.y_rot(value = -90)
        rear_panel.z_rot(value = 90)    
        
        front_panel = common_parts.add_panel(self)
        front_panel.x_dim('Height',[Height])
        front_panel.y_dim('-Width',[Width])
        front_panel.z_dim('Panel_Thickness',[Panel_Thickness])
        front_panel.x_loc(value = 0)
        front_panel.y_loc('Depth+Panel_Thickness',[Depth,Panel_Thickness])
        front_panel.z_loc(value = 0)
        front_panel.x_rot(value = 0)
        front_panel.y_rot(value = -90)
        front_panel.z_rot(value = 90)        
        
        top = common_parts.add_panel(self)
        top.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        top.y_dim('Width',[Width])
        top.z_dim('Panel_Thickness',[Panel_Thickness])
        top.x_loc(value = 0)
        top.y_loc('-Panel_Thickness',[Panel_Thickness])
        top.z_loc('Height-Panel_Thickness',[Height,Panel_Thickness])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = -90)   
        
        bottom = common_parts.add_panel(self)
        bottom.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        bottom.y_dim('Width',[Width])
        bottom.z_dim('Panel_Thickness',[Panel_Thickness])
        bottom.x_loc(value = 0)
        bottom.y_loc('-Panel_Thickness',[Panel_Thickness])
        bottom.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = -90)   
        
        left_toe_kick = common_parts.add_toe_kick(self)
        left_toe_kick.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        left_toe_kick.y_dim('Panel_Thickness',[Panel_Thickness])
        left_toe_kick.z_dim('Toe_Kick_Height',[Toe_Kick_Height])
        left_toe_kick.x_loc('Toe_Kick_Setback',[Toe_Kick_Setback])
        left_toe_kick.y_loc('-Panel_Thickness',[Panel_Thickness])
        left_toe_kick.z_loc(value = 0)
        left_toe_kick.x_rot(value = 0)
        left_toe_kick.y_rot(value = 0)
        left_toe_kick.z_rot(value = -90)
        
        right_toe_kick = common_parts.add_toe_kick(self)
        right_toe_kick.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        right_toe_kick.y_dim('-Panel_Thickness',[Panel_Thickness])
        right_toe_kick.z_dim('Toe_Kick_Height',[Toe_Kick_Height])
        right_toe_kick.x_loc('Width-Toe_Kick_Setback',[Width,Toe_Kick_Setback])
        right_toe_kick.y_loc('-Panel_Thickness',[Panel_Thickness])
        right_toe_kick.z_loc(value = 0)
        right_toe_kick.x_rot(value = 0)
        right_toe_kick.y_rot(value = 0)
        right_toe_kick.z_rot(value = -90)
        
        divider = common_parts.add_panel(self)
        divider.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        divider.y_dim('Panel_Thickness',[Panel_Thickness])
        divider.z_dim('Height-Toe_Kick_Height-(Panel_Thickness*2)',[Height,Toe_Kick_Height,Panel_Thickness])
        divider.x_loc('(Width/2)-(Panel_Thickness/2)',[Width,Panel_Thickness])
        divider.y_loc('-Panel_Thickness',[Panel_Thickness])
        divider.z_loc('Toe_Kick_Height+Panel_Thickness',[Toe_Kick_Height,Panel_Thickness])
        divider.x_rot(value = 0)
        divider.y_rot(value = 0)
        divider.z_rot(value = -90) 
        
        opening = common_parts.add_opening(self)
        opening.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        opening.y_dim('(Width/2)-(Panel_Thickness/2)',[Width,Panel_Thickness])
        opening.z_dim('Height-Toe_Kick_Height-(Panel_Thickness*2)',[Height,Toe_Kick_Height,Panel_Thickness])
        opening.x_loc(value = 0)
        opening.y_loc('-Panel_Thickness',[Panel_Thickness])
        opening.z_loc('Toe_Kick_Height+Panel_Thickness',[Toe_Kick_Height,Panel_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = -90)     
        
        opening2 = common_parts.add_opening(self)
        opening2.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        opening2.y_dim('(Width/2)-(Panel_Thickness/2)',[Width,Panel_Thickness])
        opening2.z_dim('Height-Toe_Kick_Height-(Panel_Thickness*2)',[Height,Toe_Kick_Height,Panel_Thickness])
        opening2.x_loc('Width',[Width])
        opening2.y_loc('Depth+Panel_Thickness',[Depth,Panel_Thickness])
        opening2.z_loc('Toe_Kick_Height+Panel_Thickness',[Toe_Kick_Height,Panel_Thickness])
        opening2.x_rot(value = 0)
        opening2.y_rot(value = 0)
        opening2.z_rot(value = 90)             
        
                                     
             
        
    def draw(self): 
        self.create_assembly()    
        
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        self.add_parts()
        
        self.update()
        
        
class PROMPTS_Peninsula_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".peninsula"
    bl_label = "Peninsula Carcass Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    height = bpy.props.EnumProperty(name="Height",
                          items=common_lists.PANEL_HEIGHTS,
                          default = '2131')
    
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)
    
    # Store the product as a class level property for convenience. This is not required
    product = None

    def check(self, context):
        # This gets called every time a user changes a property on the interface
        self.product.obj_y.location.y = -self.depth
        self.product.obj_z.location.z = float(self.height)/1000      
        return True

    def execute(self, context):
        # This gets called when the OK button is clicked
        return {'FINISHED'}

    def invoke(self,context,event):
        # This gets called first and is used as an init call
        
        obj = context.scene.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        self.depth = math.fabs(self.product.obj_y.location.y)
        opening_height = round(unit.meter_to_millimeter(self.product.obj_z.location.z),0)
        for index, height in enumerate(common_lists.PANEL_HEIGHTS):
            if not opening_height >= int(height[0]):
                self.height = common_lists.PANEL_HEIGHTS[index - 1][0]                                                                                                                                                                                                       
                break        
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(480))
        
    def draw(self, context):
        # This draw the interface
        layout = self.layout
        

        # Draw Product Size
        box = layout.box()
        box.prop(self.product.obj_x,'location',index=0,text="Width")
        box.prop(self,'depth',text="Depth")
        box.prop(self,'height',text="Height")

        # You can get Prompts from the Product and Display them on the interface
        Toe_Kick_Height = self.product.get_prompt("Toe Kick Height")
        Toe_Kick_Setback = self.product.get_prompt("Toe Kick Setback")
        box = layout.box()
        row = box.row()
        Toe_Kick_Height.draw_prompt(row)
        row = box.row()
        Toe_Kick_Setback.draw_prompt(row)

        # Draw Product Location and Rotation
        box = layout.box()
        row = box.row()
        row.label('Location:')
        row.prop(self.product.obj_bp,'location',text="")
        row.label('Rotation:')
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="")

        
bpy.utils.register_class(PROMPTS_Peninsula_Prompts)        