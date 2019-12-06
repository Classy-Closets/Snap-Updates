import bpy
import math
from os import path
from mv import unit, fd_types, utils
from . import mv_closet_defaults as props_closet
from . import common_prompts
from . import common_parts

IRONING_BOARD_HEIGHTS = [('157','6 1/4"','6 1/4"'),
                         ('189','7 1/2"','7 1/2"'),
                         ('221','8 3/4"','8 3/4"'),
                         ('253','10"','10"')]

class Ironing_Board(fd_types.Assembly):

    placement_type = "SPLITTER"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".ironing_boards"
    type_assembly = "INSERT"
    mirror_y = False
    
    def draw (self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_drawer_pull_prompts(self)
        
        self.add_tab(name='Ironing Board Options',tab_type='VISIBLE')
        self.add_tab(name='Ironing Board Values',tab_type='HIDDEN')
        
        self.add_prompt(name="Ironing Board Type",prompt_type='COMBOBOX',items=['DOOR','DRAWER'],value=0,tab_index=0)
        self.add_prompt(name="Shelf Height",prompt_type='DISTANCE',value=unit.millimeter(157),tab_index=1) 
        self.add_prompt(name="Ironing Board Offset",prompt_type='DISTANCE',value=unit.inch(22),tab_index=1)
        self.add_prompt(name="Door Rotation",prompt_type='ANGLE',value=90,tab_index=0)
        
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
        Inset_Front = self.get_var("Inset Front")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Ironing_Board_Type = self.get_var("Ironing Board Type")
        Shelf_Height = self.get_var("Shelf Height")
        Ironing_Board_Offset = self.get_var("Ironing Board Offset")
        Rotation = self.get_var("Door Rotation","Rotation")
        Open = self.get_var("Open")
        Use_Double_Pulls = self.get_var("Use Double Pulls")
        No_Pulls = self.get_var("No Pulls")
        
        door = common_parts.add_ironing_board_door_front(self)
        door.x_loc('-Left_Overlay',[Left_Overlay])
        door.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-IF(Ironing_Board_Type==0,0,(Depth*Open))',[Ironing_Board_Type,Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        door.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        door.x_rot(value = 0)
        door.y_rot('radians(-90)-IF(Ironing_Board_Type==0,min(radians(Open*Rotation)*4,radians(Rotation)),0)',[Open,Rotation,Ironing_Board_Type])
        door.z_rot(value = 90)      
        door.x_dim('Shelf_Height-Shelf_Thickness+Top_Overlay+Bottom_Overlay',[Shelf_Height,Shelf_Thickness,Top_Overlay,Bottom_Overlay])
        door.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
        door.z_dim('Front_Thickness',[Front_Thickness])
        door.prompt('Door Swing','3',[])
        door.prompt('No Pulls','No_Pulls',[No_Pulls])
        door.prompt('Hide','IF(Ironing_Board_Type==0,False,True)',[Ironing_Board_Type])
        
        drawer_front = common_parts.add_drawer_front(self)
        drawer_front.x_loc('-Left_Overlay',[Left_Overlay])
        drawer_front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-IF(Ironing_Board_Type==0,0,(Depth*Open))',[Ironing_Board_Type,Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        drawer_front.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        drawer_front.x_rot(value = 0)
        drawer_front.y_rot('radians(-90)-IF(Ironing_Board_Type==0,min(radians(Open*Rotation)*4,radians(Rotation)),0)',[Open,Rotation,Ironing_Board_Type])
        drawer_front.z_rot(value = 90)      
        drawer_front.x_dim('Shelf_Height-Shelf_Thickness+Top_Overlay+Bottom_Overlay',[Shelf_Height,Shelf_Thickness,Top_Overlay,Bottom_Overlay])
        drawer_front.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
        drawer_front.z_dim('Front_Thickness',[Front_Thickness])
        drawer_front.prompt('No Pulls','No_Pulls',[No_Pulls])
        drawer_front.prompt('Use Double Pulls','Use_Double_Pulls',[Use_Double_Pulls])
        drawer_front.prompt('Center Pulls on Drawers','Center_Pulls_on_Drawers',[Center_Pulls_on_Drawers])
        drawer_front.prompt('Drawer Pull From Top','Drawer_Pull_From_Top',[Drawer_Pull_From_Top])
        drawer_front.prompt('Hide','IF(Ironing_Board_Type==1,False,True)',[Ironing_Board_Type])
        
        pull = common_parts.add_door_pull(self)
        pull.set_name("Drawer Pull")
        pull.x_loc('-Left_Overlay',[Left_Overlay])
        pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-IF(Ironing_Board_Type==0,0,(Depth*Open))',[Ironing_Board_Type,Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        pull.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        pull.x_rot(value = 0)
        pull.y_rot('radians(-90)-IF(Ironing_Board_Type==0,min(radians(Open*Rotation)*4,radians(Rotation)),0)',[Open,Rotation,Ironing_Board_Type]) 
        pull.z_rot(value = 90)
        pull.x_dim('Shelf_Height',[Shelf_Height])
        pull.y_dim('(Width+Left_Overlay+Right_Overlay)*-1',[Width,Left_Overlay,Right_Overlay])
        pull.z_dim('Front_Thickness',[Front_Thickness])        
        pull.prompt("Pull Z Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
        pull.prompt("Pull X Location",'IF(Use_Double_Pulls,(Width/4),(Width/2))+Right_Overlay',[Width,Right_Overlay,Use_Double_Pulls])
        pull.prompt("Pull Rotation",value = math.radians(90))
        
        r_pull = common_parts.add_drawer_pull(self)
        r_pull.set_name("Drawer Pull")        
        r_pull.x_loc('-Left_Overlay',[Left_Overlay])
        r_pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-IF(Ironing_Board_Type==0,0,(Depth*Open))',[Ironing_Board_Type,Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        r_pull.z_loc('-Bottom_Overlay',[Bottom_Overlay])
        r_pull.x_rot(value = 0)
        r_pull.y_rot('radians(-90)-IF(Ironing_Board_Type==0,min(radians(Open*Rotation)*4,radians(Rotation)),0)',[Open,Rotation,Ironing_Board_Type]) 
        r_pull.z_rot(value = 90)
        r_pull.x_dim('Shelf_Height',[Shelf_Height])
        r_pull.y_dim('(Right_Overlay)',[Width,Left_Overlay,Right_Overlay])
        r_pull.z_dim('Front_Thickness',[Front_Thickness])        
        r_pull.prompt("Pull Z Location",'IF(Center_Pulls_on_Drawers,Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,Height,Drawer_Pull_From_Top])
        r_pull.prompt("Pull X Location",'(Width/4)+Right_Overlay',[Width,Right_Overlay])
        r_pull.prompt("Pull Rotation",value = math.radians(90))
        r_pull.prompt('Hide','IF(Use_Double_Pulls,False,True)',[Use_Double_Pulls])        
       
        #IBF IRONING BOARD
        ironing_board_door = common_parts.add_ironing_board_door(self)
        ironing_board_door.x_loc('(Width-INCH(20))/2',[Width,Ironing_Board_Offset])
        ironing_board_door.y_loc('-Door_to_Cabinet_Gap-(Depth*Open)',[Door_to_Cabinet_Gap,Depth,Open])
        ironing_board_door.z_loc(value = 0)
        ironing_board_door.x_rot(value = 0)
        ironing_board_door.y_rot(value = 0)
        ironing_board_door.z_rot(value = 0)
        ironing_board_door.x_dim(value = unit.inch(24))
        ironing_board_door.y_dim(value = unit.inch(14))
        ironing_board_door.z_dim(value = unit.inch(4))
        ironing_board_door.prompt('Hide','IF(Ironing_Board_Type==0,False,True)',[Ironing_Board_Type])  
        
        #IB-DR IRONING BOARD
        ironing_board_drawer = common_parts.add_ironing_board_drawer(self)
        ironing_board_drawer.x_loc('(Width-IF(Width>INCH(19.9),INCH(20),INCH(14.25)))/2',[Width,Ironing_Board_Offset])
        ironing_board_drawer.y_loc('-Door_to_Cabinet_Gap-(Depth*Open)',[Door_to_Cabinet_Gap,Depth,Open])
        ironing_board_drawer.z_loc(value = 0)
        ironing_board_drawer.x_rot(value = 0)
        ironing_board_drawer.y_rot(value = 0)
        ironing_board_drawer.z_rot(value = 0)
        ironing_board_drawer.x_dim('IF(Width<=INCH(14.25),INCH(14.25),IF(Width>=INCH(20),INCH(20),INCH(14.25)))',[Width])
        ironing_board_drawer.y_dim(value = unit.inch(20))
        ironing_board_drawer.z_dim(value = unit.inch(4))
        ironing_board_drawer.prompt('Hide','IF(Ironing_Board_Type==1,False,True)',[Ironing_Board_Type])      
        
        top_shelf = common_parts.add_shelf(self)
        top_shelf.x_loc(value = 0)
        top_shelf.y_loc('Depth',[Depth])
        top_shelf.z_loc('Shelf_Height',[Shelf_Height])
        top_shelf.x_rot(value = 0)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 0)
        top_shelf.x_dim('Width',[Width])
        top_shelf.y_dim('-Depth',[Depth])
        top_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        
        opening = common_parts.add_opening(self)
        opening.set_name("Opening")
        opening.x_loc(value = 0)
        opening.y_loc(value = 0)
        opening.z_loc('Shelf_Height',[Shelf_Height,Shelf_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('Width',[Width])
        opening.y_dim('Depth',[Depth])
        opening.z_dim('Height-Shelf_Height',[Height,Shelf_Height,Shelf_Thickness])                             

        self.update()
       
class PROMPTS_Ironing_Board_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".ironing_boards"
    bl_label = "Ironing Board Prompts" 
    bl_description = "This shows all of the available ironing board options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    ironing_board_height = bpy.props.EnumProperty(name="Ironing Board Height",
                                                  items=IRONING_BOARD_HEIGHTS)       
    
    assembly = None
    
    ironing_board_height_prompt = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        props = props_closet.get_scene_props()
        
        if self.ironing_board_height_prompt and props.closet_defaults.use_32mm_system:
            self.ironing_board_height_prompt.set_value(unit.inch(float(self.ironing_board_height) / 25.4))
        utils.run_calculators(self.assembly.obj_bp)
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport        
        
    def execute(self, context):
        return {'FINISHED'}

    def set_properties_from_prompts(self):
        props = props_closet.get_scene_props()
        
        self.ironing_board_height_prompt = self.assembly.get_prompt("Shelf Height")   
        
        if self.ironing_board_height_prompt and props.closet_defaults.use_32mm_system:
            value = round(self.ironing_board_height_prompt.value() * 1000,2)
            
            for index, t_height in enumerate(IRONING_BOARD_HEIGHTS):
                if not value >= float(t_height[0]):
                    if index == 0:
                        self.ironing_board_height = IRONING_BOARD_HEIGHTS[0][0]
                        
                    else:
                        self.ironing_board_height = IRONING_BOARD_HEIGHTS[index-1][0]
                    break
                if index == len(IRONING_BOARD_HEIGHTS) - 1:
                    self.ironing_board_height = IRONING_BOARD_HEIGHTS[-1][0]

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=380)
    
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                props = props_closet.get_scene_props()
                
                Ironing_Board_Type = self.assembly.get_prompt("Ironing Board Type")
                Use_Double_Pulls = self.assembly.get_prompt("Use Double Pulls")
                open_drawer = self.assembly.get_prompt('Open')
                
                box = layout.box()
                row = box.row()
                row.prop(open_drawer,'PercentageValue',text="Open")                
                row = box.row()
                
                if props.closet_defaults.use_32mm_system:  
                    row.prop(self,'ironing_board_height')     
                else:
                    self.ironing_board_height_prompt.draw_prompt(row)        
                row = box.row()
                Ironing_Board_Type.draw_prompt(row)
                row = box.row()
                Use_Double_Pulls.draw_prompt(row)

bpy.utils.register_class(PROMPTS_Ironing_Board_Prompts)