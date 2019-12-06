import bpy
from os import path
from mv import unit, fd_types, utils
from . import mv_closet_defaults as props_closet
from . import common_prompts
from . import common_parts

HAMPER_HEIGHTS = [
    ('588.95', '19H', '19H'),
    ('620.95', '20H', '20H'),
    ('652.95', '21H', '21H'),
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
        self.add_prompt(name="Remove Locking Shelf",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Hamper Height",prompt_type='DISTANCE',value=unit.millimeter(588.95),tab_index=0)
        
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
        Remove_Locking_Shelf = self.get_var("Remove Locking Shelf")
        Hamper_Height = self.get_var("Hamper Height")
        Hamper_Type = self.get_var("Hamper Type")

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
        front.x_loc('-Left_Overlay',[Left_Overlay])
        front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-IF(Tilt_Out_Hamper,0,Depth*Open)',[Door_to_Cabinet_Gap,Inset_Front,Front_Thickness,Tilt_Out_Hamper,Depth,Open])
        front.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        front.x_rot(value = 0)
        front.y_rot('IF(Tilt_Out_Hamper,radians(-90)-(Open*.325),radians(-90))',[Tilt_Out_Hamper,Open])
        front.z_rot(value = 90)
        front.x_dim('Hamper_Height+Top_Overlay+Bottom_Overlay',[Hamper_Height,Top_Overlay,Bottom_Overlay])
        front.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
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
        basket_2.x_rot('IF(Tilt_Out_Hamper,Open*.5,0)',[Open,Tilt_Out_Hamper])
        basket_2.y_rot(value = 0)
        basket_2.x_dim(value = unit.inch(18.0))
        basket_2.y_dim(value = unit.inch(12.0625))
        basket_2.z_dim(value = unit.inch(WIRE_BASKET_HEIGHT))
        basket_2.prompt('Hide','IF(AND(Width>=INCH(18.0),Width<INCH(24.0),Hamper_Type==1),False,True)',[Hamper_Type,Width])
        
        basket_3 = common_parts.add_double_canvas_hamper(self)
        basket_3.x_loc('(Width-INCH(24.0))/2',[Width])
        basket_3.y_loc('-IF(Tilt_Out_Hamper,0,Depth*Open)',[Tilt_Out_Hamper,Depth,Open])
        basket_3.z_loc(value = 0)
        basket_3.x_rot('IF(Tilt_Out_Hamper,Open*.5,0)',[Open,Tilt_Out_Hamper])
        basket_3.y_rot(value = 0)
        basket_3.z_rot(value = 0)
        basket_3.x_dim(value = unit.inch(24.0))
        basket_3.y_dim(value = unit.inch(12.0625))
        basket_3.z_dim(value = unit.inch(WIRE_BASKET_HEIGHT))
        basket_3.prompt('Hide','IF(AND(Width>=INCH(24.0),Hamper_Type==1),False,True)',[Hamper_Type,Width])     
        
        top_shelf = common_parts.add_shelf(self)
        top_shelf.x_loc(value = 0)
        top_shelf.y_loc('Depth',[Depth])
        top_shelf.z_loc('Hamper_Height+Shelf_Thickness',[Hamper_Height,Shelf_Thickness])
        top_shelf.x_rot(value = 0)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 0)
        top_shelf.x_dim('Width',[Width])
        top_shelf.y_dim('-Depth',[Depth])
        top_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.prompt('Hide','IF(Remove_Locking_Shelf,True,False)',[Remove_Locking_Shelf])
        top_shelf.prompt('Is Locked Shelf',value = True)
        
        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.x_loc(value = 0)
        bottom_shelf.y_loc('Depth',[Depth])
        bottom_shelf.z_loc('0',[Hamper_Height,Shelf_Thickness])
        bottom_shelf.x_rot(value = 0)
        bottom_shelf.y_rot(value = 0)
        bottom_shelf.z_rot(value = 0)
        bottom_shelf.x_dim('Width',[Width])
        bottom_shelf.y_dim('-Depth',[Depth])
        bottom_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        bottom_shelf.prompt('Hide','IF(Remove_Locking_Shelf,True,False)',[Remove_Locking_Shelf])
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
                                           items=HAMPER_HEIGHTS,
                                           default = '588.95')    

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
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True

    def set_properties_from_prompts(self):
        props = props_closet.get_scene_props()

        self.hamper_height_prompt = self.assembly.get_prompt("Hamper Height")
        
        if self.hamper_height_prompt and props.closet_defaults.use_32mm_system:
            value = round(self.hamper_height_prompt.value() * 1000,2)

            for index, t_height in enumerate(HAMPER_HEIGHTS):
                if not value >= float(t_height[0]):
                    if index == 0:
                        self.hamper_height = HAMPER_HEIGHTS[0][0]
                    else:
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
                    
bpy.utils.register_class(PROMPTS_Hamper_Prompts)
