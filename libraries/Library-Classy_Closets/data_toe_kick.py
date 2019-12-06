import bpy
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts

class Toe_Kick(fd_types.Assembly):
    
    property_id = props_closet.LIBRARY_NAME_SPACE + ".toe_kick_prompts"
    type_assembly = "PRODUCT"

    def add_parts(self):
        
        self.add_prompt(name="Cleat Width",prompt_type='DISTANCE',value=unit.inch(2.5),tab_index=1)
        
        Width = self.get_var('dim_x',"Width")
        Depth = self.get_var('dim_y',"Depth")
        Height = self.get_var('dim_z',"Height")
        Cleat_Width = self.get_var('Cleat Width')
        Toe_Kick_Thickness = self.get_var('Toe Kick Thickness')

        toe_kick_front = common_parts.add_toe_kick(self)
        toe_kick_front.x_dim('Width-(Toe_Kick_Thickness*2)',[Width,Toe_Kick_Thickness])
        toe_kick_front.y_dim('-Height',[Height])
        toe_kick_front.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_front.x_loc('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_front.y_loc('Depth',[Depth])
        toe_kick_front.z_loc(value = 0)
        toe_kick_front.x_rot(value = -90)
        toe_kick_front.y_rot(value = 0)
        toe_kick_front.z_rot(value = 0)
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.x_dim('Width-(Toe_Kick_Thickness*2)',[Width,Toe_Kick_Thickness])
        toe_kick.y_dim('-Height',[Height])
        toe_kick.z_dim('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick.x_loc('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick.y_loc(value = 0)
        toe_kick.z_loc(value = 0)
        toe_kick.x_rot(value = -90)
        toe_kick.y_rot(value = 0)
        toe_kick.z_rot(value = 0)        
        
        left_toe_kick = common_parts.add_toe_kick(self)
        left_toe_kick.x_dim('-Depth',[Depth])
        left_toe_kick.y_dim('-Height',[Height])
        left_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        left_toe_kick.y_loc(value = 0)
        left_toe_kick.x_loc(value = 0)
        left_toe_kick.z_loc(value = 0)
        left_toe_kick.x_rot(value = -90)
        left_toe_kick.y_rot(value = 0)
        left_toe_kick.z_rot(value = -90)        
        
        right_toe_kick = common_parts.add_toe_kick(self)
        right_toe_kick.x_dim('-Depth',[Depth])
        right_toe_kick.y_dim('Height',[Height])
        right_toe_kick.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        right_toe_kick.y_loc(value = 0)
        right_toe_kick.x_loc('Width',[Width,Toe_Kick_Thickness])
        right_toe_kick.z_loc(value = 0)
        right_toe_kick.x_rot(value = 90)
        right_toe_kick.y_rot(value = 0)
        right_toe_kick.z_rot(value = -90)
        
        toe_kick_cleat = common_parts.add_cleat(self)
        toe_kick_cleat.x_dim('Width-(Toe_Kick_Thickness*2)',[Width,Toe_Kick_Thickness])
        toe_kick_cleat.y_dim('Cleat_Width',[Cleat_Width])
        toe_kick_cleat.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_cleat.x_loc('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_cleat.y_loc('Depth+Toe_Kick_Thickness',[Depth,Toe_Kick_Thickness])
        toe_kick_cleat.z_loc('Height-Toe_Kick_Thickness',[Height,Toe_Kick_Thickness])
        toe_kick_cleat.x_rot(value = 0)
        toe_kick_cleat.y_rot(value = 0)
        toe_kick_cleat.z_rot(value = 0)
        
        toe_kick_cleat = common_parts.add_cleat(self)
        toe_kick_cleat.x_dim('Width-(Toe_Kick_Thickness*2)',[Width,Toe_Kick_Thickness])
        toe_kick_cleat.y_dim('-Cleat_Width',[Cleat_Width])
        toe_kick_cleat.z_dim('Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick_cleat.x_loc('Toe_Kick_Thickness',[Toe_Kick_Thickness])
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
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(500))
        
    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(self.product.obj_bp.mv.name_object)
        self.draw_product_size(layout)

bpy.utils.register_class(PROMPTS_Toe_Kick_Prompts)    