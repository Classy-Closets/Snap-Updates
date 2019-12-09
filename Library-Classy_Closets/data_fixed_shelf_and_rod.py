import bpy
import math
from mv import fd_types, unit, utils
from . import common_parts, common_prompts
from . import mv_closet_defaults as props_closet

class Fixed_Shelf_and_Rod(fd_types.Assembly):
    
    type_assembly = "PRODUCT"
    
    #OPTIONAL
    property_id = props_closet.LIBRARY_NAME_SPACE + ".fixed_shelf_and_rod"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + ".draw_fixed_shelf_rod_plan"
    drop_id = ""

    width = unit.inch(36)
    height = unit.inch(4)
    depth = unit.inch(12)

    height_above_floor = unit.inch(68)

    def draw(self):
        self.create_assembly()
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_fixed_shelf_and_rod_product_bp = True
        self.obj_bp.mv.opening_name = "1" #REQUIRED FOR 2D VIEWS
        
        self.add_tab(name='Main Options')
        self.add_tab(name='Formulas')
        self.add_prompt(name="Part Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Hanging Rod Placement",prompt_type='DISTANCE',value=unit.inch(10.5),tab_index=0)
        self.add_prompt(name="Hanging Vertical Placement",prompt_type='DISTANCE',value=unit.inch(1.625),tab_index=0)
        self.add_prompt(name="Hanging Rod Deduction",prompt_type='DISTANCE',value=unit.inch(.375),tab_index=0)  
        self.add_prompt(name="Cleat Width",prompt_type='DISTANCE',value=unit.inch(3.25),tab_index=0)  
        self.add_prompt(name="Support Height",prompt_type='DISTANCE',value=unit.inch(9),tab_index=0) 
        self.add_prompt(name="Width to Include Support",prompt_type='DISTANCE',value=unit.inch(42),tab_index=0) 
        self.add_prompt(name="Add Rod",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Left Fin End",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Right Fin End",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        common_prompts.add_thickness_prompts(self)
        
        dim_x = self.get_var("dim_x")
        dim_y = self.get_var("dim_y")
        dim_z = self.get_var("dim_z")
        Hanging_Rod_Placement = self.get_var("Hanging Rod Placement")
        Hanging_Vertical_Placement = self.get_var("Hanging Vertical Placement")
        Hanging_Rod_Deduction = self.get_var("Hanging Rod Deduction")
        Add_Rod = self.get_var("Add Rod")
        Left_Fin_End = self.get_var("Left Fin End")
        Right_Fin_End = self.get_var("Right Fin End")
        Cleat_Width = self.get_var("Cleat Width")
        Support_Height = self.get_var("Support Height")
        Width_to_Include_Support = self.get_var("Width to Include Support")
        Cleat_Thickness = self.get_var("Cleat Thickness")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        
        top_shelf = common_parts.add_applied_top(self)
        top_shelf.set_name("Top Shelf")
        top_shelf.x_dim('dim_x',[dim_x])
        top_shelf.y_dim('dim_y',[dim_y])
        top_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.x_rot()
        top_shelf.y_rot()
        top_shelf.z_rot()
        top_shelf.x_loc()
        top_shelf.y_loc()
        top_shelf.z_loc()
        
        rear_cleat = common_parts.add_cleat(self)
        rear_cleat.set_name("Rear Cleat")
        rear_cleat.x_dim('dim_x-IF(Left_Fin_End,Cleat_Thickness,0)-IF(Right_Fin_End,Cleat_Thickness,0)',[dim_x,Cleat_Thickness,Left_Fin_End,Right_Fin_End])
        rear_cleat.y_dim('Cleat_Width',[Cleat_Width])
        rear_cleat.z_dim('-Cleat_Thickness',[Cleat_Thickness])
        rear_cleat.x_rot(value = -90)
        rear_cleat.y_rot()
        rear_cleat.z_rot()
        rear_cleat.x_loc('IF(Left_Fin_End,Cleat_Thickness,0)',[Left_Fin_End,Cleat_Thickness])
        rear_cleat.y_loc()
        rear_cleat.z_loc('-Shelf_Thickness',[Shelf_Thickness])
        
        left_cleat = common_parts.add_shelf_and_rod_cleat(self)
        left_cleat.set_name("Left Cleat")
        left_cleat.x_dim('fabs(dim_y)-Cleat_Thickness',[dim_y,Cleat_Thickness])
        left_cleat.y_dim('Cleat_Width',[Cleat_Width])
        left_cleat.z_dim('Cleat_Thickness',[Cleat_Thickness])
        left_cleat.x_rot(value = -90)
        left_cleat.y_rot()
        left_cleat.z_rot(value = -90)
        left_cleat.x_loc()
        left_cleat.y_loc('-Cleat_Thickness',[Cleat_Thickness])
        left_cleat.z_loc('-Shelf_Thickness',[Shelf_Thickness])
        left_cleat.prompt('Hide','IF(Left_Fin_End,True,False)',[Left_Fin_End])
        
        left_fe = common_parts.add_shelf_rod_cleat_fe(self)
        left_fe.set_name("Left Cleat FE")
        left_fe.x_dim('fabs(dim_y)-Cleat_Thickness',[dim_y,Cleat_Thickness])
        left_fe.y_dim('dim_y',[dim_y])
        left_fe.z_dim('Cleat_Thickness',[Cleat_Thickness])
        left_fe.x_rot(value = 0)
        left_fe.y_rot(value = 90)
        left_fe.z_rot(value = 0)
        left_fe.x_loc()
        left_fe.y_loc()
        left_fe.z_loc('-Shelf_Thickness',[Shelf_Thickness])
        left_fe.prompt('Hide','IF(Left_Fin_End,False,True)',[Left_Fin_End])
        left_fe.prompt('Left Depth','Cleat_Width',[Cleat_Width])
        left_fe.prompt('Right Depth',value=0)
        
        right_cleat = common_parts.add_shelf_and_rod_cleat(self)
        right_cleat.set_name("Right Cleat")
        right_cleat.x_dim('fabs(dim_y)-Cleat_Thickness',[dim_y,Cleat_Thickness])
        right_cleat.y_dim('Cleat_Width',[Cleat_Width])
        right_cleat.z_dim('-Cleat_Thickness',[Cleat_Thickness])
        right_cleat.x_rot(value = -90)
        right_cleat.y_rot()
        right_cleat.z_rot(value = -90)
        right_cleat.x_loc('dim_x',[dim_x])
        right_cleat.y_loc('-Cleat_Thickness',[Cleat_Thickness])
        right_cleat.z_loc('-Shelf_Thickness',[Shelf_Thickness])
        right_cleat.prompt('Hide','IF(Right_Fin_End,True,False)',[Right_Fin_End])

        right_fe = common_parts.add_shelf_rod_cleat_fe(self)
        right_fe.set_name("Right Cleat FE")
        right_fe.x_dim('fabs(dim_y)-Cleat_Thickness',[dim_y,Cleat_Thickness])
        right_fe.y_dim('dim_y',[dim_y])
        right_fe.z_dim('-Cleat_Thickness',[Cleat_Thickness])
        right_fe.x_rot(value = 0)
        right_fe.y_rot(value = 90)
        right_fe.z_rot(value = 0)
        right_fe.x_loc('dim_x',[dim_x])
        right_fe.y_loc()
        right_fe.z_loc('-Shelf_Thickness',[Shelf_Thickness])
        right_fe.prompt('Hide','IF(Right_Fin_End,False,True)',[Right_Fin_End])
        right_fe.prompt('Left Depth','Cleat_Width',[Cleat_Width])
        right_fe.prompt('Right Depth',value=0)

        down_support_cleat = common_parts.add_cleat(self)
        down_support_cleat.set_name("Down Cleat")
        down_support_cleat.x_dim('Support_Height',[Support_Height])
        down_support_cleat.y_dim('Cleat_Width',[Cleat_Width])
        down_support_cleat.z_dim('Cleat_Thickness',[Cleat_Thickness])
        down_support_cleat.x_rot(value = 0)
        down_support_cleat.y_rot(value = 90)
        down_support_cleat.z_rot(value = -90)
        down_support_cleat.x_loc('dim_x/2-Cleat_Width/2',[dim_x,Cleat_Width])
        down_support_cleat.y_loc(value = 0)
        down_support_cleat.z_loc('-Cleat_Width-Shelf_Thickness',[Cleat_Width,Shelf_Thickness])
        down_support_cleat.prompt('Hide','IF(dim_x>Width_to_Include_Support,False,True)',[dim_x,Width_to_Include_Support])
        
        rod_support = common_parts.add_rod_support(self)
        rod_support.set_name("Rod Support")
        rod_support.x_rot(value = 0)
        rod_support.y_rot(value = 0)
        rod_support.z_rot(value = 0)
        rod_support.x_loc('dim_x/2',[dim_x,Cleat_Width])
        rod_support.y_loc('-Cleat_Thickness',[Cleat_Thickness])
        rod_support.z_loc(value = unit.inch(-10.5))
        rod_support.prompt('Hide','IF(AND(dim_x>Width_to_Include_Support,Add_Rod==True),False,True)',[dim_x,Width_to_Include_Support,Add_Rod]) 
        
        shelf_support = common_parts.add_shelf_support(self)
        shelf_support.set_name("Shelf Support")
        shelf_support.x_rot(value = 0)
        shelf_support.y_rot(value = 0)
        shelf_support.z_rot(value = 0)
        shelf_support.x_loc('dim_x/2',[dim_x,Cleat_Width])
        shelf_support.y_loc('-Cleat_Thickness',[Cleat_Thickness])
        shelf_support.z_loc(value = unit.inch(-12.75))
        shelf_support.prompt('Hide','IF(AND(dim_x>Width_to_Include_Support,Add_Rod==False),False,True)',[dim_x,Width_to_Include_Support,Add_Rod])               

        hanging_rod = common_parts.add_oval_hanging_rod(self)
        hanging_rod.set_name("Hanging Rod")
        hanging_rod.x_dim('dim_x-Cleat_Thickness*2-Hanging_Rod_Deduction',[dim_x,Cleat_Thickness,Hanging_Rod_Deduction])
        hanging_rod.x_rot()
        hanging_rod.y_rot()
        hanging_rod.z_rot()
        hanging_rod.x_loc('Cleat_Thickness+(Hanging_Rod_Deduction/2)',[Cleat_Thickness,Hanging_Rod_Deduction])
        hanging_rod.y_loc('-Hanging_Rod_Placement',[Hanging_Rod_Placement])
        hanging_rod.z_loc('-Hanging_Vertical_Placement-Shelf_Thickness',[Hanging_Vertical_Placement,Shelf_Thickness])
        hanging_rod.prompt('Hide','IF(Add_Rod,False,True)',[Add_Rod])
        
        self.update()
        
class PROMPTS_Fixed_Shelf_And_Rod_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".fixed_shelf_and_rod"
    bl_label = "Fixed Shelf and Rod Prompts" 
    bl_description = "This shows all of the available fixed shelf and rod options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)    
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4) 
    
    product = None
    
    shelf = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        self.product.obj_x.location.x = self.width
        self.product.obj_z.location.z = -self.height
        self.product.obj_y.location.y = -self.depth  
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        self.width = self.product.obj_x.location.x
        self.height = math.fabs(self.product.obj_z.location.z)
        self.depth = math.fabs(self.product.obj_y.location.y)
        
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def object_has_driver(self,obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True        
        
    def draw_product_size(self,layout):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row1.label('Width: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label('Width:')
            row1.prop(self,'width',text="")
            row1.prop(self.product.obj_x,'hide',text="")     
        
        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_y):
            row1.label('Depth: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_y.location.y))))
        else:
            row1.label('Depth:')
            row1.prop(self,'depth',text="")
            row1.prop(self.product.obj_y,'hide',text="")
        
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:

                add_rod = self.product.get_prompt("Add Rod")
                left_fin_end = self.product.get_prompt("Left Fin End")
                right_fin_end = self.product.get_prompt("Right Fin End")
                cleat_width = self.product.get_prompt("Cleat Width")
                width_to_include_support = self.product.get_prompt("Width to Include Support")
                support_height = self.product.get_prompt("Support Height")
                
                self.draw_product_size(layout)            
                
                box = layout.box()
                
                row = box.row()
                cleat_width.draw_prompt(row)                
                
                row = box.row()
                add_rod.draw_prompt(row)

                row = box.row()
                left_fin_end.draw_prompt(row)

                row = box.row()
                right_fin_end.draw_prompt(row)        
                
                if self.product.obj_x.location.x > width_to_include_support.value():
                    row = box.row()
                    support_height.draw_prompt(row)        
        
class OPERATOR_Closet_Fixed_Shelf_And_Rod_Draw_Plan(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".draw_fixed_shelf_rod_plan"
    bl_label = "Draw Fixed Shelf and Rod Plan View"
    bl_description = "Creates the plan view the Fixed Shelf and Rod"
    
    object_name = bpy.props.StringProperty(name="Object Name",default="")
    
    product = None
    
    def add_opening(self,size,x_location):
        opening_mesh = utils.create_cube_mesh(self.product.obj_bp.mv.name_object,(size[0],size[1],size[2]))
        opening_mesh.parent = self.product.obj_bp.parent
        opening_mesh.location = self.product.obj_bp.location
        opening_mesh.location.x = x_location
        opening_mesh.rotation_euler = self.product.obj_bp.rotation_euler
        opening_mesh.mv.type = 'CAGE'
        
    def add_panel(self,size,x_location,text):
        panel_mesh = utils.create_cube_mesh(self.product.obj_bp.mv.name_object,(size[0],size[1],size[2]))
        panel_mesh.parent = self.product.obj_bp.parent
        panel_mesh.location = self.product.obj_bp.location
        panel_mesh.location.x = x_location
        panel_mesh.rotation_euler = self.product.obj_bp.rotation_euler
        panel_mesh.mv.type = 'CAGE'
        
        dim = fd_types.Dimension()
        dim.parent(panel_mesh)
        dim.start_x(value = 0)
        dim.start_y(value = size[1]-unit.inch(3))
        dim.start_z(value = unit.inch(-100))
        dim.set_label(text)
        
    def execute(self, context):
        obj_bp = bpy.data.objects[self.object_name]

        self.product = fd_types.Assembly(obj_bp)
        thickness = self.product.get_prompt("Cleat Thickness")
        lfe = self.product.get_prompt("Left Fin End")
        rfe = self.product.get_prompt("Right Fin End")
        
        width = self.product.obj_x.location.x
        depth = math.fabs(self.product.obj_y.location.y)
        height = math.fabs(self.product.obj_y.location.y)
        
        text = str(int(unit.meter_to_active_unit(depth)))
        
        self.add_panel((thickness.value(),-depth,height), self.product.obj_bp.location.x, text + "TRI" if lfe.value() else text)
        
        self.add_opening((width-(thickness.value()*2),-depth,height), self.product.obj_bp.location.x + thickness.value())
        
        self.add_panel((thickness.value(),-depth,height), self.product.obj_bp.location.x + width - thickness.value(), text + "TRI" if rfe.value() else text)

        return {'FINISHED'}        
        
bpy.utils.register_class(PROMPTS_Fixed_Shelf_And_Rod_Prompts)
bpy.utils.register_class(OPERATOR_Closet_Fixed_Shelf_And_Rod_Draw_Plan)
