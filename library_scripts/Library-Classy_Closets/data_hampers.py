import bpy
from os import path
from mv import unit, fd_types, utils
from . import mv_closet_defaults as props_closet
from . import common_prompts
from . import common_parts

HAMPER_HEIGHTS = [
    ('589.280','19H-23.78"','19H-23.78"'),
    ('621.284','20H-25.04"','20H-25.04"'),
    ('653.288','21H-26.30"','21H-26.30"')
]

WIRE_BASKET_HEIGHT = 19.0

class Hamper(fd_types.Assembly):

    placement_type = "SPLITTER"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".hampers_prompts"
    type_assembly = "INSERT"
    mirror_y = False
    
    upper_interior = None
    upper_exterior = None
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_hamper_insert_bp = True
        
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_drawer_pull_prompts(self)
        
        self.add_tab(name='Hamper Options',tab_type='VISIBLE')
        self.add_prompt(name="Tilt Out Hamper",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Hamper Type",prompt_type='COMBOBOX',items=['Wire','Canvas'],value=0,tab_index=0)
        self.add_prompt(name="Remove Bottom Shelf",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Remove Top Shelf",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Hamper Height",prompt_type='DISTANCE',value=unit.millimeter(589.280),tab_index=0)
        self.add_prompt(name="Hamper Backing Gap",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Cleat Location", prompt_type='COMBOBOX', items=["Above", "Below", "None"], value=0, tab_index=0, columns=3)
        self.add_prompt(name="Cleat Height",prompt_type='DISTANCE',value=unit.inch(3.64),tab_index=0)
        self.add_prompt(name="Shelf Backing Setback",prompt_type='DISTANCE',value=0,tab_index=0)

        self.add_prompt(name="Full Overlay",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Front_Thickness = self.get_var("Front Thickness")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Open = self.get_var("Open")
        Inset_Front = self.get_var("Inset Front")
        Tilt_Out_Hamper = self.get_var("Tilt Out Hamper")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Remove_Bottom_Shelf = self.get_var("Remove Bottom Shelf")
        Remove_Top_Shelf = self.get_var("Remove Top Shelf")
        Hamper_Height = self.get_var("Hamper Height")
        Hamper_Type = self.get_var("Hamper Type")
        Cleat_Location = self.get_var("Cleat Location")
        Cleat_Height = self.get_var("Cleat Height")
        Shelf_Backing_Setback = self.get_var("Shelf Backing Setback")

        Full_Overlay = self.get_var("Full Overlay")
        SDFOD = self.get_var("Single Door Full Overlay Difference", 'SDFOD')

        self.prompt('Hamper Backing Gap', 'Hamper_Height+(Shelf_Thickness*2)', [Hamper_Height,Shelf_Thickness])        

        #PULL OUT WIDTH ERROR DIM
        dim_x = fd_types.Dimension()
        dim_x.parent(self.obj_bp)
        dim_x.start_z(value = 0)
        dim_x.start_x(value = 0)
        dim_x.end_x('Width',[Width])
        dim_x.anchor.cabinetlib.glfontx = unit.inch(20)
        dim_x.hide('IF(Width<INCH(17.99),False,True)',[Width])
        dim_x.set_color(value = 3)
        dim_x.set_label('Hamper Min Width (18")',new_line=True)
        
        #DEPTH ERROR DIM
        dim_y = fd_types.Dimension()
        dim_y.parent(self.obj_bp)
        dim_y.start_z(value=unit.inch(10))
        dim_y.start_x('Width/2',[Width])
        dim_y.end_y('Depth',[Depth])
        dim_y.anchor.cabinetlib.glfontx = unit.inch(20)
        dim_y.hide('IF(fabs(Depth)<INCH(15.99),False,True)',[Depth])
        dim_y.set_color(value = 3)
        dim_y.set_label('Hamper Min Depth (16")',new_line=True)

        front = common_parts.add_hamper_front(self)
        front.x_loc('IF(Full_Overlay,-Left_Overlay*2,-Left_Overlay)',[Left_Overlay,Full_Overlay])
        front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-IF(Tilt_Out_Hamper,0,Depth*Open)',[Door_to_Cabinet_Gap,Inset_Front,Front_Thickness,Tilt_Out_Hamper,Depth,Open])
        front.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        front.x_rot(value = 0)
        front.y_rot('IF(Tilt_Out_Hamper,radians(-90)-(Open*.325),radians(-90))',[Tilt_Out_Hamper,Open])
        front.z_rot(value = 90)
        front.x_dim('Hamper_Height+Top_Overlay+Bottom_Overlay',[Hamper_Height,Top_Overlay,Bottom_Overlay])
        front.y_dim('IF(Full_Overlay,(Width+(Shelf_Thickness*2)-SDFOD),(Width+Left_Overlay+Right_Overlay))*-1',[Width,Left_Overlay,Right_Overlay,Full_Overlay,SDFOD,Shelf_Thickness])
        front.z_dim('Front_Thickness',[Front_Thickness])

        pull = common_parts.add_drawer_pull(self)
        pull.set_name("Hamper Drawer Pull")
        pull.x_loc('-Left_Overlay',[Left_Overlay])
        pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-IF(Tilt_Out_Hamper,0,Depth*Open)',[Door_to_Cabinet_Gap,Inset_Front,Front_Thickness,Tilt_Out_Hamper,Depth,Open])
        pull.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        pull.x_rot('IF(Tilt_Out_Hamper,radians(90)+(Open*.325),radians(90))',[Tilt_Out_Hamper,Open])
        pull.y_rot(value = 0)
        pull.z_rot(value = 0)
        pull.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
        pull.y_dim('Hamper_Height+Top_Overlay+Bottom_Overlay',[Hamper_Height,Top_Overlay,Bottom_Overlay])
        pull.z_dim('Front_Thickness',[Front_Thickness])
        pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,Hamper_Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Hamper_Height,Drawer_Pull_From_Top])
        pull.prompt("Pull Z Location",'(Width/2)+Right_Overlay',[Width,Right_Overlay])

        basket_1 = common_parts.add_wire_hamper(self)
        basket_1.x_loc('IF(Width<=INCH(23.99),Width-INCH(18),Width-INCH(24))/2',[Width])
        basket_1.y_loc('-IF(Tilt_Out_Hamper,0,Depth*Open)',[Tilt_Out_Hamper,Depth,Open])
        basket_1.z_loc(value = 0)
        basket_1.x_rot('IF(Tilt_Out_Hamper,Open*.325,0)',[Open,Tilt_Out_Hamper])
        basket_1.y_rot(value = 0)
        basket_1.z_rot(value = 0)
        basket_1.x_dim('IF(Width<=INCH(23.99),INCH(18),INCH(24))',[Width])
        basket_1.y_dim('IF(Depth<=INCH(15.99),INCH(14),INCH(16))',[Depth])
        basket_1.z_dim(value = unit.inch(WIRE_BASKET_HEIGHT))
        basket_1.prompt('Hide','IF(Hamper_Type==0,False,True)',[Hamper_Type])
        
        basket_2 = common_parts.add_single_canvas_hamper(self)
        basket_2.x_loc('(Width-INCH(18.0))/2',[Width])
        basket_2.y_loc('-IF(Tilt_Out_Hamper,0,Depth*Open)',[Tilt_Out_Hamper,Depth,Open])
        basket_2.z_loc(value = 0)
        basket_2.x_rot('IF(Tilt_Out_Hamper,Open*.325,0)',[Open,Tilt_Out_Hamper])
        basket_2.y_rot(value = 0)
        basket_2.x_dim(value = unit.inch(18.0))
        basket_2.y_dim(value = unit.inch(12.0625))
        basket_2.z_dim(value = unit.inch(WIRE_BASKET_HEIGHT))
        basket_2.prompt('Hide','IF(AND(Width>=INCH(18.0),Width<INCH(24.0),Hamper_Type==1),False,True)',[Hamper_Type,Width])
        
        basket_3 = common_parts.add_double_canvas_hamper(self)
        basket_3.x_loc('(Width-INCH(24.0))/2',[Width])
        basket_3.y_loc('-IF(Tilt_Out_Hamper,0,Depth*Open)',[Tilt_Out_Hamper,Depth,Open])
        basket_3.z_loc(value = 0)
        basket_3.x_rot('IF(Tilt_Out_Hamper,Open*.325,0)',[Open,Tilt_Out_Hamper])
        basket_3.y_rot(value = 0)
        basket_3.z_rot(value = 0)
        basket_3.x_dim(value = unit.inch(24.0))
        basket_3.y_dim(value = unit.inch(12.0625))
        basket_3.z_dim(value = unit.inch(WIRE_BASKET_HEIGHT))
        basket_3.prompt('Hide','IF(AND(Width>=INCH(24.0),Hamper_Type==1),False,True)',[Hamper_Type,Width])     
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Bottom Cleat")
        cleat.x_loc(value = 0)
        cleat.y_loc('Depth',[Depth])
        cleat.z_loc('Hamper_Height+IF(Cleat_Location==0,Shelf_Thickness,0)',[Hamper_Height,Cleat_Location,Shelf_Thickness])
        cleat.x_rot(value=-90)
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0) 
        cleat.x_dim('Width',[Width])
        cleat.y_dim('IF(Cleat_Location==0,-Cleat_Height,Cleat_Height)', [Cleat_Height, Cleat_Location])
        cleat.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        cleat.prompt("Hide", "IF(Cleat_Location==2,True,False)", [Cleat_Location])
        cleat.prompt('Use Cleat Cover', 'IF(Cleat_Location==0,True,False)', [Cleat_Location])  

        top_shelf = common_parts.add_shelf(self)
        top_shelf.x_loc(value = 0)
        top_shelf.y_loc('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        top_shelf.z_loc('Hamper_Height+Shelf_Thickness',[Hamper_Height,Shelf_Thickness])
        top_shelf.x_rot(value = 0)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 0)
        top_shelf.x_dim('Width',[Width])
        top_shelf.y_dim('-Depth+Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        top_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.prompt('Hide','IF(Remove_Top_Shelf,True,False)',[Remove_Top_Shelf])
        top_shelf.prompt('Is Locked Shelf',value = True)
        
        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.x_loc(value = 0)
        bottom_shelf.y_loc('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        bottom_shelf.z_loc('0',[Hamper_Height,Shelf_Thickness])
        bottom_shelf.x_rot(value = 0)
        bottom_shelf.y_rot(value = 0)
        bottom_shelf.z_rot(value = 0)
        bottom_shelf.x_dim('Width',[Width])
        bottom_shelf.y_dim('-Depth+Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        bottom_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        bottom_shelf.prompt('Hide','IF(Remove_Bottom_Shelf,True,False)',[Remove_Bottom_Shelf])
        bottom_shelf.prompt('Is Locked Shelf',value = True)
        
        opening = common_parts.add_opening(self)
        opening.x_loc(value = 0)
        opening.y_loc(value = 0)
        opening.z_loc('Hamper_Height+Shelf_Thickness',[Hamper_Height,Shelf_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('Width',[Width])
        opening.y_dim('Depth',[Depth])
        opening.z_dim('Height-Hamper_Height-Shelf_Thickness',[Height,Hamper_Height,Shelf_Thickness])            
        
        if self.upper_exterior:
            opening.obj_bp.mv.exterior_open = False
            
            self.upper_exterior.draw()
            self.upper_exterior.obj_bp.parent = self.obj_bp
            self.upper_exterior.x_loc(value = 0)
            self.upper_exterior.y_loc(value = 0)
            self.upper_exterior.z_loc('Hamper_Height+Shelf_Thickness',[Hamper_Height,Shelf_Thickness])
            self.upper_exterior.x_rot(value = 0)
            self.upper_exterior.y_rot(value = 0)
            self.upper_exterior.z_rot(value = 0)
            self.upper_exterior.x_dim('Width',[Width])
            self.upper_exterior.y_dim('Depth',[Depth])
            self.upper_exterior.z_dim('Height-Hamper_Height-Shelf_Thickness',[Height,Hamper_Height,Shelf_Thickness])            
        
        if self.upper_interior:
            opening.obj_bp.mv.interior_open = False
            
            self.upper_interior.draw()
            self.upper_interior.obj_bp.parent = self.obj_bp
            self.upper_interior.x_loc(value = 0)
            self.upper_interior.y_loc(value = 0)
            self.upper_interior.z_loc('Hamper_Height+Shelf_Thickness',[Hamper_Height,Shelf_Thickness])
            self.upper_interior.x_rot(value = 0)
            self.upper_interior.y_rot(value = 0)
            self.upper_interior.z_rot(value = 0)
            self.upper_interior.x_dim('Width',[Width])
            self.upper_interior.y_dim('Depth',[Depth])
            self.upper_interior.z_dim('Height-Hamper_Height-Shelf_Thickness',[Height,Hamper_Height,Shelf_Thickness])               
            
        self.update()
        
class PROMPTS_Hamper_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".hampers_prompts"
    bl_label = "Hamper Options" 
    bl_description = "This shows all of the available hamper options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None

    hamper_height = bpy.props.EnumProperty(name="Hamper Face Height",
                                           items=HAMPER_HEIGHTS)    

    hamper_height_prompt = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def check(self, context):
        props = props_closet.get_scene_props()
            
        if self.hamper_height_prompt and props.closet_defaults.use_32mm_system:
            self.hamper_height_prompt.set_value(unit.inch(float(self.hamper_height) / 25.4))

        utils.run_calculators(self.assembly.obj_bp)
        utils.run_calculators(self.assembly.obj_bp.parent)# Recalc top level assembly for backing that relies on this insert height
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True

    def set_properties_from_prompts(self):
        props = props_closet.get_scene_props()

        self.hamper_height_prompt = self.assembly.get_prompt("Hamper Height")
        
        if self.hamper_height_prompt and props.closet_defaults.use_32mm_system:
            value = round(self.hamper_height_prompt.value() * 1000,3)

            for index, t_height in enumerate(HAMPER_HEIGHTS):
                if not value >= float(t_height[0]):
                    self.hamper_height = HAMPER_HEIGHTS[index-1][0]
                    break
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=380)
    
    def draw(self, context):
        props = props_closet.get_scene_props()
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                open_drawer = self.assembly.get_prompt('Open')
                tilt_out_hamper = self.assembly.get_prompt('Tilt Out Hamper')
                hamper_type = self.assembly.get_prompt('Hamper Type')
                cleat_loc = self.assembly.get_prompt("Cleat Location")
                full_overlay = self.assembly.get_prompt("Full Overlay")

                box = layout.box()
                row = box.row()
                row.prop(open_drawer,'PercentageValue',text="Open")
                row = box.row()
                hamper_type.draw_prompt(row)
                row = box.row()

                if props.closet_defaults.use_32mm_system:  
                    row.prop(self,'hamper_height') 
                else:
                    self.hamper_height_prompt.draw_prompt(row)

                row = box.row()
                if tilt_out_hamper:
                    tilt_out_hamper.draw_prompt(row)

                row = box.row()
                if(full_overlay):
                    full_overlay.draw_prompt(row) 

                row = box.row()
                if cleat_loc:
                    cleat_loc.draw_prompt(row, text="Cleat Location")


class OPS_Hamper_Drop(bpy.types.Operator):
    bl_idname = "closets.insert_hamper_drop"
    bl_label = "Custom drag and drop for hamper insert"

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
    
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.place_insert(selected_opening)
                    self.set_backing_bottom_gap(self.insert.obj_bp, selected_opening)
                    self.set_bottom_KD(self.insert.obj_bp, selected_opening)
                    context.scene.objects.active = self.insert.obj_bp
                    # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
                    utils.run_calculators(self.insert.obj_bp)
                    utils.run_calculators(self.insert.obj_bp)
                    # TOP LEVEL PRODUCT RECAL
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))

                    bpy.context.window.cursor_set('DEFAULT')
                    
                    return {'FINISHED'}

            return {'RUNNING_MODAL'}

    def set_backing_bottom_gap(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.mv.opening_name
        carcass_bp = utils.get_parent_assembly_bp(insert_bp)
        hamper_assembly = fd_types.Assembly(insert_bp)        
        Hamper_Backing_Gap = hamper_assembly.get_var('Hamper Backing Gap')

        for child in carcass_bp.children:
            if child.lm_closets.is_back_bp:
                if child.mv.opening_name == opening_name:
                    back_assembly = fd_types.Assembly(child)
                    bottom_insert_backing = back_assembly.get_prompt('Bottom Insert Backing')

                    if bottom_insert_backing:
                        back_assembly.prompt('Bottom Insert Backing', 'Hamper_Backing_Gap', [Hamper_Backing_Gap])
    
    def set_bottom_KD(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.mv.opening_name
        carcass_bp = utils.get_parent_assembly_bp(insert_bp)
        drawer_assembly = fd_types.Assembly(insert_bp)   
        carcass_assembly = fd_types.Assembly(carcass_bp)
        if(carcass_assembly.get_prompt("Opening " + str(opening_name) + " Floor Mounted") and carcass_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(opening_name))):
            if(carcass_assembly.get_prompt("Opening " + str(opening_name) + " Floor Mounted").value() or carcass_assembly.get_prompt('Remove Bottom Hanging Shelf ' + str(opening_name)).value()):
                drawer_assembly.get_prompt("Remove Bottom Shelf").set_value(True)


    def modal(self, context, event):
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC','RIGHTMOUSE'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.insert_drop(context,event)
           
bpy.utils.register_class(PROMPTS_Hamper_Prompts)
bpy.utils.register_class(OPS_Hamper_Drop)
