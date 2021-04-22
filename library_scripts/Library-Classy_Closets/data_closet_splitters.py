import bpy
from mv import fd_types, unit, utils
from os import path
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_lists
import math

class Vertical_Splitters(fd_types.Assembly):
    
    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".vertical_splitters"
    mirror_y = False
    def add_prompts(self):
        self.add_tab(name='Opening Heights',tab_type='CALCULATOR',calc_type="ZDIM")    
        self.add_tab(name='Formulas',tab_type='HIDDEN')    
                    

        for i in range(1,16):
        
            self.add_prompt(name="Shelf " + str(i) + " Setback",prompt_type='DISTANCE',value=0,tab_index=1)
            self.add_prompt(name="Opening " + str(i) + " Height",
                            prompt_type='DISTANCE',
                            value=unit.millimeter(76.962),
                            tab_index=1)
    
        self.add_prompt(name="Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Left Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Right Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=1)
        self.add_prompt(name="Extend Top Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Extend Bottom Amount",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)
        self.add_prompt(name="Remove Bottom Shelf",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=5,tab_index=1)
        self.add_prompt(name="Evenly Spaced Shelves",prompt_type='CHECKBOX',value=True ,tab_index=1)
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        Thickness = self.get_var('Thickness')
        
        self.prompt("Thickness", 'THICKNESS(sgi,"Panel")',[sgi])        
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
        Remove_Bottom_Shelf = self.get_var('Remove Bottom Shelf')
        Shelf_Quantity =self.get_var('Shelf Quantity')
        
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
        bottom_shelf.prompt('Hide','IF(Remove_Bottom_Shelf,True,False)',[Remove_Bottom_Shelf])
        bottom_shelf.prompt('Is Locked Shelf',value=True)
        
        for i in range(1,16):

            Opening_Height = self.get_var('Opening ' + str(i) + ' Height','Opening_Height')
            
            if previous_splitter:
                Previous_Z_Loc = previous_splitter.get_var("loc_z","Previous_Z_Loc")
                
            splitter = common_parts.add_shelf(self)
            
            Is_Locked_Shelf = splitter.get_var('Is Locked Shelf')
            Adj_Shelf_Setback = splitter.get_var('Adj Shelf Setback')
            Locked_Shelf_Setback = splitter.get_var('Locked Shelf Setback')
            Adj_Shelf_Clip_Gap = splitter.get_var('Adj Shelf Clip Gap')    
            Shelf_Setback = self.get_var("Shelf " + str(i) + " Setback", 'Shelf_Setback')
            
            splitter.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_loc('Depth',[Depth])
            if previous_splitter:
                splitter.z_loc('Previous_Z_Loc+Opening_Height',[Opening_Height,Previous_Z_Loc])
            else:
                splitter.z_loc('Opening_Height+INCH(0.58)',[Opening_Height])
            splitter.x_rot(value = 0)
            splitter.y_rot(value = 0)
            splitter.z_rot(value = 0)
            splitter.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Shelf_Setback',[Depth,Locked_Shelf_Setback,Is_Locked_Shelf,Adj_Shelf_Setback,Shelf_Setback])
            splitter.z_dim('-Thickness',[Thickness])
            splitter.prompt('Hide','IF(Shelf_Quantity+1>'+str(i)+',False,True)',[Shelf_Quantity])
            
            
            
       
            opening = common_parts.add_opening(self)
            opening.obj_bp.mv.opening_name = str(i) 
            opening.x_loc(value=0)
            opening.y_loc(value=0)
            if previous_splitter:
                opening_z_loc = previous_splitter.get_var("loc_z","opening_z_loc")
                opening.z_loc('opening_z_loc',[opening_z_loc])
                opening.z_dim('Opening_Height-Thickness',[Opening_Height,Thickness])
            else:
                opening.z_loc(value = 0)
                opening.z_dim('Opening_Height-Thickness+INCH(0.58)',[Opening_Height,Thickness])
            opening.x_rot(value=0)
            opening.y_rot(value=0)
            opening.z_rot(value=0)
            opening.x_dim('Width',[Width])
            opening.y_dim('Depth',[Depth])
            
            previous_splitter = splitter

        #ADD LAST INSERT
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
    
    Opening_11_Height = bpy.props.EnumProperty(name="Opening 11 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_12_Height = bpy.props.EnumProperty(name="Opening 12 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_13_Height = bpy.props.EnumProperty(name="Opening 13 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_14_Height = bpy.props.EnumProperty(name="Opening 14 Height",
                                    items=common_lists.OPENING_HEIGHTS)
    
    Opening_15_Height = bpy.props.EnumProperty(name="Opening 15 Height",
                                    items=common_lists.OPENING_HEIGHTS)                       
    
    assembly = None
    shelf_quantity = bpy.props.EnumProperty(name="Shelf Quantity",
                                   items=[('1',"1",'1'),
                                          ('2',"2",'2'),
                                          ('3',"3",'3'),
                                          ('4',"4",'4'),
                                          ('5',"5",'5'),
                                          ('6',"6",'6'),
                                          ('7',"7",'7'),
                                          ('8',"8",'8'),
                                          ('9',"9",'9'),
                                          ('10',"10",'10'),
                                          ('11',"11",'11'),
                                          ('12',"12",'12'),
                                          ('13',"13",'13'),
                                          ('14',"14",'14'),
                                          ('15',"15",'15')],
                                   default = '5')
    cur_shelf_height = None 
    def check(self, context):
        props = props_closet.get_scene_props()
        self.update_openings()
        self.set_prompts_from_properties()
        utils.run_calculators(self.assembly.obj_bp)
        props_closet.update_render_materials(self,context)
        return True
    
    def update_openings(self):
        '''This should be called in the check function before set_prompts_from_properties
           updates which openings are available based on the value of shelf_quantity
        '''
        shelf_quantity = self.assembly.get_prompt("Shelf Quantity") 
        if (shelf_quantity):
            if shelf_quantity.value() != int(self.shelf_quantity):
                for child in self.assembly.obj_bp.children:
                    if child.mv.type_group == 'OPENING':
                        if int(child.mv.opening_name) > int(self.shelf_quantity)+1:
                            child.mv.interior_open = False
                            child.mv.exterior_open = False
                        else:
                            shares_location = False
                            for cchild in self.assembly.obj_bp.children:
                                if cchild.mv.type_group != 'OPENING':
                                    if cchild.location == child.location:
                                        shares_location = True
                            if not shares_location:
                                child.mv.interior_open = True
                                child.mv.exterior_open = True
                                
                                
                                              
    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''
        shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
        if shelf_quantity:
            shelf_quantity.set_value(int(self.shelf_quantity))
        carcass_height = self.assembly.obj_z.location.z
        evenly_spaced_shelves = self.assembly.get_prompt("Evenly Spaced Shelves")
        prompts = [evenly_spaced_shelves]
        
        for i in range(1,int(self.shelf_quantity)+2):
            shelf = self.assembly.get_prompt("Opening " + str(i) + " Height")
            if shelf:
                if not shelf.equal:
                    exec("self.cur_shelf_height = float(self.Opening_" + str(i) + "_Height)/1000")                    #If Shelf was Just Moved
                    if(unit.meter_to_inch(shelf.value()) != unit.meter_to_inch(self.cur_shelf_height)):
                        
                        #Get the height of the previous shelves
                        total_shelf_height = 0
                        for ii in range (1,i+1):
                            exec("self.cur_shelf_height = float(self.Opening_" + str(ii) + "_Height)/1000")
                            total_shelf_height = total_shelf_height + self.cur_shelf_height
                            #print(unit.meter_to_inch(total_shelf_height))

                        #Adjust All Shelves above shelf that was just moved to evenly space themselves in the remaining space
                        for iii in range(i+1,int(self.shelf_quantity)+2):
                            next_shelf = self.assembly.get_prompt("Opening " + str(iii) + " Height")
                            if all(prompts):
                                if(not evenly_spaced_shelves.value()):
                                    hole_count = math.ceil(((carcass_height-total_shelf_height)*1000)/32)
                                    holes_per_shelf = round(hole_count/(int(self.shelf_quantity)+1-i))
                                    if(holes_per_shelf >=3):
                                        next_shelf.set_value(float(common_lists.OPENING_HEIGHTS[holes_per_shelf-3][0])/1000)
                                        exec("self.Opening_" + str(iii) + "_Height = common_lists.OPENING_HEIGHTS[holes_per_shelf-3][0]")
                                    else:
                                        next_shelf.set_value(float(common_lists.OPENING_HEIGHTS[0][0])/1000)
                                        exec("self.Opening_" + str(iii) + "_Height = common_lists.OPENING_HEIGHTS[0][0]")


                        exec("shelf.DistanceValue = unit.inch(float(self.Opening_" + str(i) + "_Height) / 25.4)")  
                
                if all(prompts):
                    if(evenly_spaced_shelves.value()):
                        hole_count = math.ceil((carcass_height*1000)/32)
                        
                        holes_per_shelf = round(hole_count/(int(self.shelf_quantity)+1))
                        remainder = hole_count - (holes_per_shelf * (int(self.shelf_quantity)))

                        if(i <= remainder):
                                holes_per_shelf = holes_per_shelf + 1
                        if(holes_per_shelf >=3):
                            shelf.set_value(float(common_lists.OPENING_HEIGHTS[holes_per_shelf-3][0])/1000)
                            exec("self.Opening_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[holes_per_shelf-3][0]")
                        else:
                            shelf.set_value(float(common_lists.OPENING_HEIGHTS[0][0])/1000)
                            exec("self.Opening_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[0][0]")
        
    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        for i in range(1,16):
            opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
            if opening:
                value = round(opening.value() * 1000,3)
                
                for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        exec("self.Opening_" + str(i) + "_Height = common_lists.OPENING_HEIGHTS[index - 1][0]")
                        break
        shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
        if shelf_quantity:
            self.shelf_quantity = str(shelf_quantity.value())           
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
                row = box.row()
                shelf_quantity = self.assembly.get_prompt("Shelf Quantity")
                if shelf_quantity:
                    col = box.column(align=True)
                    row = col.row()
                    row.label("Qty:")
                    row.prop(self,"shelf_quantity",expand=True)   
                row = box.row()
                evenly_spaced_shelves=self.assembly.get_prompt('Evenly Spaced Shelves')
                if evenly_spaced_shelves:
                    evenly_spaced_shelves.draw_prompt(box)
                for i in range(1,16):
                    opening = self.assembly.get_prompt("Opening " + str(i) + " Height")
                    setback = self.assembly.get_prompt("Shelf " + str(i) + " Setback")
                    if int(self.shelf_quantity) >= i: 
                        if opening:
                            row = box.row()
                            row.label("Opening " + str(i) + " Height:")
                            props = props_closet.get_scene_props()
                            if props.closet_defaults.use_32mm_system and evenly_spaced_shelves:
                                if(evenly_spaced_shelves.value()):
                                    row.label(str(math.ceil((opening.value()*1000)/32)) +"H-" + str(round(unit.meter_to_inch(opening.value()+unit.inch(0.58)),3)) + '"')    
                                else:
                                    row.prop(self,'Opening_' + str(i) + '_Height',text="")
                            else:
                                row.prop(opening,'DistanceValue',text="")
                                
                        if setback:
                            row = box.row()
                            row.label("Shelf " + str(i) + " Setback")
                            row.prop(setback,'DistanceValue',text="")
                
                remove_bottom_shelf=self.assembly.get_prompt('Remove Bottom Shelf')
                remove_bottom_shelf.draw_prompt(box)
                            
                
                        
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

class OPS_Vertical_Splitters_Drop(bpy.types.Operator):
    bl_idname = "closets.insert_vertical_splitters_drop"
    bl_label = "Custom drag and drop for vertical_splitters insert"

    object_name = bpy.props.StringProperty(name="Object Name")
    product_name = bpy.props.StringProperty(name="Product Name")
    category_name = bpy.props.StringProperty(name="Category Name")
    library_name = bpy.props.StringProperty(name="Library Name")

    insert = None
    default_z_loc = 0.0
    default_height = 0.0
    default_depth = 0.0
    
    openings = []
    objects = []
    
    header_text = "Place Insert   (Esc, Right Click) = Cancel Command  :  (Left Click) = Place Insert"
    
    def execute(self, context):
        return {'FINISHED'}

    def __del__(self):
        bpy.context.area.header_text_set()

    def set_wire_and_xray(self, obj, turn_on):
        if turn_on:
            obj.draw_type = 'WIRE'
        else:
            obj.draw_type = 'TEXTURED'
        obj.show_x_ray = turn_on
        for child in obj.children:
            self.set_wire_and_xray(child,turn_on)

    def get_insert(self,context):
        bpy.ops.object.select_all(action='DESELECT')
        
        if self.object_name in bpy.data.objects:
            bp = bpy.data.objects[self.object_name]
            self.insert = fd_types.Assembly(bp)
        
        if not self.insert:
            lib = context.window_manager.cabinetlib.lib_inserts[self.library_name]
            blend_path = os.path.join(lib.lib_path,self.category_name,self.product_name + ".blend")
            obj_bp = None

            if os.path.exists(blend_path):
                obj_bp = utils.get_group(blend_path)
                self.insert = fd_types.Assembly(obj_bp)
            else:
                self.insert = utils.get_insert_class(context,self.library_name,self.category_name,self.product_name)
    
            if obj_bp:
                pass
            #TODO: SET UP UPDATE OPERATOR
                    # self.insert.update(obj_bp)
            else:
                self.insert.draw()
                self.insert.update()
            
        self.show_openings()
        utils.init_objects(self.insert.obj_bp)
        self.default_z_loc = self.insert.obj_bp.location.z
        self.default_height = self.insert.obj_z.location.z
        self.default_depth = self.insert.obj_y.location.y

    def invoke(self,context,event):
        self.insert = None
        context.window.cursor_set('WAIT')
        self.get_insert(context)
        self.set_wire_and_xray(self.insert.obj_bp, True)
        if self.insert is None:
            bpy.ops.fd_general.error('INVOKE_DEFAULT',message="Could Not Find Insert Class: " + "\\" + self.library_name + "\\" + self.category_name + "\\" + self.product_name)
            return {'CANCELLED'}
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.insert:
            utils.delete_object_and_children(self.insert.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def show_openings(self):
        #Clear  to avoid old/duplicate openings
        self.objects.clear()        
        insert_type = self.insert.obj_bp.mv.placement_type
        for obj in  bpy.context.scene.objects:
            #Check to avoid opening that is part of the dropped insert
            if utils.get_parent_assembly_bp(obj) == self.insert.obj_bp:
                continue

            if obj.layers[0]: #Make sure wall is not hidden
                opening = None
                if obj.mv.type_group == 'OPENING':
                    if insert_type in {'INTERIOR','SPLITTER'}:
                        opening = fd_types.Assembly(obj) if obj.mv.interior_open else None
                    if insert_type == 'EXTERIOR':
                        opening = fd_types.Assembly(obj) if obj.mv.exterior_open else None
                    if opening:
                        cage = opening.get_cage()
                        opening.obj_x.hide = True
                        opening.obj_y.hide = True
                        opening.obj_z.hide = True
                        cage.hide_select = False
                        cage.hide = False
                        self.objects.append(cage)

    def selected_opening(self,selected_obj):
        if selected_obj:
            opening = fd_types.Assembly(selected_obj.parent)
            if opening.obj_bp.parent:
                if self.insert.obj_bp.parent is not opening.obj_bp.parent:
                    self.insert.obj_bp.parent = opening.obj_bp.parent
                    self.insert.obj_bp.location = opening.obj_bp.location
                    self.insert.obj_bp.rotation_euler = opening.obj_bp.rotation_euler
                    self.insert.obj_x.location.x = opening.obj_x.location.x
                    self.insert.obj_y.location.y = opening.obj_y.location.y
                    self.insert.obj_z.location.z = opening.obj_z.location.z
                    utils.run_calculators(self.insert.obj_bp)
                    return opening
            
    def set_opening_name(self,obj,name):
        obj.mv.opening_name = name
        for child in obj.children:
            if child.mv.type_group != 'OPENING':
                self.set_opening_name(child, name)
        
    def place_insert(self,opening):
        if self.insert.obj_bp.mv.placement_type == 'INTERIOR':
            opening.obj_bp.mv.interior_open = False
        if self.insert.obj_bp.mv.placement_type == 'EXTERIOR':
            opening.obj_bp.mv.exterior_open = False
        if self.insert.obj_bp.mv.placement_type == 'SPLITTER':
            opening.obj_bp.mv.interior_open = False
            opening.obj_bp.mv.exterior_open = False

        utils.copy_assembly_drivers(opening,self.insert)
        self.set_opening_name(self.insert.obj_bp, opening.obj_bp.mv.opening_name)
        self.set_wire_and_xray(self.insert.obj_bp, False)
        
        for obj in self.objects:
            obj.hide = True
            obj.hide_render = True
            obj.hide_select = True

    def insert_drop(self,context,event):
        if len(self.objects) == 0:
            bpy.ops.fd_general.error('INVOKE_DEFAULT',message="There are no openings in this scene.")
            return self.cancel_drop(context,event)
        else:
            selected_point, selected_obj = utils.get_selection_point(context,event,objects=self.objects)
            bpy.ops.object.select_all(action='DESELECT')
            selected_opening = self.selected_opening(selected_obj)
            if selected_opening:
                selected_obj.select = True
                for child in self.insert.obj_bp.children:
                    if child.mv.type_group == 'OPENING':
                        if int(child.mv.opening_name) >= 7:
                           child.mv.interior_open = False
                           child.mv.exterior_open = False             
                for i in range(1,6):
                    hole_count = math.ceil((selected_opening.obj_z.location.z*1000)/32)
                    holes_per_shelf = round(hole_count/6)  
                    remainder = hole_count - (holes_per_shelf * 5)       
                    shelf = self.insert.get_prompt("Opening " + str(i) + " Height")
                    if shelf:
                        if(i <= remainder):
                            holes_per_shelf = holes_per_shelf + 1
                        if(holes_per_shelf >=3):
                            shelf.set_value(float(common_lists.OPENING_HEIGHTS[holes_per_shelf-3][0])/1000) 
                        else:
                            shelf.set_value(float(common_lists.OPENING_HEIGHTS[0][0])/1000)
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.place_insert(selected_opening)
                    context.scene.objects.active = self.insert.obj_bp
                    closet_obj = None
                    closet_assembly = None
                    opening_width = None

                    closet_obj = utils.get_parent_assembly_bp(self.insert.obj_bp)
                    if closet_obj.lm_closets.is_closet:
                        closet_assembly = fd_types.Assembly(closet_obj)

                    if closet_assembly:
                        width = closet_assembly.get_prompt("Opening " + self.insert.obj_bp.mv.opening_name + " Width")
                        if(width):
                            opening_width = width.value()

                    # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
                    utils.run_calculators(self.insert.obj_bp)
                    utils.run_calculators(self.insert.obj_bp)
                    # TOP LEVEL PRODUCT RECAL
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))

                    bpy.context.window.cursor_set('DEFAULT')
                    
                    return {'FINISHED'}

            return {'RUNNING_MODAL'}

    def modal(self, context, event):
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC','RIGHTMOUSE'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.insert_drop(context,event)
                    
bpy.utils.register_class(PROMPTS_Vertical_Splitter_Prompts)                
bpy.utils.register_class(PROMPTS_Horizontal_Splitter_Prompts)   
bpy.utils.register_class(OPS_Vertical_Splitters_Drop)  