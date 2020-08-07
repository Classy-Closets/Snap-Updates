import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from os import path
import math
from . import mv_closet_defaults as props_closet


class Wall_Cleat(fd_types.Assembly):

    property_id = "closet.wall_cleat"
    #drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_wall_cleat"
    type_assembly = "PRODUCT"

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        props = props_closet.get_object_props(self.obj_bp)
        props.is_cleat = True
        
        self.add_tab(name='Wall Cleat Options',tab_type='VISIBLE')
        #self.add_prompt(name="Width",prompt_type='DISTANCE',value=unit.inch(18),tab_index=1)
        self.add_prompt(name="Height",prompt_type='DISTANCE',value=unit.inch(3.64),tab_index=1)
        self.add_prompt(name="Distance Above Floor",prompt_type='DISTANCE',value=unit.inch(60),tab_index=1)

        common_prompts.add_thickness_prompts(self)

        Width = self.get_var("dim_x","Width")
        Height = self.get_var("Height")


        Distance_Above_Floor = self.get_var('Distance Above Floor')
        Panel_Thickness = self.get_var('Panel Thickness')
        
        cleat = common_parts.add_cleat(self)
        cleat.obj_bp.mv.comment_2 = "1024"
        cleat.set_name("Cleat")

        cleat.y_loc(value = 0)
        cleat.z_loc('Distance_Above_Floor',[Distance_Above_Floor])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)

        cleat.x_dim('Width',[Width])
        cleat.y_dim('-Height',[Height])
        cleat.z_dim('-Panel_Thickness',[Panel_Thickness])
        cleat.prompt('Use Cleat Cover', value=False)

        self.update()

class PROMPTS_Wall_Cleat_Prompts(fd_types.Prompts_Interface):
    bl_idname = "closet.wall_cleat"
    bl_label = "Wall Cleat Prompts"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)


    placement_on_wall = bpy.props.EnumProperty(name="Placement on Wall",items=[('SELECTED_POINT',"Selected Point",""),
                                                                     ('FILL',"Fill",""),
                                                                     ('FILL_LEFT',"Fill Left",""),
                                                                     ('LEFT',"Left",""),
                                                                     ('CENTER',"Center",""),
                                                                     ('RIGHT',"Right",""),
                                                                     ('FILL_RIGHT',"Fill Right","")],default = 'SELECTED_POINT')
    
    
    current_location = bpy.props.FloatProperty(name="Current Location", default=0,subtype='DISTANCE')
    left_offset = bpy.props.FloatProperty(name="Left Offset", default=0,subtype='DISTANCE')
    right_offset = bpy.props.FloatProperty(name="Right Offset", default=0,subtype='DISTANCE') 


    product = None

    selected_location = 0
    default_width = 0


    def check(self, context):
        self.product.obj_x.location.x = self.width
        self.update_placement(context)
        return True


    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        self.current_location = self.product.obj_bp.location.x
        self.selected_location = self.product.obj_bp.location.x
        self.default_width = self.product.obj_x.location.x
        self.width = self.product.obj_x.location.x
        self.placement_on_wall = 'SELECTED_POINT'
        self.left_offset = 0
        self.right_offset = 0

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))


    def update_placement(self,context):
        left_x = self.product.get_collision_location('LEFT')
        right_x = self.product.get_collision_location('RIGHT')
        if self.placement_on_wall == 'SELECTED_POINT':
            self.product.obj_bp.location.x = self.current_location
        if self.placement_on_wall == 'LEFT':
            self.product.obj_bp.location.x = left_x + self.left_offset
            self.product.obj_x.location.x = self.width
        if self.placement_on_wall == 'RIGHT':
            if self.product.obj_bp.mv.placement_type == 'Corner':
                self.product.obj_bp.rotation_euler.z = math.radians(-90)
            self.product.obj_x.location.x = self.width
            self.product.obj_bp.location.x = (right_x- self.product.calc_width()) - self.right_offset

    
    def set_product_defaults(self):
        self.product.obj_bp.location.x = self.selected_location + self.left_offset
        self.product.obj_x.location.x = self.default_width - (self.left_offset + self.right_offset)

    def draw_product_placement(self,layout): 
        box = layout.box() 
        
        row = box.row(align=True) 
        row.label('Placement',icon='LATTICE_DATA') 
        row.prop_enum(self, "placement_on_wall", 'SELECTED_POINT', icon='MAN_TRANS', text="Selected Point") 
        row.prop_enum(self, "placement_on_wall", 'LEFT', icon='TRIA_LEFT', text="Left")  
        row.prop_enum(self, "placement_on_wall", 'RIGHT', icon='TRIA_RIGHT', text="Right")  
        
        if self.placement_on_wall in 'LEFT': 
            row = box.row(align=True) 
            row.label('Offset',icon='BACK') 
            row.prop(self, "left_offset", icon='TRIA_LEFT', text="Left")       
        
        if self.placement_on_wall in 'RIGHT': 
            row = box.row(align=True) 
            row.label('Offset',icon='FORWARD') 
            row.prop(self, "right_offset", icon='TRIA_RIGHT', text="Right")           
        
        if self.placement_on_wall == 'SELECTED_POINT': 
            row = box.row() 
            row.label('Location:') 
            row.prop(self,'current_location',text="") 
        
        row.label('Move Off Wall:') 
        row.prop(self.product.obj_bp,'location',index=1,text="") 
            
        row.label('Rotation:') 
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="") 

    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(self.product.obj_bp.mv.name_object)
        self.draw_product_size(layout)
        box = layout.box()

        distance_above_floor = self.product.get_prompt("Distance Above Floor")
        #width = self.product.get_prompt("Width")
        height = self.product.get_prompt("Height")
               

        #row = box.row()
        #width.draw_prompt(row,text="Width:",split_text=True)
        row = box.row()
        height.draw_prompt(row,text="Height:",split_text=True)
        row = box.row()
        distance_above_floor.draw_prompt(row,text="Distance Above Floor:",split_text=True)

#        row = box.row()
#        row.label('Distance From Wall:')
#        row.prop(self,'current_location',text="")

        self.draw_product_placement(layout)

bpy.utils.register_class(PROMPTS_Wall_Cleat_Prompts)