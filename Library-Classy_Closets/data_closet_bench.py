import bpy
import math
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

class Closet_Bench(fd_types.Assembly):
    
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".bench"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'
    
    def add_prompts(self):
        
        self.add_tab(name='Carcass Options',tab_type='VISIBLE')
        self.add_tab(name='Carcass Formulas',tab_type='VISIBLE')
        
        self.add_prompt(name="Front Overhang",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)    
        self.add_prompt(name="Rear Overhang",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)
        self.add_prompt(name="Left Overhang",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)
        self.add_prompt(name="Right Overhang",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0) 
        self.add_prompt(name="Bottom Gap",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)                           
    
    def add_parts(self):
        
        common_prompts.add_thickness_prompts(self) 
        common_prompts.add_toe_kick_prompts(self)   
        
        Width = self.get_var('dim_x',"Width")
        Depth = self.get_var('dim_y',"Depth")
        Height = self.get_var('dim_z',"Height")
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Panel_Thickness = self.get_var('Panel Thickness') 
        Front_Overhang = self.get_var('Front Overhang')
        Rear_Overhang = self.get_var('Rear Overhang')
        Left_Overhang = self.get_var('Left Overhang')
        Right_Overhang = self.get_var('Right Overhang')
        Bottom_Gap = self.get_var('Bottom Gap')         
        
        
        rear_panel = common_parts.add_panel(self)
        rear_panel.set_name("rear panel")
        rear_panel.x_dim('Height-Panel_Thickness',[Height,Panel_Thickness])
        rear_panel.y_dim('-Width+(Panel_Thickness*2)',[Width,Panel_Thickness])
        rear_panel.z_dim('Panel_Thickness',[Panel_Thickness])
        rear_panel.x_loc('Panel_Thickness',[Panel_Thickness])
        rear_panel.y_loc(value = 0)
        rear_panel.z_loc(value = 0)
        rear_panel.x_rot(value = 0)
        rear_panel.y_rot(value = -90)
        rear_panel.z_rot(value = 90)    
        
        front_panel = common_parts.add_panel(self)
        front_panel.set_name("front panel")
        front_panel.x_dim('Height-Panel_Thickness',[Height,Panel_Thickness])
        front_panel.y_dim('-Width+(Panel_Thickness*2)',[Width,Panel_Thickness])
        front_panel.z_dim('Panel_Thickness',[Panel_Thickness])
        front_panel.x_loc('Panel_Thickness',[Panel_Thickness])
        front_panel.y_loc('Depth+Panel_Thickness',[Depth,Panel_Thickness])
        front_panel.z_loc(value = 0)
        front_panel.x_rot(value = 0)
        front_panel.y_rot(value = -90)
        front_panel.z_rot(value = 90)
        
        left_panel = common_parts.add_panel(self)
        left_panel.set_name("left panel")
        left_panel.x_dim('-Depth',[Depth,Panel_Thickness])
        left_panel.y_dim('Left_Side_Thickness',[Left_Side_Thickness])
        left_panel.z_dim('Height-Panel_Thickness',[Height,Panel_Thickness])
        left_panel.x_loc(value = 0)
        left_panel.y_loc(value = 0)
        left_panel.z_loc(value = 0)
        left_panel.x_rot(value = 0)
        left_panel.y_rot(value = 0)
        left_panel.z_rot(value = -90)     
        
        right_panel = common_parts.add_panel(self)
        right_panel.set_name("right panel")
        right_panel.x_dim('-Depth',[Depth,Panel_Thickness])
        right_panel.y_dim('-Right_Side_Thickness',[Right_Side_Thickness])
        right_panel.z_dim('Height-Panel_Thickness',[Height,Panel_Thickness])
        right_panel.x_loc('Width',[Width])
        right_panel.y_loc(value = 0)
        right_panel.z_loc(value = 0)
        right_panel.x_rot(value = 0)
        right_panel.y_rot(value = 0)
        right_panel.z_rot(value = -90)                    
        
        top = common_parts.add_panel(self)
        top.set_name("top")
        top.x_dim('-Depth+Front_Overhang',[Depth,Rear_Overhang,Front_Overhang])
        top.y_dim('Width+Right_Overhang+Left_Overhang',[Width,Right_Overhang,Left_Overhang])
        top.z_dim('Panel_Thickness',[Panel_Thickness])
        top.x_loc('-Left_Overhang',[Left_Overhang])
        top.y_loc(value = 0)
        top.z_loc('Height-Panel_Thickness',[Height,Panel_Thickness])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = -90)   
        
        bottom = common_parts.add_panel(self)
        bottom.set_name("bottom")
        bottom.x_dim('-Depth-(Panel_Thickness*2)',[Depth,Panel_Thickness])
        bottom.y_dim('Width-(Panel_Thickness*2)',[Width,Panel_Thickness])
        bottom.z_dim('Panel_Thickness',[Panel_Thickness])
        bottom.x_loc('Panel_Thickness',[Panel_Thickness])
        bottom.y_loc('-Panel_Thickness',[Panel_Thickness])
        bottom.z_loc('Bottom_Gap',[Bottom_Gap])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = -90)  
        
    def draw(self): 
        self.create_assembly()    
        
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        self.add_prompts()
        self.add_parts()
        
        self.update()                     
        
class PROMPTS_Bench_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".bench"
    bl_label = "Bench Carcass Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    height = bpy.props.EnumProperty(name="Height",
                          items=common_lists.PANEL_HEIGHTS,
                          default = '243')
    
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
        # This draws the interface
        layout = self.layout
        
        # Draws Product Size
        box = layout.box()
        box.prop(self.product.obj_x,'location',index=0,text="Width")
        box.prop(self,'depth',text="Depth")
        box.prop(self,'height',text="Height")

        # Prompts from the Product and Displays them on the interface
        Bottom_Gap = self.product.get_prompt("Bottom Gap")
        Front_Overhang = self.product.get_prompt('Front Overhang')
        Rear_Overhang = self.product.get_prompt('Rear Overhang')
        Left_Overhang = self.product.get_prompt('Left Overhang')
        Right_Overhang = self.product.get_prompt('Right Overhang')
        box = layout.box()
        row = box.row()
        Bottom_Gap.draw_prompt(row)
        row = box.row()
        Front_Overhang.draw_prompt(row)
        row = box.row()
        Rear_Overhang.draw_prompt(row)
        row = box.row()
        Left_Overhang.draw_prompt(row)
        row = box.row()
        Right_Overhang.draw_prompt(row)                        

        # Draws Product Location and Rotation
        box = layout.box()
        row = box.row()
        row.label('Location:')
        row.prop(self.product.obj_bp,'location',text="")
        row.label('Rotation:')
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="")

        
bpy.utils.register_class(PROMPTS_Bench_Prompts)                
        
        
        
        
        
        
        
        
        
        
