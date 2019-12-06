import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts

class Deco_Filler(fd_types.Assembly):

    placement_type = "INTERIOR"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".deco_fillers"
    type_assembly = "INSERT"
    mirror_y = False
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        self.add_tab("Flute Panel Options", 'VISIBLE')
        self.add_prompt(name="Panel Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        self.add_prompt(name="Add Top Rosette",prompt_type='CHECKBOX',value=True)
        self.add_prompt(name="Add Bottom Rosette",prompt_type='CHECKBOX',value=True)
        self.add_prompt(name="Rosette Size",prompt_type='DISTANCE',value=unit.inch(3.5))
        
        Width = self.get_var('dim_x', "Width")
        Height = self.get_var('dim_z', "Height")
        Depth = self.get_var('dim_y', "Depth")
        Panel_Thickness = self.get_var("Panel Thickness")
        Add_Top_Rosette = self.get_var("Add Top Rosette")
        Add_Bottom_Rosette = self.get_var("Add Bottom Rosette")
        Rosette_Size = self.get_var("Rosette Size")

        front_filler = common_parts.add_filler(self)
        front_filler.x_loc(value = 0)
        front_filler.y_loc(value = 0)
        front_filler.z_loc(value = 0)
        front_filler.x_rot(value = 0)
        front_filler.y_rot(value = -90)
        front_filler.z_rot(value = -90)
        front_filler.x_dim("Height",[Height])
        front_filler.y_dim("Width",[Width])
        front_filler.z_dim("Panel_Thickness",[Panel_Thickness])
        
        rear_filler = common_parts.add_filler(self)
        rear_filler.x_loc(value = 0)
        rear_filler.y_loc('Depth',[Depth])
        rear_filler.z_loc(value = 0)
        rear_filler.x_rot(value = 0)
        rear_filler.y_rot(value = -90)
        rear_filler.z_rot(value = -90)
        rear_filler.x_dim("Height",[Height])
        rear_filler.y_dim("Width",[Width])
        rear_filler.z_dim("-Panel_Thickness",[Panel_Thickness])
        
        flute = common_parts.add_fluted_molding(self)
        flute.x_loc(value = unit.inch(3.25))
        flute.y_loc(value = 0)
        flute.z_loc('IF(Add_Bottom_Rosette,Rosette_Size,0)',[Add_Bottom_Rosette,Rosette_Size])
        flute.x_rot(value = 0)
        flute.y_rot(value = -90)
        flute.z_rot(value = 90)
        flute.x_dim("Height-IF(Add_Bottom_Rosette,Rosette_Size,0)-IF(Add_Top_Rosette,Rosette_Size,0)",[Height,Rosette_Size,Add_Bottom_Rosette,Add_Top_Rosette])
        flute.y_dim("Width",[Width])
        flute.z_dim("Panel_Thickness",[Panel_Thickness])

        top_rosette = common_parts.add_rosette(self)
        top_rosette.x_loc(value = unit.inch(-.25))
        top_rosette.z_loc('Height-Rosette_Size',[Height,Rosette_Size])
        top_rosette.x_rot(value = 90)
        top_rosette.hide('IF(Add_Top_Rosette,False,True)',[Add_Top_Rosette])

        bottom_rosette = common_parts.add_rosette(self)
        bottom_rosette.x_loc(value = unit.inch(-.25))
        bottom_rosette.x_rot(value = 90)
        bottom_rosette.hide('IF(Add_Bottom_Rosette,False,True)',[Add_Bottom_Rosette])

        self.update()

class PROMPTS_Deco_Fillers(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".deco_fillers"
    bl_label = "Deco Fillers Prompts" 
    bl_description = "This shows all of the available fluted molding options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(330))
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                add_top_rosette = self.assembly.get_prompt("Add Top Rosette")
                add_bottom_rosette = self.assembly.get_prompt("Add Bottom Rosette")
                
                if add_top_rosette:
                    add_top_rosette.draw_prompt(layout)
                    
                if add_bottom_rosette:
                    add_bottom_rosette.draw_prompt(layout)
                
bpy.utils.register_class(PROMPTS_Deco_Fillers)    
