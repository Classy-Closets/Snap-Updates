import bpy
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_lists

class Vertical_Splitters(fd_types.Assembly):
    
    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".vertical_splitters"
    mirror_y = False
  
    ''' Number of openings to create for this splitter
    '''
    vertical_openings = 2 #1-10
    
    ''' Override the default height for the openings
        0 will make the opening calculate equally
    '''
    opening_1_height = 0
    opening_2_height = 0
    opening_3_height = 0
    opening_4_height = 0
    opening_5_height = 0
    opening_6_height = 0
    opening_7_height = 0
    opening_8_height = 0
    opening_9_height = 0
    opening_10_height = 0
    
    
    ''' This will remove the splitter part but still 
        create an opening
    '''    
    remove_splitter_1 = False
    remove_splitter_2 = False
    remove_splitter_3 = False
    remove_splitter_4 = False
    remove_splitter_5 = False
    remove_splitter_6 = False
    remove_splitter_7 = False
    remove_splitter_8 = False
    remove_splitter_9 = False
    
    ''' fd_types.Assembly to put into the interior
        or exterior of the opening
    '''
    interior_1 = None
    exterior_1 = None
    interior_2 = None
    exterior_2 = None
    interior_3 = None
    exterior_3 = None
    interior_4 = None
    exterior_4 = None
    interior_5 = None
    exterior_5 = None
    interior_6 = None
    exterior_6 = None
    interior_7 = None
    exterior_7 = None
    interior_8 = None
    exterior_8 = None
    interior_9 = None
    exterior_9 = None
    interior_10 = None
    exterior_10 = None
    interior_11 = None
    exterior_11 = None
    
    def add_prompts(self):
        self.add_tab(name='Opening Heights',tab_type='CALCULATOR',calc_type="ZDIM")    
        self.add_tab(name='Formulas',tab_type='HIDDEN')    
        
        for i in range(1,self.vertical_openings+1):
        
            size = eval("self.opening_" + str(i) + "_height")
        
            self.add_prompt(name="Opening " + str(i) + " Height",
                            prompt_type='DISTANCE',
                            value=size,
                            tab_index=0,
                            equal=True if size == 0 else False)
    
        self.add_prompt(name="Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Left Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Inlcude Bottom Shelf",prompt_type='CHECKBOX',value=True,tab_index=1)
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        Thickness = self.get_var('Thickness')
        
        self.prompt("Thickness", 'THICKNESS(sgi,"Panel")',[sgi])
        self.calculator_deduction("Thickness*(" + str(self.vertical_openings) +"-1)",[Thickness])
        
    def add_insert(self,insert,index,z_loc_vars=[],z_loc_expression=""):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        open_var = eval("self.get_var('Opening " + str(index) + " Height')")
        z_dim_expression = "Opening_" + str(index) + "_Height"
        
        if insert:
            if not insert.obj_bp:
                insert.draw()
            insert.obj_bp.parent = self.obj_bp
            insert.x_loc(value = 0)
            insert.y_loc(value = 0)
            if index == self.vertical_openings:
                insert.z_loc(value = 0)
            else:
                insert.z_loc(z_loc_expression,z_loc_vars)
            insert.x_rot(value = 0)
            insert.y_rot(value = 0)
            insert.z_rot(value = 0)
            insert.x_dim('Width',[Width])
            insert.y_dim('Depth',[Depth])
            insert.z_dim(z_dim_expression,[open_var])
            if index == 1:
                # ALLOW DOOR TO EXTEND TO TOP OF VALANCE
                extend_top_amount = insert.get_prompt("Extend Top Amount")
                if extend_top_amount:
                    Extend_Top_Amount = self.get_var("Extend Top Amount")
                    insert.prompt('Extend Top Amount','Extend_Top_Amount',[Extend_Top_Amount])
            
            if index == self.vertical_openings:
                # ALLOW DOOR TO EXTEND TO BOTTOM OF VALANCE
                extend_bottom_amount = insert.get_prompt("Extend Bottom Amount")
                if extend_bottom_amount:
                    Extend_Bottom_Amount = self.get_var("Extend Bottom Amount")
                    insert.prompt('Extend Bottom Amount','Extend_Bottom_Amount',[Extend_Bottom_Amount])
        
    def get_opening(self,index):
        opening = common_parts.add_opening(self)
        
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))
        
        if interior:
            opening.obj_bp.mv.interior_open = False
        
        if exterior:
            opening.obj_bp.mv.exterior_open = False
            
        return opening
        
    def add_splitters(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Thickness = self.get_var('Thickness')
        Inlcude_Bottom_Shelf = self.get_var('Inlcude Bottom Shelf')
        
        previous_splitter = None
        
        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.x_loc(value = 0)
        bottom_shelf.y_loc('Depth',[Depth])
        bottom_shelf.z_loc(value = 0)
        bottom_shelf.x_rot(value = 0)
        bottom_shelf.y_rot(value = 0)
        bottom_shelf.z_rot(value = 0)
        bottom_shelf.x_dim('Width',[Width])
        bottom_shelf.y_dim('-Depth',[Depth])
        bottom_shelf.z_dim('-Thickness',[Thickness])
        bottom_shelf.prompt('Hide','IF(Inlcude_Bottom_Shelf,False,True)',[Inlcude_Bottom_Shelf])
        
        for i in range(1,self.vertical_openings):

            z_loc_vars = []
            open_var = eval("self.get_var('Opening " + str(i) + " Height')")
            z_loc_vars.append(open_var)
            
            if previous_splitter:
                z_loc = previous_splitter.get_var("loc_z","Splitter_Z_Loc")
                z_loc_vars.append(z_loc)
                
            splitter = common_parts.add_shelf(self)
            
            Is_Locked_Shelf = splitter.get_var('Is Locked Shelf')
            Adj_Shelf_Setback = splitter.get_var('Adj Shelf Setback')
            Locked_Shelf_Setback = splitter.get_var('Locked Shelf Setback')
            Adj_Shelf_Clip_Gap = splitter.get_var('Adj Shelf Clip Gap')    
            
            splitter.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_loc('Depth',[Depth])
            if previous_splitter:
                z_loc_vars.append(Thickness)
                splitter.z_loc('Splitter_Z_Loc-Opening_' + str(i) + '_Height-Thickness',z_loc_vars)
            else:
                z_loc_vars.append(Height)
                splitter.z_loc('Height-Opening_' + str(i) + '_Height',z_loc_vars)
            splitter.x_rot(value = 0)
            splitter.y_rot(value = 0)
            splitter.z_rot(value = 0)
            splitter.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',[Depth,Locked_Shelf_Setback,Is_Locked_Shelf,Adj_Shelf_Setback])
            splitter.z_dim('-Thickness',[Thickness])
            remove_splitter = eval("self.remove_splitter_" + str(i))
            if remove_splitter:
                splitter.prompt('Hide',value=True)
            
            previous_splitter = splitter
            
            opening_z_loc_vars = []
            opening_z_loc = previous_splitter.get_var("loc_z","Splitter_Z_Loc")
            opening_z_loc_vars.append(opening_z_loc)
            
            exterior = eval('self.exterior_' + str(i))
            self.add_insert(exterior, i, opening_z_loc_vars, "Splitter_Z_Loc")
            
            interior = eval('self.interior_' + str(i))
            self.add_insert(interior, i, opening_z_loc_vars, "Splitter_Z_Loc")
            
            opening = self.get_opening(i)
            self.add_insert(opening, i, opening_z_loc_vars, "Splitter_Z_Loc")

        #ADD LAST INSERT
        bottom_exterior = eval('self.exterior_' + str(self.vertical_openings))
        self.add_insert(bottom_exterior, self.vertical_openings)
        
        bottom_interior = eval('self.interior_' + str(self.vertical_openings))
        self.add_insert(bottom_interior, self.vertical_openings)

        bottom_opening = self.get_opening(self.vertical_openings)
        self.add_insert(bottom_opening, self.vertical_openings)

    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_splitter_bp = True
        
        self.add_prompts()
        
        self.add_splitters()
        
        self.update()
        
class Horizontal_Splitters(fd_types.Assembly):
    
    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".horizontal_splitters"
    mirror_y = False

    ''' Number of openings to create for this splitter
    '''
    horizontal_openings = 2 #1-10
    
    ''' Override the default width for the openings
        0 will make the opening calculate equally
    '''    
    opening_1_width = 0
    opening_2_width = 0
    opening_3_width = 0
    opening_4_width = 0
    opening_5_width = 0
    opening_6_width = 0
    opening_7_width = 0
    opening_8_width = 0
    opening_9_width = 0
    opening_10_width = 0
    
    ''' fd_types.Assembly to put into the interior
        or exterior of the opening
    '''    
    interior_1 = None
    exterior_1 = None
    interior_2 = None
    exterior_2 = None
    interior_3 = None
    exterior_3 = None
    interior_4 = None
    exterior_4 = None
    interior_5 = None
    exterior_5 = None
    interior_6 = None
    exterior_6 = None
    interior_7 = None
    exterior_7 = None
    interior_8 = None
    exterior_8 = None
    interior_9 = None
    exterior_9 = None
    interior_10 = None
    exterior_10 = None
    interior_11 = None
    exterior_11 = None
    
    def add_prompts(self):
        self.add_tab(name='Opening Widths',tab_type='CALCULATOR',calc_type="XDIM")    
        self.add_tab(name='Formulas',tab_type='HIDDEN')    
        
        for i in range(1,self.horizontal_openings+1):
        
            size = eval("self.opening_" + str(i) + "_width")
        
            self.add_prompt(name="Opening " + str(i) + " Width",
                            prompt_type='DISTANCE',
                            value=size,
                            tab_index=0,
                            equal=True if size == 0 else False)
    
        self.add_prompt(name="Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
        
        Thickness = self.get_var('Thickness')
        
        self.calculator_deduction("Thickness*(" + str(self.horizontal_openings) +"-1)",[Thickness])
        
    def add_insert(self,insert,index,x_loc_vars=[],x_loc_expression=""):
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        open_var = eval("self.get_var('Opening " + str(index) + " Width')")
        x_dim_expression = "Opening_" + str(index) + "_Width"
        
        if insert:
            if not insert.obj_bp:
                insert.draw()

            insert.obj_bp.parent = self.obj_bp
            if index == 1:
                insert.x_loc(value = 0)
            else:
                insert.x_loc(x_loc_expression,x_loc_vars)
            insert.y_loc(value = 0)
            insert.z_loc(value = 0)
            insert.x_rot(value = 0)
            insert.y_rot(value = 0)
            insert.z_rot(value = 0)
            insert.x_dim(x_dim_expression,[open_var])
            insert.y_dim('Depth',[Depth])
            insert.z_dim('Height',[Height])
        
    def get_opening(self,index):
        opening = common_parts.add_opening(self)
        exterior = eval('self.exterior_' + str(index))
        interior = eval('self.interior_' + str(index))
        
        if interior:
            opening.obj_bp.mv.interior_open = False
        
        if exterior:
            opening.obj_bp.mv.exterior_open = False
            
        return opening
        
    def add_splitters(self):
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Thickness = self.get_var('Thickness')
        
        previous_splitter = None
        
        for i in range(1,self.horizontal_openings):
            
            x_loc_vars = []
            open_var = eval("self.get_var('Opening " + str(i) + " Width')")
            x_loc_vars.append(open_var)
            
            if previous_splitter:
                x_loc = previous_splitter.get_var("loc_x","Splitter_X_Loc")
                x_loc_vars.append(x_loc)
                x_loc_vars.append(Thickness)

            splitter = common_parts.add_division(self)
            if previous_splitter:
                splitter.x_loc("Splitter_X_Loc+Thickness+Opening_" + str(i) + "_Width",x_loc_vars)
            else:
                splitter.x_loc("Opening_" + str(i) + "_Width",[open_var])
                
            splitter.y_loc('Depth',[Depth])
            splitter.z_loc(value = 0)
            splitter.x_rot(value = 0)
            splitter.y_rot(value = -90)
            splitter.z_rot(value = 0)
            splitter.x_dim('Height',[Height])
            splitter.y_dim('-Depth',[Depth])
            splitter.z_dim('-Thickness',[Thickness])
            
            previous_splitter = splitter

            exterior = eval('self.exterior_' + str(i))
            self.add_insert(exterior, i, x_loc_vars, "Splitter_X_Loc+Thickness")
            
            interior = eval('self.interior_' + str(i))
            self.add_insert(interior, i, x_loc_vars, "Splitter_X_Loc+Thickness")
            
            opening = self.get_opening(i)
            self.add_insert(opening, i, x_loc_vars, "Splitter_X_Loc+Thickness")
            
        insert_x_loc_vars = []
        insert_x_loc = previous_splitter.get_var("loc_x","Splitter_X_Loc")
        insert_x_loc_vars.append(insert_x_loc)
        insert_x_loc_vars.append(Thickness)

        #ADD LAST INSERT
        last_exterior = eval('self.exterior_' + str(self.horizontal_openings))
        self.add_insert(last_exterior, self.horizontal_openings,insert_x_loc_vars, "Splitter_X_Loc+Thickness")
          
        last_interior = eval('self.interior_' + str(self.horizontal_openings))
        self.add_insert(last_interior, self.horizontal_openings,insert_x_loc_vars, "Splitter_X_Loc+Thickness")

        last_opening = self.get_opening(self.horizontal_openings)
        self.add_insert(last_opening, self.horizontal_openings,insert_x_loc_vars, "Splitter_X_Loc+Thickness")
        
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_splitter_bp = True        
        
        self.add_prompts()
        
        self.add_splitters()
        
        self.update()

class PROMPTS_Vertical_Splitter_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".vertical_splitters"
    bl_label = "Vertical Splitter Prompts" 
    bl_description = "This shows all of the available vertical splitter options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    Opening_1_Height = bpy.props.EnumProperty(name="Opening 1 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_2_Height = bpy.props.EnumProperty(name="Opening 2 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_3_Height = bpy.props.EnumProperty(name="Opening 3 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_4_Height = bpy.props.EnumProperty(name="Opening 4 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_5_Height = bpy.props.EnumProperty(name="Opening 5 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_6_Height = bpy.props.EnumProperty(name="Opening 6 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_7_Height = bpy.props.EnumProperty(name="Opening 7 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_8_Height = bpy.props.EnumProperty(name="Opening 8 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_9_Height = bpy.props.EnumProperty(name="Opening 9 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_10_Height = bpy.props.EnumProperty(name="Opening 10 Height",
                                    items=common_lists.OPENING_HEIGHTS)                    
    
    assembly = None

    def check(self, context):
        props = props_closet.get_scene_props()
        if props.closet_defaults.use_32mm_system:
            self.set_prompts_from_properties()
        utils.run_calculators(self.assembly.obj_bp)
        return True
        
    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''        
        for i in range(1,10):
            opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
            if opening:
                if not opening.equal:
                    exec("opening.DistanceValue = unit.inch(float(self.Opening_" + str(i) + "_Height) / 25.4)")        
        
    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        for i in range(1,10):
            opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
            if opening:
                value = round(opening.value() * 1000,2)
                for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        exec("self.Opening_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[index - 1][0]")
                        break

    def get_splitter(self,obj_bp):
        ''' Gets the splitter based on selection
        '''
        props = props_closet.get_object_props(obj_bp)
        if props.is_splitter_bp:
            return fd_types.Assembly(obj_bp)
        if obj_bp.parent:
            return self.get_splitter(obj_bp.parent)

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = self.get_splitter(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
    
    def execute(self, context):
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                
                for i in range(1,10):
                    opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
                    if opening:
                        row = box.row()
                        row.label("Opening " + str(i) + " Height:")
                        if opening.equal:
                            row.label(str(unit.meter_to_active_unit(opening.DistanceValue)) + '"')
                            row.prop(opening,'equal',text="")
                        else:
                            props = props_closet.get_scene_props()
                            if props.closet_defaults.use_32mm_system:
                                row.prop(self,'Opening_' + str(i) + '_Height',text="")
                            else:
                                row.prop(opening,'DistanceValue',text="")
                            row.prop(opening,'equal',text="")
                
                include_bottom_shelf=self.assembly.get_prompt('Inlcude Bottom Shelf')
                include_bottom_shelf.draw_prompt(box)            
                        
class PROMPTS_Horizontal_Splitter_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".horizontal_splitters"
    bl_label = "Horizontal Splitter Prompts" 
    bl_description = "This shows all of the available horizontal splitter options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    def check(self, context):
        utils.run_calculators(self.assembly.obj_bp)
        return True
        
    def get_splitter(self,obj_bp):
        ''' Gets the splitter based on selection
        '''
        props = props_closet.get_object_props(obj_bp)
        if props.is_splitter_bp:
            return fd_types.Assembly(obj_bp)
        if obj_bp.parent:
            return self.get_splitter(obj_bp.parent)        
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = self.get_splitter(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)        
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                for i in range(1,10):
                    opening = self.assembly.get_prompt("Opening " + str(i) + " Width")
                    if opening:
                        row = box.row()
                        row.label("Opening " + str(i) + " Width:")
                        if opening.equal:
                            row.label(str(unit.meter_to_active_unit(opening.DistanceValue)) + '"')
                            row.prop(opening,'equal',text="")
                        else:
                            row.prop(opening,'DistanceValue',text="")
                            row.prop(opening,'equal',text="")  
                
bpy.utils.register_class(PROMPTS_Vertical_Splitter_Prompts)                
bpy.utils.register_class(PROMPTS_Horizontal_Splitter_Prompts)   
