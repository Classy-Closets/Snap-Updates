import bpy
import math
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_machining
from . import common_parts
from . import common_prompts
from . import common_lists

def update_closet_height(self,context):
    ''' EVENT changes height for all closet openings
    '''
    obj_product_bp = utils.get_bp(context.active_object,'PRODUCT')
    product = fd_types.Assembly(obj_product_bp)
    product.obj_z.location.z = -unit.millimeter(float(self.height_list))

class Stacked_Carcass(fd_types.Assembly):
    
    type_assembly = "PRODUCT"
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_stacked_carcass"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".upper"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'
    
    mirror_z = True
    
    opening_qty = 4
    
    is_hanging = True
    
    def __init__(self):
        defaults = props_closet.get_scene_props().closet_defaults
        self.width = unit.inch(18) * self.opening_qty
        self.height = unit.millimeter(float(defaults.stacked_panel_height))
        self.depth = defaults.panel_depth
    
    def add_opening_prompts(self):
        props = props_closet.get_scene_props().closet_defaults
        
        self.add_tab(name='Opening Widths',tab_type='CALCULATOR',calc_type="XDIM") #0
        self.add_tab(name='Carcass Options',tab_type='VISIBLE') #1
        
        for i in range(1,self.opening_qty+1):
            self.add_prompt(name="Opening " + str(i) + " Width",
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=0,
                            equal=True)
            
            self.add_prompt(name="Opening " + str(i) + " Depth",
                            prompt_type='DISTANCE',
                            value=self.depth,
                            tab_index=1)

    def add_machining_prompts(self):
        self.add_tab(name='Machining Options',tab_type='VISIBLE') #2
        
        for i in range(1,self.opening_qty+1):

            self.add_prompt(name="Opening " + str(i) + " Stop LB",
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=2)
            
            self.add_prompt(name="Opening " + str(i) + " Start LB",
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=2)
            
            self.add_prompt(name="Opening " + str(i) + " Add Mid Drilling",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
            
            self.add_prompt(name="Opening " + str(i) + " Drill Thru Left",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
        
            self.add_prompt(name="Opening " + str(i) + " Drill Thru Right",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
        
            self.add_prompt(name="Opening " + str(i) + " Remove Left Drill",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
        
            self.add_prompt(name="Opening " + str(i) + " Remove Right Drill",
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=2)
    
    def add_sides(self):
        props = props_closet.get_scene_props()  
        
        Product_Height = self.get_var('dim_z','Product_Height')
        Product_Width = self.get_var('dim_x','Product_Width')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        Right_Side_Wall_Filler = self.get_var('Right Side Wall Filler')
        Left_Side_Thickness = self.get_var('Left Side Thickness')
        Right_Side_Thickness = self.get_var('Right Side Thickness')
        Depth_1 = self.get_var('Opening 1 Depth','Depth_1')
        Last_Depth = self.get_var('Opening ' + str(self.opening_qty) + ' Depth',"Last_Depth")
        Add_Backing = self.get_var('Add Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Left_End_Condition = self.get_var('Left End Condition')
        Right_End_Condition = self.get_var('Right End Condition')
    
        left_filler = common_parts.add_filler(self)
        left_filler.x_dim('Product_Height',[Product_Height])
        left_filler.y_dim('-Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_filler.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
        left_filler.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_filler.y_loc('-Depth_1-IF(Add_Backing,Back_Thickness,0)',[Depth_1,Add_Backing,Back_Thickness])
        left_filler.z_loc(value = 0)
        left_filler.x_rot(value = 0)
        left_filler.y_rot(value = -90)
        left_filler.z_rot(value = -90)
        left_filler.prompt('Hide','IF(Left_Side_Wall_Filler==0,True,False)',[Left_Side_Wall_Filler])
        
        left_side = common_parts.add_panel(self)
        left_side.x_dim('-Product_Height',[Product_Height])
        left_side.y_dim('-Depth_1',[Depth_1])
        left_side.z_dim('-Left_Side_Thickness',[Left_Side_Thickness])
        left_side.x_loc('Left_Side_Wall_Filler',[Left_Side_Wall_Filler])
        left_side.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
        left_side.z_loc('Product_Height',[Product_Height])
        left_side.x_rot(value = 0)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
        left_side.prompt('Hide','IF(Left_End_Condition==3,True,False)',[Left_End_Condition])
                        
        right_filler = common_parts.add_filler(self)
        right_filler.x_dim('Product_Height',[Product_Height])
        right_filler.y_dim('Right_Side_Wall_Filler',[Right_Side_Wall_Filler])
        right_filler.z_dim('Left_Side_Thickness',[Left_Side_Thickness])
        right_filler.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
        right_filler.y_loc('-Last_Depth-IF(Add_Backing,Back_Thickness,0)',[Last_Depth,Add_Backing,Back_Thickness])
        right_filler.z_loc(value = 0)
        right_filler.x_rot(value = 0)
        right_filler.y_rot(value = -90)
        right_filler.z_rot(value = -90)
        right_filler.prompt('Hide','IF(Right_Side_Wall_Filler==0,True,False)',[Right_Side_Wall_Filler])
        
        right_side = common_parts.add_panel(self)
        right_side.x_dim('-Product_Height',[Product_Height])
        right_side.y_dim('-Last_Depth',[Last_Depth])
        right_side.z_dim('Right_Side_Thickness',[Right_Side_Thickness])
        right_side.x_loc('Product_Width-Right_Side_Wall_Filler',[Product_Width,Right_Side_Wall_Filler])
        right_side.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
        right_side.z_loc('Product_Height',[Product_Height])
        right_side.x_rot(value = 0)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)
        right_side.prompt('Hide','IF(Right_End_Condition==3,True,False)',[Right_End_Condition])

    def add_panel(self,index,previous_panel):
        props = props_closet.get_scene_props()   

        PH = self.get_var('dim_z','PH')
        Width = self.get_var('Opening ' + str(index-1) + ' Width',"Width")
        Depth = self.get_var('Opening ' + str(index-1) + ' Depth',"Depth")
        Next_Depth = self.get_var('Opening ' + str(index) + ' Depth',"Next_Depth")
        Add_Backing = self.get_var('Add Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Panel_Thickness = self.get_var('Panel Thickness')
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        
        panel = common_parts.add_panel(self)
        if previous_panel:
            Prev_Panel_X = previous_panel.get_var("loc_x",'Prev_Panel_X')
            Left_Side_Thickness = self.get_var('Left_Side_Thickness')
            panel.x_loc('Prev_Panel_X+Panel_Thickness+Width',[Prev_Panel_X,Panel_Thickness,Width])
        else:
            Left_Side_Thickness = self.get_var('Left Side Thickness')
            panel.x_loc('Left_Side_Thickness+Width+Left_Side_Wall_Filler+Panel_Thickness',
                        [Left_Side_Thickness,Width,Left_Side_Wall_Filler,Panel_Thickness])
        panel.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
        panel.z_loc('PH',[PH])
        panel.x_rot(value = 0)
        panel.y_rot(value = -90)
        panel.z_rot(value = 0)
        panel.x_dim('-PH',[PH]) 
        panel.y_dim('-max(Depth,Next_Depth)',[Depth,Next_Depth])
        panel.z_dim('Panel_Thickness',[Panel_Thickness])
        return panel
        
    def add_shelf(self,i,panel,is_top=False):
        Product_Height = self.get_var('dim_z','Product_Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Depth = self.get_var('Opening ' + str(i) + ' Depth','Depth')
        Add_Backing = self.get_var('Add Backing')
        Remove_Top_Shelf = self.get_var('Remove Top Shelf ' + str(i),'Remove_Top_Shelf')
        Remove_Bottom_Hanging_Shelf = self.get_var('Remove Bottom Hanging Shelf ' + str(i),'Remove_Bottom_Hanging_Shelf')
        Back_Thickness = self.get_var('Back Thickness')
        Shelf_Thickness = self.get_var('Shelf Thickness')

        Left_End_Condition = self.get_var('Left End Condition')
        Right_End_Condition = self.get_var('Right End Condition')  
        
        shelf = common_parts.add_shelf(self)
        shelf.prompt("Is Locked Shelf",value=True)
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            shelf.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            shelf.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])
        
        if is_top:
            shelf.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
            shelf.z_loc(value = 0)
            shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
            shelf.y_dim("-Depth",[Depth])
            shelf.prompt('Hide','IF(Remove_Top_Shelf,False,True)',[Remove_Top_Shelf])
        else:
            shelf.y_loc('IF(Add_Backing,-Back_Thickness,0)',[Add_Backing,Back_Thickness])
            shelf.z_loc('Product_Height',[Product_Height])
            shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
            shelf.y_dim("-Depth",[Depth])
            shelf.prompt('Hide','IF(Remove_Bottom_Hanging_Shelf,False,True)',[Remove_Bottom_Hanging_Shelf])
            
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 0)
        shelf.x_dim('Width',[Width])
        
        if i == 1:
            shelf.prompt("Remove Left Holes",'IF(Left_End_Condition==3,True,False)',[Left_End_Condition])
        
        if i == self.opening_qty:
            shelf.prompt("Remove Right Holes",'IF(Right_End_Condition==3,True,False)',[Right_End_Condition])
        
        if is_top:
            shelf.prompt("Drill On Top",value=True)
        else:
            shelf.prompt("Drill On Top",value=False)
    
    def add_top_cleat(self,i,panel):
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Add_Top_Cleat = self.get_var('Add ' + str(i) + ' Top Cleat','Add_Top_Cleat')
        Cleat_Location = self.get_var('Cleat ' + str(i) + ' Location','Cleat_Location')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.y_loc(value = 0)
        cleat.z_loc('-Shelf_Thickness-.09271',[Shelf_Thickness])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim(value=unit.inch(-3.64))
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        cleat.prompt('Hide','IF(Add_Top_Cleat,False,True)',[Add_Top_Cleat])
        if i == 1:
            cleat.x_loc('X_Loc+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        elif i == self.opening_qty: #LAST OPENING
            cleat.x_loc('X_Loc',[X_Loc])
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        else:
            cleat.x_loc('X_Loc',[X_Loc])
            cleat.x_dim('Width',[Width])
            
    def add_bottom_cleat(self,i,panel):
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Add_Bottom_Cleat = self.get_var('Add ' + str(i) + ' Bottom Cleat','Add_Bottom_Cleat')
        Cleat_Location = self.get_var('Cleat ' + str(i) + ' Location','Cleat_Location')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Cut_to_Fit_Amount = self.get_var("Cut to Fit Amount")
        Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
        PH = self.get_var('dim_z','PH')
        
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
        else:
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
        
        cleat = common_parts.add_cleat(self)
        cleat.y_loc(value = 0)
        cleat.z_loc('PH',[PH])
        cleat.x_rot(value = -90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0)
        cleat.y_dim(value=unit.inch(-3.64))
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        cleat.prompt('Hide','IF(Add_Bottom_Cleat,False,True)',[Add_Bottom_Cleat])
        if i == 1:
            cleat.x_loc('X_Loc+Left_Side_Wall_Filler',[X_Loc,Left_Side_Wall_Filler])
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        elif i == self.opening_qty: #LAST OPENING
            cleat.x_loc('X_Loc',[X_Loc])
            cleat.x_dim('Width',[Width,Cut_to_Fit_Amount])
        else:
            cleat.x_loc('X_Loc',[X_Loc])
            cleat.x_dim('Width',[Width])            
    
    def add_closet_opening(self,i,panel):
        props = props_closet.get_scene_props().closet_defaults
        
        Product_Height = self.get_var('dim_z','Product_Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Depth = self.get_var('Opening ' + str(i) + ' Depth','Depth')
        Add_Backing = self.get_var('Add Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        
        
        opening = common_parts.add_section_opening(self)
    
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            opening.x_loc('X_Loc',[X_Loc])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            opening.x_loc('Left_Side_Wall_Filler+X_Loc',[Left_Side_Wall_Filler,X_Loc])
        opening.y_loc('-Depth-IF(Add_Backing,Back_Thickness,0)',[Depth,Add_Backing,Back_Thickness])
        opening.z_loc('Product_Height+Shelf_Thickness',[Product_Height,Shelf_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('Width',[Width])
        opening.y_dim("fabs(Depth)",[Depth])
        opening.z_dim('fabs(Product_Height)-(Shelf_Thickness*2)',[Product_Height,Shelf_Thickness])
    
    def add_backing(self,i,panel):
        scene_props = props_closet.get_scene_props().closet_defaults
        
        Product_Height = self.get_var('dim_z','Product_Height')
        Width = self.get_var('Opening ' + str(i) + ' Width','Width')
        Add_Backing = self.get_var('Add Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Panel_Thickness = self.get_var('Panel Thickness')
        
        backing = common_parts.add_back(self)
    
        if panel:
            X_Loc = panel.get_var('loc_x','X_Loc')
            backing.x_loc('X_Loc-(Panel_Thickness/2)',[X_Loc,Panel_Thickness])
        else:
            Left_Side_Wall_Filler = self.get_var('Left Side Wall Filler')
            X_Loc = self.get_var('Left Side Thickness','X_Loc')
            backing.x_loc('Left_Side_Wall_Filler+X_Loc-(Panel_Thickness/2)',[Left_Side_Wall_Filler,X_Loc,Panel_Thickness])
        backing.y_loc(value = 0)
        backing.z_loc(value = 0)
        backing.x_rot(value = -90)
        backing.y_rot(value = -90)
        backing.z_rot(value = 0)
        backing.x_dim('Product_Height',[Product_Height])
        backing.y_dim("Width+Panel_Thickness",[Width,Panel_Thickness])
        backing.z_dim('-Back_Thickness',[Back_Thickness])
        backing.prompt('Hide','IF(Add_Backing,False,True)',[Add_Backing])
    
    def draw(self):
        defaults = props_closet.get_scene_props().closet_defaults

        self.create_assembly()
        self.obj_bp.mv.product_type = "Closet"
        product_props = props_closet.get_object_props(self.obj_bp)
        product_props.is_closet = True         
        
        self.add_opening_prompts()
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_closet_carcass_prompts(self)
        for i in range(1,10):
            self.prompt('Remove Bottom Hanging Shelf ' + str(i),value=True)
        for i in range(1,10):
            self.prompt('Remove Top Shelf ' + str(i),value=True)
        self.add_machining_prompts()
        
        self.add_sides()
        panel = None
        self.add_shelf(1,panel,is_top=True)
        self.add_shelf(1,panel,is_top=False)
        self.add_top_cleat(1,panel)
        self.add_bottom_cleat(1,panel)
        self.add_closet_opening(1,panel)
        self.add_backing(1,panel)   
        
        for i in range(2,self.opening_qty+1):
            panel = self.add_panel(i,panel)
            self.add_shelf(i,panel,is_top=True)
            self.add_shelf(i,panel,is_top=False)
            self.add_top_cleat(i,panel)
            self.add_bottom_cleat(i,panel)
            self.add_closet_opening(i,panel)
            self.add_backing(i,panel)

class PROMPTS_Upper_Starter(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".upper"
    bl_label = "Upper Starter Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    tabs = bpy.props.EnumProperty(name="Tabs",
                        items=[('OPENINGS','Opening Sizes','Show the Width x Height x Depth for each opening'),
                               ('CONSTRUCTION','Construction Options','Show Additional Construction Options')],
                        default = 'OPENINGS')
    
    placement_on_wall = bpy.props.EnumProperty(name="Placement on Wall",items=[('SELECTED_POINT',"Selected Point",""),
                                                                     ('FILL',"Fill",""),
                                                                     ('FILL_LEFT',"Fill Left",""),
                                                                     ('LEFT',"Left",""),
                                                                     ('CENTER',"Center",""),
                                                                     ('RIGHT',"Right",""),
                                                                     ('FILL_RIGHT',"Fill Right","")],default = 'SELECTED_POINT')
    
    quantity = bpy.props.IntProperty(name="Quantity",default=1)
    
    current_location = bpy.props.FloatProperty(name="Current Location", default=0,subtype='DISTANCE')
    left_offset = bpy.props.FloatProperty(name="Left Offset", default=0,subtype='DISTANCE')
    right_offset = bpy.props.FloatProperty(name="Right Offset", default=0,subtype='DISTANCE')
    product_width = bpy.props.FloatProperty(name="Product Width", default=0,subtype='DISTANCE')    
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)
    depth_1 = bpy.props.FloatProperty(name="Depth 1",unit='LENGTH',precision=4)
    depth_2 = bpy.props.FloatProperty(name="Depth 2",unit='LENGTH',precision=4)
    height_list = bpy.props.EnumProperty(name="Height",
                          items=common_lists.PANEL_HEIGHTS,
                          default = '2131',
                          update=update_closet_height)
    

    Left_End_Condition = bpy.props.EnumProperty(name="Left Side",
                                       items=common_lists.END_CONDITIONS,
                                       default = 'WP')
    
    Right_End_Condition = bpy.props.EnumProperty(name="Right Side",
                                        items=common_lists.END_CONDITIONS,
                                        default = 'WP')
    
    product = None
    
    is_island = None
    is_single_island = None
    
    inserts = []
    
    default_width = 0
    selected_location = 0

    def check(self, context):
        self.product.obj_x.location.x = self.width
        props = props_closet.get_scene_props()

        if not props.closet_defaults.use_32mm_system:
            self.product.obj_z.location.z = -self.height

        left_end_condition = self.product.get_prompt("Left End Condition")
        right_end_condition = self.product.get_prompt("Right End Condition")
        
        if left_end_condition:
            left_end_condition.set_value(self.Left_End_Condition)
        
        if right_end_condition:
            right_end_condition.set_value(self.Right_End_Condition)
        
        self.update_placement(context)
        
        utils.run_calculators(self.product.obj_bp)
        #Hack I Dont know why i need to run calculators twice just for left right side removal
#         utils.run_calculators(self.product.obj_bp)
        return True

    def set_product_defaults(self):
        self.product.obj_bp.location.x = self.selected_location + self.left_offset
        self.product.obj_x.location.x = self.default_width - (self.left_offset + self.right_offset)

    def update_placement(self,context):
        left_x = self.product.get_collision_location('LEFT')
        right_x = self.product.get_collision_location('RIGHT')
        offsets = self.left_offset + self.right_offset
        if self.placement_on_wall == 'SELECTED_POINT':
            self.product.obj_bp.location.x = self.current_location
        if self.placement_on_wall == 'FILL':
            self.product.obj_bp.location.x = left_x + self.left_offset
            self.product.obj_x.location.x = (right_x - left_x - offsets) / self.quantity
        if self.placement_on_wall == 'LEFT':
            self.product.obj_bp.location.x = left_x + self.left_offset
            self.product.obj_x.location.x = self.width
        if self.placement_on_wall == 'RIGHT':
            if self.product.obj_bp.mv.placement_type == 'Corner':
                self.product.obj_bp.rotation_euler.z = math.radians(-90)
            self.product.obj_x.location.x = self.width
            self.product.obj_bp.location.x = (right_x - self.product.calc_width()) - self.right_offset
#         utils.run_calculators(self.product.obj_bp)        

    def execute(self, context):
        obj_list = []
        obj_list = utils.get_child_objects(self.product.obj_bp, obj_list)
        for obj in obj_list:
            if obj.type == 'EMPTY':
                obj.hide = True
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                utils.run_calculators(self.product.obj_bp)
        return {'FINISHED'}

    def set_default_heights(self):
        self.height = math.fabs(self.product.obj_z.location.z)
        props = props_closet.get_scene_props()
        if props.closet_defaults.use_32mm_system:        
            opening_height = math.fabs(round(unit.meter_to_millimeter(self.product.obj_z.location.z),0))
            for index, height in enumerate(common_lists.PANEL_HEIGHTS):
                if not opening_height >= int(height[0]):
                    print("SETTING HEIGHT",height)
                    exec('self.height_list = common_lists.PANEL_HEIGHTS[index - 1][0]')                                                                                                                                                                                                        
                    break

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_product_bp = utils.get_bp(obj,'PRODUCT')
        self.product = fd_types.Assembly(obj_product_bp)
        if self.product.obj_bp:

            self.set_default_heights()
            self.width = math.fabs(self.product.obj_x.location.x)
            new_list = []
            self.inserts = utils.get_insert_bp_list(self.product.obj_bp,new_list)
            left_end_condition = self.product.get_prompt("Left End Condition")
            right_end_condition = self.product.get_prompt("Right End Condition")
            if left_end_condition:
                self.Left_End_Condition = left_end_condition.value()
            if right_end_condition:
                self.Right_End_Condition = right_end_condition.value()
                
        self.current_location = self.product.obj_bp.location.x
        self.selected_location = self.product.obj_bp.location.x
        self.default_width = self.product.obj_x.location.x
        self.width = self.product.obj_x.location.x
        self.placement_on_wall = 'SELECTED_POINT'
        self.left_offset = 0
        self.right_offset = 0
                
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=600)

    def convert_to_height(self,number):
        for index, height in enumerate(common_lists.PANEL_HEIGHTS):
            if not number * 1000 >= float(height[0]):
                return common_lists.PANEL_HEIGHTS[index - 1][0]

    def draw_product_size(self,layout):
        props = props_closet.get_scene_props()
        
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
        if self.object_has_driver(self.product.obj_z):
            row1.label('Hang Height: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z))))
        else:

            if props.closet_defaults.use_32mm_system:
                row1 = col.row(align=True)
                row1.prop(self,'height_list',text="Height")
            else:
                row1 = col.row(align=True)
                row1.label('Height:')
                row1.prop(self,'height',text="")
                row1.prop(self.product.obj_z,'hide',text="")         

            row1 = col.row(align=True)
            row1.label('Hang Height:')
            row1.prop(self.product.obj_bp,'location',index=2,text="")      
        
    def object_has_driver(self,obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True
            
    def draw_common_prompts(self,layout):
        box = layout.box()
        col = box.column(align=True)
        col.prop(self,'Left_End_Condition')
        col.prop(self,'Right_End_Condition')
        
    def get_number_of_equal_widths(self):
        number_of_equal_widths = 0
        
        for i in range(1,9):
            width = self.product.get_prompt("Opening " + str(i) + " Width")
            if width:
                number_of_equal_widths += 1 if width.equal else 0
            else:
                break
            
        return number_of_equal_widths
        
    def draw_splitter_widths(self,layout):
        props = props_closet.get_scene_props()

        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        row.label("Opening Name:")
        row.label("",icon='BLANK1')
        row.label("Width:")
        if not self.is_island or not self.is_single_island:
            row.label("Depth:")
        
        box = col.box()
        
        for i in range(1,9):
            width = self.product.get_prompt("Opening " + str(i) + " Width")
            depth = self.product.get_prompt("Opening " + str(i) + " Depth")
            if width:
                row = box.row()
                row.label( str(i) + ":")
                if width.equal == False:
                    row.prop(width,'equal',text="")
                else:
                    if self.get_number_of_equal_widths() != 1:
                        row.prop(width,'equal',text="")
                    else:
                        row.label("",icon='BLANK1')
                if width.equal:
                    row.label(str(unit.meter_to_active_unit(width.DistanceValue)) + '"')
                else:
                    row.prop(width,'DistanceValue',text="")
                row.prop(depth,'DistanceValue',text="")
                
    def draw_ctf_options(self,layout):
        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("CTF Opening " + str(i))
            if prompt:
                prompts.append(prompt)
                
        row = layout.row()
        row.label("Variable Section:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))
            
    def draw_top_shelf_options(self,layout):
        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("Remove Top Shelf " + str(i))
            if prompt:
                prompts.append(prompt)            
            
        row = layout.row()
        row.label("Top KD:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1)) 

    def draw_cleat_options(self,layout):
        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("Add " + str(i) + " Top Cleat")
            if prompt:
                prompts.append(prompt)

        row = layout.row()
        row.label("Top Cleat:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("Add " + str(i) + " Bottom Cleat")
            if prompt:
                prompts.append(prompt)

        row = layout.row()
        row.label("Bottom Cleat:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))

#         for i, prompt in enumerate(prompts):
#             if prompt.CheckBoxValue:
#                 loc_prompt = self.product.get_prompt("Cleat " + str(i + 1) + " Location")
#                 row = layout.row()
#                 row.label("Cleat " + str(i + 1) + " Location")
#                 row.prop(loc_prompt,"DistanceValue",text=str(i + 1))            
            
    def draw_bottom_options(self,layout):
        prompts = []
        for i in range(1,9):
            prompt = self.product.get_prompt("Remove Bottom Hanging Shelf " + str(i))
            if prompt:
                prompts.append(prompt)            
            
        row = layout.row()
        row.label("Bottom KD:")
        for i, prompt in enumerate(prompts):
            row.prop(prompt,"CheckBoxValue",text=str(i + 1))            
            
    def draw_construction_options(self,layout):
        box = layout.box()
        
        left_wall_filler = self.product.get_prompt("Left Side Wall Filler")
        right_wall_filler = self.product.get_prompt("Right Side Wall Filler")
        add_backing = self.product.get_prompt("Add Backing")

        # SIDE OPTIONS:
        if left_wall_filler and right_wall_filler:
            split = box.split()
            col = split.column(align=True)
            col.label("Filler Options:")
            row = col.row()
            row.prop(left_wall_filler,'DistanceValue',text="Left Filler Amount")
            row = col.row()
            row.prop(right_wall_filler,'DistanceValue',text="Right Filler Amount")
            
        self.draw_ctf_options(box)
        self.draw_top_shelf_options(box)
        self.draw_cleat_options(box)
        self.draw_bottom_options(box)
        
        # CARCASS OPTIONS:
        col = box.column(align=True)
        col.label("Back Options:")
        row = col.row()
        if add_backing:
            row.prop(add_backing,'CheckBoxValue',text="Add Backing")     
            
    def draw_new_machining_options(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Opening Name:")
        row.label("Top:")
        row.label("Bottom:")
        row.label("Mid Row:")
        row.label("Drill Thru:")
        row.label("Remove:")
        
        for i in range(1,9):
            stop_lb = self.product.get_prompt("Opening " + str(i) + " Stop LB")
            start_lb = self.product.get_prompt("Opening " + str(i) + " Start LB")
            drill_thru_left = self.product.get_prompt("Opening " + str(i) + " Drill Thru Left")
            drill_thru_right = self.product.get_prompt("Opening " + str(i) + " Drill Thru Right")
            add_mid = self.product.get_prompt("Opening " + str(i) + " Add Mid Drilling")
            remove_left_drill = self.product.get_prompt("Opening " + str(i) + " Remove Left Drill")
            remove_right_drill = self.product.get_prompt("Opening " + str(i) + " Remove Right Drill")
            
            if stop_lb:
                row = box.row(align=True)
                row.label('Opening ' + str(i) + ":")
                row.prop(self,'height',text="")
                row.prop(self,'height',text="")
                row.label("",icon='BLANK1')
                row.label("",icon='BLANK1')
                row.label("",icon='BLANK1')
                row.prop(add_mid,'CheckBoxValue',text=" ")
                row.prop(drill_thru_left,'CheckBoxValue',text="")
                row.prop(drill_thru_right,'CheckBoxValue',text=" ")
                row.prop(remove_left_drill,'CheckBoxValue',text="")
                row.prop(remove_right_drill,'CheckBoxValue',text="")
                row.label("",icon='BLANK1')
                row.label("",icon='BLANK1')

    def draw_machining_options(self,layout):
        box = layout.box()
        
        row = box.row()
        row.label("Opening Name:")
        row.label("",icon='BLANK1')
        row.label("Bottom:")
        row.label("Top:")
        row.label("Mid Row:")
        row.label("Drill Thru:")
        row.label("Remove:")
        
        for i in range(1,9):
            stop_lb = self.product.get_prompt("Opening " + str(i) + " Stop LB")
            start_lb = self.product.get_prompt("Opening " + str(i) + " Start LB")
            drill_thru_left = self.product.get_prompt("Opening " + str(i) + " Drill Thru Left")
            drill_thru_right = self.product.get_prompt("Opening " + str(i) + " Drill Thru Right")
            add_mid = self.product.get_prompt("Opening " + str(i) + " Add Mid Drilling")
            remove_left_drill = self.product.get_prompt("Opening " + str(i) + " Remove Left Drill")
            remove_right_drill = self.product.get_prompt("Opening " + str(i) + " Remove Right Drill")
            
            if stop_lb:
                row = box.row(align=True)
                row.label('Opening ' + str(i) + ":")
                row.prop(stop_lb,'DistanceValue',text="Stop")
                row.prop(start_lb,'DistanceValue',text="Stop")
                row.separator()
                row.prop(add_mid,'CheckBoxValue',text=" ")

                row.prop(drill_thru_left,'CheckBoxValue',text="")
                row.prop(drill_thru_right,'CheckBoxValue',text=" ")
                row.prop(remove_left_drill,'CheckBoxValue',text="")
                row.prop(remove_right_drill,'CheckBoxValue',text="")

    def draw_product_placment(self,layout):
        box = layout.box()
        
        row = box.row(align=True)
        row.label('Placement',icon='LATTICE_DATA')
        row.prop_enum(self, "placement_on_wall", 'SELECTED_POINT', icon='MAN_TRANS', text="Selected Point")
        row.prop_enum(self, "placement_on_wall", 'FILL', icon='ARROW_LEFTRIGHT', text="Fill")
        row.prop_enum(self, "placement_on_wall", 'LEFT', icon='TRIA_LEFT', text="Left") 
        row.prop_enum(self, "placement_on_wall", 'RIGHT', icon='TRIA_RIGHT', text="Right") 
        
        if self.placement_on_wall == 'FILL':
            row = box.row(align=True)
            row.label('Offset',icon='ARROW_LEFTRIGHT')
            row.prop(self, "left_offset", icon='TRIA_LEFT', text="Left") 
            row.prop(self, "right_offset", icon='TRIA_RIGHT', text="Right") 
        
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
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:

                box = layout.box()
                box.label(self.product.obj_bp.mv.name_object,icon='LATTICE_DATA')
                
                split = box.split(percentage=.5)
                self.draw_product_size(split)
                self.draw_common_prompts(split)
                row = box.row()
                row.prop(self,'tabs',expand=True)
                if self.tabs == 'OPENINGS':
                    self.draw_splitter_widths(box)
                elif self.tabs == 'CONSTRUCTION':
                    self.draw_construction_options(box)
#                 else:
#                     self.draw_machining_options(box)
                self.draw_product_placment(box)        
                
class OPERATOR_Place_Stacked_Carcass(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_stacked_carcass"
    bl_label = "Place Stacked Carcass"
    bl_description = "This allows you to place a stacked carcass."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.assembly = fd_types.Assembly(bp)
        utils.set_wireframe(self.assembly.obj_bp,True)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.assembly:
            utils.delete_object_and_children(self.assembly.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def stacked_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        sel_product_bp = utils.get_bp(selected_obj,'PRODUCT')
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)
        wall_bp = utils.get_wall_bp(selected_obj)
        
        if sel_product_bp and sel_assembly_bp:
            product = fd_types.Assembly(sel_product_bp)
            props = props_closet.get_object_props(product.obj_bp)

            self.assembly.obj_bp.parent = product.obj_bp.parent
            self.assembly.obj_bp.location.x = product.obj_bp.location.x
            self.assembly.obj_bp.location.z = math.fabs(product.obj_z.location.z) + math.fabs(self.assembly.obj_z.location.z)
            self.assembly.obj_x.location.x = product.obj_x.location.x
            
            ass_props = props_closet.get_object_props(sel_assembly_bp)
            if ass_props.is_plant_on_top_bp:
                sel_assembly = fd_types.Assembly(sel_assembly_bp)
                self.assembly.obj_bp.location.z += math.fabs(sel_assembly.obj_z.location.z)               

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                utils.set_wireframe(self.assembly.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.assembly.obj_bp
                self.assembly.obj_bp.select = True
                return {'FINISHED'}
            
        elif wall_bp:
            wall = fd_types.Assembly(wall_bp)
            
            self.assembly.obj_bp.rotation_euler = wall.obj_bp.rotation_euler
            self.assembly.obj_bp.location.x = selected_point[0]
            self.assembly.obj_bp.location.y = selected_point[1]

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                x_loc = utils.calc_distance((self.assembly.obj_bp.location.x,self.assembly.obj_bp.location.y,0),
                                        (wall_bp.matrix_local[0][3],wall_bp.matrix_local[1][3],0))
                self.assembly.obj_bp.location = (0,0,self.assembly.obj_bp.location.z)
                self.assembly.obj_bp.rotation_euler = (0,0,0)
                self.assembly.obj_bp.parent = wall_bp
                self.assembly.obj_bp.location.x = x_loc
                                
                utils.set_wireframe(self.assembly.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.assembly.obj_bp
                self.assembly.obj_bp.select = True
                return {'FINISHED'}            

        utils.run_calculators(self.assembly.obj_bp)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.stacked_drop(context,event)                    
                
bpy.utils.register_class(PROMPTS_Upper_Starter)
bpy.utils.register_class(OPERATOR_Place_Stacked_Carcass)